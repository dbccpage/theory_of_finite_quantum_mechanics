"""Degree-zero cup product on a shared vertex set. (a cup b)(v) = a(v) b(v).

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/cup_product.py
Claim: urn:omega:fqm:ms-majorana:cup-product:degree-zero:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: This is the cup product of 0-cochains only. It is not the Alexander-Whitney product in positive degree.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class CupProductError(ValueError):
    """One violated cup-product invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CupProductError:
    return CupProductError(invariant, parameters)


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


def _vertex(value: object, role: str) -> int:
    if isinstance(value, bool) or type(value) is not int:
        raise _fail("vertex is not an exact index", role=role, received=type(value).__name__)
    return value


@dataclass(frozen=True)
class SparseCochain:
    """A degree-zero cochain stored as vertex/value pairs."""

    degree: int
    terms: tuple[tuple[int, Fraction], ...]


def _terms(values: object, role: str) -> tuple[tuple[int, Fraction], ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("cochain terms must be a sequence", role=role, received=type(values).__name__)
    parsed: list[tuple[int, Fraction]] = []
    seen: set[int] = set()
    for index, item in enumerate(values):
        if isinstance(item, (str, bytes)) or not isinstance(item, Sequence) or len(item) != 2:
            raise _fail("cochain term must be a pair", role=f"{role}[{index}]", received=type(item).__name__)
        vertex = _vertex(item[0], f"{role}[{index}][0]")
        if vertex in seen:
            raise _fail("cochain vertex is repeated", vertex=vertex)
        seen.add(vertex)
        parsed.append((vertex, _rational(item[1], f"{role}[{index}][1]")))
    return tuple(sorted(parsed, key=lambda term: term[0]))


def cochain(terms: object) -> SparseCochain:
    """Admit a degree-zero cochain."""
    return SparseCochain(0, _terms(terms, "terms"))


@dataclass(frozen=True)
class CupProduct:
    """The degree-zero product of two cochains."""

    left_degree: int
    right_degree: int
    result: SparseCochain

    @staticmethod
    def of(left: SparseCochain, right: SparseCochain) -> CupProduct:
        if not isinstance(left, SparseCochain) or not isinstance(right, SparseCochain):
            raise _fail("cup product requires two cochains")
        if left.degree != 0 or right.degree != 0:
            raise _fail("only degree-zero cochains are admitted", left=left.degree, right=right.degree)
        right_map = dict(right.terms)
        product: list[tuple[int, Fraction]] = []
        for vertex, coeff in left.terms:
            if vertex in right_map:
                product.append((vertex, coeff * right_map[vertex]))
        result = SparseCochain(0, tuple(product))
        return CupProduct(left.degree, right.degree, result)


def certify_unit(values: object) -> CupProduct:
    """Recheck that cup with the constant cochain 1 reproduces the input on its support."""
    left = cochain(values)
    unit_terms = tuple((vertex, Fraction(1)) for vertex, _coeff in left.terms)
    product = CupProduct.of(left, SparseCochain(0, unit_terms))
    if product.result.terms != left.terms:
        raise _fail("degree-zero cup with 1 did not reproduce the cochain")
    return product


__all__ = ["CupProduct", "CupProductError", "SparseCochain", "certify_unit", "cochain"]
