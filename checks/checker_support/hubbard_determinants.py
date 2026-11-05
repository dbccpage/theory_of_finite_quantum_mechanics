"""Owned exact spin determinants and field weight. AuthorityEffect: None."""
from dataclasses import dataclass
from fractions import Fraction as Q

from .domains import integer, rational


@dataclass(frozen=True, slots=True, init=False)
class HubbardDeterminants:
    """Admitted result; weight is derived with bounded products, never supplied."""
    d_up: Q
    d_down: Q
    prefactor: Q
    weight: Q
    total_s: int

    def __init__(self, d_up: object, d_down: object, prefactor: object, total_s: object) -> None:
        up = rational(d_up, "up determinant")
        down = rational(d_down, "down determinant")
        coefficient = rational(prefactor, "field prefactor", strictly_positive=True)
        field_sum = integer(total_s, "field sum", -16, 16)
        weight = rational(rational(coefficient*up, "prefactored up determinant")*down, "field weight")
        for name, value in (("d_up", up), ("d_down", down), ("prefactor", coefficient), ("weight", weight)):
            object.__setattr__(self, name, value)
        object.__setattr__(self, "total_s", field_sum)
