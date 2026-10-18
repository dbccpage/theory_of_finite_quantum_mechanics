"""Discrete Wheeler-DeWitt and hypersurface diffeomorphism constraint cochains.

AuthorityEffect: None.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple
import numpy as np

from complex import SimplicialComplex
from simplex import regular_simplex_dihedral_angle


@dataclass
class CauchySlice3D:
    """A 3D spatial Cauchy slice with simplicial triangulation and canonical data."""

    complex_: SimplicialComplex
    edge_lengths: Dict[Tuple[int, int], float]
    conjugate_momenta: Dict[Tuple[int, int], float] = field(default_factory=dict)
    vertex_coords: Optional[Dict[int, np.ndarray]] = None

    def __post_init__(self) -> None:
        for edge in self.complex_.cells.get(1, []):
            can_e = tuple(sorted(edge))
            if can_e not in self.conjugate_momenta:
                self.conjugate_momenta[can_e] = 0.0


def compute_discrete_scalar_curvature(
    vertex_idx: int,
    incident_edges: List[Tuple[int, int]],
    edge_lengths: Dict[Tuple[int, int], float],
    deficit_angles: Dict[Tuple[int, int], float],
    dual_volume: float = 1.0,
    require_complete_data: bool = True,
) -> float:
    """Compute discrete scalar Ricci curvature R(v) at vertex v.

    Regge formula for discrete scalar curvature:
        R(v) = (2 / V_v) * sum_{e in star(v)} epsilon_e * l_e
    where V_v is the dual (Voronoi or barycentric) cell volume at vertex v.
    """
    if dual_volume <= 1e-14:
        raise ValueError("Dual cell volume must be positive")

    curv_sum = 0.0
    for e in incident_edges:
        can_e = tuple(sorted(e))
        if require_complete_data:
            if can_e not in deficit_angles:
                raise KeyError(f"Missing edge {can_e} in deficit_angles dictionary")
            if can_e not in edge_lengths:
                raise KeyError(f"Missing edge {can_e} in edge_lengths dictionary")
            eps = deficit_angles[can_e]
            length = edge_lengths[can_e]
        else:
            eps = deficit_angles.get(can_e, 0.0)
            length = edge_lengths.get(can_e, 1.0)
        curv_sum += eps * length

    return float((2.0 / dual_volume) * curv_sum)


@dataclass
class DiscreteWDWConstraintSystem:
    """Discrete Wheeler-DeWitt Hamiltonian and momentum constraint cochain system."""

    slice_: CauchySlice3D
    deficit_angles: Dict[Tuple[int, int], float]

    def build_momentum_constraint_cochain(self) -> np.ndarray:
        """Assemble spatial diffeomorphism / momentum constraint 1-cochain omega_diff in C^1.

        At each edge e, omega_diff(e) represents the deviation from momentum constraint satisfaction.
        In canonical form, this is proportional to the extrinsic curvature momentum.
        """
        edges = self.slice_.complex_.cells.get(1, [])
        cochain = np.zeros(len(edges), dtype=float)
        for idx, e in enumerate(edges):
            can_e = tuple(sorted(e))
            cochain[idx] = self.slice_.conjugate_momenta.get(can_e, 0.0)
        return cochain

    def build_hamiltonian_constraint_cochain(self) -> np.ndarray:
        """Assemble discrete Wheeler-DeWitt scalar constraint 0-cochain H_perp in C^0.

        At each vertex v, H_perp(v) = (kinetic term - potential term):
            H_perp(v) = sum_{e} (pi_e)^2 - R(v)
        """
        vertices = self.slice_.complex_.cells.get(0, [])
        cochain = np.zeros(len(vertices), dtype=float)

        for idx, v_tuple in enumerate(vertices):
            v = v_tuple[0]
            incident = [e for e in self.slice_.complex_.cells.get(1, []) if v in e]
            r_v = compute_discrete_scalar_curvature(
                v, incident, self.slice_.edge_lengths, self.deficit_angles
            )
            kinetic = sum(
                (self.slice_.conjugate_momenta.get(tuple(sorted(e)), 0.0) ** 2)
                for e in incident
            )
            cochain[idx] = kinetic - r_v

        return cochain

    def build_total_constraint_cochain(self) -> np.ndarray:
        """Assemble the combined constraint cochain in C^1(Sigma).

        WARNING (Hamiltonian Blind Spot):
        Encoding omega = diff + d_0 @ h_perp maps the vertex Hamiltonian defect
        directly into the coboundary image im(d_0). Under the quotient minimization
        Phi_{d_0}(omega) = min_alpha ||diff + d_0 h_perp - d_0 alpha||_1 = Phi_{d_0}(diff),
        the Hamiltonian violation is absorbed into alpha and completely invisible to
        the quotient score. For a sound diagnostic, use build_joint_constraint_system()
        or evaluate the Hamiltonian violation ||H_perp||_1 separately.
        """
        d0 = self.slice_.complex_.coboundary_matrix(0)
        h_perp = self.build_hamiltonian_constraint_cochain()
        diff = self.build_momentum_constraint_cochain()

        return diff + d0 @ h_perp

    def build_joint_constraint_system(self) -> Tuple[np.ndarray, np.ndarray, float]:
        """Assemble the joint constraint system in the direct-sum space C^1(Sigma) (+) C^0(Sigma).

        In this direct-sum formulation:
            Omega_joint = (p, H_perp) in C^1 (+) C^0
            D_joint = [d_0; 0] : C^0 -> C^1 (+) C^0
        The quotient distance satisfies:
            Phi_{D_joint}(Omega_joint) = min_alpha ||p - d_0 alpha||_1 + ||H_perp||_1
                                      = Phi_{d_0}(p) + ||H_perp||_1.
        This preserves both momentum and Hamiltonian constraint violations without
        allowing scalar Hamiltonian defects to disappear into the spatial gauge orbit.

        Returns:
            (omega_joint, D_joint, hamiltonian_l1_norm)
        """
        d0 = self.slice_.complex_.coboundary_matrix(0)
        diff = self.build_momentum_constraint_cochain()
        h_perp = self.build_hamiltonian_constraint_cochain()

        m_edges, n_verts = d0.shape
        omega_joint = np.concatenate([diff, h_perp])
        d0_joint = np.vstack([d0, np.zeros((len(h_perp), n_verts), dtype=float)])
        h_norm = float(np.sum(np.abs(h_perp)))

        return omega_joint, d0_joint, h_norm


def build_hamiltonian_scalar_constraint(
    vertices: Sequence[int],
    edges: Sequence[Tuple[int, int]],
    tetrahedra: Sequence[Tuple[int, int, int, int]],
    edge_lengths: Dict[Tuple[int, int], float],
    conjugate_momenta: Dict[Tuple[int, int], float],
    dual_vertex_volume: float = 1.0,
) -> Dict[int, float]:
    """Compute discrete Hamiltonian scalar constraint at each vertex on a closed 3-manifold.

    H(v) = sum_{e in star(v)} (pi_e)^2 - R(v)
    where R(v) is discrete Ricci curvature: (2 / V_v) sum_{e in star(v)} eps_e l_e.
    For regular simplicial complexes, uses regular tetrahedron dihedral angle.
    For general simplicial complexes, computes geometric dihedral angles per tetrahedron.
    """
    from simplex import tetrahedron_dihedral_angle

    edge_lens_arr = [edge_lengths.get(tuple(sorted(e)), 1.0) for e in edges]
    is_regular = len(edge_lens_arr) > 0 and np.allclose(edge_lens_arr, edge_lens_arr[0], atol=1e-12)

    edge_dihedrals: Dict[Tuple[int, int], List[float]] = {tuple(sorted(e)): [] for e in edges}
    theta_reg = regular_simplex_dihedral_angle(3)

    for tet in tetrahedra:
        tet_sq = {}
        for u, w in itertools.combinations(tet, 2):
            can_e = tuple(sorted((u, w)))
            tet_sq[can_e] = edge_lengths[can_e] ** 2

        tet_verts = list(tet)
        v_to_local = {v: i for i, v in enumerate(tet_verts)}
        local_sq = {
            (v_to_local[u], v_to_local[w]): tet_sq[tuple(sorted((u, w)))]
            for u, w in itertools.combinations(tet, 2)
        }

        for u, w in itertools.combinations(tet, 2):
            can_e = tuple(sorted((u, w)))
            if can_e in edge_dihedrals:
                if is_regular:
                    edge_dihedrals[can_e].append(theta_reg)
                else:
                    loc_u, loc_w = v_to_local[u], v_to_local[w]
                    loc_edge = (min(loc_u, loc_w), max(loc_u, loc_w))
                    th = tetrahedron_dihedral_angle(local_sq, loc_edge)
                    edge_dihedrals[can_e].append(th)

    deficit_angles: Dict[Tuple[int, int], float] = {}
    for e in edges:
        can_e = tuple(sorted(e))
        dih_list = edge_dihedrals.get(can_e, [])
        deficit_angles[can_e] = 2.0 * math.pi - sum(dih_list)

    H: Dict[int, float] = {}
    for v in vertices:
        incident = [tuple(sorted(e)) for e in edges if v in e]
        r_v = compute_discrete_scalar_curvature(
            v, incident, edge_lengths, deficit_angles, dual_volume=dual_vertex_volume
        )
        kinetic = sum(conjugate_momenta.get(e, 0.0) ** 2 for e in incident)
        H[v] = kinetic - r_v

    return H


def build_momentum_vector_constraint(
    edges: Sequence[Tuple[int, int]],
    conjugate_momenta: Dict[Tuple[int, int], float],
) -> np.ndarray:
    """Return momentum constraint 1-cochain."""
    return np.array([conjugate_momenta.get(tuple(sorted(e)), 0.0) for e in edges], dtype=float)


def build_total_constraint_cochain(
    vertices: Sequence[int],
    edges: Sequence[Tuple[int, int]],
    conjugate_momenta: Dict[Tuple[int, int], float],
    hamiltonian_cochain: Dict[int, float],
) -> Tuple[np.ndarray, np.ndarray]:
    """Assemble naive total constraint cochain omega = p + d0 H in C^1.

    Returns (omega, d0).
    """
    v_to_idx = {v: i for i, v in enumerate(vertices)}
    m = len(edges)
    n = len(vertices)
    d0 = np.zeros((m, n), dtype=float)
    for i, (u, w) in enumerate(edges):
        d0[i, v_to_idx[u]] = -1.0
        d0[i, v_to_idx[w]] = 1.0

    p = np.array([conjugate_momenta.get(tuple(sorted(e)), 0.0) for e in edges], dtype=float)
    H = np.array([hamiltonian_cochain.get(v, 0.0) for v in vertices], dtype=float)
    total_omega = p + d0 @ H
    return total_omega, d0


def build_joint_constraint_system(
    vertices: Sequence[int],
    edges: Sequence[Tuple[int, int]],
    conjugate_momenta: Dict[Tuple[int, int], float],
    hamiltonian_cochain: Dict[int, float],
) -> Tuple[np.ndarray, np.ndarray, float]:
    """Assemble joint constraint system in C^1 (+) C^0: (Omega_joint, D_joint, H_norm)."""
    v_to_idx = {v: i for i, v in enumerate(vertices)}
    m = len(edges)
    n = len(vertices)
    d0 = np.zeros((m, n), dtype=float)
    for i, (u, w) in enumerate(edges):
        d0[i, v_to_idx[u]] = -1.0
        d0[i, v_to_idx[w]] = 1.0

    p = np.array([conjugate_momenta.get(tuple(sorted(e)), 0.0) for e in edges], dtype=float)
    H = np.array([hamiltonian_cochain.get(v, 0.0) for v in vertices], dtype=float)

    omega_joint = np.concatenate([p, H])
    D_joint = np.vstack([d0, np.zeros((n, n), dtype=float)])
    H_norm = float(np.sum(np.abs(H)))
    return omega_joint, D_joint, H_norm


def solve_joint_wdw_constraints(
    vertices: Sequence[int],
    edges: Sequence[Tuple[int, int]],
    conjugate_momenta: Dict[Tuple[int, int], float],
    hamiltonian_cochain: Dict[int, float],
    tol: float = 1e-8,
) -> Dict[str, Any]:
    """Solve joint WDW constraints and return certified residual breakdown."""
    omega_joint, D_joint, H_norm = build_joint_constraint_system(
        vertices, edges, conjugate_momenta, hamiltonian_cochain
    )
    from dual_witness import DualCertifiedL1Solver
    solver = DualCertifiedL1Solver(tol=tol)
    res = solver.solve(omega_joint, D_joint)

    check_atol = max(1e-7, tol * 10)
    alpha = getattr(res, "primal_alpha", None)
    w = getattr(res, "dual_witness", None)
    r = getattr(res, "primal_residual", None)
    gap = getattr(res, "duality_gap", None)
    div_norm = getattr(res, "dual_divergence_norm", None)

    if alpha is not None and w is not None and r is not None and gap is not None:
        res_ok = np.allclose(r, omega_joint - D_joint @ alpha, atol=check_atol)
        div_ok = (div_norm is not None and div_norm <= check_atol) or np.linalg.norm(D_joint.T @ w, ord=np.inf) <= check_atol
        bounds_ok = np.all(np.abs(w) <= 1.0 + check_atol)
        gap_ok = gap <= check_atol
        is_certified = bool(res_ok and div_ok and bounds_ok and gap_ok)
    else:
        is_certified = bool(getattr(res, "is_certified", False))

    return {
        "joint_quotient_distance": res.primal_obj,
        "momentum_quotient_distance": res.primal_obj - H_norm,
        "hamiltonian_l1_violation": H_norm,
        "is_closed": res.is_closed,
        "is_certified": is_certified,
        "authority_effect": "None",
    }
