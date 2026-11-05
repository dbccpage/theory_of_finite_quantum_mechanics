from __future__ import annotations
from .witness import evaluate_wdp_ch23_next_test, witness_wdp_ch23_next_test

def test_wdp_ch23_next_test_scoped_control() -> None:
    summary = witness_wdp_ch23_next_test()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [4, 4, 1]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_wdp_ch23_next_test_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_wdp_ch23_next_test((4, 4 + 1, 1))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_wdp_ch23_next_test((True, 4, 1))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
