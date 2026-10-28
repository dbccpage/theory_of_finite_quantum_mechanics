"""Partial-pivoted LU factorization over Q.

Origin: code/rust/src/mub/native/mub6_smale_sentry.rs, which states
that an n by n matrix has an exact LU factorization with partial row pivoting,
P * A = L * U, and that L has ones on the diagonal.
Claim: urn:omega:fqm:linear-algebra:partial-pivoted-lu:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_elimination.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 8; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: plu_factor returns the permutation as a matrix and checks
P A = L U for one rational square matrix. This file does not solve A x = b,
does not compute a Smale alpha, and does not admit floats or Q(i).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class EliminationError(MatrixError):
    """One violated LU invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> EliminationError:
    return EliminationError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; PLU in this module is over Q", role=role)
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
        raise _fail("PLU input is not an ExactMatrix", received=type(matrix).__name__)
    rows = _require_dimension(matrix.rows, "rows")
    cols = _require_dimension(matrix.cols, "cols")
    _require_data_length(matrix, rows, cols)
    data = [_require_entry(value, f"entry[{index}]") for index, value in enumerate(matrix.data)]
    return ExactMatrix(rows, cols, data)


def _require_square(matrix: ExactMatrix) -> ExactMatrix:
    if matrix.rows != matrix.cols:
        raise _fail("PLU requires a square matrix", rows=matrix.rows, cols=matrix.cols)
    return matrix


def _one_row(matrix: ExactMatrix, row: int) -> list[Fraction]:
    values: list[Fraction] = []
    col = 0
    while col < matrix.cols:
        values.append(_require_entry(matrix.get(row, col), f"row[{row}]"))
        col += 1
    return values


def _copy_rows(matrix: ExactMatrix) -> list[list[Fraction]]:
    rows: list[list[Fraction]] = []
    index = 0
    while index < matrix.rows:
        rows.append(_one_row(matrix, index))
        index += 1
    return rows


def _unit_row(size: int, index: int) -> list[Fraction]:
    row: list[Fraction] = []
    column = 0
    while column < size:
        if index == column:
            row.append(Fraction(1))
        else:
            row.append(Fraction(0))
        column += 1
    return row


def _identity_rows(size: int) -> list[list[Fraction]]:
    rows: list[list[Fraction]] = []
    index = 0
    while index < size:
        rows.append(_unit_row(size, index))
        index += 1
    return rows


def _pivot_row(rows: list[list[Fraction]], column: int) -> int:
    chosen = column
    pivot_size = abs(rows[column][column])
    index = column + 1
    while index < len(rows):
        size = abs(rows[index][column])
        if size > pivot_size:
            chosen = index
            pivot_size = size
        index += 1
    if pivot_size == 0:
        raise _fail("matrix is singular", column=column)
    return chosen


def _swap_prefix(lower: list[list[Fraction]], left: int, right: int, limit: int) -> None:
    column = 0
    while column < limit:
        lower[left][column], lower[right][column] = lower[right][column], lower[left][column]
        column += 1


def _clear_from(current: list[list[Fraction]], row: int, column: int, factor: Fraction) -> None:
    index = column
    while index < len(current):
        current[row][index] -= factor * current[column][index]
        index += 1


def _eliminate(current: list[list[Fraction]], lower: list[list[Fraction]], column: int) -> None:
    pivot = current[column][column]
    row = column + 1
    while row < len(current):
        factor = current[row][column] / pivot
        lower[row][column] = factor
        _clear_from(current, row, column, factor)
        current[row][column] = Fraction(0)
        row += 1


def _permutation(origin: list[int]) -> ExactMatrix:
    size = len(origin)
    data: list[Fraction] = []
    row = 0
    while row < size:
        column = 0
        while column < size:
            if origin[row] == column:
                data.append(Fraction(1))
            else:
                data.append(Fraction(0))
            column += 1
        row += 1
    return ExactMatrix(size, size, data)


def _as_matrix(rows: list[list[Fraction]]) -> ExactMatrix:
    if not rows:
        return ExactMatrix(0, 0, [])
    data: list[Fraction] = []
    for row in rows:
        data.extend(row)
    size = len(rows)
    return ExactMatrix(size, size, data)


def _require_factors(
    perm: ExactMatrix, original: ExactMatrix, lower: ExactMatrix, upper: ExactMatrix
) -> None:
    if perm * original != lower * upper:
        raise _fail("constructed factors do not satisfy P*A = L*U", rows=original.rows)


def _require_unit_lower(lower: ExactMatrix) -> None:
    row = 0
    while row < lower.rows:
        if _require_entry(lower.get(row, row), "diagonal") != 1:
            raise _fail("lower factor is not unit triangular", index=row)
        column = row + 1
        while column < lower.cols:
            if _require_entry(lower.get(row, column), "upper") != 0:
                raise _fail("lower factor has an upper entry", row=row, col=column)
            column += 1
        row += 1


def plu_factor(matrix: object) -> tuple[ExactMatrix, ExactMatrix, ExactMatrix]:
    """Return P, L, U with P A = L U and ones on the diagonal of L."""
    parsed = _require_square(_rational_matrix(matrix))
    current = _copy_rows(parsed)
    lower_rows = _identity_rows(parsed.rows)
    origin = list(range(parsed.rows))
    column = 0
    while column < parsed.rows:
        chosen = _pivot_row(current, column)
        if chosen != column:
            current[column], current[chosen] = current[chosen], current[column]
            origin[column], origin[chosen] = origin[chosen], origin[column]
            _swap_prefix(lower_rows, column, chosen, column)
        _eliminate(current, lower_rows, column)
        column += 1
    perm = _permutation(origin)
    lower = _as_matrix(lower_rows)
    upper = _as_matrix(current)
    _require_factors(perm, parsed, lower, upper)
    _require_unit_lower(lower)
    return perm, lower, upper


def witness_upper_entry() -> Fraction:
    """(1, 1) entry of U for [[1, 2], [3, 4]]. Partial pivoting makes it 2/3."""
    matrix = ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]])
    _perm, _lower, upper = plu_factor(matrix)
    return _require_entry(upper.get(1, 1), "witness")


__all__ = [
    "EliminationError",
    "ExactMatrix",
    "plu_factor",
    "witness_upper_entry",
]
