from __future__ import annotations
from .witness import evaluate_ch19_o04, witness_ch19_o04

def test_ch19_o04_scoped_control() -> None:
    summary = witness_ch19_o04()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [3, 15, 20]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_ch19_o04_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_ch19_o04((3, 15 + 1, 20))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_ch19_o04((True, 15, 20))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
