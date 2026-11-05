"""Exact sign cochains on the additive group Z2. AuthorityEffect: None.

Coefficients are {+1,-1} with trivial action. An inverse equals the sign itself,
so the multiplicative coboundary uses the same four factors as Boolean XOR.
Only degrees two and three are admitted.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from .boundary import Violation, evaluate
from .domains import integer, sequence
from .outcome import Outcome


def _sign(value: object) -> int:
    sign = integer(value, "cochain sign")
    if sign not in (-1, 1):
        raise Violation("input", "cochain signs must be -1 or 1")
    return sign


@dataclass(frozen=True, slots=True, init=False)
class BinarySignCochain:
    """Owns 2^degree signs in lexicographic coordinate order."""
    degree: int
    phases: tuple[int, ...]

    def __init__(self, degree: object, phases: object) -> None:
        admitted_degree = integer(degree, "cochain degree", 2, 3)
        admitted_phases = tuple(_sign(value) for value in sequence(phases, "cochain phases", 2**admitted_degree, 8))
        object.__setattr__(self, "degree", admitted_degree)
        object.__setattr__(self, "phases", admitted_phases)

    def _at(self, point: object) -> int:
        bits = tuple(integer(value, "group coordinate", 0, 1)
                     for value in sequence(point, "cochain point", self.degree, 3))
        index = 0
        for bit in bits:
            index = 2*index+bit
        return self.phases[index]

    def at(self, point: object) -> Outcome[int]:
        return evaluate(self._at, point)

    def is_normalized(self) -> bool:
        return all(self._at(point) == 1 for point in product((0, 1), repeat=self.degree) if 0 in point)

    def _coboundary(self) -> BinarySignCochain:
        if self.degree != 2:
            raise Violation("input", "coboundary requires a degree-two cochain")
        phases = tuple(self._at((b, c))*self._at((a ^ b, c))*self._at((a, b ^ c))*self._at((a, b))
                       for a, b, c in product((0, 1), repeat=3))
        return BinarySignCochain(3, phases)

    def coboundary(self) -> Outcome[BinarySignCochain]:
        return evaluate(self._coboundary)

    def _pentagon(self, point: object) -> int:
        if self.degree != 3:
            raise Violation("input", "pentagon requires a degree-three cochain")
        a, b, c, d = (integer(value, "pentagon coordinate", 0, 1)
                      for value in sequence(point, "pentagon point", 4, 4))
        return (self._at((b, c, d))*self._at((a ^ b, c, d))*self._at((a, b ^ c, d))
                *self._at((a, b, c ^ d))*self._at((a, b, c)))

    def pentagon(self, point: object) -> Outcome[int]:
        return evaluate(self._pentagon, point)

    def _multiply(self, other: object) -> BinarySignCochain:
        if type(other) is not BinarySignCochain or other.degree != self.degree:
            raise Violation("input", "pointwise multiplication requires the same cochain degree")
        return BinarySignCochain(self.degree, tuple(a*b for a, b in zip(self.phases, other.phases)))

    def multiply(self, other: object) -> Outcome[BinarySignCochain]:
        return evaluate(self._multiply, other)

    @classmethod
    def generator(cls) -> BinarySignCochain:
        return cls(3, tuple((-1)**(a*b*c) for a, b, c in product((0, 1), repeat=3)))
