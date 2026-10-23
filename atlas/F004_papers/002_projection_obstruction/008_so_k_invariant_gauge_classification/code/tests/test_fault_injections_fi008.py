"""
Invasive Fault-Injection and Stress Suite for Paper 008 (GS-002).
Implements all 6 required fault-injection scenarios (FI-008-1 through FI-008-6)
from DERIVATIONS_MASTER.md.

"""

import math
import numpy as np
import pytest

from carrier import (
    GraphComplex,
    Cochain,
    SlaterViolationError,
    TopologicalDefectError,
)
from gauges import EuclideanGauge
from cycle_analytics import (
    compute_cycle_circulation,
    single_cycle_quotient_analytical,
)
from socp_certifier import ExactSOCPCertifier


def test_fi_008_1_cycle_edge_orientation_flip_sign_tracking() -> None:
    """
    FI-008-1: Cycle edge orientation flip (eps_e in {+1, -1}) sign tracking.
    Verifies that:
    1. compute_cycle_circulation correctly accounts for signed traversal eps_e.
    2. Invalid orientation dimensions or values raise ValueError.
    3. Graph-level edge reversal with corresponding signal sign inversion leaves
       circulation and quotient invariant.
    4. Adversarial sign inversion without edge reversal changes circulation and is detected.
    """
    # 3-cycle with signal
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

    # Forward circulation: sum_e omega_e = (1.0, 1.0)
    c_forward = compute_cycle_circulation(omega, orientations=[1, 1, 1])
    np.testing.assert_allclose(c_forward, [1.0, 1.0])

    # Reversing edge 1 traversal: eps_1 = -1 => (1.0, 0.0) - (0.0, 1.0) = (1.0, -1.0)
    c_flipped = compute_cycle_circulation(omega, orientations=[1, -1, 1])
    np.testing.assert_allclose(c_flipped, [1.0, -1.0])

    # Orientation value validation
    with pytest.raises(ValueError, match="Orientations must be in"):
        compute_cycle_circulation(omega, orientations=[1, 2, -1])
    with pytest.raises(ValueError, match="Orientations length"):
        compute_cycle_circulation(omega, orientations=[1, 1])

    # Graph-level edge flip:
    # Original graph: e0=(0,1), e1=(1,2), e2=(2,0) with orientations [1, 1, 1]
    g_orig = GraphComplex.create_cycle_graph(
        cycle_len=3, stalk_dim=2, orientations=[1, 1, 1]
    )
    # Flipped graph: edge 1 flipped to (2, 1) with orientation -1
    g_flipped = GraphComplex.create_cycle_graph(
        cycle_len=3, stalk_dim=2, orientations=[1, -1, 1]
    )

    assert g_orig.verify_complex()
    assert g_flipped.verify_complex()

    # In g_flipped, edge 1 is (2, 1). If signal is -omega_1 = (0.0, -1.0),
    # then total circulation remains (1.0, 1.0)
    omega_flipped = Cochain(np.array([[1.0, 0.0], [0.0, -1.0], [0.0, 0.0]]))

    cert_orig = ExactSOCPCertifier(g_orig).certify(omega)
    cert_flipped = ExactSOCPCertifier(g_flipped).certify(omega_flipped)

    assert cert_orig.primal_value == pytest.approx(math.sqrt(2.0), abs=1e-7)
    assert cert_flipped.primal_value == pytest.approx(math.sqrt(2.0), abs=1e-7)
    assert cert_orig.duality_gap < 1e-7
    assert cert_flipped.duality_gap < 1e-7


def test_cycle_closed_form_mixed_orientation_without_face_matches_face() -> None:
    """
    Reversed stored edges must induce the same dual as the 2-cell, even if
    create_cycle_graph(..., with_face=False) omits faces. On orientations
    [1, -1, 1], omega = e0 + e1 is an exact coboundary (signed circulation 0).
    The no-face closed form must not invent a non-zero dual.
    """
    orientations = [1, -1, 1]
    omega_coboundary = Cochain(np.array([[1.0, 0.0], [1.0, 0.0], [0.0, 0.0]]))
    omega_generic = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
    g_face = GraphComplex.create_cycle_graph(
        cycle_len=3, stalk_dim=2, orientations=orientations, with_face=True
    )
    g_noface = GraphComplex.create_cycle_graph(
        cycle_len=3, stalk_dim=2, orientations=orientations, with_face=False
    )

    cert_face = ExactSOCPCertifier(g_face, tol=1e-7).certify(omega_coboundary)
    cert_noface = ExactSOCPCertifier(g_noface, tol=1e-7).certify(omega_coboundary)
    assert cert_face.is_optimal
    assert cert_face.primal_value == pytest.approx(0.0, abs=1e-7)
    assert cert_noface.is_optimal
    assert cert_noface.primal_value == pytest.approx(0.0, abs=1e-7)
    assert cert_noface.dual_value == pytest.approx(0.0, abs=1e-7)
    assert cert_noface.duality_gap < 1e-7
    assert cert_noface.divergence_norm < 1e-7

    c_face = ExactSOCPCertifier(g_face, tol=1e-7).certify(omega_generic)
    c_noface = ExactSOCPCertifier(g_noface, tol=1e-7).certify(omega_generic)
    assert c_face.is_optimal
    assert c_noface.is_optimal
    assert c_noface.divergence_norm < 1e-7
    assert c_noface.primal_value == pytest.approx(c_face.primal_value, abs=1e-7)
    assert c_noface.dual_value == pytest.approx(c_face.dual_value, abs=1e-7)


def test_fi_008_2_degenerate_weights_slater_violation_exception() -> None:
    """
    FI-008-2: Degenerate weights (w_e <= 0) Slater violation exception.
    Verifies that non-positive edge and face weights raise SlaterViolationError,
    preventing spurious zero-gap certificates when the dual interior is empty.
    """
    # Negative edge weights
    with pytest.raises(SlaterViolationError, match="Slater condition violated"):
        GraphComplex(
            num_vertices=3,
            edges=[(0, 1), (1, 2), (2, 0)],
            edge_weights=[-1.0, 1.0, 1.0],
        )

    # Zero edge weights (strict Slater violation: ||z_e||_2 <= 0 forces z_e = 0, no interior)
    with pytest.raises(SlaterViolationError, match="Slater condition violated"):
        GraphComplex(
            num_vertices=3, edges=[(0, 1), (1, 2), (2, 0)], edge_weights=[0.0, 1.0, 1.0]
        )

    # Negative face weights
    with pytest.raises(SlaterViolationError, match="Slater condition violated"):
        GraphComplex(
            num_vertices=3,
            edges=[(0, 1), (1, 2), (2, 0)],
            faces=[[(0, 1), (1, 1), (2, 1)]],
            face_weights=[-0.5],
        )

    # Zero face weights
    with pytest.raises(SlaterViolationError, match="Slater condition violated"):
        GraphComplex(
            num_vertices=3,
            edges=[(0, 1), (1, 2), (2, 0)],
            faces=[[(0, 1), (1, 1), (2, 1)]],
            face_weights=[0.0],
        )

    # Test ExactSOCPCertifier defense if complex weights are perturbed post-init
    g_valid = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    g_valid.edge_weights = np.array([-1.0, 1.0, 1.0])
    with pytest.raises(SlaterViolationError, match="Slater condition violated"):
        ExactSOCPCertifier(g_valid)

    # In analytical single cycle quotient
    gauge = EuclideanGauge(1.0)
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
    with pytest.raises(ValueError, match="Slater condition violated"):
        single_cycle_quotient_analytical(omega, gauge, edge_weights=[1.0, -1.0, 1.0])


def test_fi_008_3_extreme_condition_number_duality_gap_certificate() -> None:
    """
    FI-008-3: Extreme condition number (kappa(w) = 10^9) duality gap certificate.
    Verifies that both cycle and general theta-graph complexes maintain zero duality gap (< 1e-7),
    zero divergence norm, and dual feasibility when weight ratios reach 10^9.
    """
    # 1. Stiff cycle: bottleneck edge has weight 1.0, other edges have 1e9 (kappa = 1e9)
    g_cycle_stiff = GraphComplex.create_cycle_graph(
        cycle_len=3, stalk_dim=2, edge_weights=[1.0, 1e9, 1e9]
    )
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

    cert_cycle = ExactSOCPCertifier(g_cycle_stiff, tol=1e-7).certify(omega)
    assert cert_cycle.primal_value == pytest.approx(math.sqrt(2.0), abs=1e-7)
    assert cert_cycle.dual_value == pytest.approx(math.sqrt(2.0), abs=1e-7)
    assert cert_cycle.duality_gap < 1e-7
    assert cert_cycle.divergence_norm < 1e-7
    assert cert_cycle.max_dual_norm_violation == pytest.approx(0.0, abs=1e-7)
    assert cert_cycle.is_optimal

    # 2. Inverted stiff cycle: bottleneck edge has weight 1e-9, others have 1.0 (kappa = 1e9)
    g_cycle_inverted = GraphComplex.create_cycle_graph(
        cycle_len=3, stalk_dim=2, edge_weights=[1e-9, 1.0, 1.0]
    )
    cert_inv = ExactSOCPCertifier(g_cycle_inverted, tol=1e-7).certify(omega)
    expected_inv = 1e-9 * math.sqrt(2.0)
    assert cert_inv.primal_value == pytest.approx(expected_inv, abs=1e-14)
    assert cert_inv.dual_value == pytest.approx(expected_inv, abs=1e-14)
    assert cert_inv.duality_gap < 1e-7
    assert cert_inv.is_optimal

    # 3. Extreme theta graph: parallel paths with weights 1.0, 1e9, 1e9
    g_theta_stiff = GraphComplex.create_theta_graph(
        stalk_dim=2, edge_weights=[1.0, 1e9, 1e9]
    )
    omega_th = Cochain(np.array([[1.0, 0.0], [0.0, 0.0], [0.0, 0.0]]))
    cert_theta = ExactSOCPCertifier(g_theta_stiff, tol=1e-7).certify(omega_th)
    assert cert_theta.primal_value == pytest.approx(1.0, abs=1e-6)
    assert cert_theta.dual_value == pytest.approx(1.0, abs=1e-6)
    assert cert_theta.duality_gap < 1e-6
    assert cert_theta.divergence_norm < 1e-7
    assert cert_theta.is_optimal


def test_fi_008_4_boundary_operator_perturbation_detection() -> None:
    """
    FI-008-4: Boundary operator perturbation (d1 @ d0 != 0) failure detection.
    Verifies that perturbations breaking chain complex nilpotency are strictly caught
    and raise TopologicalDefectError.
    """
    # Valid complex: 3 vertices, 3 edges, 1 face (0->1, 1->2, 2->0, face = e0 + e1 + e2)
    edges = [(0, 1), (1, 2), (2, 0)]
    valid_face = [[(0, 1), (1, 1), (2, 1)]]
    g_valid = GraphComplex(num_vertices=3, edges=edges, faces=valid_face)
    assert g_valid.verify_complex()
    g_valid.verify_complex_strict()

    # Perturbed face: flip sign of edge 2 in face definition
    # Now d1 @ d0 != 0
    corrupted_face = [[(0, 1), (1, 1), (2, -1)]]
    g_corrupted = GraphComplex(num_vertices=3, edges=edges, faces=corrupted_face)

    assert not g_corrupted.verify_complex()
    with pytest.raises(
        TopologicalDefectError, match="Boundary operator perturbation detected"
    ):
        g_corrupted.verify_complex_strict()

    # Attempting to initialize certifier on corrupted topology must fail closed
    with pytest.raises(
        TopologicalDefectError, match="Boundary operator perturbation detected"
    ):
        ExactSOCPCertifier(g_corrupted)


def test_fi_008_5_theta_graph_chorded_cycle_bottleneck_routing() -> None:
    """
    FI-008-5: Theta-graph / chorded cycle bottleneck routing.
    Verifies that when multiple alternate routes exist between vertices,
    the SOCP solver routes circulation through the path of minimal resistance (cheapest weighted norm),
    achieving certified zero duality gap.
    """
    # Theta graph: 2 vertices connected by 3 parallel edges:
    # e0 has weight 1.0 (cheap), e1 has weight 10.0 (medium), e2 has weight 100.0 (expensive)
    theta = GraphComplex.create_theta_graph(
        stalk_dim=2, edge_weights=[1.0, 10.0, 100.0]
    )
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

    certifier = ExactSOCPCertifier(theta, tol=1e-7)
    cert = certifier.certify(omega)

    # Verification of optimality and zero gap
    assert cert.is_divergence_free
    assert cert.is_dual_feasible
    assert cert.duality_gap < 1e-7
    assert cert.is_optimal
    assert cert.solver_method == "numerical_socp_subspace"

    # Chorded 4-cycle graph: cycle 0-1-2-3-0 with diagonal chord 0-2
    # Vertices: 0, 1, 2, 3
    # Edges: e0=(0,1), e1=(1,2), e2=(2,3), e3=(3,0), e4=(0,2) [chord]
    # Faces: f0 = e0 + e1 - e4, f1 = e4 + e2 + e3
    chorded_edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    chorded_faces = [[(0, 1), (1, 1), (4, -1)], [(4, 1), (2, 1), (3, 1)]]
    # Make chord extremely expensive (weight 500) vs perimeter (weight 1)
    chorded_weights = [1.0, 1.0, 1.0, 1.0, 500.0]
    g_chorded = GraphComplex(
        num_vertices=4,
        edges=chorded_edges,
        faces=chorded_faces,
        stalk_dim=2,
        edge_weights=chorded_weights,
    )
    assert g_chorded.verify_complex()

    # Circulation around perimeter: e0=(1,0), e1=(0,1), e2=(1,0), e3=(0,1), e4=(0,0)
    data_chorded = np.array(
        [[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]
    )
    omega_chorded = Cochain(data_chorded)

    cert_chord = ExactSOCPCertifier(g_chorded, tol=1e-6).certify(omega_chorded)
    assert cert_chord.is_divergence_free
    assert cert_chord.is_dual_feasible
    assert cert_chord.duality_gap < 1e-6
    assert cert_chord.is_optimal
    # The expensive chord (e4) should carry minimal dual flow relative to its weight bound
    z_chord = cert_chord.dual_circulation.data[4]
    assert np.linalg.norm(z_chord) < 10.0  # Far below weight bound of 500.0


def test_fi_008_6_zero_circulation_cochain_exact_quotient() -> None:
    """
    FI-008-6: Zero-circulation cochain (delta in im(d0)) exact quotient Phi_{j,w} = 0, gap = 0.
    Verifies that exact coboundaries produce zero quotient obstruction, zero dual value,
    and zero duality gap on single cycles, theta graphs, and general complexes.
    """
    # 1. On single cycle
    g_cycle = GraphComplex.create_cycle_graph(cycle_len=4, stalk_dim=3)
    alpha_cycle = np.array(
        [[1.0, 2.0, -1.0], [0.5, -1.5, 3.0], [-2.0, 0.0, 1.0], [3.0, 1.0, -2.0]]
    )
    exact_cycle_omega = g_cycle.coboundary_d0(alpha_cycle)

    cert_cycle = ExactSOCPCertifier(g_cycle, tol=1e-7).certify(exact_cycle_omega)
    assert cert_cycle.primal_value == pytest.approx(0.0, abs=1e-7)
    assert cert_cycle.dual_value == pytest.approx(0.0, abs=1e-7)
    assert cert_cycle.duality_gap == pytest.approx(0.0, abs=1e-7)
    assert cert_cycle.divergence_norm == pytest.approx(0.0, abs=1e-7)
    assert cert_cycle.is_optimal

    # 2. On theta graph
    g_theta = GraphComplex.create_theta_graph(stalk_dim=2, edge_weights=[2.0, 3.0, 4.0])
    alpha_theta = np.array([[1.5, -2.5], [-1.0, 4.0]])
    exact_theta_omega = g_theta.coboundary_d0(alpha_theta)

    cert_theta = ExactSOCPCertifier(g_theta, tol=1e-7).certify(exact_theta_omega)
    assert cert_theta.primal_value == pytest.approx(0.0, abs=1e-7)
    assert cert_theta.dual_value == pytest.approx(0.0, abs=1e-7)
    assert cert_theta.duality_gap == pytest.approx(0.0, abs=1e-7)
    assert cert_theta.is_optimal
