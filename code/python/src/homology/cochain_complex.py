"""A cochain complex whose consecutive coboundary matrices compose to zero.

Origin: lean4/ContextualityObstruction.lean theorem differential_squares_to_zero.
That theorem requires d1 (d0 s) = 0.
Claim: urn:omega:fqm:homology:cochain-complex-square:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_cochain_complex.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: This file certifies only the matrices it is given. It does not
prove differential_squares_to_zero for an arbitrary cochain, and it does not
inherit the Z2 coefficient ring of the Lean source.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence

from ..linear_algebra import ExactMatrix
from .coboundary import triangle_coboundaries
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


def _require_matrix(matrix: object, index: int) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail(
            DimensionMismatchError,
            "cochain complex entries must be exact matrices",
            index=index,
            received=type(matrix).__name__,
        )
    for entry_index, entry in enumerate(matrix.data):
        _rational(entry, f"matrix[{index}][{entry_index}]")
    return matrix


def _product_defect(later: ExactMatrix, earlier: ExactMatrix) -> Fraction:
    if later.cols != earlier.rows:
        raise _fail(
            DimensionMismatchError,
            "coboundary factors do not compose",
            left=later.cols,
            right=earlier.rows,
        )
    product = later * earlier
    defect = Fraction(0)
    for index, entry in enumerate(product.data):
        defect += abs(_rational(entry, f"product[{index}]"))
    return defect


def _require_square(later: ExactMatrix, earlier: ExactMatrix, index: int) -> None:
    defect = _product_defect(later, earlier)
    if defect != 0:
        raise _fail(
            NonZeroCompositionError,
            "consecutive coboundaries do not compose to zero",
            index=index,
            defect=str(defect),
        )


def _require_complex(coboundaries: object) -> tuple[ExactMatrix, ...]:
    if isinstance(coboundaries, (str, bytes)) or not isinstance(coboundaries, Sequence) or len(coboundaries) == 0:
        raise _fail(
            DimensionMismatchError,
            "cochain complex requires a nonempty sequence",
            received=type(coboundaries).__name__,
        )
    matrices = tuple(_require_matrix(item, index) for index, item in enumerate(coboundaries))
    for index in range(len(matrices) - 1):
        _require_square(matrices[index + 1], matrices[index], index)
    return matrices


class CochainComplex:
    """Consecutive exact coboundary matrices with every later-times-earlier product equal to zero."""

    def __init__(self, coboundaries: object) -> None:
        self.coboundaries = _require_complex(coboundaries)


def triangle_cochain_complex() -> CochainComplex:
    """The standard triangle, with δ0 followed by δ1."""
    delta0, delta1 = triangle_coboundaries()
    return CochainComplex((delta0, delta1))


__all__ = [
    "CochainComplex",
    "triangle_cochain_complex",
]
