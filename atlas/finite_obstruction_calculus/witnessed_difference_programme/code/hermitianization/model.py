"""Exact matrix model for the finite Hermitianization theorem.

All arithmetic uses :class:`fractions.Fraction`.  The matrix ``J`` and the
observer rows are supplied data.  Validation checks ``J^2=-I`` and the exact
skew-adjoint/isometry laws for the observer Gram matrix before any Hermitian
claim is accepted.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

Q = Fraction
Vector = tuple[Q, ...]
Matrix = tuple[tuple[Q, ...], ...]


def rational(value: object) -> Q:
    if isinstance(value, bool):
        raise TypeError(f"unsupported rational value: {value!r}")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    raise TypeError(f"unsupported rational value: {value!r}")


def vector(values: Iterable[object]) -> Vector:
    return tuple(rational(value) for value in values)


def matrix(rows: Iterable[Iterable[object]]) -> Matrix:
    result = tuple(vector(row) for row in rows)
    if result and any(len(row) != len(result[0]) for row in result):
        raise ValueError("matrix rows have unequal lengths")
    return result

def _shape(a: Matrix) -> tuple[int, int]:
    return len(a), len(a[0]) if a else 0


def transpose(a: Matrix) -> Matrix:
    rows, cols = _shape(a)
    return tuple(tuple(a[i][j] for i in range(rows)) for j in range(cols))


def matmul(a: Matrix, b: Matrix) -> Matrix:
    ar, ac = _shape(a)
    br, bc = _shape(b)
    if ac != br:
        raise ValueError(f"matrix shape mismatch: {(ar, ac)} times {(br, bc)}")
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(ac)), Q(0)) for j in range(bc))
        for i in range(ar)
    )


def matvec(a: Matrix, x: Vector) -> Vector:
    rows, cols = _shape(a)
    if cols != len(x):
        raise ValueError(f"matrix/vector shape mismatch: {(rows, cols)} and {len(x)}")
    return tuple(sum((a[i][j] * x[j] for j in range(cols)), Q(0)) for i in range(rows))


def add_matrix(a: Matrix, b: Matrix) -> Matrix:
    if _shape(a) != _shape(b):
        raise ValueError("matrix addition shape mismatch")
    return tuple(tuple(x + y for x, y in zip(arow, brow, strict=True))
                 for arow, brow in zip(a, b, strict=True))


def scale_matrix(c: Q, a: Matrix) -> Matrix:
    return tuple(tuple(c * value for value in row) for row in a)


def identity(n: int) -> Matrix:
    return tuple(tuple(Q(1) if i == j else Q(0) for j in range(n)) for i in range(n))


def dot(x: Vector, y: Vector) -> Q:
    if len(x) != len(y):
        raise ValueError("dot-product dimension mismatch")
    return sum((a * b for a, b in zip(x, y, strict=True)), Q(0))


def gram_matrix(observer: Matrix) -> Matrix:
    return matmul(transpose(observer), observer)


def bilinear(g: Matrix, x: Vector, y: Vector) -> Q:
    return dot(x, matvec(g, y))


@dataclass(frozen=True)
class GaussianRational:
    re: Q
    im: Q

    def __post_init__(self) -> None:
        object.__setattr__(self, "re", rational(self.re))
        object.__setattr__(self, "im", rational(self.im))

    @classmethod
    def of(cls, re: object, im: object = 0) -> "GaussianRational":
        return cls(rational(re), rational(im))

    def __add__(self, other: "GaussianRational") -> "GaussianRational":
        return GaussianRational(self.re + other.re, self.im + other.im)

    def __neg__(self) -> "GaussianRational":
        return GaussianRational(-self.re, -self.im)

    def __mul__(self, other: "GaussianRational") -> "GaussianRational":
        return GaussianRational(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def conjugate(self) -> "GaussianRational":
        return GaussianRational(self.re, -self.im)

    def norm(self) -> Q:
        return self.re * self.re + self.im * self.im


def add_vector(x: Vector, y: Vector) -> Vector:
    if len(x) != len(y):
        raise ValueError("vector addition dimension mismatch")
    return tuple(a + b for a, b in zip(x, y, strict=True))


def scale_vector(c: Q, x: Vector) -> Vector:
    return tuple(c * value for value in x)


def complex_scalar_action(z: GaussianRational, j: Matrix, x: Vector) -> Vector:
    return add_vector(scale_vector(z.re, x), scale_vector(z.im, matvec(j, x)))


def hermitian_pairing(g: Matrix, j: Matrix, x: Vector, y: Vector) -> GaussianRational:
    return GaussianRational(bilinear(g, x, y), bilinear(g, matvec(j, x), y))


@dataclass(frozen=True)
class HermitianizationCheck:
    dimension: int
    complex_square: bool
    gram_symmetric: bool
    skew_adjoint: bool
    isometry: bool

    @property
    def accepted(self) -> bool:
        return (
            self.complex_square
            and self.gram_symmetric
            and self.skew_adjoint
            and self.isometry
        )


def validate_hermitianization(observer: Matrix, j: Matrix) -> HermitianizationCheck:
    jr, jc = _shape(j)
    if jr == 0 or jr != jc:
        raise ValueError("J must be a nonempty square matrix")
    if _shape(observer)[1] != jr:
        raise ValueError("observer and J dimensions disagree")
    g = gram_matrix(observer)
    jt = transpose(j)
    return HermitianizationCheck(
        dimension=jr,
        complex_square=matmul(j, j) == scale_matrix(Q(-1), identity(jr)),
        gram_symmetric=g == transpose(g),
        skew_adjoint=matmul(jt, g) == scale_matrix(Q(-1), matmul(g, j)),
        isometry=matmul(matmul(jt, g), j) == g,
    )


def require_hermitianization(observer: Matrix, j: Matrix) -> HermitianizationCheck:
    result = validate_hermitianization(observer, j)
    if not result.accepted:
        failed = [
            name
            for name in ("complex_square", "gram_symmetric", "skew_adjoint", "isometry")
            if not getattr(result, name)
        ]
        raise ValueError("incompatible Hermitianization data: " + ", ".join(failed))
    return result
