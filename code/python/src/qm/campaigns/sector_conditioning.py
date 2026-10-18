"""Condition a rational distribution on a sector and renormalize.

Origin: code/python/src/qm/campaigns/sector_conditioning.py
Claim: urn:omega:fqm:qm:first-sector-weight:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 8; AST Sonar cognitive complexity max 8; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 8.
Scope Fence: (1/2, 1/4, 1/4) conditioned on the first two outcomes is (2/3, 1/3).
No general conditional-probability theorem is claimed.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_WEIGHT = Fraction(2, 3)


class SectorError(Exception):
    """One violated sector invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SectorError:
    return SectorError(invariant, parameters)


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


def _weights(values: object) -> tuple[Fraction, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, tuple) or len(values) == 0:
        raise _fail("weights are not a nonempty tuple", received=type(values).__name__)
    parsed = tuple(_require_fraction(item, "weight") for item in values)
    total = Fraction(0)
    index = 0
    while index < len(parsed):
        if parsed[index] < 0:
            raise _fail("a weight is negative", index=index, weight=str(parsed[index]))
        total += parsed[index]
        index += 1
    if total != 1:
        raise _fail("weights are not a probability vector", total=str(total))
    return parsed


def _require_sector(sector: object) -> tuple[object, ...]:
    if isinstance(sector, (str, bytes)):
        raise _fail("the sector is empty", received=type(sector).__name__)
    if not isinstance(sector, tuple):
        raise _fail("the sector is empty", received=type(sector).__name__)
    if len(sector) == 0:
        raise _fail("the sector is empty", received=type(sector).__name__)
    return sector


def _sector_index(index: object, length: int) -> int:
    slot = _require_fraction(index, "sector")
    if slot.denominator != 1:
        raise _fail("sector index is outside the distribution", index=str(slot))
    if slot < 0 or slot >= length:
        raise _fail("sector index is outside the distribution", index=str(slot))
    return int(slot)


def _selected(parsed: tuple[Fraction, ...], sector: tuple[object, ...]) -> tuple[Fraction, ...]:
    chosen: list[Fraction] = []
    for index in sector:
        chosen.append(parsed[_sector_index(index, len(parsed))])
    return tuple(chosen)


def _sector_mass(selected: tuple[Fraction, ...]) -> Fraction:
    mass = Fraction(0)
    for value in selected:
        mass += value
    if mass == 0:
        raise _fail("the sector has no mass")
    return mass


def _renormalize(selected: tuple[Fraction, ...], mass: Fraction) -> tuple[Fraction, ...]:
    scaled: list[Fraction] = []
    for value in selected:
        scaled.append(value / mass)
    return tuple(scaled)


def condition(weights: object, sector: object) -> tuple[Fraction, ...]:
    """Renormalize the selected coordinates of a rational probability vector."""
    parsed = _weights(weights)
    selected = _selected(parsed, _require_sector(sector))
    return _renormalize(selected, _sector_mass(selected))


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def first_sector_weight() -> Fraction:
    """First coordinate after conditioning (1/2, 1/4, 1/4) on (0, 1)."""
    conditional = condition((Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)), (0, 1))
    if conditional != (Fraction(2, 3), Fraction(1, 3)):
        raise _fail("conditional distribution drifted", conditional=str(conditional))
    total = conditional[0] + conditional[1]
    if total != 1:
        raise _fail("conditional weights do not sum to 1", total=str(total))
    return conditional[0]


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the first conditional weight 2/3."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(first_sector_weight(), _WEIGHT, "first sector weight drifted")


def main() -> int:
    value = first_sector_weight()
    print(value)
    if value == _WEIGHT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
