from __future__ import annotations
from .witness import evaluate_wdp_appw_native_repair_bindings, witness_wdp_appw_native_repair_bindings

def test_wdp_appw_native_repair_bindings_scoped_control() -> None:
    summary = witness_wdp_appw_native_repair_bindings()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [6, 2, 0]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_wdp_appw_native_repair_bindings_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_wdp_appw_native_repair_bindings((6, 2 + 1, 0))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_wdp_appw_native_repair_bindings((True, 2, 0))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
