"""Exact checks of the matrix-algebra laws on rational witnesses.

Origin: code/python/src/linear_algebra/laws.py
Claim: (AB)^T = B^T A^T and (AB)C = A(BC), with the defect summed in Q.
AuthorityEffect: None. The laws are certified on the matrices passed in, not schematized.
"""
from fractions import Fraction

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class LawError(Exception):
    """A law witness was non-square in a required place or not rational."""


def _rational(matrix: ExactMatrix) -> ExactMatrix:
    data = []
    for value in matrix.data:
        if isinstance(value, GaussianRational):
            raise LawError("algebra laws in this module are checked over Q, not Q(i)")
        try:
            data.append(Fraction(value))
        except (TypeError, ValueError) as exc:
            raise LawError(f"entry {value!r} is not rational") from exc
    return ExactMatrix(matrix.rows, matrix.cols, data)


def _abs_sum(matrix: ExactMatrix) -> Fraction:
    total = Fraction(0)
    for value in matrix.data:
        total += abs(Fraction(value))
    return total


def transpose_law_defect(left: ExactMatrix, right: ExactMatrix) -> Fraction:
    """Sum of absolute entries of (AB)^T − B^T A^T."""
    a = _rational(left)
    b = _rational(right)
    if a.cols != b.rows:
        raise LawError(f"cannot multiply shapes {a.shape()} and {b.shape()}")
    gap = (a * b).transpose() - (b.transpose() * a.transpose())
    return _abs_sum(gap)


def associator_defect(left: ExactMatrix, mid: ExactMatrix, right: ExactMatrix) -> Fraction:
    """Sum of absolute entries of (AB)C − A(BC)."""
    a = _rational(left)
    b = _rational(mid)
    c = _rational(right)
    if a.cols != b.rows or b.cols != c.rows:
        raise LawError("associator requires compatible shapes")
    gap = (a * b) * c - a * (b * c)
    return _abs_sum(gap)


def witness_product_entry() -> Fraction:
    """(0, 1) entry of (AB)^T for a fixed rational pair. It is computed, not stored."""
    left = ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(0), Fraction(1)]])
    right = ExactMatrix.from_rows([[Fraction(3), Fraction(0)], [Fraction(4), Fraction(5)]])
    if transpose_law_defect(left, right) != 0:
        raise LawError("transpose law failed on the witness pair")
    product = (left * right).transpose()
    return Fraction(product.get(0, 1))


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "Q",
    "q",
    "LawError",
    "transpose_law_defect",
    "associator_defect",
    "witness_product_entry",
]
