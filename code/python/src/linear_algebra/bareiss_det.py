"""Fraction-free Bareiss determinant over Q.

Origin: code/python/src/linear_algebra/bareiss_det.py
Claim: the Bareiss pivot equals the Gaussian determinant on a rational matrix.
AuthorityEffect: None. Agreement on one matrix is not a proof for every shape.
"""
from fractions import Fraction

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class BareissError(Exception):
    """Bareiss was asked for a non-square matrix or a non-rational entry."""


def bareiss_determinant(matrix: ExactMatrix):
    """Return det(matrix) by the one-step Bareiss recurrence over Q."""
    if matrix.rows != matrix.cols:
        raise BareissError(f"determinant requires a square matrix, got {matrix.shape()}")
    n = matrix.rows
    if n == 0:
        return Fraction(1)
    grid = []
    for r in range(n):
        row = []
        for c in range(n):
            value = matrix.get(r, c)
            if isinstance(value, GaussianRational):
                raise BareissError("Bareiss determinant in this module is over Q, not Q(i)")
            try:
                row.append(Fraction(value))
            except (TypeError, ValueError) as exc:
                raise BareissError(f"entry {value!r} is not rational") from exc
        grid.append(row)
    sign = 1
    previous = Fraction(1)
    for k in range(n - 1):
        if grid[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if grid[i][k] != 0), None)
            if swap is None:
                return Fraction(0)
            grid[k], grid[swap] = grid[swap], grid[k]
            sign = -sign
        pivot = grid[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = pivot * grid[i][j] - grid[i][k] * grid[k][j]
                grid[i][j] = numerator / previous
            grid[i][k] = Fraction(0)
        previous = pivot
    return sign * grid[n - 1][n - 1]


def bareiss_matches_elimination(matrix: ExactMatrix) -> Fraction:
    """Return the Bareiss determinant after checking it against Gaussian elimination."""
    bareiss = bareiss_determinant(matrix)
    gauss = matrix.determinant()
    if bareiss != gauss:
        raise BareissError(f"Bareiss det {bareiss} disagrees with elimination det {gauss}")
    return bareiss


__all__ = ["ExactMatrix", "GaussianRational", "Q", "q", "BareissError", "bareiss_determinant", "bareiss_matches_elimination"]
