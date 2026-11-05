"""Owned exact Gaussian three-vectors for the independent-checking context.

AuthorityEffect: None. Three immutable GaussianRational entries and all stored
component/total squared norms fit4096-bit rational bounds. Operations check
stored scalar results and vector norms; raw bounded rational arithmetic can
briefly exceed4096 bits before admission. Zero is a vector, not a ray.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from typing import cast

from .boundary import Violation, evaluate
from .domains import integer, rational, sequence
from .gaussian_rational import GaussianRational
from .outcome import Outcome

Entries = tuple[GaussianRational, GaussianRational, GaussianRational]
Norms = tuple[Q, Q, Q]
Pairs = tuple[tuple[Q, Q], tuple[Q, Q], tuple[Q, Q]]


def _scalar(value: object) -> GaussianRational:
    if type(value) is GaussianRational:
        return value
    re, im = sequence(value, 'Gaussian coordinate', 2)
    return GaussianRational(re, im)


@dataclass(frozen=True, slots=True, init=False)
class GaussianVector3:
    """Exact vector value object; public fallible operations return Outcome."""
    entries: Entries
    component_norms: Norms
    squared_norm: Q

    def __init__(self, value: object) -> None:
        entries = tuple(_scalar(x) for x in sequence(value, 'Gaussian three-vector', 3))
        norms = tuple(rational(x.norm_sq(), 'component squared norm') for x in entries)
        total = Q(0)
        for norm in norms:
            total = rational(total+norm, 'squared norm prefix')
        object.__setattr__(self, 'entries', entries)
        object.__setattr__(self, 'component_norms', norms)
        object.__setattr__(self, 'squared_norm', total)

    def to_pairs(self) -> Pairs:
        return cast(Pairs, tuple((x.re, x.im) for x in self.entries))

    @staticmethod
    def _integers(value: object) -> GaussianVector3:
        values = tuple(integer(x, 'integer coordinate') for x in sequence(value, 'six coordinates', 6))
        return GaussianVector3(tuple((values[i], values[i+1]) for i in (0, 2, 4)))

    @staticmethod
    def from_integers(value: object) -> Outcome[GaussianVector3]:
        return evaluate(GaussianVector3._integers, value)

    @staticmethod
    def _operand(value: object) -> GaussianVector3:
        if type(value) is not GaussianVector3:
            raise Violation('input', 'vector operation requires GaussianVector3')
        return value

    def _add(self, other: object) -> GaussianVector3:
        rhs = self._operand(other)
        return GaussianVector3(tuple(a+b for a, b in zip(self.entries, rhs.entries)))

    def add(self, other: object) -> Outcome[GaussianVector3]:
        return evaluate(self._add, other)

    def _sub(self, other: object) -> GaussianVector3:
        rhs = self._operand(other)
        return GaussianVector3(tuple(a-b for a, b in zip(self.entries, rhs.entries)))

    def sub(self, other: object) -> Outcome[GaussianVector3]:
        return evaluate(self._sub, other)

    def _scale(self, scalar: object) -> GaussianVector3:
        factor = _scalar(scalar)
        return GaussianVector3(tuple(factor*x for x in self.entries))

    def scale(self, scalar: object) -> Outcome[GaussianVector3]:
        return evaluate(self._scale, scalar)

    def _inner(self, other: object) -> GaussianRational:
        rhs = self._operand(other)
        total = GaussianRational(0)
        for left, right in zip(self.entries, rhs.entries):
            total = total + left.conj()*right
        return total

    def inner(self, other: object) -> Outcome[GaussianRational]:
        return evaluate(self._inner, other)

    def _cross(self, other: object) -> GaussianVector3:
        rhs = self._operand(other).entries
        left = self.entries
        return GaussianVector3(tuple((left[i]*rhs[j]-left[j]*rhs[i]).conj()
                                     for i, j in ((1, 2), (2, 0), (0, 1))))

    def cross(self, other: object) -> Outcome[GaussianVector3]:
        return evaluate(self._cross, other)

    def _integer_primitive(self) -> bool:
        parts = tuple(part for pair in self.to_pairs() for part in pair)
        if any(part.denominator != 1 for part in parts):
            raise Violation('input', '(1+i) primitivity requires Gaussian integer coordinates')
        return any((part.re.numerator+part.im.numerator) % 2 != 0 for part in self.entries)

    def integer_primitive(self) -> Outcome[bool]:
        return evaluate(self._integer_primitive)
