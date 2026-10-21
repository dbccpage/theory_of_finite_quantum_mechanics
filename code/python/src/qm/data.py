"""Packaged exact input fixtures.

Origin: code/python/src/qm/data/__init__.py
Claim: urn:omega:fqm:qm:fixture-purity:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 6; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: A fixture rational "a/b" parses to a reduced Fraction. The fair
bit diag(1/2, 1/2) has purity 1/2. No repository discovery is performed.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_PURITY = Fraction(1, 2)


class FixtureRationalError(Exception):
    """One violated fixture invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> FixtureRationalError:
    return FixtureRationalError(invariant, parameters)


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


def parse_fixture_rational(text: object) -> Fraction:
    """Parse a fixture rational. Integers are accepted as n/1."""
    if type(text) is not str or "/" not in text:
        raise _fail("fixture rational must be 'a/b'", received=type(text).__name__)
    numerator, denominator = text.split("/", 1)
    if numerator.startswith("-"):
        sign = -1
        numerator = numerator[1:]
    else:
        sign = 1
    if not numerator.isdecimal() or not denominator.isdecimal():
        raise _fail("fixture rational is not an integer ratio", text=text)
    parsed = Fraction(sign * int(numerator), int(denominator))
    return parsed


def fixture_purity() -> Fraction:
    """Purity of the packaged fair bit after parsing the rational fields."""
    left = parse_fixture_rational("1/2")
    right = parse_fixture_rational("2/4")
    if left != right:
        raise _fail("1/2 and 2/4 do not reduce to the same fixture rational", left=str(left), right=str(right))
    if left + right != 1:
        raise _fail("the fair bit does not sum to 1", total=str(left + right))
    return left * left + right * right


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the fixture purity 1/2."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(fixture_purity(), _PURITY, "fixture purity drifted")


def main() -> int:
    value = fixture_purity()
    print(value)
    if value == _PURITY:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
