"""
Unit tests for DDC Operation D (Descent).
AuthorityEffect: None.
"""

from fractions import Fraction

from descent import DescentProjector


def test_lossless_descent():
    """Verify that zero discarded tail components result in LOSSLESS_DESCENT."""
    projector = DescentProjector(target_dim=2)
    v = [Fraction(3, 4), Fraction(-1, 2), Fraction(0), Fraction(0)]
    receipt = projector.descend(v)

    assert receipt.is_lossless is True
    assert receipt.status == "LOSSLESS_DESCENT"
    assert receipt.loss_scalar == Fraction(0)
    assert receipt.coarse_vector == (Fraction(3, 4), Fraction(-1, 2))


def test_descent_with_positive_loss():
    """Verify that non-zero discarded coordinates are explicitly bound to loss_scalar."""
    projector = DescentProjector(target_dim=2)
    v = [Fraction(1), Fraction(2), Fraction(-3, 4), Fraction(1, 4)]
    receipt = projector.descend(v)

    assert receipt.is_lossless is False
    assert receipt.status == "DESCENT_WITH_LOSS"
    assert receipt.loss_scalar == Fraction(1)  # |-3/4| + |1/4| = 1
    assert receipt.loss_vector == (Fraction(-3, 4), Fraction(1, 4))
