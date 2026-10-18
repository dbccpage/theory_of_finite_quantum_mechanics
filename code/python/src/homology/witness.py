"""Recomputed witness that a carrier square vanishes and dim H1 matches rank-nullity.

Origin: lean4/FiniteCochain.lean theorem d1_d0_zero. The witness recomputes
that square on the carrier matrices and the rank-nullity count of dim H1.
Claim: urn:omega:fqm:homology:witness-rank-nullity:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_witness.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: A witness recomputes one carrier. It does not prove d1_d0_zero
for every cochain. A hand-built HomologyWitness is not a certificate, and the
digest is not an authority grant.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from fractions import Fraction

from ..linear_algebra import ExactMatrix
from .carrier import Carrier
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
            "witness entries must be exact matrices",
            role=role,
            received=type(matrix).__name__,
        )
    if matrix.rows != rows or matrix.cols != cols:
        raise _fail(
            DimensionMismatchError,
            "witness matrix shape does not match dimensions",
            role=role,
            rows=matrix.rows,
            cols=matrix.cols,
            expected_rows=rows,
            expected_cols=cols,
        )
    for index, entry in enumerate(matrix.data):
        _rational(entry, f"{role}[{index}]")
    return matrix


def _require_carrier(carrier: object) -> Carrier:
    if not isinstance(carrier, Carrier):
        raise _fail(
            DimensionMismatchError,
            "witness expects a carrier",
            received=type(carrier).__name__,
        )
    dim0 = _dimension(carrier.dim0, "dim0")
    dim1 = _dimension(carrier.dim1, "dim1")
    dim2 = _dimension(carrier.dim2, "dim2")
    _require_matrix(carrier.d0, "d0", dim1, dim0)
    _require_matrix(carrier.d1, "d1", dim2, dim1)
    return carrier


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
            "witness coboundaries do not compose to zero",
            defect=str(defect),
        )


def _homology_dimension(dim1: int, rank0: int, rank1: int) -> int:
    return (dim1 - rank1) - rank0


def _digest(dim0: int, dim1: int, dim2: int, d0: ExactMatrix, d1: ExactMatrix) -> str:
    digest = hashlib.sha256()
    digest.update(f"{dim0},{dim1},{dim2}:".encode("utf-8"))
    digest.update(d0.sha256().encode("utf-8"))
    digest.update(d1.sha256().encode("utf-8"))
    return digest.hexdigest()


@dataclass(frozen=True)
class HomologyWitness:
    """Receipt of a recomputed carrier square, rank-nullity count, and digest."""

    carrier_hash: str
    dim_q1: int
    dim_h1: int
    is_valid: bool

    @classmethod
    def from_carrier(cls, carrier: object) -> "HomologyWitness":
        checked = _require_carrier(carrier)
        _require_square(checked.d1, checked.d0)
        rank0 = checked.d0.rank()
        rank1 = checked.d1.rank()
        dim_q1 = checked.dim1 - rank0
        dim_h1 = _homology_dimension(checked.dim1, rank0, rank1)
        if dim_h1 != checked.dim_h1() or dim_q1 != checked.dim_q1():
            raise _fail(
                DimensionMismatchError,
                "witness rank-nullity does not match the carrier",
                dim_h1=dim_h1,
                carrier_h1=checked.dim_h1(),
                dim_q1=dim_q1,
                carrier_q1=checked.dim_q1(),
            )
        digest = _digest(checked.dim0, checked.dim1, checked.dim2, checked.d0, checked.d1)
        if digest != checked.sha256():
            raise _fail(DimensionMismatchError, "witness digest does not match the carrier")
        return cls(carrier_hash=digest, dim_q1=dim_q1, dim_h1=dim_h1, is_valid=True)


__all__ = ["HomologyWitness"]
