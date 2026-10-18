"""Moore–Penrose pseudoinverse of a rational matrix via a full-rank factorization.

Origin: code/python/src/linear_algebra/pseudoinverse.py
Claim: A = F G from the pivot columns and the RREF, and A A+ A = A over Q.
AuthorityEffect: None. The four Penrose identities are checked for the matrix that was passed.
"""
from fractions import Fraction

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class PseudoinverseError(Exception):
    """The pseudoinverse could not be built over Q."""


def _rational(matrix: ExactMatrix) -> ExactMatrix:
    data = []
    for value in matrix.data:
        if isinstance(value, GaussianRational):
            raise PseudoinverseError("pseudoinverse in this module is over Q, not Q(i)")
        try:
            data.append(Fraction(value))
        except (TypeError, ValueError) as exc:
            raise PseudoinverseError(f"entry {value!r} is not rational") from exc
    return ExactMatrix(matrix.rows, matrix.cols, data)


def moore_penrose(matrix: ExactMatrix) -> ExactMatrix:
    """Return A+ in Q^{n×m} for A in Q^{m×n}."""
    source = _rational(matrix)
    m, n = source.rows, source.cols
    reduced, pivots = source.rref()
    rank = len(pivots)
    if rank == 0:
        return ExactMatrix.zeros(n, m)
    factor_f = ExactMatrix.from_rows([[source.get(i, pivot) for pivot in pivots] for i in range(m)])
    factor_g = ExactMatrix.from_rows([[Fraction(entry) for entry in reduced.row(row)] for row in range(rank)])
    if factor_f * factor_g != source:
        raise PseudoinverseError("pivot factorization does not rebuild the matrix")
    gram_f = factor_f.transpose() * factor_f
    gram_g = factor_g * factor_g.transpose()
    try:
        inverse_f = gram_f.inverse()
        inverse_g = gram_g.inverse()
    except ValueError as exc:
        raise PseudoinverseError("a full-rank Gram matrix was singular") from exc
    pseudo = factor_g.transpose() * inverse_g * inverse_f * factor_f.transpose()
    if source * pseudo * source != source:
        raise PseudoinverseError("Penrose identity A A+ A = A failed")
    if pseudo * source * pseudo != pseudo:
        raise PseudoinverseError("Penrose identity A+ A A+ = A+ failed")
    left_proj = source * pseudo
    right_proj = pseudo * source
    if left_proj.transpose() != left_proj or right_proj.transpose() != right_proj:
        raise PseudoinverseError("a Penrose projector was not symmetric")
    return pseudo


__all__ = ["ExactMatrix", "GaussianRational", "Q", "q", "PseudoinverseError", "moore_penrose"]
