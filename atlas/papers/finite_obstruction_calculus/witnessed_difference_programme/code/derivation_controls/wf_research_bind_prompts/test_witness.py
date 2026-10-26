"""Tests for WF-RESEARCH-BIND-PROMPTS finite witness.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from .witness import (
    CARRIER_VAL,
    GOAL_ID,
    SECONDARY_FRAC,
    evaluate_primary,
    evaluate_secondary,
    reject_unlowered_packet_or_authority_escalation,
    witness,
)


def test_wf_research_bind_prompts_witness_invariants() -> None:
    w = witness()
    assert w["goal_id"] == "WF-RESEARCH-BIND-PROMPTS"
    assert w["carrier_val"] == 4
    assert evaluate_primary() == 4
    assert evaluate_secondary() == Fraction(8, 8)
    assert w["secondary_num"] == SECONDARY_FRAC.numerator
    assert w["secondary_den"] == SECONDARY_FRAC.denominator
    assert w["negative_control_rejected"] is True
    assert w["negative_control_reason"] == "reject_unlowered_packet_or_authority_escalation"


def test_wf_research_bind_prompts_negative_control() -> None:
    refused = reject_unlowered_packet_or_authority_escalation(True)
    assert refused["accepted"] is False
    admitted = reject_unlowered_packet_or_authority_escalation(False)
    assert admitted["accepted"] is True
    with pytest.raises(TypeError):
        reject_unlowered_packet_or_authority_escalation(1)  # type: ignore[arg-type]
