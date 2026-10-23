from __future__ import annotations
from .witness import evaluate_plan_7d_csq_pontryagin, witness_plan_7d_csq_pontryagin

def test_plan_7d_csq_pontryagin_scoped_control() -> None:
    summary = witness_plan_7d_csq_pontryagin()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [6, 4, 2]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_plan_7d_csq_pontryagin_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_plan_7d_csq_pontryagin((6, 4 + 1, 2))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_plan_7d_csq_pontryagin((True, 4, 2))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
