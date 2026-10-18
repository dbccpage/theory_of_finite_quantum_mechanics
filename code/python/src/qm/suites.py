"""Dispatch a named suite onto a local exact check.

The norm suite returns a sum of two rational squares. The cycle suite returns
a product of exchange rates. Unknown names are refused.
"""
from fractions import Fraction


class SuiteError(Exception):
    """The suite name is not one of the local checks."""


def _norm_suite() -> Fraction:
    value = Fraction(3, 5) ** 2 + Fraction(4, 5) ** 2
    if value != 1:
        raise SuiteError(f"norm suite returned {value}")
    return value


def _cycle_suite() -> Fraction:
    product = Fraction(2, 3) * Fraction(3, 5) * Fraction(5, 2)
    if product != 1:
        raise SuiteError(f"cycle suite returned {product}")
    return product


def run_local_suite(name: str) -> Fraction:
    """Run the named exact suite and return its rational value."""
    suites = {
        "norm": _norm_suite,
        "cycle": _cycle_suite,
    }
    if name not in suites:
        raise SuiteError(f"unknown suite {name}")
    return suites[name]()
