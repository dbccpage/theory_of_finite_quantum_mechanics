"""Collinear rational boosts and the integer composition trace.

Origin: lean4/BoostComposition.lean theorem composition_trace
(tr3 compositionNumeratorMat = 65) and theorem composition_equals_product.
Claim: urn:omega:fqm:qm:boost-composition-trace:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: composition_trace checks the 3 by 3 numerator product from that
Lean file. composed_velocity checks only the 1+1 velocities 3/5 and 5/13.
This file does not prove a general Lorentz theorem.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_TRACE = 65
_VELOCITY = Fraction(4, 5)


class BoostError(Exception):
    """One violated boost invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> BoostError:
    return BoostError(invariant, parameters)


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


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def _entry3(left: tuple[tuple[int, int, int], ...], right: tuple[tuple[int, int, int], ...], i: int, j: int) -> int:
    return left[i][0] * right[0][j] + left[i][1] * right[1][j] + left[i][2] * right[2][j]


def _row3(left: tuple[tuple[int, int, int], ...], right: tuple[tuple[int, int, int], ...], i: int) -> tuple[int, int, int]:
    return (_entry3(left, right, i, 0), _entry3(left, right, i, 1), _entry3(left, right, i, 2))


def _mul3(left: tuple[tuple[int, int, int], ...], right: tuple[tuple[int, int, int], ...]) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    return (_row3(left, right, 0), _row3(left, right, 1), _row3(left, right, 2))


def _trace3(matrix: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]) -> int:
    return matrix[0][0] + matrix[1][1] + matrix[2][2]


def composition_trace() -> int:
    """Return tr(boostNumeratorMat1 * boostNumeratorMat2), which the Lean file sets to 65."""
    first = ((5, 3, 0), (3, 5, 0), (0, 0, 4))
    second = ((5, 0, 3), (0, 4, 0), (3, 0, 5))
    value = _trace3(_mul3(first, second))
    if value != _TRACE:
        raise _fail("composition trace is not 65", trace=value)
    return value


def _velocity(left: Fraction, right: Fraction) -> Fraction:
    denom = 1 + left * right
    if denom == 0:
        raise _fail("collinear velocities are mutually lightlike", left=str(left), right=str(right))
    return (left + right) / denom


def composed_velocity(left: object | None = None, right: object | None = None) -> Fraction:
    """Return (3/5 ⊕ 5/13) = 4/5, or the same addition for another rational pair."""
    first = Fraction(3, 5) if left is None else _require_fraction(left, "left")
    second = Fraction(5, 13) if right is None else _require_fraction(right, "right")
    return _locked(_velocity(first, second), _VELOCITY if left is None and right is None else _velocity(first, second), "composed velocity drifted")


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Accept only an exact rational probe, then return the composed velocity 4/5."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    trace = composition_trace()
    if trace != _TRACE:
        raise _fail("composition trace is not 65", trace=trace)
    return _locked(composed_velocity(), _VELOCITY, "composed velocity drifted")


def main() -> int:
    value = certify()
    print(value)
    if value == _VELOCITY:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
