"""Triangle coboundaries, stored as transposes of the boundary matrices.

Origin: lean4/FiniteCochain.lean theorem d1_d0_zero. The coboundary of any
0-cochain has zero circulation around the 2-cell.
Claim: urn:omega:fqm:homology:triangle-coboundary-square:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_coboundary.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: This file certifies the standard triangle coboundaries obtained
as boundary transposes. It does not prove d1 ∘ d0 = 0 for every cochain.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence

from ..linear_algebra import ExactMatrix
from .boundary import triangle_boundaries
from .errors import DimensionMismatchError, HomologyError, NonZeroCompositionError


def _fail(kind: type[HomologyError], invariant: str, **parameters: object) -> HomologyError:
    return kind(invariant, parameters)


def _rational(value: object, role: str) -> Fraction:
    """Accept int or Fraction only. Float and bool are refused."""
    if isinstance(value, float):
        raise _fail(DimensionMismatchError, "float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail(DimensionMismatchError, "boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail(DimensionMismatchError, "value is not an exact rational", role=role, received=type(value).__name__)


def _require_vector(values: object, role: str) -> tuple[Fraction, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail(
            DimensionMismatchError,
            "coboundary cochain must be a sequence",
            role=role,
            received=type(values).__name__,
        )
    return tuple(_rational(item, f"{role}[{index}]") for index, item in enumerate(values))


def _require_matrix(matrix: object) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail(
            DimensionMismatchError,
            "coboundary operator requires an exact matrix",
            received=type(matrix).__name__,
        )
    for index, entry in enumerate(matrix.data):
        _rational(entry, f"matrix[{index}]")
    return matrix


class CoboundaryOperator:
    """Coboundary matrix stored as the transpose of one boundary matrix."""

    def __init__(self, boundary_matrix: object) -> None:
        self.matrix = _require_matrix(boundary_matrix).transpose()

    def apply(self, vec: object) -> tuple[Fraction, ...]:
        parsed = _require_vector(vec, "cochain")
        matrix = self.matrix
        if len(parsed) != matrix.cols:
            raise _fail(
                DimensionMismatchError,
                "coboundary cochain length does not match the operator",
                length=len(parsed),
                expected=matrix.cols,
            )
        image = matrix.mul_vec(list(parsed))
        return tuple(_rational(value, f"image[{index}]") for index, value in enumerate(image))


def triangle_coboundaries() -> tuple[ExactMatrix, ExactMatrix]:
    """Return δ0 = ∂1^T and δ1 = ∂2^T for the standard 2-simplex."""
    edge, face = triangle_boundaries()
    delta0 = CoboundaryOperator(edge).matrix
    delta1 = CoboundaryOperator(face).matrix
    return delta0, delta1


def coboundary_square_defect(delta1: object, delta0: object) -> Fraction:
    """Sum of absolute entries of delta1 * delta0."""
    left = _require_matrix(delta1)
    right = _require_matrix(delta0)
    if left.cols != right.rows:
        raise _fail(
            DimensionMismatchError,
            "coboundary factors do not compose",
            left=left.cols,
            right=right.rows,
        )
    product = left * right
    defect = Fraction(0)
    for index, entry in enumerate(product.data):
        defect += abs(_rational(entry, f"product[{index}]"))
    return defect


def require_coboundary_square(delta1: object, delta0: object) -> Fraction:
    """Accept the pair only when every product entry is zero."""
    defect = coboundary_square_defect(delta1, delta0)
    if defect != 0:
        raise _fail(NonZeroCompositionError, "triangle coboundary square is not zero", defect=str(defect))
    return defect


def triangle_coboundary_defect() -> Fraction:
    """Defect of δ1 δ0 on the standard triangle. The square is the zero 2-cochain."""
    delta0, delta1 = triangle_coboundaries()
    return require_coboundary_square(delta1, delta0)


__all__ = [
    "CoboundaryOperator",
    "coboundary_square_defect",
    "require_coboundary_square",
    "triangle_coboundaries",
    "triangle_coboundary_defect",
]
