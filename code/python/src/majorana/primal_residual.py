"""F2 coset weight. The weight of w + correction is recomputed by count and by sum.

Origin: papers/derivations/ms_majorana/lean4/MajoranaCore.lean theorem candidate_gauge_is_upper_bound
Claim: urn:omega:fqm:ms-majorana:primal-residual:f2-coset-weight:v1
AuthorityEffect: None
Mutation-Kills: 5 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: The correction is supplied data. This file does not solve for a minimum-weight gauge and does not certify a hardware syndrome.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


class PrimalResidualError(ValueError):
    """One violated coset-weight invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> PrimalResidualError:
    return PrimalResidualError(invariant, parameters)


def _bit(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool) or type(value) is not int:
        raise _fail("boolean or non-bit refused", role=role, received=type(value).__name__)
    if value not in (0, 1):
        raise _fail("F2 coordinate is not 0 or 1", role=role, received=value)
    return value


def _bits(values: object, role: str) -> tuple[int, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("F2 vector must be a sequence", role=role, received=type(values).__name__)
    return tuple(_bit(item, f"{role}[{index}]") for index, item in enumerate(values))


def _count(bits: Sequence[int]) -> int:
    total = 0
    for bit in bits:
        if bit == 1:
            total += 1
    return total


def _sum(bits: Sequence[int]) -> int:
    total = 0
    for bit in bits:
        total += bit
    return total


@dataclass(frozen=True)
class CosetWeightCertificate:
    """Witness that count and sum agree on w + correction."""

    combined: tuple[int, ...]
    weight: int


def certify_coset_weight(witness: object, correction: object) -> CosetWeightCertificate:
    """Add the supplied correction in F2 and recheck the weight two ways."""
    left = _bits(witness, "witness")
    right = _bits(correction, "correction")
    if len(left) != len(right):
        raise _fail("correction length does not match the witness", witness=len(left), correction=len(right))
    combined = tuple((a + b) % 2 for a, b in zip(left, right))
    counted = _count(combined)
    summed = _sum(combined)
    if counted != summed:
        raise _fail("F2 weight recount disagreed", counted=counted, summed=summed)
    return CosetWeightCertificate(combined, counted)


def verify_primal_dual_certificate(witness: object, correction: object) -> CosetWeightCertificate:
    """Public name kept for the coset-weight certificate."""
    return certify_coset_weight(witness, correction)


__all__ = [
    "CosetWeightCertificate",
    "PrimalResidualError",
    "certify_coset_weight",
    "verify_primal_dual_certificate",
]
