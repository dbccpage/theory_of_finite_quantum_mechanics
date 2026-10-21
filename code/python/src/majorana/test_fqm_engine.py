r"""
Tests for the AnomalonicQAM finite-QM reference engine.

AuthorityEffect: None.

Every test below states the invariant it defends and is written so that a real mutation of
the implementation kills it. In particular `test_nu_e_vanishes_on_the_product_manifold`
fails if Q_e is dropped (the un-projected norm there is 0.8, not 0), which is exactly the
defect D5 found in the prior reference engine.
"""

import numpy as np
import pytest

from omega_engine.crates.quantum_physics.primitives import (
    I2,
    SIGMA_X,
    SIGMA_Y,
    SIGMA_Z,
    partial_trace_a,
    partial_trace_b,
    trace_norm,
)
from omega_engine.crates.quantum_physics.bipartite_carrier import BipartiteEdge
from omega_engine.crates.quantum_physics.bipartite_retraction import d1_witness, product_witness




def test_trace_norm_is_sum_of_absolute_eigenvalues_on_a_known_matrix():
    """||diag(1,-1)||_1 = 2, not |1 + (-1)| = 0. Kills any use of |trace|."""
    assert trace_norm(np.diag([1.0, -1.0]).astype(complex)) == pytest.approx(2.0)


def test_trace_norm_of_a_density_matrix_is_one():
    rho = np.diag([0.3, 0.7]).astype(complex)
    assert trace_norm(rho) == pytest.approx(1.0)


def test_partial_traces_invert_a_product():
    """Tr_b(rho_a (x) rho_b) = rho_a and Tr_a(...) = rho_b. Kills swapped index conventions."""
    rho_a = np.array([[0.6, 0.1], [0.1, 0.4]], dtype=complex)
    rho_b = np.array([[0.8, 0.0], [0.0, 0.2]], dtype=complex)
    prod = np.kron(rho_a, rho_b)
    assert np.allclose(partial_trace_b(prod), rho_a)
    assert np.allclose(partial_trace_a(prod), rho_b)


def test_partial_trace_b_is_not_partial_trace_a():
    """Guards against both helpers collapsing to the same einsum."""
    rho_a = np.array([[0.9, 0.0], [0.0, 0.1]], dtype=complex)
    rho_b = np.array([[0.2, 0.0], [0.0, 0.8]], dtype=complex)
    prod = np.kron(rho_a, rho_b)
    assert not np.allclose(partial_trace_b(prod), partial_trace_a(prod))




def test_P_e_is_idempotent():
    """P_e is the differential of a retraction at a fixed point, so P_e o P_e = P_e."""
    edge = d1_witness()
    z, _ = edge.derivatives()
    assert np.allclose(edge.P_e(edge.P_e(z)), edge.P_e(z), atol=1e-12)


def test_Q_e_annihilates_the_tangent_component():
    """Q_e = I - P_e, so Q_e(P_e Z) = 0."""
    edge = d1_witness()
    z, _ = edge.derivatives()
    assert trace_norm(edge.Q_e(edge.P_e(z))) == pytest.approx(0.0, abs=1e-12)




def test_nu_e_vanishes_on_the_product_manifold():
    """For a non-interacting Hamiltonian the product manifold is invariant, so nu_e = 0.

    This is the test the prior engine could not pass: the UN-projected norm here is 0.8.
    If Q_e is removed from nu_e, this assertion fails.
    """
    edge = product_witness()
    rdot, _ = edge.derivatives()
    assert trace_norm(rdot) == pytest.approx(0.8)
    assert edge.nu_e() == pytest.approx(0.0, abs=1e-12)


def test_product_edge_stays_product_under_evolution():
    edge = product_witness()
    for t in (0.1, 0.3, 1.0):
        assert edge.exact_defect(t) == pytest.approx(0.0, abs=1e-10)


def test_interacting_edge_has_strictly_positive_nu_e():
    assert d1_witness().nu_e() == pytest.approx(2.0)




def test_a_e_as_defined_is_not_the_second_order_coefficient():
    """Defect D1: a_e := 0.5*||Q_e rho_ddot||_1 omits the cross term 2 rho_dot_a (x) rho_dot_b.

    These numbers are the ones quoted in the skeleton's D1 table. If someone 'fixes' the
    engine by making the two agree without adding the cross term, this test fails.
    """
    r = d1_witness().second_order_report()
    assert r["a_e_as_defined"] == pytest.approx(6.891618, abs=1e-6)
    assert r["a_e_true"] == pytest.approx(5.954592, abs=1e-6)
    assert r["omitted_cross_term_norm"] == pytest.approx(5.760000, abs=1e-6)
    assert r["discrepancy"] > 0.9


def test_cross_term_is_genuinely_omitted_from_the_defined_a_e():
    """f''(0) and Q_e rho_ddot(0) differ by exactly the cross term."""
    edge = d1_witness()
    _, rddot = edge.derivatives()
    assert np.allclose(edge.Q_e(rddot) - edge.f_second_derivative(), edge.cross_term())


def test_cross_term_is_not_small():
    """A term of norm 5.76 against a_e = 6.89 cannot be dismissed as higher order."""
    edge = d1_witness()
    assert trace_norm(edge.cross_term()) > 0.5 * edge.a_e_as_defined()




@pytest.mark.parametrize("t", [0.02, 0.05, 0.1])
def test_short_time_lower_bound_with_true_coefficient_does_not_exceed_the_exact_defect(t):
    """D_e(t) >= nu_e t - a_e_true t^2 must not be violated by the exact defect."""
    edge = d1_witness()
    bound = edge.nu_e() * t - edge.a_e_true() * t * t
    assert bound <= edge.exact_defect(t) + 1e-9


def test_first_order_slope_matches_nu_e():
    """D_e(t)/t -> nu_e as t -> 0. Ties the projected definition to observable behaviour."""
    edge = d1_witness()
    small = 1e-5
    assert edge.exact_defect(small) / small == pytest.approx(edge.nu_e(), rel=1e-3)




def test_engine_declares_its_host_as_an_import():
    """The finite complex host is supplied by numpy, not derived. No tensor product is
    constructed anywhere in the estate's Lean tree; this engine does not pretend otherwise."""
    edge = BipartiteEdge(
        hamiltonian=np.kron(SIGMA_Z, SIGMA_Y) + np.kron(SIGMA_X, I2),
        rho0=np.diag([1.0, 0.0, 0.0, 0.0]).astype(complex),
    )
    assert edge.hamiltonian.shape == (4, 4)
    assert edge.nu_e() >= 0.0




def test_solve_phi1_dual_witness():
    from omega_engine.crates.functional.phi import solve_phi1_dual_witness

    vertices = [0, 1, 2]
    edges = [(0, 1), (1, 2), (0, 2)]
    cochain = np.array([2.0, 4.0, 6.0])

    res = solve_phi1_dual_witness(vertices, edges, cochain)
    assert res["is_certified"] is True
    assert res["duality_gap"] < 1e-5
    assert res["min_l1"] == pytest.approx(0.0, abs=1e-5)




@pytest.mark.parametrize("t", [0.02, 0.05, 0.1])
def test_bar_a_e_corrected_bound_holds(t):
    """The bound must use the RIGOROUS coefficient; the 20-point sample is not one."""
    edge = d1_witness()
    sampled, rigorous = edge.bar_a_e_interval(t)
    assert sampled <= rigorous
    bound = edge.nu_e() * t - rigorous * (t * t)
    assert bound <= edge.exact_defect(t) + 1e-9




def test_gleason_d2_falsifier():
    from omega_engine.crates.quantum_physics.bipartite_retraction import gleason_d2_falsifier_check

    r = gleason_d2_falsifier_check()
    assert r["gleason_applies_at_d2"] is False
    assert r["status"] == "GLEASON_UNIQUENESS_FALSIFIED_AT_D2"
    assert r["is_a_frame_function"] is True
    assert r["is_non_born"] is True




def test_composition_sandbox_cartesian_vs_tensor():
    from omega_engine.crates.quantum_physics.composition_sandbox import (
        CartesianCompositionSandbox,
        FiniteGraphCarrier,
    )

    ca = FiniteGraphCarrier(vertices=[0, 1], edges=[(0, 1)])
    cb = FiniteGraphCarrier(vertices=[0, 1], edges=[(0, 1)])
    sandbox = CartesianCompositionSandbox(ca, cb)

    psi_a = np.array([1.0, 0.0])
    psi_b = np.array([0.0, 1.0])
    rho_sep = np.outer(np.kron(psi_a, psi_b), np.kron(psi_a, psi_b).conj())
    res_sep = sandbox.evaluate_local_tomography_contract(rho_sep)
    assert res_sep["is_separable"] is True
    assert res_sep["can_represent_in_cartesian"] is True

    psi_bell = (np.array([1.0, 0.0, 0.0, 1.0])) / np.sqrt(2.0)
    rho_bell = np.outer(psi_bell, psi_bell.conj())
    res_bell = sandbox.evaluate_local_tomography_contract(rho_bell)
    assert res_bell["is_separable"] is False
    assert res_bell["can_represent_in_cartesian"] is False
    assert res_bell["status"] == "TENSOR_PRODUCT_NOT_DERIVED"




def test_import_necessity_countermodels():
    from omega_engine.crates.pipeline.import_ledger import (
        RecoveryImportSlot,
        generate_b8_countermodels,
        verify_drop_one_necessity,
    )

    cms = generate_b8_countermodels()
    assert len(cms) == 8
    assert RecoveryImportSlot.NONCOMM in cms
    assert RecoveryImportSlot.BUNDLE_U1_LT in cms

    for slot, cm in cms.items():
        assert cm.recovery_discharged is False
        assert cm.authority_effect == "None"

    verification = verify_drop_one_necessity()
    assert verification["all_drop_one_break_recovery"] is True
    assert verification["status"] == "DROP_ONE_NECESSITY_VERIFIED"




def test_sealed_matrix_recovery_suite():
    from omega_engine.crates.quantum_physics.primitives import SIGMA_X, SIGMA_Z
    from omega_engine.crates.linear_algebra_theory.sealed_matrix_recovery import (
        FiniteMatrixRecoveryEngine,
    )

    engine = FiniteMatrixRecoveryEngine(dim=2)

    psi = np.array([1.0, 0.0], dtype=complex)
    h_op = (SIGMA_X + 0.5 * SIGMA_Z).astype(complex)

    res = engine.evaluate_full_recovery_suite(psi, h_op)
    assert res["n_targets"] == 17
    assert res["discharged_count"] == 17
    assert res["all_discharged"] is True
    assert res["sealed_recovery_closed"] is True
    assert res["authority_effect"] == "None"


def test_qam_001_covariant_wigner_yanase_monotonicity():
    """Narrowed TWICE 2026-08-04: the hypothesis is COVARIANCE, not unitality.

    The observable must be the one the channel is covariant for. z-dephasing is
    Z-covariant, not X-covariant, so H = Z here.
    """
    from omega_engine.crates.quantum_physics.primitives import SIGMA_X, SIGMA_Z
    from omega_engine.crates.quantum_physics.cptp_channel import (
        is_covariant,
        is_unital,
        solve_covariant_wigner_yanase_monotonicity,
    )

    rho = 0.5 * (np.eye(2, dtype=complex) + 0.7 * SIGMA_X + 0.3 * SIGMA_Z)
    H = SIGMA_Z.astype(complex)

    p = 0.3
    kraus_ops = [np.sqrt(1.0 - p) * np.eye(2, dtype=complex), np.sqrt(p) * SIGMA_Z]
    assert is_unital(kraus_ops) is True
    assert is_covariant(kraus_ops, SIGMA_Z.astype(complex)) is True

    res = solve_covariant_wigner_yanase_monotonicity(rho, kraus_ops, H)
    assert res["hypotheses_hold"] is True
    assert res["inequality_observed"] is True
    assert res["status"] == "COVARIANT_WIGNER_YANASE_MONOTONICITY_VERIFIED"
    assert res["delta_i"] >= -1e-9









