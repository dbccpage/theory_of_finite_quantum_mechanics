"""Planar substitution over the skill garden's coloured operad.

`EPIC-OE-OEWAS-003` deliverables 1 and 2: an evaluator for
$\\theta \\circ_i \\phi$, and a registry "verifying that every declared
composition path possesses an exact witness composite operation".

They are one thing. Substitution is admissible exactly when the colour $\\phi$
produces matches the colour $\\theta$ expects at slot $i$, and associativity is
the statement that two nestings of three admissible substitutions agree. A
registry storing witnesses without deciding admissibility would be a list of
claims, so the witness here *is* the computed composite.

The garden is the fixture. Every skill package on disk declares its operad
triple, and the tests below check the estate's own consistency rather than a
constructed example: no missing field, no arity disagreeing with its own source
list, exactly ten colours in either position. The count is read from the
directory rather than written here -- a census in prose goes stale silently, and
this docstring said 110 for twenty-five sprints after the garden reached 112.

**Arity is derived, never declared twice.** `OperadOperation.arity` reads the
length of the source tuple. An operation carrying arity as a separate field could
contradict itself -- the defect sprint 006 found in the fibration table, where a
row declared a fiber size of 7 beside eight enumerated members. Here the two
cannot disagree, because there is only one of them.
"""

from __future__ import annotations

import pytest

from omega_engine_workflows_agents_skills.domain.planar_substitution import (
    OPERAD_COLOURS,
    SKILLS_DIR,
    OperadOperation,
    SubstitutionError,
    admissible_substitutions,
    associativity_witness,
    is_admissible,
    load_garden,
    substitute,
)


def op(name: str, sources: tuple[str, ...], target: str) -> OperadOperation:
    return OperadOperation(name=name, source_colours=sources, target_colour=target)


@pytest.fixture(scope="module")
def garden():
    return load_garden()


# --------------------------------------------------------------------------
# The garden is consistent, and that is asserted rather than assumed
# --------------------------------------------------------------------------


def test_the_garden_loads_every_skill():
    """Anti-vacuity, and `load_garden` refuses rather than skipping a bad skill.

    Every refusal path in the loader -- missing frontmatter, an incomplete
    triple, an arity disagreeing with its own source list -- would raise here.
    Loading every package cleanly is therefore a statement about the estate.

    The oracle is the count of `SKILL.md` files on disk, not a constant. A
    literal was the original form and it was wrong for twenty-five sprints: two
    skills were added, the pin said 110, and nothing ran the test. A hardcoded
    census of a growing corpus reports its own staleness as a defect in the
    corpus, which is the shape `ESC-002-001` exists to name.

    Counting the directory is also the *stronger* assertion. The literal could
    not tell a dropped skill from an added one; this can. If a refusal path ever
    became a `continue`, the loader would return fewer operations than there are
    files and this fails -- which is the property the docstring above claims.
    """
    on_disk = len(list(SKILLS_DIR.glob("*/SKILL.md")))
    assert on_disk > 0, f"no skill packages found under {SKILLS_DIR}"
    assert len(load_garden()) == on_disk


def test_the_colour_vocabulary_is_exactly_ten(garden):
    """Matching what `EPIC-OE-OEWAS-RUST-001` pins as the estate vocabulary."""
    used = {operation.target_colour for operation in garden}
    used |= {colour for operation in garden for colour in operation.source_colours}
    assert used == OPERAD_COLOURS
    assert len(OPERAD_COLOURS) == 10


def test_no_operation_declares_a_colour_outside_the_vocabulary(garden):
    for operation in garden:
        assert operation.target_colour in OPERAD_COLOURS
        for colour in operation.source_colours:
            assert colour in OPERAD_COLOURS


def test_arity_is_derived_not_declared():
    """The fibration defect, made unrepeatable by construction."""
    operation = op("x", ("Code", "Audit"), "Code")
    assert operation.arity == 2
    assert not hasattr(operation, "declared_arity")


def test_the_garden_admits_the_substitutions_it_admits(garden):
    """Pinned so a colour change anywhere is reported rather than absorbed.

    Asserted as a **pair** with the garden size, because the total alone cannot
    say which of two very different things happened. Adding a skill changes this
    count legitimately; changing a colour changes it as a defect. A bare total
    conflates them, and the previous single pin failed on the benign case while
    proving nothing about the malign one.

    Read a failure as: **both numbers moved** -- a skill was added or removed, so
    update the pair and move on. **Only the second moved** -- the garden is the
    same size and a declared colour drifted, which is the case this test exists
    for; find the skill whose operad triple changed before touching this line.
    """
    # 2026-08-31: (115, 3709) -> (128, 4392). Thirteen skills admitted.
    # 2026-09-07: (128, 4392) -> (133, 4688). Five operadic skills admitted.
    pinned = (133, 4688)
    measured = (len(garden), len(admissible_substitutions(garden)))
    assert measured == pinned, (
        f"garden/substitution pair moved {pinned} -> {measured}; "
        "both moved = the garden changed size, second only = a colour drifted"
    )


# --------------------------------------------------------------------------
# Substitution
# --------------------------------------------------------------------------


def test_a_matching_colour_composes():
    theta = op("theta", ("Code", "Audit"), "Proof")
    phi = op("phi", ("State",), "Code")
    composite = substitute(theta, 0, phi)
    assert composite.source_colours == ("State", "Audit")
    assert composite.target_colour == "Proof"


def test_substitution_is_planar_the_remaining_order_is_preserved():
    """phi's inputs are spliced in place, not appended.

    Appending would compose the same colours into a different operation, and the
    difference is invisible in an arity check.
    """
    theta = op("theta", ("Code", "Audit", "Proof"), "State")
    phi = op("phi", ("Paper", "Post"), "Audit")
    composite = substitute(theta, 1, phi)
    assert composite.source_colours == ("Code", "Paper", "Post", "Proof")


def test_substituting_a_nullary_operation_removes_the_slot():
    theta = op("theta", ("Code", "Audit"), "State")
    phi = op("phi", (), "Code")
    assert substitute(theta, 0, phi).source_colours == ("Audit",)


def test_a_colour_mismatch_is_refused():
    theta = op("theta", ("Code",), "State")
    phi = op("phi", (), "Audit")
    with pytest.raises(SubstitutionError) as excinfo:
        substitute(theta, 0, phi)
    assert excinfo.value.code == "COLOUR_MISMATCH"
    assert "expects 'Code'" in str(excinfo.value)


def test_a_slot_that_does_not_exist_is_refused():
    theta = op("theta", ("Code",), "State")
    phi = op("phi", (), "Code")
    with pytest.raises(SubstitutionError) as excinfo:
        substitute(theta, 1, phi)
    assert excinfo.value.code == "INDEX_OUT_OF_RANGE"


def test_a_negative_slot_is_refused():
    """Python would happily index -1; an operad slot is not a Python index."""
    theta = op("theta", ("Code",), "State")
    phi = op("phi", (), "Code")
    with pytest.raises(SubstitutionError, match="INDEX_OUT_OF_RANGE"):
        substitute(theta, -1, phi)


def test_a_boolean_slot_is_refused():
    """`True` is an int in Python and would silently mean slot 1."""
    theta = op("theta", ("Code", "Audit"), "State")
    phi = op("phi", (), "Audit")
    with pytest.raises(SubstitutionError, match="BAD_INDEX"):
        substitute(theta, True, phi)


def test_a_colour_outside_the_vocabulary_is_refused_at_construction():
    with pytest.raises(SubstitutionError) as excinfo:
        op("x", ("Vibes",), "Code")
    assert excinfo.value.code == "UNKNOWN_COLOUR"


def test_an_unknown_target_colour_is_refused():
    with pytest.raises(SubstitutionError, match="UNKNOWN_COLOUR"):
        op("x", ("Code",), "Vibes")


def test_is_admissible_agrees_with_substitute():
    theta = op("theta", ("Code",), "State")
    good = op("good", (), "Code")
    bad = op("bad", (), "Audit")
    assert is_admissible(theta, 0, good) is True
    assert is_admissible(theta, 0, bad) is False


# --------------------------------------------------------------------------
# Associativity -- deliverable 2's witness
# --------------------------------------------------------------------------


def test_the_two_nestings_agree_and_the_witness_is_the_composite():
    """The operad axiom, with the slot shift that makes it non-obvious.

    Substituting `phi` into `theta` first splices `phi`'s inputs ahead of the
    slot `psi` targets, so that slot moves from `j` to `i + j`. An
    implementation that forgot the shift would still typecheck and would compose
    the wrong thing.
    """
    theta = op("theta", ("Code", "Audit"), "State")
    phi = op("phi", ("Paper", "Post"), "Code")
    psi = op("psi", ("Proof",), "Paper")
    witness = associativity_witness(theta, 0, phi, 0, psi)
    assert witness.source_colours == ("Proof", "Post", "Audit")
    assert witness.target_colour == "State"


def test_the_witness_holds_when_psi_targets_a_later_slot():
    theta = op("theta", ("Code",), "State")
    phi = op("phi", ("Paper", "Post"), "Code")
    psi = op("psi", ("Proof",), "Post")
    witness = associativity_witness(theta, 0, phi, 1, psi)
    assert witness.source_colours == ("Paper", "Proof")


def test_the_witness_refuses_when_an_inner_substitution_is_inadmissible():
    theta = op("theta", ("Code",), "State")
    phi = op("phi", ("Paper",), "Code")
    psi = op("psi", (), "Audit")
    with pytest.raises(SubstitutionError, match="COLOUR_MISMATCH"):
        associativity_witness(theta, 0, phi, 0, psi)


def test_associativity_holds_across_the_real_garden(garden):
    """Sampled over the estate, not over a constructed triple.

    Every admissible (theta, i, phi) whose composite admits a further psi is
    checked. If the slot shift were wrong, a real triple would expose it.
    """
    by_target: dict[str, list] = {}
    for operation in garden:
        by_target.setdefault(operation.target_colour, []).append(operation)

    checked = 0
    for theta in garden[:25]:
        for i in range(theta.arity):
            for phi in by_target.get(theta.source_colours[i], [])[:3]:
                for j in range(phi.arity):
                    for psi in by_target.get(phi.source_colours[j], [])[:2]:
                        associativity_witness(theta, i, phi, j, psi)
                        checked += 1
    assert checked > 100, f"only {checked} triples exercised; the sample is thin"


# --------------------------------------------------------------------------
# Refusals in the loader
# --------------------------------------------------------------------------


def test_a_missing_garden_is_refused(tmp_path):
    with pytest.raises(SubstitutionError, match="GARDEN_MISSING"):
        load_garden(tmp_path / "absent")


def test_an_empty_garden_is_refused(tmp_path):
    """An empty parse must not read as a garden with no defects."""
    tmp_path.joinpath("skills").mkdir()
    with pytest.raises(SubstitutionError, match="GARDEN_EMPTY"):
        load_garden(tmp_path / "skills")


def test_a_skill_whose_arity_disagrees_with_its_sources_is_refused(tmp_path):
    """The fibration defect, caught at the boundary rather than tolerated."""
    package = tmp_path / "broken"
    package.mkdir()
    package.joinpath("SKILL.md").write_text(
        "---\n"
        'operad_source_colours: ["Code", "Audit"]\n'
        'operad_target_colour: "State"\n'
        "operad_arity: 3\n"
        "---\n\nbody\n",
        encoding="utf-8", newline="\n",
    )
    with pytest.raises(SubstitutionError) as excinfo:
        load_garden(tmp_path)
    assert excinfo.value.code == "ARITY_DISAGREES"
    assert "beside 2 source colours" in str(excinfo.value)


def test_a_skill_missing_the_operad_triple_is_refused(tmp_path):
    package = tmp_path / "partial"
    package.mkdir()
    package.joinpath("SKILL.md").write_text(
        '---\nname: partial\noperad_arity: 1\n---\n\nbody\n',
        encoding="utf-8", newline="\n",
    )
    with pytest.raises(SubstitutionError, match="INCOMPLETE_OPERAD"):
        load_garden(tmp_path)


def test_a_well_formed_skill_loads(tmp_path):
    """The loader must be able to succeed, or its refusals prove nothing."""
    package = tmp_path / "fine"
    package.mkdir()
    package.joinpath("SKILL.md").write_text(
        "---\n"
        'operad_source_colours: ["Code"]\n'
        'operad_target_colour: "State"\n'
        "operad_arity: 1\n"
        "---\n\nbody\n",
        encoding="utf-8", newline="\n",
    )
    loaded = load_garden(tmp_path)
    assert len(loaded) == 1
    assert loaded[0].name == "fine"
    assert loaded[0].arity == 1


# --------------------------------------------------------------------------
# Deliverable 3 has no data
# --------------------------------------------------------------------------


def test_no_skill_declares_a_grade_or_layer():
    """Why `TwoLayerGradingValidator` is not built.

    The epic specifies it to enforce "that entry-grade skills invoke
    discipline-grade skills but never compose directly over other entry-grade
    skills". Nothing in the estate declares a grade, so the validator would have
    to invent the grading it validates. Asserted here so the gap is recorded --
    and so the day a grade field appears, this test fails and the validator
    becomes buildable.
    """
    import pathlib
    import re

    root = pathlib.Path(__file__).resolve().parents[2]
    pattern = re.compile(r"^(grade|layer|operad_grade|skill_grade)\s*:", re.MULTILINE)
    declaring = [
        path.parent.name
        for path in (root / ".agents" / "skills").glob("*/SKILL.md")
        if pattern.search(path.read_text(encoding="utf-8"))
    ]
    assert declaring == [], (
        f"skills now declare a grade: {declaring}. The two-layer grading "
        "validator is buildable; this test should be replaced by it."
    )
