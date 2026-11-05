"""Owned bounded rational matrices for independent finite-model verification.

AuthorityEffect: None. Each dimension is 1..64; every stored value and each
dot-product intermediate has <=4096-bit numerator/denominator. Expected input
and resource refusals use Violation and are converted by the Railway boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .boundary import Violation
from .domains import integer, integer_matrix, rational, sequence

Rows = tuple[tuple[Fraction, ...], ...]
Flat2 = tuple[Fraction, Fraction, Fraction, Fraction]


def _dot(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> Fraction:
    """Internal equal-length admitted rows; bound every multiplication and sum."""
    total = Fraction(0)
    for a, b in zip(left, right):
        total = rational(total + rational(a * b, "matrix product"), "matrix dot sum")
    return total


@dataclass(frozen=True, slots=True, init=False)
class RationalMatrix:
    """Rectangular exact value object owning all rows, independent of callers."""

    rows: Rows

    def __init__(self, value: object) -> None:
        outer = sequence(value, "matrix", maximum=64)
        if not outer:
            raise Violation("input", "matrix must have at least one row")
        first = sequence(outer[0], "matrix row", maximum=64)
        if not first:
            raise Violation("input", "matrix must have at least one column")
        rows = tuple(tuple(rational(x, "matrix entry") for x in sequence(row, "matrix row", len(first), 64))
                     for row in outer)
        object.__setattr__(self, "rows", rows)

    @classmethod
    def from_integers(cls, value: object) -> RationalMatrix:
        return cls(integer_matrix(value))

    @classmethod
    def from_flat2(cls, value: object) -> RationalMatrix:
        a, b, c, d = sequence(value, "flat 2x2 matrix", 4)
        return cls(((a, b), (c, d)))

    @classmethod
    def eye(cls, dimension: object) -> RationalMatrix:
        size = integer(dimension, "matrix dimension", 1, 64)
        return cls(tuple(tuple(int(i == j) for j in range(size)) for i in range(size)))

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.rows), len(self.rows[0])

    def require_shape(self, rows: object, columns: object) -> RationalMatrix:
        expected = (integer(rows, "row count", 1, 64), integer(columns, "column count", 1, 64))
        if self.shape != expected:
            raise Violation("input", "matrix has the wrong shape")
        return self

    def _operand(self, other: object) -> RationalMatrix:
        if type(other) is not RationalMatrix:
            raise Violation("input", "matrix operation requires a RationalMatrix")
        return other

    def integer_rows(self) -> tuple[tuple[int, ...], ...]:
        if any(x.denominator != 1 for row in self.rows for x in row):
            raise Violation("input", "integer export requires integral matrix entries")
        return tuple(tuple(x.numerator for x in row) for row in self.rows)

    def flat2(self) -> Flat2:
        self.require_shape(2, 2)
        return self.rows[0][0], self.rows[0][1], self.rows[1][0], self.rows[1][1]

    def add(self, other: RationalMatrix) -> RationalMatrix:
        rhs = self._operand(other).require_shape(*self.shape)
        return RationalMatrix(tuple(tuple(a + b for a, b in zip(left, right))
                                    for left, right in zip(self.rows, rhs.rows)))

    def neg(self) -> RationalMatrix:
        return RationalMatrix(tuple(tuple(-x for x in row) for row in self.rows))

    def transpose(self) -> RationalMatrix:
        return RationalMatrix(tuple(zip(*self.rows)))

    def mul(self, other: RationalMatrix) -> RationalMatrix:
        rhs = self._operand(other)
        if self.shape[1] != rhs.shape[0]:
            raise Violation("input", "matrix multiplication dimensions disagree")
        columns = tuple(zip(*rhs.rows))
        return RationalMatrix(tuple(tuple(_dot(row, column) for column in columns) for row in self.rows))

    def kron(self, other: RationalMatrix) -> RationalMatrix:
        rhs = self._operand(other)
        integer(self.shape[0] * rhs.shape[0], "tensor row count", 1, 64)
        integer(self.shape[1] * rhs.shape[1], "tensor column count", 1, 64)
        return RationalMatrix(tuple(tuple(a * b for a in left for b in right)
                                    for left in self.rows for right in rhs.rows))

    def det2(self) -> Fraction:
        a, b, c, d = self.flat2()
        return rational(rational(a * d) - rational(b * c), "determinant")

    def inverse2(self) -> RationalMatrix:
        a, b, c, d = self.flat2()
        determinant = self.det2()
        if determinant == 0:
            raise Violation("input", "singular matrix has no inverse")
        return RationalMatrix(((d / determinant, -b / determinant), (-c / determinant, a / determinant)))
