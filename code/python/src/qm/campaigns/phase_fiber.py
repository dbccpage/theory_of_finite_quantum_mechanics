"""Unit product of two frozen Gaussian phases.

Origin: code/rust/src/wdp/connection.rs, which states that phases are exact
Gaussian rationals of modulus one, such as 3/5 + 4/5 i, and gauges a triangle
by 5/13 + 12/13 i.
Claim: urn:omega:fqm:qm:phase-fiber-unit-product:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_phase_fiber.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 2; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 4.
Scope Fence: The product norm is checked in Q(i). This file does not construct
continuum U(1), a cyclic phase group, or a graph connection.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from ...linear_algebra.scalars import GaussianRational


class PhaseFiberError(ValueError):
    """One violated phase-fiber invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> PhaseFiberError:
    return PhaseFiberError(invariant, parameters)


_FIRST: tuple[Fraction, Fraction] = (Fraction(3, 5), Fraction(4, 5))
_SECOND: tuple[Fraction, Fraction] = (Fraction(5, 13), Fraction(12, 13))


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _reject_bool(value: object, role: str) -> None:
    if type(value) is bool:
        raise _fail("boolean refused where an exact rational was required", role=role)


def _exact(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    _reject_bool(value, role)
    if isinstance(value, Fraction):
        return value
    if type(value) is not int:
        raise _fail("phase coordinate is not an exact rational", role=role, received=type(value).__name__)
    return Fraction(value)


def _pair(value: object, role: str) -> tuple[Fraction, Fraction]:
    if isinstance(value, (str, bytes)) or not isinstance(value, tuple) or len(value) != 2:
        raise _fail("phase representative is not a coordinate pair", role=role, received=type(value).__name__)
    return (_exact(value[0], role + "_real"), _exact(value[1], role + "_imag"))


def _require_unit(value: GaussianRational, role: str) -> None:
    norm = value.norm_sq()
    if norm != 1:
        raise _fail("phase representative is not on the unit circle", role=role, norm=str(norm))


def _component(value: object, default: tuple[Fraction, Fraction], role: str) -> GaussianRational:
    pair = default if value is None else _pair(value, role)
    phase = GaussianRational(pair[0], pair[1])
    _require_unit(phase, role)
    return phase


def unit_product(first: object = None, second: object = None) -> Fraction:
    """Norm of the product of the two frozen unit phases, which is 1."""
    left = _component(first, _FIRST, "first")
    right = _component(second, _SECOND, "second")
    product = left * right
    _require_unit(product, "product")
    return product.norm_sq()
