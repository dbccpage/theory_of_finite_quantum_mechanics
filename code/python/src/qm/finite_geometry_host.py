"""The Fano plane as a host geometry.

Origin: code/python/src/qm/campaigns/finite_geometry_host.py
Claim: urn:omega:fqm:qm:fano-incidence-defect:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: Seven lines are enumerated. Every point lies on 3 lines and every
pair lies on exactly one line. No projective-plane classification is claimed.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_DEFECT = Fraction(0)
FANO_LINES = (
    frozenset({0, 1, 2}),
    frozenset({0, 3, 4}),
    frozenset({0, 5, 6}),
    frozenset({1, 3, 5}),
    frozenset({1, 4, 6}),
    frozenset({2, 3, 6}),
    frozenset({2, 4, 5}),
)


class FanoError(Exception):
    """One violated incidence invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> FanoError:
    return FanoError(invariant, parameters)


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


def _require_point(value: object) -> int:
    parsed = _require_fraction(value, "point")
    if parsed.denominator != 1 or parsed < 0 or parsed > 6:
        raise _fail("Fano point is outside 0..6", point=str(parsed))
    return int(parsed)


def lines_through(point: object) -> int:
    """How many of the seven lines contain the point."""
    slot = _require_point(point)
    count = 0
    for line in FANO_LINES:
        if slot in line:
            count += 1
    return count


def pair_line_count(left: object, right: object) -> int:
    """How many lines contain both points."""
    pair = frozenset({_require_point(left), _require_point(right)})
    count = 0
    for line in FANO_LINES:
        if pair <= line:
            count += 1
    return count


def _point_defect() -> int:
    defect = 0
    point = 0
    while point < 7:
        defect += abs(lines_through(point) - 3)
        point += 1
    return defect


def _pair_row(left: int) -> int:
    defect = 0
    right = left + 1
    while right < 7:
        defect += abs(pair_line_count(left, right) - 1)
        right += 1
    return defect


def _pair_defect() -> int:
    defect = 0
    left = 0
    while left < 7:
        defect += _pair_row(left)
        left += 1
    return defect


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def fano_incidence_defect() -> Fraction:
    """Zero when every point has 3 lines and every pair has one line."""
    defect = _point_defect() + _pair_defect()
    if len(FANO_LINES) != 7:
        raise _fail("Fano line count drifted", lines=len(FANO_LINES))
    return _locked(Fraction(defect), _DEFECT, "Fano incidence defect drifted")


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the incidence defect 0."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return fano_incidence_defect()


def main() -> int:
    value = fano_incidence_defect()
    print(value)
    if value == _DEFECT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
