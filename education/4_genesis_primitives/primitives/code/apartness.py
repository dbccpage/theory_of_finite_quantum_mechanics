"""Genesis Primitives Category 8: Constructive Positive Apartness & Indistinguishability.

Selected educational models related to 19L57G1 (lean4/Derivation/Apartness.lean and code/derivation/apartness.py).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

Positive apartness (irreflexive, symmetric, cotransitive), indistinguishability
as its negation, the equivalence theorem verified exhaustively, and the minimal
insufficiency countermodels.
"""

from __future__ import annotations

from itertools import product
from typing import Any

Rel = frozenset[tuple[int, int]]


def _valid_relation(n: int, relation: Rel) -> bool:
    return (
        type(n) is int
        and n >= 0
        and type(relation) is frozenset
        and all(
            type(pair) is tuple
            and len(pair) == 2
            and all(type(point) is int and 0 <= point < n for point in pair)
            for pair in relation
        )
    )


def all_relations(n: int) -> list[Rel]:
    """All binary relations on carrier range(n)."""
    if type(n) is not int or n < 0:
        raise ValueError("REFUSED_SHAPE: natural-number carrier size required")
    pairs = [(i, j) for i in range(n) for j in range(n)]
    out: list[Rel] = []
    for bits in product((False, True), repeat=len(pairs)):
        out.append(frozenset(p for p, b in zip(pairs, bits) if b))
    return out


def is_irrefl(n: int, r: Rel) -> bool:
    """Irreflexivity: ∀ x, ¬ r(x, x)."""
    return _valid_relation(n, r) and all((x, x) not in r for x in range(n))


def is_symm(n: int, r: Rel) -> bool:
    """Symmetry: ∀ x y, r(x, y) → r(y, x)."""
    return _valid_relation(n, r) and all((y, x) in r for (x, y) in r)


def is_cotrans(n: int, r: Rel) -> bool:
    """Cotransitivity: ∀ x y, r(x, y) → ∀ z, r(x, z) ∨ r(z, y)."""
    return _valid_relation(n, r) and all(
        (x, z) in r or (z, y) in r for (x, y) in r for z in range(n)
    )


def is_apart(n: int, r: Rel) -> bool:
    """Positive constructive apartness predicate: irreflexive ∧ symmetric ∧ cotransitive."""
    return is_irrefl(n, r) and is_symm(n, r) and is_cotrans(n, r)


def indist(r: Rel, x: int, y: int) -> bool:
    """Indistinguishability: negation of apartness ¬ r(x, y)."""
    return (x, y) not in r


def indist_is_equivalence(n: int, r: Rel) -> bool:
    """Checks whether indistinguishability forms an equivalence relation."""
    refl = all(indist(r, x, x) for x in range(n))
    symm = all((not indist(r, x, y)) or indist(r, y, x) for x in range(n) for y in range(n))
    trans = all(
        (not (indist(r, x, y) and indist(r, y, z))) or indist(r, x, z)
        for x in range(n)
        for y in range(n)
        for z in range(n)
    )
    return refl and symm and trans


def equivalence_theorem_exhaustive(max_n: int) -> bool:
    """Mirror of indist_equivalence: positive apartness forces indistinguishability to be an equivalence."""
    return all(
        indist_is_equivalence(n, r)
        for n in range(1, max_n + 1)
        for r in all_relations(n)
        if is_apart(n, r)
    )


def insufficiency_countermodels() -> dict[str, Any]:
    """The three minimal insufficiency countermodels."""
    bare = frozenset({(0, 0)})
    d2 = frozenset({(0, 1)})
    tri = frozenset({(0, 1), (1, 0)})

    min2 = all(indist_is_equivalence(1, r) for r in all_relations(1) if is_irrefl(1, r))
    min3 = all(
        indist_is_equivalence(2, r) for r in all_relations(2) if is_irrefl(2, r) and is_symm(2, r)
    )

    return {
        "bare_breaks_refl": not indist(bare, 0, 0),
        "irrefl_alone_breaks_symm": (
            is_irrefl(2, d2) and indist(d2, 1, 0) and not indist(d2, 0, 1)
        ),
        "symm_without_cotrans_breaks_trans": (
            is_irrefl(3, tri)
            and is_symm(3, tri)
            and not is_cotrans(3, tri)
            and indist(tri, 0, 2)
            and indist(tri, 2, 1)
            and not indist(tri, 0, 1)
        ),
        "two_point_countermodel_minimal": min2,
        "three_point_countermodel_minimal": min3,
    }
