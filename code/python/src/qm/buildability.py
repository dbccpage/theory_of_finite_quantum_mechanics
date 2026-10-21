"""A shear word builds the exponent 5.

Origin: code/python/src/qm/campaigns/buildability.py
Claim: urn:omega:fqm:qm:shear-word-exponent:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 6; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: S(2) S(3) = S(5) is one word in elementary transvections.
This file does not decide the device-model set S.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_EXPONENT = 5


class BuildError(Exception):
    """One violated shear invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> BuildError:
    return BuildError(invariant, parameters)


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


def _require_exponent(value: object) -> int:
    parsed = _require_fraction(value, "exponent")
    if parsed.denominator != 1:
        raise _fail("shear exponent is not an integer", exponent=str(parsed))
    return int(parsed)


def shear(exponent: object) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    """Return the elementary shear S(exponent) = [[1, exponent], [0, 1]]."""
    power = _require_exponent(exponent)
    return ((Fraction(1), Fraction(power)), (Fraction(0), Fraction(1)))


def _product_entry(left: int, right: int) -> int:
    return left + right


def built_exponent(left: object | None = None, right: object | None = None) -> int:
    """Off-diagonal entry of S(left) S(right). The default word is S(2) S(3)."""
    first = 2 if left is None else _require_exponent(left)
    second = 3 if right is None else _require_exponent(right)
    built = shear(_product_entry(first, second))
    target = _mul_shears(shear(first), shear(second))
    if built != target:
        raise _fail("word did not build the shear", built=str(built), target=str(target))
    if left is None and right is None and int(built[0][1]) != _EXPONENT:
        raise _fail("default shear exponent drifted", exponent=int(built[0][1]))
    return int(target[0][1])


def _mul_shears(
    left: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
    right: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    top = (left[0][0] * right[0][0] + left[0][1] * right[1][0], left[0][0] * right[0][1] + left[0][1] * right[1][1])
    bottom = (left[1][0] * right[0][0] + left[1][1] * right[1][0], left[1][0] * right[0][1] + left[1][1] * right[1][1])
    return (top, bottom)


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the built exponent 5."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(Fraction(built_exponent()), Fraction(_EXPONENT), "built exponent drifted")


def main() -> int:
    value = built_exponent()
    print(value)
    if value == _EXPONENT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
