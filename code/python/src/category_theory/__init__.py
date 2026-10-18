"""Frozen arrow-category certificate and one compatible report-query decoder.

Origin: code/rust/src/category_theory/finite_report_query.rs struct
FactorizationCertificate, rechecked against the arrow presented in
code/python/src/category_theory/finite_category.py.
Claim: urn:omega:fqm:category:exported-arrow-decoder:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/category_theory/test_arrow_decoder.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 3; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: arrow_decoder_size checks one two-object arrow category and one
three-point report. It does not classify finite categories and does not
inherit an authority grant from a passing witness.
"""

from __future__ import annotations

from typing import Mapping

from .finite_category import (
    CategoryLawError,
    FiniteCategory,
    factor_report_query,
    verify_report_query_factorization,
)

__all__ = [
    "CategoryLawError",
    "FiniteCategory",
    "arrow_decoder_size",
    "factor_report_query",
    "verify_report_query_factorization",
]

_REPORT: tuple[tuple[int, int], ...] = ((0, 10), (1, 10), (2, 20))
_QUERY: tuple[tuple[int, int], ...] = ((0, 1), (1, 1), (2, 0))


def _fail(invariant: str, **parameters: object) -> CategoryLawError:
    return CategoryLawError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _exact_int(value: object, role: str) -> int:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where an integer label was required", role=role)
    if type(value) is not int:
        raise _fail("label is not an exact integer", role=role, received=type(value).__name__)
    return value


def _pair(row: object, role: str) -> tuple[int, int]:
    if isinstance(row, (str, bytes)) or not isinstance(row, tuple) or len(row) != 2:
        raise _fail("witness pair must contain two integers", role=role, received=type(row).__name__)
    return (_exact_int(row[0], role + "_0"), _exact_int(row[1], role + "_1"))


def _table(rows: object, role: str) -> dict[int, int]:
    if isinstance(rows, (str, bytes)) or not isinstance(rows, tuple) or len(rows) == 0:
        raise _fail("witness table must be a nonempty tuple", role=role, received=type(rows).__name__)
    parsed = [_pair(row, role) for row in rows]
    return {key: value for key, value in parsed}


def _arrow_category() -> FiniteCategory:
    return FiniteCategory(
        objects=frozenset({"A", "B"}),
        morphisms={"id_A": ("A", "A"), "id_B": ("B", "B"), "f": ("A", "B")},
        identities={"A": "id_A", "B": "id_B"},
        composition={
            ("id_A", "id_A"): "id_A",
            ("id_B", "id_B"): "id_B",
            ("f", "id_A"): "f",
            ("id_B", "f"): "f",
        },
    )


def _require_arrow(category: FiniteCategory) -> None:
    if category.verify_axioms() is not True:
        raise _fail("arrow category failed identity, unit, or associativity")


def _require_decoder(decoder: Mapping[int, int]) -> int:
    if dict(decoder) != {10: 1, 20: 0}:
        raise _fail("compatible query did not decode through the report", received=str(dict(decoder)))
    return len(decoder)


def arrow_decoder_size(report: object = None, query: object = None) -> int:
    """Size of the frozen compatible decoder. The default witness returns 2."""
    report_rows = _REPORT if report is None else report
    query_rows = _QUERY if query is None else query
    _require_arrow(_arrow_category())
    return _require_decoder(factor_report_query(_table(report_rows, "report"), _table(query_rows, "query")))
