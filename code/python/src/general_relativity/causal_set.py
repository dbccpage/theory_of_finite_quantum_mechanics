"""Exact finite causal sets, interval abundances and the dimension-two interval action.

These finite observables do not identify a continuum spacetime.
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Dict, List, Set, Tuple


AUTHORITY_FENCE = (
    "AuthorityEffect None; not PROVED; not GlobalGreen; finite causal set; no continuum admission."
)


class PosetError(Exception):
    pass


@dataclass
class FinitePoset:
    """Finite partially ordered set with transitive closure."""
    size: int
    strict_relations: Set[Tuple[int, int]] = field(default_factory=set)

    @classmethod
    def from_relations(cls, size: int, relations: List[Tuple[int, int]]) -> FinitePoset:
        # Transitive closure
        adj: Dict[int, Set[int]] = {i: set() for i in range(size)}
        for u, v in relations:
            if u < 0 or u >= size or v < 0 or v >= size:
                raise PosetError(f"Element index out of bounds: ({u}, {v})")
            if u == v:
                continue
            adj[u].add(v)

        # Floyd-Warshall / reachability for transitive closure
        for k in range(size):
            for i in range(size):
                if k in adj[i]:
                    adj[i].update(adj[k])

        # Check acyclicity
        for i in range(size):
            if i in adj[i]:
                raise PosetError(f"Cycle detected involving element {i}")

        strict = {(u, v) for u in range(size) for v in adj[u]}
        return cls(size=size, strict_relations=strict)

    def less(self, u: int, v: int) -> bool:
        if u < 0 or u >= self.size or v < 0 or v >= self.size:
            raise PosetError(f"Index out of bounds: ({u}, {v})")
        return (u, v) in self.strict_relations

    def interval(self, u: int, v: int) -> List[int]:
        """Closed Alexandrov interval [u, v] = {w | u <= w <= v}."""
        if u == v:
            return [u]
        if not self.less(u, v):
            return []
        res = [u]
        for w in range(self.size):
            if w != u and w != v and self.less(u, w) and self.less(w, v):
                res.append(w)
        res.append(v)
        return sorted(res)

    def predecessors(self, v: int) -> List[int]:
        return sorted([u for u in range(self.size) if self.less(u, v)])

    def successors(self, v: int) -> List[int]:
        return sorted([w for w in range(self.size) if self.less(v, w)])

    def relation_count(self) -> int:
        return len(self.strict_relations)


@dataclass
class CausalSet:
    """Discrete causal set carrying exact finite observables."""
    degree: int
    label: str
    order: FinitePoset

    @classmethod
    def discrete(cls, degree: int, label: str = "") -> CausalSet:
        return cls(degree=degree, label=label, order=FinitePoset(degree, set()))

    @classmethod
    def from_relations(cls, degree: int, relations: List[Tuple[int, int]], label: str = "") -> CausalSet:
        order = FinitePoset.from_relations(degree, relations)
        return cls(degree=degree, label=label, order=order)

    @staticmethod
    def authority_fence() -> str:
        return AUTHORITY_FENCE

    def spacelike(self, u: int, v: int) -> bool:
        """True if u and v are distinct and un-ordered (spacelike separated)."""
        return u != v and not self.order.less(u, v) and not self.order.less(v, u)

    def alexandrov_interval(self, u: int, v: int) -> List[int]:
        return self.order.interval(u, v)

    def past(self, v: int) -> List[int]:
        return self.order.predecessors(v)

    def future(self, v: int) -> List[int]:
        return self.order.successors(v)

    def ordering_fraction(self) -> Fraction:
        n = self.degree
        if n < 2:
            return Fraction(0)
        return Fraction(2 * self.order.relation_count(), n * (n - 1))

    def interval_abundances(self) -> List[int]:
        """Counts comparable pairs (u, v) by the cardinality of open interval (u, v)."""
        max_open = max(0, self.degree - 2)
        counts = [0] * (max_open + 1)
        for u, v in self.order.strict_relations:
            # open interval excludes endpoints u and v
            open_count = len(self.order.interval(u, v)) - 2
            if open_count < len(counts):
                counts[open_count] += 1
        return counts

    def two_dimensional_interval_action(self) -> int:
        """Benincasa-Dowker interval action in 2D: N - 2*N_0 + 4*N_1 - 2*N_2."""
        counts = self.interval_abundances()
        n0 = counts[0] if len(counts) > 0 else 0
        n1 = counts[1] if len(counts) > 1 else 0
        n2 = counts[2] if len(counts) > 2 else 0
        return self.degree - 2 * n0 + 4 * n1 - 2 * n2
