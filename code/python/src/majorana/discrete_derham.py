from __future__ import annotations
"""Base graph/cochain finite operator.

This module contains the finite graph incidence representation acting as
the coboundary operator (0->1) on a network.

SCOPE: This is a finite discrete/combinatorial approximation on a graph-like
grid complex, NOT continuous de Rham cohomology. It evaluates finite
combinatorial incidence matrices on graph-like grids; it does NOT verify the
continuous de Rham topology of smooth manifolds. The "de Rham" name refers to
the discrete analogy (incidence as a discrete coboundary), not to a proof about
continuous differential forms.
"""


from typing import List, Tuple

import numpy as np


class DiscreteDeRham:
    """Finite graph coboundary operator using incidence matrix.

    Edges are treated as oriented; reversing (u,v) flips its sign.

    This is a finite discrete/combinatorial approximation on a grid complex,
    NOT continuous de Rham cohomology of a manifold. All methods below operate
    on finite incidence data; they do not certify continuous topology.
    """

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int]]):
        if num_vertices <= 0:
            raise ValueError("Graph must have at least one vertex.")

        for u, v in edges:
            if not (0 <= u < num_vertices and 0 <= v < num_vertices):
                raise ValueError(
                    f"Edge ({u}, {v}) contains invalid vertex indices for V={num_vertices}"
                )

        self.V = num_vertices
        self.edges = edges
        self.E = len(edges)
        if self.E > 0:
            self.B = self._build_incidence_matrix()
        else:
            self.B = np.zeros((0, self.V))

    def _build_incidence_matrix(self) -> np.ndarray:
        """Build B in R^{|E| x |V|}, with -1 at source and +1 at target."""
        incidence = np.zeros((self.E, self.V))
        for i, (u, v) in enumerate(self.edges):
            if u == v:
                continue
            incidence[i, u] = -1.0
            incidence[i, v] = 1.0
        return incidence

    def d0(self, f: np.ndarray) -> np.ndarray:
        """Compute (d_0 f)(e_uv) = f(v) - f(u)."""
        return self.B @ f

    def divergence(self, omega: np.ndarray) -> np.ndarray:
        """Compute d_0^* omega = B^T omega."""
        return self.B.T @ omega

    def betti_1(self, num_components: int = 1) -> int:
        """Return the combinatorial graph first Betti number beta_1(G) = |E| - |V| + num_components.

        This is the cycle rank of the finite graph (a combinatorial count),
        NOT the de Rham first Betti number of a continuous manifold.
        """
        return self.E - self.V + num_components

    def nullspace_rank(self) -> int:
        """Compute the rank of the incidence matrix."""
        if self.E == 0:
            return 0
        return int(np.linalg.matrix_rank(self.B))

