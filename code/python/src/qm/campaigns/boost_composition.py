"""Collinear composition of rational Lorentz boosts.

Origin: code/python/src/qm/campaigns/boost_composition.py
Claim: boosts of velocities 3/5 and 5/13 multiply to the boost of velocity 4/5.
AuthorityEffect: None. This is 1+1 dimension, not a general Lorentz theorem.
"""
from fractions import Fraction


class BoostError(Exception):
    """A rational boost failed gamma^2 (1-beta^2) = 1 or the composition identity."""


def _boost(beta: Fraction, gamma: Fraction):
    if gamma * gamma * (1 - beta * beta) != 1:
        raise BoostError(f"gamma {gamma} is not the Lorentz factor of beta {beta}")
    return ((gamma, gamma * beta), (gamma * beta, gamma))


def _mul(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def velocity_addition(left: Fraction, right: Fraction) -> Fraction:
    """(u+v)/(1+uv), refused when the denominator vanishes."""
    denom = 1 + left * right
    if denom == 0:
        raise BoostError("collinear velocities are mutually lightlike")
    return (left + right) / denom


def composed_velocity() -> Fraction:
    """Matrix product of the two boosts, read back as a velocity and checked against addition."""
    first = _boost(Fraction(3, 5), Fraction(5, 4))
    second = _boost(Fraction(5, 13), Fraction(13, 12))
    product = _mul(first, second)
    added = velocity_addition(Fraction(3, 5), Fraction(5, 13))
    expected = _boost(added, Fraction(5, 3))
    if product != expected:
        raise BoostError(f"boost product {product} is not the composite {expected}")
    return added
