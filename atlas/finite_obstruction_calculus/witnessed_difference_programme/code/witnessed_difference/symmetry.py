"""Exhaustive finite symmetry witnesses for an admitted labelled carrier."""

from __future__ import annotations

from itertools import combinations, permutations
from typing import Iterable, Iterator

Pair = tuple[int, int]
Permutation = tuple[int, ...]
Relation = frozenset[Pair]


def carrier(n: int) -> tuple[int, ...]:
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n must be a non-negative integer")
    return tuple(range(n))


def all_permutations(n: int) -> tuple[Permutation, ...]:
    return tuple(permutations(carrier(n)))


def validate_permutation(perm: Permutation, n: int) -> None:
    if any(type(v) is not int for v in perm) or tuple(sorted(perm)) != carrier(n):
        raise ValueError("permutation must contain every carrier label exactly once")


def validate_relation(relation: Iterable[Pair], n: int) -> Relation:
    labels = set(carrier(n))
    frozen = frozenset(relation)
    if any(type(u) is not int or type(v) is not int or u not in labels or v not in labels for u, v in frozen):
        raise ValueError("relation contains a pair outside the carrier")
    return frozen


def apply_permutation(relation: Iterable[Pair], perm: Permutation, n: int) -> Relation:
    validate_permutation(perm, n)
    frozen = validate_relation(relation, n)
    return frozenset((perm[u], perm[v]) for u, v in frozen)


def relation_orbits(n: int) -> tuple[Relation, ...]:
    labels = carrier(n)
    unseen = {(u, v) for u in labels for v in labels}
    perms = all_permutations(n)
    orbits: list[Relation] = []
    while unseen:
        seed = min(unseen)
        orbit = frozenset((perm[seed[0]], perm[seed[1]]) for perm in perms)
        orbits.append(orbit)
        unseen.difference_update(orbit)
    return tuple(sorted(orbits, key=lambda orbit: (len(orbit), sorted(orbit))))


def invariant_binary_relations(n: int) -> tuple[Relation, ...]:
    orbits = relation_orbits(n)
    invariant: list[Relation] = []
    for mask in range(1 << len(orbits)):
        relation: set[Pair] = set()
        for bit, orbit in enumerate(orbits):
            if mask & (1 << bit):
                relation.update(orbit)
        invariant.append(frozenset(relation))
    return tuple(sorted(invariant, key=lambda rel: (len(rel), sorted(rel))))


def is_invariant(relation: Iterable[Pair], n: int) -> bool:
    frozen = validate_relation(relation, n)
    return all(apply_permutation(frozen, perm, n) == frozen for perm in all_permutations(n))


def all_relations(n: int) -> Iterator[Relation]:
    if n > 4:
        raise ValueError("exhaustive relation enumeration is limited to n <= 4")
    pairs = tuple((u, v) for u in carrier(n) for v in carrier(n))
    for mask in range(1 << len(pairs)):
        yield frozenset(pair for bit, pair in enumerate(pairs) if mask & (1 << bit))


def strict_order_from_sequence(sequence: Permutation) -> Relation:
    n = len(sequence)
    validate_permutation(sequence, n)
    return frozenset((sequence[i], sequence[j]) for i in range(n) for j in range(i + 1, n))


def is_strict_total_order(relation: Iterable[Pair], n: int) -> bool:
    frozen = validate_relation(relation, n)
    labels = carrier(n)
    if any((x, x) in frozen for x in labels):
        return False
    for x, y in combinations(labels, 2):
        if ((x, y) in frozen) == ((y, x) in frozen):
            return False
    return all((x, z) in frozen for x, y in frozen for y2, z in frozen if y == y2)


def invariant_strict_total_orders(n: int) -> tuple[Relation, ...]:
    orders = (strict_order_from_sequence(perm) for perm in all_permutations(n))
    return tuple(order for order in orders if is_invariant(order, n))


def fixed_points(n: int) -> tuple[int, ...]:
    perms = all_permutations(n)
    return tuple(x for x in carrier(n) if all(perm[x] == x for perm in perms))


def fixed_oriented_edges(n: int) -> tuple[Pair, ...]:
    perms = all_permutations(n)
    return tuple(
        (u, v)
        for u in carrier(n)
        for v in carrier(n)
        if u != v and all((perm[u], perm[v]) == (u, v) for perm in perms)
    )


def exhaustive_relation_audit(n: int = 3) -> dict[str, object]:
    relations = tuple(all_relations(n))
    invariant = tuple(relation for relation in relations if is_invariant(relation, n))
    return {
        "authority_effect": "None",
        "invariant_relation_count": len(invariant),
        "invariant_relations": invariant,
        "invariant_strict_order_count": len(invariant_strict_total_orders(n)),
        "n": n,
        "permutation_count": len(all_permutations(n)),
        "relation_count": len(relations),
    }
# Executable finite evidence; AuthorityEffect: None.
