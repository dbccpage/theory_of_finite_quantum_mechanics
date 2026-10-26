"""Genesis Primitives Category 11: Renaming Structures, Permutations & Gauge Transport.

Selected educational models related to 19L57G1 (lean4/Derivation/RenamingStructure.lean, FormRenaming.lean, IsoCanon.lean).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

Full permutation actions, canonical form invariants, automorphism groups, and
relational state quotients modulo isomorphism.
"""

from __future__ import annotations

from itertools import permutations

Perm = tuple[int, ...]
Rel = frozenset[tuple[int, int]]


def all_permutations(n: int) -> list[Perm]:
    """All permutations of carrier range(n)."""
    if type(n) is not int or n < 0:
        raise ValueError("REFUSED_SHAPE: natural-number carrier size required")
    return list(permutations(range(n)))


def apply_perm_pair(p: Perm, pair: tuple[int, int]) -> tuple[int, int]:
    """Action of permutation p on a pair (i, j)."""
    if (
        type(p) is not tuple
        or any(type(index) is not int for index in p)
        or sorted(p) != list(range(len(p)))
        or type(pair) is not tuple
        or len(pair) != 2
        or any(type(index) is not int or not 0 <= index < len(p) for index in pair)
    ):
        raise ValueError("REFUSED_SHAPE: permutation action outside its declared carrier")
    return (p[pair[0]], p[pair[1]])


def apply_perm_rel(p: Perm, r: Rel) -> Rel:
    """Action of permutation p on a binary relation r."""
    return frozenset(apply_perm_pair(p, pair) for pair in r)


def are_isomorphic_relations(n: int, r1: Rel, r2: Rel) -> bool:
    """Decides relational isomorphism over the symmetric group S_n."""
    if len(r1) != len(r2):
        return False
    return any(apply_perm_rel(p, r1) == r2 for p in all_permutations(n))


def automorphism_group(n: int, r: Rel) -> list[Perm]:
    """The automorphism group Aut(r) of symmetries stabilizing relation r."""
    return [p for p in all_permutations(n) if apply_perm_rel(p, r) == r]


def iso_canon_key(n: int, r: Rel) -> tuple[tuple[int, int], ...]:
    """Canonical representative of relation r modulo permutation action (gauge invariant)."""
    all_images = [sorted(apply_perm_rel(p, r)) for p in all_permutations(n)]
    return tuple(min(all_images))
