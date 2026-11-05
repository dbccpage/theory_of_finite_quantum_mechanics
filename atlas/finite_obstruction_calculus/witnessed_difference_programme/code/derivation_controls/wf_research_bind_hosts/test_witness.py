"""Tests for WF-RESEARCH-BIND-HOSTS finite witness.

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
    reject_missing_host_or_digest_drift,
    witness,
)


def test_wf_research_bind_hosts_witness_invariants() -> None:
    w = witness()
    assert w["goal_id"] == "WF-RESEARCH-BIND-HOSTS"
    assert w["carrier_val"] == 4
    assert evaluate_primary() == 4
    assert evaluate_secondary() == Fraction(2, 2)
    assert w["secondary_num"] == SECONDARY_FRAC.numerator
    assert w["secondary_den"] == SECONDARY_FRAC.denominator
    assert w["negative_control_rejected"] is True
    assert w["negative_control_reason"] == "reject_missing_host_or_digest_drift"


def test_wf_research_bind_hosts_negative_control() -> None:
    refused = reject_missing_host_or_digest_drift(True)
    assert refused["accepted"] is False
    admitted = reject_missing_host_or_digest_drift(False)
    assert admitted["accepted"] is True
    with pytest.raises(TypeError):
        reject_missing_host_or_digest_drift(1)  # type: ignore[arg-type]
