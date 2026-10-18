"""Every shipped workflow, composed against the operad it claims to use.

`EPIC-OE-OEWAS-004` deliverable 1 asks for a validator "checking port type
connectivity, input/output colour matching, and unreachable node absence", and
deliverable 2 for cycle obstruction detection.

A workflow declares a signature and a `pipeline` of `{slot, operation}` steps
where each operation names a skill. That is planar substitution applied in
sequence, so validation reuses sprint 014's algebra rather than inventing a
second one.

**All three shipped workflows were broken and nothing had composed them.** Five
operations named skills that do not exist, and two workflows declared a signature
their own pipeline cannot produce.

Three of the five had successors the estate itself documents and were repaired:
`omega-old-man-chatgpt-red-team` (the rename PR #187 made across `*.md`, which
never scanned `*.json`), and `github` / `0-oe-commit`, which `techne-github`'s
own SKILL.md records as "archived and consolidated here".

Repairing those surfaced the defect underneath: with both names resolving to
`techne-github`, `cppms_commit_sync_workflow` substitutes one skill into the same
slot twice. The consolidation turned a two-step pipeline into a repeated step and
nobody updated the workflow.

The remaining findings are pinned rather than fixed. `paper-build` and
`meta-law-contract-enforcer` have no unambiguous successor, and the two colour
mismatches are design decisions -- either the declared signature is wrong or the
pipeline is, and choosing is not an agent's call.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from omega_engine_workflows_agents_skills.domain.workflow_graph import (
    REQUIRED_WORKFLOW_KEYS,
    WorkflowError,
    detect_cycle,
    unknown_operations,
    validate_all,
    validate_workflow,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
WORKFLOWS = REPO_ROOT / ".agents" / "workflows"

# Measured after repairing the three documented renames. Pinned as a set so a
# sixth appearing -- or one of these being resolved -- is reported.
UNRESOLVED_OPERATIONS = ("meta-law-contract-enforcer", "paper-build")


@pytest.fixture(scope="module")
def reports():
    return validate_all()


# --------------------------------------------------------------------------
# The estate
# --------------------------------------------------------------------------


def test_every_shipped_workflow_is_validated(reports):
    """Anti-vacuity. An empty sweep is not a clean sweep."""
    assert len(reports) == 3


def test_the_repaired_operations_no_longer_appear(reports):
    """The three renames the estate documents.

    `omega-old-man-chatgpt-red-team` is the one PR #187 fixed across markdown and
    missed in JSON, because that fixer scanned only `*.md`.
    """
    remaining = unknown_operations(reports)
    for repaired in ("omega-old-man-chatgpt-red-team", "github", "0-oe-commit"):
        assert repaired not in remaining


def test_no_workflow_still_names_the_stale_red_team_skill():
    """Checked in the file rather than through the validator.

    The validator would report it as merely unknown; this asserts the specific
    rename landed in JSON, which is where PR #187's fixer could not reach.
    """
    for path in sorted(WORKFLOWS.glob("*.json")):
        text = path.read_text(encoding="utf-8")
        assert "omega-old-man-chatgpt-red-team" not in text, path.name


def test_the_unresolved_operations_are_the_two_already_known(reports):
    """Ratchet. The set may shrink; it may not grow.

    Neither has an unambiguous successor, so guessing one would put a name in a
    shipped workflow that no document supports.
    """
    assert unknown_operations(reports) == UNRESOLVED_OPERATIONS


def test_the_consolidation_left_a_duplicate_step(reports):
    """The defect repairing the names revealed.

    `github` and `0-oe-commit` were separate skills consolidated into
    `techne-github`. The workflow still invokes both, at the same slot, so one
    skill is now substituted twice into a port the first fill consumed.
    """
    cppms = next(r for r in reports if r.workflow_id == "cppms_commit_sync_workflow")
    cycles = [f for f in cppms.findings if f.code == "CYCLE_OBSTRUCTION"]
    assert len(cycles) == 1
    assert cycles[0].operation == "techne-github"


def test_two_workflows_declare_a_signature_their_pipeline_cannot_produce(reports):
    """Design decisions, pinned rather than fixed.

    Either the declared signature is wrong or the pipeline is, and choosing
    between them is not an agent's call.
    """
    mismatched = [
        r.workflow_id
        for r in reports
        if any(f.code == "COLOUR_MISMATCH" for f in r.findings)
    ]
    assert sorted(mismatched) == [
        "contract_compliance_audit_workflow",
        "paper_proof_release_workflow",
    ]


def test_no_workflow_is_currently_valid(reports):
    """Stated plainly, so a later green run is a real change.

    All three carry findings. Asserting that keeps the suite honest: if someone
    repairs one, this test fails and the count must be updated deliberately.
    """
    assert [r.is_valid for r in reports] == [False, False, False]


def test_every_workflow_declares_authority_effect_none(reports):
    """The one invariant all three already satisfy."""
    for report in reports:
        assert not [f for f in report.findings if f.code == "AUTHORITY"]


# --------------------------------------------------------------------------
# The validator itself
# --------------------------------------------------------------------------


def _write(tmp_path, name, payload):
    path = tmp_path / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def _valid_payload(**overrides):
    payload = {
        "workflow_id": "wf",
        "name": "test workflow",
        "source_colours": ["Code"],
        "target_colour": "Code",
        "pipeline": [{"slot": 0, "operation": "rip-code"}],
        "authority_effect": "None",
    }
    payload.update(overrides)
    return payload


def test_a_well_formed_workflow_validates(tmp_path):
    """The validator must be able to pass, or its findings prove nothing.

    A workflow whose declared inputs survive its own pipeline. `session`
    consumes ("State",) and produces "State", so substituting it into a State
    slot leaves the signature exactly as declared.
    """
    path = _write(
        tmp_path,
        "ok",
        _valid_payload(
            source_colours=["State"],
            target_colour="State",
            pipeline=[{"slot": 0, "operation": "session"}],
        ),
    )
    report = validate_workflow(path)
    assert report.is_valid, report.findings
    assert report.signature_matches


def test_an_unknown_operation_is_reported_with_its_step(tmp_path):
    path = _write(
        tmp_path,
        "bad",
        _valid_payload(pipeline=[{"slot": 0, "operation": "not-a-skill"}]),
    )
    report = validate_workflow(path)
    finding = report.findings[0]
    assert finding.code == "UNKNOWN_OPERATION"
    assert finding.step_index == 0
    assert finding.operation == "not-a-skill"


def test_a_colour_mismatch_is_reported(tmp_path):
    path = _write(
        tmp_path, "bad", _valid_payload(source_colours=["Paper"], target_colour="Paper")
    )
    report = validate_workflow(path)
    assert any(f.code == "COLOUR_MISMATCH" for f in report.findings)


def test_input_signature_drift_is_reported(tmp_path):
    """A pipeline can compose admissibly and still demand an undeclared input.

    Substituting `rip-code` -- which consumes ("Code", "Audit") -- into a
    single-Code workflow leaves the composite needing an Audit the declaration
    never mentioned. A caller supplying only what was declared would be short a
    port.

    The target colour is deliberately *not* what is checked: `substitute`
    returns theta's target, so comparing it against the declaration can never
    fail. A check that cannot fire is worse than no check, and this suite caught
    one in its own first draft.
    """
    path = _write(tmp_path, "drift", _valid_payload())
    report = validate_workflow(path)
    codes = {f.code for f in report.findings}
    assert "INPUT_SIGNATURE_DRIFT" in codes
    assert not report.signature_matches


def test_an_empty_pipeline_is_reported(tmp_path):
    path = _write(tmp_path, "empty", _valid_payload(pipeline=[]))
    report = validate_workflow(path)
    assert report.findings[0].code == "EMPTY_PIPELINE"


def test_a_non_none_authority_effect_is_reported(tmp_path):
    path = _write(tmp_path, "auth", _valid_payload(authority_effect="ACTION_LICENSE"))
    report = validate_workflow(path)
    assert any(f.code == "AUTHORITY" for f in report.findings)


@pytest.mark.parametrize("key", REQUIRED_WORKFLOW_KEYS)
def test_a_workflow_missing_any_required_key_is_refused(tmp_path, key):
    payload = _valid_payload()
    del payload[key]
    path = _write(tmp_path, "partial", payload)
    with pytest.raises(WorkflowError) as excinfo:
        validate_workflow(path)
    assert excinfo.value.code == "MISSING_KEYS"
    assert key in str(excinfo.value)


def test_malformed_json_is_refused(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{ not json", encoding="utf-8", newline="\n")
    with pytest.raises(WorkflowError, match="MALFORMED_JSON"):
        validate_workflow(path)


def test_a_missing_workflow_is_refused(tmp_path):
    with pytest.raises(WorkflowError, match="MISSING"):
        validate_workflow(tmp_path / "absent.json")


def test_an_empty_workflow_directory_is_refused(tmp_path):
    """An empty sweep must not read as a clean one."""
    with pytest.raises(WorkflowError, match="NO_WORKFLOWS"):
        validate_all(tmp_path)


def test_a_missing_workflow_directory_is_refused(tmp_path):
    with pytest.raises(WorkflowError, match="WORKFLOWS_MISSING"):
        validate_all(tmp_path / "absent")


# --------------------------------------------------------------------------
# Cycle detection
# --------------------------------------------------------------------------


def test_the_same_operation_at_the_same_slot_is_a_cycle():
    pipeline = [
        {"slot": 0, "operation": "a"},
        {"slot": 0, "operation": "a"},
    ]
    assert detect_cycle(pipeline) == ("a",)


def test_the_same_operation_at_different_slots_is_not_a_cycle():
    """Filling two distinct ports with one skill is ordinary composition."""
    pipeline = [
        {"slot": 0, "operation": "a"},
        {"slot": 1, "operation": "a"},
    ]
    assert detect_cycle(pipeline) == ()


def test_different_operations_at_one_slot_are_not_a_cycle():
    pipeline = [
        {"slot": 0, "operation": "a"},
        {"slot": 0, "operation": "b"},
    ]
    assert detect_cycle(pipeline) == ()


def test_a_repeated_operation_is_reported_once():
    pipeline = [{"slot": 0, "operation": "a"}] * 4
    assert detect_cycle(pipeline) == ("a",)
