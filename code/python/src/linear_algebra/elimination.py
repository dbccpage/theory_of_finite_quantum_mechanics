"""Partial-pivoted LU factorization over Q.

Origin: code/python/src/linear_algebra/elimination.py
Claim: for a nonsingular rational matrix, P A = L U with unit lower-triangular L.
AuthorityEffect: None.
"""
from fractions import Fraction
from typing import Tuple

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class EliminationError(Exception):
    """Elimination was asked for a singular, non-square, or non-rational matrix."""


def plu_factor(matrix: ExactMatrix) -> Tuple[ExactMatrix, ExactMatrix, ExactMatrix]:
    """Return P, L, U such that P * matrix = L * U."""
    if matrix.rows != matrix.cols:
        raise EliminationError(f"PLU requires a square matrix, got {matrix.shape()}")
    n = matrix.rows
    current = []
    for r in range(n):
        row = []
        for c in range(n):
            value = matrix.get(r, c)
            if isinstance(value, GaussianRational):
                raise EliminationError("PLU in this module is over Q, not Q(i)")
            try:
                row.append(Fraction(value))
            except (TypeError, ValueError) as exc:
                raise EliminationError(f"entry {value!r} is not rational") from exc
        current.append(row)
    lower = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    origin = list(range(n))
    for k in range(n):
        pivot_row = k
        pivot_size = abs(current[k][k])
        for i in range(k + 1, n):
            size = abs(current[i][k])
            if size > pivot_size:
                pivot_row = i
                pivot_size = size
        if pivot_size == 0:
            raise EliminationError("matrix is singular")
        if pivot_row != k:
            current[k], current[pivot_row] = current[pivot_row], current[k]
            origin[k], origin[pivot_row] = origin[pivot_row], origin[k]
            for j in range(k):
                lower[k][j], lower[pivot_row][j] = lower[pivot_row][j], lower[k][j]
        for i in range(k + 1, n):
            lower[i][k] = current[i][k] / current[k][k]
            for j in range(k, n):
                current[i][j] -= lower[i][k] * current[k][j]
            current[i][k] = Fraction(0)
    permutation = [[Fraction(1 if origin[i] == j else 0) for j in range(n)] for i in range(n)]
    p_mat = ExactMatrix.from_rows(permutation)
    l_mat = ExactMatrix.from_rows(lower)
    u_mat = ExactMatrix.from_rows(current)
    if p_mat * matrix != l_mat * u_mat:
        raise EliminationError("constructed factors do not satisfy P*A = L*U")
    return p_mat, l_mat, u_mat


__all__ = ["ExactMatrix", "GaussianRational", "Q", "q", "EliminationError", "plu_factor"]
