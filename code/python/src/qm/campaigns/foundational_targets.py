"""Foundational target: purity of a rational density with trace 1.

Origin: code/python/src/qm/campaigns/foundational_targets.py
Claim: rho = [[1/2, 1/4], [1/4, 1/2]] has trace 1 and tr(rho^2) = 5/8.
AuthorityEffect: None. Positive-semidefiniteness is the principal-minor check below, not a spectrum oracle.
"""
from fractions import Fraction


class TargetError(Exception):
    """The target matrix was not a rational trace-1 Hermitian matrix."""


def _mul(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def purity(matrix) -> Fraction:
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise TargetError("the target density is 2 by 2")
    entries = tuple(tuple(Fraction(value) for value in row) for row in matrix)
    if entries[0][1] != entries[1][0]:
        raise TargetError("the target density is not symmetric")
    trace = entries[0][0] + entries[1][1]
    if trace != 1:
        raise TargetError(f"trace is {trace}, not 1")
    determinant = entries[0][0] * entries[1][1] - entries[0][1] * entries[1][0]
    if entries[0][0] < 0 or determinant < 0:
        raise TargetError("a principal minor is negative")
    square = _mul(entries, entries)
    return square[0][0] + square[1][1]


def target_purity() -> Fraction:
    value = purity(((Fraction(1, 2), Fraction(1, 4)), (Fraction(1, 4), Fraction(1, 2))))
    if value != Fraction(5, 8):
        raise TargetError(f"purity {value} disagrees with 5/8")
    return value
