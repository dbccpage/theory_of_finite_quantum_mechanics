"""Pythagorean ray witness collected with two local closed forms.

Origin: lean4/FiniteQM.lean theorem unit_sphere_pythagorean_ray_witness
(P2 (3/5) (4/5) 0 = 1, P4 = 337/625, P22 = 144/625, and
P4 = 1 - 2 * P22) and theorem p2_sq_eq_p4_add_two_p22
(P2 * P2 = P4 + 2 * P22). P2, P4, and P22 are the symmetric power sums in
that file.
Claim: urn:omega:fqm:suite:pythagorean-ray:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_legacy_suites.py.
Gate 5: earlier measurements are retained in contract history; the changed source requires a fresh structural assessment.
Scope Fence: polynomial_gap returns P2^2 - (P4 + 2 * P22) for a rational
triple. certified_ray checks (3/5, 4/5, 0) and returns P2, which is 1.
suite_pass_count also checks the local product (2/3)*(3/5)*(5/2) and the
local sum 2/3 + 4/5, then returns how many of the three checks match.
Those two closed forms are not the cited theorems. This file uses Python
Fraction, does not prove the Lean theorems, and does not claim the other
countermodels in FiniteQM.lean.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_RAY: tuple[object, ...] = (Fraction(3, 5), Fraction(4, 5), Fraction(0))
_UNIT = Fraction(1)
_FOURTH = Fraction(337, 625)
_CROSS = Fraction(144, 625)
_SUITE_COUNT = 3


class LegacySuiteError(Exception):
    """One violated ray or suite invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> LegacySuiteError:
    return LegacySuiteError(invariant, parameters)


def _require_tuple(amplitudes: object) -> tuple[object, ...]:
    if isinstance(amplitudes, (str, bytes)) or not isinstance(amplitudes, tuple):
        raise _fail("ray amplitudes are not a tuple", received=type(amplitudes).__name__)
    return tuple(amplitudes)


def _require_three(amplitudes: tuple[object, ...]) -> tuple[object, ...]:
    if len(amplitudes) != 3:
        raise _fail("ray amplitudes are not three", length=len(amplitudes))
    return amplitudes


def _require_amplitude(value: object, index: int) -> Fraction:
    if issubclass(type(value), float):
        raise _fail("float refused at the ray boundary", index=index, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational amplitude was required", index=index)
    if type(value) in (int, Fraction):
        numerator = value if type(value) is int else value.numerator
        denominator = 1 if type(value) is int else value.denominator
        if max(numerator.bit_length(), denominator.bit_length()) > 1024:
            raise _fail("exact scalar exceeds the 1024-bit limit", index=index)
    if type(value) is Fraction:
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail(
        "ray amplitude is not an exact rational",
        index=index,
        received=type(value).__name__,
    )


def _collect(amplitudes: tuple[object, ...]) -> tuple[Fraction, Fraction, Fraction]:
    collected: list[Fraction] = []
    for index, value in enumerate(amplitudes):
        collected.append(_require_amplitude(value, index))
    return (collected[0], collected[1], collected[2])


def _square(value: Fraction) -> Fraction:
    return value * value


def _power_sum_two(x_pos: Fraction, y_pos: Fraction, z_pos: Fraction) -> Fraction:
    return _square(x_pos) + _square(y_pos) + _square(z_pos)


def _power_sum_four(x_pos: Fraction, y_pos: Fraction, z_pos: Fraction) -> Fraction:
    return _square(_square(x_pos)) + _square(_square(y_pos)) + _square(_square(z_pos))


def _cross_sum(x_pos: Fraction, y_pos: Fraction, z_pos: Fraction) -> Fraction:
    return (
        _square(x_pos) * _square(y_pos)
        + _square(y_pos) * _square(z_pos)
        + _square(z_pos) * _square(x_pos)
    )


def polynomial_gap(amplitudes: object) -> Fraction:
    """Return P2^2 - (P4 + 2 * P22) for an exact rational triple."""
    x_pos, y_pos, z_pos = _collect(_require_three(_require_tuple(amplitudes)))
    left = _square(_power_sum_two(x_pos, y_pos, z_pos))
    right = _power_sum_four(x_pos, y_pos, z_pos) + 2 * _cross_sum(x_pos, y_pos, z_pos)
    if left != right:
        raise _fail("degree readings differ", left=str(left), right=str(right))
    return left - right


def certified_ray() -> Fraction:
    """P2 of (3/5, 4/5, 0). The degree-4 witness requires it to be 1."""
    x_pos, y_pos, z_pos = _collect(_require_three(_require_tuple(_RAY)))
    value = _power_sum_two(x_pos, y_pos, z_pos)
    fourth = _power_sum_four(x_pos, y_pos, z_pos)
    cross = _cross_sum(x_pos, y_pos, z_pos)
    if value != _UNIT:
        raise _fail("certified ray power sum is not one", power=str(value))
    if fourth != _FOURTH or cross != _CROSS:
        raise _fail("certified degree-4 readings missed the witness", fourth=str(fourth), cross=str(cross))
    if fourth != _UNIT - 2 * cross:
        raise _fail("certified degree-4 identity failed", fourth=str(fourth), cross=str(cross))
    return value


def _cycle_product() -> Fraction:
    return Fraction(2, 3) * Fraction(3, 5) * Fraction(5, 2)


def _shear_sum() -> Fraction:
    return Fraction(2, 3) + Fraction(4, 5)


def suite_pass_count() -> int:
    """Return how many of the ray, the local product, and the local sum match."""
    closed = (
        (certified_ray(), _UNIT),
        (_cycle_product(), _UNIT),
        (_shear_sum(), Fraction(22, 15)),
    )
    passed = 0
    for value, target in closed:
        if value != target:
            raise _fail("suite check does not match its closed form", value=str(value), target=str(target))
        passed += 1
    if passed != _SUITE_COUNT:
        raise _fail("suite pass count is not three", count=passed)
    return passed


def main() -> int:
    value = certified_ray()
    print(value)
    if value == _UNIT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
