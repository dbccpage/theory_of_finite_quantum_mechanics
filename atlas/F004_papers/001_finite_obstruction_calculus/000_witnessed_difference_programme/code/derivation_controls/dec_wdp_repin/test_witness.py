from __future__ import annotations
from .witness import evaluate_dec_wdp_repin, witness_dec_wdp_repin

def test_dec_wdp_repin_scoped_control() -> None:
    summary = witness_dec_wdp_repin()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [2183, 2184, 1]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_dec_wdp_repin_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_dec_wdp_repin((2183, 2184 + 1, 1))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_dec_wdp_repin((True, 2184, 1))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
