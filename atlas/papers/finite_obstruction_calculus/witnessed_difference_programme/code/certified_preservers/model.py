"""Exact carrier and arithmetic shared by proposals and witness checks.

The scalar and matrix operations reuse the preceding paper rungs. Admission
here additionally checks exact field types, dimensions and positive definiteness.
Wire rationals are integers or canonical rational strings; floats and booleans
are never admitted as exact data.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction as Q

from hermitianization.model import GaussianRational as G
from state_effect_readout.model import GMatrix, add, dagger, gsum, identity, matmul

Vector = tuple[G, ...]
ZERO, ONE, I = G.of(0), G.of(1), G.of(0, 1)  # noqa: E741 - imaginary-unit notation


def rational(value: object) -> Q:
    if type(value) is Q:
        return value
    if type(value) is int:
        return Q(value)
    if type(value) is str:
        result = Q(value)
        if str(result) == value:
            return result
    raise ValueError("expected an integer or canonical exact rational")


def gaussian(value: object) -> G:
    if type(value) is G:
        if type(value.re) is not Q or type(value.im) is not Q:
            raise ValueError("Gaussian fields must be exact Fractions")
        return value
    if type(value) in (list, tuple):
        if len(value) != 2:
            raise ValueError("a Gaussian scalar has two coordinates")
        return G(rational(value[0]), rational(value[1]))
    return G(rational(value), Q(0))


def vector(raw: object, dimension: int | None = None) -> Vector:
    if type(raw) not in (list, tuple) or not raw:
        raise ValueError("expected a nonempty vector")
    result = tuple(gaussian(x) for x in raw)
    if dimension is not None and len(result) != dimension:
        raise ValueError("vector dimension mismatch")
    return result


def matrix(raw: object, dimension: int | None = None) -> GMatrix:
    if type(raw) not in (list, tuple) or not raw:
        raise ValueError("expected a nonempty square matrix")
    n = len(raw) if dimension is None else dimension
    if len(raw) != n:
        raise ValueError("matrix dimension mismatch")
    return tuple(vector(row, n) for row in raw)


def inv(z: G) -> G:
    n = z.norm()
    if n == 0:
        raise ValueError("zero Gaussian denominator")
    return G(z.re / n, -z.im / n)


def scale(z: G, a: GMatrix) -> GMatrix:
    return tuple(tuple(z * x for x in row) for row in a)


def subtract(a: GMatrix, b: GMatrix) -> GMatrix:
    return add(a, scale(-ONE, b))


def apply(a: GMatrix, x: Vector) -> Vector:
    if len(a[0]) != len(x):
        raise ValueError("operator/vector dimension mismatch")
    return tuple(gsum(u * v for u, v in zip(row, x, strict=True)) for row in a)


def conjugate(a: GMatrix) -> GMatrix:
    return tuple(tuple(x.conjugate() for x in row) for row in a)


def inverse(a: GMatrix) -> GMatrix:
    n = len(a)
    rows = [list(row) + list(unit) for row, unit in zip(a, identity(n), strict=True)]
    for col in range(n):
        pivot = next((j for j in range(col, n) if rows[j][col] != ZERO), None)
        if pivot is None:
            raise ValueError("singular matrix")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        c = inv(rows[col][col])
        rows[col] = [c * x for x in rows[col]]
        for j in range(n):
            if j != col:
                c = rows[j][col]
                rows[j] = [x + -(c * y) for x, y in zip(rows[j], rows[col], strict=True)]
    return tuple(tuple(row[n:]) for row in rows)


def positive_pivots(h: GMatrix) -> tuple[Q, ...]:
    """Exact Hermitian Schur complements; no numerical eigenvalue test."""
    if h != dagger(h):
        raise ValueError("Gram matrix is not Hermitian")
    a = h
    pivots = []
    while a:
        pivot = a[0][0]
        if pivot.im or pivot.re <= 0:
            raise ValueError("Gram matrix is not positive definite")
        pivots.append(pivot.re)
        a = tuple(
            tuple(a[j][k] + -(a[j][0] * inv(pivot) * a[0][k]) for k in range(1, len(a)))
            for j in range(1, len(a))
        )
    return tuple(pivots)


@dataclass(frozen=True)
class Carrier:
    gram: GMatrix

    def __post_init__(self) -> None:
        if type(self.gram) is not tuple or any(type(row) is not tuple for row in self.gram):
            raise ValueError("carrier matrix must be immutable")
        object.__setattr__(self, "gram", matrix(self.gram))
        positive_pivots(self.gram)

    @classmethod
    def from_wire(cls, raw: object) -> Carrier:
        return cls(matrix(raw))

    @property
    def dimension(self) -> int:
        return len(self.gram)

    def inner(self, x: Vector, y: Vector) -> G:
        if len(x) != self.dimension or len(y) != self.dimension:
            raise ValueError("inner-product dimension mismatch")
        return gsum(a.conjugate() * b for a, b in zip(x, apply(self.gram, y), strict=True))

    def norm(self, x: Vector) -> Q:
        value = self.inner(x, x)
        if value.im or value.re < 0:
            raise ValueError("invalid squared length")
        return value.re

    def probability(self, x: Vector, y: Vector) -> Q:
        den = self.norm(x) * self.norm(y)
        if den == 0:
            raise ValueError("zero vector has no ray probability")
        return self.inner(x, y).norm() / den

    def adjoint(self, a: GMatrix) -> GMatrix:
        return matmul(inverse(self.gram), matmul(dagger(a), self.gram))


def canonical_ray(x: Vector) -> Vector:
    first = next((v for v in x if v != ZERO), None)
    if first is None:
        raise ValueError("zero vector has no projective ray")
    return tuple(inv(first) * v for v in x)


def projection(carrier: Carrier, g: Vector) -> GMatrix:
    r = carrier.norm(g)
    if r <= 0:
        raise ValueError("zero projection target")
    covector = tuple(x.conjugate() for x in apply(carrier.gram, g))
    return tuple(tuple(x * y * G.of(1 / r) for y in covector) for x in g)


def basis_unit(n: int, j: int, k: int) -> GMatrix:
    return tuple(tuple(ONE if (r, c) == (j, k) else ZERO for c in range(n)) for r in range(n))


def linear_extension(table: tuple[GMatrix, ...], a: GMatrix) -> GMatrix:
    n = len(a)
    out = scale(ZERO, identity(n))
    for j in range(n):
        for k in range(n):
            out = add(out, scale(a[j][k], table[j * n + k]))
    return out


def wire(value: object) -> object:
    if type(value) is G:
        return [str(value.re), str(value.im)]
    if type(value) is Q:
        return str(value)
    if type(value) in (tuple, list):
        return [wire(v) for v in value]
    if type(value) is dict:
        return {k: wire(v) for k, v in value.items()}
    if value is None or type(value) in (str, int, bool):
        return value
    raise ValueError("unsupported wire value")


def digest(value: object) -> str:
    encoded = json.dumps(wire(value), sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def strict_json(text: str) -> object:
    def object_pairs(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError("duplicate JSON key")
            out[key] = value
        return out

    def refuse_number(value):
        raise ValueError(f"nonexact JSON number: {value}")

    return json.loads(
        text,
        object_pairs_hook=object_pairs,
        parse_float=refuse_number,
        parse_constant=refuse_number,
    )


class Exhausted(Exception):
    """An arithmetic search/check stopped; it proved no negative conclusion."""


@dataclass
class Fuel:
    limit: int
    used: int = 0

    def __post_init__(self) -> None:
        if type(self.limit) is not int or type(self.used) is not int:
            raise ValueError("fuel must be integral, not boolean")
        if not 0 <= self.used <= self.limit:
            raise ValueError("invalid fuel accounting")

    def spend(self) -> None:
        if self.used == self.limit:
            raise Exhausted("arithmetic operation budget exhausted")
        self.used += 1
