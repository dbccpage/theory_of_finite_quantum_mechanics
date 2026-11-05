"""Pointed relations (X, R, a, b): relatedness, apartness, and irreflexivity.

R(a, b) does not imply a != b, a != b does not imply R(a, b), and R(a, b)
together with irreflexivity of R implies a != b.  The census enumerates every
pointed relation on the carriers {0}, {0, 1}, {0, 1, 2} and compares the counts
with their closed forms; it certifies nothing about larger carriers.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Hashable, Mapping

from .outcomes import Accepted, Outcome, RefusalCode, Refused

Pair = tuple[Hashable, Hashable]
CENSUS_BUDGET = 3


@dataclass(frozen=True)
class PointedRelation:
    carrier: tuple[Hashable, ...]
    relation: frozenset[Pair]
    first: Hashable
    second: Hashable


@dataclass(frozen=True)
class PointedPredicates:
    related: bool
    irreflexive: bool
    distinct: bool


def make_pointed_relation(
    carrier: tuple[Hashable, ...],
    relation: object,
    first: Hashable,
    second: Hashable,
) -> Outcome[PointedRelation]:
    """Admit (X, R, a, b) only when R is a set of ordered pairs of X and a, b lie in X."""

    if type(carrier) is not tuple or not carrier or len(set(carrier)) != len(carrier):
        return Refused(RefusalCode.INVALID_INPUT, "the carrier must be a nonempty tuple of distinct points")
    if isinstance(relation, (str, bytes, Mapping)) or not isinstance(relation, (set, frozenset, tuple, list)):
        return Refused(RefusalCode.INVALID_INPUT, "a relation is a finite collection of ordered pairs")
    pairs = set()
    for pair in relation:
        if type(pair) is not tuple or len(pair) != 2:
            return Refused(RefusalCode.INVALID_INPUT, f"{pair!r} is not an ordered pair; R is not a relation")
        if pair[0] not in carrier or pair[1] not in carrier:
            return Refused(RefusalCode.OUTSIDE_CARRIER, f"pair {pair!r} leaves the carrier")
        pairs.add(pair)
    if first not in carrier or second not in carrier:
        return Refused(RefusalCode.OUTSIDE_CARRIER, "both poles must lie in the carrier")
    return Accepted(PointedRelation(carrier, frozenset(pairs), first, second))


def _predicates(relation: frozenset[Pair], first: Hashable, second: Hashable) -> PointedPredicates:
    return PointedPredicates(
        (first, second) in relation,
        all(left != right for left, right in relation),
        first != second,
    )


def pointed_predicates(pointed: PointedRelation) -> Outcome[PointedPredicates]:
    """R(a, b), irreflexivity of R, and a != b, after re-admitting the pointed relation."""

    if not isinstance(pointed, PointedRelation):
        return Refused(RefusalCode.INVALID_INPUT, "a pointed relation is required")
    admitted = make_pointed_relation(pointed.carrier, pointed.relation, pointed.first, pointed.second)
    if isinstance(admitted, Refused):
        return admitted
    return Accepted(_predicates(admitted.value.relation, pointed.first, pointed.second))


@dataclass(frozen=True)
class PointedCensus:
    """Counts over all pointed relations on carriers of size 1 through ``max_carrier``."""

    max_carrier: int
    pointed_relations: int
    related: int
    related_irreflexive: int
    distinct: int
    related_and_distinct: int
    related_not_distinct: int
    distinct_not_related: int
    irreflexive_related_not_distinct: int


def _budget(max_carrier: object) -> Refused | None:
    if type(max_carrier) is not int or max_carrier < 1:
        return Refused(RefusalCode.INVALID_INPUT, "the carrier bound must be a positive integer")
    if max_carrier > CENSUS_BUDGET:
        return Refused(RefusalCode.BUDGET_EXHAUSTED, f"the census is budgeted to carriers of size <= {CENSUS_BUDGET}")
    return None


def enumerate_pointed_relations(max_carrier: int = CENSUS_BUDGET) -> Outcome[PointedCensus]:
    """Exhaustively classify every (R, a, b) on {0, ..., n - 1} for 1 <= n <= max_carrier."""

    refusal = _budget(max_carrier)
    if refusal is not None:
        return refusal
    counts = [0] * 8
    for size in range(1, max_carrier + 1):
        carrier = tuple(range(size))
        pairs = tuple(product(carrier, repeat=2))
        for mask in range(1 << len(pairs)):
            relation = frozenset(pair for index, pair in enumerate(pairs) if mask >> index & 1)
            for first, second in pairs:
                seen = _predicates(relation, first, second)
                flags = (
                    True,
                    seen.related,
                    seen.related and seen.irreflexive,
                    seen.distinct,
                    seen.related and seen.distinct,
                    seen.related and not seen.distinct,
                    seen.distinct and not seen.related,
                    seen.related and seen.irreflexive and not seen.distinct,
                )
                counts = [count + flag for count, flag in zip(counts, flags)]
    return Accepted(PointedCensus(max_carrier, *counts))


def closed_form_census(max_carrier: int = CENSUS_BUDGET) -> Outcome[PointedCensus]:
    """The same counts from their closed forms, summed over n = 1, ..., max_carrier.

    related: n^2 2^(n^2 - 1); related and irreflexive: n(n - 1) 2^(n(n - 1) - 1);
    distinct: n(n - 1) 2^(n^2); related and distinct: n(n - 1) 2^(n^2 - 1).
    """

    refusal = _budget(max_carrier)
    if refusal is not None:
        return refusal
    sizes = range(1, max_carrier + 1)
    total = sum(n * n * 2 ** (n * n) for n in sizes)
    related = sum(n * n * 2 ** (n * n - 1) for n in sizes)
    irreflexive = sum(n * (n - 1) * 2 ** (n * (n - 1) - 1) for n in sizes if n > 1)
    distinct = sum(n * (n - 1) * 2 ** (n * n) for n in sizes)
    both = sum(n * (n - 1) * 2 ** (n * n - 1) for n in sizes)
    return Accepted(
        PointedCensus(max_carrier, total, related, irreflexive, distinct, both, related - both, distinct - both, 0)
    )


def apartness_countermodels() -> tuple[PointedRelation, PointedRelation]:
    """R(a, b) with a = b on one point, and a != b with the empty relation on two points."""

    return (
        PointedRelation(("a",), frozenset({("a", "a")}), "a", "a"),
        PointedRelation(("a", "b"), frozenset(), "a", "b"),
    )


# Executable finite evidence; AuthorityEffect: None.
