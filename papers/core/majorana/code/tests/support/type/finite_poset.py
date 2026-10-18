"""
Graph utilities for L1 topology on finite posets.

Provides graph construction and manipulation used in Papers 000-005.
"""

from typing import List, Tuple, Dict, Set


class FinitePoset:
    """
    A finite directed-graph carrier (NOT a validated poset).

    This class is a directed-graph container: `nodes` are vertices and `edges`
    are directed arcs. Its "poset" interpretation is BY REACHABILITY (a <= b
    iff b is reachable from a along edges). It does NOT by itself enforce the
    poset axioms: it does not verify antisymmetry or transitivity, and it does
    not require the edge relation to be a partial order. The constructor only
    validates that every edge endpoint is a declared node.

    Note: `is_chain` only inspects out-degree (it does not certify a total
    order), and `is_cycle` tests whether the whole graph is a single directed
    cycle. Use `has_cycle()` to detect any directed cycle.
    """

    def __init__(self, nodes: List[str], edges: List[Tuple[str, str]]):
        """
        Initialize a finite directed-graph carrier.

        Args:
            nodes: List of node labels
            edges: List of (source, target) tuples (directed arcs)

        Raises:
            ValueError: if any edge endpoint is not a declared node.
        """
        self.nodes: List[str] = nodes
        self.edges: List[Tuple[str, str]] = edges
        self._validate_edges()
        self._adjacency: Dict[str, Set[str]] = self._build_adjacency()

    def _validate_edges(self) -> None:
        """Validate that every edge endpoint is a declared node."""
        node_set = set(self.nodes)
        for a, b in self.edges:
            if a not in node_set:
                raise ValueError(f"edge source {a!r} is not a declared node")
            if b not in node_set:
                raise ValueError(f"edge target {b!r} is not a declared node")

    def _build_adjacency(self) -> Dict[str, Set[str]]:
        """Build adjacency list representation."""
        adj: Dict[str, Set[str]] = {n: set() for n in self.nodes}
        for a, b in self.edges:
            adj[a].add(b)
        return adj

    def successors(self, node: str) -> Set[str]:
        """Return all nodes covered by the given node."""
        return self._adjacency.get(node, set())

    def degree(self, node: str) -> int:
        """Return the out-degree of a node."""
        return len(self._adjacency.get(node, set()))

    def is_chain(self) -> bool:
        """Check if the poset is a linear chain."""
        if len(self.nodes) <= 1:
            return True
        return all(self.degree(n) <= 1 for n in self.nodes)

    def is_cycle(self) -> bool:
        """Check if the graph forms a single directed cycle (Paper 006)."""
        if len(self.nodes) != len(self.edges):
            return False
        return all(self.degree(n) == 1 for n in self.nodes)

    def has_cycle(self) -> bool:
        """Return True iff the directed graph contains any directed cycle.

        Distinct from `is_cycle` (which tests whether the whole graph is one
        single directed cycle). Uses DFS with a recursion stack.
        """
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def visit(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for nb in self._adjacency.get(node, set()):
                if nb not in visited:
                    if visit(nb):
                        return True
                elif nb in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        return any(visit(n) for n in self.nodes if n not in visited)
