"""Exact certificate that two rational matrices compose to zero.

Origin: lean4/FiniteCochain.lean theorem d1_d0_zero.
Claim: urn:omega:fqm:cochain:composition-zero-certificate:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_composition_zero.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: This file certifies only the matrices it is given. It does not
prove d1 ∘ d0 = 0 for every cochain, and it does not inherit an authority
grant from a zero defect.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, Sequence


class HomologyError(ValueError):
    """One violated composition invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


class NonZeroCompositionError(HomologyError):
    """The rational matrix product is not the zero matrix."""


class DimensionMismatchError(HomologyError):
    """The matrices do not have a defined rational composition."""


def _fail(kind: type[HomologyError], invariant: str, **parameters: object) -> HomologyError:
    return kind(invariant, parameters)


def require_rational(value: object, role: str) -> Fraction:
    """Accept int or Fraction only. Float and bool are refused."""
    if isinstance(value, float):
        raise _fail(HomologyError, "float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail(HomologyError, "boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail(HomologyError, "value is not an exact rational", role=role, received=type(value).__name__)


def _require_row(row: object, role: str, index: int, width: int | None) -> tuple[Fraction, ...]:
    if isinstance(row, (str, bytes)) or not isinstance(row, Sequence) or len(row) == 0:
        raise _fail(DimensionMismatchError, "matrix row is empty or not a vector", role=role, row=index)
    parsed = tuple(require_rational(item, f"{role}[{index}][{column}]") for column, item in enumerate(row))
    if width is not None and len(parsed) != width:
        raise _fail(
            DimensionMismatchError,
            "jagged rational matrices cannot be composed",
            role=role,
            row=index,
            expected=width,
            actual=len(parsed),
        )
    return parsed


def _require_rows(values: object, role: str) -> tuple[tuple[Fraction, ...], ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or len(values) == 0:
        raise _fail(
            DimensionMismatchError,
            "composition requires nonempty matrices",
            role=role,
            received=type(values).__name__,
        )
    parsed: list[tuple[Fraction, ...]] = []
    width: int | None = None
    for index, row in enumerate(values):
        parsed_row = _require_row(row, role, index, width)
        width = len(parsed_row)
        parsed.append(parsed_row)
    return tuple(parsed)


def _require_product_shape(left_columns: int, right_rows: int) -> None:
    if right_rows != left_columns:
        raise _fail(
            DimensionMismatchError,
            "cannot compose widths",
            left_columns=left_columns,
            right_rows=right_rows,
        )


def _dot_column(row: Sequence[Fraction], right: Sequence[Sequence[Fraction]], column: int) -> Fraction:
    total = Fraction(0)
    for index, entry in enumerate(row):
        total += entry * right[index][column]
    return total


def _composition_defect(
    left: Sequence[Sequence[Fraction]],
    right: Sequence[Sequence[Fraction]],
) -> Fraction:
    defect = Fraction(0)
    columns = len(right[0])
    for row in left:
        for column in range(columns):
            defect += abs(_dot_column(row, right, column))
    return defect


def require_composition_zero(left: object, right: object) -> Fraction:
    """Return 0 when left * right is the zero matrix, else a typed defect."""
    parsed_left = _require_rows(left, "left")
    parsed_right = _require_rows(right, "right")
    _require_product_shape(len(parsed_left[0]), len(parsed_right))
    defect = _composition_defect(parsed_left, parsed_right)
    if defect != 0:
        raise _fail(NonZeroCompositionError, "composition defect is not zero", defect=str(defect))
    return defect


def triangle_composition_defect() -> Fraction:
    """∂1 ∂2 for the standard triangle, checked through require_composition_zero."""
    edge = (
        (Fraction(-1), Fraction(-1), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(-1)),
        (Fraction(0), Fraction(1), Fraction(1)),
    )
    face = ((Fraction(1),), (Fraction(-1),), (Fraction(1),))
    return require_composition_zero(edge, face)


__all__ = [
    "DimensionMismatchError",
    "HomologyError",
    "NonZeroCompositionError",
    "require_composition_zero",
    "require_rational",
    "triangle_composition_defect",
]
