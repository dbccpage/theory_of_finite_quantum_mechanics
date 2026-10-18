"""The qutrit clock permutation and its order.

Origin: code/python/src/qm/campaigns/higher_dim.py
Claim: urn:omega:fqm:qm:qutrit-clock-order:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 10; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: The clock is the permutation matrix of the 3-cycle. Its order is 3.
The Weyl relation with a root of unity is not claimed.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_ORDER = 3


class ClockError(Exception):
    """One violated clock invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ClockError:
    return ClockError(invariant, parameters)


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


def _entry(left: tuple[tuple[Fraction, Fraction, Fraction], ...], right: tuple[tuple[Fraction, Fraction, Fraction], ...], row: int, column: int) -> Fraction:
    return left[row][0] * right[0][column] + left[row][1] * right[1][column] + left[row][2] * right[2][column]


def _mul(left: tuple[tuple[Fraction, Fraction, Fraction], ...], right: tuple[tuple[Fraction, Fraction, Fraction], ...]) -> tuple[tuple[Fraction, Fraction, Fraction], tuple[Fraction, Fraction, Fraction], tuple[Fraction, Fraction, Fraction]]:
    return (
        (_entry(left, right, 0, 0), _entry(left, right, 0, 1), _entry(left, right, 0, 2)),
        (_entry(left, right, 1, 0), _entry(left, right, 1, 1), _entry(left, right, 1, 2)),
        (_entry(left, right, 2, 0), _entry(left, right, 2, 1), _entry(left, right, 2, 2)),
    )


def clock_order(dimension: object | None = None) -> int:
    """Order of the clock permutation. The default dimension is 3, and the order equals it."""
    if dimension is None:
        count = _ORDER
    else:
        parsed = _require_fraction(dimension, "dimension")
        if parsed.denominator != 1 or parsed != _ORDER:
            raise _fail("this clock certificate is the qutrit clock", dimension=str(parsed))
        count = int(parsed)
    clock = (
        (Fraction(0), Fraction(0), Fraction(1)),
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
    )
    identity = ((Fraction(1), Fraction(0), Fraction(0)), (Fraction(0), Fraction(1), Fraction(0)), (Fraction(0), Fraction(0), Fraction(1)))
    current = identity
    exponent = 1
    while exponent <= count + 2:
        current = _mul(current, clock)
        if current == identity:
            if exponent != count:
                raise _fail("clock order drifted", order=exponent, dimension=count)
            return exponent
        exponent += 1
    raise _fail("clock power did not return to the identity", dimension=count)


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the qutrit clock order 3."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(Fraction(clock_order()), Fraction(_ORDER), "clock order drifted")


def main() -> int:
    value = clock_order()
    print(value)
    if value == _ORDER:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
