from __future__ import annotations
from .witness import evaluate_wdp_21_8_lean_extension, witness_wdp_21_8_lean_extension

def test_wdp_21_8_lean_extension_scoped_control() -> None:
    summary = witness_wdp_21_8_lean_extension()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [154, 124, 30]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_wdp_21_8_lean_extension_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_wdp_21_8_lean_extension((154, 124 + 1, 30))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_wdp_21_8_lean_extension((True, 124, 30))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
