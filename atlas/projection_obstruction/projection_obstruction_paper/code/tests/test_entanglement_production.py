"""Finite NumPy examples of short-time entropy and product-tangent formulas.

AuthorityEffect: None. Numerical checks cover the supplied fixtures only.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
from scipy.linalg import expm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from entanglement_production import (
    compute_edge_excitation_vector,
    compute_edge_normal_rate,
    lindblad_dissipator,
    linear_entropy,
    partial_trace_bipartite,
    renyi_entropy,
    two_qubit_concurrence,
    verify_lindblad_local_immunity,
)


def test_two_qubit_tfim_linear_entropy_and_concurrence_rates():
    """Verify that S_L(rho_1(t)) = 1/2 * nu_e^2 * t^2 + O(t^4) and C(t) = nu_e * t + O(t^3) for TFIM."""
    j_val = 1.3
    h_val = 0.7
    omega_val = 0.5  # Transverse field (one-local term)

    sigma_x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    eye2 = np.eye(2, dtype=np.complex128)

    h_two_body = j_val * np.kron(sigma_x, sigma_x)
    h_total = (
        h_two_body
        + h_val * (np.kron(sigma_z, eye2) + np.kron(eye2, sigma_z))
        + omega_val * np.kron(sigma_x, eye2)
    )

    u_0 = np.array([1.0, 0.0], dtype=np.complex128)
    psi_0 = np.kron(u_0, u_0)

    nu_e = compute_edge_normal_rate(u_0, u_0, h_two_body)
    assert np.isclose(nu_e, 2.0 * abs(j_val))

    evals, evecs = np.linalg.eigh(h_total)

    t_values = [0.001, 0.002, 0.005, 0.01]
    for t in t_values:
        u_t = evecs @ np.diag(np.exp(-1j * evals * t)) @ evecs.conj().T
        psi_t = u_t @ psi_0
        rho_t = np.outer(psi_t, psi_t.conj())

        rho_1 = partial_trace_bipartite(rho_t, 2, 2, keep="a")
        s_l = linear_entropy(rho_1)
        s_2 = renyi_entropy(rho_1, alpha=2.0)

        s_l_leading = 0.5 * (nu_e**2) * (t**2)
        rel_error = abs(s_l - s_l_leading) / s_l_leading
        assert rel_error < 0.05
        # Rényi-2 entropy agrees to O(t^4)
        assert abs(s_2 - s_l_leading) / s_l_leading < 0.05

        c_val = two_qubit_concurrence(rho_t)
        c_leading = nu_e * t
        c_rel_error = abs(c_val - c_leading) / c_leading
        assert c_rel_error < 0.05


def test_three_qubit_chain_boundary_area_law_and_internal_invariance():
    """Verify that internal interactions do not contribute to subsystem linear entropy at O(t^2)."""
    j12 = 1.7
    j23 = 0.9

    sigma_x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    eye2 = np.eye(2, dtype=np.complex128)

    h12 = j12 * np.kron(np.kron(sigma_x, sigma_x), eye2)
    h23 = j23 * np.kron(np.kron(eye2, sigma_x), sigma_x)
    h_total = h12 + h23

    u_0 = np.array([1.0, 0.0], dtype=np.complex128)
    psi_0 = np.kron(np.kron(u_0, u_0), u_0)

    nu_23 = compute_edge_normal_rate(u_0, u_0, j23 * np.kron(sigma_x, sigma_x))
    assert np.isclose(nu_23, 2.0 * abs(j23))

    evals, evecs = np.linalg.eigh(h_total)

    t_values = [0.001, 0.002, 0.005]
    for t in t_values:
        u_t = evecs @ np.diag(np.exp(-1j * evals * t)) @ evecs.conj().T
        psi_t = u_t @ psi_0
        rho_t = np.outer(psi_t, psi_t.conj())

        rho_12 = partial_trace_bipartite(rho_t, 4, 2, keep="a")
        s_l_12 = linear_entropy(rho_12)

        s_l_expected = 0.5 * (nu_23**2) * (t**2)
        rel_error = abs(s_l_12 - s_l_expected) / s_l_expected
        assert rel_error < 0.02


def test_2d_grid_subsystem_area_law_and_internal_cancellations():
    """Verify Area Law on 2x2 grid with internal couplings J_A, J_B and boundary J_1, J_2."""
    j_a = 2.1
    j_b = 1.9
    j_1 = 1.2
    j_2 = 1.5

    h_fields = [0.8, 0.6, 0.7, 0.9]

    sx = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    eye2 = np.eye(2, dtype=np.complex128)

    def embed_two_site(op: np.ndarray, s1: int, s2: int) -> np.ndarray:
        res = np.zeros((16, 16), dtype=np.complex128)
        for i in range(16):
            b_in = [(i >> (3 - k)) & 1 for k in range(4)]
            for j in range(16):
                b_out = [(j >> (3 - k)) & 1 for k in range(4)]
                if all(b_in[k] == b_out[k] for k in range(4) if k not in (s1, s2)):
                    in_idx = (b_in[s1] << 1) | b_in[s2]
                    out_idx = (b_out[s1] << 1) | b_out[s2]
                    res[i, j] = op[in_idx, out_idx]
        return res

    def embed_one_site(op: np.ndarray, s: int) -> np.ndarray:
        factors = [eye2] * 4
        factors[s] = op
        res = factors[0]
        for k in range(1, 4):
            res = np.kron(res, factors[k])
        return res

    xx = np.kron(sx, sx)
    h_grid = (
        embed_two_site(j_a * xx, 0, 1)
        + embed_two_site(j_b * xx, 2, 3)
        + embed_two_site(j_1 * xx, 0, 2)
        + embed_two_site(j_2 * xx, 1, 3)
    )
    for s in range(4):
        h_grid += embed_one_site(h_fields[s] * sx, s)

    psi0 = np.zeros(16, dtype=np.complex128)
    psi0[0] = 1.0

    nu_1 = 2.0 * abs(j_1)
    nu_2 = 2.0 * abs(j_2)
    nu_boundary_sq = nu_1**2 + nu_2**2

    evals, evecs = np.linalg.eigh(h_grid)

    for t in [0.001, 0.002, 0.005]:
        u_t = evecs @ np.diag(np.exp(-1j * evals * t)) @ evecs.conj().T
        psi_t = u_t @ psi0
        rho_t = np.outer(psi_t, psi_t.conj())

        rho_a = np.trace(rho_t.reshape(4, 4, 4, 4), axis1=1, axis2=3)
        s_l = linear_entropy(rho_a)
        s_l_pred = 0.5 * nu_boundary_sq * (t**2)
        rel_err = abs(s_l - s_l_pred) / s_l_pred
        assert rel_err < 0.001  # Matches within 0.1%


def test_qutrit_d3_linear_entropy_production():
    """Check the pure-product boundary coefficient in a finite qutrit example."""
    j = 1.4
    k = 0.8
    h_ab = np.zeros((9, 9), dtype=np.complex128)
    h_ab[4, 0] = h_ab[0, 4] = j  # |11><00| + h.c.
    h_ab[5, 0] = h_ab[0, 5] = k  # |12><00| + h.c.

    h_single_a = np.zeros((3, 3), dtype=np.complex128)
    h_single_a[1, 0] = h_single_a[0, 1] = 0.9
    h_total = h_ab + np.kron(h_single_a, np.eye(3, dtype=np.complex128))

    chi_e_norm_sq = j**2 + k**2
    nu_e = 2.0 * np.sqrt(chi_e_norm_sq)

    evals, evecs = np.linalg.eigh(h_total)
    psi0 = np.zeros(9, dtype=np.complex128)
    psi0[0] = 1.0

    for t in [0.001, 0.002, 0.005]:
        u_t = evecs @ np.diag(np.exp(-1j * evals * t)) @ evecs.conj().T
        psi_t = u_t @ psi0
        rho = np.outer(psi_t, psi_t.conj())

        rho_a = np.trace(rho.reshape(3, 3, 3, 3), axis1=1, axis2=3)
        s_l = linear_entropy(rho_a)
        s_l_pred = 0.5 * (nu_e**2) * (t**2)
        rel_err = abs(s_l - s_l_pred) / s_l_pred
        assert rel_err < 0.001  # Matches within 0.1%


def test_three_qubit_mixed_state_concurrence_in_environment():
    """Check a reduced pair from a globally pure unitary three-qubit example.

    This environment does not model Markovian local Lindblad noise.
    """
    j_ab = 1.6
    j_bc = 1.1

    sx = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    eye2 = np.eye(2, dtype=np.complex128)

    h_total = j_ab * np.kron(np.kron(sx, sx), eye2) + j_bc * np.kron(np.kron(eye2, sx), sx)
    psi0 = np.zeros(8, dtype=np.complex128)
    psi0[0] = 1.0

    nu_ab = 2.0 * abs(j_ab)

    evals, evecs = np.linalg.eigh(h_total)

    for t in [0.001, 0.002, 0.005]:
        u_t = evecs @ np.diag(np.exp(-1j * evals * t)) @ evecs.conj().T
        psi_t = u_t @ psi0
        rho_global = np.outer(psi_t, psi_t.conj())

        # Trace out qubit c (index 2) to get mixed state rho_ab
        rho_ab = np.trace(rho_global.reshape(4, 2, 4, 2), axis1=1, axis2=3)
        c_val = two_qubit_concurrence(rho_ab)
        c_pred = nu_ab * t
        rel_err = abs(c_val - c_pred) / c_pred
        assert rel_err < 0.05  # Within 5% at short times despite mixed state


def test_lindblad_local_dissipator_immunity():
    """Check the tangent projection for sampled local jumps, not concurrence."""
    rng = np.random.default_rng(42)

    for _ in range(5):
        m_a = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        rho_a = m_a @ m_a.conj().T
        rho_a /= np.trace(rho_a)

        m_b = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        rho_b = m_b @ m_b.conj().T
        rho_b /= np.trace(rho_b)

        jump_ops_a = [
            rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2)),
            rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2)),
        ]
        jump_ops_b = [
            rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)),
        ]

        norm_a, norm_b = verify_lindblad_local_immunity(rho_a, rho_b, jump_ops_a, jump_ops_b)

        assert norm_a < 1.0e-12
        assert norm_b < 1.0e-12


@pytest.mark.parametrize("gamma, expected_slope", [(0.0, 2.0), (0.5, 1.0), (2.0, 0.0)])
def test_local_noise_changes_concurrence_despite_zero_normal_projection(gamma, expected_slope):
    """Local raising noise gives C'(0+) = 2 max(0, 1-gamma) for H=XX."""
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    identity = np.eye(2, dtype=complex)
    jump = np.sqrt(gamma) * np.array([[0, 0], [1, 0]], dtype=complex)
    jumps = [np.kron(jump, identity), np.kron(identity, jump)]
    hamiltonian = np.kron(sx, sx)
    u = np.array([1, 0], dtype=complex)
    rho_site = np.outer(u, u.conj())
    projections = verify_lindblad_local_immunity(rho_site, rho_site, [jump], [jump])
    assert max(projections) < 1e-12
    assert compute_edge_normal_rate(u, u, hamiltonian) == pytest.approx(2.0)

    # Independent dense Liouvillian evolution includes first-order local mixing.
    basis = np.eye(16, dtype=complex).reshape(16, 4, 4)
    generator = np.column_stack([
        (-1j * (hamiltonian @ b - b @ hamiltonian) + lindblad_dissipator(b, jumps)).ravel()
        for b in basis
    ])
    rho0 = np.zeros((4, 4), dtype=complex)
    rho0[0, 0] = 1
    for t in (1e-5, 2e-5):
        rho = (expm(t * generator) @ rho0.ravel()).reshape(4, 4)
        assert two_qubit_concurrence(rho) / t == pytest.approx(expected_slope, abs=2e-4)


def test_heisenberg_xxz_orthogonal_excitation_sectors():
    """Verify orthogonal sector summation nu_global^2 = sum_e nu_e^2 for Heisenberg XXZ."""
    j_xy = 1.0
    j_z = 2.0

    sigma_x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=np.complex128)

    h_xxz = j_xy * (np.kron(sigma_x, sigma_x) + np.kron(sigma_y, sigma_y)) + j_z * np.kron(
        sigma_z, sigma_z
    )

    u_0 = np.array([1.0, 0.0], dtype=np.complex128)
    chi_e = compute_edge_excitation_vector(u_0, u_0, h_xxz)

    assert np.allclose(chi_e, 0.0)
    assert compute_edge_normal_rate(u_0, u_0, h_xxz) == 0.0

    u_plus = np.array([1.0, 1.0], dtype=np.complex128) / np.sqrt(2.0)
    chi_e_plus = compute_edge_excitation_vector(u_0, u_plus, h_xxz)
    norm_chi = np.linalg.norm(chi_e_plus)
    assert norm_chi > 0.0
    nu_e = compute_edge_normal_rate(u_0, u_plus, h_xxz)
    assert np.isclose(nu_e, 2.0 * norm_chi)
