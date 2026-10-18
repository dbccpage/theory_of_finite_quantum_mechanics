"""Spectral claim for a rational 2 by 2 matrix with rational eigenvalues.

Origin: code/python/src/qm/campaigns/spectral_claims.py
Claim: det(λI − A) = (λ − 1)(λ − 2) for A = [[1, 1], [0, 2]], and both eigenvalues kill the polynomial.
AuthorityEffect: None.
"""
from fractions import Fraction


class SpectralError(Exception):
    """The characteristic polynomial did not vanish at a claimed eigenvalue."""


def characteristic_value(matrix, point: Fraction) -> Fraction:
    """det(point * I − matrix) for a 2 by 2 matrix."""
    a = Fraction(matrix[0][0])
    b = Fraction(matrix[0][1])
    c = Fraction(matrix[1][0])
    d = Fraction(matrix[1][1])
    return (point - a) * (point - d) - b * c


def eigenvalue_defect() -> Fraction:
    matrix = ((1, 1), (0, 2))
    defect = abs(characteristic_value(matrix, Fraction(1))) + abs(characteristic_value(matrix, Fraction(2)))
    expanded = characteristic_value(matrix, Fraction(0))
    if expanded != 2:
        raise SpectralError(f"constant term is {expanded}, not det(A) = 2")
    if defect != 0:
        raise SpectralError(f"eigenvalue defect is {defect}")
    return defect
