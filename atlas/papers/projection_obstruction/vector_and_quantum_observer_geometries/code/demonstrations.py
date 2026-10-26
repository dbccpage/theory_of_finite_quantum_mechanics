"""
Numerical Demonstrations of Vector and Quantum Observer Geometries.
Paper: GS-003 (vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

from __future__ import annotations
from typing import Dict, Any
import numpy as np

from cochain_complex import GraphComplex, Cochain
from classical_geometry import ClassicalQuotientSolver
from quantum_geometry import HermitianOperator, QuantumQuotientSolver
from cptp_channels import KrausChannel, CochainMorphism


def demo_classical_triangle_separation() -> Dict[str, Any]:
    """
    Demonstration 1: Classical Vector Separation on 3-Cycle Triangle.
    Fixture:
        Edges: (0, 1), (1, 2), (2, 0), equal weights w_e = 1.
        Offsets: omega_01 = (1, 0), omega_12 = (0, 1), omega_20 = (0, 0).
        Net circulation: c = sum_e omega_e = (1, 1).
    Results:
        Coordinate l1 gauge: Phi_{1,1} = 2.0.
        Euclidean l2 gauge: Phi_{2,1} = sqrt(2) approx 1.41421356.
    """
    comp = GraphComplex.triangle_complex(edge_weights=[1.0, 1.0, 1.0])
    omega_data = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]], dtype=float)
    omega = Cochain(omega_data, degree=1)

    solver = ClassicalQuotientSolver(comp, tol=1e-5)

    cert_l1 = solver.solve(omega, p=1)
    cert_l2 = solver.solve(omega, p=2)
    cert_linf = solver.solve(omega, p=np.inf)

    analytic_l1 = solver.cycle_analytic_quotient(omega, p=1)
    analytic_l2 = solver.cycle_analytic_quotient(omega, p=2)

    return {
        "circulation": np.sum(omega_data, axis=0).tolist(),
        "phi_1_1_primal": cert_l1.primal_value,
        "phi_1_1_dual": cert_l1.dual_value,
        "phi_1_1_gap": cert_l1.duality_gap,
        "phi_1_1_analytic": analytic_l1,
        "phi_2_1_primal": cert_l2.primal_value,
        "phi_2_1_dual": cert_l2.dual_value,
        "phi_2_1_gap": cert_l2.duality_gap,
        "phi_2_1_analytic": analytic_l2,
        "phi_inf_1_primal": cert_linf.primal_value,
        "phi_inf_1_dual": cert_linf.dual_value,
        "phi_inf_1_gap": cert_linf.duality_gap,
        "separation_ratio_l1_over_l2": cert_l1.primal_value / cert_l2.primal_value,
        "theoretical_sqrt2": np.sqrt(2.0),
    }


def demo_quantum_triangle_uniform_z() -> Dict[str, Any]:
    """
    Demonstration 2: Quantum Trace Obstruction on 3-Cycle Triangle.
    Part A:
        Uniform Pauli Z offsets: delta_e = 0.5 * sigma_z on all 3 edges.
        Net circulation: c = 3A = diag(1.5, -1.5).
        Result: Phi_Q = 3/2 = 1.5.
    Part B:
        Telescoping marginal pure states: |0>, |+>, |1>.
        Coboundary delta = d0 phi.
        Result: Phi_Q = 0.0 (exact coboundary).
    """
    comp = GraphComplex.triangle_complex(edge_weights=[1.0, 1.0, 1.0])
    solver = QuantumQuotientSolver(comp, tol=1e-4)

    # Part A: Uniform Pauli Z
    a_mat = 0.5 * HermitianOperator.SIGMA_Z
    delta_uniform_data = np.array([a_mat, a_mat, a_mat], dtype=complex)
    delta_uniform = Cochain(delta_uniform_data, degree=1)

    cert_uniform = solver.solve(delta_uniform)
    analytic_uniform = solver.cycle_analytic_quotient(delta_uniform)

    # Part B: Telescoping marginal pure states
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
    delta_telescoping = comp.d0(phi_cochain)

    cert_telescoping = solver.solve(delta_telescoping)

    return {
        "uniform_phi_q_primal": cert_uniform.primal_value,
        "uniform_phi_q_dual": cert_uniform.dual_value,
        "uniform_phi_q_gap": cert_uniform.duality_gap,
        "uniform_phi_q_analytic": analytic_uniform,
        "telescoping_phi_q_primal": cert_telescoping.primal_value,
        "telescoping_phi_q_dual": cert_telescoping.dual_value,
        "telescoping_is_zero": cert_telescoping.primal_value < 1e-4,
    }


def demo_bloch_isometry_vs_qutrit_crosspolytope() -> Dict[str, Any]:
    """
    Demonstration 3: Bloch Sphere Isometry (d=2) vs Qutrit Spectral Cross-Polytope (d=3).
    - d = 2: j_Q(X) = 0.5 ||X||_1 = ||v||_2 exactly, and parallelogram law holds:
      2 ||X1||_1^2 + 2 ||X2||_1^2 == ||X1+X2||_1^2 + ||X1-X2||_1^2.
    - d = 3: For X1 = diag(1, -1, 0) and X2 = diag(0, 1, -1), parallelogram law fails,
      proving non-Euclidean geometry of the Schatten 1-norm unit ball.
    """
    # 1. Qubit (d=2) Bloch vector checks
    rng = np.random.default_rng(42)
    v_random = rng.standard_normal(3)
    x_qubit = HermitianOperator.from_bloch_vector(v_random)
    j_q_qubit = HermitianOperator.trace_distance(x_qubit)
    l2_v = float(np.linalg.norm(v_random))
    bloch_isometry_diff = abs(j_q_qubit - l2_v)

    # Parallelogram law on qubits:
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([0.0, 1.0, 0.0])
    x1_q = HermitianOperator.from_bloch_vector(v1)
    x2_q = HermitianOperator.from_bloch_vector(v2)
    norm_x1_q = HermitianOperator.schatten_norm(x1_q, p=1)
    norm_x2_q = HermitianOperator.schatten_norm(x2_q, p=1)
    norm_sum_q = HermitianOperator.schatten_norm(x1_q + x2_q, p=1)
    norm_diff_q = HermitianOperator.schatten_norm(x1_q - x2_q, p=1)
    lhs_q = 2.0 * (norm_x1_q**2) + 2.0 * (norm_x2_q**2)
    rhs_q = (norm_sum_q**2) + (norm_diff_q**2)
    qubit_parallelogram_err = abs(lhs_q - rhs_q)

    # 2. Qutrit (d=3) non-Euclidean cross-polytope check
    x1_qutrit = np.diag([1.0, -1.0, 0.0]).astype(complex)
    x2_qutrit = np.diag([0.0, 1.0, -1.0]).astype(complex)
    norm_x1_3 = HermitianOperator.schatten_norm(x1_qutrit, p=1)
    norm_x2_3 = HermitianOperator.schatten_norm(x2_qutrit, p=1)
    norm_sum_3 = HermitianOperator.schatten_norm(x1_qutrit + x2_qutrit, p=1)
    norm_diff_3 = HermitianOperator.schatten_norm(x1_qutrit - x2_qutrit, p=1)

    lhs_3 = 2.0 * (norm_x1_3**2) + 2.0 * (norm_x2_3**2)
    rhs_3 = (norm_sum_3**2) + (norm_diff_3**2)
    qutrit_parallelogram_discrepancy = abs(lhs_3 - rhs_3)

    return {
        "qubit_bloch_isometry_diff": bloch_isometry_diff,
        "qubit_parallelogram_err": qubit_parallelogram_err,
        "qubit_is_euclidean": qubit_parallelogram_err < 1e-12,
        "qutrit_norm_x1": norm_x1_3,
        "qutrit_norm_x2": norm_x2_3,
        "qutrit_norm_sum": norm_sum_3,
        "qutrit_norm_diff": norm_diff_3,
        "qutrit_parallelogram_lhs": lhs_3,
        "qutrit_parallelogram_rhs": rhs_3,
        "qutrit_parallelogram_discrepancy": qutrit_parallelogram_discrepancy,
        "qutrit_is_non_euclidean": qutrit_parallelogram_discrepancy > 1e-3,
    }


def demo_cptp_quotient_monotonicity() -> Dict[str, Any]:
    """
    Demonstration 4: CPTP Quotient Monotonicity under Coboundary Intertwining.
    Shows:
        Phi_Q'([Lambda^1 delta]) <= Phi_Q([delta])
    under depolarizing noise (strict contraction), amplitude damping, and unitary conjugation (equality).
    """
    comp = GraphComplex.triangle_complex(edge_weights=[1.0, 1.0, 1.0])
    solver = QuantumQuotientSolver(comp, tol=1e-4)

    a_mat = 0.5 * HermitianOperator.SIGMA_Z
    delta = Cochain(np.array([a_mat, a_mat, a_mat], dtype=complex), degree=1)
    cert_base = solver.solve(delta)
    phi_base = cert_base.primal_value  # 1.5

    # 1. Depolarizing channel with p = 0.4
    depol_ch = KrausChannel.depolarizing(d=2, p=0.4)
    morphism_depol = CochainMorphism.uniform(comp, depol_ch)
    is_intertwined_depol, _ = morphism_depol.verify_intertwining(comp)
    is_mono_depol, _, phi_depol = morphism_depol.verify_quotient_monotonicity(
        solver, delta
    )

    # 2. Amplitude damping channel with gamma = 0.3
    ad_ch = KrausChannel.amplitude_damping(gamma=0.3)
    morphism_ad = CochainMorphism.uniform(comp, ad_ch)
    is_intertwined_ad, _ = morphism_ad.verify_intertwining(comp)
    is_mono_ad, _, phi_ad = morphism_ad.verify_quotient_monotonicity(solver, delta)

    # 3. Unitary channel (Hadamard gate)
    h_gate = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / np.sqrt(2.0)
    u_ch = KrausChannel.unitary(h_gate)
    morphism_u = CochainMorphism.uniform(comp, u_ch)
    is_intertwined_u, _ = morphism_u.verify_intertwining(comp)
    is_mono_u, _, phi_u = morphism_u.verify_quotient_monotonicity(solver, delta)

    return {
        "phi_base": phi_base,
        "depolarizing": {
            "p": 0.4,
            "is_intertwined": is_intertwined_depol,
            "phi_depol": phi_depol,
            "is_monotone": is_mono_depol,
            "ratio": phi_depol / phi_base,
        },
        "amplitude_damping": {
            "gamma": 0.3,
            "is_intertwined": is_intertwined_ad,
            "phi_ad": phi_ad,
            "is_monotone": is_mono_ad,
            "ratio": phi_ad / phi_base,
        },
        "unitary_invariance": {
            "is_intertwined": is_intertwined_u,
            "phi_u": phi_u,
            "abs_difference": abs(phi_u - phi_base),
            "is_exact_invariant": abs(phi_u - phi_base) < 1e-4,
        },
    }
