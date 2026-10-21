"""Bridge from a rational qubit amplitude to the expectation of Pauli Z.

Origin: lean4/GroupParameter.lean definition pauliZ, which is diag(1, -1).
On a rational amplitude the expectation is |up|^2 - |down|^2.
Claim: urn:omega:fqm:qm:pythagorean-z-expectation:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_engine_bridge.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 3; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 4.
Scope Fence: The locked value is the population difference on (3/5, 4/5).
This file does not build a channel, a Kraus map, or a continuum generator.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping


class BridgeError(ValueError):
    """One violated bridge invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> BridgeError:
    return BridgeError(invariant, parameters)


_PYTHAGOREAN: tuple[Fraction, Fraction] = (Fraction(3, 5), Fraction(4, 5))
_POPULATION = Fraction(9, 25) - Fraction(16, 25)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _exact(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where an exact rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is not int:
        raise _fail("amplitude coordinate is not an exact rational", role=role, received=type(value).__name__)
    return Fraction(value)


def _pair(value: object, role: str) -> tuple[Fraction, Fraction]:
    if isinstance(value, (str, bytes)) or not isinstance(value, tuple) or len(value) != 2:
        raise _fail("the bridge expects a qubit amplitude", role=role, received=type(value).__name__)
    return (_exact(value[0], role + "_up"), _exact(value[1], role + "_down"))


def _require_unit(up: Fraction, down: Fraction, role: str) -> None:
    norm = up * up + down * down
    if norm != 1:
        raise _fail("amplitude norm is not 1", role=role, norm=str(norm))


def _expectation(up: Fraction, down: Fraction) -> Fraction:
    return up * up - down * down


def z_expectation(amplitude: object = None) -> Fraction:
    """Return |up|^2 - |down|^2. The default amplitude is (3/5, 4/5)."""
    pair = _PYTHAGOREAN if amplitude is None else _pair(amplitude, "amplitude")
    _require_unit(pair[0], pair[1], "amplitude")
    return _expectation(pair[0], pair[1])


def pythagorean_expectation(amplitude: object = None) -> Fraction:
    """Return -7/25 when the amplitude is the frozen Pythagorean state."""
    value = z_expectation(amplitude)
    if value != _POPULATION:
        raise _fail(
            "expectation disagrees with the population difference",
            value=str(value),
            population=str(_POPULATION),
        )
    return value


__all__ = ["BridgeError", "pythagorean_expectation", "z_expectation"]
