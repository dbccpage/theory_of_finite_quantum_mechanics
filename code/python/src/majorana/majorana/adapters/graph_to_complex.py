from __future__ import annotations


from typing import Any, Sequence

from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix
from omega_engine.crates.majorana.core.gf2_schema import mod2
from omega_engine.crates.majorana.carriers.parity_carrier import MajoranaParityCarrier


class GraphToComplexAdapter:
    """Adapter to map custom parity-check cell complexes to exact chain complexes."""

    def __init__(
        self,
        vertices: Sequence[Any],
        edges: Sequence[tuple[int, int]],
        faces: Sequence[Sequence[int]],
    ):
        """Initialize the adapter.

        Args:
            vertices: List of vertex identifiers (C0 basis).
            edges: List of edges as pairs of vertex indices (C1 basis).
            faces: List of faces as sequences of edge indices (C2 basis).
        """
        self.vertices = list(vertices)
        self.edges = list(edges)
        self.faces = [list(f) for f in faces]

        self.num_vertices = len(self.vertices)
        self.num_edges = len(self.edges)
        self.num_faces = len(self.faces)

        self._build_boundary_operators()

    @classmethod
    def from_finite_directed_graph(
        cls, graph: Any, faces: Sequence[Sequence[int]] = ()
    ) -> GraphToComplexAdapter:
        """Construct a complex adapter directly from a FiniteDirectedGraph."""
        nodes = list(graph.nodes())
        node_index = {node: i for i, node in enumerate(nodes)}

        edges: list[tuple[int, int]] = []
        for u, v in graph.edges():
            u_idx = u if (isinstance(u, int) and 0 <= u < len(nodes)) else node_index.get(u)
            v_idx = v if (isinstance(v, int) and 0 <= v < len(nodes)) else node_index.get(v)

            if u_idx is None:
                u_idx = node_index[u]
            if v_idx is None:
                v_idx = node_index[v]

            edges.append((u_idx, v_idx))

        return cls(nodes, edges, faces)

    def _build_boundary_operators(self) -> None:
        d0_data = [[0] * self.num_vertices for _ in range(self.num_edges)]
        for j, (u, v) in enumerate(self.edges):
            if u < 0 or u >= self.num_vertices or v < 0 or v >= self.num_vertices:
                raise ValueError(f"Invalid vertex indices in edge {j}: ({u}, {v})")
            d0_data[j][u] = 1
            d0_data[j][v] = 1

        self.D0 = GF2Matrix(d0_data)

        if self.num_faces == 0:
            d1_data = [[0] * self.num_edges]
        else:
            d1_data = [[0] * self.num_edges for _ in range(self.num_faces)]

        for i, face_edges in enumerate(self.faces):
            for edge_idx in face_edges:
                if edge_idx < 0 or edge_idx >= self.num_edges:
                    raise ValueError(f"Invalid edge index {edge_idx} in face {i}")
                d1_data[i][edge_idx] = 1

        self.D1 = GF2Matrix(d1_data, cols=self.num_edges)

        for col_idx in range(self.num_vertices):
            col = [self.D0[row_idx][col_idx] for row_idx in range(self.num_edges)]
            result = self.D1.mat_vec_mul(col)
            if any(result):
                raise ValueError(
                    f"Complex validation failed: D1 * D0 != 0 at vertex {col_idx}. "
                    f"Got boundary: {result}"
                )

    def create_carrier(self, residual_mismatch: Sequence[int], metadata: dict[str, Any] | None = None) -> MajoranaParityCarrier:
        """Create a verified MajoranaParityCarrier representing readout mismatch r."""
        r = [mod2(x) for x in residual_mismatch]
        if len(r) != self.num_edges:
            raise ValueError(
                f"Mismatch vector length {len(r)} must equal edge count {self.num_edges}"
            )

        meta = dict(metadata) if metadata is not None else {}
        meta.update({
            "graph_vertices": self.vertices,
            "graph_edges": self.edges,
            "graph_faces": self.faces,
        })
        if self.num_faces == 0:
            meta["zero_coherence_placeholder"] = True

        carrier = MajoranaParityCarrier(
            carrier_kind="majorana_parity_gf2",
            coefficient_field="GF2",
            D0=self.D0.to_list(),
            D1=self.D1.to_list(),
            residual=r,
            metadata=meta,
        )
        return carrier.normalized()




