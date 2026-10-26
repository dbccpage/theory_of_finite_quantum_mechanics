from __future__ import annotations
from .witness import evaluate_ms_po001_residual, witness_ms_po001_residual

def test_ms_po001_residual_scoped_control() -> None:
    summary = witness_ms_po001_residual()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [9, 9, 0]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_ms_po001_residual_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_ms_po001_residual((9, 9 + 1, 0))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_ms_po001_residual((True, 9, 0))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
