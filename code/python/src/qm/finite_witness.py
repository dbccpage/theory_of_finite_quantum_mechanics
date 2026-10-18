"""Exact eigenpair witness for a 2 by 2 rational matrix.

The residual A v - λ v is summed entrywise. A second eigenpair is checked
the same way, and the returned value is the total residual.
"""
from fractions import Fraction


class FiniteWitnessError(Exception):
    """An eigenpair residual was nonzero."""


def _residual(matrix, vector, eigenvalue: Fraction) -> Fraction:
    total = Fraction(0)
    for row in range(2):
        image = matrix[row][0] * vector[0] + matrix[row][1] * vector[1]
        total += abs(image - eigenvalue * vector[row])
    return total


def eigenpair_residual() -> Fraction:
    """Return the summed residual of two eigenpairs of [[1, 1], [0, 2]]."""
    matrix = (
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(2)),
    )
    first = _residual(matrix, (Fraction(1), Fraction(0)), Fraction(1))
    second = _residual(matrix, (Fraction(1), Fraction(1)), Fraction(2))
    residual = first + second
    if residual != 0:
        raise FiniteWitnessError(f"eigenpair residual is {residual}")
    return residual
