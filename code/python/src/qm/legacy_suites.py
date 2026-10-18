"""Three local exact checks collected as a legacy suite.

Each check returns a rational or an integer. The suite total is the number
of checks whose recomputed value matches a second evaluation.
"""
from fractions import Fraction


class LegacySuiteError(Exception):
    """A legacy check did not reproduce."""


def _norm() -> Fraction:
    return Fraction(3, 5) ** 2 + Fraction(4, 5) ** 2


def _cycle() -> Fraction:
    rates = (Fraction(2, 3), Fraction(3, 5), Fraction(5, 2))
    product = Fraction(1)
    for rate in rates:
        product *= rate
    return product


def _shear_entry() -> Fraction:
    return Fraction(2, 3) + Fraction(4, 5)


def suite_pass_count() -> int:
    """Return how many checks equal their closed forms."""
    closed = (
        (_norm(), Fraction(1)),
        (_cycle(), Fraction(1)),
        (_shear_entry(), Fraction(22, 15)),
    )
    passed = 0
    for value, target in closed:
        if value != target:
            raise LegacySuiteError(f"{value} does not equal {target}")
        passed += 1
    return passed
