"""GF(2) chain complex over finite directed graphs.

Implements boundary operators d1: C1 -> C0 and d2: C2 -> C1 over GF(2),
with the chain complex validation law d1 . d2 = 0.

contract_id: urn:omega:math:chain_complex:v1.0.0
"""
from __future__ import annotations

# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jeremy H. Carroll

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .gf2_matrix import GF2Matrix

if TYPE_CHECKING:
    from omega_engine.crates.homology_theory.finite_directed_graph import FiniteDirectedGraph
    from omega_engine.crates.homology_theory.gf2_cochain_complex import GF2CochainComplex


@dataclass
class GF2ChainComplex:
    """GF(2) chain complex over a finite directed graph with optional 2-cell faces.

    contract_id: urn:omega:math:chain_complex:v1.0.0

    Boundary law: d1 . d2 = 0 (validated by validate_chain).
    """
    graph: FiniteDirectedGraph
    faces: tuple[tuple[int, ...], ...]

    @property
    def num_vertices(self) -> int:
        return len(self.graph.nodes())

    @property
    def num_edges(self) -> int:
        return len(self.graph.edges())

    @property
    def num_faces(self) -> int:
        return len(self.faces)

    def boundary_1(self) -> GF2Matrix:
        """d1: C1 -> C0. Shape: |V| x |E|. Over GF(2), an edge contributes to both endpoints."""
        data = [[0] * self.num_edges for _ in range(self.num_vertices)]
        for edge_idx, (u, v) in enumerate(self.graph.edges()):
            data[u][edge_idx] = 1
            data[v][edge_idx] = 1
        return GF2Matrix(data)

    def boundary_2(self) -> GF2Matrix:
        """d2: C2 -> C1. Shape: |E| x |F|. Each face is a list of edge indices."""
        if self.num_faces == 0:
            return GF2Matrix.zeros(self.num_edges, 0)

        data = [[0] * self.num_faces for _ in range(self.num_edges)]
        for face_idx, edge_indices in enumerate(self.faces):
            for edge_idx in edge_indices:
                if edge_idx < 0 or edge_idx >= self.num_edges:
                    raise ValueError(f"Face {face_idx} references invalid edge {edge_idx}")
                data[edge_idx][face_idx] = 1
        return GF2Matrix(data)

    def validate_chain(self) -> None:
        """Check d1 . d2 = 0 (boundary law)."""
        b1 = self.boundary_1()
        b2 = self.boundary_2()

        for col_idx in range(b2.cols):
            face_boundary = [b2[row][col_idx] for row in range(b2.rows)]
            vertex_boundary = b1.mat_vec_mul(face_boundary)
            if any(vertex_boundary):
                raise ValueError(
                    f"Invalid chain complex: d1.d2 != 0 at face {col_idx}: {vertex_boundary}"
                )

    def to_cochain(self) -> GF2CochainComplex:
        self.validate_chain()
        from omega_engine.crates.homology_theory.gf2_cochain_complex import (
            GF2CochainComplex,
        )
        return GF2CochainComplex.from_chain(self)


