"""Checksum of a positive rational packet payload.

Origin: lean4/HilbertWalkRationals.lean theorem padd_assoc
(padd (padd a b) c = padd a (padd b c)) and theorem fadd_assoc
(fadd (fadd x y) z = fadd x (fadd y z)).
Claim: urn:omega:fqm:packet:payload-checksum:v1
AuthorityEffect: None
Mutation-Kills: 9 non-equivalent source mutants, executed by code/python/tests/test_packet_protocol.py.
Gate 5: earlier measurements are retained in contract history; the changed source requires a fresh structural assessment.
Scope Fence: payload_checksum returns the sum of a nonempty tuple of positive
exact rationals after a left fold and a right fold agree. certified_checksum
checks that sum on (1/2, 1/3, 1/7) and requires it to be 41/42. The cited
theorems are associativity for the PreQ and Frac constructors. This file uses
Python Fraction, does not prove those theorems, and does not claim a packet
schema, a digest, or a gauge differential.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_FIXTURE: tuple[object, ...] = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 7))
_CHECKSUM = Fraction(41, 42)


class PacketProtocolError(Exception):
    """One violated payload-checksum invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> PacketProtocolError:
    return PacketProtocolError(invariant, parameters)


def _require_tuple(entries: object) -> tuple[object, ...]:
    if isinstance(entries, (str, bytes)) or not isinstance(entries, tuple):
        raise _fail("payload entries are not a tuple", received=type(entries).__name__)
    return tuple(entries)


def _require_nonempty(entries: tuple[object, ...]) -> tuple[object, ...]:
    if len(entries) == 0:
        raise _fail("payload entries are empty")
    return entries


def _require_entry(value: object, index: int) -> Fraction:
    if issubclass(type(value), float):
        raise _fail("float refused at the payload boundary", index=index, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", index=index)
    if type(value) in (int, Fraction):
        numerator = value if type(value) is int else value.numerator
        denominator = 1 if type(value) is int else value.denominator
        if max(numerator.bit_length(), denominator.bit_length()) > 1024:
            raise _fail("exact scalar exceeds the 1024-bit limit", index=index)
    if type(value) is Fraction:
        entry = value
    elif type(value) is int:
        entry = Fraction(value)
    else:
        raise _fail(
            "payload entry is not an exact rational",
            index=index,
            received=type(value).__name__,
        )
    if entry <= 0:
        raise _fail("payload entry is not positive", index=index, received=str(entry))
    return entry


def _collect(entries: tuple[object, ...]) -> tuple[Fraction, ...]:
    collected: list[Fraction] = []
    for index, value in enumerate(entries):
        collected.append(_require_entry(value, index))
    return tuple(collected)


def _sum_left(entries: tuple[Fraction, ...]) -> Fraction:
    total = Fraction(0)
    for entry in entries:
        total = total + entry
    return total


def _sum_right(entries: tuple[Fraction, ...]) -> Fraction:
    total = Fraction(0)
    for entry in reversed(entries):
        total = entry + total
    return total


def payload_checksum(entries: object) -> Fraction:
    """Return the sum of a nonempty tuple of positive exact rationals."""
    checked = _collect(_require_nonempty(_require_tuple(entries)))
    left = _sum_left(checked)
    right = _sum_right(checked)
    if left != right:
        raise _fail("payload folds differ", left=str(left), right=str(right))
    return left


def certified_checksum() -> Fraction:
    """Sum of (1/2, 1/3, 1/7), required to be 41/42."""
    value = payload_checksum(_FIXTURE)
    if value != _CHECKSUM:
        raise _fail("certified checksum is not forty-one forty-seconds", checksum=str(value))
    return value


def main() -> int:
    value = certified_checksum()
    print(value)
    if value == _CHECKSUM:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
