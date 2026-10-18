"""Named local checks for the Pythagorean ray and a rational product.

Origin: lean4/FiniteQM.lean theorem unit_sphere_pythagorean_ray_witness
(P2 (3/5) (4/5) 0 = 1, P4 = 337/625, P22 = 144/625, and
P4 = 1 - 2 * P22) and theorem p2_sq_eq_p4_add_two_p22
(P2 * P2 = P4 + 2 * P22).
Claim: urn:omega:fqm:suite:named-norm:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_suites.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: ray_norm returns the sum of squares of a rational triple.
witness_gap returns P2^2 - (P4 + 2 * P22). run_local_suite("norm") checks
(3/5, 4/5, 0) against the cited witness and returns 1.
run_local_suite("cycle") returns (2/3) * (3/5) * (5/2), which is not the
cited theorem. This file uses Python Fraction, does not prove the Lean
theorems, and does not claim the other FiniteQM countermodels.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_RAY: tuple[object, ...] = (Fraction(3, 5), Fraction(4, 5), Fraction(0))
_UNIT = Fraction(1)
_FOURTH = Fraction(337, 625)
_CROSS = Fraction(144, 625)


class SuiteError(Exception):
    """One violated suite invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SuiteError:
    return SuiteError(invariant, parameters)


def _require_tuple(amplitudes: object) -> tuple[object, ...]:
    if isinstance(amplitudes, (str, bytes)) or not isinstance(amplitudes, tuple):
        raise _fail("ray amplitudes are not a tuple", received=type(amplitudes).__name__)
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
    if isinstance(value, Fraction):
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


def _parsed(amplitudes: object) -> tuple[Fraction, Fraction, Fraction]:
    return _collect(_require_three(_require_tuple(amplitudes)))


def ray_norm(amplitudes: object) -> Fraction:
    """Return the sum of squares of an exact rational triple."""
    x_pos, y_pos, z_pos = _parsed(amplitudes)
    return _power_sum_two(x_pos, y_pos, z_pos)


def witness_gap(amplitudes: object) -> Fraction:
    """Return P2^2 - (P4 + 2 * P22) for an exact rational triple."""
    x_pos, y_pos, z_pos = _parsed(amplitudes)
    left = _square(_power_sum_two(x_pos, y_pos, z_pos))
    right = _power_sum_four(x_pos, y_pos, z_pos) + 2 * _cross_sum(x_pos, y_pos, z_pos)
    if left != right:
        raise _fail("degree readings differ", left=str(left), right=str(right))
    return left - right


def _norm_suite() -> Fraction:
    x_pos, y_pos, z_pos = _parsed(_RAY)
    value = _power_sum_two(x_pos, y_pos, z_pos)
    fourth = _power_sum_four(x_pos, y_pos, z_pos)
    cross = _cross_sum(x_pos, y_pos, z_pos)
    if value != _UNIT or witness_gap(_RAY) != 0:
        raise _fail("norm suite missed the unit ray", power=str(value))
    if fourth != _FOURTH or cross != _CROSS:
        raise _fail("norm suite missed the degree-4 witness", fourth=str(fourth), cross=str(cross))
    return value


def _cycle_product() -> Fraction:
    return Fraction(2, 3) * Fraction(3, 5) * Fraction(5, 2)


def _cycle_suite() -> Fraction:
    product = _cycle_product()
    if product != _UNIT:
        raise _fail("cycle suite is not one", product=str(product))
    return product


def _require_name(name: object) -> str:
    if type(name) is not str:
        raise _fail("suite name is not a string", received=type(name).__name__)
    return name


def run_local_suite(name: object) -> Fraction:
    """Run the named exact suite and return its rational value."""
    checked = _require_name(name)
    if checked == "norm":
        return _norm_suite()
    if checked == "cycle":
        return _cycle_suite()
    raise _fail("unknown suite", name=checked)


def main() -> int:
    value = run_local_suite("norm")
    print(value)
    if value == _UNIT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
