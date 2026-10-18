"""F2 cocycle certificate: a cochain is closed when its coboundary bit is zero.

Origin: papers/derivations/ms_majorana/lean4/MajoranaCore.lean def is_cocycle
Claim: urn:omega:fqm:ms-majorana:cocycle:f2-linear-form:v1
AuthorityEffect: None
Mutation-Kills: 5 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: This file decides one F2 linear form. It does not decide the full trichotomy.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


class CocycleError(ValueError):
    """One violated cocycle invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CocycleError:
    return CocycleError(invariant, parameters)


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


def _dot(left: Sequence[int], right: Sequence[int]) -> int:
    total = 0
    for coeff, bit in zip(left, right):
        total = (total + coeff * bit) % 2
    return total


@dataclass(frozen=True)
class Cocycle:
    """Witness that the coboundary linear form evaluates to zero."""

    cochain: tuple[int, ...]
    coefficients: tuple[int, ...]
    image: int


def try_cocycle(coefficients: object, cochain: object) -> Cocycle:
    """Accept the cochain only when the F2 coboundary bit is zero."""
    form = _bits(coefficients, "coefficients")
    vector = _bits(cochain, "cochain")
    if len(form) != len(vector):
        raise _fail("cocycle form length does not match the cochain", form=len(form), cochain=len(vector))
    image = _dot(form, vector)
    if image != 0:
        raise _fail("cochain is not an F2 cocycle", image=image)
    return Cocycle(vector, form, image)


__all__ = ["Cocycle", "CocycleError", "try_cocycle"]
