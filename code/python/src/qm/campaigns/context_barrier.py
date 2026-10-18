"""A context barrier is a pair of contexts whose union does not commute.

Origin: code/python/src/qm/campaigns/context_barrier.py
Claim: urn:omega:fqm:qm:context-barrier-mass:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: {Z⊗I, I⊗Z} commute with each other. Z⊗I does not commute with
X⊗X. The reported mass is the absolute commutator mass 8. No Kochen–Specker
theorem is claimed.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from .commuting_obs import commutator_mass

_MASS = Fraction(8)


class ContextBarrierError(Exception):
    """One violated context invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ContextBarrierError:
    return ContextBarrierError(invariant, parameters)


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


def _scale(block: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], factor: Fraction) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    return (
        (factor * block[0][0], factor * block[0][1]),
        (factor * block[1][0], factor * block[1][1]),
    )


def _join(left: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], right: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    return (left[0] + right[0], left[1] + right[1])


def _kron(left: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], right: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> tuple[tuple[Fraction, ...], ...]:
    top = _join(_scale(right, left[0][0]), _scale(right, left[0][1]))
    bottom = _join(_scale(right, left[1][0]), _scale(right, left[1][1]))
    return (top[0], top[1], bottom[0], bottom[1])


def _pair(values: tuple[int, int]) -> tuple[Fraction, Fraction]:
    return (_require_fraction(values[0], "entry"), _require_fraction(values[1], "entry"))


def barrier_mass() -> Fraction:
    """Commutator mass across the two contexts. Within the Z context the mass is 0."""
    z = (_pair((1, 0)), _pair((0, -1)))
    x = (_pair((0, 1)), _pair((1, 0)))
    eye = (_pair((1, 0)), _pair((0, 1)))
    context_z = _kron(z, eye)
    context_eye = _kron(eye, z)
    context_x = _kron(x, x)
    inside = commutator_mass(context_z, context_eye)
    if inside != 0:
        raise _fail("the Z context does not commute", mass=str(inside))
    mass = commutator_mass(context_z, context_x)
    if mass == 0:
        raise _fail("the contexts commute, so there is no barrier")
    return mass


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the barrier mass 8."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(barrier_mass(), _MASS, "context barrier mass drifted")


def main() -> int:
    value = barrier_mass()
    print(value)
    if value == _MASS:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
