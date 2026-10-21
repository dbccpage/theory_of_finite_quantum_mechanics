"""CLI collision sum for a rational probability vector.

Origin: lean4/DerivationDagQMClosure.lean theorem
fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census
((p + q)^2 = p^2 + q^2 + 2*p*q, and that defect is zero iff p = 0 or q = 0)
and theorem fq_embedding_relativity_and_entropy_baker_dichotomy_closure
(d^2 - (p^2 + (d - p)^2) = 2*(d*p - p^2) for an integer 2-outcome scale).
Claim: urn:omega:fqm:entropy:cli-collision-gap:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_entropy_cli.py.
Gate 5: use the source-bound measurements in the companion history.
Scope Fence: collision_probability sums squares of the rational weights it is
given after checking nonnegativity and unit mass. The cited theorems are a
Nat purity dichotomy and an integer 2-outcome deficit. They do not prove the
sum of squares for an arbitrary-length rational vector. parity_gap compares
(1, 0) with (1/2, 1/2) as that calculation. This file does not prove the
six-import census, the Baker gate, or the Galois sign flip.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

# Declared engineering policies; a refusal never rounds a probability.
MAX_OUTCOMES = 4096
MAX_SCALAR_BITS = 1024
MAX_WORK_BITS = 8192

_PURE: tuple[object, ...] = (1, 0)
_FAIR: tuple[object, ...] = (Fraction(1, 2), Fraction(1, 2))
_GAP = Fraction(1, 2)


class ParityError(Exception):
    """One violated parity-weight invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ParityError:
    return ParityError(invariant, parameters)


def _require_tuple(weights: object) -> tuple[object, ...]:
    if issubclass(type(weights), (str, bytes)) or not issubclass(type(weights), tuple):
        raise _fail("parity weights are not a tuple", received=type(weights).__name__)
    if type(weights) is not tuple:
        raise _fail("parity container subclass refused", received=type(weights).__name__)
    if len(weights) > MAX_OUTCOMES:
        raise _fail("parity vector budget exceeded", limit=MAX_OUTCOMES)
    return tuple(weights)


def _require_nonempty(weights: tuple[object, ...]) -> tuple[object, ...]:
    if len(weights) == 0:
        raise _fail("parity weights are empty")
    return weights


def _require_weight(value: object, index: int) -> Fraction:
    if issubclass(type(value), float):
        raise _fail("float refused at the parity boundary", index=index, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational weight was required", index=index)
    if type(value) is Fraction:
        weight = value
    elif type(value) is int:
        _require_bits(value, MAX_SCALAR_BITS, "weight", index)
        weight = Fraction(value)
    else:
        raise _fail("parity weight is not an exact rational", index=index, received=type(value).__name__)
    _require_fraction_bits(weight, MAX_SCALAR_BITS, "weight", index)
    if weight < 0:
        raise _fail("parity weight is negative", index=index, received=str(weight))
    return weight


def _require_bits(value: int, limit: int, role: str, index: int = -1) -> None:
    if value.bit_length() > limit:
        raise _fail("parity scalar bit budget exceeded", role=role, index=index, bits=value.bit_length(), limit=limit)


def _require_fraction_bits(value: Fraction, limit: int, role: str, index: int = -1) -> None:
    _require_bits(value.numerator, limit, role, index)
    _require_bits(value.denominator, limit, role, index)


def _collect_weights(weights: tuple[object, ...]) -> tuple[Fraction, ...]:
    collected: list[Fraction] = []
    for index, value in enumerate(weights):
        collected.append(_require_weight(value, index))
    return tuple(collected)


def _sum_mass(weights: tuple[Fraction, ...]) -> Fraction:
    total = Fraction(0)
    for weight in weights:
        total += weight
        _require_fraction_bits(total, MAX_WORK_BITS, "mass sum")
    return total


def _require_mass(total: Fraction) -> None:
    if total != 1:
        raise _fail("parity weights do not sum to one", total=str(total))


def _collision(weights: tuple[Fraction, ...]) -> Fraction:
    total = Fraction(0)
    for weight in weights:
        total += weight
        _require_fraction_bits(total, MAX_WORK_BITS, "collision sum")
    return total


def collision_probability(weights: object) -> Fraction:
    """Return the sum of squares for a nonnegative rational probability vector."""
    checked = _collect_weights(_require_nonempty(_require_tuple(weights)))
    _require_mass(_sum_mass(checked))
    return _collision(checked)


def parity_gap() -> Fraction:
    """Collision of (1, 0) minus collision of (1/2, 1/2)."""
    gap = collision_probability(_PURE) - collision_probability(_FAIR)
    if gap != _GAP:
        raise _fail("parity gap is not one half", gap=str(gap))
    return gap


def main() -> int:
    gap = parity_gap()
    try:
        print(gap)
    except (OSError, ValueError):
        return 2
    if gap == Fraction(1, 2):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
