"""Additive carrier on a triangle.

Origin: code/python/src/qm/campaigns/carrier.py
Claim: urn:omega:fqm:qm:triangle-carrier-curvature:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: Curvature is the oriented sum of three edge weights. A constant
weight 1 has curvature 3. This file does not compute homology ranks.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_FLAT = Fraction(0)


class CarrierCurvatureError(Exception):
    """One violated carrier invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CarrierCurvatureError:
    return CarrierCurvatureError(invariant, parameters)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def curvature(weights: object) -> Fraction:
    """Sum of the three oriented edge weights around the face."""
    if isinstance(weights, (str, bytes)) or not isinstance(weights, tuple) or len(weights) != 3:
        raise _fail("triangle carrier needs 3 edges", received=type(weights).__name__)
    total = _require_fraction(weights[0], "edge0")
    total += _require_fraction(weights[1], "edge1")
    total += _require_fraction(weights[2], "edge2")
    return total


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def flat_carrier_curvature() -> Fraction:
    """Curvature of the connection whose third edge closes the first two."""
    first = Fraction(2, 3)
    second = Fraction(-1, 5)
    closed = curvature((first, second, -(first + second)))
    return _locked(closed, _FLAT, "closing edge left curvature")


def constant_weight_curvature() -> Fraction:
    """Curvature of the constant weight 1 on three edges."""
    return curvature((_require_fraction(1, "w0"), _require_fraction(1, "w1"), _require_fraction(1, "w2")))


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the flat curvature 0."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    if constant_weight_curvature() != 3:
        raise _fail("constant weight curvature is not 3")
    return flat_carrier_curvature()


def main() -> int:
    value = flat_carrier_curvature()
    print(value)
    if value == _FLAT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
