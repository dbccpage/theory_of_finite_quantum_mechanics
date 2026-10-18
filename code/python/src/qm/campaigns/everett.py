"""Everett branch weights as a rational partition of unity.

Origin: code/python/src/qm/campaigns/everett.py
Claim: branches 1/2, 1/3, 1/6 sum to 1, and the conditional weight of the first branch in its sector is 3/5.
AuthorityEffect: None. This does not derive the Born rule.
"""
from fractions import Fraction


class EverettError(Exception):
    """Branch weights were negative or did not sum to 1."""


def branch_total(weights) -> Fraction:
    total = Fraction(0)
    for weight in weights:
        value = Fraction(weight)
        if value < 0:
            raise EverettError("a branch weight is negative")
        total += value
    if total != 1:
        raise EverettError(f"branch weights sum to {total}, not 1")
    return total


def conditional_weight(weights, sector) -> Fraction:
    """Renormalized weight of the first selected branch."""
    branch_total(weights)
    selected = [Fraction(weights[index]) for index in sector]
    mass = sum(selected, Fraction(0))
    if mass == 0:
        raise EverettError("the conditioning sector has no mass")
    return selected[0] / mass


def first_branch_conditional() -> Fraction:
    weights = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
    if branch_total(weights) != 1:
        raise EverettError("the Everett partition is not exhaustive")
    return conditional_weight(weights, (0, 1))
