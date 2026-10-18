"""Commutators of rational observables, measured by the sum of absolute entries.

Origin: code/python/src/qm/campaigns/commuting_obs.py
Claim: two diagonal matrices commute, and X and Z do not.
AuthorityEffect: None.
"""
from fractions import Fraction


class CommutatorError(Exception):
    """The observables were not square of the same shape."""


def _mul(left, right):
    rows = len(left)
    cols = len(right[0])
    mid = len(right)
    if any(len(row) != mid for row in left):
        raise CommutatorError("observable shapes do not match")
    return tuple(
        tuple(sum(Fraction(left[i][k]) * Fraction(right[k][j]) for k in range(mid)) for j in range(cols))
        for i in range(rows)
    )


def commutator_mass(left, right) -> Fraction:
    """Sum of absolute entries of XY − YX."""
    xy = _mul(left, right)
    yx = _mul(right, left)
    total = Fraction(0)
    for i in range(len(xy)):
        for j in range(len(xy[0])):
            total += abs(xy[i][j] - yx[i][j])
    return total


def pauli_commutator_mass() -> Fraction:
    """Mass of [X, Z]. The diagonal pair is checked to contribute 0."""
    diagonal_a = ((1, 0), (0, 2))
    diagonal_b = ((3, 0), (0, -1))
    if commutator_mass(diagonal_a, diagonal_b) != 0:
        raise CommutatorError("diagonal observables failed to commute")
    pauli_x = ((0, 1), (1, 0))
    pauli_z = ((1, 0), (0, -1))
    mass = commutator_mass(pauli_x, pauli_z)
    if mass == 0:
        raise CommutatorError("X and Z commuted")
    return mass
