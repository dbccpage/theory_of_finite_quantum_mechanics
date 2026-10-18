"""Buildability of a shear by a word in the elementary transvection S.

Origin: code/python/src/qm/campaigns/buildability.py
Claim: S(2) S(3) = S(5), so the exponent 5 is built by multiplying the generators.
AuthorityEffect: None.
"""
from fractions import Fraction


class BuildError(Exception):
    """A word in the shear generators did not build the target."""


def shear(exponent: int):
    if isinstance(exponent, bool) or not isinstance(exponent, int):
        raise BuildError("shear exponent must be an int")
    return ((Fraction(1), Fraction(exponent)), (Fraction(0), Fraction(1)))


def _mul(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def built_exponent() -> int:
    """Off-diagonal entry of S(2) S(3). It equals 5, which is the sum of the exponents."""
    built = _mul(shear(2), shear(3))
    target = shear(5)
    if built != target:
        raise BuildError(f"word built {built}, not {target}")
    return int(built[0][1])
