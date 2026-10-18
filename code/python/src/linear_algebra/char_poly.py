"""Characteristic polynomial by the Faddeev–LeVerrier recurrence over Q.

Origin: code/rust/src/linear_algebra/char_poly.rs, which defines the
characteristic polynomial as det(xI − A), and evidence/dossiers/reduction_proof.md
section 1.3, which states that this polynomial has degree d.
Claim: urn:omega:fqm:linear-algebra:characteristic-polynomial:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_char_poly.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: certify_characteristic_polynomial checks the rational matrix it is
given. The coefficients come from the LeVerrier recurrence, the constant term
is checked against (-1)^n det(A) from Gaussian elimination, and the
Cayley–Hamilton defect on that same matrix is required to be zero. This file
does not implement the division-free Berkowitz algorithm, does not compute a
minimal polynomial, does not split the polynomial, and does not admit floats
or Q(i).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, Sequence

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class CharacteristicError(MatrixError):
    """One violated characteristic-polynomial invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CharacteristicError:
    return CharacteristicError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; characteristic polynomial in this module is over Q", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("matrix entry is not an exact rational", role=role, received=type(value).__name__)


def _require_dimension(value: object, role: str) -> int:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a matrix dimension was required", role=role)
    if type(value) is int:
        if value < 0:
            raise _fail("matrix shape is negative", role=role, received=value)
        return value
    raise _fail("matrix shape is not an integer", role=role, received=type(value).__name__)


def _require_data_length(matrix: ExactMatrix, rows: int, cols: int) -> None:
    length = len(matrix.data)
    if length != rows * cols:
        raise _fail("matrix data length does not match the shape", length=length, rows=rows, cols=cols)


def _rational_square(matrix: object) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail("characteristic input is not an ExactMatrix", received=type(matrix).__name__)
    rows = _require_dimension(matrix.rows, "rows")
    cols = _require_dimension(matrix.cols, "cols")
    if rows != cols:
        raise _fail("characteristic polynomial requires a square matrix", rows=rows, cols=cols)
    _require_data_length(matrix, rows, cols)
    data = [_require_entry(value, f"entry[{index}]") for index, value in enumerate(matrix.data)]
    return ExactMatrix(rows, cols, data)


def _trace(matrix: ExactMatrix) -> Fraction:
    total = Fraction(0)
    for index in range(matrix.rows):
        total += _require_entry(matrix.get(index, index), "trace")
    return total


def _on_diagonal(index: int, size: int) -> bool:
    return index % size == index // size


def _add_scaled_identity(matrix: ExactMatrix, coeff: Fraction) -> ExactMatrix:
    size = matrix.rows
    data: list[Fraction] = []
    for index, value in enumerate(matrix.data):
        entry = _require_entry(value, "scaled-entry")
        if _on_diagonal(index, size):
            entry = entry + coeff
        data.append(entry)
    return ExactMatrix(size, size, data)


def _advance_leverrier(
    source: ExactMatrix,
    current: ExactMatrix,
    coeff: Fraction,
    step: int,
    size: int,
) -> ExactMatrix:
    if step == size:
        return current
    return source * _add_scaled_identity(current, coeff)


def _leverrier(source: ExactMatrix) -> list[Fraction]:
    size = source.rows
    coeffs = [Fraction(1)]
    current = source
    for step in range(1, size + 1):
        coeff = -_trace(current) / Fraction(step)
        coeffs.append(coeff)
        current = _advance_leverrier(source, current, coeff, step, size)
    return coeffs


def _signed_determinant(source: ExactMatrix) -> Fraction:
    determinant = source.determinant()
    if type(determinant) is not Fraction:
        raise _fail("elimination determinant left Q", received=type(determinant).__name__)
    if source.rows % 2 == 0:
        return determinant
    return -determinant


def _require_constant_term(source: ExactMatrix, coeffs: Sequence[Fraction]) -> None:
    expected = _signed_determinant(source)
    if coeffs[-1] != expected:
        raise _fail(
            "constant term is not (-1)^n det(A)",
            n=source.rows,
            constant=str(coeffs[-1]),
            determinant=str(expected),
        )


def characteristic_coefficients(matrix: object) -> list[Fraction]:
    """Return [1, c_1, ..., c_n] for monic det(λI − A)."""
    source = _rational_square(matrix)
    coeffs = [Fraction(1)] if source.rows == 0 else _leverrier(source)
    _require_constant_term(source, coeffs)
    return coeffs


def _fraction_data(matrix: ExactMatrix, role: str) -> list[Fraction]:
    return [_require_entry(value, role) for value in matrix.data]


def _add_term(total: ExactMatrix, power: ExactMatrix, coeff: Fraction) -> ExactMatrix:
    if coeff == 0:
        return total
    scaled = [coeff * entry for entry in _fraction_data(power, "power-entry")]
    return total + ExactMatrix(power.rows, power.cols, scaled)


def _horner(source: ExactMatrix, coeffs: Sequence[Fraction]) -> ExactMatrix:
    size = source.rows
    total = ExactMatrix.zeros(size, size)
    power = ExactMatrix.identity(size)
    for coeff in reversed(coeffs):
        total = _add_term(total, power, coeff)
        power = source * power
    return total


def matrix_polynomial(matrix: object, coeffs: Sequence[object]) -> ExactMatrix:
    """Evaluate c_0 A^n + ... + c_n I, with c_0 the leading coefficient."""
    source = _rational_square(matrix)
    degree = source.rows
    if len(coeffs) != degree + 1:
        raise _fail(
            "coefficient count is not one more than the dimension",
            degree=degree,
            count=len(coeffs),
        )
    rational = [_require_entry(coeff, f"coeff[{index}]") for index, coeff in enumerate(coeffs)]
    return _horner(source, rational)


def _entry_mass(matrix: ExactMatrix) -> Fraction:
    defect = Fraction(0)
    for entry in matrix.data:
        defect += abs(_require_entry(entry, "defect-entry"))
    return defect


def cayley_hamilton_defect(matrix: object) -> Fraction:
    """Sum of absolute entries of χ(A)."""
    source = _rational_square(matrix)
    value = matrix_polynomial(source, characteristic_coefficients(source))
    return _entry_mass(value)


def _require_zero_defect(defect: Fraction, degree: int) -> None:
    if defect != 0:
        raise _fail("Cayley-Hamilton defect is nonzero", defect=str(defect), degree=degree)


def certify_characteristic_polynomial(matrix: object) -> tuple[Fraction, ...]:
    """Return the monic coefficients after the constant-term and Cayley–Hamilton checks."""
    coeffs = characteristic_coefficients(matrix)
    _require_zero_defect(cayley_hamilton_defect(matrix), len(coeffs) - 1)
    return tuple(coeffs)


__all__ = [
    "CharacteristicError",
    "ExactMatrix",
    "cayley_hamilton_defect",
    "certify_characteristic_polynomial",
    "characteristic_coefficients",
    "matrix_polynomial",
]
