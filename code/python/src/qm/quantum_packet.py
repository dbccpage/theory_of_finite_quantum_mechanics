"""Squared norm of a two-amplitude rational packet.

Origin: lean4/FiniteQM.lean theorem unit_sphere_pythagorean_ray_witness
(P2 (3 / 5) (4 / 5) 0 = 1) and lean4/FiniteQFTAndGravity.lean theorem
phase_damping_trace_preserving
((p / q) * (p / q) + (r / q) * (r / q) = 1 whenever p * p + r * r = q * q)
together with theorem phase_damping_triples
((3 / 5) * (3 / 5) + (4 / 5) * (4 / 5) = 1).
Claim: urn:omega:fqm:packet:pythagorean-norm:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_quantum_packet.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: packet_norm returns the sum of squares of a length-2 exact
rational amplitude pair after a second square-sum agrees.
certified_packet_norm checks that sum on (3/5, 4/5) and requires it to be 1.
The cited theorems also state a degree-4 frame identity and a Kraus trace
identity. This file does not prove those theorems, does not accept a third
amplitude, and does not build a channel or a density matrix.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_WIDTH = 2
_FIXTURE: tuple[object, ...] = (Fraction(3, 5), Fraction(4, 5))
_UNIT = Fraction(1)


class QuantumPacketError(Exception):
    """One violated packet-norm invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> QuantumPacketError:
    return QuantumPacketError(invariant, parameters)


def _require_tuple(amplitudes: object) -> tuple[object, ...]:
    if isinstance(amplitudes, (str, bytes)) or not isinstance(amplitudes, tuple):
        raise _fail("packet amplitudes are not a tuple", received=type(amplitudes).__name__)
    return tuple(amplitudes)


def _require_pair(amplitudes: tuple[object, ...]) -> tuple[object, ...]:
    if len(amplitudes) != _WIDTH:
        raise _fail("packet amplitudes are not a pair", length=len(amplitudes))
    return amplitudes


def _require_amplitude(value: object, index: int) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the packet boundary", index=index, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational amplitude was required", index=index)
    if isinstance(value, Fraction):
        amplitude = value
    elif type(value) is int:
        amplitude = Fraction(value)
    else:
        raise _fail(
            "packet amplitude is not an exact rational",
            index=index,
            received=type(value).__name__,
        )
    return amplitude


def _collect(amplitudes: tuple[object, ...]) -> tuple[Fraction, Fraction]:
    return (_require_amplitude(amplitudes[0], 0), _require_amplitude(amplitudes[1], 1))


def _prepare(amplitudes: object) -> tuple[Fraction, Fraction]:
    return _collect(_require_pair(_require_tuple(amplitudes)))


def _square(value: Fraction) -> Fraction:
    return value * value


def _direct_norm(left: Fraction, right: Fraction) -> Fraction:
    return _square(left) + _square(right)


def _born_sum(left: Fraction, right: Fraction) -> Fraction:
    first = left * left
    second = right * right
    return first + second


def packet_norm(amplitudes: object) -> Fraction:
    """Return the sum of squares for an exact rational amplitude pair."""
    left, right = _prepare(amplitudes)
    direct = _direct_norm(left, right)
    born = _born_sum(left, right)
    if direct != born:
        raise _fail("norm readings differ", direct=str(direct), born=str(born))
    return direct


def certified_packet_norm() -> Fraction:
    """Squared norm of (3/5, 4/5), required to be one."""
    value = packet_norm(_FIXTURE)
    if value != _UNIT:
        raise _fail("certified packet norm is not one", norm=str(value))
    return value


def main() -> int:
    value = certified_packet_norm()
    print(value)
    if value == _UNIT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
