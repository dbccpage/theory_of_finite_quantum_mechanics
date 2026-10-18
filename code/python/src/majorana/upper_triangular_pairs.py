"""Diagonal product of an upper-triangular rational matrix agrees with its determinant.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/upper_triangular_pairs.py
Claim: urn:omega:fqm:ms-majorana:upper-triangular:determinant:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: Only sizes 1, 2, and 3 are certified. This file does not claim a general Leibniz expansion.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class TriangularError(ValueError):
    """One violated triangular invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> TriangularError:
    return TriangularError(invariant, parameters)


def _rational(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _matrix(values: object) -> tuple[tuple[Fraction, ...], ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or len(values) == 0:
        raise _fail("matrix must be a nonempty sequence of rows", received=type(values).__name__)
    rows = tuple(
        tuple(_rational(entry, f"matrix[{row}][{column}]") for column, entry in enumerate(_row(item, row)))
        for row, item in enumerate(values)
    )
    width = len(rows)
    for index, row in enumerate(rows):
        if len(row) != width:
            raise _fail("matrix is not square", row=index, length=len(row), expected=width)
    if width > 3:
        raise _fail("triangular certificate admits size at most 3", size=width)
    return rows


def _row(values: object, index: int) -> Sequence[object]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("matrix row must be a sequence", row=index, received=type(values).__name__)
    return values


def _upper(matrix: Sequence[Sequence[Fraction]]) -> None:
    for row, entries in enumerate(matrix):
        for column, entry in enumerate(entries):
            if column < row and entry != 0:
                raise _fail("matrix is not upper triangular", row=row, column=column, entry=str(entry))


def _product(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    total = Fraction(1)
    for index, row in enumerate(matrix):
        total *= row[index]
    return total


def _det(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    if size == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return _det3(matrix)


def _det3(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


@dataclass(frozen=True)
class TriangularCertificate:
    """Witness that the diagonal product equals the determinant."""

    diagonal_product: Fraction
    determinant: Fraction


def certify_upper_triangular(matrix: object) -> TriangularCertificate:
    """Refuse a lower entry and recheck the determinant identity."""
    parsed = _matrix(matrix)
    _upper(parsed)
    product = _product(parsed)
    determinant = _det(parsed)
    if product != determinant:
        raise _fail(
            "diagonal product is not the determinant",
            product=str(product),
            determinant=str(determinant),
        )
    return TriangularCertificate(product, determinant)


__all__ = ["TriangularCertificate", "TriangularError", "certify_upper_triangular"]
