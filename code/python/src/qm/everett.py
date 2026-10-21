"""Everett branch weights as a rational partition of unity.

Origin: code/python/src/qm/campaigns/everett.py
Claim: urn:omega:fqm:qm:everett-conditional-weight:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 7; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: Branches 1/2, 1/3, and 1/6 sum to 1. The conditional weight of the
first branch inside the first two is 3/5. This file does not derive the Born rule.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_WEIGHT = Fraction(3, 5)


class EverettError(Exception):
    """One violated branch invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> EverettError:
    return EverettError(invariant, parameters)


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


def branch_total(weights: object) -> Fraction:
    """Sum of nonnegative branch weights. The sum must be 1."""
    if isinstance(weights, (str, bytes)) or not isinstance(weights, tuple) or len(weights) == 0:
        raise _fail("branch weights are not a nonempty tuple", received=type(weights).__name__)
    total = Fraction(0)
    for weight in weights:
        value = _require_fraction(weight, "branch")
        if value < 0:
            raise _fail("a branch weight is negative", weight=str(value))
        total += value
    if total != 1:
        raise _fail("branch weights do not sum to 1", total=str(total))
    return total


def _require_sector(sector: object) -> tuple[object, ...]:
    if isinstance(sector, (str, bytes)):
        raise _fail("the conditioning sector is empty", received=type(sector).__name__)
    if not isinstance(sector, tuple):
        raise _fail("the conditioning sector is empty", received=type(sector).__name__)
    if len(sector) == 0:
        raise _fail("the conditioning sector is empty", received=type(sector).__name__)
    return sector


def _branch_slot(index: object, length: int) -> int:
    slot = _require_fraction(index, "sector")
    if slot.denominator != 1:
        raise _fail("sector index is outside the branches", index=str(slot))
    if slot < 0 or slot >= length:
        raise _fail("sector index is outside the branches", index=str(slot))
    return int(slot)


def _branch_tuple(weights: object) -> tuple[Fraction, ...]:
    parsed = weights if isinstance(weights, tuple) else tuple()
    branch_total(parsed)
    collected: list[Fraction] = []
    for weight in parsed:
        collected.append(_require_fraction(weight, "branch"))
    return tuple(collected)


def _sector_mass(parsed: tuple[Fraction, ...], sector: tuple[object, ...]) -> Fraction:
    mass = Fraction(0)
    for index in sector:
        mass += parsed[_branch_slot(index, len(parsed))]
    if mass == 0:
        raise _fail("the conditioning sector has no mass")
    return mass


def conditional_weight(weights: object, sector: object) -> Fraction:
    """Renormalized weight of the first selected branch."""
    parsed = _branch_tuple(weights)
    chosen = _require_sector(sector)
    first = _branch_slot(chosen[0], len(parsed))
    mass = _sector_mass(parsed, chosen)
    return parsed[first] / mass


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def first_branch_conditional() -> Fraction:
    """Conditional weight of the branch 1/2 inside the sector of the first two weights."""
    weights = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
    if branch_total(weights) != 1:
        raise _fail("the Everett partition is not exhaustive")
    return _locked(conditional_weight(weights, (0, 1)), _WEIGHT, "Everett conditional weight drifted")


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the conditional weight 3/5."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return first_branch_conditional()


def main() -> int:
    value = first_branch_conditional()
    print(value)
    if value == _WEIGHT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
