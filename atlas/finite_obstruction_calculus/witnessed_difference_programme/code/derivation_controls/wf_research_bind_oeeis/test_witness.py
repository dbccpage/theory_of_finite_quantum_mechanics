"""Tests for WF-RESEARCH-BIND-OEEIS finite witness.

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
    reject_inert_candidate_self_activation,
    witness,
)


def test_wf_research_bind_oeeis_witness_invariants() -> None:
    w = witness()
    assert w["goal_id"] == "WF-RESEARCH-BIND-OEEIS"
    assert w["carrier_val"] == 3
    assert evaluate_primary() == 3
    assert evaluate_secondary() == Fraction(1, 1)
    assert w["secondary_num"] == SECONDARY_FRAC.numerator
    assert w["secondary_den"] == SECONDARY_FRAC.denominator
    assert w["negative_control_rejected"] is True
    assert w["negative_control_reason"] == "reject_inert_candidate_self_activation"


def test_wf_research_bind_oeeis_negative_control() -> None:
    refused = reject_inert_candidate_self_activation(True)
    assert refused["accepted"] is False
    admitted = reject_inert_candidate_self_activation(False)
    assert admitted["accepted"] is True
    with pytest.raises(TypeError):
        reject_inert_candidate_self_activation(1)  # type: ignore[arg-type]
