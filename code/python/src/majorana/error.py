"""Typed homology failures. A nonzero boundary square records its exact defect.

Origin: papers/derivations/ms_majorana/lean4/MajoranaCore.lean theorem nilpotency_refusal_sound
Claim: urn:omega:fqm:ms-majorana:error:nilpotency-defect:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: The defect is an exact rational sum of absolute entries. It is not a numerical tolerance.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class HomologyError(ValueError):
    """Base failure. Each instance names the invariant it violated."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


class BoundarySquaredNonzero(HomologyError):
    """d squared is not the zero matrix."""


def _fail(invariant: str, **parameters: object) -> BoundarySquaredNonzero:
    return BoundarySquaredNonzero(invariant, parameters)


def _rational(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise HomologyError("float refused at the public boundary", {"role": role, "received": "float"})
    if isinstance(value, bool):
        raise HomologyError("boolean refused where a rational was required", {"role": role})
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise HomologyError("value is not an exact rational", {"role": role, "received": type(value).__name__})


def _entries(values: object) -> tuple[Fraction, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise HomologyError("defect entries must be a sequence", {"received": type(values).__name__})
    return tuple(_rational(item, f"entries[{index}]") for index, item in enumerate(values))


def _absolute_sum(entries: Sequence[Fraction]) -> Fraction:
    total = Fraction(0)
    for entry in entries:
        if entry < 0:
            total -= entry
        else:
            total += entry
    return total


@dataclass(frozen=True)
class NilpotencyCertificate:
    """Witness that every supplied product entry is zero."""

    defect: Fraction


def certify_boundary_square(entries: object) -> NilpotencyCertificate:
    """Accept the product only when the exact absolute defect is zero."""
    parsed = _entries(entries)
    defect = _absolute_sum(parsed)
    if defect != 0:
        raise _fail("boundary square is not zero", defect=str(defect), entries=len(parsed))
    return NilpotencyCertificate(defect)


__all__ = [
    "BoundarySquaredNonzero",
    "HomologyError",
    "NilpotencyCertificate",
    "certify_boundary_square",
]
