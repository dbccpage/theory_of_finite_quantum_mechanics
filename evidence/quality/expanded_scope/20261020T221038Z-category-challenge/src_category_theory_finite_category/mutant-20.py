"""Finite categories and report-query factorization over an explicit table.

Origin: code/rust/src/category_theory/category/category.rs struct FiniteCategoryShell
and code/rust/src/category_theory/finite_report_query.rs struct FactorizationCertificate.
Claim: urn:omega:fqm:category:finite-arrow-factorization:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/category_theory/test_finite_category.py.
Gate 5: use source-bound measurements in the companion history.
Scope Fence: Identity, unit, and associativity are checked on the morphisms
that were supplied. Factorization is the set-theoretic decoder of one total
table. This file does not claim a free category, a topos, or that every
query factors.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, Mapping, Tuple

# Declared engineering policies, not mathematical cardinality theorems.
MAX_OBJECTS = 64
MAX_MORPHISMS = 64
MAX_COMPOSITION_ENTRIES = 4096
MAX_FACTOR_SOURCES = 4096
MAX_LABEL_CHARACTERS = 256
MAX_INTEGER_BITS = 1024


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
    if issubclass(type(value), float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer label was required", role=role)
    if type(value) is not int:
        raise _fail("label is not an exact integer", role=role, received=type(value).__name__)
    if value.bit_length() > MAX_INTEGER_BITS:
        raise _fail("integer label bit budget exceeded", role=role, bits=value.bit_length(), limit=MAX_INTEGER_BITS)
    return value


def _label(value: object) -> str:
    if type(value) is not str:
        raise _fail("category label must be a built-in string", received=type(value).__name__)
    if len(value) > MAX_LABEL_CHARACTERS:
        raise _fail("category label length budget exceeded", limit=MAX_LABEL_CHARACTERS)
    return value


def _label_pair(value: object) -> tuple[str, str]:
    if type(value) is not tuple or len(value) != 2:
        raise _fail("category pair must contain two labels")
    return (_label(value[0]), _label(value[1]))


def _copy_table(value: object, limit: int, role: str) -> dict:
    if type(value) is not dict:
        raise _fail("category table must be a built-in dict", role=role, received=type(value).__name__)
    if len(value) > limit:
        raise _fail("category table entry budget exceeded", role=role, limit=limit)
    return value.copy()


def _objects(value: object) -> frozenset[str]:
    if type(value) is not frozenset:
        raise _fail("category objects must be a built-in frozenset", received=type(value).__name__)
    if len(value) > MAX_OBJECTS:
        raise _fail("category object budget exceeded", limit=MAX_OBJECTS)
    for item in value:
        _label(item)
    return value


def _morphisms(value: object) -> Mapping[str, tuple[str, str]]:
    entries = _copy_table(value, MAX_MORPHISMS, "morphisms")
    return MappingProxyType({_label(name): _label_pair(pair) for name, pair in entries.items()})


def _identities(value: object) -> Mapping[str, str]:
    entries = _copy_table(value, MAX_OBJECTS, "identities")
    return MappingProxyType({_label(name): _label(identity) for name, identity in entries.items()})


def _composition(value: object) -> Mapping[tuple[str, str], str]:
    entries = _copy_table(value, MAX_COMPOSITION_ENTRIES, "composition")
    return MappingProxyType({_label_pair(pair): _label(result) for pair, result in entries.items()})


@dataclass(frozen=True, slots=True, init=False, eq=False)
class FiniteCategory:
    """Immutable bounded category presentation; verify_axioms checks all laws.

    Shape/type admission is separate from the boolean law check. The empty
    presentation is admitted and is the empty category. Ordinary state mutation
    and repeated initialization are refused; Python reflection is not isolated.
    """

    objects: frozenset[str]
    morphisms: Mapping[str, Tuple[str, str]]
    identities: Mapping[str, str]
    composition: Mapping[Tuple[str, str], str]
    __hash__ = None

    def __init__(self, objects: object, morphisms: object, identities: object, composition: object) -> None:
        if hasattr(self, "objects"):
            raise _fail("category presentation already initialized")
        admitted = (_objects(objects), _morphisms(morphisms), _identities(identities), _composition(composition))
        for name, value in zip(("objects", "morphisms", "identities", "composition"), admitted, strict=True):
            object.__setattr__(self, name, value)

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("FiniteCategory does not admit subclasses")

    def __eq__(self, other: object) -> bool:
        if type(other) is not FiniteCategory:
            return False
        return (self.objects, self.morphisms, self.identities, self.composition) == (other.objects, other.morphisms, other.identities, other.composition)

    def _morphism_endpoints(self) -> bool:
        return all(source in self.objects and target in self.objects for source, target in self.morphisms.values())

    def _identity_endpoints(self) -> bool:
        if self.identities.keys() != self.objects:
            return False
        for obj in self.objects:
            if obj not in self.identities:
                return False
            if self.morphisms.get(self.identities[obj]) != (obj, obj):
                return False
        return True

    def _composition_typing(self) -> bool:
        pairs = 0
        for outer, (source, target) in self.morphisms.items():
            for inner, (domain, codomain) in self.morphisms.items():
                if source == codomain:
                    pairs += 1
                    result = self.composition.get((outer, inner))
                    if self.morphisms.get(result) != (domain, target):
                        return False
                elif (outer, inner) in self.composition:
                    return False
        return len(self.composition) == pairs

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
        """Check endpoints, exact composition domain/typing, identities and laws."""
        if not self._morphism_endpoints() or not self._composition_typing():
            return False
        if not self._identity_endpoints():
            return False
        if not self._unit_laws():
            return False
        return self._associative()


def _require_map(values: object, role: str) -> Mapping[object, object]:
    if not issubclass(type(values), dict) or len(values) == 0:
        raise _fail("factorization map must be a nonempty table", role=role, received=type(values).__name__)
    if len(values) > MAX_FACTOR_SOURCES:
        raise _fail("factorization source budget exceeded", role=role, limit=MAX_FACTOR_SOURCES)
    entries = values.copy()
    for key, value in entries.items():
        _exact_int(key, role + " source")
        _exact_int(value, role + " value")
    return entries


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
    if report.keys() != query.keys():
        raise _fail("report and query domains differ", report_sources=len(report), query_sources=len(query))
    decoder: Dict[int, int] = {}
    for source, image in report.items():
        _assign(decoder, source, image, query)
    return decoder


def verify_report_query_factorization(
    report_map: object,
    query_map: object,
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
