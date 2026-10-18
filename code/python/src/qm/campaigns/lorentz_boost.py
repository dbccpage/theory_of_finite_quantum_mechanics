"""A rational Lorentz boost preserves the Minkowski form diag(1, −1).

Origin: code/python/src/qm/campaigns/lorentz_boost.py
Claim: for beta = 3/5 and gamma = 5/4, B^T η B − η is the zero matrix.
AuthorityEffect: None.
"""
from fractions import Fraction


class LorentzError(Exception):
    """The boost did not preserve η or failed the gamma identity."""


def _mul(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def _transpose(matrix):
    return tuple(tuple(matrix[i][j] for i in range(2)) for j in range(2))


def minkowski_defect() -> Fraction:
    beta = Fraction(3, 5)
    gamma = Fraction(5, 4)
    if gamma * gamma * (1 - beta * beta) != 1:
        raise LorentzError("gamma is not the Lorentz factor of beta")
    boost = ((gamma, gamma * beta), (gamma * beta, gamma))
    eta = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(-1)))
    preserved = _mul(_transpose(boost), _mul(eta, boost))
    defect = Fraction(0)
    for i in range(2):
        for j in range(2):
            defect += abs(preserved[i][j] - eta[i][j])
    if defect != 0:
        raise LorentzError(f"Minkowski defect is {defect}")
    return defect
