"""
Tests for quantum observer geometries, Schatten norms, and Helstrom dual solvers.
Paper: GS-003 (006_vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

import pytest
import numpy as np

from cochain_complex import Cochain, GraphComplex
from quantum_geometry import HermitianOperator, QuantumQuotientSolver
from exceptions import NonHermitianOperatorError, DimensionMismatchError


def test_hermitian_operator_basics():
    # Pauli matrices
    for sigma in HermitianOperator.PAULI_VECTOR:
        HermitianOperator.check_hermitian(sigma)
        assert HermitianOperator.check_traceless(sigma)

    # Identity is Hermitian but not traceless
    eye = np.eye(2, dtype=complex)
    HermitianOperator.check_hermitian(eye)
    assert not HermitianOperator.check_traceless(eye)

    # Non-Hermitian matrix
    non_herm = np.array([[1.0, 2.0], [0.0, 1.0]], dtype=complex)
    with pytest.raises(NonHermitianOperatorError):
        HermitianOperator.check_hermitian(non_herm)

    # Non-square matrix
    rect = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], dtype=complex)
    with pytest.raises(DimensionMismatchError):
        HermitianOperator.check_hermitian(rect)


def test_schatten_norms():
    # A = diag(3, -4)
    # Singular values: 4, 3
    a = np.diag([3.0, -4.0]).astype(complex)

    assert abs(HermitianOperator.schatten_norm(a, p=1) - 7.0) < 1e-12
    assert abs(HermitianOperator.schatten_norm(a, p=2) - 5.0) < 1e-12
    assert abs(HermitianOperator.schatten_norm(a, p=np.inf) - 4.0) < 1e-12
    assert abs(HermitianOperator.schatten_norm(a, p="inf") - 4.0) < 1e-12

    # Custom p=3: (4^3 + 3^3)^(1/3) = (64 + 27)^(1/3) = 91^(1/3)
    p3 = HermitianOperator.schatten_norm(a, p=3)
    assert abs(p3 - (91.0 ** (1.0 / 3.0))) < 1e-12

    # Trace distance gauge: 0.5 * ||A||_1 = 3.5
    assert abs(HermitianOperator.trace_distance(a) - 3.5) < 1e-12


def test_bloch_vector_mapping():
    rng = np.random.default_rng(123)
    for _ in range(5):
        v = rng.standard_normal(3)
        mat = HermitianOperator.from_bloch_vector(v)
        v_recovered = HermitianOperator.to_bloch_vector(mat)
        np.testing.assert_allclose(v_recovered, v, atol=1e-12)

        # Isometry: j_Q(X) = ||v||_2
        j_q = HermitianOperator.trace_distance(mat)
        assert abs(j_q - np.linalg.norm(v)) < 1e-12

    # Dimension errors
    with pytest.raises(DimensionMismatchError):
        HermitianOperator.from_bloch_vector([1.0, 2.0])

    mat3 = np.zeros((3, 3), dtype=complex)
    with pytest.raises(DimensionMismatchError):
        HermitianOperator.to_bloch_vector(mat3)


def test_gell_mann_basis():
    for d in [2, 3, 4]:
        basis = HermitianOperator.gell_mann_basis(d)
        assert len(basis) == d**2 - 1

        for a, gen_a in enumerate(basis):
            HermitianOperator.check_hermitian(gen_a)
            assert HermitianOperator.check_traceless(gen_a)

            for b, gen_b in enumerate(basis):
                tr_ab = float(np.real(np.trace(gen_a @ gen_b)))
                expected = 2.0 if a == b else 0.0
                assert abs(tr_ab - expected) < 1e-10


def test_quantum_quotient_solver_uniform_z():
    comp = GraphComplex.triangle_complex(edge_weights=[1.0, 1.0, 1.0])
    solver = QuantumQuotientSolver(comp, tol=1e-4)

    a_mat = 0.5 * HermitianOperator.SIGMA_Z
    delta = Cochain(np.array([a_mat, a_mat, a_mat], dtype=complex), degree=1)

    cert = solver.solve(delta)
    assert abs(cert.primal_value - 1.5) < 1e-4
    assert abs(cert.dual_value - 1.5) < 1e-4
    assert cert.duality_gap < 1e-4
    assert cert.is_divergence_free
    assert cert.is_dual_feasible
    assert cert.is_optimal

    analytic = solver.cycle_analytic_quotient(delta)
    assert abs(cert.primal_value - analytic) < 1e-4


def test_quantum_quotient_solver_telescoping():
    comp = GraphComplex.triangle_complex()
    solver = QuantumQuotientSolver(comp, tol=1e-4)

    psi0 = np.array([1.0, 0.0], dtype=complex)
    psi1 = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    psi2 = np.array([0.0, 1.0], dtype=complex)

    rho0 = np.outer(psi0, psi0.conj())
    rho1 = np.outer(psi1, psi1.conj())
    rho2 = np.outer(psi2, psi2.conj())

    phi0 = rho0 - 0.5 * np.eye(2, dtype=complex)
    phi1 = rho1 - 0.5 * np.eye(2, dtype=complex)
    phi2 = rho2 - 0.5 * np.eye(2, dtype=complex)

    phi_cochain = Cochain(np.array([phi0, phi1, phi2]), degree=0)
    delta_tel = comp.d0(phi_cochain)

    cert = solver.solve(delta_tel)
    assert cert.primal_value < 1e-4
    assert cert.duality_gap < 1e-4


def test_quantum_solver_errors():
    comp = GraphComplex.triangle_complex()
    solver = QuantumQuotientSolver(comp)

    # Vector cochain
    c_vec = Cochain([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]], degree=1)
    with pytest.raises(ValueError):
        solver.solve(c_vec)

    # Degree mismatch
    sz = HermitianOperator.SIGMA_Z
    c_deg0 = Cochain(np.array([sz, sz, sz]), degree=0)
    with pytest.raises(DimensionMismatchError):
        solver.solve(c_deg0)

    # Cell count mismatch
    c_cells = Cochain(np.array([sz, sz]), degree=1)
    with pytest.raises(DimensionMismatchError):
        solver.solve(c_cells)

    # List input to check_hermitian
    HermitianOperator.check_hermitian([[1.0, 0.0], [0.0, -1.0]])

    # solve with check_hermitian=False
    delta = Cochain(np.array([0.5 * sz, 0.5 * sz, 0.5 * sz]), degree=1)
    cert_nocheck = solver.solve(delta, check_hermitian=False)
    assert abs(cert_nocheck.primal_value - 1.5) < 1e-4
