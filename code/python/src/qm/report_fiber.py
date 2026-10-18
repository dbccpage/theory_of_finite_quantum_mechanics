"""Named relative-phase fiber on two Gaussian integer vectors.

Origin: lean4/QuotientFiber.lean theorem psi1_psi2_in_same_fiber
(phaseRel psi1 psi2), theorem psi1_psi2_distinct (psi1 ≠ psi2), and
theorem fiber_exceeds_global_gauge_orbit (no GaussInt u multiplies psi1
onto psi2). psi1 is GaussInt.one at both Bool values. psi2 is
GaussInt.one at false and GaussInt.neg GaussInt.one at true. phaseBlind
is GaussInt.sqMod. The default witness also checks
lean4/PhaseBlindPresentation.lean theorem global_phase_blind: GaussInt.mul
by GaussInt.i preserves sqMod, and lean4/GaussIntKernel.lean theorem
sqMod_nonneg.
Claim: urn:omega:fqm:fiber:relative-phase-count:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_report_fiber.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: relative_fiber_size returns 2 when the two vectors are
distinct and have equal phase-blind weights. On the named pair it also
requires the two components of psi2 to differ, which is the scalar
obstruction, and requires i * GaussInt.one to keep sqMod 1. Supplied
vectors skip that named obstruction. This file does not enumerate rational
sign patterns of (3/5, 4/5), does not prove the phase setoid, and does not
claim that every unit multiple stays in the fiber.
"""

from __future__ import annotations

from typing import Mapping

_ONE: tuple[int, int] = (1, 0)
_NEG_ONE: tuple[int, int] = (-1, 0)
_PSI1: tuple[tuple[int, int], tuple[int, int]] = (_ONE, _ONE)
_PSI2: tuple[tuple[int, int], tuple[int, int]] = (_ONE, _NEG_ONE)
_I: tuple[int, int] = (0, 1)


class ReportFiberError(Exception):
    """One violated fiber invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ReportFiberError:
    return ReportFiberError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the gaussian boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer part was required", role=role)
    if type(value) is int:
        return value
    raise _fail("gaussian part is not an integer", role=role, received=type(value).__name__)


def _require_pair(pair: object, role: str) -> tuple[int, int]:
    if isinstance(pair, (str, bytes)) or not isinstance(pair, tuple):
        raise _fail("gaussian integer is not a tuple", role=role, received=type(pair).__name__)
    if len(pair) != 2:
        raise _fail("gaussian integer is not a pair", role=role, length=len(pair))
    return (_require_int(pair[0], role), _require_int(pair[1], role))


def _require_vector(vector: object) -> tuple[tuple[int, int], tuple[int, int]]:
    if isinstance(vector, (str, bytes)) or not isinstance(vector, tuple):
        raise _fail("amplitude vector is not a tuple", received=type(vector).__name__)
    if len(vector) != 2:
        raise _fail("amplitude vector is not a pair", length=len(vector))
    return (_require_pair(vector[0], "false"), _require_pair(vector[1], "true"))


def _choose_vector(
    vector: object | None,
    default: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    if vector is None:
        return default
    return _require_vector(vector)


def _sq(component: tuple[int, int]) -> int:
    real, imag = component
    return real * real + imag * imag


def _weights(vector: tuple[tuple[int, int], tuple[int, int]]) -> tuple[int, int]:
    return (_sq(vector[0]), _sq(vector[1]))


def _mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _require_phase_blind(component: tuple[int, int]) -> None:
    turned = _mul(_I, component)
    if _sq(turned) != _sq(component):
        raise _fail(
            "i-multiple changed the phase-blind weight",
            origin=_sq(component),
            image=_sq(turned),
        )


def _require_scalar_gap(vector: tuple[tuple[int, int], tuple[int, int]]) -> None:
    if vector[0] == vector[1]:
        raise _fail("global scalar was not excluded")


def phase_weight(component: object) -> int:
    """Return GaussInt.sqMod of one integer pair."""
    pair = _require_pair(component, "component")
    weight = _sq(pair)
    if weight < 0:
        raise _fail("phase-blind weight is negative", weight=weight)
    return weight


def relative_fiber_size(left: object | None = None, right: object | None = None) -> int:
    """Return 2 for the named psi1/psi2 fiber, or for another distinct equal-weight pair."""
    first = _choose_vector(left, _PSI1)
    second = _choose_vector(right, _PSI2)
    if _weights(first) != _weights(second):
        raise _fail("phase-blind weights differ", left=str(_weights(first)), right=str(_weights(second)))
    if first == second:
        raise _fail("vectors are not distinct")
    if left is None and right is None:
        _require_scalar_gap(second)
        _require_phase_blind(_ONE)
    return 2


def main() -> int:
    value = relative_fiber_size()
    print(value)
    if value == 2 and phase_weight(_ONE) == 1:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
