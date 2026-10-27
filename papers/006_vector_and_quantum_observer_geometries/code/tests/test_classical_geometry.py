"""
Tests for classical vector observer geometries and mixed norm solvers.
Paper: GS-003 (006_vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

import pytest
import numpy as np

from cochain_complex import Cochain, GraphComplex
from classical_geometry import ClassicalQuotientSolver
from exceptions import DimensionMismatchError


def test_classical_triangle_l2_separation():
    comp = GraphComplex.triangle_complex(edge_weights=[1.0, 1.0, 1.0])
    omega_data = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]], dtype=float)
    omega = Cochain(omega_data, degree=1)

    solver = ClassicalQuotientSolver(comp, tol=1e-5)
    cert = solver.solve(omega, p=2)

    assert cert.p_norm == 2
    assert abs(cert.primal_value - np.sqrt(2.0)) < 1e-5
    assert abs(cert.dual_value - np.sqrt(2.0)) < 1e-5
    assert cert.duality_gap < 1e-5
    assert cert.is_divergence_free
    assert cert.is_dual_feasible
    assert cert.is_optimal

    analytic = solver.cycle_analytic_quotient(omega, p=2)
    assert abs(cert.primal_value - analytic) < 1e-5


def test_classical_triangle_l1():
    comp = GraphComplex.triangle_complex(edge_weights=[1.0, 1.0, 1.0])
    omega_data = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]], dtype=float)
    omega = Cochain(omega_data, degree=1)

    solver = ClassicalQuotientSolver(comp, tol=1e-5)
    cert = solver.solve(omega, p=1)

    assert cert.p_norm == 1
    assert abs(cert.primal_value - 2.0) < 1e-5
    assert abs(cert.dual_value - 2.0) < 1e-5
    assert cert.duality_gap < 1e-5
    assert cert.is_divergence_free
    assert cert.is_dual_feasible
    assert cert.is_optimal

    analytic = solver.cycle_analytic_quotient(omega, p=1)
    assert abs(cert.primal_value - analytic) < 1e-5


def test_classical_triangle_linf():
    comp = GraphComplex.triangle_complex(edge_weights=[1.0, 1.0, 1.0])
    omega_data = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]], dtype=float)
    omega = Cochain(omega_data, degree=1)

    solver = ClassicalQuotientSolver(comp, tol=1e-5)
    cert = solver.solve(omega, p=np.inf)

    assert cert.p_norm == np.inf
    # Net circulation is (1, 1). Linf norm is max(|1|, |1|) = 1.0
    assert abs(cert.primal_value - 1.0) < 1e-5
    assert abs(cert.dual_value - 1.0) < 1e-5
    assert cert.duality_gap < 1e-5
    assert cert.is_divergence_free
    assert cert.is_dual_feasible
    assert cert.is_optimal

    analytic = solver.cycle_analytic_quotient(omega, p=np.inf)
    assert abs(cert.primal_value - analytic) < 1e-5


def test_classical_zero_circulation():
    comp = GraphComplex.triangle_complex()
    # Construct exact coboundary omega = d0 phi
    phi = Cochain([[1.0, -1.0], [2.0, 0.5], [-0.5, 3.0]], degree=0)
    omega = comp.d0(phi)

    solver = ClassicalQuotientSolver(comp, tol=1e-5)
    cert_l2 = solver.solve(omega, p=2)
    assert cert_l2.primal_value < 1e-5
    assert cert_l2.duality_gap < 1e-5

    cert_l1 = solver.solve(omega, p=1)
    assert cert_l1.primal_value < 1e-5
    assert cert_l1.duality_gap < 1e-5


def test_classical_cycle_analytic_custom_p():
    comp = GraphComplex.triangle_complex(edge_weights=[2.0, 3.0, 4.0])
    omega = Cochain([[1.0, 2.0], [0.0, -1.0], [1.0, 0.0]], degree=1)
    solver = ClassicalQuotientSolver(comp)

    # c = (2, 1)
    # min_w = 2.0
    # p = 3: norm = (2^3 + 1^3)^(1/3) = 9^(1/3)
    val = solver.cycle_analytic_quotient(omega, p=3)
    exp = 2.0 * (9.0 ** (1.0 / 3.0))
    assert abs(val - exp) < 1e-12


def test_classical_solver_errors():
    comp = GraphComplex.triangle_complex()
    solver = ClassicalQuotientSolver(comp)

    # Bad degree
    c_deg0 = Cochain([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], degree=0)
    with pytest.raises(DimensionMismatchError):
        solver.solve(c_deg0)

    # Bad cell count
    c_bad_cells = Cochain([[1.0, 2.0], [3.0, 4.0]], degree=1)
    with pytest.raises(DimensionMismatchError):
        solver.solve(c_bad_cells)

    # Operator cochain
    sz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    c_op = Cochain(np.array([sz, sz, sz]), degree=1)
    with pytest.raises(ValueError):
        solver.solve(c_op)

    # Unsupported p norm
    c_vec = Cochain([[1.0], [2.0], [3.0]], degree=1)
    with pytest.raises(NotImplementedError):
        solver.solve(c_vec, p=3)
