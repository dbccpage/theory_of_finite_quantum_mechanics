"""Owned equatorial Gaussian geometry for exact Piron and rotation controls.

AuthorityEffect: None. A nonzero vector in the north-pole orthogonal plane is
owned with its pole sum and quarter-turn. All arithmetic composes bounded
GaussianVector3 values; public fallible queries use Outcome.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q

from .boundary import Violation, evaluate
from .domains import rational
from .gaussian_rational import GaussianRational as G
from .gaussian_vector3 import GaussianVector3 as V
from .orthogonal_gaussian_pair import OrthogonalGaussianPair
from .outcome import Outcome

NORTH = V(((1, 0), (0, 0), (0, 0)))


@dataclass(frozen=True, slots=True, init=False)
class EquatorialRayGeometry:
    """Invariant: y!=0 and y.x=0; north+y is nonzero, with cached quarter-turn."""
    vector: V
    base: V
    quarter_turn: V

    def __init__(self, value: object) -> None:
        vector = V._operand(value)
        if vector.entries[0] != G(0) or vector.squared_norm == 0:
            raise Violation('input', 'equatorial geometry requires a nonzero vector with x=0')
        _, y, z = vector.entries
        turned = V((G(0), G(-z.re, z.im), y.conj()))
        base = NORTH._add(vector)
        object.__setattr__(self, 'vector', vector)
        object.__setattr__(self, 'base', base)
        object.__setattr__(self, 'quarter_turn', turned)

    @staticmethod
    def _born_weight(value: object) -> Q:
        vector = V._operand(value)
        if vector.squared_norm == 0:
            raise Violation('input', 'Born ray weight requires a nonzero vector')
        return rational(vector.component_norms[0]/vector.squared_norm, 'north-pole Born weight')

    @staticmethod
    def born_weight(value: object) -> Outcome[Q]:
        return evaluate(EquatorialRayGeometry._born_weight, value)

    def _tangent(self, parameter: object) -> V:
        t = rational(parameter, 'real tangent parameter')
        return self.vector._add(self.quarter_turn._scale(G(t)))

    def tangent(self, parameter: object) -> Outcome[V]:
        return evaluate(self._tangent, parameter)

    def _pythagorean(self, parameter: object) -> V:
        k = rational(parameter, 'real Pythagorean parameter')
        square = rational(k*k, 'Pythagorean square')
        denominator = rational(square+1, 'Pythagorean denominator')
        first = rational((square-1)/denominator, 'Pythagorean cosine')
        second = rational(rational(2*k, 'Pythagorean numerator')/denominator, 'Pythagorean sine')
        return self.vector._scale(G(first))._add(self.quarter_turn._scale(G(second)))

    def pythagorean(self, parameter: object) -> Outcome[V]:
        return evaluate(self._pythagorean, parameter)

    def _kelvin(self) -> V:
        return self.vector._scale(G(-1/self.vector.squared_norm))

    def kelvin(self) -> Outcome[V]:
        return evaluate(self._kelvin)

    def _meridian(self) -> V:
        return NORTH._scale(G(-self.vector.squared_norm))._add(self.vector)

    def meridian(self) -> Outcome[V]:
        return evaluate(self._meridian)

    def _piron(self, scalar: object) -> OrthogonalGaussianPair:
        partner = self.quarter_turn._scale(scalar)
        pair = OrthogonalGaussianPair(self.base, partner)
        return pair._rotate(G(1), G(1))

    def piron(self, scalar: object) -> Outcome[OrthogonalGaussianPair]:
        return evaluate(self._piron, scalar)
