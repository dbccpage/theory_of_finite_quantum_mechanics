"""Exact agreement of two purity expressions for a rational weight vector.

Origin: lean4/DerivationDagQMClosure.lean definition purityDiag3
(w0 * w0 + w1 * w1 + w2 * w2) and theorem
qm020_thm4_hilbert_lift_redundancy
(purityDiag3 w0 w1 w2 < purityRankOneExpanded3 w0 w1 w2 whenever
0 < w0 * w1, and purityRankOneExpanded3 2 3 5 = (2 + 3 + 5) * (2 + 3 + 5)).
Claim: urn:omega:fqm:entropy:purity-expression-gap:v1
AuthorityEffect: None
Mutation-Kills: 9 non-equivalent source mutants, executed by code/python/tests/test_entropy_solver.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 6; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: purity_gap returns (sum w_i^2) / (sum w_i)^2 for a nonempty
tuple of nonnegative exact rationals with positive mass, after checking that
this ratio equals the sum of squares of the normalized weights.
certified_purity checks that value on (1/2, 1/3, 1/6). The cited definition
and theorem are three natural-number weights and a rank-one lift. This file
does not prove that inequality, does not build a density matrix, and does
not claim the Renyi purity dichotomy.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_FIXTURE: tuple[object, ...] = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
_FIXTURE_PURITY = Fraction(7, 18)


class EntropySolverError(Exception):
    """One violated purity-expression invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> EntropySolverError:
    return EntropySolverError(invariant, parameters)


def _require_tuple(weights: object) -> tuple[object, ...]:
    if isinstance(weights, (str, bytes)) or not isinstance(weights, tuple):
        raise _fail("purity weights are not a tuple", received=type(weights).__name__)
    return tuple(weights)


def _require_nonempty(weights: tuple[object, ...]) -> tuple[object, ...]:
    if len(weights) == 0:
        raise _fail("purity weights are empty")
    return weights


def _require_weight(value: object, index: int) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the purity boundary", index=index, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational weight was required", index=index)
    if isinstance(value, Fraction):
        num, den = value.numerator, value.denominator
    elif type(value) is int:
        num, den = value, 1
    else:
        raise _fail("purity weight is not an exact rational", index=index, received=type(value).__name__)
    if type(num) is not int or type(den) is not int:
        raise _fail("exact rational numerator and denominator must be int", index=index)
    if num.bit_length() > 1024 or den.bit_length() > 1024:
        raise _fail("integer exceeds 1024 bits", index=index)
    weight = Fraction(num, den)
    if weight < 0:
        raise _fail("purity weight is negative", index=index, received=str(weight))
    return weight


def _collect(weights: tuple[object, ...]) -> tuple[Fraction, ...]:
    collected: list[Fraction] = []
    for index, value in enumerate(weights):
        collected.append(_require_weight(value, index))
    return tuple(collected)


def _sum_mass(weights: tuple[Fraction, ...]) -> Fraction:
    total = Fraction(0)
    for weight in weights:
        total += weight
    return total


def _require_positive_mass(total: Fraction) -> None:
    if total == 0:
        raise _fail("purity weights have zero mass", total=str(total))


def _square(weight: Fraction) -> Fraction:
    return weight * weight


def _square_sum(weights: tuple[Fraction, ...]) -> Fraction:
    total = Fraction(0)
    for weight in weights:
        total += _square(weight)
    return total


def _normalized_square_sum(weights: tuple[Fraction, ...], mass: Fraction) -> Fraction:
    total = Fraction(0)
    for weight in weights:
        scaled = weight / mass
        total += scaled * scaled
    return total


def purity_gap(weights: object) -> Fraction:
    """Return (sum w_i^2) / (sum w_i)^2 after the two purity expressions agree."""
    checked = _collect(_require_nonempty(_require_tuple(weights)))
    mass = _sum_mass(checked)
    _require_positive_mass(mass)
    by_ratio = _square_sum(checked) / (mass * mass)
    by_normalization = _normalized_square_sum(checked, mass)
    gap = by_ratio - by_normalization
    if gap != 0:
        raise _fail("purity expressions differ", gap=str(gap))
    return by_normalization


def certified_purity() -> Fraction:
    """Normalized purity of (1/2, 1/3, 1/6)."""
    value = purity_gap(_FIXTURE)
    if value != _FIXTURE_PURITY:
        raise _fail("certified purity is not seven eighteenths", purity=str(value))
    return value


def main() -> int:
    value = certified_purity()
    print(value)
    if value == Fraction(7, 18):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
