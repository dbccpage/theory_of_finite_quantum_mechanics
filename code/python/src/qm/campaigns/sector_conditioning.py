"""Condition a rational distribution on a sector and renormalize.

Origin: code/python/src/qm/campaigns/sector_conditioning.py
Claim: (1/2, 1/4, 1/4) conditioned on the first two outcomes is (2/3, 1/3).
AuthorityEffect: None.
"""
from fractions import Fraction


class SectorError(Exception):
    """The sector was empty or the distribution was not a probability."""


def condition(weights, sector) -> tuple:
    values = [Fraction(weight) for weight in weights]
    if any(value < 0 for value in values) or sum(values, Fraction(0)) != 1:
        raise SectorError("weights must be a rational probability vector")
    if not sector:
        raise SectorError("the sector is empty")
    selected = [values[index] for index in sector]
    mass = sum(selected, Fraction(0))
    if mass == 0:
        raise SectorError("the sector has no mass")
    return tuple(value / mass for value in selected)


def first_sector_weight() -> Fraction:
    conditional = condition((Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)), (0, 1))
    if conditional != (Fraction(2, 3), Fraction(1, 3)):
        raise SectorError(f"conditional distribution is {conditional}")
    if sum(conditional, Fraction(0)) != 1:
        raise SectorError("conditional weights do not sum to 1")
    return conditional[0]
