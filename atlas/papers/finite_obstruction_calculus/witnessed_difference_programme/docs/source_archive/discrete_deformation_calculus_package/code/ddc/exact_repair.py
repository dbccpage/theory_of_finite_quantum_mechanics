"""DDC letter E: exact repair of a defect that lies in ``im d0``.

E is the *exact* part of the Hodge split, not the co-exact part. Given a defect
``x`` on the edges of a finite graph, E finds a potential ``phi`` with
``d0 phi = x`` (one gauge vertex fixed per component) and repairs by
``x -> x - d0 phi = 0``. A defect with non-zero circulation around some cycle
is not in ``im d0``; E then refuses with ``REFUSED_NON_ZERO_CURL`` (the name is
kept for wire compatibility; its meaning is exactly ``x not in im d0``).

Leaf module: standard library only, loadable by path. AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Dict, List, Optional, Tuple

Edge = Tuple[str, str]

NOT_EXACT = "REFUSED_NON_ZERO_CURL"


def _exact(value: object) -> Fraction:
    if isinstance(value, (bool, float)) or not isinstance(value, (int, Fraction)):
        raise ValueError(f"NOT_EXACT: {value!r}")
    return Fraction(value)


@dataclass(frozen=True)
class ExactRepairReceipt:
    operation: str
    paper_id: str
    success: bool
    input_norm: Fraction
    residual_norm: Fraction
    gauge_vertex: str
    potential: Dict[str, Fraction]
    error: Optional[str] = None
    repaired: Dict[Edge, Fraction] = field(default_factory=dict)
    authority_effect: str = "None"


class ExactRepairSolver:
    """Exact rational solver for DDC letter E on the edges of a finite graph."""

    def __init__(self, vertices: List[str], edges: List[Edge]):
        if len(set(vertices)) != len(vertices) or len(set(edges)) != len(edges):
            raise ValueError("DUPLICATE_CARRIER")
        self.vertices = sorted(set(vertices))
        if not self.vertices:
            raise ValueError("vertices must be non-empty")
        known = set(self.vertices)
        for u, v in edges:
            if u not in known or v not in known:
                raise ValueError(f"UNKNOWN_VERTEX: {(u, v)!r}")
            if u == v:
                raise ValueError(f"SELF_LOOP: {(u, v)!r}")
        self.edges = list(edges)
        self._adj: Dict[str, List[Tuple[str, int, int]]] = {v: [] for v in self.vertices}
        for idx, (u, v) in enumerate(self.edges):
            self._adj[u].append((v, 1, idx))
            self._adj[v].append((u, -1, idx))

    def coboundary_0(self, potential: Dict[str, Fraction]) -> Dict[Edge, Fraction]:
        """``d0 phi`` on each directed edge: ``phi(v) - phi(u)``."""
        if set(potential) != set(self.vertices):
            raise ValueError("POTENTIAL_NOT_TOTAL")
        potential = {v: _exact(value) for v, value in potential.items()}
        return {
            (u, v): potential[v] - potential[u]
            for u, v in self.edges
        }

    def solve(
        self,
        defect: Dict[Edge, Fraction],
        gauge_vertex: Optional[str] = None,
    ) -> ExactRepairReceipt:
        """Solve ``d0 phi = defect``; refuse when the defect is not exact.

        The requested gauge vertex fixes its own component; every other
        component is fixed at its smallest vertex name.
        """
        values = {edge: _exact(value) for edge, value in defect.items()}
        undeclared = sorted(set(values) - set(self.edges))
        if undeclared:
            raise ValueError(f"UNTYPED_DEFECT: {undeclared!r} are not carrier edges")
        if gauge_vertex is not None and gauge_vertex not in self._adj:
            raise ValueError("UNKNOWN_GAUGE_VERTEX")
        v0 = gauge_vertex if gauge_vertex is not None else self.vertices[0]
        input_norm = sum((abs(v) for v in values.values()), Fraction(0))
        potential: Dict[str, Fraction] = {}
        roots = [v0] + [v for v in self.vertices if v != v0]
        for root in roots:
            if root in potential:
                continue
            potential[root] = Fraction(0)
            queue: List[str] = [root]
            while queue:
                curr = queue.pop(0)
                for nxt, direction, idx in self._adj[curr]:
                    edge_val = values.get(self.edges[idx], Fraction(0))
                    nxt_val = potential[curr] + (edge_val if direction == 1 else -edge_val)
                    if nxt not in potential:
                        potential[nxt] = nxt_val
                        queue.append(nxt)
                    elif potential[nxt] != nxt_val:
                        return ExactRepairReceipt(
                            operation="E",
                            paper_id="DDC-E",
                            success=False,
                            input_norm=input_norm,
                            residual_norm=input_norm,
                            gauge_vertex=v0,
                            potential={},
                            error=NOT_EXACT,
                        )

        d0 = self.coboundary_0(potential)
        repaired = {e: values.get(e, Fraction(0)) - d0[e] for e in self.edges}
        residual_norm = sum((abs(v) for v in repaired.values()), Fraction(0))
        return ExactRepairReceipt(
            operation="E",
            paper_id="DDC-E",
            success=residual_norm == 0,
            input_norm=input_norm,
            residual_norm=residual_norm,
            gauge_vertex=v0,
            potential=potential,
            error=None,
            repaired=repaired,
        )
