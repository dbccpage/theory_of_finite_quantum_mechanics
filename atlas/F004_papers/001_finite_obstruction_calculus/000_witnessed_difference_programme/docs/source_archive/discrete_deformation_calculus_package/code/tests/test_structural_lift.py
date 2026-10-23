"""
Unit tests for DDC Operation Lambda (Structural Lift).
AuthorityEffect: None.
"""

from fractions import Fraction

import pytest
from structural_lift import (
    FiniteLambdaLedger,
    FiniteLambdaStep,
    StructuralLifter,
)


def test_licensed_structural_lift():
    """Verify that a licensed lift extends dimension with zero-padding."""
    lifter = StructuralLifter(authorized_licenses={"LCE-001"})
    v = [Fraction(1), Fraction(2)]
    receipt = lifter.lift(v, added_dims=2, license_id="LCE-001", trigger="ClosedResidual")

    assert receipt.success is True
    assert receipt.initial_dim == 2
    assert receipt.extended_dim == 4
    assert receipt.lifted_vector == [Fraction(1), Fraction(2), Fraction(0), Fraction(0)]
    assert receipt.error is None


def test_unlicensed_lift_refusal():
    """Verify fail-closed refusal when license is missing or invalid."""
    lifter = StructuralLifter(authorized_licenses={"LCE-001"})
    v = [Fraction(5)]
    receipt = lifter.lift(v, added_dims=3, license_id="UNAUTHORIZED_TICKET")

    assert receipt.success is False
    assert receipt.error == "REFUSED_UNLICENSED_LIFT"
    assert receipt.lifted_vector == v


def test_finite_lambda_ledger_valid_chain():
    """Verify chained finite lambda ledger succeeds when sequence is valid descent to terminal."""
    step1 = FiniteLambdaStep(
        before_phi=Fraction(3),
        before_gamma=Fraction(2),
        after_phi=Fraction(2),
        after_gamma=Fraction(1),
        is_descent=True,
        is_valid=True,
    )
    step2 = FiniteLambdaStep(
        before_phi=Fraction(2),
        before_gamma=Fraction(1),
        after_phi=Fraction(0),
        after_gamma=Fraction(0),
        is_descent=True,
        is_valid=True,
    )
    ledger = FiniteLambdaLedger.new(
        initial=(3, 2),
        steps=[step1, step2],
        terminal=(0, 0),
    )
    assert ledger.require_chained() is True


def test_finite_lambda_ledger_empty():
    """Verify empty ledger requires identical and resolved (0, 0) endpoints."""
    # Valid resolved empty ledger
    ledger_ok = FiniteLambdaLedger.new(
        initial=(0, 0),
        steps=[],
        terminal=(0, 0),
    )
    assert ledger_ok.require_chained() is True

    # Empty ledger with endpoint mismatch
    ledger_mismatch = FiniteLambdaLedger.new(
        initial=(0, 0),
        steps=[],
        terminal=(1, 0),
    )
    with pytest.raises(ValueError, match="EMPTY_LEDGER_ENDPOINT_MISMATCH"):
        ledger_mismatch.require_chained()

    # Empty ledger with non-zero unresolved endpoints
    ledger_unresolved = FiniteLambdaLedger.new(
        initial=(1, 0),
        steps=[],
        terminal=(1, 0),
    )
    with pytest.raises(ValueError, match="EMPTY_LEDGER_UNRESOLVED"):
        ledger_unresolved.require_chained()


def test_finite_lambda_ledger_broken_invariants():
    """Verify failure modes on head, tail, broken chain, non-descent, and invalid final step."""
    step1 = FiniteLambdaStep(
        before_phi=Fraction(3),
        before_gamma=Fraction(2),
        after_phi=Fraction(2),
        after_gamma=Fraction(1),
        is_descent=True,
        is_valid=True,
    )
    step2 = FiniteLambdaStep(
        before_phi=Fraction(2),
        before_gamma=Fraction(1),
        after_phi=Fraction(0),
        after_gamma=Fraction(0),
        is_descent=True,
        is_valid=True,
    )

    # 1. Head mismatch
    ledger_head = FiniteLambdaLedger.new(
        initial=(4, 2),
        steps=[step1, step2],
        terminal=(0, 0),
    )
    with pytest.raises(ValueError, match="HEAD_MISMATCH"):
        ledger_head.require_chained()

    # 2. Tail mismatch
    ledger_tail = FiniteLambdaLedger.new(
        initial=(3, 2),
        steps=[step1, step2],
        terminal=(1, 0),
    )
    with pytest.raises(ValueError, match="TAIL_MISMATCH"):
        ledger_tail.require_chained()

    # 3. Broken adjacency chain
    broken_step2 = FiniteLambdaStep(
        before_phi=Fraction(5),  # mismatch with step1.after (2)
        before_gamma=Fraction(1),
        after_phi=Fraction(0),
        after_gamma=Fraction(0),
        is_descent=True,
        is_valid=True,
    )
    ledger_broken = FiniteLambdaLedger.new(
        initial=(3, 2),
        steps=[step1, broken_step2],
        terminal=(0, 0),
    )
    with pytest.raises(ValueError, match="BROKEN_CHAIN"):
        ledger_broken.require_chained()

    # 4. Non-final step not descent
    non_descent_step1 = FiniteLambdaStep(
        before_phi=Fraction(3),
        before_gamma=Fraction(2),
        after_phi=Fraction(2),
        after_gamma=Fraction(1),
        is_descent=False,
        is_valid=True,
    )
    ledger_non_descent = FiniteLambdaLedger.new(
        initial=(3, 2),
        steps=[non_descent_step1, step2],
        terminal=(0, 0),
    )
    with pytest.raises(ValueError, match="NON_FINAL_ROW_NOT_DESCENT"):
        ledger_non_descent.require_chained()

    # 5. Final step invalid
    invalid_step2 = FiniteLambdaStep(
        before_phi=Fraction(2),
        before_gamma=Fraction(1),
        after_phi=Fraction(0),
        after_gamma=Fraction(0),
        is_descent=True,
        is_valid=False,
    )
    ledger_invalid_final = FiniteLambdaLedger.new(
        initial=(3, 2),
        steps=[step1, invalid_step2],
        terminal=(0, 0),
    )
    with pytest.raises(ValueError, match="FINAL_ROW_INVALID"):
        ledger_invalid_final.require_chained()

