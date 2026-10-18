"""Harmonic density matrix -- a topological fingerprint.

Faithful port of ``crates/omega_engine.crates.engine/src/quantum/harmonic_density.rs``.

Builds a mixed quantum state over the space of harmonic 1-forms (the nullspace
of the Hodge Laplacian). The rank of this state is the first Betti number
beta_1 of the graph. Density math is reused from
:class:`omega_linear_algebra.density.NumericalDensityMatrix`.
"""

from __future__ import annotations
from typing import List, Tuple

import numpy as np

from omega_engine.crates.linear_algebra_theory.density import (
    DensityMatrixConfig,
    DensityMatrixCandidate,
    NumericalDensityMatrix,
    NoValidStates,
    ZeroDimension,
    DimensionMismatch,
    NonPhysical,
)
from omega_engine.crates.type.finite_directed_graph import (
    FiniteDirectedGraph,
    TheoremProvenance,
)

from omega_engine.crates.operator.lambda_op.lamb_qm_cycle_space import compute_harmonic_basis


def density_from_harmonics(
    harmonics: List[np.ndarray], tol: float
) -> NumericalDensityMatrix:
    if not harmonics:
        raise NoValidStates("no valid states")
    m = len(harmonics[0])
    beta = len(harmonics)

    for i in range(beta):
        for j in range(beta):
            dot = float(np.dot(harmonics[i], harmonics[j]))
            target = 1.0 if i == j else 0.0
            if abs(dot - target) > tol:
                raise NonPhysical("harmonic basis not orthonormal")

    rho = np.zeros((m, m), dtype=complex)
    for omega in harmonics:
        rho += np.outer(omega, omega) / beta

    cfg = DensityMatrixConfig.default()
    return DensityMatrixCandidate.from_rho(rho).validate(cfg)


def harmonic_density(
    edges: List[Tuple[int, int]], n_vertices: int, tol: float
) -> NumericalDensityMatrix:
    if n_vertices == 0:
        raise ZeroDimension("density matrix dimension must be positive")

    for u, v in edges:
        if u >= n_vertices or v >= n_vertices:
            raise DimensionMismatch(
                f"dimension mismatch: expected {n_vertices}, actual {max(u, v) + 1}"
            )

    if not edges:
        raise NoValidStates("no valid states")

    from omega_engine.crates.homology_theory import DirectedGraphBuilder
    graph = DirectedGraphBuilder.from_anonymous(
        n_vertices, list(edges), TheoremProvenance(verification_source="engine_internal")
    )
    harmonics = compute_harmonic_basis(graph)
    return density_from_harmonics(harmonics, tol)



