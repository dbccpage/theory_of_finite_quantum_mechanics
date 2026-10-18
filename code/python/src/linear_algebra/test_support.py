"""Exact fixtures for rational matrix checks.

Origin: code/python/src/linear_algebra/test_support.py
Claim: the 2 by 2 witness [[1, 2], [3, 4]] has determinant 1*4 − 2*3 = −2, matching elimination.
AuthorityEffect: None.
"""
from fractions import Fraction

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class FixtureError(Exception):
    """A fixture did not satisfy the identity it advertises."""


def sample_matrix() -> ExactMatrix:
    """The integer witness used by the determinant check."""
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(2)],
            [Fraction(3), Fraction(4)],
        ]
    )


def sample_determinant() -> Fraction:
    """ad − bc, recomputed from the entries and checked against ExactMatrix.determinant."""
    matrix = sample_matrix()
    a = Fraction(matrix.get(0, 0))
    b = Fraction(matrix.get(0, 1))
    c = Fraction(matrix.get(1, 0))
    d = Fraction(matrix.get(1, 1))
    by_minors = a * d - b * c
    if by_minors != matrix.determinant():
        raise FixtureError(f"minor determinant {by_minors} disagrees with elimination")
    return by_minors


def hilbert_entry(i: int, j: int) -> Fraction:
    """The rational Hilbert entry 1/(i+j+1), indexed from 0."""
    if isinstance(i, bool) or isinstance(j, bool) or not isinstance(i, int) or not isinstance(j, int):
        raise FixtureError("Hilbert indices must be ints")
    if i < 0 or j < 0:
        raise FixtureError("Hilbert indices must be nonnegative")
    return Fraction(1, i + j + 1)


def hilbert_matrix(n: int) -> ExactMatrix:
    """The n by n Hilbert matrix over Q. Its 2 by 2 determinant is checked when n >= 2."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise FixtureError("Hilbert size must be a positive int")
    matrix = ExactMatrix.from_rows([[hilbert_entry(i, j) for j in range(n)] for i in range(n)])
    if n >= 2:
        minor = ExactMatrix.from_rows([[hilbert_entry(0, 0), hilbert_entry(0, 1)], [hilbert_entry(1, 0), hilbert_entry(1, 1)]])
        expected = Fraction(1, 1) * Fraction(1, 3) - Fraction(1, 2) * Fraction(1, 2)
        if minor.determinant() != expected:
            raise FixtureError("2 by 2 Hilbert determinant disagrees with the minor formula")
    return matrix


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "Q",
    "q",
    "FixtureError",
    "sample_matrix",
    "sample_determinant",
    "hilbert_entry",
    "hilbert_matrix",
]
