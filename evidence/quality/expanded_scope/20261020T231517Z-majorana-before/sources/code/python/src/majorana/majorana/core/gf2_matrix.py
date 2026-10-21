"""GF(2) matrix carrier with arithmetic delegated to native linear algebra.

contract_id: urn:omega:math:finite_field:v1.0.0
contract_id: urn:omega:math:matrix:v1.0.0
"""

from __future__ import annotations

from typing import Any, Sequence

from omega_engine_operating_system.adapters.rust_host.majorana_math import call_native

from .basic_matrix import BasicMatrix
from .gf2_schema import mod2


class GF2Matrix:
    """Exact public GF(2) carrier; native operations retain empty matrix shapes."""

    def __init__(self, data: Sequence[Sequence[int]], cols: int | None = None):
        if cols is not None and (isinstance(cols, bool) or not isinstance(cols, int) or cols < 0):
            raise ValueError("matrix columns must be a nonnegative integer")
        self.data = [[mod2(x) for x in row] for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0]) if self.rows else (0 if cols is None else cols)
        if isinstance(self.cols, bool) or not isinstance(self.cols, int) or self.cols < 0:
            raise ValueError("matrix columns must be a nonnegative integer")
        if cols is not None and self.rows and cols != self.cols:
            raise ValueError("explicit columns do not match matrix data")
        if any(len(row) != self.cols for row in self.data):
            raise ValueError("All matrix rows must have equal length")

    @classmethod
    def zeros(cls, rows: int, cols: int) -> GF2Matrix:
        if any(isinstance(d, bool) or not isinstance(d, int) or d < 0 for d in (rows, cols)):
            raise ValueError("Matrix dimensions must be nonnegative integers")
        return cls([[0] * cols for _ in range(rows)], cols=cols)

    @classmethod
    def from_basic_matrix(cls, basic: BasicMatrix) -> GF2Matrix:
        return cls(basic.to_nested(), cols=basic.shape()[1])

    def to_basic_matrix(self) -> BasicMatrix:
        return BasicMatrix.from_row_major(
            self.rows, self.cols, [x for row in self.data for x in row]
        )

    def to_list(self) -> list[list[int]]:
        return [list(row) for row in self.data]

    def shape(self) -> tuple[int, int]:
        return self.rows, self.cols

    def __getitem__(self, index: int) -> list[int]:
        return self.data[index]

    def _wire(self) -> dict[str, Any]:
        return {
            "rows": self.rows,
            "cols": self.cols,
            "data": [[mod2(x) for x in row] for row in self.data],
        }

    @classmethod
    def _from_wire(cls, wire: dict[str, Any]) -> GF2Matrix:
        matrix = cls(wire["data"], cols=wire["cols"])
        if matrix.rows != wire["rows"]:
            raise ValueError("native GF(2) response has inconsistent row count")
        return matrix

    def transpose(self) -> GF2Matrix:
        result = call_native("math_gf2_matrix", {"operation": "transpose", "matrix": self._wire()})
        return self._from_wire(result["matrix"])

    def mat_vec_mul(self, vec: Sequence[int]) -> list[int]:
        if len(vec) != self.cols:
            raise ValueError(f"Vector length {len(vec)} does not match matrix columns {self.cols}")
        vector_matrix = {"rows": len(vec), "cols": 1, "data": [[mod2(x)] for x in vec]}
        result = call_native(
            "math_gf2_matrix",
            {"operation": "multiply", "matrix": self._wire(), "other": vector_matrix},
        )["matrix"]
        return [row[0] for row in self._from_wire(result).data]

    def rref(self) -> tuple[GF2Matrix, list[int]]:
        result = call_native("math_gf2_matrix", {"operation": "rref", "matrix": self._wire()})
        return self._from_wire(result["matrix"]), result["pivots"]

    def kernel_basis(self) -> list[list[int]]:
        return call_native("math_gf2_matrix", {"operation": "kernel", "matrix": self._wire()})[
            "basis"
        ]

    def solve(self, b: Sequence[int]) -> list[int] | None:
        if len(b) != self.rows:
            raise ValueError(f"Vector length {len(b)} does not match matrix rows {self.rows}")
        return call_native(
            "math_gf2_matrix",
            {"operation": "solve", "matrix": self._wire(), "vector": [mod2(x) for x in b]},
        )["solution"]

    def __repr__(self) -> str:
        return f"GF2Matrix({self.data})"
