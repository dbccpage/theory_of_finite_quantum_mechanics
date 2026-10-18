"""Centralizer of a rational matrix, as the kernel of X |-> XA − AX.

Origin: code/python/src/linear_algebra/commutant.py
Claim: every returned basis matrix commutes with the input, and the commutator map's nullity is that dimension.
AuthorityEffect: None. This does not classify the algebra beyond the matrix that was passed.
"""
from fractions import Fraction
from typing import List

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class CommutantError(Exception):
    """The commutant was requested for a non-rational or non-square matrix."""


def _rational_square(matrix: ExactMatrix) -> ExactMatrix:
    if matrix.rows != matrix.cols:
        raise CommutantError(f"commutant requires a square matrix, got {matrix.shape()}")
    data = []
    for value in matrix.data:
        if isinstance(value, GaussianRational):
            raise CommutantError("commutant in this module is over Q, not Q(i)")
        try:
            data.append(Fraction(value))
        except (TypeError, ValueError) as exc:
            raise CommutantError(f"entry {value!r} is not rational") from exc
    return ExactMatrix(matrix.rows, matrix.cols, data)


def _commutator(left: ExactMatrix, right: ExactMatrix) -> ExactMatrix:
    return left * right - right * left


def commutant_basis(matrix: ExactMatrix) -> List[ExactMatrix]:
    """Return a rational basis of {X : XA = AX}, vectorized in row-major order."""
    source = _rational_square(matrix)
    n = source.rows
    columns = []
    for row in range(n):
        for col in range(n):
            data = [Fraction(0)] * (n * n)
            data[row * n + col] = Fraction(1)
            probe = ExactMatrix(n, n, data)
            columns.append(_commutator(probe, source).data)
    if n == 0:
        return []
    stacked = []
    for row in range(n * n):
        stacked.append([columns[col][row] for col in range(n * n)])
    kernel = ExactMatrix.from_rows(stacked).kernel_basis()
    basis = []
    for vec in kernel:
        basis.append(ExactMatrix(n, n, [Fraction(entry) for entry in vec]))
    return basis


def commutant_dimension(matrix: ExactMatrix) -> int:
    """Dimension of the commutant. Each basis element is rechecked by multiplication."""
    source = _rational_square(matrix)
    basis = commutant_basis(source)
    for element in basis:
        defect = _commutator(element, source)
        if any(Fraction(entry) != 0 for entry in defect.data):
            raise CommutantError("commutant basis element does not commute with the matrix")
    return len(basis)


__all__ = ["ExactMatrix", "GaussianRational", "Q", "q", "CommutantError", "commutant_basis", "commutant_dimension"]
