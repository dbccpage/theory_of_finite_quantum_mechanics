"""Symmetric congruence diagonalisation over Q.

Origin: code/rust/src/linear_algebra/congruence.rs, which states that a
symmetric matrix has an invertible S and a diagonal D with Sᵀ A S = D, that
the field must satisfy 2 ≠ 0, and that a non-symmetric matrix is refused.
Claim: urn:omega:fqm:linear-algebra:symmetric-congruence:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_congruence.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 6; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: congruent_diagonal replays Sᵀ A S against the rational symmetric
matrix it is given. This file does not treat the Hermitian case, does not
read inertia, does not charge allocation fuel, and does not admit floats or Q(i).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class CongruenceError(MatrixError):
    """One violated congruence invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CongruenceError:
    return CongruenceError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; congruence in this module is over Q", role=role)
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


def _rational_matrix(matrix: object) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail("congruence input is not an ExactMatrix", received=type(matrix).__name__)
    rows = _require_dimension(matrix.rows, "rows")
    cols = _require_dimension(matrix.cols, "cols")
    _require_data_length(matrix, rows, cols)
    data = [_require_entry(value, f"entry[{index}]") for index, value in enumerate(matrix.data)]
    return ExactMatrix(rows, cols, data)


def _require_square(matrix: ExactMatrix) -> ExactMatrix:
    if matrix.rows != matrix.cols:
        raise _fail("congruence requires a square matrix", rows=matrix.rows, cols=matrix.cols)
    return matrix


def _require_symmetric(matrix: ExactMatrix) -> ExactMatrix:
    row = 0
    while row < matrix.rows:
        col = row + 1
        while col < matrix.cols:
            left = _require_entry(matrix.get(row, col), "symmetry")
            right = _require_entry(matrix.get(col, row), "symmetry")
            if left != right:
                raise _fail("congruence requires a symmetric matrix", row=row, col=col)
            col += 1
        row += 1
    return matrix


def _identity_data(size: int) -> list[Fraction]:
    data = [Fraction(0)] * (size * size)
    slot = 0
    while slot < size:
        data[slot * size + slot] = Fraction(1)
        slot += 1
    return data


def _add_multiple(size: int, target: int, source: int, factor: Fraction) -> ExactMatrix:
    """E = I + factor · e_source · e_targetᵀ, so column target gains factor · column source."""
    data = _identity_data(size)
    index = source * size + target
    data[index] = data[index] + factor
    return ExactMatrix(size, size, data)


def _transposition(size: int, left: int, right: int) -> ExactMatrix:
    data = _identity_data(size)
    data[left * size + left] = Fraction(0)
    data[right * size + right] = Fraction(0)
    data[left * size + right] = Fraction(1)
    data[right * size + left] = Fraction(1)
    return ExactMatrix(size, size, data)


def _apply(
    current: ExactMatrix, transform: ExactMatrix, operator: ExactMatrix
) -> tuple[ExactMatrix, ExactMatrix]:
    updated = operator.transpose() * current * operator
    return updated, transform * operator


def _diagonal_donor(matrix: ExactMatrix, start: int) -> int | None:
    index = start + 1
    while index < matrix.rows:
        if _require_entry(matrix.get(index, index), "donor") != 0:
            return index
        index += 1
    return None


def _off_pair(matrix: ExactMatrix, start: int) -> tuple[int, int] | None:
    row = start
    while row < matrix.rows:
        col = row + 1
        while col < matrix.rows:
            if _require_entry(matrix.get(row, col), "off-pair") != 0:
                return row, col
            col += 1
        row += 1
    return None


def _pivot_ready(
    current: ExactMatrix, transform: ExactMatrix, index: int
) -> tuple[ExactMatrix, ExactMatrix, bool]:
    if _require_entry(current.get(index, index), "pivot") != 0:
        return current, transform, False
    donor = _diagonal_donor(current, index)
    if donor is not None:
        updated, moved = _apply(current, transform, _transposition(current.rows, index, donor))
        return updated, moved, False
    pair = _off_pair(current, index)
    if pair is None:
        return current, transform, True
    row, col = pair
    entry = _require_entry(current.get(row, col), "shear")
    coeff = Fraction(1) / entry
    updated, moved = _apply(current, transform, _add_multiple(current.rows, row, col, coeff))
    if row != index:
        updated, moved = _apply(updated, moved, _transposition(updated.rows, index, row))
    return updated, moved, False


def _clear_row(
    current: ExactMatrix, transform: ExactMatrix, index: int
) -> tuple[ExactMatrix, ExactMatrix]:
    pivot = _require_entry(current.get(index, index), "clear-pivot")
    if pivot == 0:
        raise _fail("congruence pivot vanished", index=index)
    column = index + 1
    while column < current.rows:
        entry = _require_entry(current.get(index, column), "clear")
        if entry != 0:
            factor = -(entry / pivot)
            current, transform = _apply(
                current, transform, _add_multiple(current.rows, column, index, factor)
            )
        column += 1
    return current, transform


def _off_diagonal_mass(matrix: ExactMatrix) -> Fraction:
    total = Fraction(0)
    row = 0
    while row < matrix.rows:
        col = 0
        while col < matrix.cols:
            if row != col:
                total += abs(_require_entry(matrix.get(row, col), "off-diagonal"))
            col += 1
        row += 1
    return total


def _gap_mass(matrix: ExactMatrix) -> Fraction:
    total = Fraction(0)
    for value in matrix.data:
        total += abs(_require_entry(value, "gap-entry"))
    return total


def _require_diagonal(matrix: ExactMatrix) -> None:
    mass = _off_diagonal_mass(matrix)
    if mass != 0:
        raise _fail("reduction left a nonzero off-diagonal entry", mass=str(mass))


def _require_replay(original: ExactMatrix, diagonal: ExactMatrix, transform: ExactMatrix) -> None:
    rebuilt = transform.transpose() * original * transform
    mass = _gap_mass(rebuilt - diagonal)
    if mass != 0:
        raise _fail("S transpose A S differs from the diagonal", mass=str(mass))


def _require_unimodular(transform: ExactMatrix) -> None:
    det = transform.determinant()
    if type(det) is not Fraction:
        raise _fail("transform determinant is not rational", received=type(det).__name__)
    if abs(det) != 1:
        raise _fail("transform determinant is not ±1", determinant=str(det))


def congruent_diagonal(matrix: object) -> tuple[ExactMatrix, ExactMatrix]:
    """Return D, S with Sᵀ A S = D, D diagonal, and det S = ±1."""
    parsed = _require_symmetric(_require_square(_rational_matrix(matrix)))
    current = parsed
    transform = ExactMatrix.identity(parsed.rows)
    index = 0
    while index < parsed.rows:
        current, transform, finished = _pivot_ready(current, transform, index)
        if finished:
            break
        current, transform = _clear_row(current, transform, index)
        index += 1
    _require_diagonal(current)
    _require_replay(parsed, current, transform)
    _require_unimodular(transform)
    return current, transform


def witness_diagonal_entry() -> Fraction:
    """(1, 1) entry of the diagonal of [[1, 2], [2, 3]]. It is −1."""
    shear = ExactMatrix.from_rows([[Fraction(0), Fraction(2)], [Fraction(2), Fraction(0)]])
    shear_diagonal, _shear_transform = congruent_diagonal(shear)
    pivot = _require_entry(shear_diagonal.get(0, 0), "shear-witness")
    if pivot != 2:
        raise _fail("shear diagonal moved", received=str(pivot))
    matrix = ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(2), Fraction(3)]])
    diagonal, _transform = congruent_diagonal(matrix)
    return _require_entry(diagonal.get(1, 1), "witness")


__all__ = [
    "CongruenceError",
    "ExactMatrix",
    "congruent_diagonal",
    "witness_diagonal_entry",
]
