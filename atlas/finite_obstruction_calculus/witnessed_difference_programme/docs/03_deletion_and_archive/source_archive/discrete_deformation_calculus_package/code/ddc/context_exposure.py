"""DDC letter C: context exposure of a window and its boundary interface.

C restricts an ambient cochain to a window ``W`` and exposes the edges that
straddle it. C changes the carrier; it never repairs. Law 8 ("context exposure
is not repair") is enforced on the tape: a C step may not lower Phi1 or Gamma2.
Hiding obstruction by re-scoping has to be priced as a descent with a loss
ledger (D) or a licensed lift (Λ).

``glue`` recombines two exposures that agree on every shared edge; the result
is unique because each edge of the union is internal or boundary to a window.

Leaf module: standard library only, loadable by path. AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Set, Tuple

Edge = Tuple[str, str]


def _exact(value: object) -> Fraction:
    if isinstance(value, (bool, float)) or not isinstance(value, (int, Fraction)):
        raise ValueError(f"NOT_EXACT: {value!r}")
    return Fraction(value)


@dataclass(frozen=True)
class ContextExposureReceipt:
    operation: str
    paper_id: str
    window_vertices: List[str]
    internal_edges: List[Edge]
    boundary_edges: List[Edge]
    internal_cochain: Dict[Edge, Fraction]
    boundary_cochain: Dict[Edge, Fraction]
    status: str
    authority_effect: str = "None"


class ContextWindowExtractor:
    """Partitions an ambient cochain into internal and boundary-interface parts."""

    def __init__(self, edges: List[Edge]):
        if len(set(edges)) != len(edges):
            raise ValueError("DUPLICATE_EDGE")
        for u, v in edges:
            if u == v:
                raise ValueError(f"SELF_LOOP: {(u, v)!r}")
        self.edges = list(edges)

    def expose(
        self,
        window_vertices: Set[str],
        ambient_cochain: Dict[Edge, Fraction],
    ) -> ContextExposureReceipt:
        """Expose the window's internal cochain and its straddling edges."""
        if set(ambient_cochain) - set(self.edges):
            raise ValueError("UNTYPED_DEFECT")
        ambient_cochain = {edge: _exact(value) for edge, value in ambient_cochain.items()}
        internal_edges: List[Edge] = []
        boundary_edges: List[Edge] = []
        for u, v in self.edges:
            u_in = u in window_vertices
            v_in = v in window_vertices
            if u_in and v_in:
                internal_edges.append((u, v))
            elif u_in or v_in:
                boundary_edges.append((u, v))
        return ContextExposureReceipt(
            operation="C",
            paper_id="DDC-C",
            window_vertices=sorted(window_vertices),
            internal_edges=internal_edges,
            boundary_edges=boundary_edges,
            internal_cochain={e: _exact(ambient_cochain.get(e, Fraction(0))) for e in internal_edges},
            boundary_cochain={e: _exact(ambient_cochain.get(e, Fraction(0))) for e in boundary_edges},
            status="CONTEXT_EXPOSED",
        )


def exposed_values(receipt: ContextExposureReceipt) -> Dict[Edge, Fraction]:
    values = dict(receipt.internal_cochain)
    values.update(receipt.boundary_cochain)
    return values


def glue(
    first: ContextExposureReceipt, second: ContextExposureReceipt
) -> Optional[Dict[Edge, Fraction]]:
    """Joint cochain on every exposed edge, or ``None`` when a shared edge disagrees."""
    a = exposed_values(first)
    b = exposed_values(second)
    for edge in set(a) & set(b):
        if a[edge] != b[edge]:
            return None
    joint = dict(a)
    joint.update(b)
    return joint
