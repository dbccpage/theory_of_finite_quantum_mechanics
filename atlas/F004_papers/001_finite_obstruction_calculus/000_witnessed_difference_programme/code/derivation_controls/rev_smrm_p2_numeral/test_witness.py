from __future__ import annotations

from .witness import witness


def test_witness() -> None:
    w = witness()
    assert w["goal_id"] == "REV-SMRM-P2-NUMERAL"
    assert w["negative_uncertainty_refused"] is True
    assert w["valid_measurement_accepted"] is True
    assert w["enclosure_matches_expected"] is True
    assert w["replay_verified"] is True
    assert w["altered_record_refused"] is True
