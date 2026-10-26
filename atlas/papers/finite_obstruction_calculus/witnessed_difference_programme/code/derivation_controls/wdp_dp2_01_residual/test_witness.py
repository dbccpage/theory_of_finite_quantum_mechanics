from __future__ import annotations
from .witness import check_single_witness_realization_rule, witness_wdp_dp2_01_residual

def test_wdp_dp2_01_residual_realization_rule() -> None:
    summary = witness_wdp_dp2_01_residual()
    assert summary["positive_status"] == "PASS"
    assert summary["realized_questions"] == ["q_parity", "q_sign"]
    assert summary["negative_status"] == "REFUSED"
    assert summary["negative_reason"] == "REALIZATION_COLLISION:q_parity"

def test_wdp_dp2_01_residual_refuses_missing_witness() -> None:
    res = check_single_witness_realization_rule({"q1": (0, 1)}, {})
    assert res.status == "REFUSED"
    assert res.reason == "MISSING_OR_MALFORMED_WITNESS:q1"
