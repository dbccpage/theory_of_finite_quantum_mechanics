from __future__ import annotations
from .witness import evaluate_po001_native_transport, witness_po001_native_transport

def test_po001_native_transport_scoped_control() -> None:
    summary = witness_po001_native_transport()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [4, 3, 1]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_po001_native_transport_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_po001_native_transport((4, 3 + 1, 1))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_po001_native_transport((True, 3, 1))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
