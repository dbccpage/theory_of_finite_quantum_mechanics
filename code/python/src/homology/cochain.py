"""Exact cochains, their evaluation pairing, and the triangle coboundary square.

Origin: lean4/TriangleNetworkComplexCarrier.lean theorems
eval_pairing_left_additive and eval_pairing_right_additive. The evaluation
pairing is additive in the chain and in the cochain.
Claim: urn:omega:fqm:homology:triangle-cochain-pairing:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_cochain.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: This file certifies equal-length exact rational sequences and
the standard triangle square. It does not prove the 5-edge diamond pairing.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

from .chain import Chain
from .coboundary import triangle_coboundaries
from .errors import DimensionMismatchError


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
        raise _fail("cochain dimension must be a nonnegative int", received=type(dim).__name__)
    return dim


def _require_coefficients(values: object, role: str) -> tuple[Fraction, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("coefficients must be a sequence", role=role, received=type(values).__name__)
    return tuple(_rational(item, f"{role}[{index}]") for index, item in enumerate(values))


@dataclass(frozen=True)
class Cochain:
    """A finite cochain with a nonnegative dimension and exact rational coefficients."""

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


def _require_same_slot(cochain: Cochain, chain: Chain) -> None:
    if cochain.dim != chain.dim:
        raise _fail(
            "cochain and chain dimensions differ",
            cochain_dim=cochain.dim,
            chain_dim=chain.dim,
        )
    if len(cochain.coefficients) != len(chain.coefficients):
        raise _fail(
            "cochain and chain lengths differ",
            cochain_length=len(cochain.coefficients),
            chain_length=len(chain.coefficients),
        )


def pairing(cochain: Cochain, chain: Chain) -> Fraction:
    """Sum alpha_i c_i. The arguments must share dimension and length."""
    _require_same_slot(cochain, chain)
    total = Fraction(0)
    for alpha, coeff in zip(cochain.coefficients, chain.coefficients):
        total += alpha * coeff
    return total


def coboundary_values(vertex_values: object) -> list[Fraction]:
    """δ0 of a 0-cochain on the three vertices of the triangle."""
    parsed = _require_coefficients(vertex_values, "vertex")
    delta0, _delta1 = triangle_coboundaries()
    if len(parsed) != delta0.cols:
        raise _fail("triangle 0-cochain has length 3", length=len(parsed), expected=delta0.cols)
    image = delta0.mul_vec(list(parsed))
    return [_rational(value, f"edge[{index}]") for index, value in enumerate(image)]


def coboundary_square(vertex_values: object) -> list[Fraction]:
    """δ1 δ0 of a 0-cochain. The single face component is computed, not stored."""
    _delta0, delta1 = triangle_coboundaries()
    edge_values = coboundary_values(vertex_values)
    image = delta1.mul_vec(edge_values)
    return [_rational(value, f"face[{index}]") for index, value in enumerate(image)]


__all__ = [
    "Cochain",
    "coboundary_square",
    "coboundary_values",
    "pairing",
]
