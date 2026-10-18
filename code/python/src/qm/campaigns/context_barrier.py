"""A context barrier is a pair of contexts whose union does not commute.

Origin: code/python/src/qm/campaigns/context_barrier.py
Claim: {Z⊗I, I⊗Z} and {X⊗X} are separately commuting contexts, and Z⊗I fails to commute with X⊗X.
AuthorityEffect: None.
"""
from fractions import Fraction

from .commuting_obs import commutator_mass


class ContextBarrierError(Exception):
    """A declared context was not commuting, or the barrier pair commuted."""


def _kron(left, right):
    rows = []
    for i in range(len(left)):
        for k in range(len(right)):
            row = []
            for j in range(len(left[0])):
                for ell in range(len(right[0])):
                    row.append(Fraction(left[i][j]) * Fraction(right[k][ell]))
            rows.append(tuple(row))
    return tuple(rows)


def barrier_mass() -> Fraction:
    """Commutator mass across the two contexts. Within each context the mass is 0."""
    z = ((1, 0), (0, -1))
    x = ((0, 1), (1, 0))
    eye = ((1, 0), (0, 1))
    context_a = (_kron(z, eye), _kron(eye, z))
    context_b = (_kron(x, x),)
    if commutator_mass(context_a[0], context_a[1]) != 0:
        raise ContextBarrierError("the Z context does not commute")
    mass = commutator_mass(context_a[0], context_b[0])
    if mass == 0:
        raise ContextBarrierError("the contexts commute, so there is no barrier")
    return mass
