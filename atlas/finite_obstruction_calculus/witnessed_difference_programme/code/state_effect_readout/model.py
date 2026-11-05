"""Exact Gaussian-rational Gram-factor state/effect model."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from hermitianization.model import GaussianRational, rational

G = GaussianRational
GMatrix = tuple[tuple[G, ...], ...]


def gaussian(value: object) -> G:
    if isinstance(value, G):
        return value
    if isinstance(value, (int, str, Fraction)):
        return G.of(value)
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return G.of(value[0], value[1])
    raise TypeError(f"unsupported Gaussian-rational value: {value!r}")


def gmatrix(rows: Iterable[Iterable[object]]) -> GMatrix:
    result = tuple(tuple(gaussian(value) for value in row) for row in rows)
    if not result or not result[0]:
        raise ValueError("matrix must be nonempty")
    if any(len(row) != len(result[0]) for row in result):
        raise ValueError("matrix rows have unequal lengths")
    return result


def shape(a: GMatrix) -> tuple[int, int]:
    return len(a), len(a[0])


def gsum(values: Iterable[G]) -> G:
    result = G.of(0)
    for value in values:
        result = result + value
    return result


def dagger(a: GMatrix) -> GMatrix:
    rows, cols = shape(a)
    return tuple(tuple(a[i][j].conjugate() for i in range(rows)) for j in range(cols))


def matmul(a: GMatrix, b: GMatrix) -> GMatrix:
    ar, ac = shape(a)
    br, bc = shape(b)
    if ac != br:
        raise ValueError(f"matrix shape mismatch: {(ar, ac)} times {(br, bc)}")
    return tuple(
        tuple(gsum(a[i][k] * b[k][j] for k in range(ac)) for j in range(bc))
        for i in range(ar)
    )


def add(a: GMatrix, b: GMatrix) -> GMatrix:
    if shape(a) != shape(b):
        raise ValueError("matrix addition shape mismatch")
    return tuple(tuple(x + y for x, y in zip(arow, brow, strict=True))
                 for arow, brow in zip(a, b, strict=True))


def scale_real(c: Fraction, a: GMatrix) -> GMatrix:
    scalar = G.of(c)
    return tuple(tuple(scalar * value for value in row) for row in a)


def identity(n: int) -> GMatrix:
    if type(n) is not int or n <= 0:
        raise ValueError("dimension must be positive")
    return tuple(tuple(G.of(1 if i == j else 0) for j in range(n)) for i in range(n))


def trace(a: GMatrix) -> G:
    rows, cols = shape(a)
    if rows != cols:
        raise ValueError("trace requires a square matrix")
    return gsum(a[i][i] for i in range(rows))


def gram(a: GMatrix) -> GMatrix:
    return matmul(dagger(a), a)


def frobenius_square(a: GMatrix) -> Fraction:
    return sum((value.norm() for row in a for value in row), Fraction(0))


@dataclass(frozen=True)
class StateFactor:
    factor: GMatrix

    def __post_init__(self) -> None:
        object.__setattr__(self, "factor", gmatrix(self.factor))
        if frobenius_square(self.factor) <= 0:
            raise ValueError("state factor must have positive Frobenius mass")

    @property
    def dimension(self) -> int:
        return shape(self.factor)[1]

    @property
    def denominator(self) -> Fraction:
        return frobenius_square(self.factor)

    @property
    def density(self) -> GMatrix:
        return scale_real(Fraction(1, 1) / self.denominator, gram(self.factor))


@dataclass(frozen=True)
class BinaryEffectFactor:
    accept: GMatrix
    reject: GMatrix

    def __post_init__(self) -> None:
        object.__setattr__(self, "accept", gmatrix(self.accept))
        object.__setattr__(self, "reject", gmatrix(self.reject))
        ar, ac = shape(self.accept)
        rr, rc = shape(self.reject)
        if ac != rc:
            raise ValueError("binary effect factors must have equal column counts")
        if add(gram(self.accept), gram(self.reject)) != identity(ac):
            raise ValueError("binary effect factors do not resolve the identity")

    @property
    def dimension(self) -> int:
        return shape(self.accept)[1]

    @property
    def effect(self) -> GMatrix:
        return gram(self.accept)

    @property
    def complement(self) -> GMatrix:
        return gram(self.reject)


def born_numerator(state: StateFactor, factor: GMatrix) -> Fraction:
    factor = gmatrix(factor)
    if shape(factor)[1] != state.dimension:
        raise ValueError("state/effect dimension mismatch")
    return frobenius_square(matmul(factor, dagger(state.factor)))


def born_probability(state: StateFactor, effect: BinaryEffectFactor) -> Fraction:
    if state.dimension != effect.dimension:
        raise ValueError("state/effect dimension mismatch")
    return born_numerator(state, effect.accept) / state.denominator


def complement_probability(state: StateFactor, effect: BinaryEffectFactor) -> Fraction:
    if state.dimension != effect.dimension:
        raise ValueError("state/effect dimension mismatch")
    return born_numerator(state, effect.reject) / state.denominator


def trace_probability(state: StateFactor, effect: BinaryEffectFactor) -> Fraction:
    value = trace(matmul(state.density, effect.effect))
    if value.im != 0:
        raise ValueError("trace readout is not real")
    return value.re


def depolarized_probability(
    state: StateFactor, effect: BinaryEffectFactor, weight: Fraction
) -> Fraction:
    weight = rational(weight)
    if not 0 <= weight <= 1:
        raise ValueError("depolarization weight must lie in [0,1]")
    maximally_mixed = trace(effect.effect).re / state.dimension
    return weight * born_probability(state, effect) + (1 - weight) * maximally_mixed


def phase_scale(z: G, a: GMatrix) -> GMatrix:
    if z.norm() != 1:
        raise ValueError("phase must have unit norm")
    return tuple(tuple(z * value for value in row) for row in a)
