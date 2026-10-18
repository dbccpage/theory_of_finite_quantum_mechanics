"""Exact triangle edge-cycle whose vertex boundary is zero.

Origin: lean4/FiniteCochain.lean theorem d1_d0_zero. On the standard
triangle the face column (1, -1, 1) is a 1-cycle, so its vertex boundary vanishes.
Claim: urn:omega:fqm:homology:triangle-cycle-boundary:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_chain.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: This file does not prove d1 ∘ d0 = 0 for every cochain. It
certifies the standard triangle cycle and chains built from exact rationals.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

from .boundary import triangle_boundaries
from .errors import DimensionMismatchError

_FACE_CYCLE = (Fraction(1), Fraction(-1), Fraction(1))


def _fail(invariant: str, **parameters: object) -> DimensionMismatchError:
    return DimensionMismatchError(invariant, parameters)


def _rational(value: object, role: str) -> Fraction:
    """Accept int or Fraction only. Float and bool are refused."""
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _require_dim(dim: object) -> int:
    if isinstance(dim, bool) or not isinstance(dim, int) or dim < 0:
        raise _fail("chain dimension must be a nonnegative int", received=type(dim).__name__)
    return dim


def _require_coefficients(values: object, role: str) -> tuple[Fraction, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("coefficients must be a sequence", role=role, received=type(values).__name__)
    return tuple(_rational(item, f"{role}[{index}]") for index, item in enumerate(values))


@dataclass(frozen=True)
class Chain:
    """A finite chain with a nonnegative dimension and exact rational coefficients."""

    dim: int
    coefficients: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        dim = _require_dim(self.dim)
        coefficients = _require_coefficients(self.coefficients, "coeff")
        object.__setattr__(self, "dim", dim)
        object.__setattr__(self, "coefficients", coefficients)

    def total(self) -> Fraction:
        total = Fraction(0)
        for coeff in self.coefficients:
            total += coeff
        return total


def vertex_boundary(edge_coefficients: object) -> tuple[Fraction, ...]:
    """Apply ∂1 of the triangle to a 1-chain on the three edges."""
    parsed = _require_coefficients(edge_coefficients, "edge")
    edge, _face = triangle_boundaries()
    if len(parsed) != edge.cols:
        raise _fail("triangle edge chain has length 3", length=len(parsed), expected=edge.cols)
    image = edge.mul_vec(list(parsed))
    return tuple(_rational(value, f"image[{index}]") for index, value in enumerate(image))


def require_closed_edge_cycle(edge_coefficients: object) -> tuple[Fraction, ...]:
    """Accept the edge chain only when every vertex-boundary entry is zero."""
    image = vertex_boundary(edge_coefficients)
    for index, entry in enumerate(image):
        if entry != 0:
            raise _fail("edge cycle is not closed", index=index, entry=str(entry))
    return image


def face_column() -> tuple[Fraction, ...]:
    """Return the oriented face column stored by the neighboring boundary matrix."""
    _edge, face = triangle_boundaries()
    column = tuple(_rational(entry, f"face[{index}]") for index, entry in enumerate(face.col(0)))
    if column != _FACE_CYCLE:
        raise _fail("face column is not the oriented cycle", column=str(column))
    return column


def face_cycle_boundary() -> tuple[Fraction, ...]:
    """Boundary of ∂[0,1,2] = e01 − e02 + e12. The image is the zero 0-chain."""
    return require_closed_edge_cycle(face_column())


__all__ = [
    "Chain",
    "face_column",
    "face_cycle_boundary",
    "require_closed_edge_cycle",
    "vertex_boundary",
]
