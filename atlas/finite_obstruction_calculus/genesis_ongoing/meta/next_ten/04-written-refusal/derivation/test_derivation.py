"""Comprehensive test suite for Problem 04 (Written Refusal) derivation.

Verifies:
1. Written identity, properties, and orbit-stabilizer theorem.
2. Refusal semantics: loop detection, state invariance, and accounting.
3. Breadth-first exploration at bound 3 under all 4 combinations (bra x sameness).
4. Strict equality of written refusal closure with Eighteenth closure at every round (Falsifier holds).
5. Projection of written refusal closure onto Twentyfirst canonical quotient closure.
6. Non-trivial fiber splitting: quotient classes containing multiple written representatives.
7. Independent census by relation counting and orbit partition.
8. Evidence generation and `--check` CLI functionality, including mismatch detection.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import cast

import pytest

# Ensure derivation directory is on sys.path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# Ensure repo code/ directory is on sys.path
ROOT = Path(__file__).resolve().parents[4]
if str(ROOT / "code") not in sys.path:
    sys.path.insert(0, str(ROOT / "code"))

from evidence import main as evidence_main  # noqa: E402
from evidence import measure_run, write_all  # noqa: E402
from model import (  # noqa: E402
    AttemptRecord,
    aut_size,
    compare_with_eighteenth,
    compare_with_twentyfirst,
    explore_written_refusal,
    independent_written_census,
    orbit,
    orbit_size,
    orbit_splits_factorial,
    refusal_result,
    refused,
    same_written,
    to_quotient,
    total_census_count,
    verify_census,
)
from xry.state import Sameness, State, canonical, given  # noqa: E402


def test_written_identity_and_quotient() -> None:
    """Distinct writings of identical structure are different written states but identical in quotient."""
    s1 = State.of(2, [(0, 1)], names=None)
    s2 = State.of(2, [(1, 0)], names=None)

    assert not same_written(s1, s2)
    assert s1 != s2
    assert s1.key() != s2.key()

    # In canonical quotient, they are identified
    assert to_quotient(s1) == to_quotient(s2)
    assert canonical(s1) == canonical(s2)

    # Identical state is same written
    assert same_written(s1, State.of(2, [(0, 1)], names=None))


def test_orbit_and_stabilizer() -> None:
    """Orbit size times automorphism size equals n! for all written states."""
    # Empty graph on 3 terms: orbit size 1, Aut size 6
    s_empty = State.of(3, [], names=None)
    assert orbit_size(s_empty) == 1
    assert aut_size(s_empty) == 6
    assert orbit_splits_factorial(s_empty)
    assert orbit(s_empty) == frozenset([s_empty])

    # Single directed edge on 3 terms: 6 possible directed edges, Aut size 1
    s_edge = State.of(3, [(0, 1)], names=None)
    assert orbit_size(s_edge) == 6
    assert aut_size(s_edge) == 1
    assert orbit_splits_factorial(s_edge)

    # State with names (anchored): orbit size under name-preserving or name-moving permutations
    s_named = State.of(2, [(0, 1)], names=(0, 1))
    assert orbit_size(s_named) == 2
    assert aut_size(s_named) == 1
    assert orbit_splits_factorial(s_named)


def test_refusal_logic() -> None:
    """Obstructed changes produce loop assertions, are refused, and change nothing."""
    legal_state = State.of(2, [(0, 1)], names=(0, 1))
    illegal_state = State.of(2, [(0, 0)], names=(0, 1))

    assert not refused(legal_state)
    assert refused(illegal_state)

    # Refusal changes nothing: returns the exact same state
    assert refusal_result(legal_state) is legal_state
    assert refusal_result(illegal_state) is illegal_state


def test_exploration_validation() -> None:
    """Exploration enforces valid start state and bound constraints."""
    illegal_start = State.of(2, [(0, 0)], names=(0, 1))
    with pytest.raises(ValueError, match="what is given asserts no xrx"):
        explore_written_refusal(illegal_start, bound=3)

    legal_start = State.of(3, [(0, 1)], names=None)
    with pytest.raises(ValueError, match="the bound is below what is given"):
        explore_written_refusal(legal_start, bound=2)


def test_exploration_free_closure() -> None:
    """FREE exploration reaches 69 states at bound 3, with exact round waves matching Eighteenth."""
    start = given(False, Sameness.FREE)
    expl = explore_written_refusal(start, bound=3, rounds=12, keep_log=True)

    assert len(expl.depth) == 69
    assert expl.new_per_round == [1, 3, 8, 15, 20, 15, 6, 1, 0, 0, 0, 0, 0]
    assert expl.total_refusals > 0
    assert len(expl.frontier) == 64
    assert len(expl.log) > 0

    # Every logged record has expected attributes
    rec = expl.log[0]
    assert isinstance(rec, AttemptRecord)
    assert isinstance(rec.obstructed, bool)

    # Test census match
    assert verify_census(expl, Sameness.FREE)


def test_exploration_anchored_closure() -> None:
    """ANCHORED exploration reaches 137 states at bound 3, with exact round waves matching Eighteenth."""
    start = given(False, Sameness.ANCHORED)
    expl = explore_written_refusal(start, bound=3, rounds=12, keep_log=False)

    assert len(expl.depth) == 137
    assert expl.new_per_round == [1, 3, 8, 16, 23, 22, 21, 21, 15, 6, 1, 0, 0]
    assert len(expl.frontier) == 128
    assert verify_census(expl, Sameness.ANCHORED)


def test_independent_census_formulas() -> None:
    """Independent census matches closed form 2^(n*(n-1)) for FREE and anchored multipliers."""
    census_free = independent_written_census(3, Sameness.FREE)
    assert census_free == {1: 1, 2: 4, 3: 64}
    assert total_census_count(3, Sameness.FREE) == 69

    census_anchored = independent_written_census(3, Sameness.ANCHORED)
    assert census_anchored == {1: 1, 2: 8, 3: 128}
    assert total_census_count(3, Sameness.ANCHORED) == 137


def test_falsifier_exact_match_with_eighteenth() -> None:
    """The written refusal closure is exactly the Eighteenth closure at every round across all 4 configs."""
    for bra in (False, True):
        for sameness in (Sameness.ANCHORED, Sameness.FREE):
            comp = compare_with_eighteenth(bra, sameness, bound=3, rounds=12)
            assert comp["depth_matches"], f"Depth mismatch for bra={bra}, sameness={sameness}"
            assert comp["waves_match"], f"Waves mismatch for bra={bra}, sameness={sameness}"
            assert comp["frontier_matches"], f"Frontier mismatch for bra={bra}, sameness={sameness}"
            assert len(comp["disagreements"]) == 0  # type: ignore[arg-type]
            assert len(comp["round_mismatches"]) == 0  # type: ignore[arg-type]


def test_twentyfirst_quotient_projection_and_fiber_splitting() -> None:
    """Projecting the written refusal closure by canonical renaming yields Twentyfirst's quotient closure."""
    for bra in (False, True):
        for sameness in (Sameness.ANCHORED, Sameness.FREE):
            comp = compare_with_twentyfirst(bra, sameness, bound=3, rounds=12)
            assert comp["quotient_matches"]
            assert cast(int, comp["splitting_classes_count"]) > 0
            assert cast(int, comp["max_fiber_size"]) > 1

    # Check specific fiber counts for FREE
    comp_free = compare_with_twentyfirst(False, Sameness.FREE, bound=3, rounds=12)
    assert comp_free["twentyfirst_count"] == 20
    assert comp_free["written_count"] == 69
    assert comp_free["splitting_classes_count"] == 15
    assert (
        comp_free["max_fiber_size"] == 6
    )  # 3! = 6 distinct writings for an asymmetric graph on 3 terms


def test_measure_run_and_evidence_generation(tmp_path: Path) -> None:
    """Measure run gathers full metrics and write_all outputs valid JSON summary and manifest."""
    res = measure_run(False, Sameness.FREE, bound=3, rounds=12)
    assert res["written_results"] == 69
    assert res["eighteenth_depth_matches"] is True
    assert res["twentyfirst_quotient_matches"] is True
    assert res["census_matches"] is True
    assert len(res["orbit_formula_fails"]) == 0  # type: ignore[arg-type]

    out_dir = tmp_path / "evidence"
    summary = write_all(out_dir, bound=3, rounds=12)
    assert summary["falsifier_holds"] is True
    assert summary["hypothesis_holds"] is False
    assert (out_dir / "summary.json").is_file()
    assert (out_dir / "MANIFEST.sha256").is_file()


def test_evidence_cli_and_check(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Evidence CLI correctly writes, verifies with --check, and detects errors."""
    ev_dir = tmp_path / "ev_cli"

    # 1. Missing directory with --check returns 1
    code = evidence_main(["--out", str(ev_dir), "--check"])
    assert code == 1

    # 2. Normal generation writes files and returns 0
    code = evidence_main(["--out", str(ev_dir), "--bound", "2", "--rounds", "4"])
    assert code == 0
    assert (ev_dir / "summary.json").is_file()

    # 3. Successful --check returns 0
    code = evidence_main(["--out", str(ev_dir), "--bound", "2", "--rounds", "4", "--check"])
    assert code == 0

    # 4. Tampered directory with --check detects discrepancy and returns 1
    (ev_dir / "summary.json").write_text("tampered content\n", encoding="utf-8")
    code = evidence_main(["--out", str(ev_dir), "--bound", "2", "--rounds", "4", "--check"])
    assert code == 1


def _assert_manuscript_census(
    text: str, summary: dict[str, object], *, resolution: bool = False
) -> None:
    """Check the four Section 3 cohorts without accepting numeric coercions."""
    import json

    fields = (
        "written_results",
        "new_per_round",
        "total_refusals",
        "frontier_exits",
        "quotient_classes_count",
        "splitting_classes_count",
    )
    runs = summary["runs"]
    assert isinstance(runs, list)
    expected = {(run["bra"], run["sameness"]): run for run in runs}
    assert len(expected) == len(runs) == 4
    if resolution:
        initial = {"`bra = False`": False, "`bra = True`": True}
        fields = fields[:-1]  # The resolution table has no splitting-fiber column.
    else:
        initial = {"$arb$ only": False, "$arb \\land bra$": True}
    seen: set[tuple[bool, str]] = set()
    prefix = "| `bra =" if resolution else "| $arb"
    rows = [line for line in text.splitlines() if line.startswith(prefix)]
    assert len(rows) == 4, "census must contain exactly four rows"
    for row in rows:
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        assert len(cells) == (9 if resolution else 8), "wrong census column count"
        assert cells[0] in initial, "unknown initial alternative"
        assert cells[1] in ("ANCHORED", "FREE"), "unknown sameness reading"
        key = (initial[cells[0]], cells[1].lower())
        assert key in expected and key not in seen, "duplicate or unknown cohort"
        seen.add(key)
        if resolution:
            parent_count = json.loads(cells[3])
            assert type(parent_count) is int and parent_count == expected[key]["written_results"], (
                "parent count disagrees with replay"
            )
            assert cells[4] == "**Exact**" and expected[key]["eighteenth_depth_matches"] is True, (
                "closure match disagrees with replay"
            )
            values = [cells[2], *cells[5:]]
        else:
            values = cells[2:]
        for field, cell in zip(fields, values):
            value = json.loads(cell.strip("`"))
            if field == "new_per_round":
                assert isinstance(value, list), "wave vector must be a list"
                assert all(type(item) is int and item >= 0 for item in value), (
                    "wave entries must be nonnegative integers"
                )
            else:
                assert type(value) is int and value >= 0, "counts must be nonnegative integers"
            assert value == expected[key][field], f"{key}: {field} disagrees with replay"
    assert seen == set(expected), "missing cohort"


@pytest.fixture(scope="module")
def replayed_census(tmp_path_factory: pytest.TempPathFactory) -> dict[str, object]:
    return write_all(tmp_path_factory.mktemp("manuscript_census"), bound=3, rounds=12)


def test_stored_census_matches_fresh_replay(replayed_census: dict[str, object]) -> None:
    import json

    stored = json.loads((HERE / "evidence" / "summary.json").read_text(encoding="utf-8"))
    assert stored == replayed_census


def test_manuscript_census_matches_fresh_replay(replayed_census: dict[str, object]) -> None:
    _assert_manuscript_census((HERE / "paper.md").read_text(encoding="utf-8"), replayed_census)


def test_resolution_census_matches_fresh_replay(replayed_census: dict[str, object]) -> None:
    _assert_manuscript_census(
        (HERE / "resolution.md").read_text(encoding="utf-8"), replayed_census, resolution=True
    )


@pytest.mark.parametrize("resolution", [False, True])
@pytest.mark.parametrize(
    "mutation",
    [
        "missing",
        "duplicate",
        "count_bool",
        "count_float",
        "wave_bool",
        "wave_float",
        "wrong_wave",
        "wrong_count",
        "unknown_reading",
    ],
)
def test_manuscript_census_rejects_mutations(
    replayed_census: dict[str, object], mutation: str, resolution: bool
) -> None:
    import json

    # Construct a known-good four-row control from the fresh model, then alter
    # exactly one property. A manuscript defect cannot make this control pass.
    runs = replayed_census["runs"]
    assert isinstance(runs, list)
    cells = []
    for run in runs:
        initial = "$arb \\land bra$" if run["bra"] else "$arb$ only"
        row = [
            initial,
            run["sameness"].upper(),
            *[
                json.dumps(run[field])
                for field in (
                    "written_results",
                    "new_per_round",
                    "total_refusals",
                    "frontier_exits",
                    "quotient_classes_count",
                    "splitting_classes_count",
                )
            ],
        ]
        if resolution:
            row = [f"`bra = {run['bra']}`", row[1], row[2], row[2], "**Exact**", *row[3:-1]]
        cells.append(row)

    def render() -> str:
        return "\n".join("| " + " | ".join(row) + " |" for row in cells)

    _assert_manuscript_census(render(), replayed_census, resolution=resolution)
    if mutation == "missing":
        cells.pop()
    elif mutation == "duplicate":
        cells[-1] = cells[0].copy()
    elif mutation == "count_bool":
        cells[0][2] = "true"
    elif mutation == "count_float":
        cells[0][2] += ".0"
    elif mutation in ("wave_bool", "wave_float", "wrong_wave"):
        column = 5 if resolution else 3
        wave = json.loads(cells[0][column])
        wave[0] = {"wave_bool": True, "wave_float": 1.0, "wrong_wave": 2}[mutation]
        cells[0][column] = json.dumps(wave)
    elif mutation == "wrong_count":
        cells[0][2] = str(int(cells[0][2]) + 1)
    elif mutation == "unknown_reading":
        cells[0][1] = "UNSPECIFIED"
    with pytest.raises(AssertionError):
        _assert_manuscript_census(render(), replayed_census, resolution=resolution)
