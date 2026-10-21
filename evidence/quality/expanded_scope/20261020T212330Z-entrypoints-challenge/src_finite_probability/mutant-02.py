"""Scaled integer simplex separators on a two-point report.

Origin: lean4/H001ProbabilitySimplex.lean theorem probability_simplex,
theorem signed_mass_one, theorem signed_not_nonneg, theorem double_mass_two,
theorem double_not_normalized, and theorem l1dist_self. pointW is 1 at
false and 0 at true. signedW is -1 at false and 2 at true. doubleW is 1
at both points. l1dist of a weight vector with itself is 0.
Claim: urn:omega:fqm:simplex:scaled-integer-separator:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_scaled_simplex.py.
Gate 5: use the source-bound measurements in the companion history.
Scope Fence: integer_mass sums one integer pair. scaled_simplex_witness
checks the named point, signed, and double pairs and the zero self-gap,
then returns the point mass 1. This file does not build a rational
probability simplex and does not claim that L1 distance is canonical.
"""

from __future__ import annotations

from typing import Mapping

# Declared input budget; the signed sum may need one additional result bit.
MAX_WEIGHT_BITS = 1024

_POINT: tuple[int, int] = (1, 0)
_SIGNED: tuple[int, int] = (-1, 2)
_DOUBLE: tuple[int, int] = (1, 1)


class ScaledSimplexError(Exception):
    """One violated scaled-simplex invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ScaledSimplexError:
    return ScaledSimplexError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if issubclass(type(value), float):
        raise _fail("float refused at the weight boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer weight was required", role=role)
    if isinstance(value, int):
        if value.bit_length() > MAX_WEIGHT_BITS:
            raise _fail("integer weight bit budget exceeded", role=role, bits=value.bit_length(), limit=MAX_WEIGHT_BITS)
        return value
    raise _fail("weight is not an integer", role=role, received=type(value).__name__)


def _require_pair(weights: object) -> tuple[int, int]:
    if issubclass(type(weights), (str, bytes)) or not issubclass(type(weights), tuple):
        raise _fail("weights are not a tuple", received=type(weights).__name__)
    if type(weights) is not tuple:
        raise _fail("weight container subclass refused", received=type(weights).__name__)
    entries = tuple(weights)
    if len(entries) != 2:
        raise _fail("weights are not a Bool pair", length=len(entries))
    return (_require_int(entries[0], "false"), _require_int(entries[1], "true"))


def _mass(pair: tuple[int, int]) -> int:
    return pair[0] + pair[1]


def integer_mass(weights: object) -> int:
    """Return the total integer mass of one Bool weight pair."""
    return _mass(_require_pair(weights))


def _require_point(pair: tuple[int, int]) -> int:
    mass = _mass(pair)
    if mass != 1:
        raise _fail("point mass is not one", mass=mass)
    if pair[0] < 0 or pair[1] < 0:
        raise _fail("point weights are signed", false=pair[0], true=pair[1])
    return mass


def _require_signed(pair: tuple[int, int]) -> int:
    total = _mass(pair)
    if total != 1:
        raise _fail("signed mass is not one", mass=total)
    if pair[0] >= 0 and pair[1] >= 0:
        raise _fail("signed weights are nonnegative", false=pair[0], true=pair[1])
    return total


def _require_double(pair: tuple[int, int]) -> int:
    mass = _mass(pair)
    if mass != 2:
        raise _fail("double mass is not two", mass=mass)
    if pair[0] < 0 or pair[1] < 0:
        raise _fail("double weights are signed", false=pair[0], true=pair[1])
    return mass


def _self_gap(pair: tuple[int, int]) -> int:
    return abs(pair[0] - pair[0]) + abs(pair[1] - pair[1])


def scaled_simplex_witness() -> int:
    """Return the point mass after the three named separators agree."""
    point = _require_point(_POINT)
    _require_signed(_SIGNED)
    doubled = _require_double(_DOUBLE)
    gap = _self_gap(_POINT)
    if doubled != 2 or gap != 0:
        raise _fail("separator witness missed", doubled=doubled, gap=gap)
    return point


def main() -> int:
    value = scaled_simplex_witness()
    try:
        print(value)
    except (OSError, ValueError):
        return 2
    if value == 1:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
