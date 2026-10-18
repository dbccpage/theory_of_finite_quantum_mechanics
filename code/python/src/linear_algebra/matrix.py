"""Exact matrix arithmetic over exact fields (Q, Q(i))."""
from fractions import Fraction
import hashlib
from typing import List, Sequence, Tuple, Union
from .scalars import GaussianRational, Q, q

class MatrixError(Exception):
    pass

class ExactMatrix:
    __slots__ = ("rows", "cols", "data")

    def __init__(self, rows: int, cols: int, data: Sequence[object]):
        if len(data) != rows * cols:
            raise ValueError(f"Data length {len(data)} does not match dimensions {rows}x{cols}")
        self.rows = rows
        self.cols = cols
        self.data = list(data)

    @classmethod
    def zeros(cls, rows: int, cols: int, is_gaussian: bool = False) -> "ExactMatrix":
        zero = GaussianRational(0, 0) if is_gaussian else Fraction(0)
        return cls(rows, cols, [zero] * (rows * cols))

    @classmethod
    def identity(cls, n: int, is_gaussian: bool = False) -> "ExactMatrix":
        zero = GaussianRational(0, 0) if is_gaussian else Fraction(0)
        one = GaussianRational(1, 0) if is_gaussian else Fraction(1)
        data = []
        for r in range(n):
            for c in range(n):
                data.append(one if r == c else zero)
        return cls(n, n, data)

    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[object]]) -> "ExactMatrix":
        if not rows:
            return cls(0, 0, [])
        num_rows = len(rows)
        num_cols = len(rows[0])
        data = []
        for r in rows:
            if len(r) != num_cols:
                raise ValueError("Jagged rows are not allowed")
            data.extend(r)
        return cls(num_rows, num_cols, data)

    def shape(self) -> Tuple[int, int]:
        return (self.rows, self.cols)

    def get(self, r: int, c: int) -> object:
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            raise IndexError(f"Index ({r}, {c}) out of bounds for shape {self.shape()}")
        return self.data[r * self.cols + c]

    def set(self, r: int, c: int, val: object) -> None:
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            raise IndexError(f"Index ({r}, {c}) out of bounds for shape {self.shape()}")
        self.data[r * self.cols + c] = val

    def row(self, r: int) -> List[object]:
        return self.data[r * self.cols : (r + 1) * self.cols]

    def col(self, c: int) -> List[object]:
        return [self.data[r * self.cols + c] for r in range(self.rows)]

    def __add__(self, other: "ExactMatrix") -> "ExactMatrix":
        if (self.rows, self.cols) != (other.rows, other.cols):
            raise ValueError(f"Shape mismatch: {self.shape()} vs {other.shape()}")
        return ExactMatrix(self.rows, self.cols, [a + b for a, b in zip(self.data, other.data)])

    def __sub__(self, other: "ExactMatrix") -> "ExactMatrix":
        if (self.rows, self.cols) != (other.rows, other.cols):
            raise ValueError(f"Shape mismatch: {self.shape()} vs {other.shape()}")
        return ExactMatrix(self.rows, self.cols, [a - b for a, b in zip(self.data, other.data)])

    def __mul__(self, other: "ExactMatrix") -> "ExactMatrix":
        if self.cols != other.rows:
            raise ValueError(f"Cannot multiply shapes {self.shape()} and {other.shape()}")
        m, k, n = self.rows, self.cols, other.cols
        data = []
        is_gaussian = any(isinstance(x, GaussianRational) for x in self.data + other.data)
        zero = GaussianRational(0, 0) if is_gaussian else Fraction(0)
        for r in range(m):
            for c in range(n):
                s = zero
                for i in range(k):
                    s += self.data[r * k + i] * other.data[i * n + c]
                data.append(s)
        return ExactMatrix(m, n, data)

    def mul_vec(self, v: Sequence[object]) -> List[object]:
        if self.cols != len(v):
            raise ValueError(f"Cannot multiply matrix shape {self.shape()} by vector length {len(v)}")
        out = []
        is_gaussian = any(isinstance(x, GaussianRational) for x in self.data) or any(isinstance(x, GaussianRational) for x in v)
        zero = GaussianRational(0, 0) if is_gaussian else Fraction(0)
        for r in range(self.rows):
            s = zero
            for c in range(self.cols):
                s += self.data[r * self.cols + c] * v[c]
            out.append(s)
        return out

    def transpose(self) -> "ExactMatrix":
        data = []
        for c in range(self.cols):
            for r in range(self.rows):
                data.append(self.data[r * self.cols + c])
        return ExactMatrix(self.cols, self.rows, data)

    def adjoint(self) -> "ExactMatrix":
        data = []
        for c in range(self.cols):
            for r in range(self.rows):
                val = self.data[r * self.cols + c]
                if isinstance(val, GaussianRational):
                    data.append(val.conjugate())
                else:
                    data.append(val)
        return ExactMatrix(self.cols, self.rows, data)

    def is_hermitian(self) -> bool:
        if self.rows != self.cols:
            return False
        return self == self.adjoint()

    def is_unitary(self) -> bool:
        if self.rows != self.cols:
            return False
        prod = self * self.adjoint()
        is_g = any(isinstance(x, GaussianRational) for x in self.data)
        return prod == ExactMatrix.identity(self.rows, is_gaussian=is_g)

    def rref(self) -> Tuple["ExactMatrix", List[int]]:
        grid = [list(self.row(r)) for r in range(self.rows)]
        pivots = []
        pivot_row = 0
        for c in range(self.cols):
            if pivot_row >= self.rows:
                break
            found = None
            for r in range(pivot_row, self.rows):
                val = grid[r][c]
                is_z = val.is_zero() if hasattr(val, "is_zero") else (val == 0)
                if not is_z:
                    found = r
                    break
            if found is None:
                continue
            if found != pivot_row:
                grid[pivot_row], grid[found] = grid[found], grid[pivot_row]

            p_val = grid[pivot_row][c]
            for col_idx in range(self.cols):
                grid[pivot_row][col_idx] = grid[pivot_row][col_idx] / p_val

            for r in range(self.rows):
                if r != pivot_row:
                    factor = grid[r][c]
                    is_z = factor.is_zero() if hasattr(factor, "is_zero") else (factor == 0)
                    if not is_z:
                        for col_idx in range(self.cols):
                            grid[r][col_idx] -= factor * grid[pivot_row][col_idx]
            pivots.append(c)
            pivot_row += 1

        flat_data = [val for row in grid for val in row]
        return ExactMatrix(self.rows, self.cols, flat_data), pivots

    def rank(self) -> int:
        _, pivots = self.rref()
        return len(pivots)

    def kernel_basis(self) -> List[List[object]]:
        rref, pivots = self.rref()
        pivot_set = set(pivots)
        free_cols = [c for c in range(self.cols) if c not in pivot_set]
        is_g = any(isinstance(x, GaussianRational) for x in self.data)
        zero = GaussianRational(0, 0) if is_g else Fraction(0)
        one = GaussianRational(1, 0) if is_g else Fraction(1)

        basis = []
        for free_col in free_cols:
            vec = [zero] * self.cols
            vec[free_col] = one
            for p_row, p_col in enumerate(pivots):
                vec[p_col] = -rref.get(p_row, free_col)
            basis.append(vec)
        return basis

    def determinant(self) -> object:
        if self.rows != self.cols:
            raise ValueError(f"Determinant requires square matrix, got {self.shape()}")
        n = self.rows
        if n == 0:
            return Fraction(1)
        grid = [list(self.row(r)) for r in range(n)]
        sign = 1
        is_g = any(isinstance(x, GaussianRational) for x in self.data)
        det = GaussianRational(1, 0) if is_g else Fraction(1)

        for i in range(n):
            pivot = None
            for r in range(i, n):
                val = grid[r][i]
                is_z = val.is_zero() if hasattr(val, "is_zero") else (val == 0)
                if not is_z:
                    pivot = r
                    break
            if pivot is None:
                return GaussianRational(0, 0) if is_g else Fraction(0)

            if pivot != i:
                grid[i], grid[pivot] = grid[pivot], grid[i]
                sign = -sign

            p_val = grid[i][i]
            det *= p_val
            for r in range(i + 1, n):
                factor = grid[r][i]
                is_z = factor.is_zero() if hasattr(factor, "is_zero") else (factor == 0)
                if not is_z:
                    scale = factor / p_val
                    for c in range(i, n):
                        grid[r][c] -= scale * grid[i][c]

        return det * sign

    def inverse(self) -> "ExactMatrix":
        if self.rows != self.cols:
            raise ValueError(f"Inverse requires square matrix, got {self.shape()}")
        n = self.rows
        is_g = any(isinstance(x, GaussianRational) for x in self.data)
        zero = GaussianRational(0, 0) if is_g else Fraction(0)
        one = GaussianRational(1, 0) if is_g else Fraction(1)

        aug_data = []
        for r in range(n):
            for c in range(n):
                aug_data.append(self.get(r, c))
            for c in range(n):
                aug_data.append(one if r == c else zero)

        aug = ExactMatrix(n, 2 * n, aug_data)
        rref, pivots = aug.rref()
        if len(pivots) < n or pivots[:n] != list(range(n)):
            raise ValueError("Matrix is singular")

        inv_data = []
        for r in range(n):
            for c in range(n):
                inv_data.append(rref.get(r, n + c))
        return ExactMatrix(n, n, inv_data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExactMatrix):
            return False
        if (self.rows, self.cols) != (other.rows, other.cols):
            return False
        return all(a == b for a, b in zip(self.data, other.data))

    def __repr__(self) -> str:
        return f"ExactMatrix({self.rows}x{self.cols}, data={self.data})"

    def sha256(self) -> str:
        h = hashlib.sha256()
        h.update(f"{self.rows}x{self.cols}:".encode("utf-8"))
        for x in self.data:
            if hasattr(x, "canonical_bytes"):
                h.update(x.canonical_bytes())
            elif isinstance(x, Fraction):
                h.update(f"{x.numerator}/{x.denominator}".encode("utf-8"))
            else:
                h.update(str(x).encode("utf-8"))
            h.update(b",")
        return h.hexdigest()
