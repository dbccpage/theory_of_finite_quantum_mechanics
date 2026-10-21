"""Squared overlap of two rational orthonormal frames.

Origin: code/python/src/qm/campaigns/mub_reports.py
Claim: urn:omega:fqm:qm:mub-overlap-gap:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: The coordinate basis and the (3, 4, 5) frame have maximum squared
overlap 16/25. The gap against the unbiased value 1/2 is -7/50. Dimension 2
has no pair of rational mutually unbiased bases. This file does not prove that
absence beyond the reported gap.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_GAP = Fraction(1, 2) - Fraction(16, 25)


class MubReportError(Exception):
    """One violated frame invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> MubReportError:
    return MubReportError(invariant, parameters)


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


def _dot(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _max_square(left: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], right: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    squares = (
        _dot(left[0], right[0]) ** 2,
        _dot(left[0], right[1]) ** 2,
        _dot(left[1], right[0]) ** 2,
        _dot(left[1], right[1]) ** 2,
    )
    best = squares[0]
    if squares[1] > best:
        best = squares[1]
    if squares[2] > best:
        best = squares[2]
    if squares[3] > best:
        best = squares[3]
    return best


def _parseval(left: tuple[Fraction, Fraction], right: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return _dot(left, right[0]) ** 2 + _dot(left, right[1]) ** 2 - _dot(left, left)


def overlap_gap() -> Fraction:
    """Unbiased value 1/2 minus the maximum squared overlap."""
    coordinate = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    pythagorean = (
        (_require_fraction(3, "p0") / _require_fraction(5, "p1"), _require_fraction(4, "p2") / _require_fraction(5, "p3")),
        (Fraction(-4, 5), Fraction(3, 5)),
    )
    if _dot(coordinate[0], coordinate[1]) != 0 or _dot(pythagorean[0], pythagorean[1]) != 0:
        raise _fail("a reported frame is not orthogonal")
    overlap = _max_square(coordinate, pythagorean)
    defect = _parseval(coordinate[0], pythagorean) + _parseval(coordinate[1], pythagorean)
    if defect != 0:
        raise _fail("Parseval defect is not zero", defect=str(defect))
    return Fraction(1, 2) - overlap


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the overlap gap -7/50."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(overlap_gap(), _GAP, "overlap gap drifted")


def main() -> int:
    value = overlap_gap()
    print(value)
    if value == _GAP:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
