"""
Direct Unit Regression Tests for Remediation of M1-M4 Findings from 1 October 2026 Publication Review.

Tests:
- M1: verify_full_coverage refuses proper sub-boxes and overlapping leaves.
- M2: verify_a4 and verify_a6 refuse unbound evidence and truthy string flags.
- M3: packet_firewall refuses invalid hash format, off-carrier result states, and enforces custom alphabet.
- M4: l1_governor refuses EDGE_MATCH on undeclared vertices and undeclared edges.
"""

from fractions import Fraction as Q
import hashlib
import pytest

from mub_verify.interval import RationalInterval as I
from mub_verify.cover import (
    gauge_fixed_torus_region,
    verify_full_coverage,
)
from mub_verify.mub6_proposer import (
    MUB6ProposerHost,
    SessionResult,
    scripted_proposer,
)
from mub_verify.packet_firewall import (
    PacketFirewallHost,
    DerivationStep,
    FirewallRefusalCode,
)
from mub_verify.l1_governor import (
    ConstraintGraph,
    Edge,
    L1SymbolGameGovernor,
)


def test_m1_sub_box_refused():
    """M1: Proper sub-box on 11D active coordinates must be refused (volume mismatch)."""
    domain = gauge_fixed_torus_region()
    leaf = list(domain)
    leaf[2] = I(Q(-41, 100), 0)
    ok, msg = verify_full_coverage(domain, [tuple(leaf)], [])
    assert not ok
    assert "Volume mismatch" in msg


def test_m1_duplicated_leaves_refused():
    """M1: Duplicated leaves must be refused by relative interior overlap check regardless of leaf count."""
    cube = tuple(I(0, 1) for _ in range(12))
    slab = (I(0, Q(1, 201)),) + cube[1:]
    ok, msg = verify_full_coverage(cube, [slab] * 201, [])
    assert not ok
    assert "overlap in interior" in msg


def test_m2_a4_unbound_negative_scalar_refused():
    """M2: Unbound 1x1 negative scalar [[Fraction(-1)]] must be refused by A4 verifier."""
    a4 = MUB6ProposerHost(scripted_proposer(["[[Fraction(-1)]]"]))
    res = a4.verify_a4()
    assert res.terminal_status == "REFUSED"
    assert res.admitted == 0


def test_m2_a6_truthy_string_refused():
    """M2: Truthy string flag {'consistent': 'false'} must be refused by A6 verifier."""
    a6 = MUB6ProposerHost(scripted_proposer(["{'consistent': 'false'}"]))
    res = a6.verify_a6()
    assert res.terminal_status == "REFUSED"
    assert res.admitted == 0


def test_m2_a6_bare_boolean_without_equations_refused():
    """M2: Bare boolean {'consistent': True} without phase-transition equations must be refused."""
    a6 = MUB6ProposerHost(scripted_proposer(["{'consistent': True}"]))
    res = a6.verify_a6()
    assert res.terminal_status == "REFUSED"


def test_m3_preflight_invalid_hashes_refused():
    """M3: Preflight verify_step must refuse invalid hash format."""
    host = PacketFirewallHost()
    step = DerivationStep("VERIFY", 0, "r", {}, "bad", "bad", "VERIFY")
    verdict = host.verify_step(step, {"r": None})
    assert not verdict.admitted
    assert verdict.refusal_code == FirewallRefusalCode.HASH_MISMATCH


def test_m3_pipeline_off_carrier_result_refused():
    """M3: Pipeline must refuse transitions whose resulting state is off-carrier."""
    host = PacketFirewallHost()
    digest = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()
    result = "\U0001f600"
    step = DerivationStep("VERIFY", 0, "r", {}, digest("old"), digest(result), "VERIFY")
    assert not host.check_fw_carrier(result).admitted
    pipeline_verdict = host.evaluate_pipeline("old", step, {"r": None}, lambda *args: result)
    assert not pipeline_verdict.admitted
    assert pipeline_verdict.refusal_code == FirewallRefusalCode.FW_CARRIER_VIOLATION


def test_m3_custom_alphabet_restriction():
    """M3: Pinned custom alphabet must strictly restrict allowable characters."""
    host = PacketFirewallHost(carrier_alphabet={"a", "b"})
    assert host.check_fw_carrier("ab").admitted
    assert not host.check_fw_carrier("Z").admitted


def test_m4_governor_ghost_edge_refused():
    """M4: Governor step_verify must refuse EDGE_MATCH on undeclared edge/vertices."""
    graph = ConstraintGraph(["u", "v"], [Edge("u", "v", Q(1))])
    governor = L1SymbolGameGovernor(graph)
    verdict = governor.step_verify("EDGE_MATCH:ghost,other_ghost")
    assert not verdict.admitted
    assert "not declared" in verdict.details


def test_m4_governor_unasserted_edge_refused():
    """M4: Governor step_verify must refuse EDGE_MATCH on declared edge with no asserted claim."""
    graph = ConstraintGraph(["u", "v"], [Edge("u", "v", Q(1))])
    governor = L1SymbolGameGovernor(graph)
    verdict = governor.step_verify("EDGE_MATCH:u,v")
    assert not verdict.admitted
    assert "no asserted claim" in verdict.details


def test_m5_session_result_value_object_exact_type_equality():
    """M5: SessionResult domain Value Object enforces exact-type equality and immutability."""
    res1 = SessionResult(terminal_status="ADMITTED", admitted=1, refused=0, turn_records=[{"turn": 1}])
    res2 = SessionResult(terminal_status="ADMITTED", admitted=1, refused=0, turn_records=({"turn": 1},))
    res_diff = SessionResult(terminal_status="REFUSED", admitted=0, refused=1, turn_records=())

    assert res1 == res2
    assert res1 != res_diff

    fake_dict = {"terminal_status": "ADMITTED", "admitted": 1, "refused": 0, "turn_records": ({"turn": 1},)}
    assert res1 != fake_dict
    assert res1 != "ADMITTED"
    assert res1 != 42
    assert res1 is not None

    with pytest.raises(Exception):
        res1.terminal_status = "MUTATED"

