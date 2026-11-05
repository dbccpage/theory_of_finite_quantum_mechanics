from __future__ import annotations

from .witness import witness


def test_witness() -> None:
    w = witness()
    assert w["goal_id"] == "PROD-P4"
    assert w["runtime_package"] == "omega_engine_cognitive_operations"
    assert w["planned_suite"] == ["I_pair01", "I_pair12"]
    assert w["planned_cost"] == "7/2"
    assert w["suite_verified"] is True
    assert w["future_preserving_cost"] == "15/4"
    assert w["static_safe_suite_cost"] == "6"
    assert w["beats_static_safe_suite"] is True
    assert w["infeasible_refused"] is True
    assert w["authority_effect"] == "None"
