"""One step of the simple random walk on the 3-cycle.

Origin: code/python/src/qm/campaigns/quantum_walk.py
Claim: urn:omega:fqm:qm:cycle-return:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: P is the classical stochastic matrix with zeros on the diagonal
and 1/2 off it. P^2 at the start vertex is 1/2. This is not a unitary coin.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_RETURN = Fraction(1, 2)


class WalkError(Exception):
    """One violated walk invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> WalkError:
    return WalkError(invariant, parameters)


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


def _column_sum(step: tuple[tuple[Fraction, Fraction, Fraction], ...], column: int) -> Fraction:
    return step[0][column] + step[1][column] + step[2][column]


def _step() -> tuple[tuple[Fraction, Fraction, Fraction], tuple[Fraction, Fraction, Fraction], tuple[Fraction, Fraction, Fraction]]:
    half = _require_fraction(1, "half") / _require_fraction(2, "two")
    zero = _require_fraction(0, "zero")
    return ((zero, half, half), (half, zero, half), (half, half, zero))


def cycle_return() -> Fraction:
    """Return probability of being home after two steps. It is 1/2."""
    step = _step()
    column = 0
    while column < 3:
        if _column_sum(step, column) != 1:
            raise _fail("the walk is not column-stochastic", column=column)
        column += 1
    square = _mul(step, step)
    uniform = (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3))
    image0 = step[0][0] * uniform[0] + step[0][1] * uniform[1] + step[0][2] * uniform[2]
    if image0 != uniform[0]:
        raise _fail("uniform measure moved", image=str(image0))
    return square[0][0]


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the two-step return 1/2."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(cycle_return(), _RETURN, "cycle return drifted")


def main() -> int:
    value = cycle_return()
    print(value)
    if value == _RETURN:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
