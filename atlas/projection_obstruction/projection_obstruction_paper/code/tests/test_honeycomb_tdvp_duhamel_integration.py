"""Integration tests for edge-decomposed TDVP Duhamel bounds on a 2D honeycomb lattice cluster.

Validates the TDVP Duhamel Master Theorem (Theorem 1 / §5.10.1) against exact
Krylov subspace time evolution (scipy.sparse.linalg.expm_multiply) on a 2D honeycomb
lattice cluster with coordination number z=3 at bulk sites:

1. Honeycomb Cluster Topology:
   Two fused hexagonal rings (8 qubits, 9 edges) with bulk vertices of degree 3
   and boundary vertices of degree 2.
2. Two-Site Bond Correlator Enclosure:
   For O = Z_2 Z_3 on the central coordination-3 shared edge, the edge-decomposed
   Duhamel bound:
       Delta <O>(t) <= sum_{e in E} int_0^t nu_e(s) ds
   strictly encloses the exact expectation error along the TDVP trajectory.
3. Spatial Locality & Light-Cone Suppression:
   For local observable O = Z_0 on a boundary site, influence weights w_{O,e}(t-s)
   decay exponentially with graph distance d(e, 0) across the honeycomb cluster,
   and the spatially weighted Duhamel bound:
       Delta <O>(t) <= sum_{e in E} int_0^t w_{O,e}(t-s) nu_e(s) ds
   rigorously encloses the exact error across the full time window.

AuthorityEffect: None.
"""

from __future__ import annotations

import numpy as np
import pytest
import scipy.sparse as sp
from krylov_scaling_benchmark import (
    SIGMA_Z,
    SIGMA_X,
    SpinChainModel,
    build_initial_product_state,
    build_sparse_hamiltonian,
    compute_edge_normal_defects,
    evolve_exact_krylov,
    solve_mean_field_trajectory,
)
from observable_duhamel import (
    ObservableSupport,
    compute_graph_distance_table,
    compute_influence_weight,
)


def build_honeycomb_two_hexagon_cluster(
    j_zz: float = 1.0, hx: float = 0.5, hz: float = 0.0
) -> tuple[SpinChainModel, list[tuple[int, int]]]:
    """Construct an 8-qubit, two-hexagon fused honeycomb lattice cluster.

    Hexagon 1: 0 - 1 - 2 - 3 - 4 - 5 - 0
    Hexagon 2: 2 - 6 - 7 - 3 - 2 (shares edge (2, 3))
    Vertices 2 and 3 have coordination number z=3 (honeycomb bulk).
    Vertices 0, 1, 4, 5, 6, 7 have coordination number z=2 (boundary).
    """
    bonds = [
        (0, 1),
        (1, 2),
        (2, 3),  # shared coordination-3 edge
        (3, 4),
        (4, 5),
        (5, 0),
        (2, 6),
        (6, 7),
        (7, 3),
    ]
    num_qubits = 8
    model = SpinChainModel(num_qubits=num_qubits, j_zz=j_zz, hx=hx, hz=hz, bonds=bonds)
    return model, bonds


def build_full_pauli_operator(ops_dict: dict[int, np.ndarray], num_qubits: int) -> np.ndarray:
    """Build full 2^N tensor product operator from sparse site specifications."""
    eye = np.eye(2, dtype=complex)
    op_list = [ops_dict.get(i, eye) for i in range(num_qubits)]
    res = op_list[0]
    for o in op_list[1:]:
        res = np.kron(res, o)
    return res


class TestHoneycombTDVPDuhamelIntegration:
    """Integration test suite for TDVP Duhamel bounds on 2D honeycomb cluster."""

    def test_honeycomb_cluster_topology(self):
        """Verify honeycomb cluster graph coordination and distances."""
        model, bonds = build_honeycomb_two_hexagon_cluster()
        assert model.num_qubits == 8
        assert len(bonds) == 9

        # Verify degree distribution
        degrees = [0] * 8
        for u, v in bonds:
            degrees[u] += 1
            degrees[v] += 1

        # Central vertices 2 and 3 must have honeycomb coordination 3
        assert degrees[2] == 3
        assert degrees[3] == 3
        # Boundary vertices must have degree 2
        for v in [0, 1, 4, 5, 6, 7]:
            assert degrees[v] == 2

        # Verify graph distance table
        dist = compute_graph_distance_table(list(range(8)), bonds)
        assert dist[(0, 1)] == 1
        assert dist[(0, 2)] == 2
        assert dist[(0, 7)] == 4  # 0-1-2-6-7 or 0-5-4-3-7
        assert dist[(6, 7)] == 1

    def test_honeycomb_two_body_correlator_duhamel_enclosure(self):
        """Validate edge-decomposed Duhamel bound for O = Z_2 Z_3 against exact Krylov."""
        model, bonds = build_honeycomb_two_hexagon_cluster(j_zz=1.0, hx=0.5, hz=0.0)
        h_sparse = build_sparse_hamiltonian(model)

        plus = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
        init_sites = [plus] * 8
        psi0, _ = build_initial_product_state(init_sites)

        times = np.linspace(0.0, 0.2, 11)
        exact_states = evolve_exact_krylov(h_sparse, psi0, times)
        mf_traj = solve_mean_field_trajectory(model, init_sites, times)

        # Observable O = Z_2 (x) Z_3 on central coordination-3 edge
        obs_z2z3 = build_full_pauli_operator({2: SIGMA_Z, 3: SIGMA_Z}, 8)

        dt = times[1] - times[0]
        cumulative_bound = 0.0

        for step in range(len(times)):
            t = times[step]
            # Exact expectation
            psi_t = exact_states[step]
            exp_exact = float(np.real(psi_t.conj() @ (obs_z2z3 @ psi_t)))

            # Mean-field expectation (factorized product on product state)
            u_sites = mf_traj[step]
            exp_mf = float(
                np.real(u_sites[2].conj() @ (SIGMA_Z @ u_sites[2]))
                * np.real(u_sites[3].conj() @ (SIGMA_Z @ u_sites[3]))
            )
            actual_error = abs(exp_exact - exp_mf)

            # Cumulative edge-decomposed Duhamel bound
            if step > 0:
                defects_prev = compute_edge_normal_defects(model, mf_traj[step - 1])
                defects_curr = compute_edge_normal_defects(model, mf_traj[step])
                # Trapezoid step for sum_e nu_e
                cumulative_bound += 0.5 * dt * (sum(defects_prev) + sum(defects_curr))

            assert actual_error <= cumulative_bound + 1e-12, (
                f"At t={t:.3f}, actual error {actual_error:.6e} exceeds Duhamel bound {cumulative_bound:.6e}"
            )

        # Confirm non-trivial error was generated dynamically
        assert actual_error > 0.05, f"Expected noticeable correlation error by t=0.2, got {actual_error}"

    def test_honeycomb_spatial_influence_lightcone_decay(self):
        """Validate spatially weighted Duhamel bound with Lieb-Robinson decay on honeycomb."""
        # Nonzero hz=0.2 on site 0 to induce dynamical local magnetisation
        model, bonds = build_honeycomb_two_hexagon_cluster(j_zz=1.0, hx=0.5, hz=0.2)
        h_sparse = build_sparse_hamiltonian(model)

        plus = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
        init_sites = [plus] * 8
        psi0, _ = build_initial_product_state(init_sites)

        times = np.linspace(0.0, 0.15, 7)
        exact_states = evolve_exact_krylov(h_sparse, psi0, times)
        mf_traj = solve_mean_field_trajectory(model, init_sites, times)

        g_dist = compute_graph_distance_table(list(range(8)), bonds)
        obs_supp = ObservableSupport(sites=(0,), operator_norm=1.0)
        v_lr = 2.0
        mu = 1.0

        # Observable O = Z_0
        obs_z0 = build_full_pauli_operator({0: SIGMA_Z}, 8)

        # First verify spatial decay of influence weights
        # Bond (0, 1) is adjacent (dist 0 or 1 to site 0)
        w_near = compute_influence_weight(
            observable_support=obs_supp,
            edge=(0, 1),
            elapsed_time=0.05,
            velocity=v_lr,
            decay_rate=mu,
            observable_norm=1.0,
            edge_norm=1.0,
            graph_distances=g_dist,
        )
        # Bond (6, 7) is on the far hexagon (dist 3 from site 0)
        w_far = compute_influence_weight(
            observable_support=obs_supp,
            edge=(6, 7),
            elapsed_time=0.05,
            velocity=v_lr,
            decay_rate=mu,
            observable_norm=1.0,
            edge_norm=1.0,
            graph_distances=g_dist,
        )
        assert w_far < w_near, f"Distant weight {w_far} must be strictly less than near weight {w_near}"

        # Verify enclosure for all time steps
        dt = times[1] - times[0]
        cumulative_weighted_bound = 0.0

        for step in range(len(times)):
            t = times[step]
            psi_t = exact_states[step]
            exp_exact = float(np.real(psi_t.conj() @ (obs_z0 @ psi_t)))

            u_sites = mf_traj[step]
            exp_mf = float(np.real(u_sites[0].conj() @ (SIGMA_Z @ u_sites[0])))
            actual_error = abs(exp_exact - exp_mf)

            # Evaluate Duhamel integral with spatial weights
            integral = 0.0
            if step > 0:
                for s_idx in range(step + 1):
                    s = times[s_idx]
                    defects = compute_edge_normal_defects(model, mf_traj[s_idx])
                    weight_s = 0.5 if (s_idx == 0 or s_idx == step) else 1.0

                    for b_idx, bond in enumerate(bonds):
                        w_e = compute_influence_weight(
                            observable_support=obs_supp,
                            edge=bond,
                            elapsed_time=t - s,
                            velocity=v_lr,
                            decay_rate=mu,
                            observable_norm=1.0,
                            edge_norm=1.0,
                            graph_distances=g_dist,
                        )
                        integral += dt * weight_s * w_e * defects[b_idx]

            assert actual_error <= integral + 1e-12, (
                f"At t={t:.3f}, actual error {actual_error:.6e} exceeds weighted Duhamel bound {integral:.6e}"
            )
