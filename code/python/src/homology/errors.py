"""Homology error definitions.

Origin: code/python/src/homology/errors.py
Claim: NonZeroCompositionError is raised exactly when a rational matrix product is not zero.
AuthorityEffect: None.
"""
from fractions import Fraction
from typing import Sequence


class HomologyError(Exception):
    pass


class NonZeroCompositionError(HomologyError):
    pass


class DimensionMismatchError(HomologyError):
    pass


def require_composition_zero(left: Sequence[Sequence[object]], right: Sequence[Sequence[object]]) -> Fraction:
    """Multiply two rational matrices and return 0, or raise if any entry survives."""
    if not left or not right:
        raise DimensionMismatchError("composition requires nonempty matrices")
    mid = len(left[0])
    if any(len(row) != mid for row in left) or any(len(row) != len(right[0]) for row in right):
        raise DimensionMismatchError("jagged rational matrices cannot be composed")
    if len(right) != mid:
        raise DimensionMismatchError(f"cannot compose widths {mid} and {len(right)}")
    defect = Fraction(0)
    out_cols = len(right[0])
    for row in left:
        for col in range(out_cols):
            entry = Fraction(0)
            for k in range(mid):
                entry += Fraction(row[k]) * Fraction(right[k][col])
            defect += abs(entry)
    if defect != 0:
        raise NonZeroCompositionError(f"composition defect is {defect}, not 0")
    return defect


def triangle_composition_defect() -> Fraction:
    """∂1 ∂2 for the standard triangle, checked through require_composition_zero."""
    edge = (
        (Fraction(-1), Fraction(-1), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(-1)),
        (Fraction(0), Fraction(1), Fraction(1)),
    )
    face = ((Fraction(1),), (Fraction(-1),), (Fraction(1),))
    return require_composition_zero(edge, face)
