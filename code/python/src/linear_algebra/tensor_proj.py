"""Rational orthogonal projector onto a tensor, and its partial trace.

Origin: code/python/src/linear_algebra/tensor_proj.py
Claim: P = vv^T / (v·v) satisfies P^2 = P and tr(P) = 1, and tr_B(P_A ⊗ P_B) = P_A.
AuthorityEffect: None.
"""
from fractions import Fraction
from typing import Sequence

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class ProjectorError(Exception):
    """A projector vector was zero or not rational."""


def _coords(vector: Sequence[object]):
    if not vector:
        raise ProjectorError("projector vector must be nonempty")
    coords = []
    for value in vector:
        if isinstance(value, GaussianRational):
            raise ProjectorError("tensor projector in this module is over Q, not Q(i)")
        try:
            coords.append(Fraction(value))
        except (TypeError, ValueError) as exc:
            raise ProjectorError(f"entry {value!r} is not rational") from exc
    return coords


def rank_one_projector(vector: Sequence[object]) -> ExactMatrix:
    """Return vv^T / (v·v). The square and the trace are checked before return."""
    coords = _coords(vector)
    norm_sq = sum((coord * coord for coord in coords), Fraction(0))
    if norm_sq == 0:
        raise ProjectorError("projector vector must be nonzero")
    n = len(coords)
    data = [coords[i] * coords[j] / norm_sq for i in range(n) for j in range(n)]
    projector = ExactMatrix(n, n, data)
    if projector * projector != projector:
        raise ProjectorError("rank-one matrix was not idempotent")
    trace = sum((Fraction(projector.get(i, i)) for i in range(n)), Fraction(0))
    if trace != 1:
        raise ProjectorError(f"rank-one projector has trace {trace}, not 1")
    return projector


def partial_trace_b(operator: ExactMatrix, dim_a: int, dim_b: int) -> ExactMatrix:
    """Trace out the right factor of a dim_a * dim_b matrix written in Kronecker order."""
    if dim_a < 1 or dim_b < 1 or operator.rows != dim_a * dim_b or operator.cols != dim_a * dim_b:
        raise ProjectorError("partial trace shape does not match the declared factors")
    data = []
    for i in range(dim_a):
        for j in range(dim_a):
            total = Fraction(0)
            for k in range(dim_b):
                total += Fraction(operator.get(i * dim_b + k, j * dim_b + k))
            data.append(total)
    return ExactMatrix(dim_a, dim_a, data)


def product_projector_trace(left: Sequence[object], right: Sequence[object]) -> Fraction:
    """Trace of tr_B(P(u) ⊗ P(v)) − P(u). It is 0, and the trace of P(u) is 1."""
    from .complex_tensor import kronecker

    p_left = rank_one_projector(left)
    p_right = rank_one_projector(right)
    reduced = partial_trace_b(kronecker(p_left, p_right), p_left.rows, p_right.rows)
    gap = reduced - p_left
    defect = sum((abs(Fraction(entry)) for entry in gap.data), Fraction(0))
    return defect


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "Q",
    "q",
    "ProjectorError",
    "rank_one_projector",
    "partial_trace_b",
    "product_projector_trace",
]
