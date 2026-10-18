"""Additive carrier on a triangle: curvature is the oriented sum of edge weights.

Origin: code/python/src/qm/campaigns/carrier.py
Claim: weights (a, b, -(a+b)) have curvature 0, and a constant weight 1 has curvature 3.
AuthorityEffect: None.
"""
from fractions import Fraction


class CarrierCurvatureError(Exception):
    """An edge weight was not rational or the flat connection was not flat."""


def curvature(weights) -> Fraction:
    """Sum of the three oriented edge weights around the face."""
    if len(weights) != 3:
        raise CarrierCurvatureError(f"triangle carrier needs 3 edges, got {len(weights)}")
    total = Fraction(0)
    for weight in weights:
        total += Fraction(weight)
    return total


def flat_carrier_curvature() -> Fraction:
    """Curvature of the connection whose third edge closes the first two."""
    first = Fraction(2, 3)
    second = Fraction(-1, 5)
    closed = curvature((first, second, -(first + second)))
    if closed != 0:
        raise CarrierCurvatureError(f"closing edge left curvature {closed}")
    return closed
