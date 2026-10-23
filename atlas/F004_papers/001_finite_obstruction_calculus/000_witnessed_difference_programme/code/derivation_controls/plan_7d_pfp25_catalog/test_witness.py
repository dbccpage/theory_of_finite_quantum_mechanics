from __future__ import annotations
from .witness import evaluate_plan_7d_pfp25_catalog, witness_plan_7d_pfp25_catalog

def test_plan_7d_pfp25_catalog_scoped_control() -> None:
    summary = witness_plan_7d_pfp25_catalog()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [25, 7, 0]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_plan_7d_pfp25_catalog_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_plan_7d_pfp25_catalog((25, 7 + 1, 0))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_plan_7d_pfp25_catalog((True, 7, 0))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
