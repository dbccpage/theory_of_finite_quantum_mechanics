from __future__ import annotations
from .witness import evaluate_gen_wdp_o03, witness_gen_wdp_o03

def test_gen_wdp_o03_scoped_control() -> None:
    summary = witness_gen_wdp_o03()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [3, 3, 1]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_gen_wdp_o03_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_gen_wdp_o03((3, 3 + 1, 1))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_gen_wdp_o03((True, 3, 1))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
