"""Unit and Integration Tests: CT-AUX Rank-1 Fast Determinant and Inverse Updates.
AuthorityEffect: None.

Tests:
1. Birth Schur complement ratio and bordered block inverse exactness (O(k^2)).
2. Death diagonal ratio and outer product inverse exactness (O(1) ratio, O(k^2) inverse).
3. Spin-flip Sherman-Morrison ratio and rank-1 inverse exactness (O(k) ratio, O(k^2) inverse).
4. Fast Markov chain sampler trajectory stability and norm boundedness.
5. Exact parity between fast incremental updates and full scratch LU recomputations.
6. Empirical wall-clock benchmark confirming O(k^2) vs O(k^3) speedup for k >= 20.
"""

from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import numpy as np
import pytest

code_dir = Path(__file__).resolve().parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.ct_aux_streaming_gin_engine import (
    CtAuxConfiguration,
    CtAuxMarkovChainSampler,
    CtAuxVertex,
)


def _setup_test_sampler() -> CtAuxMarkovChainSampler:
    """Helper creating a standard 4-site Hubbard sampler."""
    return CtAuxMarkovChainSampler(
        num_sites=4,
        t_hopping=1.0,
        u_interaction=2.0,
        beta=1.0,
        k_shift=2.0,
        seed=12345,
    )


def test_birth_schur_complement_ratio_and_inverse_exactness():
    """Validates that O(k^2) Schur complement ratio and block inverse exactly match full LU."""
    sampler = _setup_test_sampler()

    initial_vertices = [
        CtAuxVertex(site=1, tau=0.2, spin=1),
        CtAuxVertex(site=2, tau=0.5, spin=-1),
        CtAuxVertex(site=3, tau=0.8, spin=1),
    ]
    sampler.current_vertices = list(initial_vertices)
    sampler.recompute_inverses_from_scratch()

    k = len(sampler.current_vertices)
    assert k == 3

    new_v = CtAuxVertex(site=4, tau=0.4, spin=-1)

    N_up_old, N_down_old = sampler.build_N_matrices(sampler.current_vertices)
    cand_vertices = list(sampler.current_vertices) + [new_v]
    N_up_new, N_down_new = sampler.build_N_matrices(cand_vertices)

    det_up_old = np.linalg.det(N_up_old)
    det_up_new = np.linalg.det(N_up_new)
    true_ratio_up = det_up_new / det_up_old

    det_down_old = np.linalg.det(N_down_old)
    det_down_new = np.linalg.det(N_down_new)
    true_ratio_down = det_down_new / det_down_old

    taus_exist = np.array([v.tau for v in sampler.current_vertices], dtype=float)
    sites_exist = np.array([v.site for v in sampler.current_vertices], dtype=int)
    spins_exist = np.array([v.spin for v in sampler.current_vertices], dtype=float)

    tau_diff_to_new = taus_exist - new_v.tau
    g0_to_new = np.array(
        [sampler.g0(s_i, new_v.site, t_diff) for s_i, t_diff in zip(sites_exist, tau_diff_to_new)]
    )
    tau_diff_from_new = new_v.tau - taus_exist
    g0_from_new = np.array(
        [sampler.g0(new_v.site, s_i, t_diff) for s_i, t_diff in zip(sites_exist, tau_diff_from_new)]
    )
    g0_diag = sampler.g0(new_v.site, new_v.site, 0.0)

    e_up_exist = np.exp(sampler.gamma * spins_exist)
    e_up_new = math.exp(sampler.gamma * new_v.spin)
    u_up = -(e_up_exist - 1.0) * g0_to_new
    v_up = -(e_up_new - 1.0) * g0_from_new
    d_up = e_up_new - (e_up_new - 1.0) * g0_diag

    u_tilde_up = sampler.M_up @ u_up
    v_tilde_up = v_up @ sampler.M_up
    S_up = d_up - float(v_up @ u_tilde_up)

    e_down_exist = np.exp(-sampler.gamma * spins_exist)
    e_down_new = math.exp(-sampler.gamma * new_v.spin)
    u_down = -(e_down_exist - 1.0) * g0_to_new
    v_down = -(e_down_new - 1.0) * g0_from_new
    d_down = e_down_new - (e_down_new - 1.0) * g0_diag

    u_tilde_down = sampler.M_down @ u_down
    v_tilde_down = v_down @ sampler.M_down
    S_down = d_down - float(v_down @ u_tilde_down)

    assert abs(S_up - true_ratio_up) < 1e-11
    assert abs(S_down - true_ratio_down) < 1e-11

    M_up_fast = np.empty((k + 1, k + 1), dtype=float)
    inv_S_up = 1.0 / S_up
    M_up_fast[:k, :k] = sampler.M_up + inv_S_up * np.outer(u_tilde_up, v_tilde_up)
    M_up_fast[:k, k] = -inv_S_up * u_tilde_up
    M_up_fast[k, :k] = -inv_S_up * v_tilde_up
    M_up_fast[k, k] = inv_S_up

    res_up = np.max(np.abs(M_up_fast @ N_up_new - np.eye(k + 1)))
    inv_diff_up = np.max(np.abs(M_up_fast - np.linalg.inv(N_up_new)))
    assert res_up < 1e-11
    assert inv_diff_up < 1e-11

    M_down_fast = np.empty((k + 1, k + 1), dtype=float)
    inv_S_down = 1.0 / S_down
    M_down_fast[:k, :k] = sampler.M_down + inv_S_down * np.outer(u_tilde_down, v_tilde_down)
    M_down_fast[:k, k] = -inv_S_down * u_tilde_down
    M_down_fast[k, :k] = -inv_S_down * v_tilde_down
    M_down_fast[k, k] = inv_S_down

    res_down = np.max(np.abs(M_down_fast @ N_down_new - np.eye(k + 1)))
    inv_diff_down = np.max(np.abs(M_down_fast - np.linalg.inv(N_down_new)))
    assert res_down < 1e-11
    assert inv_diff_down < 1e-11


def test_death_diagonal_ratio_and_inverse_exactness():
    """Validates that O(1) diagonal ratio and O(k^2) inverse reduction exactly match full LU."""
    sampler = _setup_test_sampler()

    initial_vertices = [
        CtAuxVertex(site=1, tau=0.1, spin=1),
        CtAuxVertex(site=2, tau=0.3, spin=-1),
        CtAuxVertex(site=3, tau=0.6, spin=1),
        CtAuxVertex(site=4, tau=0.9, spin=-1),
    ]
    sampler.current_vertices = list(initial_vertices)
    sampler.recompute_inverses_from_scratch()
    k = len(sampler.current_vertices)
    assert k == 4

    N_up, N_down = sampler.build_N_matrices(sampler.current_vertices)
    det_up = np.linalg.det(N_up)
    det_down = np.linalg.det(N_down)

    for p in range(k):
        rem_vertices = [v for i, v in enumerate(sampler.current_vertices) if i != p]
        N_up_rem, N_down_rem = sampler.build_N_matrices(rem_vertices)

        true_ratio_up = np.linalg.det(N_up_rem) / det_up
        true_ratio_down = np.linalg.det(N_down_rem) / det_down

        ratio_up_fast = sampler.M_up[p, p]
        ratio_down_fast = sampler.M_down[p, p]

        assert abs(ratio_up_fast - true_ratio_up) < 1e-11
        assert abs(ratio_down_fast - true_ratio_down) < 1e-11

        idx = [i for i in range(k) if i != p]
        M_up_fast = sampler.M_up[np.ix_(idx, idx)] - (1.0 / ratio_up_fast) * np.outer(
            sampler.M_up[idx, p], sampler.M_up[p, idx]
        )
        M_down_fast = sampler.M_down[np.ix_(idx, idx)] - (1.0 / ratio_down_fast) * np.outer(
            sampler.M_down[idx, p], sampler.M_down[p, idx]
        )

        res_up = np.max(np.abs(M_up_fast @ N_up_rem - np.eye(k - 1)))
        inv_diff_up = np.max(np.abs(M_up_fast - np.linalg.inv(N_up_rem)))
        assert res_up < 1e-11
        assert inv_diff_up < 1e-11

        res_down = np.max(np.abs(M_down_fast @ N_down_rem - np.eye(k - 1)))
        inv_diff_down = np.max(np.abs(M_down_fast - np.linalg.inv(N_down_rem)))
        assert res_down < 1e-11
        assert inv_diff_down < 1e-11


def test_spin_flip_sherman_morrison_exactness():
    """Validates that O(k) Sherman-Morrison ratio and O(k^2) rank-1 update match full LU."""
    sampler = _setup_test_sampler()

    initial_vertices = [
        CtAuxVertex(site=1, tau=0.15, spin=1),
        CtAuxVertex(site=2, tau=0.45, spin=1),
        CtAuxVertex(site=3, tau=0.75, spin=-1),
    ]
    sampler.current_vertices = list(initial_vertices)
    sampler.recompute_inverses_from_scratch()
    k = len(sampler.current_vertices)

    N_up_old, N_down_old = sampler.build_N_matrices(sampler.current_vertices)
    det_up_old = np.linalg.det(N_up_old)
    det_down_old = np.linalg.det(N_down_old)

    for p in range(k):
        v_old = sampler.current_vertices[p]
        new_spin = -v_old.spin

        flipped_vertices = [
            CtAuxVertex(site=v.site, tau=v.tau, spin=new_spin if i == p else v.spin)
            for i, v in enumerate(sampler.current_vertices)
        ]
        N_up_new, N_down_new = sampler.build_N_matrices(flipped_vertices)

        true_ratio_up = np.linalg.det(N_up_new) / det_up_old
        true_ratio_down = np.linalg.det(N_down_new) / det_down_old

        sites = np.array([v.site for v in sampler.current_vertices], dtype=int)
        taus = np.array([v.tau for v in sampler.current_vertices], dtype=float)
        g0_row = np.array([sampler.g0(v_old.site, s, v_old.tau - t) for s, t in zip(sites, taus)])

        delta_e_up = math.exp(sampler.gamma * new_spin) - math.exp(sampler.gamma * v_old.spin)
        delta_r_up = -delta_e_up * g0_row
        delta_r_up[p] += delta_e_up

        delta_e_down = math.exp(-sampler.gamma * new_spin) - math.exp(-sampler.gamma * v_old.spin)
        delta_r_down = -delta_e_down * g0_row
        delta_r_down[p] += delta_e_down

        lambda_up = 1.0 + float(delta_r_up @ sampler.M_up[:, p])
        lambda_down = 1.0 + float(delta_r_down @ sampler.M_down[:, p])

        assert abs(lambda_up - true_ratio_up) < 1e-11
        assert abs(lambda_down - true_ratio_down) < 1e-11

        w_up = delta_r_up @ sampler.M_up
        M_up_fast = sampler.M_up - (1.0 / lambda_up) * np.outer(sampler.M_up[:, p], w_up)

        w_down = delta_r_down @ sampler.M_down
        M_down_fast = sampler.M_down - (1.0 / lambda_down) * np.outer(sampler.M_down[:, p], w_down)

        res_up = np.max(np.abs(M_up_fast @ N_up_new - np.eye(k)))
        inv_diff_up = np.max(np.abs(M_up_fast - np.linalg.inv(N_up_new)))
        assert res_up < 1e-11
        assert inv_diff_up < 1e-11

        res_down = np.max(np.abs(M_down_fast @ N_down_new - np.eye(k)))
        inv_diff_down = np.max(np.abs(M_down_fast - np.linalg.inv(N_down_new)))
        assert res_down < 1e-11
        assert inv_diff_down < 1e-11


def test_fast_sampler_mcmc_trajectory_and_refresh_stability():
    """Runs 500 fast MCMC steps and asserts strict inverse residual boundedness."""
    sampler = _setup_test_sampler()
    sampler.refresh_interval = 50

    accepted_count = 0
    for step_i in range(500):
        accepted, cfg = sampler.step(fast=True)
        if accepted:
            accepted_count += 1
            k = len(sampler.current_vertices)
            if k > 0:
                N_up, N_down = sampler.build_N_matrices(sampler.current_vertices)
                res_up = np.max(np.abs(sampler.M_up @ N_up - np.eye(k)))
                res_down = np.max(np.abs(sampler.M_down @ N_down - np.eye(k)))
                assert res_up < 1e-9
                assert res_down < 1e-9

    assert accepted_count > 50
    assert sampler.step_count == accepted_count


def test_speedup_benchmark_scaling():
    """Empirically validates that O(k^2) fast updates outperform full O(k^3) inversion at k >= 40."""
    sampler = _setup_test_sampler()

    k = 40
    vertices = [
        CtAuxVertex(
            site=(i % 4) + 1,
            tau=(0.02 * i) % 1.0,
            spin=1 if i % 2 == 0 else -1,
        )
        for i in range(k)
    ]
    sampler.current_vertices = list(vertices)
    sampler.recompute_inverses_from_scratch()

    new_v = CtAuxVertex(site=2, tau=0.55, spin=1)
    cand = list(vertices) + [new_v]
    N_up, N_down = sampler.build_N_matrices(cand)

    num_reps = 300
    t0 = time.perf_counter()
    for _ in range(num_reps):
        _ = np.linalg.slogdet(N_up)
        _ = np.linalg.slogdet(N_down)
        _ = np.linalg.inv(N_up)
        _ = np.linalg.inv(N_down)
    t_full = time.perf_counter() - t0

    u_up = np.random.randn(k)
    v_up = np.random.randn(k)
    d_up = 1.45

    t0 = time.perf_counter()
    for _ in range(num_reps):
        u_tilde = sampler.M_up @ u_up
        v_tilde = v_up @ sampler.M_up
        S = d_up - float(v_up @ u_tilde)
        inv_S = 1.0 / S

        M_new = np.empty((k + 1, k + 1), dtype=float)
        M_new[:k, :k] = sampler.M_up + inv_S * np.outer(u_tilde, v_tilde)
        M_new[:k, k] = -inv_S * u_tilde
        M_new[k, :k] = -inv_S * v_tilde
        M_new[k, k] = inv_S
    t_fast = time.perf_counter() - t0

    speedup = t_full / t_fast
    assert speedup > 2.0, f"Expected speedup > 2.0x at k=40, observed {speedup:.2f}x"

