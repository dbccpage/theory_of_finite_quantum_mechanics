"""Lattice Gauge Holonomies & Wilson Loop Defects for GS-000 Extension.

AuthorityEffect: None. Discrete gauge theory on 2-dimensional cell complexes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class Plaquette:
    """An oriented 2-cell (plaquette) in a discrete cell complex.

    boundary_edges: tuple of (edge_index, orientation) where orientation is +1 or -1.
    """

    plaquette_id: int
    boundary: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class CellComplex2D:
    """A 2D cell complex consisting of vertices, edges, and plaquettes."""

    num_vertices: int
    edges: tuple[tuple[int, int], ...]  # (source, target)
    plaquettes: tuple[Plaquette, ...]

    @property
    def num_edges(self) -> int:
        return len(self.edges)

    @property
    def num_plaquettes(self) -> int:
        return len(self.plaquettes)


class U1GaugeField:
    """A U(1) lattice gauge field assigning a phase angle theta_e in [-pi, pi) to each edge."""

    def __init__(self, num_edges: int, edge_phases: Sequence[float] | np.ndarray | None = None) -> None:
        self.num_edges = num_edges
        if edge_phases is None:
            self.phases = np.zeros(num_edges, dtype=float)
        else:
            if len(edge_phases) != num_edges:
                raise ValueError("Edge phases count mismatch")
            self.phases = np.mod(np.asarray(edge_phases, dtype=float) + np.pi, 2 * np.pi) - np.pi

    def link_variable(self, edge: int) -> complex:
        """Returns U_e = exp(i * theta_e)."""
        return np.exp(1j * self.phases[edge])

    def plaquette_holonomy(self, plaquette: Plaquette) -> complex:
        """Compute holonomy W_square = prod_{e in d_square} U_e^{sigma_e}."""
        w = 1.0 + 0.0j
        for e, orient in plaquette.boundary:
            w *= np.exp(1j * orient * self.phases[e])
        return w

    def plaquette_flux(self, plaquette: Plaquette) -> float:
        """Compute gauge-invariant plaquette flux angle Phi_square in (-pi, pi]."""
        w = self.plaquette_holonomy(plaquette)
        return float(np.angle(w))

    def wilson_curvature_defect(self, plaquette: Plaquette) -> float:
        """Compute Re Tr(I - W_square) = 1 - cos(Phi_square)."""
        w = self.plaquette_holonomy(plaquette)
        return float(1.0 - np.real(w))


class SU2GaugeField:
    """An SU(2) lattice gauge field assigning a 2x2 unitary matrix with det=1 to each edge."""

    def __init__(self, num_edges: int, edge_matrices: Sequence[np.ndarray] | None = None) -> None:
        self.num_edges = num_edges
        if edge_matrices is None:
            self.matrices = [np.eye(2, dtype=complex) for _ in range(num_edges)]
        else:
            if len(edge_matrices) != num_edges:
                raise ValueError("Edge matrices count mismatch")
            self.matrices = [np.asarray(m, dtype=complex) for m in edge_matrices]

    def plaquette_holonomy(self, plaquette: Plaquette) -> np.ndarray:
        """Compute SU(2) holonomy matrix W_square = prod U_e^{sigma_e}."""
        w = np.eye(2, dtype=complex)
        for e, orient in plaquette.boundary:
            m = self.matrices[e]
            if orient == -1:
                m = m.conj().T
            w = w @ m
        return w

    def wilson_curvature_defect(self, plaquette: Plaquette) -> float:
        """Compute Re Tr(I - W_square) in SU(2). Tr(I) = 2."""
        w = self.plaquette_holonomy(plaquette)
        return float(np.real(2.0 - np.trace(w)))


def evaluate_u1_flux_l1(field: U1GaugeField, complex2d: CellComplex2D, weights: Sequence[float]) -> float:
    """Compute orbit-weighted plaquette flux l1 gauge sum_square w_square |Phi_square|."""
    if len(weights) != complex2d.num_plaquettes:
        raise ValueError("Plaquette weights count mismatch")
    total = 0.0
    for p, w in zip(complex2d.plaquettes, weights):
        flux = field.plaquette_flux(p)
        total += w * abs(flux)
    return total


def check_disjoint_plaquette_additivity(
    complex2d: CellComplex2D,
    field_a: U1GaugeField,
    field_b: U1GaugeField,
    weights: Sequence[float],
    active_plaquettes_a: set[int],
    active_plaquettes_b: set[int],
    atol: float = 1e-9,
) -> bool:
    """Verify that independent flux excitations on disjoint plaquettes add linearly."""
    if active_plaquettes_a.intersection(active_plaquettes_b):
        raise ValueError("Plaquette sets must be disjoint")

    # Combined field
    combined_phases = field_a.phases + field_b.phases
    field_combined = U1GaugeField(complex2d.num_edges, combined_phases)

    val_a = evaluate_u1_flux_l1(field_a, complex2d, weights)
    val_b = evaluate_u1_flux_l1(field_b, complex2d, weights)
    val_comb = evaluate_u1_flux_l1(field_combined, complex2d, weights)

    return abs(val_comb - (val_a + val_b)) <= atol
