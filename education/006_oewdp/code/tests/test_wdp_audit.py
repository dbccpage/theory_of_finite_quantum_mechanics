"""Targeted unit tests for wdp_audit.py stage transition audit harness.

AuthorityEffect: None. GenesisEffect: None.
Verifies:
1. WDP wire validation and issue detection.
2. Mathematical WIR verification under nf.wdp.wdnf invariants (Delta_support = 2, irreflexivity).
3. Linking of WDP difference events directly to S(n) Postnikov tower obstruction resolution steps.
4. Terminal route dispatch (AcceptWitnessedDifference, RejectSelfDifference, RequireSupportDeclaration, RejectGhostDistinction).
5. Fail-closed typed refusal handling (refusal<code>).
6. Full S(0) through S(6) stage transition chain auditing.
7. Normal form contract validation against normal_form_contract_schema.yaml.
8. Markdown ```wdp code fence audit.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

MODULE_ROOT = next(
    (
        p
        for p in Path(__file__).resolve().parents
        if (p / "levels").is_dir() or (p / "grammar").is_dir()
    ),
    Path(__file__).resolve().parents[2],
)
REPO_ROOT = next(
    (
        p
        for p in Path(__file__).resolve().parents
        if (p / ".git").exists() or (p / "pixi.toml").exists()
    ),
    Path(__file__).resolve().parents[5],
)
CODE_DIR = MODULE_ROOT / "code"
NORMAL_FORMS_DIR = MODULE_ROOT / "normal_forms"

if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from wdp_audit import (
    audit_markdown,
    audit_stage_sequence,
    audit_stage_transition,
    load_yaml,
    validate_contract,
    verify_wdp_wir,
    wire_issue,
)
from wdp_codec import (
    DistinctCut,
    Glyph,
)

# ---------------------------------------------------------------------------
# 1. Wire Issue Checking
# ---------------------------------------------------------------------------


def test_wire_issue_valid():
    valid_wires = [
        "<a!=b>",
        "<x,y>",
        "quot<a/fiber1>",
        "d0(t)",
        "d1(a,b)",
        "H(a,b)",
        "witness<fiber:w1,status:EXACT_REPAIR>",
        "balance<sites:2,trace:1>",
        "refusal<ERR_FIBER_NON_CONSTANT>",
    ]
    for w in valid_wires:
        assert wire_issue(w) is None


def test_wire_issue_invalid():
    invalid_wires = [
        "<a=b>",
        "d0()",
        "witness<fiber:w,status:INVALID>",
        "refusal<UNKNOWN>",
        "",
        "bad_token",
    ]
    for w in invalid_wires:
        assert wire_issue(w) is not None


# ---------------------------------------------------------------------------
# 2. Mathematical WIR Verification (Delta_support = 2, Irreflexivity)
# ---------------------------------------------------------------------------


def test_verify_wdp_wir_valid():
    res = verify_wdp_wir(carrier=("a", "b"), counts={("a", "b"): 1, ("b", "a"): 0})
    assert res["carrier_size"] == 2
    assert res["primitive_endpoint_arity"] == 2
    assert res["asserted_pair_count"] == 1
    assert res["witness_occurrence_count"] == 1
    assert res["terminal_route"] == "AcceptWitnessedDifference"


def test_verify_wdp_wir_self_difference_violation():
    with pytest.raises(ValueError, match="Irreflexivity violated: self-difference claimed"):
        verify_wdp_wir(carrier=("a", "b"), counts={("a", "a"): 1})


def test_verify_wdp_wir_subsingleton_violation():
    with pytest.raises(ValueError, match="Subsingleton distinction violation: \\|carrier\\| < 2"):
        verify_wdp_wir(carrier=("a",), counts={("a", "a"): 0})


def test_verify_wdp_wir_undeclared_endpoint():
    with pytest.raises(ValueError, match="Undeclared endpoint"):
        verify_wdp_wir(carrier=("a", "b"), counts={("a", "c"): 1})


# ---------------------------------------------------------------------------
# 3. Postnikov Stage Transition & Obstruction Linking
# ---------------------------------------------------------------------------


def test_stage_0_to_1_ground_supply():
    receipt = audit_stage_transition(
        from_stage=0,
        to_stage=1,
        event="d0(t)",
        carrier=("t",),
    )
    assert receipt.passed
    assert receipt.obstruction_id == "W0_EMPTY_CARRIER"
    assert receipt.terminal_route == "AcceptWitnessedDifference"


def test_stage_1_to_2_pair_supply():
    receipt = audit_stage_transition(
        from_stage=1,
        to_stage=2,
        event="<x,y>",
        carrier=("x", "y"),
    )
    assert receipt.passed
    assert receipt.obstruction_id == "W1_SUBSINGLETON_INSEPARABILITY"
    assert receipt.delta_support == 2
    assert receipt.terminal_route == "AcceptWitnessedDifference"


def test_stage_2_to_3_primitive_cut():
    receipt = audit_stage_transition(
        from_stage=2,
        to_stage=3,
        event="<a!=b>",
        carrier=("a", "b"),
    )
    assert receipt.passed
    assert receipt.obstruction_id == "W2_UNWITNESSED_RELATION"
    assert receipt.delta_support == 2
    assert receipt.terminal_route == "AcceptWitnessedDifference"


def test_stage_3_to_4_boundary_transport():
    receipt = audit_stage_transition(
        from_stage=3,
        to_stage=4,
        event="d1(a,b)",
        carrier=("a", "b"),
    )
    assert receipt.passed
    assert receipt.obstruction_id == "W3_BOUNDARY_CYCLE_DEFICIT"


def test_stage_4_to_5_homotopy_filler():
    receipt = audit_stage_transition(
        from_stage=4,
        to_stage=5,
        event="H(a,b)",
        carrier=("a", "b"),
    )
    assert receipt.passed
    assert receipt.obstruction_id == "W4_HARMONIC_1_RESIDUAL"


def test_stage_5_to_6_quotient_witness_closure():
    receipt = audit_stage_transition(
        from_stage=5,
        to_stage=6,
        event="witness<fiber:w1,status:EXACT_REPAIR>",
        carrier=("a", "b"),
    )
    assert receipt.passed
    assert receipt.obstruction_id == "W5_OPEN_OBSTRUCTION_DESCENT"


# ---------------------------------------------------------------------------
# 4. Failure Modes and Terminal Route Verification
# ---------------------------------------------------------------------------


def test_transition_self_difference_rejection():
    # Cut with identical endpoints <a!=a>
    ast = DistinctCut(first=Glyph("a"), second=Glyph("a"))
    receipt = audit_stage_transition(
        from_stage=2,
        to_stage=3,
        event=ast,
        carrier=("a",),
    )
    assert not receipt.passed
    assert receipt.terminal_route == "RejectSelfDifference"
    assert "Self-difference violation" in receipt.diagnosis


def test_transition_subsingleton_floor_refusal():
    receipt = audit_stage_transition(
        from_stage=2,
        to_stage=3,
        event="<a!=b>",
        carrier=("a",),  # Carrier size 1 violates floor |carrier| >= 2
    )
    assert not receipt.passed
    assert receipt.terminal_route == "RequireSupportDeclaration"
    assert "Subsingleton distinction violation" in receipt.diagnosis


def test_transition_open_obstruction_flag():
    receipt = audit_stage_transition(
        from_stage=5,
        to_stage=6,
        event="witness<fiber:w1,status:OPEN_OBSTRUCTION>",
        carrier=("a", "b"),
    )
    assert not receipt.passed
    assert receipt.terminal_route == "RequireSupportDeclaration"
    assert "Obstruction unresolved" in receipt.diagnosis


def test_transition_fail_closed_typed_refusal():
    receipt = audit_stage_transition(
        from_stage=5,
        to_stage=4,
        event="refusal<ERR_FIBER_NON_CONSTANT>",
        carrier=("a", "b"),
    )
    assert receipt.passed  # Verified typed refusal terminal
    assert receipt.is_descent
    assert receipt.terminal_route == "RequireSupportDeclaration"
    assert "Fail-closed typed refusal emitted" in receipt.diagnosis


def test_transition_malformed_wire():
    receipt = audit_stage_transition(
        from_stage=2,
        to_stage=3,
        event="<a=b>",
    )
    assert not receipt.passed
    assert receipt.terminal_route == "RejectGhostDistinction"
    assert "Malformed WDP wire token" in receipt.diagnosis


# ---------------------------------------------------------------------------
# 5. Full Stage Transition Sequence Audit
# ---------------------------------------------------------------------------


def test_full_postnikov_stage_sequence():
    steps = [
        (0, 1, "d0(t)", ("t",)),
        (1, 2, "<x,y>", ("x", "y")),
        (2, 3, "<x!=y>", ("x", "y")),
        (3, 4, "d1(x,y)", ("x", "y")),
        (4, 5, "H(x,y)", ("x", "y")),
        (5, 6, "witness<fiber:w1,status:EXACT_REPAIR>", ("x", "y")),
    ]
    receipts = audit_stage_sequence(steps)
    assert len(receipts) == 6
    for idx, r in enumerate(receipts):
        assert r.passed, f"Step {idx} failed: {r.issues}"
        assert r.from_stage == idx
        assert r.to_stage == idx + 1


# ---------------------------------------------------------------------------
# 6. Normal Form Contract Validation
# ---------------------------------------------------------------------------


def test_audit_wdnf_contract():
    schema = load_yaml(NORMAL_FORMS_DIR / "normal_form_contract_schema.yaml")
    contract = load_yaml(NORMAL_FORMS_DIR / "nf.wdp.wdnf.yaml")
    issues = validate_contract(contract, schema)
    assert issues == [], f"Found issues in nf.wdp.wdnf.yaml: {issues}"


def test_audit_executable_normal_form_contracts():
    schema = load_yaml(NORMAL_FORMS_DIR / "normal_form_contract_schema.yaml")
    executable_contracts = [
        "nf.wdp.wdnf.yaml",
        "nf.derivation.pdnf.yaml",
        "nf.derivation.obnf.yaml",
        "nf.derivation.scnf.yaml",
        "nf.coda.tsnf.yaml",
        "nf.cochain.dhnf.yaml",
        "nf.fsp.bssnf.yaml",
        "nf.fsp.micnf.yaml",
        "nf.coda.eqnf.yaml",
    ]
    for c_name in executable_contracts:
        c_path = NORMAL_FORMS_DIR / c_name
        assert c_path.is_file(), f"Missing contract {c_name}"
        data = load_yaml(c_path)
        issues = validate_contract(data, schema)
        assert issues == [], f"Validation findings in {c_name}: {issues}"


def test_validate_contract_detects_defect():
    schema = {
        "required_top_level_sections": ["identity", "terminal_routes", "terminal_route_map"],
        "contract_kinds": {"enum": ["form_contract"]},
        "section_definitions": {
            "identity": {"required_fields": ["id", "version"]},
        },
        "canonical_terminals": {"enum": ["Preserve", "Reject", "Refuse"]},
    }
    bad_contract = {
        "contract_kind": "form_contract",
        "identity": {"id": "test.id"},  # missing version
        "terminal_routes": ["RouteA"],
        "terminal_route_map": {"RouteA": "UnknownTerminal"},
    }
    issues = validate_contract(bad_contract, schema)
    assert "Missing identity.version" in issues
    assert "Unknown canonical terminal" in issues


# ---------------------------------------------------------------------------
# 7. Markdown Fence Audit
# ---------------------------------------------------------------------------


def test_audit_markdown_valid(tmp_path: Path):
    doc = tmp_path / "test_doc.md"
    doc.write_text(
        "# Example Document\n\n```wdp\n<a!=b>\nd0(x)\n```\n",
        encoding="utf-8",
    )
    findings = audit_markdown(doc)
    assert findings == []


def test_audit_markdown_detects_invalid_token(tmp_path: Path):
    doc = tmp_path / "test_invalid.md"
    doc.write_text(
        "# Example Document\n\n```wdp\n<a=b>\n```\n",
        encoding="utf-8",
    )
    findings = audit_markdown(doc)
    assert len(findings) == 1
    assert findings[0]["token"] == "<a=b>"
