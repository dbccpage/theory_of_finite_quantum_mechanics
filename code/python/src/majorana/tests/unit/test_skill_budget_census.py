"""The Budget Ceiling Invariant, measured against the whole garden.

`EPIC-OE-OEWAS-006` declares: "Skills must not exceed 300 lines or 20KB without
explicit governance waiver." A gate for it exists and passes.

It passes because it scans five skills out of 110, and **all seven breaches are
among the 105 it never looks at**. These tests pin that state: the coverage
ratio, the fact that no breach is visible to the gate, and a shrink-only ratchet
so the seven cannot become eight while nobody is watching.

The breaches are not repaired here. Rewriting `techne-sprint-planning` -- 1163
lines, 3.9x the ceiling -- is a content decision for the humans who own it, not
a side effect of adding a check.
"""

from __future__ import annotations

import ast
import json
import pathlib
import subprocess
import sys

import pytest

from omega_engine_workflows_agents_skills.infrastructure.skill_budget_census import (
    BASELINE_SCHEMA,
    GATE_SOURCE,
    SKILL_ROOT,
    CensusError,
    GardenCensus,
    GateTerms,
    SkillMeasurement,
    format_report,
    load_baseline,
    measure_garden,
    ratchet_violations,
    read_gate_terms,
    render_baseline,
    take_census,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
BASELINE_PATH = (
    REPO_ROOT
    / "omega_engine_workflows_agents_skills"
    / "manifests"
    / "skill_budget_baseline.json"
)

EPIC_MAX_LINES = 300
EPIC_MAX_BYTES = 20 * 1024


@pytest.fixture(scope="module")
def census() -> GardenCensus:
    return take_census(REPO_ROOT)


def synthetic(name: str, lines: int, size: int) -> SkillMeasurement:
    return SkillMeasurement(name=name, lines=lines, size=size)


def synthetic_census(
    *measurements: SkillMeasurement, governed: frozenset[str] = frozenset()
) -> GardenCensus:
    return GardenCensus(
        terms=GateTerms(
            governed=governed, max_lines=EPIC_MAX_LINES, max_bytes=EPIC_MAX_BYTES
        ),
        measurements=measurements,
    )




def test_the_gate_scans_a_small_fraction_of_the_garden(census):
    """The headline. If this ever fails, the rollout finally happened."""
    scanned, total = census.coverage()
    assert total >= 100, "the garden should hold the full skill roster"
    assert scanned < total, (
        "the gate now scans the whole garden; this test and the module docstring "
        "should be revised rather than left as a stale motivation"
    )
    assert scanned <= 10, f"expected the Phase 0 set, got {scanned} scanned"


def test_every_breach_is_invisible_to_the_gate(census):
    """Why the gate is green.

    Not "some breaches are missed" -- *every* one of them is outside the scanned
    set. The gate is not lenient, it is looking somewhere else.
    """
    breaches = census.breaches()
    assert breaches, "expected the measured breaches; the garden may have changed"
    assert census.unenforced_breaches() == breaches


def test_the_gate_passes_on_its_own_governed_set(census):
    """The gate is not broken; its scope is.

    Running it is what separates "the check is wrong" from "the check is right
    about too little", and only the second is true here.
    """
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / GATE_SOURCE)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"the gate failed: {result.stdout}{result.stderr}"
    assert "PASS" in result.stdout
    assert census.breaches(), "…while breaches exist elsewhere in the garden"


def test_the_largest_breach_is_a_skill_this_pipeline_runs(census):
    """`techne-sprint-planning` opens every sprint in this programme."""
    worst = max(census.breaches(), key=lambda m: m.lines)
    assert worst.name == "techne-sprint-planning"
    assert worst.lines > 3 * EPIC_MAX_LINES
    assert worst.size > 2 * EPIC_MAX_BYTES


def test_a_breach_inside_the_governed_set_is_not_unenforced():
    """Tested synthetically because the live garden cannot exercise it.

    Today every breach is unscanned, so `unenforced_breaches()` and
    `breaches()` return the same tuple and a mutation collapsing one into the
    other is *equivalent* against real data. The distinction only becomes
    observable when a breach is inside the gate's scope -- which is the state
    this repository should eventually be in, and which a synthetic census can
    reach now.
    """
    watched = synthetic_census(
        synthetic("seen", 400, 1000),
        synthetic("unseen", 500, 1000),
        governed=frozenset({"seen"}),
    )
    assert {m.name for m in watched.breaches()} == {"seen", "unseen"}
    assert {m.name for m in watched.unenforced_breaches()} == {"unseen"}


def test_coverage_is_a_pair_not_a_ratio(census):
    """A ratio can be rounded; 5-of-110 and 109-of-110 must stay distinguishable."""
    scanned, total = census.coverage()
    assert isinstance(scanned, int) and isinstance(total, int)
    assert scanned + len(census.unscanned()) == total


def test_the_report_states_coverage_before_a_verdict(census):
    report = format_report(census)
    assert "skills in garden" in report
    assert "scanned by gate" in report
    assert "never scanned" in report


def test_the_report_marks_which_breaches_are_unscanned(census):
    report = format_report(census)
    assert "UNSCANNED" in report




def test_the_limits_match_the_epic(census):
    assert census.terms.max_lines == EPIC_MAX_LINES
    assert census.terms.max_bytes == EPIC_MAX_BYTES


def test_the_governed_set_is_read_from_the_gate_and_is_not_empty(census):
    """A rename that emptied the set would make every count look healthy.

    `scanned` would fall to 0, `breaching unseen` would equal `breaching`, and
    nothing would look wrong -- so emptiness has to be an error rather than a
    reading.
    """
    assert census.terms.governed
    assert "autoskill" in census.terms.governed


def test_a_gate_missing_a_constant_is_refused(tmp_path):
    gate = tmp_path / GATE_SOURCE
    gate.parent.mkdir(parents=True)
    gate.write_text("DEFAULT_MAX_LINES = 300\n", encoding="utf-8")
    with pytest.raises(CensusError) as excinfo:
        read_gate_terms(tmp_path)
    assert excinfo.value.code == "GATE_UNREADABLE"
    assert "DEFAULT_GOVERNED" in str(excinfo.value)


def test_an_absent_gate_is_refused(tmp_path):
    with pytest.raises(CensusError) as excinfo:
        read_gate_terms(tmp_path)
    assert excinfo.value.code == "GATE_ABSENT"


def test_the_byte_limit_is_read_through_arithmetic(tmp_path):
    """The gate writes `20 * 1024`, which `ast.literal_eval` refuses.

    Reading it must not require the gate to give up the readable form.
    """
    gate = tmp_path / GATE_SOURCE
    gate.parent.mkdir(parents=True)
    gate.write_text(
        "DEFAULT_GOVERNED = ('a',)\n"
        "DEFAULT_MAX_LINES = 100 + 200\n"
        "DEFAULT_MAX_BYTES = 20 * 1024\n",
        encoding="utf-8",
    )
    terms = read_gate_terms(tmp_path)
    assert terms.max_lines == 300
    assert terms.max_bytes == 20480


def test_a_computed_limit_that_cannot_be_read_statically_is_refused(tmp_path):
    """A limit requiring execution to know is a limit nobody can audit."""
    gate = tmp_path / GATE_SOURCE
    gate.parent.mkdir(parents=True)
    gate.write_text(
        "DEFAULT_GOVERNED = ('a',)\n"
        "DEFAULT_MAX_LINES = 300\n"
        "DEFAULT_MAX_BYTES = int(os.environ['CEILING'])\n",
        encoding="utf-8",
    )
    with pytest.raises(CensusError) as excinfo:
        read_gate_terms(tmp_path)
    assert excinfo.value.code == "GATE_UNREADABLE"


def test_a_non_sequence_governed_list_is_refused(tmp_path):
    gate = tmp_path / GATE_SOURCE
    gate.parent.mkdir(parents=True)
    gate.write_text(
        "DEFAULT_GOVERNED = 'autoskill'\n"
        "DEFAULT_MAX_LINES = 300\n"
        "DEFAULT_MAX_BYTES = 20480\n",
        encoding="utf-8",
    )
    with pytest.raises(CensusError, match="not a sequence"):
        read_gate_terms(tmp_path)


def test_the_census_does_not_hardcode_the_governed_names():
    """The list must come from the gate, not from a copy that can drift."""
    source = (
        REPO_ROOT
        / "omega_engine_workflows_agents_skills"
        / "infrastructure"
        / "skill_budget_census.py"
    ).read_text(encoding="utf-8")
    tree = ast.parse(source)
    literals = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }
    assert "auto-symmetry-hunter" not in literals, (
        "a governed skill name is hardcoded in the census; read it from the gate"
    )




def test_a_file_without_a_trailing_newline_still_counts_its_last_line(tmp_path):
    skill = tmp_path / SKILL_ROOT / "ragged"
    skill.mkdir(parents=True)
    skill.joinpath("SKILL.md").write_bytes(b"one\ntwo\nthree")
    (measured,) = measure_garden(tmp_path)
    assert measured.lines == 3
    assert measured.size == 13


def test_an_empty_file_measures_zero_lines(tmp_path):
    skill = tmp_path / SKILL_ROOT / "empty"
    skill.mkdir(parents=True)
    skill.joinpath("SKILL.md").write_bytes(b"")
    (measured,) = measure_garden(tmp_path)
    assert measured.lines == 0
    assert measured.size == 0


def test_an_empty_garden_is_refused_rather_than_reported_as_clean(tmp_path):
    """0 breaches out of 0 skills is the most dangerous possible green."""
    (tmp_path / SKILL_ROOT).mkdir(parents=True)
    with pytest.raises(CensusError) as excinfo:
        measure_garden(tmp_path)
    assert excinfo.value.code == "GARDEN_EMPTY"


def test_a_missing_garden_is_refused(tmp_path):
    with pytest.raises(CensusError) as excinfo:
        measure_garden(tmp_path)
    assert excinfo.value.code == "GARDEN_ABSENT"


def test_breach_is_either_limit_not_both():
    assert synthetic("a", 301, 10).breaches(EPIC_MAX_LINES, EPIC_MAX_BYTES)
    assert synthetic("b", 10, EPIC_MAX_BYTES + 1).breaches(
        EPIC_MAX_LINES, EPIC_MAX_BYTES
    )
    assert not synthetic("c", 300, EPIC_MAX_BYTES).breaches(
        EPIC_MAX_LINES, EPIC_MAX_BYTES
    )


def test_the_limits_are_inclusive_ceilings():
    """"must not exceed 300" -- 300 passes, 301 does not."""
    assert not synthetic("at", 300, 1).breaches(EPIC_MAX_LINES, EPIC_MAX_BYTES)
    assert synthetic("over", 301, 1).breaches(EPIC_MAX_LINES, EPIC_MAX_BYTES)




def test_the_committed_baseline_matches_the_garden(census):
    """The baseline is a record of the present, not a wish about it."""
    assert ratchet_violations(census, load_baseline(BASELINE_PATH)) == ()


def test_the_committed_baseline_records_every_current_breach(census):
    baseline = load_baseline(BASELINE_PATH)
    assert set(baseline) == {m.name for m in census.breaches()}


def test_a_new_breach_fails_the_ratchet(census):
    baseline = load_baseline(BASELINE_PATH)
    grown = synthetic_census(
        *census.measurements, synthetic("newcomer", 999, 1),
    )
    problems = ratchet_violations(grown, baseline)
    assert any("newcomer" in problem and "new breach" in problem for problem in problems)


def test_a_recorded_breach_that_grows_in_lines_fails():
    baseline = {"big": synthetic("big", 400, 1000)}
    grown = synthetic_census(synthetic("big", 401, 1000))
    problems = ratchet_violations(grown, baseline)
    assert any("grew from 400 to 401 lines" in problem for problem in problems)


def test_a_recorded_breach_that_grows_in_bytes_fails():
    baseline = {"big": synthetic("big", 400, EPIC_MAX_BYTES + 1)}
    grown = synthetic_census(synthetic("big", 400, EPIC_MAX_BYTES + 2))
    problems = ratchet_violations(grown, baseline)
    assert any("bytes" in problem and "grew" in problem for problem in problems)


def test_a_fixed_breach_must_be_removed_from_the_baseline():
    """What makes this a ratchet rather than a permanent excuse list."""
    baseline = {"big": synthetic("big", 400, 1000)}
    repaired = synthetic_census(synthetic("big", 120, 1000))
    problems = ratchet_violations(repaired, baseline)
    assert any("no longer breaches" in problem for problem in problems)
    assert any("remove the entry" in problem for problem in problems)


def test_a_baseline_entry_for_a_vanished_skill_fails():
    baseline = {"ghost": synthetic("ghost", 400, 1000)}
    problems = ratchet_violations(synthetic_census(synthetic("other", 10, 10)), baseline)
    assert any("no longer in the garden" in problem for problem in problems)


def test_the_ratchet_is_identity_keyed_not_count_keyed():
    """Swapping one breach for another keeps the count and must still fail.

    A count-only baseline ("7 breaches allowed") reads green while the seven are
    a completely different seven. That is `ESC-004-001` in miniature.
    """
    baseline = {"alpha": synthetic("alpha", 400, 1000)}
    swapped = synthetic_census(synthetic("beta", 400, 1000))
    problems = ratchet_violations(swapped, baseline)
    assert len(problems) == 2, problems
    assert any("beta" in problem and "new breach" in problem for problem in problems)
    assert any("alpha" in problem for problem in problems)


def test_an_unchanged_recorded_breach_passes():
    baseline = {"steady": synthetic("steady", 400, 1000)}
    assert ratchet_violations(synthetic_census(synthetic("steady", 400, 1000)), baseline) == ()


def test_a_shrunk_but_still_breaching_skill_passes():
    """Progress is allowed without editing the baseline; regression is not."""
    baseline = {"big": synthetic("big", 400, 30000)}
    assert ratchet_violations(synthetic_census(synthetic("big", 350, 29000)), baseline) == ()


def test_a_duplicate_baseline_entry_is_refused(tmp_path):
    path = tmp_path / "dupe.json"
    path.write_text(
        json.dumps(
            {
                "schema": BASELINE_SCHEMA,
                "breaches": [
                    {"name": "a", "lines": 1, "size": 1},
                    {"name": "a", "lines": 2, "size": 2},
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(CensusError) as excinfo:
        load_baseline(path)
    assert excinfo.value.code == "BASELINE_DUPLICATE"


def test_a_baseline_with_the_wrong_schema_is_refused(tmp_path):
    path = tmp_path / "old.json"
    path.write_text(json.dumps({"schema": "v0", "breaches": []}), encoding="utf-8")
    with pytest.raises(CensusError) as excinfo:
        load_baseline(path)
    assert excinfo.value.code == "BASELINE_SCHEMA"


def test_an_absent_baseline_is_refused(tmp_path):
    with pytest.raises(CensusError) as excinfo:
        load_baseline(tmp_path / "nope.json")
    assert excinfo.value.code == "BASELINE_ABSENT"


def test_unparseable_baseline_is_refused(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(CensusError) as excinfo:
        load_baseline(path)
    assert excinfo.value.code == "BASELINE_UNREADABLE"


def test_a_rendered_baseline_round_trips(census, tmp_path):
    path = tmp_path / "rendered.json"
    path.write_text(render_baseline(census), encoding="utf-8", newline="\n")
    assert ratchet_violations(census, load_baseline(path)) == ()


def test_the_rendered_baseline_says_regenerating_it_defeats_it(census):
    """The file has to warn the next person, because the file is the temptation."""
    document = json.loads(render_baseline(census))
    assert "defeats it" in document["note"]




def test_the_eval_runner_claim_of_sixteen_of_sixteen_holds():
    """AC1, and it is true -- which is worth recording.

    Fifteen sprints of this programme have found quantitative claims in the
    planning corpus that did not hold. This one does, and a passing check is the
    only way that stays visible.
    """
    runner = REPO_ROOT / ".agents" / "operad" / "skill_compiler" / "eval_runner.py"
    result = subprocess.run(
        [sys.executable, str(runner)], cwd=REPO_ROOT, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "16/16 passed; 0 failed." in result.stdout


def test_the_polarized_pair_the_epic_names_both_exist():
    """The Polarized Pairing Law, at the only place the estate makes it concrete.

    The general law -- "every constructive generator is paired with an
    adversarial detector" -- cannot be checked, because no skill declares a
    polarity. What can be checked is the one pair the epic names by name, and a
    rename breaking it is exactly the failure PR #187's sweep caused elsewhere.
    """
    garden = REPO_ROOT / SKILL_ROOT
    assert (garden / "autoskill" / "SKILL.md").is_file()
    assert (garden / "auto-anti-skill-search" / "SKILL.md").is_file()


def test_no_skill_declares_a_polarity(census):
    """The finding behind the previous test, pinned so it stays visible.

    The Polarized Pairing Law is enforced nowhere because there is nothing to
    enforce it against: no skill states whether it is constructive or
    adversarial. Inventing that vocabulary and assigning it across 110 skills is
    a governance decision, not a side effect of this sprint. If a polarity field
    ever lands, this test fails and the law becomes checkable.
    """
    garden = REPO_ROOT / SKILL_ROOT
    declaring = [
        path.parent.name
        for path in garden.rglob("SKILL.md")
        if b"polarity:" in path.read_bytes()
    ]
    assert declaring == [], f"a polarity field now exists on {declaring}"
