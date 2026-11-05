from __future__ import annotations

from .witness import witness


def test_witness() -> None:
    w = witness()
    assert w["goal_id"] == "PROD-P1"
    assert w["runtime_package"] == "omega_engine_pfp"
    assert w["out_of_fuel_label"] == "Exhausted"
    assert w["terminated_label"] == "ResolvedWithinBudget"
    assert w["impossible_label"] == "Impossible"
    assert w["initial_value"] == "3"
    assert w["quotient_state_count"] < w["raw_state_count"]
    assert w["quotient_verified"] is True
    assert w["authority_effect"] == "None"
