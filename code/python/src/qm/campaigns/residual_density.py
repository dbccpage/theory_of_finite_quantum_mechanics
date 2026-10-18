"""Residual of a classically correlated state after replacing it by its product marginals.

Origin: code/python/src/qm/campaigns/residual_density.py
Claim: rho = diag(1/2, 0, 0, 1/2) has product marginals I/4, and the trace norm of the residual is 1.
AuthorityEffect: None.
"""
from fractions import Fraction


class ResidualError(Exception):
    """A marginal or the residual trace norm disagreed with the diagonal arithmetic."""


def _partial_trace(diagonal) -> tuple:
    """Diagonal of a 4-vector in order 00, 01, 10, 11. Trace out the right factor, then the left."""
    left = (diagonal[0] + diagonal[1], diagonal[2] + diagonal[3])
    right = (diagonal[0] + diagonal[2], diagonal[1] + diagonal[3])
    return left, right


def residual_trace_norm() -> Fraction:
    state = (Fraction(1, 2), Fraction(0), Fraction(0), Fraction(1, 2))
    left, right = _partial_trace(state)
    if left != (Fraction(1, 2), Fraction(1, 2)) or right != left:
        raise ResidualError(f"marginals {(left, right)} are not both I/2")
    product = tuple(left[i] * right[j] for i in range(2) for j in range(2))
    residual = tuple(state[k] - product[k] for k in range(4))
    trace_norm = sum((abs(entry) for entry in residual), Fraction(0))
    if trace_norm != 1:
        raise ResidualError(f"residual trace norm is {trace_norm}, not 1")
    return trace_norm
