from __future__ import annotations
from .witness import evaluate_plan_7d_csq_character_classification, witness_plan_7d_csq_character_classification

def test_plan_7d_csq_character_classification_scoped_control() -> None:
    summary = witness_plan_7d_csq_character_classification()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [8, 8, 1]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_plan_7d_csq_character_classification_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_plan_7d_csq_character_classification((8, 8 + 1, 1))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_plan_7d_csq_character_classification((True, 8, 1))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
