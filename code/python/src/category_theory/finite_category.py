"""Finite categories, functors, natural transformations, and report-query factorization.

AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, FrozenSet, Mapping, Tuple


@dataclass(frozen=True)
class FiniteCategory:
    """Finite category with explicit objects, morphisms, identities, and composition table."""

    objects: FrozenSet[str]
    morphisms: Dict[str, Tuple[str, str]]  # morph_id -> (dom, cod)
    identities: Dict[str, str]  # obj -> morph_id
    composition: Dict[Tuple[str, str], str]  # (g, f) -> g o f where dom(g) == cod(f)

    def verify_axioms(self) -> bool:
        """Verify identity and associativity laws on all composable triples."""
        for obj in self.objects:
            if obj not in self.identities:
                return False
            id_m = self.identities[obj]
            if self.morphisms.get(id_m) != (obj, obj):
                return False

        for f, (a, b) in self.morphisms.items():
            id_a = self.identities[a]
            id_b = self.identities[b]
            if self.composition.get((f, id_a)) != f:
                return False
            if self.composition.get((id_b, f)) != f:
                return False

        for f, (_, b) in self.morphisms.items():
            for g, (b2, c) in self.morphisms.items():
                if b != b2:
                    continue
                gf = self.composition.get((g, f))
                if gf is None:
                    return False
                for h, (c2, _) in self.morphisms.items():
                    if c != c2:
                        continue
                    hg = self.composition.get((h, g))
                    if hg is None:
                        return False
                    if self.composition.get((h, gf)) != self.composition.get((hg, f)):
                        return False
        return True


def verify_report_query_factorization(
    report_map: Mapping[int, int],
    query_map: Mapping[int, int],
) -> Tuple[bool, Dict[int, int]]:
    """Check whether query_map factors through report_map (q = d o r) on a finite state set."""
    decoder: Dict[int, int] = {}
    for x, r_val in report_map.items():
        q_val = query_map[x]
        if r_val in decoder and decoder[r_val] != q_val:
            return (False, {})
        decoder[r_val] = q_val
    return (True, decoder)
