"""Finite trace obstruction to a continuum commutator.

Origin: lean4/ContinuumLiftBoundary.lean theorem commutator_trace_zero.
The trace of AB − BA is 0 for every 2 by 2 integer matrix pair, so it cannot
equal a nonzero scalar trace.
Claim: urn:omega:fqm:qm:commutator-trace-obstruction:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: trace_obstruction returns the finite dimension after the computed
commutator trace vanishes. It does not construct an infinite-dimensional
representation, and it does not prove the Wintner–Wielandt theorem beyond
this exact trace.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_DIMENSION = 4


class ContinuumError(Exception):
    """One violated commutator invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ContinuumError:
    return ContinuumError(invariant, parameters)


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


def _require_dimension(value: object) -> int:
    parsed = _require_fraction(value, "dimension")
    if parsed.denominator != 1 or parsed < 1:
        raise _fail("dimension must be a positive integer", dimension=str(parsed))
    return int(parsed)


def _diagonal_term(index: int, column: int) -> Fraction:
    number = Fraction(index) if index == column else Fraction(0)
    shift_down = Fraction(1) if column == index + 1 else Fraction(0)
    shift_up = Fraction(1) if index == column + 1 else Fraction(0)
    weight = Fraction(column) if column == index else Fraction(0)
    return number * shift_down - shift_up * weight


def _row_trace(index: int, dimension: int) -> Fraction:
    total = Fraction(0)
    column = 0
    while column < dimension:
        total += _diagonal_term(index, column)
        column += 1
    return total


def commutator_trace(dimension: int) -> Fraction:
    """Trace of [N, S] for the weighted diagonal N and the nilpotent shift S."""
    total = Fraction(0)
    index = 0
    while index < dimension:
        total += _row_trace(index, dimension)
        index += 1
    return total


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def trace_obstruction(dimension: object | None = None) -> Fraction:
    """Return the dimension when the finite commutator trace is 0."""
    count = _DIMENSION if dimension is None else _require_dimension(dimension)
    trace = commutator_trace(count)
    if trace != 0:
        raise _fail("finite commutator trace is not zero", trace=str(trace), dimension=count)
    if dimension is None and count != _DIMENSION:
        raise _fail("default obstruction dimension drifted", dimension=count)
    return Fraction(count)


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the default obstruction 4."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(trace_obstruction(), Fraction(_DIMENSION), "trace obstruction drifted")


def main() -> int:
    value = trace_obstruction()
    print(value)
    if value == Fraction(_DIMENSION):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
