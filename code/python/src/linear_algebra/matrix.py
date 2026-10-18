"""Exact matrix arithmetic over Q and Q(i).

Origin: code/rust/src/linear_algebra/matrix.rs, which states matrix construction
and arithmetic over an exact field, with shapes checked before any scalar work.
Claim: urn:omega:fqm:linear-algebra:exact-matrix:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_matrix.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: Construction stores the caller's entries so a neighboring scanner
can read them. Every arithmetic, elimination, comparison, and digest method
refuses float and bool before a numeric branch. This file does not enforce
operation budgets, Kronecker products, or matrix powers.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from typing import Mapping, Sequence

from .scalars import GaussianRational


Scalar = Fraction | GaussianRational


class MatrixError(Exception):
    """Base error shared with neighboring exact-matrix modules."""


class MatrixFailure(MatrixError, ValueError):
    """One violated matrix invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


class MatrixIndexError(MatrixError, IndexError):
    """An entry index outside the stored shape."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> MatrixFailure:
    return MatrixFailure(invariant, parameters)


def _index_fail(invariant: str, **parameters: object) -> MatrixIndexError:
    return MatrixIndexError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _reject_bool(value: object, role: str, invariant: str) -> None:
    if type(value) is bool:
        raise _fail(invariant, role=role)


def _dimension(value: object, role: str) -> int:
    _refuse_float(value, role)
    _reject_bool(value, role, "boolean refused where a matrix dimension was required")
    if isinstance(value, int):
        return value
    raise _fail("matrix dimension must be an exact integer", role=role, received=type(value).__name__)


def _require_scalar(value: object, role: str) -> Scalar:
    _refuse_float(value, role)
    _reject_bool(value, role, "boolean refused where an exact scalar was required")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, GaussianRational):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("exact scalar required", role=role, received=type(value).__name__)


def _uses_gaussian(values: Sequence[object]) -> bool:
    return any(isinstance(item, GaussianRational) for item in values)


def _zero(gaussian: bool) -> Scalar:
    if gaussian:
        return GaussianRational(0, 0)
    return Fraction(0)


def _one(gaussian: bool) -> Scalar:
    if gaussian:
        return GaussianRational(1, 0)
    return Fraction(1)


def _is_zero(value: Scalar) -> bool:
    if isinstance(value, GaussianRational):
        return value.is_zero()
    return value == 0


def _diagonal_entry(zero: Scalar, one: Scalar, row: int, col: int) -> Scalar:
    if row == col:
        return one
    return zero


def _times(left: Scalar, right: Scalar) -> Scalar:
    if isinstance(left, GaussianRational):
        return left * right
    if isinstance(right, GaussianRational):
        return right * left
    return left * right


def _plus(left: Scalar, right: Scalar) -> Scalar:
    if isinstance(left, GaussianRational):
        return left + right
    if isinstance(right, GaussianRational):
        return right + left
    return left + right


def _minus(left: Scalar, right: Scalar) -> Scalar:
    if isinstance(left, GaussianRational):
        return left - right
    if isinstance(right, GaussianRational):
        return -(right - left)
    return left - right


def _divide(left: Scalar, right: Scalar) -> Scalar:
    if isinstance(left, GaussianRational):
        return left / right
    if isinstance(right, GaussianRational):
        return GaussianRational(left, 0) / right
    return left / right


def _scale(value: Scalar, factor: int) -> Scalar:
    if isinstance(value, GaussianRational):
        return value * factor
    return value * factor


def _dot(left: Sequence[Scalar], right: Sequence[Scalar], gaussian: bool) -> Scalar:
    total = _zero(gaussian)
    for left_value, right_value in zip(left, right, strict=True):
        total = _plus(total, _times(left_value, right_value))
    return total


def _pivot_row(grid: Sequence[Sequence[Scalar]], start: int, column: int) -> int | None:
    for row in range(start, len(grid)):
        if not _is_zero(grid[row][column]):
            return row
    return None


def _clear_row(grid: list[list[Scalar]], row: int, pivot_row: int, column: int) -> None:
    factor = grid[row][column]
    if _is_zero(factor):
        return
    for index in range(len(grid[row])):
        grid[row][index] = _minus(grid[row][index], _times(factor, grid[pivot_row][index]))


def _normalize_and_clear(grid: list[list[Scalar]], pivot_row: int, column: int) -> None:
    pivot = grid[pivot_row][column]
    for index in range(len(grid[pivot_row])):
        grid[pivot_row][index] = _divide(grid[pivot_row][index], pivot)
    for row in range(len(grid)):
        if row != pivot_row:
            _clear_row(grid, row, pivot_row, column)


def _eliminate_column(grid: list[list[Scalar]], pivot_row: int, column: int, pivots: list[int]) -> int:
    if pivot_row >= len(grid):
        return pivot_row
    found = _pivot_row(grid, pivot_row, column)
    if found is None:
        return pivot_row
    if found != pivot_row:
        grid[pivot_row], grid[found] = grid[found], grid[pivot_row]
    _normalize_and_clear(grid, pivot_row, column)
    pivots.append(column)
    return pivot_row + 1


def _clear_det_row(grid: list[list[Scalar]], row: int, index: int, pivot: Scalar) -> None:
    factor = grid[row][index]
    if _is_zero(factor):
        return
    scale = _divide(factor, pivot)
    for column in range(index, len(grid)):
        grid[row][column] = _minus(grid[row][column], _times(scale, grid[index][column]))


def _clear_below(grid: list[list[Scalar]], index: int, pivot: Scalar) -> None:
    for row in range(index + 1, len(grid)):
        _clear_det_row(grid, row, index, pivot)


def _det_step(grid: list[list[Scalar]], index: int, det: Scalar, sign: int) -> tuple[Scalar, int, bool]:
    pivot = _pivot_row(grid, index, index)
    if pivot is None:
        return det, sign, True
    if pivot != index:
        grid[index], grid[pivot] = grid[pivot], grid[index]
        sign = -sign
    pivot_value = grid[index][index]
    _clear_below(grid, index, pivot_value)
    return _times(det, pivot_value), sign, False


def _augment_identity(source: ExactMatrix, zero: Scalar, one: Scalar) -> list[Scalar]:
    data: list[Scalar] = []
    for row in range(source.rows):
        data.extend(source.row_scalars(row, isinstance(zero, GaussianRational)))
        data.extend(_diagonal_entry(zero, one, row, col) for col in range(source.rows))
    return data


def _right_block(reduced: ExactMatrix, size: int) -> list[Scalar]:
    data: list[Scalar] = []
    for row in range(size):
        for col in range(size):
            data.append(reduced.scalar_at(row, size + col))
    return data


class ExactMatrix:
    """Row-major matrix over Q or Q(i). Stored entries are scanned by neighbors."""

    __slots__ = ("rows", "cols", "data")

    def __init__(self, rows: object, cols: object, data: Sequence[object]) -> None:
        row_count = _dimension(rows, "rows")
        col_count = _dimension(cols, "cols")
        if len(data) != row_count * col_count:
            raise _fail(
                "Data length does not match dimensions",
                length=len(data),
                rows=row_count,
                cols=col_count,
            )
        self.rows = row_count
        self.cols = col_count
        self.data: list[object] = list(data)

    @classmethod
    def zeros(cls, rows: object, cols: object, is_gaussian: bool = False) -> ExactMatrix:
        row_count = _dimension(rows, "rows")
        col_count = _dimension(cols, "cols")
        zero = _zero(is_gaussian)
        return cls(row_count, col_count, [zero] * (row_count * col_count))

    @classmethod
    def identity(cls, n: object, is_gaussian: bool = False) -> ExactMatrix:
        size = _dimension(n, "rows")
        zero = _zero(is_gaussian)
        one = _one(is_gaussian)
        data = [_diagonal_entry(zero, one, row, col) for row in range(size) for col in range(size)]
        return cls(size, size, data)

    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[object]]) -> ExactMatrix:
        if not rows:
            return cls(0, 0, [])
        width = len(rows[0])
        data: list[object] = []
        for row in rows:
            if len(row) != width:
                raise _fail("Jagged rows are not allowed", width=width, received=len(row))
            data.extend(row)
        return cls(len(rows), width, data)

    def shape(self) -> tuple[int, int]:
        return self.rows, self.cols

    def get(self, row: int, col: int) -> object:
        self._require_index(row, col)
        return self.data[row * self.cols + col]

    def set(self, row: int, col: int, value: object) -> None:
        self._require_index(row, col)
        self.data[row * self.cols + col] = value

    def row(self, row: int) -> list[object]:
        return self.data[row * self.cols : (row + 1) * self.cols]

    def col(self, col: int) -> list[object]:
        return [self.data[row * self.cols + col] for row in range(self.rows)]

    def scalar_at(self, row: int, col: int) -> Scalar:
        return _require_scalar(self.get(row, col), "entry")

    def row_scalars(self, row: int, gaussian: bool) -> list[Scalar]:
        start = row * self.cols
        values = [_require_scalar(self.data[start + col], "entry") for col in range(self.cols)]
        if not gaussian:
            return values
        return [_as_gaussian(value) for value in values]

    def col_scalars(self, col: int, gaussian: bool) -> list[Scalar]:
        values = [_require_scalar(self.data[row * self.cols + col], "entry") for row in range(self.rows)]
        if not gaussian:
            return values
        return [_as_gaussian(value) for value in values]

    def _require_index(self, row: int, col: int) -> None:
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise _index_fail("Index out of bounds", row=row, col=col, rows=self.rows, cols=self.cols)

    def _refuse_matrix(self, role: str) -> None:
        for value in self.data:
            _require_scalar(value, role)

    def _grid(self) -> list[list[Scalar]]:
        gaussian = _uses_gaussian(self.data)
        return [self.row_scalars(row, gaussian) for row in range(self.rows)]

    def __add__(self, other: ExactMatrix) -> ExactMatrix:
        self._refuse_matrix("left")
        other._refuse_matrix("right")
        if (self.rows, self.cols) != (other.rows, other.cols):
            raise _fail("Shape mismatch", left=self.shape(), right=other.shape())
        return _add_entries(self, other)

    def __sub__(self, other: ExactMatrix) -> ExactMatrix:
        self._refuse_matrix("left")
        other._refuse_matrix("right")
        if (self.rows, self.cols) != (other.rows, other.cols):
            raise _fail("Shape mismatch", left=self.shape(), right=other.shape())
        return _subtract_entries(self, other)

    def __mul__(self, other: ExactMatrix) -> ExactMatrix:
        self._refuse_matrix("left")
        other._refuse_matrix("right")
        if self.cols != other.rows:
            raise _fail("Cannot multiply shapes", left=self.shape(), right=other.shape())
        gaussian = _uses_gaussian(self.data) or _uses_gaussian(other.data)
        data: list[Scalar] = []
        for row in range(self.rows):
            left = self.row_scalars(row, gaussian)
            for col in range(other.cols):
                data.append(_dot(left, other.col_scalars(col, gaussian), gaussian))
        return ExactMatrix(self.rows, other.cols, data)

    def mul_vec(self, vector: Sequence[object]) -> list[Scalar]:
        self._refuse_matrix("matrix")
        if self.cols != len(vector):
            raise _fail("Cannot multiply matrix shape by vector length", cols=self.cols, length=len(vector))
        scalars = [_require_scalar(value, "vector") for value in vector]
        gaussian = _uses_gaussian(self.data) or _uses_gaussian(scalars)
        if gaussian:
            scalars = [_as_gaussian(value) for value in scalars]
        return [_dot(self.row_scalars(row, gaussian), scalars, gaussian) for row in range(self.rows)]

    def transpose(self) -> ExactMatrix:
        data = [self.get(row, col) for col in range(self.cols) for row in range(self.rows)]
        return ExactMatrix(self.cols, self.rows, data)

    def adjoint(self) -> ExactMatrix:
        self._refuse_matrix("matrix")
        data = [_conjugate(self.scalar_at(row, col)) for col in range(self.cols) for row in range(self.rows)]
        return ExactMatrix(self.cols, self.rows, data)

    def is_hermitian(self) -> bool:
        self._refuse_matrix("matrix")
        if self.rows != self.cols:
            return False
        return self == self.adjoint()

    def is_unitary(self) -> bool:
        self._refuse_matrix("matrix")
        if self.rows != self.cols:
            return False
        gaussian = _uses_gaussian(self.data)
        return self * self.adjoint() == ExactMatrix.identity(self.rows, is_gaussian=gaussian)

    def rref(self) -> tuple[ExactMatrix, list[int]]:
        self._refuse_matrix("matrix")
        grid = self._grid()
        pivots: list[int] = []
        pivot_row = 0
        for column in range(self.cols):
            pivot_row = _eliminate_column(grid, pivot_row, column, pivots)
            if pivot_row >= self.rows:
                break
        flat = [value for row in grid for value in row]
        return ExactMatrix(self.rows, self.cols, flat), pivots

    def rank(self) -> int:
        _reduced, pivots = self.rref()
        return len(pivots)

    def kernel_basis(self) -> list[list[Scalar]]:
        self._refuse_matrix("matrix")
        reduced, pivots = self.rref()
        pivot_set = set(pivots)
        free_cols = [col for col in range(self.cols) if col not in pivot_set]
        gaussian = _uses_gaussian(self.data)
        zero = _zero(gaussian)
        one = _one(gaussian)
        basis: list[list[Scalar]] = []
        for free_col in free_cols:
            vector = [zero] * self.cols
            vector[free_col] = one
            for pivot_row, pivot_col in enumerate(pivots):
                vector[pivot_col] = _neg(reduced.scalar_at(pivot_row, free_col))
            basis.append(vector)
        return basis

    def determinant(self) -> Scalar:
        self._refuse_matrix("matrix")
        if self.rows != self.cols:
            raise _fail("Determinant requires square matrix", rows=self.rows, cols=self.cols)
        if self.rows == 0:
            return Fraction(1)
        grid = self._grid()
        det = _one(_uses_gaussian(self.data))
        sign = 1
        for index in range(self.rows):
            det, sign, singular = _det_step(grid, index, det, sign)
            if singular:
                return _zero(_uses_gaussian(self.data))
        return _scale(det, sign)

    def inverse(self) -> ExactMatrix:
        self._refuse_matrix("matrix")
        if self.rows != self.cols:
            raise _fail("Inverse requires square matrix", rows=self.rows, cols=self.cols)
        gaussian = _uses_gaussian(self.data)
        augmented = ExactMatrix(self.rows, 2 * self.rows, _augment_identity(self, _zero(gaussian), _one(gaussian)))
        reduced, pivots = augmented.rref()
        size = self.rows
        if len(pivots) < size or pivots[:size] != list(range(size)):
            raise _fail("Matrix is singular", rows=size)
        return ExactMatrix(size, size, _right_block(reduced, size))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExactMatrix):
            return False
        if (self.rows, self.cols) != (other.rows, other.cols):
            return False
        return _entries_equal(self.data, other.data)

    def __repr__(self) -> str:
        return f"ExactMatrix({self.rows}x{self.cols}, data={self.data})"

    def sha256(self) -> str:
        digest = hashlib.sha256()
        digest.update(f"{self.rows}x{self.cols}:".encode("utf-8"))
        for value in self.data:
            _refuse_float(value, "entry")
            _reject_bool(value, "entry", "boolean refused where an exact scalar was required")
            digest.update(_canonical_bytes(value))
            digest.update(b",")
        return digest.hexdigest()


def _neg(value: Scalar) -> Scalar:
    if isinstance(value, GaussianRational):
        return -value
    return -value


def _as_gaussian(value: Scalar) -> GaussianRational:
    if isinstance(value, GaussianRational):
        return value
    return GaussianRational(value, 0)


def _conjugate(value: Scalar) -> Scalar:
    if isinstance(value, GaussianRational):
        return value.conjugate()
    return value


def _combine_entries(left: ExactMatrix, right: ExactMatrix, subtract: bool) -> ExactMatrix:
    gaussian = _uses_gaussian(left.data) or _uses_gaussian(right.data)
    paired: list[Scalar] = []
    for row in range(left.rows):
        for col in range(left.cols):
            paired.append(_combine(left.scalar_at(row, col), right.scalar_at(row, col), subtract))
    if gaussian:
        paired = [_as_gaussian(value) for value in paired]
    return ExactMatrix(left.rows, left.cols, paired)


def _combine(left: Scalar, right: Scalar, subtract: bool) -> Scalar:
    if subtract:
        return _minus(left, right)
    return _plus(left, right)


def _add_entries(left: ExactMatrix, right: ExactMatrix) -> ExactMatrix:
    return _combine_entries(left, right, False)


def _subtract_entries(left: ExactMatrix, right: ExactMatrix) -> ExactMatrix:
    return _combine_entries(left, right, True)


def _entries_equal(left: Sequence[object], right: Sequence[object]) -> bool:
    for left_value, right_value in zip(left, right, strict=True):
        _refuse_float(left_value, "entry")
        _refuse_float(right_value, "entry")
        _reject_bool(left_value, "entry", "boolean refused where an exact scalar was required")
        _reject_bool(right_value, "entry", "boolean refused where an exact scalar was required")
        if left_value != right_value:
            return False
    return True


def _canonical_bytes(value: object) -> bytes:
    if isinstance(value, GaussianRational):
        return value.canonical_bytes()
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}".encode("utf-8")
    return str(value).encode("utf-8")


__all__ = [
    "ExactMatrix",
    "MatrixError",
    "MatrixFailure",
    "MatrixIndexError",
]
