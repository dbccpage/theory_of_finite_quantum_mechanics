"""Binary entrypoint witness for the Pythagorean rational ray.

Origin: lean4/FiniteQM.lean theorem unit_sphere_pythagorean_ray_witness
(P2 (3/5) (4/5) 0 = 1, P4 = 337/625, P22 = 144/625, and
P4 = 1 - 2 * P22). P2, P4, and P22 are the symmetric power sums in
that file.
Claim: urn:omega:fqm:bin:pythagorean-ray:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_bin_witness.py.
Gate 5: use the source-bound measurements in the companion history.
Scope Fence: ray_power_two returns P2 for one exact rational triple.
bin_two_square checks the four conjuncts on (3/5, 4/5, 0) and returns
P2, which is 1. This file does not check the standard basis ray or the
ray (1/3, 2/3, 2/3), and it does not prove FiniteQM.lean.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

# Declared engineering policy, not a physical or mathematical constant.
MAX_SCALAR_BITS = 1024

_RAY: tuple[object, ...] = (Fraction(3, 5), Fraction(4, 5), Fraction(0))
_UNIT = Fraction(1)
_FOURTH = Fraction(337, 625)
_CROSS = Fraction(144, 625)


class BinWitnessError(Exception):
    """One violated ray invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> BinWitnessError:
    return BinWitnessError(invariant, parameters)


def _require_tuple(amplitudes: object) -> tuple[object, ...]:
    if isinstance(amplitudes, (str, bytes)) or not isinstance(amplitudes, tuple):
        raise _fail("ray amplitudes are not a tuple", received=type(amplitudes).__name__)
    if type(amplitudes) is not tuple:
        raise _fail("ray container subclass refused", received=type(amplitudes).__name__)
    return tuple(amplitudes)


def _require_three(amplitudes: tuple[object, ...]) -> tuple[object, ...]:
    if len(amplitudes) != 3:
        raise _fail("ray amplitudes are not three", length=len(amplitudes))
    return amplitudes


def _require_amplitude(value: object, index: int) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the ray boundary", index=index, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational amplitude was required", index=index)
    if type(value) is Fraction:
        _require_bits(value.numerator, index)
        _require_bits(value.denominator, index)
        return value
    if type(value) is int:
        _require_bits(value, index)
        return Fraction(value)
    raise _fail("ray amplitude is not an exact rational", index=index, received=type(value).__name__)


def _require_bits(value: int, index: int) -> None:
    if value.bit_length() > MAX_SCALAR_BITS:
        raise _fail("ray scalar bit budget exceeded", index=index, bits=value.bit_length(), limit=MAX_SCALAR_BITS)


def _collect(amplitudes: tuple[object, ...]) -> tuple[Fraction, Fraction, Fraction]:
    collected: list[Fraction] = []
    for index, value in enumerate(amplitudes):
        collected.append(_require_amplitude(value, index))
    return (collected[0], collected[1], collected[2])


def _parsed(amplitudes: object) -> tuple[Fraction, Fraction, Fraction]:
    return _collect(_require_three(_require_tuple(amplitudes)))


def _square(value: Fraction) -> Fraction:
    return value * value


def _power_two(x_pos: Fraction, y_pos: Fraction, z_pos: Fraction) -> Fraction:
    return _square(x_pos) + _square(y_pos) + _square(z_pos)


def _power_four(x_pos: Fraction, y_pos: Fraction, z_pos: Fraction) -> Fraction:
    return _square(_square(x_pos)) + _square(_square(y_pos)) + _square(_square(z_pos))


def _cross(x_pos: Fraction, y_pos: Fraction, z_pos: Fraction) -> Fraction:
    return (
        _square(x_pos) * _square(y_pos)
        + _square(y_pos) * _square(z_pos)
        + _square(z_pos) * _square(x_pos)
    )


def _require_witness(power: Fraction, fourth: Fraction, cross: Fraction) -> Fraction:
    if power != _UNIT:
        raise _fail("power two is not one", power=str(power))
    if fourth != _FOURTH or cross != _CROSS:
        raise _fail("degree-4 witness missed", fourth=str(fourth), cross=str(cross))
    if fourth != _UNIT - 2 * cross:
        raise _fail("degree-4 relation missed", fourth=str(fourth), cross=str(cross))
    return power


def ray_power_two(amplitudes: object | None = None) -> Fraction:
    """Return P2 for the Pythagorean ray, or for another exact triple."""
    parsed = _parsed(_RAY if amplitudes is None else amplitudes)
    return _power_two(parsed[0], parsed[1], parsed[2])


def bin_two_square() -> Fraction:
    """Return P2 (3/5, 4/5, 0) after the four theorem conjuncts match."""
    parsed = _parsed(_RAY)
    power = _power_two(parsed[0], parsed[1], parsed[2])
    fourth = _power_four(parsed[0], parsed[1], parsed[2])
    cross = _cross(parsed[0], parsed[1], parsed[2])
    return _require_witness(power, fourth, cross)


def main() -> int:
    value = bin_two_square()
    try:
        print(value)
    except (OSError, ValueError):
        return 2
    if value == _UNIT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
