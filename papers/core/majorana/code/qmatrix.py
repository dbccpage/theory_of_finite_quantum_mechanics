"""Exact rational matrix carrier backed by the native linear algebra crate.

Fractions preserve the public Python representation; all matrix arithmetic and
elimination run through the canonical Rust host. Native refusals propagate.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Sequence

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    call_native,
    decode_rational,
)

from .errors import DimensionMismatch


def _rational(value: Any) -> Fraction:
    if isinstance(value, (bool, float)):
        raise TypeError("floating point / bool forbidden; use exact rational values")
    return Fraction(value)


class QMatrix:
    __slots__ = ("rows", "cols", "data")

    def __init__(self, rows: int, cols: int, data: list[list[Fraction]]):
        if any(isinstance(d, bool) or not isinstance(d, int) or d < 0 for d in (rows, cols)):
            raise ValueError("matrix dimensions must be nonnegative integers")
        if len(data) != rows or any(len(row) != cols for row in data):
            raise DimensionMismatch(f"data does not match matrix shape {rows}x{cols}")
        self.rows = rows
        self.cols = cols
        self.data = [[_rational(value) for value in row] for row in data]

    @classmethod
    def zero(cls, rows: int, cols: int) -> QMatrix:
        return cls(rows, cols, [[Fraction(0)] * cols for _ in range(rows)])

    @classmethod
    def identity(cls, n: int) -> QMatrix:
        return cls(n, n, [[Fraction(i == j) for j in range(n)] for i in range(n)])

    @classmethod
    def from_row_major(cls, rows: int, cols: int, flat: Sequence) -> QMatrix:
        if len(flat) != rows * cols:
            raise DimensionMismatch(
                f"expected {rows * cols} entries for {rows}x{cols}, got {len(flat)}"
            )
        values = [_rational(x) for x in flat]
        return cls(rows, cols, [values[r * cols : (r + 1) * cols] for r in range(rows)])

    @property
    def shape(self) -> tuple[int, int]:
        return self.rows, self.cols

    def as_flat(self) -> list[Fraction]:
        return [x for row in self.data for x in row]

    def _wire(self) -> dict[str, Any]:
        return {
            "rows": self.rows,
            "cols": self.cols,
            "data": [[str(_rational(x)) for x in row] for row in self.data],
        }

    @classmethod
    def _from_wire(cls, wire: dict[str, Any]) -> QMatrix:
        return cls(
            wire["rows"],
            wire["cols"],
            [[decode_rational(value) for value in row] for row in wire["data"]],
        )

    def matmul(self, other: QMatrix) -> QMatrix:
        if self.cols != other.rows:
            raise DimensionMismatch(f"cannot multiply {self.shape} by {other.shape}")
        result = call_native(
            "math_rational_matrix",
            {"operation": "multiply", "matrix": self._wire(), "other": other._wire()},
        )
        return self._from_wire(result["matrix"])

    def transpose(self) -> QMatrix:
        result = call_native(
            "math_rational_matrix", {"operation": "transpose", "matrix": self._wire()}
        )
        return self._from_wire(result["matrix"])

    def is_zero(self) -> bool:
        return all(x == 0 for row in self.data for x in row)

    def rank(self) -> int:
        return call_native("math_rational_matrix", {"operation": "rank", "matrix": self._wire()})[
            "rank"
        ]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, QMatrix) and self.shape == other.shape and self.data == other.data
