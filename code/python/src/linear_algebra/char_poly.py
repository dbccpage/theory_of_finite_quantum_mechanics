"""Characteristic polynomial by the Faddeev–LeVerrier recurrence over Q.

Origin: code/python/src/linear_algebra/char_poly.py
Claim: det(λI − A) = λ^n + c_1 λ^{n-1} + ... + c_n, and that polynomial kills A.
AuthorityEffect: None. Cayley–Hamilton is checked on the matrix that was passed.
"""
from fractions import Fraction
from typing import List

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class CharacteristicError(Exception):
    """The characteristic polynomial is only built for rational square matrices."""


def _as_rational_square(matrix: ExactMatrix) -> ExactMatrix:
    if matrix.rows != matrix.cols:
        raise CharacteristicError(f"characteristic polynomial requires a square matrix, got {matrix.shape()}")
    data = []
    for value in matrix.data:
        if isinstance(value, GaussianRational):
            raise CharacteristicError("characteristic polynomial in this module is over Q, not Q(i)")
        try:
            data.append(Fraction(value))
        except (TypeError, ValueError) as exc:
            raise CharacteristicError(f"entry {value!r} is not rational") from exc
    return ExactMatrix(matrix.rows, matrix.cols, data)


def _trace(matrix: ExactMatrix) -> Fraction:
    total = Fraction(0)
    for i in range(matrix.rows):
        total += Fraction(matrix.get(i, i))
    return total


def _add_scaled_identity(matrix: ExactMatrix, coeff: Fraction) -> ExactMatrix:
    n = matrix.rows
    data = []
    for i in range(n):
        for j in range(n):
            value = Fraction(matrix.get(i, j))
            if i == j:
                value += coeff
            data.append(value)
    return ExactMatrix(n, n, data)


def characteristic_coefficients(matrix: ExactMatrix) -> List[Fraction]:
    """Return [1, c_1, ..., c_n] for monic det(λI − A)."""
    source = _as_rational_square(matrix)
    n = source.rows
    if n == 0:
        return [Fraction(1)]
    coeffs = [Fraction(1)]
    leverrier = source
    for k in range(1, n + 1):
        coeff = -_trace(leverrier) / Fraction(k)
        coeffs.append(coeff)
        if k == n:
            break
        leverrier = source * _add_scaled_identity(leverrier, coeff)
    return coeffs


def matrix_polynomial(matrix: ExactMatrix, coeffs: List[Fraction]) -> ExactMatrix:
    """Evaluate c_0 A^{n} + c_1 A^{n-1} + ... + c_n I, with c_0 the leading term."""
    source = _as_rational_square(matrix)
    n = source.rows
    if len(coeffs) != n + 1:
        raise CharacteristicError(f"expected {n + 1} coefficients, got {len(coeffs)}")
    acc = ExactMatrix.zeros(n, n)
    power = ExactMatrix.identity(n)
    for coeff in reversed(coeffs):
        if coeff != 0:
            term = ExactMatrix(n, n, [Fraction(coeff) * Fraction(value) for value in power.data])
            acc = acc + term
        power = source * power
    return acc


def cayley_hamilton_defect(matrix: ExactMatrix) -> Fraction:
    """Sum of absolute entries of χ(A). The Cayley–Hamilton theorem says this is 0."""
    coeffs = characteristic_coefficients(matrix)
    value = matrix_polynomial(matrix, coeffs)
    defect = Fraction(0)
    for entry in value.data:
        defect += abs(Fraction(entry))
    return defect


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "Q",
    "q",
    "CharacteristicError",
    "characteristic_coefficients",
    "matrix_polynomial",
    "cayley_hamilton_defect",
]
