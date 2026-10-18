"""Triangle incidence matrices whose boundary square is the zero chain.

Origin: lean4/CellGrammar.lean structure ChainGrammar field boundarySquare.
That field requires boundary1 (boundary2 face) = zero0.
Claim: urn:omega:fqm:homology:triangle-boundary-square:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_boundary.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: This file certifies the standard triangle incidence matrices.
It does not prove boundarySquare for an arbitrary chain grammar.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence

from ..linear_algebra import ExactMatrix
from .errors import DimensionMismatchError, HomologyError, NonZeroCompositionError

_FACE_MIDDLE = Fraction(-1)


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
            "boundary chain must be a sequence",
            role=role,
            received=type(values).__name__,
        )
    return tuple(_rational(item, f"{role}[{index}]") for index, item in enumerate(values))


def _require_matrix(matrix: object) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail(
            DimensionMismatchError,
            "boundary operator requires an exact matrix",
            received=type(matrix).__name__,
        )
    for index, entry in enumerate(matrix.data):
        _rational(entry, f"matrix[{index}]")
    return matrix


class BoundaryOperator:
    """One exact boundary matrix. apply refuses a chain of the wrong length."""

    def __init__(self, matrix: object) -> None:
        self.matrix = _require_matrix(matrix)

    def apply(self, vec: object) -> tuple[Fraction, ...]:
        parsed = _require_vector(vec, "chain")
        matrix = self.matrix
        if len(parsed) != matrix.cols:
            raise _fail(
                DimensionMismatchError,
                "boundary chain length does not match the operator",
                length=len(parsed),
                expected=matrix.cols,
            )
        image = matrix.mul_vec(list(parsed))
        return tuple(_rational(value, f"image[{index}]") for index, value in enumerate(image))


def triangle_boundaries() -> tuple[ExactMatrix, ExactMatrix]:
    """Return ∂1 (vertices × edges) and ∂2 (edges × one face) for the standard 2-simplex."""
    edge = ExactMatrix.from_rows(
        [
            [Fraction(-1), Fraction(-1), Fraction(0)],
            [Fraction(1), Fraction(0), Fraction(-1)],
            [Fraction(0), Fraction(1), Fraction(1)],
        ]
    )
    face = ExactMatrix.from_rows(
        [
            [Fraction(1)],
            [_FACE_MIDDLE],
            [Fraction(1)],
        ]
    )
    return _require_matrix(edge), _require_matrix(face)


def boundary_square_defect(edge: object, face: object) -> Fraction:
    """Sum of absolute entries of edge * face."""
    left = _require_matrix(edge)
    right = _require_matrix(face)
    if left.cols != right.rows:
        raise _fail(
            DimensionMismatchError,
            "boundary factors do not compose",
            left=left.cols,
            right=right.rows,
        )
    product = left * right
    defect = Fraction(0)
    for index, entry in enumerate(product.data):
        defect += abs(_rational(entry, f"product[{index}]"))
    return defect


def require_boundary_square(edge: object, face: object) -> Fraction:
    """Accept the pair only when every product entry is zero."""
    defect = boundary_square_defect(edge, face)
    if defect != 0:
        raise _fail(NonZeroCompositionError, "triangle boundary square is not zero", defect=str(defect))
    return defect


def triangle_boundary_defect() -> Fraction:
    """Defect of ∂1 ∂2 on the standard triangle. The oriented square is zero."""
    edge, face = triangle_boundaries()
    return require_boundary_square(edge, face)


__all__ = [
    "BoundaryOperator",
    "boundary_square_defect",
    "require_boundary_square",
    "triangle_boundaries",
    "triangle_boundary_defect",
]
