from __future__ import annotations

from .witness import witness


def test_witness() -> None:
    w = witness()
    assert w["goal_id"] == "REV-SMRM-P3-MINE"
    assert w["trace_verified"] is True
    assert w["spent"] == "17"
    assert w["remaining"] == "1"
    assert w["bundle_matches_parent"] is True
    assert w["tampered_parent_rejected"] is True
    assert w["sound_on_valid"] is True
    assert w["authority_effect"] == "None"
