"""Exact residual of a rational 2 by 2 eigenpair.

Origin: lean4/LorentzBoost.lean theorem boost_eigenvalue_1
(mulVec2 boostNumeratorMat v1 = fun i => 8 * v1 i for v1 = (1, 1))
and theorem boost_eigenvalue_2
(mulVec2 boostNumeratorMat v2 = fun i => 2 * v2 i for v2 = (1, -1)),
where boostNumeratorMat is [[5, 3], [3, 5]].
Claim: urn:omega:fqm:witness:boost-eigenpair-residual:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_finite_witness.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: pair_residual returns the L1 norm of A v - lambda v for one
2 by 2 rational pair. eigenpair_residual adds that residual on the two
numerator eigenpairs above and requires the sum to be zero. The cited
theorems are integer matrix-vector identities. This file does not prove
them, does not divide by 4 to recover the rational boost, and does not
claim that no power of the boost is the identity.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_MATRIX: tuple[tuple[object, object], tuple[object, object]] = ((5, 3), (3, 5))
_LEFT: tuple[object, object] = (1, 1)
_RIGHT: tuple[object, object] = (1, -1)
_LEFT_EIGENVALUE = 8
_RIGHT_EIGENVALUE = 2


class FiniteWitnessError(Exception):
    """One violated eigenpair invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> FiniteWitnessError:
    return FiniteWitnessError(invariant, parameters)


def _require_tuple(value: object, role: str) -> tuple[object, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, tuple):
        raise _fail("eigenpair value is not a tuple", role=role, received=type(value).__name__)
    return tuple(value)


def _require_length(values: tuple[object, ...], length: int, role: str) -> tuple[object, ...]:
    if len(values) != length:
        raise _fail("eigenpair value has the wrong length", role=role, length=len(values))
    return values


def _require_rational(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the eigenpair boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("eigenpair entry is not an exact rational", role=role, received=type(value).__name__)


def _require_matrix(matrix: object) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    rows = _require_length(_require_tuple(matrix, "matrix"), 2, "matrix")
    top = _require_length(_require_tuple(rows[0], "row"), 2, "row")
    bottom = _require_length(_require_tuple(rows[1], "row"), 2, "row")
    return (
        (_require_rational(top[0], "entry"), _require_rational(top[1], "entry")),
        (_require_rational(bottom[0], "entry"), _require_rational(bottom[1], "entry")),
    )


def _require_vector(vector: object) -> tuple[Fraction, Fraction]:
    entries = _require_length(_require_tuple(vector, "vector"), 2, "vector")
    return (_require_rational(entries[0], "vector"), _require_rational(entries[1], "vector"))


def _scale(eigenvalue: Fraction, component: Fraction) -> Fraction:
    return eigenvalue * component


def _abs_ratio(value: Fraction) -> Fraction:
    if value < 0:
        return -value
    return value


def _image(row: tuple[Fraction, Fraction], vector: tuple[Fraction, Fraction]) -> Fraction:
    return row[0] * vector[0] + row[1] * vector[1]


def _component_residual(image: Fraction, eigenvalue: Fraction, component: Fraction) -> Fraction:
    gap = image - _scale(eigenvalue, component)
    return _abs_ratio(gap)


def pair_residual(matrix: object, vector: object, eigenvalue: object) -> Fraction:
    """Return |A v - lambda v|_1 for one rational 2 by 2 pair."""
    rows = _require_matrix(matrix)
    entries = _require_vector(vector)
    scale = _require_rational(eigenvalue, "eigenvalue")
    first = _component_residual(_image(rows[0], entries), scale, entries[0])
    second = _component_residual(_image(rows[1], entries), scale, entries[1])
    return first + second


def eigenpair_residual() -> Fraction:
    """Sum of the two boost-numerator eigenpair residuals. It must be zero."""
    left = pair_residual(_MATRIX, _LEFT, _LEFT_EIGENVALUE)
    right = pair_residual(_MATRIX, _RIGHT, _RIGHT_EIGENVALUE)
    total = left + right
    if total != 0:
        raise _fail("boost eigenpair residual is not zero", residual=str(total))
    return total


def main() -> int:
    value = eigenpair_residual()
    print(value)
    if value == 0:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
