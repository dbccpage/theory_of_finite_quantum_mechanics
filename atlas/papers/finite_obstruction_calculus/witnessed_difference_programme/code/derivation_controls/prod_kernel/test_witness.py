from __future__ import annotations

from .witness import witness


def test_witness() -> None:
    w = witness()
    assert w["goal_id"] == "PROD-KERNEL"
    assert w["certificate_valid"] is True
    assert w["claim"] == "WIN_OPTIMAL"
    assert w["initial_value"] == "3"
    assert w["receipt_verified"] is True
    assert w["tampered_rejected"] is True
    assert w["refusal_code"] == "digest_mismatch"
    assert w["any_kill_condition_holds"] is False
    assert w["authority_effect"] == "None"
