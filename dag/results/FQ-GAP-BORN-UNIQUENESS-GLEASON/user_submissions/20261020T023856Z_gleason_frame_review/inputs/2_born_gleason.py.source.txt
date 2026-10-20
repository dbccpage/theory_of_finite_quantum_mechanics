"""Born weights as a quadratic frame function on a rational orthonormal basis.

Origin: code/python/src/qm/campaigns/born_gleason.py
Claim: urn:omega:fqm:qm:born-frame-gap:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: The two frames are the coordinate basis and the (3, 4, 5) rotation.
This file does not prove Gleason's theorem.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_GAP = Fraction(0)


class BornGleasonError(Exception):
    """One violated frame invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> BornGleasonError:
    return BornGleasonError(invariant, parameters)


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


def _pair(value: object, role: str) -> tuple[Fraction, Fraction]:
    if isinstance(value, (str, bytes)) or not isinstance(value, tuple) or len(value) != 2:
        raise _fail("frame vector is not a pair", role=role, received=type(value).__name__)
    return (_require_fraction(value[0], role), _require_fraction(value[1], role))


def _dot(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _orthonormal(frame: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> None:
    if _dot(frame[0], frame[0]) != 1 or _dot(frame[1], frame[1]) != 1:
        raise _fail("frame vector is not a unit vector")
    if _dot(frame[0], frame[1]) != 0:
        raise _fail("frame vectors are not orthogonal")


def _frame_sum(vector: tuple[Fraction, Fraction], frame: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    _orthonormal(frame)
    first = _dot(vector, frame[0])
    second = _dot(vector, frame[1])
    return first * first + second * second


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def born_frame_gap() -> Fraction:
    """Difference of the frame sums on the coordinate basis and a Pythagorean basis."""
    vector = (_require_fraction(3, "vx") / _require_fraction(5, "vd"), _require_fraction(4, "vy") / _require_fraction(5, "vd2"))
    coordinate = ((_require_fraction(1, "e0"), _require_fraction(0, "e1")), (_require_fraction(0, "e2"), _require_fraction(1, "e3")))
    rotated = ((vector[0], vector[1]), (Fraction(-4, 5), Fraction(3, 5)))
    gap = _frame_sum(vector, coordinate) - _frame_sum(vector, rotated)
    return _locked(gap, _GAP, "Born frame gap drifted")


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the Born frame gap 0."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return born_frame_gap()


def main() -> int:
    value = born_frame_gap()
    print(value)
    if value == _GAP:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
