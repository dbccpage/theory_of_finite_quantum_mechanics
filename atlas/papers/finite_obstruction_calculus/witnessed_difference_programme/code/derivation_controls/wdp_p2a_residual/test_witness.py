from __future__ import annotations
from .witness import audit_single_witness_sufficiency, witness_wdp_p2a_residual

def test_wdp_p2a_residual_single_witness_sufficiency() -> None:
    summary = witness_wdp_p2a_residual()
    assert summary["positive_status"] == "PASS"
    assert summary["positive_sufficient"] is True
    assert summary["negative_status"] == "REFUSED"
    assert summary["negative_collisions"] == [["s0", "s1"]]

def test_wdp_p2a_residual_refuses_empty_carrier() -> None:
    empty = audit_single_witness_sufficiency((), {}, {})
    assert empty.status == "REFUSED"
    assert empty.reason == "EMPTY_STATE_CARRIER"
