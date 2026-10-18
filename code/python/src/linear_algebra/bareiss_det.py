"""Fraction-free Bareiss determinant over Q, checked against elimination.

Origin: code/rust/src/linear_algebra/bareiss_det.rs, which states that Bareiss
elimination uses checked exact divisions, and code/python/src/linear_algebra/matrix.py
ExactMatrix.determinant, the Gaussian comparison used by this certificate.
Claim: urn:omega:fqm:linear-algebra:bareiss-determinant:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_bareiss_det.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: bareiss_matches_elimination checks the rational matrix it is given.
The Bareiss pivot is compared with ExactMatrix.determinant on that matrix.
This file does not enforce the Rust fuel, bit, or element limits, does not
solve a linear system, and does not admit floats or Q(i).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class BareissError(MatrixError):
    """One violated Bareiss invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> BareissError:
    return BareissError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; Bareiss determinant in this module is over Q", role=role)
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
        raise _fail("Bareiss input is not an ExactMatrix", received=type(matrix).__name__)
    rows = _require_dimension(matrix.rows, "rows")
    cols = _require_dimension(matrix.cols, "cols")
    if rows != cols:
        raise _fail("determinant requires a square matrix", rows=rows, cols=cols)
    _require_data_length(matrix, rows, cols)
    data = [_require_entry(value, f"entry[{index}]") for index, value in enumerate(matrix.data)]
    return ExactMatrix(rows, cols, data)


def _rational_square_grid(matrix: object) -> list[list[Fraction]]:
    source = _rational_square(matrix)
    size = source.rows
    grid: list[list[Fraction]] = []
    for row in range(size):
        grid.append([_require_entry(source.get(row, col), "grid-entry") for col in range(size)])
    return grid


def _find_pivot_row(grid: list[list[Fraction]], column: int) -> int | None:
    size = len(grid)
    for row in range(column + 1, size):
        if grid[row][column] != 0:
            return row
    return None


def _clear_row(
    grid: list[list[Fraction]],
    column: int,
    row: int,
    pivot: Fraction,
    previous: Fraction,
) -> None:
    size = len(grid)
    current = grid[row]
    pivot_row = grid[column]
    for index in range(column + 1, size):
        numerator = pivot * current[index] - current[column] * pivot_row[index]
        current[index] = numerator / previous
    current[column] = Fraction(0)


def _advance(
    grid: list[list[Fraction]],
    column: int,
    sign: int,
    previous: Fraction,
) -> tuple[int, Fraction, bool]:
    if grid[column][column] == 0:
        swap = _find_pivot_row(grid, column)
        if swap is None:
            return sign, previous, True
        grid[column], grid[swap] = grid[swap], grid[column]
        sign = -sign
    pivot = grid[column][column]
    for row in range(column + 1, len(grid)):
        _clear_row(grid, column, row, pivot, previous)
    return sign, pivot, False


def bareiss_determinant(matrix: object) -> Fraction:
    """Return det(matrix) by the one-step Bareiss recurrence over Q."""
    grid = _rational_square_grid(matrix)
    size = len(grid)
    if size == 0:
        return Fraction(1)
    sign = 1
    previous = Fraction(1)
    for column in range(size - 1):
        sign, previous, singular = _advance(grid, column, sign, previous)
        if singular:
            return Fraction(0)
    return sign * grid[size - 1][size - 1]


def _as_fraction_determinant(value: object) -> Fraction:
    if type(value) is not Fraction:
        raise _fail("elimination determinant left Q", received=type(value).__name__)
    return value


def _require_agreement(bareiss: Fraction, gauss: Fraction) -> None:
    if bareiss != gauss:
        raise _fail(
            "Bareiss determinant disagrees with elimination",
            bareiss=str(bareiss),
            elimination=str(gauss),
        )


def bareiss_matches_elimination(matrix: object) -> Fraction:
    """Return the Bareiss determinant after checking it against Gaussian elimination."""
    source = _rational_square(matrix)
    bareiss = bareiss_determinant(source)
    gauss = _as_fraction_determinant(source.determinant())
    _require_agreement(bareiss, gauss)
    return bareiss


__all__ = [
    "BareissError",
    "ExactMatrix",
    "bareiss_determinant",
    "bareiss_matches_elimination",
]
