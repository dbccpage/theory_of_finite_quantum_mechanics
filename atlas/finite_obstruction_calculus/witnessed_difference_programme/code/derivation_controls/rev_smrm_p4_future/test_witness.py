from __future__ import annotations

from .witness import witness


def test_witness() -> None:
    w = witness()
    assert w["goal_id"] == "REV-SMRM-P4-FUTURE"
    assert w["preserved_cost"] == "15/4"
    assert w["answers_only_cost"] == "7/2"
    assert w["fixed_suite_cost"] == "6"
    assert w["strictly_cheaper_than_fixed"] is True
    assert w["construction_verified"] is True
    assert w["certificate_verified"] is True
    assert w["replay_verified"] is True
    assert w["authority_effect"] == "None"
