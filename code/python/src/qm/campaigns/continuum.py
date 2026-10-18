"""Finite trace obstruction to the continuum canonical commutation relation.

Origin: code/python/src/qm/campaigns/continuum.py
Claim: tr(XP − PX) computed by matrix multiplication is 0 in every finite dimension.
AuthorityEffect: None. The file does not construct an infinite-dimensional representation.
"""
from fractions import Fraction


class ContinuumError(Exception):
    """The dimension was not a positive integer."""


def commutator_trace(dimension: int) -> Fraction:
    """Trace of [N, S] where S is the nilpotent shift and N is the diagonal of weights 0..d-1."""
    if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension < 1:
        raise ContinuumError(f"dimension must be a positive int, got {dimension!r}")
    trace = Fraction(0)
    for i in range(dimension):
        diagonal = Fraction(0)
        for k in range(dimension):
            number = Fraction(i) if i == k else Fraction(0)
            shift_ki = Fraction(1) if k == i + 1 else Fraction(0)
            shift_ik = Fraction(1) if i == k + 1 else Fraction(0)
            weight_ki = Fraction(k) if k == i else Fraction(0)
            diagonal += number * shift_ki - shift_ik * weight_ki
        trace += diagonal
    return trace


def trace_obstruction(dimension: int = 4) -> Fraction:
    """Return the dimension when the commutator trace vanishes, else raise."""
    trace = commutator_trace(dimension)
    if trace != 0:
        raise ContinuumError(f"finite commutator trace is {trace}, not 0")
    return Fraction(dimension)
