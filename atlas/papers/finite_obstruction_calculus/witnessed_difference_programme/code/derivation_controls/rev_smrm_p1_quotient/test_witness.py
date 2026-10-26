from __future__ import annotations

from .witness import witness


def test_witness() -> None:
    w = witness()
    assert w["goal_id"] == "REV-SMRM-P1-QUOTIENT"
    assert w["quotient_reachable_count"] < w["raw_reachable_count"]
    assert w["refinement_check_passed"] is True
    assert w["quotient_check_passed"] is True
    assert w["refined_congruent"] is True
    assert w["bad_blocks_congruent"] is False
    assert w["raw_initial_value"] == "3"
    assert w["quotient_initial_value"] == "3"
