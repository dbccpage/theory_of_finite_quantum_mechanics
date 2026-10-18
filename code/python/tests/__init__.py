"""Finite QM End-to-End (E2E) Test Suite Package.

AuthorityEffect: None.

Origin: code/python/tests/__init__.py
Claim: the test-package witness (3/5)^2 + (4/5)^2 equals 1.
"""
from fractions import Fraction


def test_package_two_square() -> Fraction:
    """Rational norm used as the package witness. Tests may compare it with Fraction(1)."""
    norm = Fraction(3, 5) ** 2 + Fraction(4, 5) ** 2
    if norm != 1:
        raise ValueError(f"test package norm is {norm}, not 1")
    return norm
