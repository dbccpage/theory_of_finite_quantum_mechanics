"""Minimal port of ``omega_homological::finite_directed_graph::FiniteDirectedGraph``.

The full Rust type (crates/omega_homological/src/finite_directed_graph.rs)
carries named nodes, a witness hash, and provenance. The solvers only use
``num_nodes()``, ``edges()`` (a list of ``(usize, usize)`` directed pairs), and
the checked ``from_pairs`` constructor that rejects self-loops and duplicate
edges (cycles are permitted). We port exactly that surface plus the
``TheoremProvenance`` marker used in the Rust tests.
"""

from __future__ import annotations
from dataclasses import field
from dataclasses import dataclass
from typing import List, Tuple


class DirectedGraphError(Exception):
    """Mirror of ``omega_homological::DirectedGraphError`` (subset)."""


@dataclass
class TheoremProvenance:
    verification_source: str = ""


@dataclass
class FiniteDirectedGraph:
    """Finite directed graph carrier (edges are directed ``(source, target)``)."""

    _num_nodes: int
    _edges: List[Tuple[int, int]] = field(default_factory=list)
    provenance: TheoremProvenance = field(default_factory=TheoremProvenance)

    @classmethod
    def from_pairs(
        cls,
        pairs: List[Tuple[int, int]],
        provenance: TheoremProvenance | None = None,
    ) -> "FiniteDirectedGraph":
        if provenance is None:
            provenance = TheoremProvenance()
        for src, dst in pairs:
            if src < 0 or dst < 0:
                raise DirectedGraphError(f"negative edge endpoint: ({src}, {dst})")
        num_nodes = (max(max(s, d) for (s, d) in pairs) + 1) if pairs else 0
        seen = set()
        edges: List[Tuple[int, int]] = []
        for src, dst in pairs:
            if src >= num_nodes or dst >= num_nodes:
                raise DirectedGraphError(f"edge endpoint out of range: ({src}, {dst})")
            if src == dst:
                raise DirectedGraphError(f"self-loop at ({src}, {dst})")
            if (src, dst) in seen:
                raise DirectedGraphError(f"duplicate edge ({src}, {dst})")
            seen.add((src, dst))
            edges.append((src, dst))
        return cls(_num_nodes=num_nodes, _edges=edges, provenance=provenance)

    def num_nodes(self) -> int:
        return self._num_nodes

    def node_count(self) -> int:
        return self._num_nodes

    def num_edges(self) -> int:
        return len(self._edges)

    def edges(self) -> List[Tuple[int, int]]:
        return list(self._edges)



