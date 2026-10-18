from __future__ import annotations
"""Build a Carrier from a finite directed graph and a set of triangle faces.

Port of ``graph_carrier.rs``. d0 is the graph incidence; d1 is the simplicial
face boundary of each declared triangle, oriented so that d1 . d0 = 0. A
triangle whose three edges are not all present is rejected.
"""


from typing import List, Tuple

from .carrier import Carrier
from .errors import TriangleMissingEdge
from .finite_directed_graph import FiniteDirectedGraph
from .ids import TheoremProvenance
from .qmatrix import QMatrix


def graph_carrier(
    graph: FiniteDirectedGraph,
    triangles: List[Tuple[int, int, int]],
    weights: List,
    provenance: TheoremProvenance,
) -> Carrier:
    c0_dim = graph.num_nodes() if callable(graph.num_nodes) else graph.num_nodes
    c1_dim = graph.num_edges() if callable(graph.num_edges) else graph.num_edges
    c2_dim = len(triangles)

    d0 = graph.incidence_d0()  

    d1 = QMatrix.zero(c2_dim, c1_dim)
    for face, tri in enumerate(triangles):
        a, b, c = sorted(tri)
        for x, y, coeff in ((a, b, 1), (b, c, 1), (a, c, -1)):
            found = graph.find_edge(x, y)
            if found is None:
                raise TriangleMissingEdge(
                    f"triangle {tri} requires edge between {x} and {y}, which is absent"
                )
            idx, orient = found
            d1.data[face][idx] += coeff * orient

    return Carrier.new(c0_dim, c1_dim, c2_dim, d0, d1, weights, provenance)

