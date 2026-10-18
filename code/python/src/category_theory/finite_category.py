"""Finite categories and report-query factorization over an explicit table.

Origin: code/rust/src/category_theory/category/category.rs struct FiniteCategoryShell
and code/rust/src/category_theory/finite_report_query.rs struct FactorizationCertificate.
Claim: urn:omega:fqm:category:finite-arrow-factorization:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/category_theory/test_finite_category.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 4.
Scope Fence: Identity, unit, and associativity are checked on the morphisms
that were supplied. Factorization is the set-theoretic decoder of one total
table. This file does not claim a free category, a topos, or that every
query factors.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Tuple


class CategoryLawError(ValueError):
    """One violated finite-category invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CategoryLawError:
    return CategoryLawError(invariant, parameters)


def _exact_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer label was required", role=role)
    if type(value) is not int:
        raise _fail("label is not an exact integer", role=role, received=type(value).__name__)
    return value


@dataclass(frozen=True)
class FiniteCategory:
    """Finite category presented by objects, morphisms, identities, and a composition table."""

    objects: frozenset[str]
    morphisms: Dict[str, Tuple[str, str]]
    identities: Dict[str, str]
    composition: Dict[Tuple[str, str], str]

    def _identity_endpoints(self) -> bool:
        for obj in self.objects:
            if obj not in self.identities:
                return False
            if self.morphisms.get(self.identities[obj]) != (obj, obj):
                return False
        return True

    def _unit_laws(self) -> bool:
        for name, (source, target) in self.morphisms.items():
            if not self._unit_one(name, source, target):
                return False
        return True

    def _unit_one(self, name: str, source: str, target: str) -> bool:
        left = self.identities.get(source)
        right = self.identities.get(target)
        if left is None or right is None:
            return False
        if self.composition.get((name, left)) != name:
            return False
        return self.composition.get((right, name)) == name

    def _associative(self) -> bool:
        for name, (_source, target) in self.morphisms.items():
            if not self._assoc_from(name, target):
                return False
        return True

    def _assoc_from(self, left: str, target: str) -> bool:
        for middle, (source, codomain) in self.morphisms.items():
            if source != target:
                continue
            if not self._assoc_triple(left, middle, codomain):
                return False
        return True

    def _assoc_triple(self, left: str, middle: str, codomain: str) -> bool:
        composed = self.composition.get((middle, left))
        if composed is None:
            return False
        return self._assoc_right(left, middle, composed, codomain)

    def _assoc_right(self, left: str, middle: str, composed: str, codomain: str) -> bool:
        for right, (source, _ignored) in self.morphisms.items():
            if source != codomain:
                continue
            if not self._assoc_pair(left, middle, composed, right):
                return False
        return True

    def _assoc_pair(self, left: str, middle: str, composed: str, right: str) -> bool:
        other = self.composition.get((right, middle))
        if other is None:
            return False
        return self.composition.get((right, composed)) == self.composition.get((other, left))

    def verify_axioms(self) -> bool:
        """Return whether identity, unit, and associativity hold on this table."""
        if not self._identity_endpoints():
            return False
        if not self._unit_laws():
            return False
        return self._associative()


def _require_map(values: object, role: str) -> Mapping[object, object]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Mapping) or len(values) == 0:
        raise _fail("factorization map must be a nonempty table", role=role, received=type(values).__name__)
    return values


def _assign(decoder: Dict[int, int], source: object, report: object, query_map: Mapping[object, object]) -> None:
    key = _exact_int(source, "source")
    image = _exact_int(report, "report")
    if key not in query_map:
        raise _fail("query misses a report source", source=key)
    query = _exact_int(query_map[key], "query")
    if image in decoder and decoder[image] != query:
        raise _fail(
            "query does not factor through the report",
            report=image,
            left=decoder[image],
            right=query,
        )
    decoder[image] = query


def factor_report_query(report_map: object, query_map: object) -> Dict[int, int]:
    """Return the decoder d such that query = d o report, or a typed refusal."""
    report = _require_map(report_map, "report")
    query = _require_map(query_map, "query")
    decoder: Dict[int, int] = {}
    for source, image in report.items():
        _assign(decoder, source, image, query)
    return decoder


def verify_report_query_factorization(
    report_map: Mapping[int, int],
    query_map: Mapping[int, int],
) -> Tuple[bool, Dict[int, int]]:
    """Boolean form of factor_report_query. A refusal returns (False, {})."""
    try:
        return (True, factor_report_query(report_map, query_map))
    except CategoryLawError:
        return (False, {})


__all__ = [
    "CategoryLawError",
    "FiniteCategory",
    "factor_report_query",
    "verify_report_query_factorization",
]
