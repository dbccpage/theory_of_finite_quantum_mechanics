from __future__ import annotations
from .witness import evaluate_plan_odm_6_pr426, witness_plan_odm_6_pr426

def test_plan_odm_6_pr426_scoped_control() -> None:
    summary = witness_plan_odm_6_pr426()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [2, 3, 36]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_plan_odm_6_pr426_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_plan_odm_6_pr426((2, 3 + 1, 36))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_plan_odm_6_pr426((True, 3, 36))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
