"""Exact carrier: two rational coboundaries with d1 ∘ d0 = 0.

Origin: lean4/CellGrammar.lean structure Dualization and theorem
boundarySquare_implies_cochain. That theorem requires d1 (d0 alpha) = zero.
Claim: urn:omega:fqm:homology:carrier-coboundary-square:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_carrier.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: This file certifies only the matrices it is given. It does not
prove boundarySquare_implies_cochain for an arbitrary dualization, and it does
not inherit a homology or topology theorem from CellGrammar. dim H1 is the
rank-nullity count on these matrices. The digest commits to dimensions and
matrix entries, not to weights, and it is not an authority grant.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from typing import Sequence

from ..linear_algebra import ExactMatrix
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


def _dimension(value: object, role: str) -> int:
    if type(value) is bool:
        raise _fail(DimensionMismatchError, "boolean refused where a dimension was required", role=role)
    if type(value) is not int:
        raise _fail(
            DimensionMismatchError,
            "dimension is not an integer",
            role=role,
            received=type(value).__name__,
        )
    if value < 0:
        raise _fail(DimensionMismatchError, "dimension is negative", role=role, received=value)
    return value


def _require_matrix(matrix: object, role: str, rows: int, cols: int) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail(
            DimensionMismatchError,
            "carrier entries must be exact matrices",
            role=role,
            received=type(matrix).__name__,
        )
    if matrix.rows != rows or matrix.cols != cols:
        raise _fail(
            DimensionMismatchError,
            "carrier matrix shape does not match dimensions",
            role=role,
            rows=matrix.rows,
            cols=matrix.cols,
            expected_rows=rows,
            expected_cols=cols,
        )
    for index, entry in enumerate(matrix.data):
        _rational(entry, f"{role}[{index}]")
    return matrix


def _product_defect(later: ExactMatrix, earlier: ExactMatrix) -> Fraction:
    product = later * earlier
    defect = Fraction(0)
    for index, entry in enumerate(product.data):
        defect += abs(_rational(entry, f"product[{index}]"))
    return defect


def _require_square(later: ExactMatrix, earlier: ExactMatrix) -> None:
    defect = _product_defect(later, earlier)
    if defect != 0:
        raise _fail(
            NonZeroCompositionError,
            "carrier coboundaries do not compose to zero",
            defect=str(defect),
        )


def _require_weights(weights: object) -> tuple[Fraction, ...] | None:
    if weights is None:
        return None
    if isinstance(weights, (str, bytes)) or not isinstance(weights, Sequence):
        raise _fail(
            DimensionMismatchError,
            "carrier weights must be a sequence",
            received=type(weights).__name__,
        )
    return tuple(_rational(item, f"weight[{index}]") for index, item in enumerate(weights))


class Carrier:
    """Rational coboundary pair d0 : C0 → C1, d1 : C1 → C2, with d1 ∘ d0 = 0."""

    __slots__ = ("dim0", "dim1", "dim2", "d0", "d1", "weights")

    def __init__(
        self,
        dim0: object,
        dim1: object,
        dim2: object,
        d0: object,
        d1: object,
        weights: object = None,
    ) -> None:
        checked0 = _dimension(dim0, "dim0")
        checked1 = _dimension(dim1, "dim1")
        checked2 = _dimension(dim2, "dim2")
        checked_d0 = _require_matrix(d0, "d0", checked1, checked0)
        checked_d1 = _require_matrix(d1, "d1", checked2, checked1)
        _require_square(checked_d1, checked_d0)
        self.dim0 = checked0
        self.dim1 = checked1
        self.dim2 = checked2
        self.d0 = checked_d0
        self.d1 = checked_d1
        self.weights = _require_weights(weights)

    def dimensions(self) -> tuple[int, int, int]:
        return (self.dim0, self.dim1, self.dim2)

    def rank_d0(self) -> int:
        return self.d0.rank()

    def rank_d1(self) -> int:
        return self.d1.rank()

    def dim_q1(self) -> int:
        return self.dim1 - self.rank_d0()

    def dim_h1(self) -> int:
        return (self.dim1 - self.rank_d1()) - self.rank_d0()

    def sha256(self) -> str:
        digest = hashlib.sha256()
        digest.update(f"{self.dim0},{self.dim1},{self.dim2}:".encode("utf-8"))
        digest.update(self.d0.sha256().encode("utf-8"))
        digest.update(self.d1.sha256().encode("utf-8"))
        return digest.hexdigest()


__all__ = ["Carrier"]
