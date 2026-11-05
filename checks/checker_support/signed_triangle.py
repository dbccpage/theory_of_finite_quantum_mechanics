"""Owned vertex-sign switching on one three-cycle. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass

from .boundary import Violation, evaluate
from .domains import integer, sequence
from .outcome import Outcome
from .rational_matrix import RationalMatrix


def _sign(value: object) -> int:
    sign = integer(value, "triangle sign")
    if sign not in (-1, 1):
        raise Violation("input", "triangle signs must be -1 or 1")
    return sign


def _signs(value: object, name: str) -> tuple[int, int, int]:
    a, b, c = (_sign(item) for item in sequence(value, name, 3, 3))
    return a, b, c


@dataclass(frozen=True, slots=True, init=False)
class SignedTriangle:
    """Owns three signs in edge order (01,12,20) for a symmetric triangle."""
    edges: tuple[int, int, int]

    def __init__(self, edges: object) -> None:
        object.__setattr__(self, "edges", _signs(edges, "triangle edges"))

    @property
    def cycle_product(self) -> int:
        a, b, c = self.edges
        return a*b*c

    @property
    def is_balanced(self) -> bool:
        return self.cycle_product == 1

    @property
    def normalizing_gauge(self) -> tuple[int, int, int]:
        a, b, _ = self.edges
        return 1, a, a*b

    @property
    def adjacency(self) -> RationalMatrix:
        a, b, c = self.edges
        return RationalMatrix(((0, a, c), (a, 0, b), (c, b, 0)))

    def _switch(self, gauge: object) -> SignedTriangle:
        g0, g1, g2 = _signs(gauge, "vertex gauge")
        a, b, c = self.edges
        return SignedTriangle((g0*a*g1, g1*b*g2, g2*c*g0))

    def switch(self, gauge: object) -> Outcome[SignedTriangle]:
        return evaluate(self._switch, gauge)
