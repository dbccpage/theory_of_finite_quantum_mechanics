"""
Tests for numerical demonstrations of vector and quantum observer geometries.
Paper: GS-003 (006_vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

import numpy as np
from demonstrations import (
    demo_classical_triangle_separation,
    demo_quantum_triangle_uniform_z,
    demo_bloch_isometry_vs_qutrit_crosspolytope,
    demo_cptp_quotient_monotonicity,
)


def test_demo_classical_triangle_separation():
    d1 = demo_classical_triangle_separation()
    assert abs(d1["phi_1_1_primal"] - 2.0) < 1e-4
    assert abs(d1["phi_2_1_primal"] - np.sqrt(2.0)) < 1e-4
    assert abs(d1["phi_inf_1_primal"] - 1.0) < 1e-4
    assert abs(d1["separation_ratio_l1_over_l2"] - np.sqrt(2.0)) < 1e-4
    assert d1["phi_1_1_gap"] < 1e-4
    assert d1["phi_2_1_gap"] < 1e-4
    assert d1["phi_inf_1_gap"] < 1e-4


def test_demo_quantum_triangle_uniform_z():
    d2 = demo_quantum_triangle_uniform_z()
    assert abs(d2["uniform_phi_q_primal"] - 1.5) < 1e-4
    assert abs(d2["uniform_phi_q_dual"] - 1.5) < 1e-4
    assert d2["uniform_phi_q_gap"] < 1e-4
    assert abs(d2["telescoping_phi_q_primal"]) < 1e-4
    assert d2["telescoping_is_zero"]


def test_demo_bloch_isometry_vs_qutrit_crosspolytope():
    d3 = demo_bloch_isometry_vs_qutrit_crosspolytope()
    assert d3["qubit_bloch_isometry_diff"] < 1e-12
    assert d3["qubit_parallelogram_err"] < 1e-12
    assert d3["qubit_is_euclidean"]
    assert d3["qutrit_is_non_euclidean"]
    assert d3["qutrit_parallelogram_discrepancy"] > 1.0


def test_demo_cptp_quotient_monotonicity():
    d4 = demo_cptp_quotient_monotonicity()
    assert abs(d4["phi_base"] - 1.5) < 1e-4

    depol = d4["depolarizing"]
    assert depol["is_intertwined"]
    assert depol["is_monotone"]
    assert abs(depol["ratio"] - 0.6) < 1e-4

    ad = d4["amplitude_damping"]
    assert ad["is_intertwined"]
    assert ad["is_monotone"]
    assert ad["ratio"] <= 1.0 + 1e-4

    u_inv = d4["unitary_invariance"]
    assert u_inv["is_intertwined"]
    assert u_inv["is_exact_invariant"]
    assert u_inv["abs_difference"] < 1e-4
