"""Rational Householder involution and Gaussian conjugation.

Origin: code/python/src/linear_algebra/involution.py
Claim: J(v)^2 = I for a nonzero rational vector, and conjugation squares to the identity on Q(i).
AuthorityEffect: None.
"""
from fractions import Fraction
from typing import Sequence

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class InvolutionError(Exception):
    """The vector was empty, zero, or not rational."""


def householder(vector: Sequence[object]) -> ExactMatrix:
    """Return I − 2 vv^T / (v·v), which is an involution over Q."""
    if not vector:
        raise InvolutionError("Householder vector must be nonempty")
    coords = []
    for value in vector:
        if isinstance(value, GaussianRational):
            raise InvolutionError("Householder involution in this module is over Q, not Q(i)")
        try:
            coords.append(Fraction(value))
        except (TypeError, ValueError) as exc:
            raise InvolutionError(f"entry {value!r} is not rational") from exc
    norm_sq = sum((coord * coord for coord in coords), Fraction(0))
    if norm_sq == 0:
        raise InvolutionError("Householder vector must be nonzero")
    n = len(coords)
    data = []
    for i in range(n):
        for j in range(n):
            value = Fraction(1) if i == j else Fraction(0)
            value -= Fraction(2) * coords[i] * coords[j] / norm_sq
            data.append(value)
    mirror = ExactMatrix(n, n, data)
    if mirror * mirror != ExactMatrix.identity(n):
        raise InvolutionError("constructed Householder matrix is not an involution")
    return mirror


def conjugation_square(real: object, imag: object) -> GaussianRational:
    """Conjugate twice and return the original Gaussian rational."""
    value = GaussianRational(Fraction(real), Fraction(imag))
    twice = value.conjugate().conjugate()
    if twice != value:
        raise InvolutionError("conjugation failed to be an involution")
    return twice


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "Q",
    "q",
    "InvolutionError",
    "householder",
    "conjugation_square",
]
