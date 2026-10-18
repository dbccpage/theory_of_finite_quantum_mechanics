"""Kronecker product over Q and over the Gaussian rationals Q(i).

Origin: code/python/src/linear_algebra/complex_tensor.py
Claim: (A ⊗ B)(C ⊗ D) = (AC) ⊗ (BD) when the ordinary products are defined.
AuthorityEffect: None.
"""
from fractions import Fraction
from typing import List

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class TensorError(Exception):
    """A Kronecker factor had the wrong shape or a non-exact entry."""


def _entry(value):
    if isinstance(value, GaussianRational):
        return value
    try:
        return Fraction(value)
    except (TypeError, ValueError) as exc:
        raise TensorError(f"entry {value!r} is not rational or Gaussian rational") from exc


def kronecker(left: ExactMatrix, right: ExactMatrix) -> ExactMatrix:
    """Return the Kronecker product left ⊗ right."""
    data = []
    for i in range(left.rows):
        for k in range(right.rows):
            for j in range(left.cols):
                for ell in range(right.cols):
                    data.append(_entry(left.get(i, j)) * _entry(right.get(k, ell)))
    return ExactMatrix(left.rows * right.rows, left.cols * right.cols, data)


def mixed_product_defect(a: ExactMatrix, b: ExactMatrix, c: ExactMatrix, d: ExactMatrix) -> Fraction:
    """Sum of absolute real and imaginary parts of (A⊗B)(C⊗D) − (AC)⊗(BD)."""
    if a.cols != c.rows or b.cols != d.rows:
        raise TensorError("mixed-product identity needs A*C and B*D to be defined")
    left = kronecker(a, b) * kronecker(c, d)
    right = kronecker(a * c, b * d)
    if left.shape() != right.shape():
        raise TensorError("mixed-product sides have different shapes")
    defect = Fraction(0)
    for x, y in zip(left.data, right.data):
        gap = _entry(x) - _entry(y)
        if isinstance(gap, GaussianRational):
            defect += abs(gap.real) + abs(gap.imag)
        else:
            defect += abs(Fraction(gap))
    return defect


def sample_gaussian_tensor() -> List[GaussianRational]:
    """(1+i) ⊗ (1, i) as a column, with squared norm 1+1 = 2 times 1+1 = 4."""
    left = ExactMatrix.from_rows([[GaussianRational(1, 1)]])
    right = ExactMatrix.from_rows([[GaussianRational(1, 0)], [GaussianRational(0, 1)]])
    product = kronecker(left, right)
    return [entry for entry in product.data]


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "Q",
    "q",
    "TensorError",
    "kronecker",
    "mixed_product_defect",
    "sample_gaussian_tensor",
]
