"""A separating predicate: the observable Z takes different expectations on two states.

Origin: code/python/src/qm/campaigns/separating_preds.py
Claim: <Z> on (1, 0) is 1 and <Z> on (3/5, 4/5) is −7/25, so the difference is 32/25.
AuthorityEffect: None.
"""
from fractions import Fraction


class SeparationError(Exception):
    """The predicate did not separate the two states."""


def z_expectation(amplitude) -> Fraction:
    up = Fraction(amplitude[0])
    down = Fraction(amplitude[1])
    if up * up + down * down != 1:
        raise SeparationError("a state is not normalized")
    return up * up - down * down


def expectation_gap() -> Fraction:
    computational = z_expectation((1, 0))
    tilted = z_expectation((Fraction(3, 5), Fraction(4, 5)))
    gap = computational - tilted
    if gap == 0:
        raise SeparationError("Z does not separate the two states")
    return gap
