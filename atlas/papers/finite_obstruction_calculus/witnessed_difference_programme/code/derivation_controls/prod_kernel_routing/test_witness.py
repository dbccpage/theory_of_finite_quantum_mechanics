from __future__ import annotations

from .witness import witness


def test_witness() -> None:
    w = witness()
    assert w["goal_id"] == "PROD-KERNEL-ROUTING"
    assert w["before_phi1"] == "3"
    assert w["after_good_phi1"] == "2"
    assert w["damage_refused"] is True
    assert w["good_edit_accepted"] is True
    assert w["no_descent_refused"] is True
    assert w["lift_valid"] is True
    assert w["invalid_lift_refused"] is True
    assert w["exact_terminal"] == "ExactCertified"
    assert w["stabilized_terminal"] == "StabilizedSurvivor"
    assert w["invalid_stability_refused"] is True
