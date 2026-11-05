from __future__ import annotations
from .witness import evaluate_wdp_appx_cost_formalization, witness_wdp_appx_cost_formalization

def test_wdp_appx_cost_formalization_scoped_control() -> None:
    summary = witness_wdp_appx_cost_formalization()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [3, 3, 8]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_wdp_appx_cost_formalization_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_wdp_appx_cost_formalization((3, 3 + 1, 8))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_wdp_appx_cost_formalization((True, 3, 8))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
