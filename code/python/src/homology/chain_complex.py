"""A chain complex whose consecutive boundary matrices compose to zero.

Origin: lean4/CellGrammar.lean structure ChainGrammar field boundarySquare.
That field requires boundary1 (boundary2 face) = zero0.
Claim: urn:omega:fqm:homology:chain-complex-square:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_chain_complex.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 5; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: This file certifies only the matrices it is given. It does not
prove boundarySquare for an arbitrary chain grammar.
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


def _require_matrix(matrix: object, index: int) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail(
            DimensionMismatchError,
            "chain complex entries must be exact matrices",
            index=index,
            received=type(matrix).__name__,
        )
    for entry_index, entry in enumerate(matrix.data):
        _rational(entry, f"matrix[{index}][{entry_index}]")
    return matrix


def _product_defect(left: ExactMatrix, right: ExactMatrix) -> Fraction:
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


def _require_square(left: ExactMatrix, right: ExactMatrix, index: int) -> None:
    defect = _product_defect(left, right)
    if defect != 0:
        raise _fail(
            NonZeroCompositionError,
            "consecutive boundaries do not compose to zero",
            index=index,
            defect=str(defect),
        )


def _require_complex(boundaries: object) -> tuple[ExactMatrix, ...]:
    if isinstance(boundaries, (str, bytes)) or not isinstance(boundaries, Sequence) or len(boundaries) == 0:
        raise _fail(
            DimensionMismatchError,
            "chain complex requires a nonempty sequence",
            received=type(boundaries).__name__,
        )
    matrices = tuple(_require_matrix(item, index) for index, item in enumerate(boundaries))
    for index in range(len(matrices) - 1):
        _require_square(matrices[index], matrices[index + 1], index)
    return matrices


class ChainComplex:
    """Consecutive exact boundary matrices with every product equal to zero."""

    def __init__(self, boundaries: object) -> None:
        self.boundaries = _require_complex(boundaries)


def triangle_chain_complex() -> ChainComplex:
    """The standard triangle, with ∂1 followed by ∂2."""
    edge, face = triangle_boundaries()
    return ChainComplex((edge, face))


__all__ = [
    "ChainComplex",
    "triangle_chain_complex",
]
