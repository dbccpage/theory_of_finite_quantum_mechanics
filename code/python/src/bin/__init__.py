"""Binary entrypoints for the finite engine.

Origin: code/python/src/bin/__init__.py
Claim: the rational point (3/5, 4/5) on the circle has norm 1, as a witness for this package.
AuthorityEffect: None.
"""
from fractions import Fraction


class BinWitnessError(Exception):
    """The bin-package two-square witness failed."""


def bin_two_square() -> Fraction:
    """Return (3/5)^2 + (4/5)^2, which is the rational norm 1."""
    norm = Fraction(3, 5) ** 2 + Fraction(4, 5) ** 2
    if norm != 1:
        raise BinWitnessError(f"bin two-square norm is {norm}, not 1")
    return norm
