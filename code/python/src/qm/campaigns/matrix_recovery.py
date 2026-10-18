"""Recover a matrix from its action on the coordinate basis.

Origin: code/python/src/qm/campaigns/matrix_recovery.py
Claim: the columns A e_i rebuild A, and the entrywise defect is 0.
AuthorityEffect: None.
"""
from fractions import Fraction


class RecoveryError(Exception):
    """The recovered matrix differed from the original."""


def recover(columns) -> tuple:
    """columns[j] is A e_j. The rebuilt matrix has those columns."""
    size = len(columns)
    if any(len(column) != size for column in columns):
        raise RecoveryError("basis images do not match the dimension")
    return tuple(tuple(Fraction(columns[j][i]) for j in range(size)) for i in range(size))


def recovery_defect() -> Fraction:
    original = ((Fraction(1), Fraction(2)), (Fraction(3), Fraction(4)))
    columns = ((original[0][0], original[1][0]), (original[0][1], original[1][1]))
    rebuilt = recover(columns)
    defect = Fraction(0)
    for i in range(2):
        for j in range(2):
            defect += abs(rebuilt[i][j] - original[i][j])
    if defect != 0:
        raise RecoveryError(f"recovery defect is {defect}")
    return defect
