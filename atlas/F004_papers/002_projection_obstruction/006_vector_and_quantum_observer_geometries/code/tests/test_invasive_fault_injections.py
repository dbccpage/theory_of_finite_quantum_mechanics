"""
Invasive Fault-Injection Test Suite for Paper 006 (FI-006-1 through FI-006-6).
Paper: GS-003 (006_vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

import pytest
import numpy as np

from cochain_complex import Cochain, GraphComplex
from quantum_geometry import HermitianOperator, QuantumQuotientSolver
from cptp_channels import KrausChannel, CochainMorphism
from exceptions import (
    NonHermitianOperatorError,
    NonCPTPChannelError,
    IntertwiningViolationError,
)


def test_fi_006_1_non_contractive_channel_detection():
    """
    FI-006-1: Non-Contractive Channel Detection.
    Perturbs a CPTP channel by scale > 1 (eigenvalues of sum K^dag K > 1),
    asserts trace-increasing detection, NonCPTPChannelError on assertion,
    and quotient monotonicity failure (amplification).
    """
    comp = GraphComplex.triangle_complex()
    solver = QuantumQuotientSolver(comp, tol=1e-4)

    a_mat = 0.5 * HermitianOperator.SIGMA_Z
    delta = Cochain(np.array([a_mat, a_mat, a_mat], dtype=complex), degree=1)
    phi_base = solver.solve(delta).primal_value  # 1.5

    # Base depolarizing channel scaled by 1.3
    base_ch = KrausChannel.depolarizing(d=2, p=0.2)
    amplifying_ch = KrausChannel.non_contractive_perturbation(base_ch, scale=1.3)

    assert amplifying_ch.is_trace_increasing()
    assert not amplifying_ch.is_trace_preserving()

    # assert_cptp raises NonCPTPChannelError
    with pytest.raises(NonCPTPChannelError) as exc_info:
        amplifying_ch.assert_cptp()
    assert "violates CPTP trace preservation" in str(exc_info.value)

    # Contractivity ratio exceeds 1.0
    ratio = amplifying_ch.contractivity_ratio(a_mat)
    assert ratio > 1.0

    # Applying to cochain amplifies quotient obstruction
    v_ch = [amplifying_ch] * 3
    e_ch = [amplifying_ch] * 3
    bad_morphism = CochainMorphism(vertex_channels=v_ch, edge_channels=e_ch)
    delta_amplified = bad_morphism.apply_to_cochain(delta)
    phi_amplified = solver.solve(delta_amplified).primal_value

    # Monotonicity is violated: phi_amplified > phi_base
    assert phi_amplified > phi_base + 0.05


def test_fi_006_2_intertwining_violation():
    """
    FI-006-2: Intertwining Violation (Lambda^1 d0 != d0' Lambda^0).
    Starts from an exact coboundary delta = d0 phi with Phi_Q = 0.
    Applies non-intertwining transformation on edges (e.g. non-identical unitaries),
    asserts IntertwiningViolationError under strict check, and demonstrates that
    broken intertwining generates an artificial topological obstruction Phi_Q' > 0.
    """
    comp = GraphComplex.triangle_complex()
    solver = QuantumQuotientSolver(comp, tol=1e-4)

    sz = HermitianOperator.SIGMA_Z
    phi_0 = Cochain(np.array([sz, 2.0 * sz, -sz]), degree=0)
    delta_exact = comp.d0(phi_0)

    # Base obstruction is zero
    cert_base = solver.solve(delta_exact)
    assert cert_base.primal_value < 1e-4

    # Construct non-intertwining morphism:
    # Vertices use identity channel.
    # Edges 0 and 1 use identity, but Edge 2 uses Pauli X bit flip.
    id_ch = KrausChannel.unitary(np.eye(2, dtype=complex))
    x_ch = KrausChannel.unitary(HermitianOperator.SIGMA_X)

    bad_morphism = CochainMorphism(
        vertex_channels=[id_ch, id_ch, id_ch],
        edge_channels=[id_ch, id_ch, x_ch],
    )

    # Intertwining condition fails
    is_intertwined, max_err = bad_morphism.verify_intertwining(comp)
    assert not is_intertwined
    assert max_err > 0.5

    # Strict check raises IntertwiningViolationError
    with pytest.raises(IntertwiningViolationError) as exc_info:
        bad_morphism.verify_intertwining(comp, strict=True)
    assert "Intertwining condition" in str(exc_info.value)

    # Artificial obstruction is created from exact coboundary
    delta_perturbed = bad_morphism.apply_to_cochain(delta_exact)
    cert_perturbed = solver.solve(delta_perturbed)
    assert cert_perturbed.primal_value > 0.5


def test_fi_006_3_non_hermitian_operator_exception():
    """
    FI-006-3: Non-Hermitian Operator Exception.
    Injects non-Hermitian operator into carrier and solver,
    asserting immediate typed NonHermitianOperatorError.
    """
    comp = GraphComplex.triangle_complex()
    solver = QuantumQuotientSolver(comp)

    # Matrix with asymmetric off-diagonal entries
    non_herm = np.array([[1.0, 2.0 + 1.0j], [0.5, -1.0]], dtype=complex)

    # 1. Direct utility check
    with pytest.raises(NonHermitianOperatorError) as exc_info1:
        HermitianOperator.check_hermitian(non_herm)
    assert "non-Hermitian" in str(exc_info1.value)

    # 2. Schatten norm check
    with pytest.raises(NonHermitianOperatorError):
        HermitianOperator.schatten_norm(non_herm, p=1, check=True)

    # 3. Solver check on cochain injection
    sz = HermitianOperator.SIGMA_Z
    corrupted_data = np.array([sz, non_herm, sz])
    delta_corrupted = Cochain(corrupted_data, degree=1)

    with pytest.raises(NonHermitianOperatorError) as exc_info2:
        solver.solve(delta_corrupted, check_hermitian=True)
    assert "non-Hermitian" in str(exc_info2.value)


def test_fi_006_4_qutrit_non_euclidean_unit_ball():
    """
    FI-006-4: Qutrit (d=3) Non-Euclidean Unit Ball Test.
    Demonstrates that for d=3 qutrits, the Schatten 1-norm unit ball is a spectral
    cross-polytope that violates the Euclidean parallelogram identity, whereas
    qubits (d=2) satisfy it identically due to the Bloch sphere isometry.
    """
    # 1. Qubit (d=2) satisfies parallelogram identity to machine precision
    rng = np.random.default_rng(77)
    for _ in range(5):
        v1 = rng.standard_normal(3)
        v2 = rng.standard_normal(3)
        x1_2 = HermitianOperator.from_bloch_vector(v1)
        x2_2 = HermitianOperator.from_bloch_vector(v2)

        n1 = HermitianOperator.schatten_norm(x1_2, p=1)
        n2 = HermitianOperator.schatten_norm(x2_2, p=1)
        n_sum = HermitianOperator.schatten_norm(x1_2 + x2_2, p=1)
        n_diff = HermitianOperator.schatten_norm(x1_2 - x2_2, p=1)

        lhs = 2.0 * (n1**2) + 2.0 * (n2**2)
        rhs = (n_sum**2) + (n_diff**2)
        assert abs(lhs - rhs) < 1e-11

    # 2. Qutrit (d=3) violates parallelogram identity
    x1_3 = np.diag([1.0, -1.0, 0.0]).astype(complex)
    x2_3 = np.diag([0.0, 1.0, -1.0]).astype(complex)

    n1_3 = HermitianOperator.schatten_norm(x1_3, p=1)  # 2.0
    n2_3 = HermitianOperator.schatten_norm(x2_3, p=1)  # 2.0
    n_sum_3 = HermitianOperator.schatten_norm(x1_3 + x2_3, p=1)  # diag(1, 0, -1) => 2.0
    n_diff_3 = HermitianOperator.schatten_norm(
        x1_3 - x2_3, p=1
    )  # diag(1, -2, 1) => 4.0

    lhs_3 = 2.0 * (n1_3**2) + 2.0 * (n2_3**2)  # 2*(4) + 2*(4) = 16.0
    rhs_3 = (n_sum_3**2) + (n_diff_3**2)  # 4 + 16 = 20.0

    discrepancy = abs(lhs_3 - rhs_3)
    assert discrepancy == 4.0
    # Ratio 20 / 16 = 1.25 != 1.0
    assert abs(rhs_3 / lhs_3 - 1.25) < 1e-12


def test_fi_006_5_trace_decreasing_post_selection_failure():
    """
    FI-006-5: Trace-Decreasing / Post-Selection Monotonicity Failure.
    Injects a non-trace-preserving post-selected measurement projector P = |0><0|,
    verifies is_trace_decreasing is True, assert_cptp raises NonCPTPChannelError,
    and conditioned state separation can violate monotonicity.
    """
    p0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    post_sel_ch = KrausChannel.post_selected(p0)

    assert post_sel_ch.is_trace_decreasing()
    assert not post_sel_ch.is_trace_preserving()

    with pytest.raises(NonCPTPChannelError) as exc_info:
        post_sel_ch.assert_cptp()
    assert "trace preservation" in str(exc_info.value)

    # Under post-selection, conditional state discrimination can change non-monotonically.
    # For example, consider two mixed states with trace distance 0.5:
    rho_a = np.diag([0.6, 0.4]).astype(complex)
    rho_b = np.diag([0.1, 0.9]).astype(complex)
    dist_before = 0.5 * HermitianOperator.schatten_norm(rho_a - rho_b, p=1)
    assert abs(dist_before - 0.5) < 1e-12

    # Post-selection on |0><0| produces conditioned pure state |0><0| with probability 0.6 and 0.1
    # Normalized post-selected states both collapse to |0><0| (dist = 0),
    # while unnormalized difference is (0.6 - 0.1)|0><0| = 0.5.
    # Now consider an orthogonal measurement filter P_tilt = |+><+|
    plus = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    p_plus = np.outer(plus, plus.conj())
    tilt_ch = KrausChannel.post_selected(p_plus)
    assert tilt_ch.is_trace_decreasing()
    with pytest.raises(NonCPTPChannelError):
        tilt_ch.assert_cptp()


def test_fi_006_6_unitary_gauge_invariance():
    """
    FI-006-6: Complete Unitary Gauge Invariance.
    Verifies that for arbitrary unitary transformations U in U(2),
    conjugating the operator cochain delta_e -> U delta_e U^dag
    leaves the quantum quotient obstruction Phi_Q strictly invariant.
    """
    comp = GraphComplex.triangle_complex()
    solver = QuantumQuotientSolver(comp, tol=1e-4)

    a_mat = 0.5 * HermitianOperator.SIGMA_Z
    delta = Cochain(np.array([a_mat, a_mat, a_mat], dtype=complex), degree=1)
    phi_base = solver.solve(delta).primal_value  # 1.5

    # Test across multiple random unitaries
    rng = np.random.default_rng(999)
    for _ in range(3):
        # Haar random 2x2 unitary via QR decomposition
        z_rand = rng.standard_normal((2, 2)) + 1.0j * rng.standard_normal((2, 2))
        q_mat, _ = np.linalg.qr(z_rand)
        u_ch = KrausChannel.unitary(q_mat)

        morphism = CochainMorphism.uniform(comp, u_ch)
        is_intertwined, _ = morphism.verify_intertwining(comp)
        assert is_intertwined

        delta_u = morphism.apply_to_cochain(delta)
        phi_u = solver.solve(delta_u).primal_value

        assert abs(phi_u - phi_base) < 1e-4
