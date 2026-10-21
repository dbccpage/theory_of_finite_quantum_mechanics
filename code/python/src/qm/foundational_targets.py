"""Purity of a rational trace-1 density.

Origin: code/python/src/qm/campaigns/foundational_targets.py
Claim: urn:omega:fqm:qm:target-purity:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 8; AST Sonar cognitive complexity max 7; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 8.
Scope Fence: rho = [[1/2, 1/4], [1/4, 1/2]] has trace 1, nonnegative principal
minors, and tr(rho^2) = 5/8. This is not a spectrum oracle.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_PURITY = Fraction(5, 8)


class TargetError(Exception):
    """One violated density invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> TargetError:
    return TargetError(invariant, parameters)


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


def _matrix(value: object) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    if isinstance(value, (str, bytes)) or not isinstance(value, tuple) or len(value) != 2:
        raise _fail("the target density is not 2 by 2", received=type(value).__name__)
    top = value[0]
    bottom = value[1]
    if not isinstance(top, tuple) or not isinstance(bottom, tuple) or len(top) != 2 or len(bottom) != 2:
        raise _fail("a density row is not a pair")
    return (
        (_require_fraction(top[0], "a"), _require_fraction(top[1], "b")),
        (_require_fraction(bottom[0], "c"), _require_fraction(bottom[1], "d")),
    )


def _square_trace(matrix: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    square_00 = matrix[0][0] * matrix[0][0] + matrix[0][1] * matrix[1][0]
    square_11 = matrix[1][0] * matrix[0][1] + matrix[1][1] * matrix[1][1]
    return square_00 + square_11


def purity(matrix: object) -> Fraction:
    """Return tr(rho^2) after the trace, symmetry, and principal-minor checks."""
    entries = _matrix(matrix)
    if entries[0][1] != entries[1][0]:
        raise _fail("the target density is not symmetric")
    trace = entries[0][0] + entries[1][1]
    if trace != 1:
        raise _fail("trace is not 1", trace=str(trace))
    determinant = entries[0][0] * entries[1][1] - entries[0][1] * entries[1][0]
    if entries[0][0] < 0 or determinant < 0:
        raise _fail("a principal minor is negative", leading=str(entries[0][0]), determinant=str(determinant))
    return _square_trace(entries)


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def target_purity() -> Fraction:
    """Purity of [[1/2, 1/4], [1/4, 1/2]]."""
    value = purity(((Fraction(1, 2), Fraction(1, 4)), (Fraction(1, 4), Fraction(1, 2))))
    return _locked(value, _PURITY, "target purity drifted")


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the purity 5/8."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return target_purity()


def main() -> int:
    value = target_purity()
    print(value)
    if value == _PURITY:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
