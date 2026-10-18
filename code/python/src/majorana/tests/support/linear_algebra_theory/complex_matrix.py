import math
from typing import Any

from .basic_matrix import BasicMatrix, MatrixError


class ComplexMatrixError(Exception):
    pass


class NonFiniteEntry(ComplexMatrixError):
    def __init__(self, index, value):
        super().__init__(f"non-finite entry at index {index}: {value}")


class NonFiniteScalar(ComplexMatrixError):
    def __init__(self, value):
        super().__init__(f"non-finite scalar: {value}")


C64 = complex
NComplex = complex


class ComplexMatrix:
    def __init__(self, matrix: BasicMatrix):
        self.matrix = matrix

    @classmethod
    def from_row_major(cls, rows: int, cols: int, data: list):
        for index, value in enumerate(data):
            if not isinstance(value, complex):
                value = complex(value)
            if not (math.isfinite(value.real) and math.isfinite(value.imag)):
                raise NonFiniteEntry(index, value)
        try:
            bm = BasicMatrix.from_row_major(rows, cols, data)
            return cls(bm)
        except MatrixError as e:
            raise ComplexMatrixError(str(e))

    @classmethod
    def zero(cls, rows: int, cols: int):
        try:
            bm = BasicMatrix.zero(rows, cols, zero_val=0.0 + 0.0j)
            return cls(bm)
        except MatrixError as e:
            raise ComplexMatrixError(str(e))

    @classmethod
    def identity(cls, dim: int):
        try:
            data = [
                (1.0 + 0.0j) if r == c else (0.0 + 0.0j)
                for r in range(dim)
                for c in range(dim)
            ]
            bm = BasicMatrix.from_row_major(dim, dim, data)
            return cls(bm)
        except MatrixError as e:
            raise ComplexMatrixError(str(e))

    @classmethod
    def try_from_fn(cls, rows: int, cols: int, f):
        data = []
        for r in range(rows):
            for c in range(cols):
                val = f(r, c)
                if not isinstance(val, complex):
                    val = complex(val)
                data.append(val)
        return cls.from_row_major(rows, cols, data)

    @classmethod
    def from_nalgebra(cls, matrix):
        if isinstance(matrix, BasicMatrix):
            bm = matrix
        elif hasattr(matrix, "tolist"):  
            arr = matrix.tolist()
            rows = len(arr)
            cols = len(arr[0]) if rows > 0 else 0
            flat = [x for row in arr for x in row]
            bm = BasicMatrix.from_row_major(rows, cols, flat)
        else:  
            rows = len(matrix)
            cols = len(matrix[0]) if rows > 0 else 0
            flat = [x for row in matrix for x in row]
            bm = BasicMatrix.from_row_major(rows, cols, flat)

        for index, value in enumerate(bm.as_slice()):
            if not (math.isfinite(value.real) and math.isfinite(value.imag)):
                raise NonFiniteEntry(index, value)
        return cls(bm)

    def to_nalgebra(self):
        rows = self.rows()
        cols = self.cols()
        return [[self.get(r, c) for c in range(cols)] for r in range(rows)]

    def rows(self) -> Any:
        return self.matrix.rows

    def cols(self) -> Any:
        return self.matrix.cols

    def shape(self):
        return self.matrix.shape()

    def as_slice(self):
        return self.matrix.as_slice()

    def get(self, row: int, col: int) -> complex:
        try:
            return self.matrix.get(row, col)
        except MatrixError as e:
            raise ComplexMatrixError(str(e))

    def set(self, row: int, col: int, value: complex):
        if not isinstance(value, complex):
            value = complex(value)
        if not (math.isfinite(value.real) and math.isfinite(value.imag)):
            raise NonFiniteEntry(row * self.cols() + col, value)
        try:
            self.matrix.set(row, col, value)
        except MatrixError as e:
            raise ComplexMatrixError(str(e))

    def trace(self) -> complex:
        n = min(self.rows(), self.cols())
        trace = 0.0 + 0.0j
        for i in range(n):
            trace += self.get(i, i)
        return trace

    def adjoint(self):
        data = []
        for r in range(self.cols()):
            for c in range(self.rows()):
                data.append(self.get(c, r).conjugate())
        return self.from_row_major(self.cols(), self.rows(), data)

    def add(self, other: "ComplexMatrix"):
        try:
            return ComplexMatrix(self.matrix.add(other.matrix))
        except MatrixError as e:
            raise ComplexMatrixError(str(e))

    def sub(self, other: "ComplexMatrix"):
        try:
            return ComplexMatrix(self.matrix.sub(other.matrix))
        except MatrixError as e:
            raise ComplexMatrixError(str(e))

    def mul(self, other: "ComplexMatrix"):
        try:
            return ComplexMatrix(self.matrix.mul(other.matrix))
        except MatrixError as e:
            raise ComplexMatrixError(str(e))

    def scale_real(self, scalar: float):
        if not math.isfinite(scalar):
            raise NonFiniteScalar(scalar)
        data = [x * scalar for x in self.as_slice()]
        return self.from_row_major(self.rows(), self.cols(), data)

    def frobenius_norm(self) -> float:
        return math.sqrt(sum(abs(x) ** 2 for x in self.as_slice()))

    def is_finite(self) -> bool:
        return all(
            math.isfinite(x.real) and math.isfinite(x.imag) for x in self.as_slice()
        )

    def to_real_block(self):
        import numpy as np

        n = self.rows()
        m = self.cols()
        block = np.zeros((2 * n, 2 * m), dtype=float)
        for i in range(n):
            for j in range(m):
                z = self.get(i, j)
                block[i, j] = z.real
                block[i, j + m] = -z.imag
                block[i + n, j] = z.imag
                block[i + n, j + m] = z.real
        return block

