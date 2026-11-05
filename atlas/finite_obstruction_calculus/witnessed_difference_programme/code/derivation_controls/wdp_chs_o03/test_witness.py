from __future__ import annotations
from .witness import evaluate_wdp_chs_o03, witness_wdp_chs_o03

def test_wdp_chs_o03_scoped_control() -> None:
    summary = witness_wdp_chs_o03()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [2, 1, 4]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_wdp_chs_o03_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_wdp_chs_o03((2, 1 + 1, 4))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_wdp_chs_o03((True, 1, 4))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
