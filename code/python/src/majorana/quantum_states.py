"""Exact real rank-one Gram matrix. Complex amplitudes and floats are refused.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/quantum_states.py
Claim: urn:omega:fqm:ms-majorana:quantum-states:rational-gram:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: The Gram matrix is not a density operator, not a Born rule, and not a complex projector.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class StateError(ValueError):
    """One violated Gram invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> StateError:
    return StateError(invariant, parameters)


def _rational(value: object, role: str) -> Fraction:
    if isinstance(value, float) or isinstance(value, complex):
        raise _fail("float refused at the public boundary", role=role, received=type(value).__name__)
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _vector(values: object) -> tuple[Fraction, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or len(values) == 0:
        raise _fail("state must be a nonempty sequence", received=type(values).__name__)
    return tuple(_rational(item, f"state[{index}]") for index, item in enumerate(values))


def _row(left: Fraction, coords: Sequence[Fraction]) -> tuple[Fraction, ...]:
    return tuple(left * right for right in coords)


def density(psi: object) -> tuple[tuple[Fraction, ...], ...]:
    """Return the rank-one matrix psi psi^T over the rationals."""
    coords = _vector(psi)
    return tuple(_row(left, coords) for left in coords)


def _trace(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    total = Fraction(0)
    for index, row in enumerate(matrix):
        total += row[index]
    return total


def _norm_sq(coords: Sequence[Fraction]) -> Fraction:
    total = Fraction(0)
    for coord in coords:
        total += coord * coord
    return total


@dataclass(frozen=True)
class GramCertificate:
    """Witness that the Gram matrix is symmetric and its trace is the squared norm."""

    coords: tuple[Fraction, ...]
    matrix: tuple[tuple[Fraction, ...], ...]
    trace: Fraction


def certify_gram(psi: object) -> GramCertificate:
    """Recheck symmetry and the trace identity."""
    coords = _vector(psi)
    matrix = density(coords)
    trace = _trace(matrix)
    if trace != _norm_sq(coords):
        raise _fail("Gram trace is not the squared norm", trace=str(trace))
    for left, row in enumerate(matrix):
        for right, entry in enumerate(row):
            if entry != matrix[right][left]:
                raise _fail("Gram matrix is not symmetric", row=left, column=right)
    return GramCertificate(coords, matrix, trace)


__all__ = ["GramCertificate", "StateError", "certify_gram", "density"]
