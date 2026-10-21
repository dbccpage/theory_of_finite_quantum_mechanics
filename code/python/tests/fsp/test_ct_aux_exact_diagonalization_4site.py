"""Unit and Integration Tests: CT-AUX Monte Carlo vs Exact Diagonalization Cross-Validation on 4-Site Hubbard Clusters.

AuthorityEffect: None.
Claim Hygiene:
1. What this supports:
   - Numerical cross-validation of CT-AUX continuous-time auxiliary-field Monte Carlo trajectories
     against exact diagonalization on 4-site Hubbard clusters (bipartite square plaquette / ring).
   - Exact agreement between non-interacting Green's function g0(tau) and matrix exponential of tight-binding H0.
   - Numerical agreement between CT-AUX mean expansion order <k> and exact grand-canonical expectation.
   - Absence of fermion sign problem (average sign = 1.0) on bipartite 4-site cluster at half-filling.
   - Matrix inverse accuracy and log-determinant drift bounded to machine precision.
2. What this does not support:
   - Thermodynamic limit (N -> inf), continuous spacetime quantum field theory, or general solution to NP-hard sign problems.
3. Narrowest defensible claim:
   - On the declared 4-site cluster, CT-AUX Monte Carlo trajectories reproduce exact spectral observables
     within declared finite statistical and numerical error envelopes.
4. Next test needed:
   - Extend cross-validation to 8-site and 16-site bipartite clusters under multi-orbital hybridization.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from fractions import Fraction
from typing import Dict, List, Tuple

import numpy as np
import pytest
import scipy.linalg

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.ct_aux_streaming_gin_engine import (
    CtAuxConfiguration,
    CtAuxMarkovChainSampler,
    CtAuxVertex,
    StreamingGinPostingIndex,
    StreamingSignRecoveryReceipt,
    run_streaming_ct_aux_simulation,
)
from src.fsp.fermionic_hamiltonian import (
    DiscreteFermionicHamiltonian,
    FermionicLattice,
    FockState,
)


def _build_grand_canonical_4site_hamiltonian(
    t: float = 1.0,
    u: float = 2.0,
    mu: float = 0.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Constructs the exact 2^8 = 256 dimensional grand canonical Hamiltonian for 4-site ring.
    
    Returns (H, evals, evecs).
    """
    num_sites = 4
    dim = 256
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    H = np.zeros((dim, dim), dtype=float)

    def get_bit(mask: int, site: int) -> int:
        return (mask >> site) & 1

    def count_ones_between(mask: int, s1: int, s2: int) -> int:
        low, high = min(s1, s2), max(s1, s2)
        return sum((mask >> s) & 1 for s in range(low + 1, high))

    for idx in range(dim):
        up = idx & 15
        down = (idx >> 4) & 15

        # On-site interaction in CT-AUX particle-hole symmetric form:
        # U sum_i (n_{i up} - 1/2)(n_{i down} - 1/2) - mu sum_i (n_{i up} + n_{i down})
        diag = 0.0
        for i in range(num_sites):
            n_up_i = get_bit(up, i)
            n_dn_i = get_bit(down, i)
            diag += u * (n_up_i - 0.5) * (n_dn_i - 0.5) - mu * (n_up_i + n_dn_i)
        H[idx, idx] += diag

        # Nearest-neighbor hopping
        for u_s, v_s in edges:
            for src, dst in [(u_s, v_s), (v_s, u_s)]:
                # Spin up
                if get_bit(up, src) and not get_bit(up, dst):
                    phase = -1.0 if (count_ones_between(up, src, dst) % 2 == 1) else 1.0
                    new_up = (up ^ (1 << src)) | (1 << dst)
                    new_idx = new_up | (down << 4)
                    H[new_idx, idx] += -t * phase
                # Spin down
                if get_bit(down, src) and not get_bit(down, dst):
                    phase = -1.0 if (count_ones_between(down, src, dst) % 2 == 1) else 1.0
                    new_dn = (down ^ (1 << src)) | (1 << dst)
                    new_idx = up | (new_dn << 4)
                    H[new_idx, idx] += -t * phase

    evals, evecs = np.linalg.eigh(H)
    return H, evals, evecs


# ==============================================================================
# 1. Non-interacting Green's Function vs Matrix Exponential
# ==============================================================================

def test_bare_greens_function_matches_matrix_exponential():
    """Cross-validates sampler.g0 against exact matrix exponential exp(-tau H0) inv(I + exp(-beta H0))."""
    num_sites = 4
    t = 1.0
    u = 2.0
    mu = 0.25
    beta = 1.5

    sampler = CtAuxMarkovChainSampler(
        num_sites=num_sites,
        t_hopping=t,
        u_interaction=u,
        mu_chemical_potential=mu,
        beta=beta,
        seed=101,
    )

    # Tight-binding H0 matrix
    H0 = np.zeros((num_sites, num_sites), dtype=float)
    for i in range(num_sites):
        j = (i + 1) % num_sites
        H0[i, j] -= t
        H0[j, i] -= t
        H0[i, i] -= mu

    exp_beta_H0 = scipy.linalg.expm(-beta * H0)
    inv_fermi = np.linalg.inv(np.eye(num_sites) + exp_beta_H0)

    # Evaluate across a grid of tau in (0, beta)
    tau_grid = [0.05, 0.2, 0.5, 0.75, 1.0, 1.3, 1.45]
    for tau in tau_grid:
        G0_exact = scipy.linalg.expm(-tau * H0) @ inv_fermi
        for x in range(1, num_sites + 1):
            for y in range(1, num_sites + 1):
                g0_val = sampler.g0(x, y, tau)
                exact_val = G0_exact[x - 1, y - 1]
                assert abs(g0_val - exact_val) < 1e-13, (
                    f"Discrepancy at ({x}, {y}, tau={tau}): sampler={g0_val}, exact={exact_val}"
                )


def test_bare_greens_function_antiperiodicity_and_symmetry():
    """Verifies KMS anti-periodicity G0(tau + beta) = -G0(tau) and particle-hole symmetry at mu=0."""
    num_sites = 4
    sampler = CtAuxMarkovChainSampler(
        num_sites=num_sites,
        t_hopping=1.0,
        u_interaction=2.0,
        mu_chemical_potential=0.0,
        beta=2.0,
        seed=202,
    )

    # Antiperiodicity
    for tau in [0.1, 0.5, 1.2, 1.8]:
        g_pos = sampler.g0(1, 2, tau)
        g_neg = sampler.g0(1, 2, tau - sampler.beta)
        assert abs(g_pos + g_neg) < 1e-14, f"Antiperiodicity failed at tau={tau}"

    # Particle-hole symmetry at half filling (mu=0):
    # Under particle-hole conjugation at half-filling, G0(x, x, tau) = G0(x, x, beta - tau)
    for tau in [0.2, 0.7, 1.0, 1.6]:
        g1 = sampler.g0(1, 1, tau)
        g2 = sampler.g0(1, 1, sampler.beta - tau)
        assert abs(g1 - g2) < 1e-13, f"Particle-hole symmetry failed at tau={tau}: g1={g1}, g2={g2}"

    # Equal-time occupancy at half filling is 0.5
    assert abs(sampler.g0(1, 1, 0.0) - 0.5) < 1e-14


# ==============================================================================
# 2. Exact Diagonalization via DiscreteFermionicHamiltonian
# ==============================================================================

def test_canonical_4site_exact_diagonalization():
    """Cross-validates 4-site cluster using DiscreteFermionicHamiltonian in (2, 2) sector."""
    lat = FermionicLattice.square_plaquette()
    assert lat.num_sites == 4
    assert len(lat.edges) == 4

    ham = DiscreteFermionicHamiltonian(
        lattice=lat,
        t=1.0,
        u=2.0,
        num_up=2,
        num_down=2,
    )
    # Dimension is comb(4, 2) * comb(4, 2) = 6 * 6 = 36
    assert ham.dim == 36

    # Verify thermal trace is strictly positive
    z_exact = ham.compute_exact_thermal_trace(beta=1.0)
    assert z_exact > 0.0

    # Verify Trotterized path partition functions and average sign
    res = ham.compute_partition_functions(beta=1.0, trotter_steps=6)
    assert res["z_fermionic"] > 0.0
    assert res["z_bosonic"] > 0.0
    # In finite Trotter Euler transfer matrix representation, sign is positive (> 0.85)
    assert res["average_sign"] > 0.85


def test_frustrated_vs_bipartite_sign_problem_contrast():
    """Confirms that bipartite 4-site cluster retains high average sign while frustrated 3-site triangle decays."""
    # Bipartite 4-site
    lat_bipartite = FermionicLattice.square_plaquette()
    ham_bipartite = DiscreteFermionicHamiltonian(
        lattice=lat_bipartite, t=1.0, u=4.0, num_up=2, num_down=2
    )
    res_bipartite = ham_bipartite.compute_partition_functions(beta=1.0, trotter_steps=4)
    assert res_bipartite["average_sign"] > 0.90

    # Frustrated 3-site triangle
    lat_triangle = FermionicLattice.triangle_cluster()
    ham_triangle = DiscreteFermionicHamiltonian(
        lattice=lat_triangle, t=1.0, u=4.0, num_up=2, num_down=1
    )
    res_triangle = ham_triangle.compute_partition_functions(beta=1.0, trotter_steps=4)
    # Sign drops significantly due to geometric frustration
    assert res_triangle["average_sign"] < res_bipartite["average_sign"]


# ==============================================================================
# 3. CT-AUX Monte Carlo Trajectory Cross-Validation
# ==============================================================================

def test_ct_aux_trajectory_all_positive_signs_on_4site_bipartite():
    """Cross-validates that CT-AUX sampling on 4-site bipartite cluster at half filling has strictly sign +1."""
    sampler = CtAuxMarkovChainSampler(
        num_sites=4,
        t_hopping=1.0,
        u_interaction=2.0,
        mu_chemical_potential=0.0,
        beta=1.0,
        k_shift=2.0,
        seed=303,
    )

    signs = []
    orders = []
    for _ in range(2500):
        accepted, cfg = sampler.step(fast=True)
        if accepted and cfg is not None:
            signs.append(cfg.sign)
            orders.append(cfg.order)

    assert len(signs) > 1000, "Sufficient moves accepted"
    # 100% of configurations must have sign +1
    assert set(signs) == {1}
    assert np.mean(signs) == 1.0
    assert np.mean(orders) > 1.5


def test_fast_rank1_vs_full_determinant_trajectory_parity():
    """Asserts log-determinant drift < 1e-13 and inverse residual < 1e-13 over 1,000 MCMC trajectory steps."""
    sampler = CtAuxMarkovChainSampler(
        num_sites=4,
        t_hopping=1.0,
        u_interaction=2.0,
        mu_chemical_potential=0.0,
        beta=1.0,
        k_shift=2.0,
        seed=404,
    )

    max_det_error = 0.0
    max_inv_error = 0.0

    for step in range(1200):
        accepted, cfg = sampler.step(fast=True)
        if accepted and cfg is not None and len(sampler.current_vertices) > 0:
            k = len(sampler.current_vertices)

            # Compare cached fast log-determinant with full direct slogdet
            full_log_up, full_log_down, full_sign = sampler.compute_log_determinants(sampler.current_vertices)
            err_up = abs(sampler.current_logdet_up - full_log_up)
            err_down = abs(sampler.current_logdet_down - full_log_down)
            max_det_error = max(max_det_error, err_up, err_down)
            assert sampler.current_sign == full_sign

            # Check exact inverse condition M @ N = I
            N_up, N_down = sampler.build_N_matrices(sampler.current_vertices)
            res_up = np.max(np.abs(sampler.M_up @ N_up - np.eye(k)))
            res_down = np.max(np.abs(sampler.M_down @ N_down - np.eye(k)))
            max_inv_error = max(max_inv_error, res_up, res_down)

    assert max_det_error < 1e-13, f"Max det drift too high: {max_det_error}"
    assert max_inv_error < 1e-13, f"Max inverse error too high: {max_inv_error}"


def test_ct_aux_mean_order_cross_validation_with_exact_diagonalization():
    """Cross-validates the CT-AUX mean expansion order <k> against the exact grand-canonical expectation.
    
    Formula: <k>_exact = K - beta * U * <sum_i (n_{i up} - 1/2)(n_{i down} - 1/2)>_exact.
    """
    t = 1.0
    u = 2.0
    mu = 0.0
    beta = 1.0
    k_shift = 2.0

    # 1. Exact Grand Canonical Diagonalization
    dim = 256
    H, evals, evecs = _build_grand_canonical_4site_hamiltonian(t=t, u=u, mu=mu)
    Z = np.sum(np.exp(-beta * evals))
    weights = np.exp(-beta * evals) / Z

    def get_bit(mask: int, site: int) -> int:
        return (mask >> site) & 1

    int_term = np.zeros(dim)
    for idx in range(dim):
        up = idx & 15
        down = (idx >> 4) & 15
        int_term[idx] = sum(
            (get_bit(up, i) - 0.5) * (get_bit(down, i) - 0.5) for i in range(4)
        )

    exact_int_expectation = 0.0
    for m in range(dim):
        diag_elem = np.sum(evecs[:, m] ** 2 * int_term)
        exact_int_expectation += weights[m] * diag_elem

    exact_expected_k = k_shift - beta * u * exact_int_expectation
    assert math.isclose(exact_expected_k, 2.60917, rel_tol=1e-3)

    # 2. CT-AUX Monte Carlo Measurement
    sampler = CtAuxMarkovChainSampler(
        num_sites=4,
        t_hopping=t,
        u_interaction=u,
        mu_chemical_potential=mu,
        beta=beta,
        k_shift=k_shift,
        seed=505,
    )

    # Thermalize
    for _ in range(2000):
        sampler.step(fast=True)

    # Sample trajectory
    measured_orders = []
    for _ in range(15000):
        sampler.step(fast=True)
        measured_orders.append(len(sampler.current_vertices))

    mean_k = float(np.mean(measured_orders))

    # Cross-validation: agreement within declared finite envelope
    assert 2.0 < mean_k < 3.2, f"MCMC mean <k>={mean_k:.4f} outside physical regime"
    assert abs(mean_k - exact_expected_k) < 0.25, (
        f"MCMC mean <k>={mean_k:.4f} differs from exact {exact_expected_k:.4f} by more than envelope"
    )


# ==============================================================================
# 4. Streaming GIN Indexing & Invariant Receipt
# ==============================================================================

def test_streaming_gin_indexing_receipt_on_4site_simulation():
    """Runs a complete CT-AUX trajectory coupled to live streaming GIN and validates the receipt."""
    receipt, perf = run_streaming_ct_aux_simulation(
        num_steps=1500,
        window_size=250,
        num_sites=4,
        t_hop=1.0,
        u_int=2.0,
        mu=0.0,
        beta=1.0,
        k_shift=2.0,
        seed=606,
    )

    assert receipt.total_steps == 1500
    assert receipt.memory_bounded is True
    assert receipt.current_window_size <= receipt.max_window_capacity
    assert receipt.raw_negative_count == 0
    assert receipt.raw_positive_count > 0
    assert receipt.raw_average_sign == 1.0
    assert receipt.quotiented_average_sign == 1.0
    assert receipt.max_cancellation_defect == 0.0
    assert receipt.status == "STREAMING_INDEX_CERTIFIED"

    assert perf["total_configs_accepted"] > 500
    assert perf["mean_insert_us"] > 0.0


# ==============================================================================
# 5. Negative and Boundary Control Tests
# ==============================================================================

def test_adversarial_negative_controls():
    """Verifies that non-physical parameters and invalid inputs are refused fail-closed."""
    # Invalid num_sites
    with pytest.raises(ValueError):
        FermionicLattice(num_sites=0, edges=[])

    with pytest.raises(ValueError):
        FermionicLattice(num_sites=33, edges=[])

    # Boolean rejection
    with pytest.raises(ValueError):
        FermionicLattice(num_sites=True, edges=[])

    # Negative couplings
    lat = FermionicLattice.square_plaquette()
    with pytest.raises(ValueError):
        DiscreteFermionicHamiltonian(lattice=lat, num_up=0, num_down=0)

    with pytest.raises(TypeError):
        DiscreteFermionicHamiltonian(lattice=lat, num_up=True, num_down=1)

    # Infinite beta in thermal trace
    ham = DiscreteFermionicHamiltonian(lattice=lat, num_up=1, num_down=1)
    with pytest.raises(ValueError):
        ham.compute_exact_thermal_trace(beta=float("inf"))

    with pytest.raises(ValueError):
        ham.compute_partition_functions(beta=0.0)
