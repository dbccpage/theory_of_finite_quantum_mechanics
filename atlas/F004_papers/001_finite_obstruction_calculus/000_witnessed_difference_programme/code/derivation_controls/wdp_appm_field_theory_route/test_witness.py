from __future__ import annotations
from .witness import evaluate_wdp_appm_field_theory_route, witness_wdp_appm_field_theory_route

def test_wdp_appm_field_theory_route_scoped_control() -> None:
    summary = witness_wdp_appm_field_theory_route()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [5, 5, 0]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_wdp_appm_field_theory_route_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_wdp_appm_field_theory_route((5, 5 + 1, 0))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_wdp_appm_field_theory_route((True, 5, 0))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
