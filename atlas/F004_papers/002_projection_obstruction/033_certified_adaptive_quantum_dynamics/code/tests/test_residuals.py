"""Tests for retraction tangent projectors, normal residuals, and Schatten-1 dual witnesses.

AuthorityEffect: None.
"""

import pytest
import numpy as np

from caqd.residuals import (
    retraction_tangent_projector,
    normal_projector,
    compute_edge_residual,
    compute_local_residuals,
    dual_witness_schatten1,
    verify_lemma_5_3_tangent_isolation,
)
from caqd.spin_chains import (
    TFIMChain,
    operator_norm,
    trace_norm,
    partial_trace,
    pauli_matrices,
)


def test_tangent_projector_idempotence():
    """Verify that retraction differential P_e is idempotent: P_e^2 = P_e."""
    # Random single-qubit density matrices
    psi_a = np.array([0.6, 0.8j], dtype=complex)
    rho_a = np.outer(psi_a, psi_a.conj())
    psi_b = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho_b = np.outer(psi_b, psi_b.conj())
    
    # Random 4x4 matrix Z
    np.random.seed(42)
    Z = np.random.randn(4, 4) + 1.0j * np.random.randn(4, 4)
    Z = Z - np.trace(Z) * np.eye(4) / 4.0 # traceless
    
    P_Z = retraction_tangent_projector(rho_a, rho_b, Z)
    P_P_Z = retraction_tangent_projector(rho_a, rho_b, P_Z)
    
    np.testing.assert_allclose(P_P_Z, P_Z, atol=1e-14)


def test_normal_projector_annihilation():
    """Verify that Q_e = I - P_e and Q_e P_e = 0, P_e Q_e = 0."""
    psi_a = np.array([1.0, 0.0], dtype=complex)
    rho_a = np.outer(psi_a, psi_a.conj())
    psi_b = np.array([0.0, 1.0], dtype=complex)
    rho_b = np.outer(psi_b, psi_b.conj())
    
    np.random.seed(43)
    Z = np.random.randn(4, 4) + 1.0j * np.random.randn(4, 4)
    
    P_Z = retraction_tangent_projector(rho_a, rho_b, Z)
    Q_Z = normal_projector(rho_a, rho_b, Z)
    
    np.testing.assert_allclose(P_Z + Q_Z, Z, atol=1e-14)
    
    # Orthogonality/annihilation
    Q_P_Z = normal_projector(rho_a, rho_b, P_Z)
    P_Q_Z = retraction_tangent_projector(rho_a, rho_b, Q_Z)
    np.testing.assert_allclose(Q_P_Z, np.zeros((4, 4)), atol=1e-14)
    np.testing.assert_allclose(P_Q_Z, np.zeros((4, 4)), atol=1e-14)


def test_marginal_preservation():
    """Verify that P_e preserves single-site reduced marginals exactly."""
    psi_a = np.array([0.8, 0.6], dtype=complex)
    rho_a = np.outer(psi_a, psi_a.conj())
    psi_b = np.array([0.6, -0.8j], dtype=complex)
    rho_b = np.outer(psi_b, psi_b.conj())
    
    np.random.seed(44)
    Z = np.random.randn(4, 4) + 1.0j * np.random.randn(4, 4)
    
    P_Z = retraction_tangent_projector(rho_a, rho_b, Z)
    
    # Check Tr_B(P_e Z) == Tr_B(Z)
    tr_B_Z = partial_trace(Z, [0], 2)
    tr_B_PZ = partial_trace(P_Z, [0], 2)
    np.testing.assert_allclose(tr_B_PZ, tr_B_Z, atol=1e-14)
    
    # Check Tr_A(P_e Z) == Tr_A(Z)
    tr_A_Z = partial_trace(Z, [1], 2)
    tr_A_PZ = partial_trace(P_Z, [1], 2)
    np.testing.assert_allclose(tr_A_PZ, tr_A_Z, atol=1e-14)


def test_po000_lemma_5_3_tangent_isolation():
    """Kill test: 1-local terms generate zero normal residual across the edge."""
    psi_a = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho_a = np.outer(psi_a, psi_a.conj())
    psi_b = np.array([1.0, 0.0], dtype=complex)
    rho_b = np.outer(psi_b, psi_b.conj())
    
    p = pauli_matrices()
    for name in ["X", "Y", "Z"]:
        h_a = p[name]
        residual_norm = verify_lemma_5_3_tangent_isolation(rho_a, rho_b, h_a)
        assert residual_norm == pytest.approx(0.0, abs=1e-14)


def test_two_body_interaction_generates_nonzero_residual():
    """Verify that genuine 2-body interaction produces non-zero residual rate nu_e > 0."""
    psi_plus = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho_plus = np.outer(psi_plus, psi_plus.conj())
    
    p = pauli_matrices()
    h_zz = np.kron(p["Z"], p["Z"])
    
    n_e, nu_e = compute_edge_residual(rho_plus, rho_plus, h_zz)
    assert nu_e > 0.1
    # Check that n_e is traceless and Hermitian
    np.testing.assert_allclose(np.trace(n_e), 0.0, atol=1e-14)
    np.testing.assert_allclose(n_e, n_e.conj().T, atol=1e-14)


def test_schatten1_dual_witness_certification():
    """Verify Schatten-1 dual witness satisfies ||W||_inf <= 1 and Tr(W^dagger Q) = ||Q||_1."""
    # Construct arbitrary Hermitian matrix Q
    np.random.seed(45)
    A = np.random.randn(4, 4) + 1.0j * np.random.randn(4, 4)
    Q = A + A.conj().T
    
    W, gap = dual_witness_schatten1(Q)
    assert operator_norm(W) <= 1.0 + 1e-12
    assert gap == pytest.approx(0.0, abs=1e-12)
    
    # Assert alignment: Re(Tr(W^dagger Q)) == ||Q||_1
    val = float(np.real(np.trace(W.conj().T @ Q)))
    assert val == pytest.approx(trace_norm(Q), abs=1e-12)


def test_lattice_local_residuals(tfim_n4):
    """Verify compute_local_residuals computes rates for all edges."""
    from caqd.spin_chains import polarized_x_state
    rho0 = polarized_x_state(4)
    rates = compute_local_residuals(tfim_n4, rho0)
    
    assert len(rates) == len(tfim_n4.edges)
    for edge in tfim_n4.edges:
        assert rates[edge] >= 0.0
