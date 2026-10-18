"""Exact purity solver for a rational diagonal state.

The purity sum p_i^2 and the ratio (sum p_i^2) / (sum p_i)^2 are computed
independently. Their gap is the certificate.
"""
from fractions import Fraction


class EntropySolverError(Exception):
    """The spectrum is empty, negative, or not a probability vector."""


def purity_gap() -> Fraction:
    """Return the gap between two purity expressions of (1/2, 1/3, 1/6)."""
    weights = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
    if not weights:
        raise EntropySolverError("spectrum is empty")
    for weight in weights:
        if weight < 0:
            raise EntropySolverError(f"weight {weight} is negative")
    mass = sum(weights, Fraction(0))
    if mass == 0:
        raise EntropySolverError("spectrum has zero mass")
    raw_square_sum = sum((weight * weight for weight in weights), Fraction(0))
    by_ratio = raw_square_sum / (mass * mass)
    by_normalization = sum(((weight / mass) ** 2 for weight in weights), Fraction(0))
    gap = by_ratio - by_normalization
    if gap != 0:
        raise EntropySolverError(f"purity expressions differ by {gap}")
    return by_normalization
