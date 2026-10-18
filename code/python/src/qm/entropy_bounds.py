"""Exact Cauchy collision bound for a rational probability triple.

Origin: lean4/DerivationDagQMClosure.lean theorem
signed_sqrt_density_lift_cauchy_schwarz
(0 ≤ sqDiffSum3 w0 w1 w2 and sqDiffSum3 w0 w0 w0 = 0, where
sqDiffSum3 = (w0 - w1)^2 + (w1 - w2)^2 + (w2 - w0)^2 and the
declaration states that this sum equals 3 * Gamma_2 - Phi_1^2).
Claim: urn:omega:fqm:entropy:cauchy-collision-bound:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_entropy_bounds.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 6; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: collision_probability returns the sum of squares of a length-3
nonnegative rational probability vector. cauchy_defect returns the pairwise
squared-difference sum of that same triple. certified_collision checks those
two against 3 * sum p_i^2 - 1 for the weights (1/2, 1/3, 1/6). The cited
theorem is an integer identity with no unit-mass hypothesis. This file does
not prove that theorem, does not extend Cauchy-Schwarz past three weights,
and does not claim a signed square root or a density lift.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_WIDTH = 3
_FIXTURE: tuple[object, ...] = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
_FIXTURE_COLLISION = Fraction(7, 18)


class EntropyBoundError(Exception):
    """One violated collision-bound invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> EntropyBoundError:
    return EntropyBoundError(invariant, parameters)


def _require_tuple(weights: object) -> tuple[object, ...]:
    if isinstance(weights, (str, bytes)) or not isinstance(weights, tuple):
        raise _fail("collision weights are not a tuple", received=type(weights).__name__)
    return tuple(weights)


def _require_triple(weights: tuple[object, ...]) -> tuple[object, ...]:
    if len(weights) != _WIDTH:
        raise _fail("collision weights are not a triple", length=len(weights))
    return weights


def _require_weight(value: object, index: int) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the collision boundary", index=index, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational weight was required", index=index)
    if isinstance(value, Fraction):
        weight = value
    elif type(value) is int:
        weight = Fraction(value)
    else:
        raise _fail("collision weight is not an exact rational", index=index, received=type(value).__name__)
    if weight < 0:
        raise _fail("collision weight is negative", index=index, received=str(weight))
    return weight


def _collect(weights: tuple[object, ...]) -> tuple[Fraction, Fraction, Fraction]:
    return (
        _require_weight(weights[0], 0),
        _require_weight(weights[1], 1),
        _require_weight(weights[2], 2),
    )


def _mass(weights: tuple[Fraction, Fraction, Fraction]) -> Fraction:
    return weights[0] + weights[1] + weights[2]


def _require_mass(total: Fraction) -> None:
    if total != 1:
        raise _fail("collision weights do not sum to one", total=str(total))


def _square(weight: Fraction) -> Fraction:
    return weight * weight


def _collision(weights: tuple[Fraction, Fraction, Fraction]) -> Fraction:
    return _square(weights[0]) + _square(weights[1]) + _square(weights[2])


def _pair_square(left: Fraction, right: Fraction) -> Fraction:
    gap = left - right
    return gap * gap


def _prepare(weights: object) -> tuple[Fraction, Fraction, Fraction]:
    return _collect(_require_triple(_require_tuple(weights)))


def collision_probability(weights: object) -> Fraction:
    """Return the sum of squares for a nonnegative rational probability triple."""
    triple = _prepare(weights)
    _require_mass(_mass(triple))
    return _collision(triple)


def cauchy_defect(weights: object) -> Fraction:
    """Return (p0-p1)^2 + (p1-p2)^2 + (p2-p0)^2 for a probability triple."""
    triple = _prepare(weights)
    _require_mass(_mass(triple))
    first = _pair_square(triple[0], triple[1])
    second = _pair_square(triple[1], triple[2])
    third = _pair_square(triple[2], triple[0])
    return first + second + third


def certified_collision() -> Fraction:
    """Collision of (1/2, 1/3, 1/6), checked against the pairwise Cauchy defect."""
    collision = collision_probability(_FIXTURE)
    defect = cauchy_defect(_FIXTURE)
    expected = Fraction(_WIDTH) * collision - Fraction(1)
    if defect != expected:
        raise _fail("pairwise Cauchy identity failed", defect=str(defect), expected=str(expected))
    if collision != _FIXTURE_COLLISION:
        raise _fail("certified collision is not seven eighteenths", collision=str(collision))
    return collision


def main() -> int:
    value = certified_collision()
    print(value)
    if value == Fraction(7, 18):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
