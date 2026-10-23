"""Tests for AuthorizationBoundary."""

from __future__ import annotations

import sys
from pathlib import Path

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from authorization_boundary import (
    factors_through,
    fiber_splits_valid,
    no_report_decision,
    p_neg,
    p_pos,
    valid_neg,
    valid_pos,
    with_extra,
)

BOOLS = (False, True)


def test_negative_fiber_splits() -> None:
    assert fiber_splits_valid(BOOLS, p_neg, valid_neg)


def test_negative_no_report_decision() -> None:
    result = no_report_decision(BOOLS, p_neg, valid_neg)
    assert result.factors is False
    assert result.reason == "no report-only decider"


def test_positive_identity_factors() -> None:
    assert not fiber_splits_valid(BOOLS, p_pos, valid_pos)
    assert factors_through(BOOLS, p_pos, valid_pos, valid_pos)


def test_extra_input_recovers_negative() -> None:
    for x in BOOLS:
        assert with_extra(p_neg, lambda z: z, lambda _r, e: bool(e), x) == valid_neg(x)
