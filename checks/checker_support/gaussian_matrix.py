"""Owned bounded Gaussian matrices for finite cycles. AuthorityEffect: None.

Dimensions 1..18; owned Gaussian components and every completed Gaussian
operation have <=4096-bit rational components. Matrix queries use Outcome.
Internal value operations raise typed Violation for composition by callers.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import cast
import sympy as sp

from .boundary import Violation, evaluate
from .domains import integer, sequence
from .gaussian_expression import _decode, _encode
from .gaussian_rational import GaussianRational as G
from .outcome import Outcome

Rows = tuple[tuple[G, ...], ...]


def _dot(left: tuple[G, ...], right: tuple[G, ...]) -> G:
    total = G(0)
    for a, b in zip(left, right):
        total = total+a.mul(b)
    return total


def _eliminate(row: list[G], pivot: list[G], column: int) -> list[G]:
    factor = row[column].div(pivot[column])
    return row[:column]+[value-factor.mul(entry) for value, entry in zip(row[column:], pivot[column:])]


@dataclass(frozen=True, slots=True, init=False)
class GaussianMatrix:
    """Owns rectangular immutable rows; full shape preflight precedes scalar admission."""
    rows: Rows

    def __init__(self, value: object) -> None:
        outer = sequence(value, "Gaussian matrix", maximum=18)
        if not outer:
            raise Violation("input", "Gaussian matrix requires at least one row")
        first = sequence(outer[0], "Gaussian row", maximum=18)
        if not first:
            raise Violation("input", "Gaussian matrix requires at least one column")
        layout = tuple(sequence(row, "Gaussian row", len(first), 18) for row in outer)
        owned = tuple(tuple(_decode(entry) for entry in row) for row in layout)
        object.__setattr__(self, "rows", owned)

    @classmethod
    def eye(cls, dimension: object) -> GaussianMatrix:
        size = integer(dimension, "Gaussian matrix dimension", 1, 18)
        return cls(tuple(tuple(int(i == j) for j in range(size)) for i in range(size)))

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.rows), len(self.rows[0])

    def require_shape(self, rows: int, columns: int) -> GaussianMatrix:
        expected = (integer(rows, "Gaussian row count", 1, 18),
                    integer(columns, "Gaussian column count", 1, 18))
        if self.shape != expected:
            raise Violation("input", "Gaussian matrix has the wrong shape")
        return self

    def _operand(self, value: object) -> GaussianMatrix:
        if type(value) is not GaussianMatrix:
            raise Violation("input", "Gaussian operation requires an owned GaussianMatrix")
        return value

    def add(self, other: object) -> GaussianMatrix:
        rhs = self._operand(other).require_shape(*self.shape)
        return GaussianMatrix(tuple(tuple(a+b for a, b in zip(left, right))
                                    for left, right in zip(self.rows, rhs.rows)))

    def neg(self) -> GaussianMatrix:
        return self.scale(-1)

    def scale(self, scalar: object) -> GaussianMatrix:
        factor = _decode(scalar)
        return GaussianMatrix(tuple(tuple(entry.mul(factor) for entry in row) for row in self.rows))

    def adjoint(self) -> GaussianMatrix:
        return GaussianMatrix(tuple(tuple(entry.conj() for entry in column) for column in zip(*self.rows)))

    def mul(self, other: object) -> GaussianMatrix:
        rhs = self._operand(other)
        if self.shape[1] != rhs.shape[0]:
            raise Violation("input", "Gaussian multiplication dimensions disagree")
        columns = tuple(zip(*rhs.rows))
        return GaussianMatrix(tuple(tuple(_dot(row, column) for column in columns) for row in self.rows))

    def determinant(self) -> G:
        self.require_shape(self.shape[0], self.shape[0])
        rows = [list(row) for row in self.rows]
        result = G(1)
        size = len(rows)
        for column in range(size):
            pivot = next((i for i in range(column, size) if rows[i][column] != G(0)), None)
            if pivot is None:
                return G(0)
            if pivot != column:
                rows[column], rows[pivot] = rows[pivot], rows[column]
                result = G(-1).mul(result)
            result = result.mul(rows[column][column])
            rows[column+1:] = [_eliminate(row, rows[column], column) for row in rows[column+1:]]
        return result

    def determinant_result(self) -> Outcome[G]:
        return evaluate(self.determinant)

    def to_sympy(self) -> sp.ImmutableMatrix:
        return sp.ImmutableMatrix(tuple(tuple(_encode(entry) for entry in row) for row in self.rows))

    @classmethod
    def from_sympy(cls, value: object) -> GaussianMatrix:
        if type(value) is not sp.ImmutableDenseMatrix:
            raise Violation("input", "Gaussian import requires an immutable dense matrix")
        matrix = cast(sp.ImmutableMatrix, value)
        integer(matrix.rows, "Gaussian import rows", 1, 18)
        integer(matrix.cols, "Gaussian import columns", 1, 18)
        return cls(tuple(tuple(matrix[i, j] for j in range(matrix.cols)) for i in range(matrix.rows)))
