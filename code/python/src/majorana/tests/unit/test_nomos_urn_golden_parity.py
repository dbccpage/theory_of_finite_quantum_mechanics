"""The Nomos URN grammar has two implementations and nothing compared them.

`nomos_urn.py` and `nomos_urn.rs` each parse the same URN grammar, each has its
own tests -- 10 and 9 respectively -- and each tests itself against its own
expectations. Nothing made them agree. The two could drift apart on any input
neither suite happened to cover, and the first symptom would be a contract id
accepted on one side of the seam and refused on the other.

`nomos_urn_golden_vectors_v1.json` is the shared corpus. Python is its declared
owner, so the expectations were produced by running the Python parser rather
than hand-authored -- a hand-written expectation is a third implementation, and
a wrong one is indistinguishable from a real disagreement. Rust conforms to the
same bytes in `nomos_urn.rs`.

These tests are the Python half. They are not a restatement of the existing
suite: the existing tests check that the parser behaves, these check that it
behaves *exactly as the shared corpus records*, which is what the other language
is also held to.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from omega_engine.crates.contract_core import nomos_urn as urn

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
VECTORS_PATH = (
    REPO_ROOT
    / "omega_engine_governance/contracts/fixtures/nomos_urn_golden_vectors_v1.json"
)

# Every error kind the grammar declares. Pinned as a set so adding a variant to
# one language without the other, or renaming one, is reported rather than
# absorbed -- the two enums agree today and nothing was keeping them that way.
DECLARED_ERROR_KINDS = frozenset({
    "Empty",
    "MissingPrefix",
    "WrongSegmentCount",
    "EmptySegment",
    "BadDomainCharset",
    "BadNameCharset",
    "BadCrateCharset",
    "BadVersion",
    "UnexpectedFileMarker",
})


def _load() -> dict:
    return json.loads(VECTORS_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def corpus() -> dict:
    return _load()


def test_the_corpus_exists_and_is_not_empty(corpus):
    assert corpus["schema"] == "omega.contract.nomos_urn_golden_vectors.v1"
    assert len(corpus["vectors"]) >= 28, (
        "the corpus shrank; vectors are removed only when the grammar drops a "
        "case, and that must be deliberate"
    )


def test_the_corpus_covers_every_declared_error_kind(corpus):
    """A corpus missing a kind cannot detect drift in that kind."""
    covered = {v["error_kind"] for v in corpus["vectors"] if not v["accepts"]}
    assert covered == DECLARED_ERROR_KINDS, (
        f"uncovered={sorted(DECLARED_ERROR_KINDS - covered)} "
        f"unexpected={sorted(covered - DECLARED_ERROR_KINDS)}"
    )


def test_the_python_error_vocabulary_is_exactly_the_declared_set():
    """Pins the module's own constants, not just what the corpus happens to use."""
    exported = {
        getattr(urn, name) for name in dir(urn) if name.startswith("ERR_")
    }
    assert exported == DECLARED_ERROR_KINDS, (
        f"module exports {sorted(exported)}; "
        f"declared set is {sorted(DECLARED_ERROR_KINDS)}"
    )


def test_the_corpus_has_both_accepts_and_rejects(corpus):
    """A corpus of one polarity proves nothing about the other."""
    accepts = [v for v in corpus["vectors"] if v["accepts"]]
    rejects = [v for v in corpus["vectors"] if not v["accepts"]]
    assert len(accepts) >= 8
    assert len(rejects) >= 20


def test_every_label_is_unique(corpus):
    """Rust reports failures by label; a duplicate makes a failure ambiguous."""
    labels = [v["label"] for v in corpus["vectors"]]
    assert len(labels) == len(set(labels))


def test_every_accepted_vector_parses_to_the_recorded_parts(corpus):
    mismatches = []
    for vector in corpus["vectors"]:
        if not vector["accepts"]:
            continue
        try:
            parsed = urn.parse_nomos_urn(vector["raw"])
        except urn.NomosUrnError as exc:
            mismatches.append(f"{vector['label']}: refused with {exc.kind}")
            continue
        for field in ("domain", "name", "version", "crate_name", "file_locus"):
            if getattr(parsed, field) != vector[field]:
                mismatches.append(
                    f"{vector['label']}: {field} is {getattr(parsed, field)!r}, "
                    f"corpus records {vector[field]!r}"
                )
    assert not mismatches, "accepted-vector disagreements:\n  " + "\n  ".join(mismatches)


def test_every_rejected_vector_refuses_with_the_recorded_kind(corpus):
    """The kind matters, not merely that it refused.

    Two parsers can agree a URN is bad and disagree about why, and a caller
    branching on the kind would then behave differently across the seam.
    """
    mismatches = []
    for vector in corpus["vectors"]:
        if vector["accepts"]:
            continue
        try:
            urn.parse_nomos_urn(vector["raw"])
        except urn.NomosUrnError as exc:
            if exc.kind != vector["error_kind"]:
                mismatches.append(
                    f"{vector['label']}: refused with {exc.kind}, "
                    f"corpus records {vector['error_kind']}"
                )
        else:
            mismatches.append(f"{vector['label']}: accepted, corpus records refusal")
    assert not mismatches, "rejected-vector disagreements:\n  " + "\n  ".join(mismatches)


def test_is_well_formed_agrees_with_parse_on_every_vector(corpus):
    """The cheap predicate and the full parse must not disagree."""
    disagreements = [
        vector["label"]
        for vector in corpus["vectors"]
        if urn.is_well_formed_nomos_urn(vector["raw"]) is not vector["accepts"]
    ]
    assert not disagreements, f"predicate disagrees with corpus on: {disagreements}"


def test_accepted_vectors_round_trip_through_format(corpus):
    """format(parse(x)) == x for every accepted form, or the pair is lossy."""
    lossy = []
    for vector in corpus["vectors"]:
        if not vector["accepts"]:
            continue
        parsed = urn.parse_nomos_urn(vector["raw"])
        if urn.format_nomos_urn(parsed) != vector["raw"]:
            lossy.append(
                f"{vector['label']}: {urn.format_nomos_urn(parsed)!r} != "
                f"{vector['raw']!r}"
            )
    assert not lossy, "format/parse round trip is lossy:\n  " + "\n  ".join(lossy)


def test_the_corpus_names_its_owner(corpus):
    """A shared fixture with no declared owner drifts by consensus."""
    assert corpus["owner"] == "omega_engine/crates/contract_core/nomos_urn.py"


# --------------------------------------------------------------------------
# EPIC-OE-GOV-001's stated deliverables, checked against the tree
# --------------------------------------------------------------------------

EPIC = (
    REPO_ROOT
    / "omega_engine_product_planning_office/plans/epics/oeags"
    / "epic_oe_gov_001_canonical_contract_schema_and_urn_registry_plan.md"
)


def test_the_epic_states_the_measured_contract_count():
    """Compare the current deliverable bullet, not a historical number mention.

    Measured here rather than restated, so the epic and the tree cannot drift
    apart again without this failing. The same defect in CWGATE-001 is what
    ESC-002-001 escalated.
    """
    contracts = list(
        (REPO_ROOT / "omega_engine_governance/contracts").rglob("*.contract.yaml")
    )
    yaml_count = len(list((REPO_ROOT / "omega_engine_governance/contracts").rglob("*.yaml")))
    assert contracts and yaml_count >= len(contracts)
    live_bullet = (
        f"- `omega_engine_governance/contracts/**/*.contract.yaml` -- **{len(contracts)}** contracts\n"
        f"  ({yaml_count} YAML files in total under that tree)."
    )
    assert live_bullet in EPIC.read_text(encoding="utf-8")


def test_the_epic_locates_the_python_owner_where_it_actually_is():
    """It pointed at a path nothing has ever occupied.

    The wrong path is checked for as a *deliverable bullet*, not as a substring.
    The epic keeps a note saying it previously pointed there, and that note is
    provenance: it is how the next reader learns the path was wrong rather than
    merely finding it silently changed. Banning the substring would delete the
    record. See the shared test-quality law, "A live claim and a record of a
    past error are not the same string" -- written after this exact mistake.
    """
    text = EPIC.read_text(encoding="utf-8")
    assert "omega_engine/crates/contract_core/nomos_urn.py" in text
    assert (REPO_ROOT / "omega_engine/crates/contract_core/nomos_urn.py").is_file()

    claimed_as_deliverable = [
        line for line in text.splitlines()
        if line.lstrip().startswith("- `omega_engine_governance/contracts/nomos_urn.py")
    ]
    assert not claimed_as_deliverable, (
        f"the epic still lists the nonexistent path as a deliverable: "
        f"{claimed_as_deliverable}"
    )


def test_both_implementations_of_the_grammar_exist():
    """Two implementations is the premise of the parity corpus."""
    assert (REPO_ROOT / "omega_engine/crates/contract_core/nomos_urn.py").is_file()
    assert (
        REPO_ROOT / "omega_engine/crates_rs/omega_contract_core/src/nomos_urn.rs"
    ).is_file()
