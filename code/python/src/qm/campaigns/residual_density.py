"""Residual of a classically correlated state against its product marginals.

Origin: code/python/src/qm/campaigns/residual_density.py
Claim: urn:omega:fqm:qm:residual-trace-norm:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: The state is diag(1/2, 0, 0, 1/2). Product marginals are I/4 and
the trace norm of the residual is 1. No continuity or entropy theorem is claimed.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_NORM = Fraction(1)


class ResidualError(Exception):
    """One violated residual invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ResidualError:
    return ResidualError(invariant, parameters)


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


def _partial(diagonal: tuple[Fraction, Fraction, Fraction, Fraction]) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    left = (diagonal[0] + diagonal[1], diagonal[2] + diagonal[3])
    right = (diagonal[0] + diagonal[2], diagonal[1] + diagonal[3])
    return left, right


def _product(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return (left[0] * right[0], left[0] * right[1], left[1] * right[0], left[1] * right[1])


def _trace_norm(residual: tuple[Fraction, Fraction, Fraction, Fraction]) -> Fraction:
    return abs(residual[0]) + abs(residual[1]) + abs(residual[2]) + abs(residual[3])


def residual_trace_norm() -> Fraction:
    """Trace norm of rho minus the product of its marginals."""
    state = (_require_fraction(1, "s0") / _require_fraction(2, "s1"), Fraction(0), Fraction(0), Fraction(1, 2))
    left, right = _partial(state)
    if left != (Fraction(1, 2), Fraction(1, 2)) or right != left:
        raise _fail("marginals are not both I/2", left=str(left), right=str(right))
    product = _product(left, right)
    residual = (state[0] - product[0], state[1] - product[1], state[2] - product[2], state[3] - product[3])
    return _trace_norm(residual)


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the residual trace norm 1."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(residual_trace_norm(), _NORM, "residual trace norm drifted")


def main() -> int:
    value = residual_trace_norm()
    print(value)
    if value == _NORM:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
