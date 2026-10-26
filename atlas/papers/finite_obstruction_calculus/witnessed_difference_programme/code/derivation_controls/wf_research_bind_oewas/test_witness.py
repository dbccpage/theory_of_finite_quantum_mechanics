"""Tests for WF-RESEARCH-BIND-OEWAS finite witness.

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
    reject_invented_catalog_hash,
    witness,
)


def test_wf_research_bind_oewas_witness_invariants() -> None:
    w = witness()
    assert w["goal_id"] == "WF-RESEARCH-BIND-OEWAS"
    assert w["carrier_val"] == 9
    assert evaluate_primary() == 9
    assert evaluate_secondary() == Fraction(1, 1)
    assert w["secondary_num"] == SECONDARY_FRAC.numerator
    assert w["secondary_den"] == SECONDARY_FRAC.denominator
    assert w["negative_control_rejected"] is True
    assert w["negative_control_reason"] == "reject_invented_catalog_hash"


def test_wf_research_bind_oewas_negative_control() -> None:
    refused = reject_invented_catalog_hash(True)
    assert refused["accepted"] is False
    admitted = reject_invented_catalog_hash(False)
    assert admitted["accepted"] is True
    with pytest.raises(TypeError):
        reject_invented_catalog_hash(1)  # type: ignore[arg-type]
