"""A quadratic frame function on two coordinate frames in dimension 3.

Origin: code/python/src/qm/campaigns/gleason.py
Claim: urn:omega:fqm:qm:gleason-frame-gap:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: For v = (1/3, 2/3, 2/3), the coordinate frame and a coordinate
permutation assign the same sum 1. This is not Gleason's classification.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_GAP = Fraction(0)


class GleasonError(Exception):
    """One violated frame invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> GleasonError:
    return GleasonError(invariant, parameters)


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


def _dot(left: tuple[Fraction, Fraction, Fraction], right: tuple[Fraction, Fraction, Fraction]) -> Fraction:
    return left[0] * right[0] + left[1] * right[1] + left[2] * right[2]


def _frame_total(vector: tuple[Fraction, Fraction, Fraction], frame: tuple[tuple[Fraction, Fraction, Fraction], tuple[Fraction, Fraction, Fraction], tuple[Fraction, Fraction, Fraction]]) -> Fraction:
    first = _dot(vector, frame[0])
    second = _dot(vector, frame[1])
    third = _dot(vector, frame[2])
    return first * first + second * second + third * third


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def gleason_frame_gap() -> Fraction:
    """Difference of the two frame totals. Both totals equal 1."""
    vector = (Fraction(1, 3), Fraction(2, 3), Fraction(2, 3))
    if _dot(vector, vector) != 1:
        raise _fail("the witness vector is not a unit vector", norm=str(_dot(vector, vector)))
    one = _require_fraction(1, "one")
    zero = _require_fraction(0, "zero")
    coordinate = ((one, zero, zero), (zero, one, zero), (zero, zero, one))
    permuted = (coordinate[1], coordinate[2], coordinate[0])
    left = _frame_total(vector, coordinate)
    right = _frame_total(vector, permuted)
    if left != 1 or right != 1:
        raise _fail("frame totals are not both 1", left=str(left), right=str(right))
    return _locked(left - right, _GAP, "Gleason frame gap drifted")


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the frame gap 0."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return gleason_frame_gap()


def main() -> int:
    value = gleason_frame_gap()
    print(value)
    if value == _GAP:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
