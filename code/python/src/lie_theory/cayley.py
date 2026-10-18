"""Lie theory and exact Cayley transforms over complex rational fields.
Implements unitary Cayley chart: U = (I - i tau H)(I + i tau H)^-1
and its inverse generator map: H = i(U - I)(U + I)^-1.
"""

from __future__ import annotations
from fractions import Fraction
from dataclasses import dataclass
from typing import List, Sequence, Tuple, Optional


@dataclass(frozen=True)
class ComplexRational:
    """Exact complex rational number a + b*i where a, b in Fraction."""
    re: Fraction
    im: Fraction

    def __init__(self, re: Fraction | int | Tuple[int, int] = 0, im: Fraction | int | Tuple[int, int] = 0) -> None:
        object.__setattr__(self, 're', Fraction(re[0], re[1]) if isinstance(re, tuple) else Fraction(re))
        object.__setattr__(self, 'im', Fraction(im[0], im[1]) if isinstance(im, tuple) else Fraction(im))

    def __add__(self, other: ComplexRational) -> ComplexRational:
        return ComplexRational(self.re + other.re, self.im + other.im)

    def __sub__(self, other: ComplexRational) -> ComplexRational:
        return ComplexRational(self.re - other.re, self.im - other.im)

    def __mul__(self, other: ComplexRational) -> ComplexRational:
        return ComplexRational(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re
        )

    def __truediv__(self, other: ComplexRational) -> ComplexRational:
        denom = other.re * other.re + other.im * other.im
        if denom == 0:
            raise ZeroDivisionError("Division by zero in ComplexRational")
        return ComplexRational(
            (self.re * other.re + self.im * other.im) / denom,
            (self.im * other.re - self.re * other.im) / denom
        )

    def conjugate(self) -> ComplexRational:
        return ComplexRational(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    @classmethod
    def zero(cls) -> ComplexRational:
        return cls(0, 0)

    @classmethod
    def one(cls) -> ComplexRational:
        return cls(1, 0)

    @classmethod
    def i(cls) -> ComplexRational:
        return cls(0, 1)


class ComplexMatrix:
    """Exact matrix with ComplexRational entries."""

    def __init__(self, rows: int, cols: int, data: Sequence[Sequence[ComplexRational]]) -> None:
        self.rows = rows
        self.cols = cols
        self._data = [list(row) for row in data]

    @classmethod
    def identity(cls, dim: int) -> ComplexMatrix:
        data = [[ComplexRational.one() if i == j else ComplexRational.zero() for j in range(dim)] for i in range(dim)]
        return cls(dim, dim, data)

    @classmethod
    def zero(cls, rows: int, cols: int) -> ComplexMatrix:
        data = [[ComplexRational.zero() for _ in range(cols)] for _ in range(rows)]
        return cls(rows, cols, data)

    def __getitem__(self, idx: int) -> List[ComplexRational]:
        return self._data[idx]

    def add(self, other: ComplexMatrix) -> ComplexMatrix:
        return ComplexMatrix(self.rows, self.cols, [
            [self._data[i][j] + other._data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def sub(self, other: ComplexMatrix) -> ComplexMatrix:
        return ComplexMatrix(self.rows, self.cols, [
            [self._data[i][j] - other._data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def scale(self, scalar: ComplexRational) -> ComplexMatrix:
        return ComplexMatrix(self.rows, self.cols, [
            [self._data[i][j] * scalar for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def multiply(self, other: ComplexMatrix) -> ComplexMatrix:
        if self.cols != other.rows:
            raise ValueError(f"Shape mismatch: {self.rows}x{self.cols} vs {other.rows}x{other.cols}")
        res = [
            [
                sum((self._data[i][k] * other._data[k][j] for k in range(self.cols)), ComplexRational.zero())
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]
        return ComplexMatrix(self.rows, other.cols, res)

    def dagger(self) -> ComplexMatrix:
        """Conjugate transpose."""
        res = [
            [self._data[j][i].conjugate() for j in range(self.rows)]
            for i in range(self.cols)
        ]
        return ComplexMatrix(self.cols, self.rows, res)

    def is_hermitian(self) -> bool:
        if self.rows != self.cols:
            return False
        return all(self._data[i][j] == self._data[j][i].conjugate() for i in range(self.rows) for j in range(self.cols))

    def is_unitary(self) -> bool:
        if self.rows != self.cols:
            return False
        prod = self.multiply(self.dagger())
        id_m = self.identity(self.rows)
        return all(prod._data[i][j] == id_m._data[i][j] for i in range(self.rows) for j in range(self.cols))

    def inverse(self) -> ComplexMatrix:
        if self.rows != self.cols:
            raise ValueError("Only square matrices can be inverted")
        n = self.rows
        aug = [row[:] + [ComplexRational.one() if i == j else ComplexRational.zero() for j in range(n)] for i, row in enumerate(self._data)]

        for col in range(n):
            pivot = None
            for r in range(col, n):
                if aug[r][col] != ComplexRational.zero():
                    pivot = r
                    break
            if pivot is None:
                raise ValueError("Singular matrix")
            aug[col], aug[pivot] = aug[pivot], aug[col]

            scale = aug[col][col]
            for c in range(2 * n):
                aug[col][c] = aug[col][c] / scale

            for r in range(n):
                if r != col and aug[r][col] != ComplexRational.zero():
                    factor = aug[r][col]
                    for c in range(2 * n):
                        aug[r][c] = aug[r][c] - factor * aug[col][c]

        inv_data = [row[n:] for row in aug]
        return ComplexMatrix(n, n, inv_data)


def cayley_unitary(h: ComplexMatrix, tau: Fraction | int = 1) -> ComplexMatrix:
    """Computes unitary U = (I - i tau H)(I + i tau H)^-1 for Hermitian H."""
    if not h.is_hermitian():
        raise ValueError("Matrix H must be Hermitian")
    n = h.rows
    id_n = ComplexMatrix.identity(n)
    i_tau = ComplexRational(0, tau)
    scaled = h.scale(i_tau)
    num = id_n.sub(scaled)
    denom = id_n.add(scaled).inverse()
    return num.multiply(denom)


def cayley_generator(u: ComplexMatrix) -> ComplexMatrix:
    """Computes Hermitian generator H = i(U - I)(U + I)^-1 for unitary U."""
    if not u.is_unitary():
        raise ValueError("Matrix U must be unitary")
    n = u.rows
    id_n = ComplexMatrix.identity(n)
    denom = u.add(id_n).inverse()
    num = u.sub(id_n)
    return num.multiply(denom).scale(ComplexRational.i())


def pauli_matrices() -> Tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]:
    """Returns (sigma_x, sigma_y, sigma_z)."""
    sx = ComplexMatrix(2, 2, [
        [ComplexRational(0), ComplexRational(1)],
        [ComplexRational(1), ComplexRational(0)],
    ])
    sy = ComplexMatrix(2, 2, [
        [ComplexRational(0), ComplexRational(0, -1)],
        [ComplexRational(0, 1), ComplexRational(0)],
    ])
    sz = ComplexMatrix(2, 2, [
        [ComplexRational(1), ComplexRational(0)],
        [ComplexRational(0), ComplexRational(-1)],
    ])
    return sx, sy, sz
