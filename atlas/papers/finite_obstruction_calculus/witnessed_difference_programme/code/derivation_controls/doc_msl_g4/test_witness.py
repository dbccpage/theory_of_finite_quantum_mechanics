from __future__ import annotations
from .witness import evaluate_doc_msl_g4, witness_doc_msl_g4

def test_doc_msl_g4_scoped_control() -> None:
    summary = witness_doc_msl_g4()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [6, 4, 1]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_doc_msl_g4_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_doc_msl_g4((6, 4 + 1, 1))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_doc_msl_g4((True, 4, 1))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
