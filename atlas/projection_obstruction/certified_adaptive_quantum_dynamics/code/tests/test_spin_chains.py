"""Tests for spin chain models, Pauli algebra, and norm metrics.

AuthorityEffect: None.
"""

import pytest
import numpy as np
import scipy.linalg

from caqd.spin_chains import (
    TFIMChain,
    XXZChain,
    pauli_matrices,
    operator_norm,
    trace_norm,
    hilbert_schmidt_norm,
    partial_trace,
    pauli_on_site,
    two_body_op,
    staggered_magnetization,
    center_correlation,
    transverse_magnetization,
    neel_state,
    polarized_x_state,
    all_up_state,
)


def test_pauli_algebra():
    """Verify algebraic properties of single-qubit Pauli matrices."""
    p = pauli_matrices()
    X, Y, Z, I = p["X"], p["Y"], p["Z"], p["I"]
    
    # Involutory: sigma^2 = I
    np.testing.assert_allclose(X @ X, I, atol=1e-14)
    np.testing.assert_allclose(Y @ Y, I, atol=1e-14)
    np.testing.assert_allclose(Z @ Z, I, atol=1e-14)
    
    # Commutation: [X, Y] = 2i Z
    np.testing.assert_allclose(X @ Y - Y @ X, 2.0j * Z, atol=1e-14)
    np.testing.assert_allclose(Y @ Z - Z @ Y, 2.0j * X, atol=1e-14)
    np.testing.assert_allclose(Z @ X - X @ Z, 2.0j * Y, atol=1e-14)


def test_matrix_norms():
    """Verify spectral norm, Schatten-1 trace norm, and Hilbert-Schmidt norm."""
    diag = np.diag([3.0, -2.0, 1.0, 0.0])
    assert operator_norm(diag) == pytest.approx(3.0)
    assert trace_norm(diag) == pytest.approx(6.0)
    assert hilbert_schmidt_norm(diag) == pytest.approx(np.sqrt(9.0 + 4.0 + 1.0))
    
    # Zero matrix norm
    zero_mat = np.zeros((3, 3), dtype=complex)
    assert operator_norm(zero_mat) == 0.0
    assert trace_norm(zero_mat) == 0.0
    assert hilbert_schmidt_norm(zero_mat) == 0.0


def test_partial_trace():
    """Verify partial trace implementation on bipartite and multipartite systems."""
    # Bipartite state: Bell state (|00> + |11>)/sqrt(2)
    psi = np.array([1.0, 0.0, 0.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho_bell = np.outer(psi, psi.conj())
    
    # Tracing out site 1 leaves maximally mixed state I/2 on site 0
    rho_0 = partial_trace(rho_bell, [0], num_sites=2)
    np.testing.assert_allclose(rho_0, 0.5 * np.eye(2), atol=1e-14)
    
    # Tracing out site 0 leaves I/2 on site 1
    rho_1 = partial_trace(rho_bell, [1], num_sites=2)
    np.testing.assert_allclose(rho_1, 0.5 * np.eye(2), atol=1e-14)
    
    # Keeping all sites returns original state
    np.testing.assert_allclose(partial_trace(rho_bell, [0, 1], num_sites=2), rho_bell, atol=1e-14)
    
    # Keeping 0 sites returns total trace
    np.testing.assert_allclose(partial_trace(rho_bell, [], num_sites=2), np.array([[1.0]]), atol=1e-14)


def test_tfim_hermiticity_and_spectrum(tfim_n4):
    """Verify TFIM Hamiltonian is Hermitian and has real spectrum."""
    H = tfim_n4.H
    assert H.shape == (16, 16)
    np.testing.assert_allclose(H, H.conj().T, atol=1e-14)
    
    evals = scipy.linalg.eigvalsh(H)
    assert np.all(np.isreal(evals))
    
    # Check edges
    assert tfim_n4.edges == [(0, 1), (1, 2), (2, 3)]


def test_xxz_hermiticity_and_spectrum(xxz_n4):
    """Verify XXZ Hamiltonian is Hermitian and has real spectrum."""
    H = xxz_n4.H
    assert H.shape == (16, 16)
    np.testing.assert_allclose(H, H.conj().T, atol=1e-14)
    
    evals = scipy.linalg.eigvalsh(H)
    assert np.all(np.isreal(evals))
    assert xxz_n4.edges == [(0, 1), (1, 2), (2, 3)]


def test_periodic_boundary_conditions():
    """Verify periodic boundary conditions include wrap-around term."""
    tfim_p = TFIMChain(num_sites=4, J=1.0, h=1.0, periodic=True)
    assert tfim_p.edges == [(0, 1), (1, 2), (2, 3), (3, 0)]
    assert len(tfim_p.terms) == 4 + 4 # 4 1-local + 4 2-local


def test_observables_norm_and_hermiticity():
    """Verify standard observables are Hermitian with operator norm <= 1."""
    N = 4
    for obs in [staggered_magnetization(N), center_correlation(N), transverse_magnetization(N)]:
        np.testing.assert_allclose(obs, obs.conj().T, atol=1e-14)
        assert operator_norm(obs) <= 1.0 + 1e-12


def test_initial_states_purity():
    """Verify standard initial states are valid pure density matrices."""
    N = 4
    for state in [neel_state(N), polarized_x_state(N), all_up_state(N)]:
        np.testing.assert_allclose(state, state.conj().T, atol=1e-14)
        assert np.trace(state) == pytest.approx(1.0)
        # Pure state has Tr(rho^2) = 1
        assert np.real(np.trace(state @ state)) == pytest.approx(1.0)
        # Positive semidefinite
        evals = scipy.linalg.eigvalsh(state)
        assert np.all(evals >= -1e-14)


def test_invalid_parameters():
    """Verify model constructor catches invalid arguments."""
    with pytest.raises(ValueError):
        TFIMChain(num_sites=1)
    with pytest.raises(ValueError):
        pauli_on_site(np.eye(2), site=5, num_sites=4)
    with pytest.raises(ValueError):
        two_body_op(np.eye(2), np.eye(2), site1=2, site2=2, num_sites=4)
