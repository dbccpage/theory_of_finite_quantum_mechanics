"""Tests for WF-RESEARCH-BIND-RUNNER finite witness.

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
    reject_model_stage5_or_copied_stage8_terminal,
    witness,
)


def test_wf_research_bind_runner_witness_invariants() -> None:
    w = witness()
    assert w["goal_id"] == "WF-RESEARCH-BIND-RUNNER"
    assert w["carrier_val"] == 8
    assert evaluate_primary() == 8
    assert evaluate_secondary() == Fraction(5, 8)
    assert w["secondary_num"] == SECONDARY_FRAC.numerator
    assert w["secondary_den"] == SECONDARY_FRAC.denominator
    assert w["negative_control_rejected"] is True
    assert w["negative_control_reason"] == "reject_model_stage5_or_copied_stage8_terminal"


def test_wf_research_bind_runner_negative_control() -> None:
    refused = reject_model_stage5_or_copied_stage8_terminal(True)
    assert refused["accepted"] is False
    admitted = reject_model_stage5_or_copied_stage8_terminal(False)
    assert admitted["accepted"] is True
    with pytest.raises(TypeError):
        reject_model_stage5_or_copied_stage8_terminal(1)  # type: ignore[arg-type]
