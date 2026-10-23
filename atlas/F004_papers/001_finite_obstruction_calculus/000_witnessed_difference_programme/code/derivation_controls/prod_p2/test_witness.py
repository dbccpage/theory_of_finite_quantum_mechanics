from __future__ import annotations

from .witness import witness


def test_witness() -> None:
    w = witness()
    assert w["goal_id"] == "PROD-P2"
    assert w["runtime_package"] == "omega_engine_cognitive_operations"
    assert w["stage"] == "measurement"
    assert w["replay_verified"] is True
    assert w["negative_uncertainty_refused"] is True
    assert w["unmapped_key_refused"] is True
    assert w["authority_effect"] == "None"
