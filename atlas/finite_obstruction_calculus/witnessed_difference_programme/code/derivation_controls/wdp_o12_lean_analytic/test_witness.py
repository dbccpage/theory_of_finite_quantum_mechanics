from __future__ import annotations
from .witness import evaluate_wdp_o12_lean_analytic, witness_wdp_o12_lean_analytic

def test_wdp_o12_lean_analytic_scoped_control() -> None:
    summary = witness_wdp_o12_lean_analytic()
    assert summary["positive_status"] == "PASS"
    assert summary["invariant_tuple"] == [1, 256, 127]
    assert summary["mismatch_status"] == "REFUSED"
    assert summary["promotion_status"] == "REFUSED"
    assert summary["promotion_reason"] == "UNRESTRICTED_PROMOTION_REFUSED"

def test_wdp_o12_lean_analytic_refuses_boolean_and_drifted_inputs() -> None:
    drifted = evaluate_wdp_o12_lean_analytic((1, 256 + 1, 127))
    assert drifted.status == "REFUSED"
    assert drifted.reason == "INVARIANT_MISMATCH_ON_DECLARED_CARRIER"
    bool_in = evaluate_wdp_o12_lean_analytic((True, 256, 127))  # type: ignore[arg-type]
    assert bool_in.status == "REFUSED"
    assert bool_in.reason == "NON_INTEGER_CARRIER_REFUSED"
