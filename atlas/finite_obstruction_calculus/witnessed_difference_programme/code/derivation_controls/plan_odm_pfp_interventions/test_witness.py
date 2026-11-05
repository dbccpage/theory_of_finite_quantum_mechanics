from __future__ import annotations
from .witness import evaluate_plan_odm_pfp_interventions, witness_plan_odm_pfp_interventions

def test_plan_odm_pfp_interventions_scoped_control() -> None:
    summary = witness_plan_odm_pfp_interventions()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [5, 0, 1]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_plan_odm_pfp_interventions_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_plan_odm_pfp_interventions((5, 0 + 1, 1))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_plan_odm_pfp_interventions((True, 0, 1))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
