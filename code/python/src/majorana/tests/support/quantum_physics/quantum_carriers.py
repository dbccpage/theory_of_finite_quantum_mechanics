r"""
Typed finite graph, U(1), and SU(N) constructions for QM_000.

AuthorityEffect: None.

Canonical Implementation: omega_engine.crates.quantum_physics.quantum_carriers
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from scipy.optimize import linprog

from omega_engine.crates.homology_theory.finite_graph import FiniteGraph
from omega_engine.crates.linear_algebra_theory import (
    connection_laplacian as connection_laplacian,
    covariant_difference as covariant_difference,
    covariant_matrix as covariant_matrix,
    gauge_transform as gauge_transform,
    incidence_matrix_dmatrix,
    path_holonomy as path_holonomy,
)


@dataclass(frozen=True, slots=True)
class QuotientWitness:
    value: float
    potential: np.ndarray
    residual: np.ndarray
    circulation: np.ndarray
    duality_gap: float
    authority_effect: str = "None"


def incidence_matrix(graph: FiniteGraph) -> np.ndarray:
    return incidence_matrix_dmatrix(graph.n_vertices, list(graph.edges))


def primitive_difference(graph: FiniteGraph, values: Iterable[float]) -> np.ndarray:
    vertex_values = np.asarray(tuple(values), dtype=float)
    if vertex_values.shape != (graph.n_vertices,):
        raise ValueError("vertex field dimension mismatch")
    return incidence_matrix(graph) @ vertex_values


def solve_l1_quotient(
    graph: FiniteGraph,
    omega: Iterable[float],
    weights: Iterable[float],
    *,
    tolerance: float = 1e-8,
) -> QuotientWitness:
    cochain = np.asarray(tuple(omega), dtype=float)
    w = np.asarray(tuple(weights), dtype=float)
    m = len(graph.edges)
    if cochain.shape != (m,) or w.shape != (m,):
        raise ValueError("edge cochain or weight dimension mismatch")
    if not np.all(np.isfinite(cochain)) or not np.all(np.isfinite(w)):
        raise ValueError("cochains and weights must be finite")
    if np.any(w <= 0):
        raise ValueError("edge weights must be strictly positive")
    d0 = incidence_matrix(graph)
    if m == 0:
        return QuotientWitness(
            0.0,
            np.zeros(graph.n_vertices),
            np.zeros(0),
            np.zeros(0),
            0.0,
        )

    n = graph.n_vertices
    objective = np.concatenate((w, w, np.zeros(n)))
    equality = np.concatenate((np.eye(m), -np.eye(m), -d0), axis=1)
    primal = linprog(
        objective,
        A_eq=equality,
        b_eq=cochain,
        bounds=[(0.0, None)] * (2 * m) + [(None, None)] * n,
        method="highs",
    )
    dual = linprog(
        -cochain,
        A_eq=d0.T,
        b_eq=np.zeros(n),
        bounds=[(-float(weight), float(weight)) for weight in w],
        method="highs",
    )
    if not primal.success or not dual.success:
        raise RuntimeError("primal or dual quotient LP failed")
    residual = primal.x[:m] - primal.x[m : 2 * m]
    potential = primal.x[2 * m :]
    circulation = dual.x
    dual_value = float(cochain @ circulation)
    gap = abs(float(primal.fun) - dual_value)
    if not np.allclose(residual - d0 @ potential, cochain, atol=tolerance):
        raise RuntimeError("invalid primal quotient witness")
    if not np.allclose(d0.T @ circulation, 0.0, atol=tolerance):
        raise RuntimeError("invalid circulation witness")
    if np.any(np.abs(circulation) > w + tolerance) or gap > tolerance:
        raise RuntimeError("invalid capacity or duality witness")
    return QuotientWitness(float(primal.fun), potential, residual, circulation, gap)


def cochain_to_connection(omega: Iterable[float], alpha: float) -> np.ndarray:
    cochain = np.asarray(tuple(omega), dtype=float)
    if not np.all(np.isfinite(cochain)) or not np.isfinite(alpha):
        raise ValueError("cochain and phase scale must be finite")
    return np.exp(1j * alpha * cochain)


def gell_mann(n: int) -> tuple[np.ndarray, ...]:
    if n < 2:
        raise ValueError("SU(N) label carrier requires N>=2")
    matrices: list[np.ndarray] = []
    for j in range(n):
        for k in range(j + 1, n):
            symmetric = np.zeros((n, n), dtype=complex)
            symmetric[j, k] = symmetric[k, j] = 1.0
            matrices.append(symmetric)
            antisymmetric = np.zeros((n, n), dtype=complex)
            antisymmetric[j, k] = -1j
            antisymmetric[k, j] = 1j
            matrices.append(antisymmetric)
    for ell in range(1, n):
        diagonal = np.zeros((n, n), dtype=complex)
        scale = np.sqrt(2.0 / (ell * (ell + 1)))
        diagonal[range(ell), range(ell)] = scale
        diagonal[ell, ell] = -ell * scale
        matrices.append(diagonal)
    return tuple(matrices)


def structure_constants(n: int) -> np.ndarray:
    basis = gell_mann(n)
    count = len(basis)
    constants = np.zeros((count, count, count), dtype=float)
    for a, left in enumerate(basis):
        for b, right in enumerate(basis):
            commutator = left @ right - right @ left
            for c, target in enumerate(basis):
                constants[a, b, c] = float(
                    np.real(np.trace(commutator @ target) / (4j))
                )
    return constants


def mass_phase_amplitudes(
    masses: Iterable[float], phases: Iterable[float]
) -> np.ndarray:
    mass = np.asarray(tuple(masses), dtype=float)
    phase = np.asarray(tuple(phases), dtype=float)
    if mass.ndim != 1 or phase.shape != mass.shape or mass.size == 0:
        raise ValueError("masses and phases must be nonempty vectors of equal size")
    if not np.all(np.isfinite(mass)) or not np.all(np.isfinite(phase)):
        raise ValueError("masses and phases must be finite")
    if np.any(mass < 0) or mass.sum() <= 0:
        raise ValueError("masses must be nonnegative and not all zero")
    probability = mass / mass.sum()
    return np.sqrt(probability) * np.exp(1j * phase)


__all__ = [
    "FiniteGraph",
    "QuotientWitness",
    "incidence_matrix",
    "primitive_difference",
    "solve_l1_quotient",
    "cochain_to_connection",
    "gell_mann",
    "structure_constants",
    "mass_phase_amplitudes",
    "connection_laplacian",
    "covariant_difference",
    "covariant_matrix",
    "gauge_transform",
    "incidence_matrix_dmatrix",
    "path_holonomy",
]




