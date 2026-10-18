from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence, TypeAlias

Scalar: TypeAlias = Fraction
Vector: TypeAlias = tuple[Scalar, ...]
Matrix: TypeAlias = tuple[Vector, ...]
COEFFICIENT_DOMAIN = "Q"


def _scalar(value: int | str | Fraction) -> Scalar:
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError(
            "use integers, strings, or Fraction; floating point is forbidden"
        )
    if not isinstance(value, (int, str, Fraction)):
        raise TypeError(f"unsupported exact scalar: {type(value).__name__}")
    return Fraction(value)


def coerce_vector(
    values: Iterable[int | str | Fraction], expected: int, label: str
) -> Vector:
    result = tuple(_scalar(value) for value in values)
    if len(result) != expected:
        raise ValueError(f"{label} has length {len(result)}; expected {expected}")
    return result


def _matrix(rows, row_count: int, column_count: int, label: str) -> Matrix:
    result = tuple(
        coerce_vector(row, column_count, f"{label}[{index}]")
        for index, row in enumerate(rows)
    )
    if len(result) != row_count:
        raise ValueError(f"{label} has {len(result)} rows; expected {row_count}")
    return result


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum(
            (coefficient * value for coefficient, value in zip(row, vector)),
            Fraction(0),
        )
        for row in matrix
    )


def _matmul(left: Matrix, right: Matrix, inner_dimension: int) -> Matrix:
    if not left:
        return ()
    right_columns = len(right[0]) if right else 0
    return tuple(
        tuple(
            sum(
                (left[row][k] * right[k][column] for k in range(inner_dimension)),
                Fraction(0),
            )
            for column in range(right_columns)
        )
        for row in range(len(left))
    )


@dataclass(frozen=True)
class FiniteCochainComplex:

    c0_dimension: int
    c1_dimension: int
    c2_dimension: int
    d0: Matrix
    d1: Matrix

    @classmethod
    def from_rows(
        cls,
        dimensions: tuple[int, int, int],
        d0: Sequence[Sequence[int | str | Fraction]],
        d1: Sequence[Sequence[int | str | Fraction]],
    ) -> "FiniteCochainComplex":
        if len(dimensions) != 3 or any(
            isinstance(dimension, bool)
            or not isinstance(dimension, int)
            or dimension < 0
            for dimension in dimensions
        ):
            raise ValueError("dimensions must be three nonnegative integers")
        c0_dimension, c1_dimension, c2_dimension = dimensions
        return cls(
            c0_dimension=c0_dimension,
            c1_dimension=c1_dimension,
            c2_dimension=c2_dimension,
            d0=_matrix(d0, c1_dimension, c0_dimension, "d0"),
            d1=_matrix(d1, c2_dimension, c1_dimension, "d1"),
        )

    def complex_defect(self) -> Matrix:
        if self.c2_dimension == 0:
            return ()
        if self.c0_dimension == 0:
            return tuple(() for _ in range(self.c2_dimension))
        if self.c1_dimension == 0:
            return tuple(
                tuple(Fraction(0) for _ in range(self.c0_dimension))
                for _ in range(self.c2_dimension)
            )
        return _matmul(self.d1, self.d0, self.c1_dimension)

    def primitive_difference(self, alpha: Sequence[int | str | Fraction]) -> Vector:
        return _matvec(self.d0, coerce_vector(alpha, self.c0_dimension, "alpha"))

    def closure_defect(self, beta: Sequence[int | str | Fraction]) -> Vector:
        return _matvec(self.d1, coerce_vector(beta, self.c1_dimension, "beta"))


__all__ = [
    "COEFFICIENT_DOMAIN",
    "FiniteCochainComplex",
    "Matrix",
    "Scalar",
    "Vector",
    "coerce_vector",
]


