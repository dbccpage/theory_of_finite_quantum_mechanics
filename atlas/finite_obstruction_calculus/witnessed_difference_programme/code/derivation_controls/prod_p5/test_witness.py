from __future__ import annotations

from .witness import witness


def test_witness() -> None:
    w = witness()
    assert w["goal_id"] == "PROD-P5"
    assert w["runtime_package"] == "omega_engine_woland"
    assert w["full_statuses"]["C1_BASE"] == "Proved"
    assert w["full_statuses"]["C2_DERIVED"] == "Proved"
    assert w["full_statuses"]["C3_OPEN"] == "Undetermined"
    assert w["missing_pointer_statuses"]["C1_BASE"] == "Undetermined"
    assert w["missing_pointer_statuses"]["C2_DERIVED"] == "Undetermined"
    assert w["p2_unverified_statuses"]["C1_BASE"] == "Undetermined"
    assert w["full_proved_count"] == 2
    assert w["missing_proved_count"] == 0
    assert w["authority_effect"] == "None"
