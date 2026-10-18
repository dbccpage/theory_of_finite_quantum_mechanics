"""Harmonic cycle-space basis.

Computes an orthonormal basis for the harmonic cycle space: the nullspace of
the incidence matrix transpose B^T (the orthogonal complement of im(B)). With
B the (edges x nodes) incidence matrix, the harmonic forms live in edge-space
and their count equals the first Betti number beta_1.
"""

from __future__ import annotations
from typing import List

import numpy as np

from omega_engine.crates.type.finite_directed_graph import FiniteDirectedGraph


def compute_harmonic_basis(topology: FiniteDirectedGraph) -> List[np.ndarray]:
    edges = topology.edges() if callable(topology.edges) else topology.edges
    if not edges:
        return []

    d0 = topology.incidence_d0()
    b = np.array([[float(x) for x in row] for row in d0.data], dtype=float)

    bt = b.T
    u, s, vh = np.linalg.svd(bt, full_matrices=True)

    basis = []
    n_edges = len(edges)
    for i in range(n_edges):
        sv = s[i] if i < len(s) else 0.0
        if sv < 1e-10:
            basis.append(vh[i, :].copy())
    return basis
