"""Basic exact matrix alias, plus the trace of an identity.

Origin: code/python/src/linear_algebra/basic_matrix.py
Claim: the trace of the n by n identity, summed on the diagonal, equals n.
AuthorityEffect: None.
"""
from fractions import Fraction

from .matrix import ExactMatrix, MatrixError


def identity_trace(n: int) -> Fraction:
    """Sum the diagonal of the rational identity of size n."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise MatrixError(f"identity size must be a nonnegative int, got {n!r}")
    eye = ExactMatrix.identity(n)
    total = Fraction(0)
    for i in range(n):
        total += Fraction(eye.get(i, i))
    if total != Fraction(n):
        raise MatrixError(f"identity trace {total} is not the dimension {n}")
    return total


__all__ = ["ExactMatrix", "MatrixError", "identity_trace"]
