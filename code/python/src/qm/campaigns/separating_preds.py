"""Z expectation separates two rational qubit states.

Origin: lean4/GroupParameter.lean definition pauliZ, which is diag(1, -1),
and theorem pauli_z_trace_zero.
Claim: urn:omega:fqm:qm:separating-z-gap:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_separating_preds.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 3; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 4.
Scope Fence: The gap is |up|^2 - |down|^2 on the two frozen states (1, 0)
and (3/5, 4/5). This file does not classify CHSH, Tsirelson, or a
Mermin-Peres assignment, and it does not claim that every pair of states
is separated by Z.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping


class SeparationError(ValueError):
    """One violated separating-predicate invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SeparationError:
    return SeparationError(invariant, parameters)


_COMPUTATIONAL: tuple[Fraction, Fraction] = (Fraction(1), Fraction(0))
_TILTED: tuple[Fraction, Fraction] = (Fraction(3, 5), Fraction(4, 5))


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
        raise _fail("state is not an amplitude pair", role=role, received=type(value).__name__)
    return (_exact(value[0], role + "_up"), _exact(value[1], role + "_down"))


def _require_unit(up: Fraction, down: Fraction, role: str) -> None:
    norm = up * up + down * down
    if norm != 1:
        raise _fail("a state is not normalized", role=role, norm=str(norm))


def _expectation(up: Fraction, down: Fraction) -> Fraction:
    return up * up - down * down


def _state(value: object, default: tuple[Fraction, Fraction], role: str) -> tuple[Fraction, Fraction]:
    pair = default if value is None else _pair(value, role)
    _require_unit(pair[0], pair[1], role)
    return pair


def z_expectation(amplitude: object) -> Fraction:
    """Return |up|^2 - |down|^2 for one normalized rational amplitude."""
    up, down = _state(amplitude, _COMPUTATIONAL, "amplitude")
    return _expectation(up, down)


def expectation_gap(computational: object = None, tilted: object = None) -> Fraction:
    """Return <Z>_(1, 0) - <Z>_(3/5, 4/5), which is 32/25."""
    left = _state(computational, _COMPUTATIONAL, "computational")
    right = _state(tilted, _TILTED, "tilted")
    gap = _expectation(left[0], left[1]) - _expectation(right[0], right[1])
    if gap == 0:
        raise _fail("Z does not separate the two states", gap="0")
    return gap


__all__ = ["SeparationError", "expectation_gap", "z_expectation"]
