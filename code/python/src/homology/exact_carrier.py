"""Betti count of the filled triangle carrier over the rationals.

Origin: lean4/FiniteCochain.lean theorem d1_d0_zero. That theorem requires
d1 (d0 a) = 0 on the 3-vertex, 3-edge, 1-face cochain.
Claim: urn:omega:fqm:homology:filled-triangle-betti:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_exact_carrier.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: The Lean theorem proves the circulation identity, not these
integer ranks. This file reports rank(d0), rank(d1), and dim H1 for the
coboundary matrices from triangle_coboundaries. It does not prove the Betti
numbers of every cochain. ExactCarrier is the Carrier alias and adds no
authority.
"""

from __future__ import annotations

from fractions import Fraction

from .carrier import Carrier
from .coboundary import triangle_coboundaries
from .errors import DimensionMismatchError, HomologyError


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


def _require_carrier(carrier: object) -> Carrier:
    if not isinstance(carrier, Carrier):
        raise _fail(
            DimensionMismatchError,
            "triangle Betti expects a carrier",
            received=type(carrier).__name__,
        )
    for index, entry in enumerate(carrier.d0.data):
        _rational(entry, f"d0[{index}]")
    for index, entry in enumerate(carrier.d1.data):
        _rational(entry, f"d1[{index}]")
    return carrier


def _require_dimensions(carrier: Carrier) -> None:
    dim0, dim1, dim2 = carrier.dimensions()
    if (dim0, dim1, dim2) != (3, 3, 1):
        raise _fail(
            DimensionMismatchError,
            "triangle carrier dimensions are not (3, 3, 1)",
            dim0=dim0,
            dim1=dim1,
            dim2=dim2,
        )


def _require_triple(rank0: int, rank1: int, betti: int) -> tuple[int, int, int]:
    if rank0 != 2 or rank1 != 1 or betti != 0:
        raise _fail(
            DimensionMismatchError,
            "triangle Betti triple is not (2, 1, 0)",
            rank0=rank0,
            rank1=rank1,
            betti=betti,
        )
    return (rank0, rank1, betti)


ExactCarrier = Carrier


def triangle_carrier() -> Carrier:
    """Coboundary matrices of the 2-simplex, in the Carrier shape convention."""
    delta0, delta1 = triangle_coboundaries()
    return Carrier(3, 3, 1, delta0, delta1)


def require_triangle_betti(carrier: object) -> tuple[int, int, int]:
    """Return (2, 1, 0) only when the carrier's measured triple is that value."""
    checked = _require_carrier(carrier)
    _require_dimensions(checked)
    return _require_triple(checked.rank_d0(), checked.rank_d1(), checked.dim_h1())


def triangle_betti() -> tuple[int, int, int]:
    """Return (rank d0, rank d1, dim H1) for the filled triangle."""
    return require_triangle_betti(triangle_carrier())


__all__ = [
    "ExactCarrier",
    "require_triangle_betti",
    "triangle_betti",
    "triangle_carrier",
]
