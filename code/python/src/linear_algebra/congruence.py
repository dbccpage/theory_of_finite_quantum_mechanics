"""Rational congruence reduction of a symmetric matrix to a diagonal.

Origin: code/python/src/linear_algebra/congruence.py
Claim: the returned invertible P satisfies P^T A P = D with D diagonal.
AuthorityEffect: None. This is a congruence over Q, not an orthogonal diagonalization.
"""
from fractions import Fraction
from typing import Tuple

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class CongruenceError(Exception):
    """The matrix is not a rational symmetric matrix, or reduction failed."""


def _rational(value) -> Fraction:
    if isinstance(value, GaussianRational):
        raise CongruenceError("congruence in this module is over Q, not Q(i)")
    try:
        return Fraction(value)
    except (TypeError, ValueError) as exc:
        raise CongruenceError(f"entry {value!r} is not rational") from exc


def _elementary(n: int, row: int, col: int, coeff: Fraction) -> ExactMatrix:
    data = []
    for i in range(n):
        for j in range(n):
            value = Fraction(1) if i == j else Fraction(0)
            if i == row and j == col:
                value += coeff
            data.append(value)
    return ExactMatrix(n, n, data)


def congruent_diagonal(matrix: ExactMatrix) -> Tuple[ExactMatrix, ExactMatrix]:
    """Return D, P with P invertible over Q and P^T * matrix * P = D diagonal."""
    if matrix.rows != matrix.cols:
        raise CongruenceError(f"congruence requires a square matrix, got {matrix.shape()}")
    n = matrix.rows
    current = ExactMatrix(n, n, [_rational(value) for value in matrix.data])
    for i in range(n):
        for j in range(n):
            if current.get(i, j) != current.get(j, i):
                raise CongruenceError("congruence requires a symmetric matrix")
    transform = ExactMatrix.identity(n)
    for k in range(n):
        if all(current.get(i, j) == 0 for i in range(k, n) for j in range(k, n)):
            break
        if current.get(k, k) == 0:
            donor = next(j for j in range(k + 1, n) if current.get(k, j) != 0)
            coeff = Fraction(1)
            trial = 2 * coeff * Fraction(current.get(k, donor)) + coeff * coeff * Fraction(current.get(donor, donor))
            if trial == 0:
                coeff = Fraction(2)
            shear = _elementary(n, donor, k, coeff)
            current = shear.transpose() * current * shear
            transform = transform * shear
        for i in range(k + 1, n):
            pivot = Fraction(current.get(k, k))
            if pivot == 0 or current.get(i, k) == 0:
                continue
            factor = Fraction(current.get(i, k)) / pivot
            elim = _elementary(n, k, i, -factor)
            current = elim.transpose() * current * elim
            transform = transform * elim
    for i in range(n):
        for j in range(n):
            if i != j and current.get(i, j) != 0:
                raise CongruenceError("reduction left a nonzero off-diagonal entry")
    rebuilt = transform.transpose() * ExactMatrix(n, n, [_rational(value) for value in matrix.data]) * transform
    if rebuilt != current:
        raise CongruenceError("P^T A P does not equal the diagonal reduction")
    return current, transform


__all__ = ["ExactMatrix", "GaussianRational", "Q", "q", "CongruenceError", "congruent_diagonal"]
