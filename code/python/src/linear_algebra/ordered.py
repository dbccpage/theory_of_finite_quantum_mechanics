"""Order on the rationals by cross-multiplication, with sums of squares.

Origin: code/python/src/linear_algebra/ordered.py
Claim: the comparator agrees with the sign of a*d − b*c, and a sum of rational squares is nonnegative.
AuthorityEffect: None. Q(i) is not ordered by this module.
"""
from fractions import Fraction
from typing import List, Sequence

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class OrderError(Exception):
    """A compared value was not rational."""


def as_fraction(value) -> Fraction:
    if isinstance(value, GaussianRational):
        raise OrderError("the order in this module is the order of Q, not Q(i)")
    try:
        return Fraction(value)
    except (TypeError, ValueError) as exc:
        raise OrderError(f"value {value!r} is not rational") from exc


def compare(left: object, right: object) -> int:
    """Return −1, 0, or 1 by the sign of left − right, computed as a rational difference."""
    gap = as_fraction(left) - as_fraction(right)
    if gap > 0:
        return 1
    if gap < 0:
        return -1
    return 0


def cross_sign(numerator_left: object, denominator_left: object, numerator_right: object, denominator_right: object) -> int:
    """Sign of a/b − c/d from a*d − b*c, without reducing first."""
    a = as_fraction(numerator_left)
    b = as_fraction(denominator_left)
    c = as_fraction(numerator_right)
    d = as_fraction(denominator_right)
    if b == 0 or d == 0:
        raise OrderError("cross-multiplication requires nonzero denominators")
    if b < 0:
        a, b = -a, -b
    if d < 0:
        c, d = -c, -d
    gap = a * d - b * c
    if gap > 0:
        return 1
    if gap < 0:
        return -1
    return 0


def sum_of_squares(values: Sequence[object]) -> Fraction:
    """Return Σ v_i^2. The result is a nonnegative rational."""
    total = Fraction(0)
    for value in values:
        coord = as_fraction(value)
        total += coord * coord
    if total < 0:
        raise OrderError("a sum of rational squares was negative")
    return total


def sorted_fractions(values: Sequence[object]) -> List[Fraction]:
    """Insertion-sort by the exact comparator. Adjacent pairs are rechecked by cross-multiplication."""
    ordered = [as_fraction(value) for value in values]
    for i in range(1, len(ordered)):
        current = ordered[i]
        j = i
        while j > 0 and compare(ordered[j - 1], current) > 0:
            ordered[j] = ordered[j - 1]
            j -= 1
        ordered[j] = current
    for i in range(len(ordered) - 1):
        if cross_sign(ordered[i].numerator, ordered[i].denominator, ordered[i + 1].numerator, ordered[i + 1].denominator) > 0:
            raise OrderError("sorted rationals are not nondecreasing")
    return ordered


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "Q",
    "q",
    "OrderError",
    "as_fraction",
    "compare",
    "cross_sign",
    "sum_of_squares",
    "sorted_fractions",
]
