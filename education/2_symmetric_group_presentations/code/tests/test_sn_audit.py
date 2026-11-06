"""Targeted unit test suite for canonical sn_audit.py.

AuthorityEffect: None. GenesisEffect: None.
Verifies:
1. Wire v1 and v2 parsing and rendering.
2. Balanced Gamma38 packet parsing and rendering.
3. Tagged codec round trips (e.g. rational, legacy bodycut, nested lifts).
4. Mathematical WIR verification (endpoint support Delta_w = 2, witness occurrences, irreflexivity).
5. Chromatic separation tag searches (single pair, triangle, 4-cycle, budget gate).
6. Contract schema validation against normal_form_contract_schema.yaml across all 5 domain contracts.
7. Explicit detection of schema defect regressions.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE_DIR = HERE.parent
REPO = HERE.parents[4]
NORMAL_FORMS_DIR = CODE_DIR.parent / "normal_forms"
SCHEMA_PATH = NORMAL_FORMS_DIR / "normal_form_contract_schema.yaml"

sys.path.insert(0, str(CODE_DIR))

import pytest
from sn_audit import (
    SN,
    atom,
    decode_sn,
    encode_sn,
    load_yaml,
    minimum_tag_values,
    parse_packet,
    parse_sn,
    render_packet,
    render_sn,
    term,
    validate_contract,
    verify_wir,
    wire_issue,
)

# ---------------------------------------------------------------------------
# 1. Wire Profiles: v1 and v2 Parsing & Rendering
# ---------------------------------------------------------------------------


def test_wire_v1_parsing_and_rendering():
    cases = [
        ("<>", SN("ground")),
        ("NON_DESCENT", SN("non_descent")),
        ("<a>", SN("mark", ("a",))),
        ("<ab>", SN("pair", ("a", "b"))),
        ("<a->b>", SN("cut", ("a", "b"))),
        ("[a,b]", SN("simplex", ("a", "b"))),
        ("u_6<a->b>", SN("u", ("6", SN("legacy_body", ("a->b",))))),
        ("r_6<ab>", SN("r", ("6", SN("legacy_body", ("ab",))))),
    ]
    for wire, expected_node in cases:
        node = parse_sn(wire, "sn-wire-v1")
        assert node == expected_node
        assert render_sn(node, "sn-wire-v1") == wire
        assert wire_issue(wire, "sn-wire-v1") is None


def test_wire_v2_recursive_parsing_and_rendering():
    cases = [
        ("u_0<<>>", SN("u", ("0", SN("ground")))),
        ("r_6<u_6<<ab>>>", SN("r", ("6", SN("u", ("6", SN("pair", ("a", "b"))))))),
    ]
    for wire, expected_node in cases:
        node = parse_sn(wire, "sn-wire-v2")
        assert node == expected_node
        assert render_sn(node, "sn-wire-v2") == wire
        assert wire_issue(wire, "sn-wire-v2") is None


def test_wire_profile_rejection():
    # Nested lift is rejected under v1
    with pytest.raises(ValueError, match="Outside sn-wire-v1"):
        parse_sn("r_6<u_6<<ab>>>", "sn-wire-v1")
    assert wire_issue("r_6<u_6<<ab>>>", "sn-wire-v1") is not None

    # Unknown profiles raise ValueError
    with pytest.raises(ValueError, match="Declare sn-wire-v1 or sn-wire-v2"):
        parse_sn("<>", "unknown-profile")


# ---------------------------------------------------------------------------
# 2. Balanced Packet Syntax & Strict Gamma38 Wire
# ---------------------------------------------------------------------------


def test_packet_parsing_and_rendering():
    parsed = parse_packet("<<rat><pos><1><1>>")
    assert parsed.kind == "composite"
    rendered = render_packet(parsed)
    assert rendered == "<<rat><pos><1><1>>"


def test_tagged_codec_rational():
    rational = term("rat", atom("pos"), atom("1"), atom("1"))
    assert render_packet(rational) == "<<rat><pos><1><1>>"


def test_tagged_codec_v1_legacy_body_roundtrip():
    source = parse_sn("u_6<a->b>", "sn-wire-v1")
    code = encode_sn(source)
    assert render_packet(code) == "<<u><6><<bodycut><a><b>>>"
    assert decode_sn(code, "sn-wire-v1") == source


def test_tagged_codec_v2_nested_roundtrip():
    nested = parse_sn("r_6<u_6<<ab>>>", "sn-wire-v2")
    code = encode_sn(nested)
    assert decode_sn(code, "sn-wire-v2") == nested


# ---------------------------------------------------------------------------
# 3. Mathematical WIR Verification (Endpoint Support & Multiplicity)
# ---------------------------------------------------------------------------


def test_verify_wir_single_oriented():
    # Asymmetric single-oriented witness consistent with PrimDiff.single_oriented_witness_consistent
    res = verify_wir(("false", "true"), {("false", "true"): 1, ("true", "false"): 0})
    assert res == {
        "carrier_size": 2,
        "primitive_endpoint_arity": 2,
        "asserted_pair_count": 1,
        "witness_occurrence_count": 1,
    }


def test_verify_wir_symmetric_multi_witness():
    res = verify_wir(("a", "b"), {("a", "b"): 2, ("b", "a"): 1})
    assert res == {
        "carrier_size": 2,
        "primitive_endpoint_arity": 2,
        "asserted_pair_count": 2,
        "witness_occurrence_count": 3,
    }


def test_verify_wir_self_loop_refused():
    with pytest.raises(ValueError, match="Irreflexivity violated"):
        verify_wir(("a", "b"), {("a", "a"): 1})


def test_verify_wir_duplicate_carrier_identities_refused():
    with pytest.raises(ValueError, match="Carrier identities must be unique"):
        verify_wir(("a", "a"), {("a", "b"): 1})


def test_verify_wir_no_inhabited_primitive_distinction():
    with pytest.raises(ValueError, match="No inhabited primitive distinction"):
        verify_wir(("a", "b"), {("a", "b"): 0})


# ---------------------------------------------------------------------------
# 4. Chromatic Separation Tag Searches (Observation Collisions)
# ---------------------------------------------------------------------------


def test_minimum_tag_values_single_pair():
    # Single pair requires chromatic number 2
    assert minimum_tag_values(("a", "b"), (("a", "b"),)) == 2


def test_minimum_tag_values_triangle():
    # 3-cycle (triangle) requires chromatic number 3
    triangle_edges = (("a", "b"), ("b", "c"), ("a", "c"))
    assert minimum_tag_values(("a", "b", "c"), triangle_edges) == 3


def test_minimum_tag_values_even_cycle():
    # 4-cycle (even cycle) is bipartite, requiring chromatic number 2
    c4_edges = (("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"))
    assert minimum_tag_values(("a", "b", "c", "d"), c4_edges) == 2


def test_minimum_tag_values_budget_exceeded():
    with pytest.raises(ValueError, match="Declared finite search budget exceeded"):
        minimum_tag_values(("a", "b", "c", "d", "e", "f", "g"), ())


# ---------------------------------------------------------------------------
# 5. Contract Schema Alignment & Validation
# ---------------------------------------------------------------------------


def test_validate_all_normal_form_contracts():
    schema = load_yaml(SCHEMA_PATH)
    contracts = [p.name for p in sorted(NORMAL_FORMS_DIR.glob("nf.*.yaml"))]
    assert len(contracts) == 8
    for contract_file in contracts:
        path = NORMAL_FORMS_DIR / contract_file
        assert path.is_file(), f"Missing contract {contract_file}"
        contract_data = load_yaml(path)
        issues = validate_contract(contract_data, schema)
        assert issues == [], f"Validation findings in {contract_file}: {issues}"


def test_validate_contract_detects_schema_defect():
    schema = load_yaml(SCHEMA_PATH)
    contract_data = load_yaml(NORMAL_FORMS_DIR / "nf.epistemic.pvnf.yaml")
    # Simulate defect: missing loss_ledger_trigger_id when required
    del contract_data["certification"]["loss_ledger_trigger_id"]
    issues = validate_contract(contract_data, schema)
    assert any("Missing certification.loss_ledger_trigger_id" in issue for issue in issues)
