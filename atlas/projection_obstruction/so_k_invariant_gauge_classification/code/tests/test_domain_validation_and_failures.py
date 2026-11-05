"""
Comprehensive Negative and Domain-Validation Test Suite for GS-002.
Verifies fail-fast rejection of invalid theorem-domain inputs (F1, F2, F4, F5, F7).
"""

from __future__ import annotations
import math
import numpy as np
import pytest

from carrier import (
    GraphComplex,
    Cochain,
    SlaterViolationError,
)
from gauges import (
    EuclideanGauge,
    CoordinateL1Gauge,
    AnisotropicGauge,
    audit_so_k_invariance,
    audit_sphere_constancy,
    make_so2_rotation,
)
from solver import MixedNormSolver, CoordinateL1Solver
from socp_certifier import (
    SOCPCertifier,
    CycleClosedFormCertifier,
    ExactSOCPCertifier,
)
from cycle_analytics import (
    compute_cycle_circulation,
    single_cycle_quotient_analytical,
    analyze_triangle_separation,
    compute_holonomy,
    apply_vertex_gauge_transformation,
)
from closure import ClosureBoundEvaluator, ClosureBoundResult


class TestCochainDomainValidation:
    """F2: Cochain rank, shape, finiteness, degree, and norm weight validation."""

    def test_invalid_rank(self) -> None:
        with pytest.raises(ValueError, match="must be 1D or 2D"):
            Cochain(np.zeros((2, 2, 2)), degree=1)

    def test_invalid_degree(self) -> None:
        with pytest.raises(ValueError, match="Degree must be 0, 1, or 2"):
            Cochain(np.zeros((2, 2)), degree=3)
        with pytest.raises(ValueError, match="Degree must be 0, 1, or 2"):
            Cochain(np.zeros((2, 2)), degree=-1)

    def test_non_finite_cochain_data(self) -> None:
        with pytest.raises(ValueError, match="must contain finite real numbers"):
            Cochain(np.array([[1.0, np.nan], [0.0, 1.0]]))
        with pytest.raises(ValueError, match="must contain finite real numbers"):
            Cochain(np.array([[1.0, np.inf], [0.0, 1.0]]))

    def test_coordinate_l1_norm_weight_length_validation(self) -> None:
        """F2 finding: Cochain.coordinate_l1_l1_norm(weights=[2]) must reject 1 weight on 3 cells."""
        c = Cochain(np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]))
        assert c.num_cells == 3
        with pytest.raises(ValueError, match="Weights length"):
            c.coordinate_l1_l1_norm(weights=[2.0])

    def test_coordinate_l1_norm_non_finite_and_negative_weights(self) -> None:
        c = Cochain(np.array([[1.0, 2.0], [3.0, 4.0]]))
        with pytest.raises(ValueError, match="finite"):
            c.coordinate_l1_l1_norm(weights=[1.0, np.nan])
        with pytest.raises(ValueError, match="strictly positive"):
            c.coordinate_l1_l1_norm(weights=[1.0, -0.5])
        with pytest.raises(ValueError, match="strictly positive"):
            c.coordinate_l1_l1_norm(weights=[1.0, 0.0])

    def test_mixed_norm_weight_validation(self) -> None:
        c = Cochain(np.array([[1.0, 2.0], [3.0, 4.0]]))
        with pytest.raises(ValueError, match="Weights length"):
            c.mixed_l1_l2_norm(weights=[1.0])
        with pytest.raises(ValueError, match="finite"):
            c.mixed_l1_l2_norm(weights=[1.0, np.inf])
        with pytest.raises(ValueError, match="strictly positive"):
            c.mixed_l1_l2_norm(weights=[1.0, -1.0])


class TestGraphComplexDomainValidation:
    """F2: Fail-fast validation of vertex count, stalk dimension, edge endpoints, and face signs."""

    def test_invalid_num_vertices_and_stalk_dim(self) -> None:
        with pytest.raises(ValueError, match="num_vertices must be integer >= 1"):
            GraphComplex(num_vertices=0, edges=[])
        with pytest.raises(ValueError, match="stalk_dim must be integer >= 1"):
            GraphComplex(num_vertices=2, edges=[(0, 1)], stalk_dim=0)

    def test_invalid_edge_endpoints_at_construction(self) -> None:
        """F2 finding: GraphComplex must reject out-of-bounds endpoints at construction."""
        # Out of bounds vertex index (u >= V)
        with pytest.raises(ValueError, match="out of bounds"):
            GraphComplex(num_vertices=3, edges=[(0, 1), (1, 3)])
        # Negative vertex index
        with pytest.raises(ValueError, match="out of bounds"):
            GraphComplex(num_vertices=3, edges=[(0, -1)])
        # Self loop
        with pytest.raises(ValueError, match="self-loop"):
            GraphComplex(num_vertices=3, edges=[(1, 1)])

    def test_invalid_edge_weights(self) -> None:
        with pytest.raises(ValueError, match="Edge weights must match"):
            GraphComplex(num_vertices=2, edges=[(0, 1)], edge_weights=[1.0, 2.0])
        with pytest.raises(ValueError, match="finite"):
            GraphComplex(num_vertices=2, edges=[(0, 1)], edge_weights=[np.nan])
        with pytest.raises(SlaterViolationError, match="strictly positive"):
            GraphComplex(num_vertices=2, edges=[(0, 1)], edge_weights=[-1.0])

    def test_invalid_face_boundary_and_weights(self) -> None:
        # Nonexistent edge index in face
        with pytest.raises(ValueError, match="out-of-bounds edge index"):
            GraphComplex(num_vertices=2, edges=[(0, 1)], faces=[[(1, 1)]])
        # Invalid face orientation sign
        with pytest.raises(ValueError, match="orientation sign must be \\+1 or -1"):
            GraphComplex(num_vertices=2, edges=[(0, 1)], faces=[[(0, 2)]])
        with pytest.raises(ValueError, match="orientation sign must be \\+1 or -1"):
            GraphComplex(num_vertices=2, edges=[(0, 1)], faces=[[(0, 0)]])
        # Face weights mismatch / non-positive
        with pytest.raises(ValueError, match="Face weights must match"):
            GraphComplex(
                num_vertices=2, edges=[(0, 1)], faces=[[(0, 1)]], face_weights=[1.0, 2.0]
            )
        with pytest.raises(SlaterViolationError, match="strictly positive"):
            GraphComplex(
                num_vertices=2, edges=[(0, 1)], faces=[[(0, 1)]], face_weights=[0.0]
            )


class TestAnalyticsDomainValidation:
    """F2: Input validation on analytical routines."""

    def test_single_cycle_quotient_analytical_weight_length(self) -> None:
        """F2 finding: single_cycle_quotient_analytical(..., edge_weights=[2]) must reject 1 weight on 3 edges."""
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        gauge = EuclideanGauge(1.0)
        with pytest.raises(ValueError, match="Edge weights length"):
            single_cycle_quotient_analytical(omega, gauge, edge_weights=[2.0])

    def test_single_cycle_quotient_analytical_negative_weights(self) -> None:
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        gauge = EuclideanGauge(1.0)
        with pytest.raises(ValueError, match="strictly positive"):
            single_cycle_quotient_analytical(omega, gauge, edge_weights=[1.0, -1.0, 1.0])

    def test_analyze_triangle_separation_negative_weights(self) -> None:
        """F2 finding: analyze_triangle_separation([-1, 2, 3]) must reject negative weights."""
        with pytest.raises(ValueError, match="strictly positive"):
            analyze_triangle_separation(edge_weights=[-1.0, 2.0, 3.0])
        with pytest.raises(ValueError, match="requires exactly 3 edge weights"):
            analyze_triangle_separation(edge_weights=[1.0, 2.0])

    def test_coordinate_l1_solver_stalk_dimension_mismatch(self) -> None:
        """F2 finding: CoordinateL1Solver.solve must reject 3-coordinate cochain on stalk_dim=2 complex."""
        g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        omega_3coord = Cochain(np.array([[1.0, 0.0, 5.0], [0.0, 1.0, 5.0], [0.0, 0.0, 5.0]]))
        solver = CoordinateL1Solver(g)
        with pytest.raises(ValueError, match="does not match complex"):
            solver.solve(omega_3coord)

    def test_compute_cycle_circulation_domain_validation(self) -> None:
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        # Orientations length mismatch
        with pytest.raises(ValueError, match="Orientations length"):
            compute_cycle_circulation(omega, orientations=[1, 1])
        # Orientations value not in {-1, 1}
        with pytest.raises(ValueError, match="Orientations must be in"):
            compute_cycle_circulation(omega, orientations=[1, 0, -1])

    def test_compute_holonomy_strict_so_k_validation(self) -> None:
        """F2 finding: compute_holonomy must reject orientation=0, non-orthogonal, or det!=1."""
        rot = make_so2_rotation(0.5)

        # Orientation zero must be rejected (not treated as transpose)
        with pytest.raises(ValueError, match="Orientation sign .* must be \\+1 or -1"):
            compute_holonomy([rot], orientations=[0])

        # Orientation 2 must be rejected
        with pytest.raises(ValueError, match="Orientation sign .* must be \\+1 or -1"):
            compute_holonomy([rot], orientations=[2])

        # Non-square matrix
        with pytest.raises(ValueError, match="square 2D matrices"):
            compute_holonomy([np.ones((2, 3))])

        # Non-orthogonal matrix
        non_ortho = np.array([[2.0, 0.0], [0.0, 1.0]])
        with pytest.raises(ValueError, match="not orthogonal"):
            compute_holonomy([non_ortho])

        # Reflection matrix: det = -1 (not in SO(k))
        refl = np.array([[1.0, 0.0], [0.0, -1.0]])
        with pytest.raises(ValueError, match="must be \\+1 for SO\\(k\\)"):
            compute_holonomy([refl])

        # Dimension mismatch
        rot3 = np.eye(3)
        with pytest.raises(ValueError, match="expected \\(2, 2\\)"):
            compute_holonomy([rot, rot3])


class TestSOCPCertifierClassification:
    """F1: Certifier naming, methods, orientations, and signed weak duality gap."""

    def test_certifier_orientation_validation(self) -> None:
        """F2 finding: ExactSOCPCertifier.certify(..., orientations=[2, 1, 1]) must reject orientation 2."""
        g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        certifier = SOCPCertifier(g)

        with pytest.raises(ValueError, match="Orientations must be in"):
            certifier.certify(omega, orientations=[2, 1, 1])

    def test_signed_duality_gap_preservation(self) -> None:
        """F1 finding: certify must record signed weak-duality gap (primal - dual)."""
        g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        certifier = SOCPCertifier(g, tol=1e-7)
        cert = certifier.certify(omega)

        assert hasattr(cert, "signed_duality_gap")
        assert cert.signed_duality_gap == pytest.approx(cert.primal_value - cert.dual_value)
        assert cert.is_zero_gap is True
        assert cert.solver_method == "cycle_closed_form"

    def test_cycle_closed_form_certifier_enforces_cycle(self) -> None:
        """CycleClosedFormCertifier must reject non-cycle graph complexes."""
        theta = GraphComplex.create_theta_graph(stalk_dim=2)
        with pytest.raises(ValueError, match="requires a simple directed cycle complex"):
            CycleClosedFormCertifier(theta)

    def test_exact_socp_certifier_alias(self) -> None:
        """Verify backward-compatible alias ExactSOCPCertifier is SOCPCertifier."""
        assert ExactSOCPCertifier is SOCPCertifier
        g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        cert = ExactSOCPCertifier(g).certify(omega)
        assert cert.is_optimal

    def test_solver_method_selection(self) -> None:
        """MixedNormSolver supports method='auto', 'cycle_closed_form', 'numerical', 'smoothed_lbfgs'."""
        g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        solver = MixedNormSolver(g)

        cert_auto = solver.solve(omega, method="auto")
        assert cert_auto.solver_method == "cycle_closed_form"

        cert_num = solver.solve(omega, method="numerical")
        assert cert_num.solver_method == "numerical_socp_subspace"
        assert cert_num.is_optimal

        with pytest.raises(ValueError, match="Unknown solver method"):
            solver.solve(omega, method="nonexistent_solver")


class TestSO3NoncommutingAndGaugeConjugacy:
    """F4: Noncommuting SO(3) regression and genuine vertex gauge conjugacy."""

    def test_so3_product_order_noncommuting(self) -> None:
        """Verify that SO(3) rotations do not commute and holonomy depends on cycle traversal order."""
        # 90 degree rotation about X
        rx = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 0.0, -1.0],
            [0.0, 1.0, 0.0],
        ])
        # 90 degree rotation about Y
        ry = np.array([
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
            [-1.0, 0.0, 0.0],
        ])

        # Non-commutativity: Rx @ Ry != Ry @ Rx
        assert not np.allclose(rx @ ry, ry @ rx)

        # Cycle holonomy forward vs reversed
        h_xy = compute_holonomy([rx, ry])
        h_yx = compute_holonomy([ry, rx])
        assert not np.allclose(h_xy, h_yx)
        np.testing.assert_allclose(h_xy, ry @ rx)
        np.testing.assert_allclose(h_yx, rx @ ry)

    def test_vertex_gauge_transformation_conjugacy(self) -> None:
        """Verify that vertex gauge transformations conjugate cycle holonomy and conserve trace/eigenvalues."""
        g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        rot = make_so2_rotation(0.4)
        connections = [rot, np.eye(2), np.eye(2)]
        h_orig = compute_holonomy(connections)

        # Vertex gauges g_0, g_1, g_2
        g_v = [make_so2_rotation(0.1), make_so2_rotation(0.3), make_so2_rotation(-0.5)]
        transformed = apply_vertex_gauge_transformation(connections, g_v, g.edges)
        h_trans = compute_holonomy(transformed)

        # Holonomy conjugates by basepoint gauge g_0: H' = g_0 @ H @ g_0.T
        expected = g_v[0] @ h_orig @ g_v[0].T
        np.testing.assert_allclose(h_trans, expected, atol=1e-7)

        # Trace and eigenvalues strictly preserved
        assert np.trace(h_trans) == pytest.approx(np.trace(h_orig))
        assert np.linalg.norm(h_trans - np.eye(2)) > 0.1  # curvature preserved!


class TestClosureBoundFailClosed:
    """F5: Closure evaluation candidate vs certified values and fail-closed bound."""

    def test_closure_result_candidate_vs_certified(self) -> None:
        g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        evaluator = ClosureBoundEvaluator(g)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

        res = evaluator.evaluate(omega)
        assert isinstance(res, ClosureBoundResult)
        assert res.candidate_primal_value == pytest.approx(math.sqrt(2.0))
        assert res.certified_quotient_value == pytest.approx(math.sqrt(2.0))
        assert res.candidate_bound_holds is True
        assert res.certified_bound_holds is True
        assert res.is_bound_satisfied is True
        assert res.phi_quotient_obstruction == pytest.approx(math.sqrt(2.0))


class TestStochasticAuditorValidation:
    """F7: Sample count validation in stochastic auditors and AnisotropicGauge docstring."""

    def test_empty_sample_set_raises_error(self) -> None:
        gauge = EuclideanGauge(1.0)
        with pytest.raises(ValueError, match="num_samples must be integer >= 1"):
            audit_so_k_invariance(gauge, dim=2, num_samples=0)
        with pytest.raises(ValueError, match="num_samples must be integer >= 1"):
            audit_sphere_constancy(gauge, dim=2, num_samples=-5)

    def test_anisotropic_gauge_requires_invertible_matrix(self) -> None:
        # Non-square matrix
        with pytest.raises(ValueError, match="Matrix A must be square"):
            AnisotropicGauge(np.ones((2, 3)))
        # Singular matrix (rank deficient)
        singular = np.array([[1.0, 2.0], [2.0, 4.0]])
        with pytest.raises(ValueError, match="full column rank"):
            AnisotropicGauge(singular)


class TestResidualFailFastDefects:
    """Targeted regression tests for Section 7.6 residual fail-fast defects."""

    def test_defect_1_cochain_scalar_rejected(self) -> None:
        """Cochain(1.0) must reject scalar / rank 0 at construction."""
        with pytest.raises(ValueError, match="scalar / rank 0"):
            Cochain(1.0)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="scalar / rank 0"):
            Cochain(np.array(5.0))

    def test_defect_2_edge_weights_shaped_m_1_rejected(self) -> None:
        """Edge weights shaped (m, 1) must be rejected across all public entry points."""
        w_2d = np.array([[1.0], [2.0], [3.0]])
        # GraphComplex
        with pytest.raises(ValueError, match="exact 1D shape"):
            GraphComplex(num_vertices=3, edges=[(0, 1), (1, 2), (2, 0)], edge_weights=w_2d)

        # Cochain.mixed_l1_l2_norm
        c = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        with pytest.raises(ValueError, match="exact 1D shape"):
            c.mixed_l1_l2_norm(w_2d)

        # Cochain.coordinate_l1_l1_norm
        with pytest.raises(ValueError, match="exact 1D shape"):
            c.coordinate_l1_l1_norm(w_2d)

        # single_cycle_quotient_analytical
        gauge = EuclideanGauge(1.0)
        with pytest.raises(ValueError, match="exact 1D shape"):
            single_cycle_quotient_analytical(c, gauge, edge_weights=w_2d)

        # analyze_triangle_separation
        with pytest.raises(ValueError, match="1D shape"):
            analyze_triangle_separation(w_2d)

    def test_defect_3_fractional_face_index_rejected(self) -> None:
        """Fractional face index 0.5 must be rejected at construction."""
        with pytest.raises(ValueError, match="edge index must be an integer"):
            GraphComplex(
                num_vertices=3,
                edges=[(0, 1), (1, 2), (2, 0)],
                faces=[[(0.5, 1), (1, 1), (2, 1)]],  # type: ignore[list-item]
            )

    def test_defect_4_holonomy_fractional_orientation_rejected(self) -> None:
        """Holonomy orientation 1.5 must be rejected before conversion."""
        mats = [np.eye(2), np.eye(2)]
        with pytest.raises(ValueError, match="Orientation sign must be exactly"):
            compute_holonomy(mats, orientations=[1.5, 1])  # type: ignore[list-item]

    def test_defect_5_cycle_factory_fractional_orientation_rejected(self) -> None:
        """Cycle-factory orientation 1.5 must be rejected before conversion."""
        with pytest.raises(ValueError, match="Orientation sign must be exactly"):
            GraphComplex.create_cycle_graph(cycle_len=3, orientations=[1.5, 1, 1])  # type: ignore[list-item]

    def test_defect_6_coordinate_l1_gauge_negative_weights_rejected(self) -> None:
        """CoordinateL1Gauge with negative weights must be rejected."""
        with pytest.raises(ValueError, match="Weights must be strictly positive"):
            CoordinateL1Gauge(weights=[-1.0, 1.0])
        # Also check length mismatch at call
        g = CoordinateL1Gauge(weights=[2.0, 3.0])
        with pytest.raises(ValueError, match="Weights length.*does not match"):
            g(np.array([1.0, 2.0, 3.0]))

    def test_defect_7_euclidean_gauge_nan_scale_rejected(self) -> None:
        """EuclideanGauge with NaN or non-positive scale must be rejected."""
        with pytest.raises(ValueError, match="Scale must be strictly positive and finite"):
            EuclideanGauge(scale=float("nan"))
        with pytest.raises(ValueError, match="Scale must be strictly positive and finite"):
            EuclideanGauge(scale=-2.0)

    def test_defect_8_non_orthogonal_vertex_gauges_rejected(self) -> None:
        """Non-orthogonal vertex gauge transformations must be rejected."""
        edges = [(0, 1), (1, 2), (2, 0)]
        connections = [np.eye(2), np.eye(2), np.eye(2)]
        non_ortho_gauges = [2.0 * np.eye(2), np.eye(2), np.eye(2)]
        with pytest.raises(ValueError, match="not orthogonal"):
            apply_vertex_gauge_transformation(connections, non_ortho_gauges, edges)

    def test_defect_9_inconsistent_cycle_signs_rejected(self) -> None:
        """Inconsistent cycle signs [1, -1, 1] on triangle must be rejected as not a closed cycle."""
        tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        certifier = SOCPCertifier(tri)
        with pytest.raises(ValueError, match="do not represent a closed cycle circulation"):
            certifier.certify(omega, orientations=[1, -1, 1], method="cycle_closed_form")

    def test_defect_10_smoothed_lbfgs_certificate_fields_consistent(self) -> None:
        """method='smoothed_lbfgs' must populate solver_method='smoothed_lbfgs' and is_zero_gap consistently."""
        tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        solver = MixedNormSolver(tri)
        cert = solver.solve(omega, method="smoothed_lbfgs")
        assert cert.solver_method == "smoothed_lbfgs"
        assert isinstance(cert.is_zero_gap, bool)
        assert cert.is_zero_gap == (cert.is_optimal and cert.duality_gap <= solver.tol)

    def test_defect_11_exact_theta_coboundary_routed_to_zero_circulation(self) -> None:
        """Exact theta-graph coboundary must route to zero_circulation with zero gap."""
        theta = GraphComplex.create_theta_graph(stalk_dim=2)
        # Construct an exact coboundary omega = d0 alpha
        alpha = np.array([[1.0, 2.0], [3.0, 4.0]])
        omega = theta.coboundary_d0(alpha)

        certifier = SOCPCertifier(theta)
        cert = certifier.certify(omega, method="auto")
        assert cert.solver_method == "zero_circulation"
        assert cert.is_optimal is True
        assert cert.is_zero_gap is True
        assert cert.primal_value == pytest.approx(0.0, abs=1e-6)
        assert cert.dual_value == pytest.approx(0.0, abs=1e-6)
        assert cert.duality_gap == pytest.approx(0.0, abs=1e-6)

    def test_defect_12_socp_certifier_unknown_method_rejected(self) -> None:
        """F1/F7 finding: SOCPCertifier.certify must reject unknown method on all cochains."""
        tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        certifier = SOCPCertifier(tri)

        # On non-exact cochain
        with pytest.raises(ValueError, match="Unknown solver method 'not-a-method'"):
            certifier.certify(omega, method="not-a-method")

        # On exact coboundary
        exact_omega = tri.coboundary_d0(np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]))
        with pytest.raises(ValueError, match="Unknown solver method 'not-a-method'"):
            certifier.certify(exact_omega, method="not-a-method")

    def test_defect_13_cycle_closed_form_certifier_unknown_method_rejected(self) -> None:
        """CycleClosedFormCertifier.certify must reject unknown method."""
        tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        cycle_cert = CycleClosedFormCertifier(tri)
        with pytest.raises(ValueError, match="Unknown solver method 'not-a-method'"):
            cycle_cert.certify(omega, method="not-a-method")

    def test_defect_14_single_cycle_quotient_analytical_scalar_weight_rejected(self) -> None:
        """single_cycle_quotient_analytical must raise ValueError on scalar edge_weights."""
        c = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        gauge = EuclideanGauge(1.0)
        with pytest.raises(ValueError, match="exact 1D shape"):
            single_cycle_quotient_analytical(c, gauge, edge_weights=2.0)  # type: ignore[arg-type]

    def test_defect_15_apply_vertex_gauge_transformation_float_endpoint_rejected(self) -> None:
        """apply_vertex_gauge_transformation must reject float endpoints."""
        connections = [np.eye(2), np.eye(2), np.eye(2)]
        vertex_gauges = [np.eye(2), np.eye(2), np.eye(2)]
        with pytest.raises(ValueError, match="Edge endpoints must be integers"):
            apply_vertex_gauge_transformation(
                connections, vertex_gauges, [(0.0, 1), (1, 2), (2, 0)]  # type: ignore[list-item]
            )

    def test_defect_16_mixed_norm_solver_numerical_honors_subspace_on_exact_coboundary(self) -> None:
        """MixedNormSolver.solve with method='numerical' must honor numerical solve on exact coboundary."""
        tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        exact_omega = tri.coboundary_d0(np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]))
        solver = MixedNormSolver(tri)
        cert = solver.solve(exact_omega, method="numerical")
        assert cert.solver_method == "numerical_socp_subspace"
        assert cert.primal_value == pytest.approx(0.0, abs=1e-5)


class TestCoverageCompleteness:
    """Targeted coverage tests for remaining branches across all modules."""

    def test_gauges_edge_cases(self) -> None:
        # EuclideanGauge non-finite
        eg = EuclideanGauge(1.0)
        with pytest.raises(ValueError, match="finite real numbers"):
            eg(np.array([1.0, float("nan")]))

        # CoordinateL1Gauge non-1D weights, non-finite weights, non-finite input, call with weights
        with pytest.raises(ValueError, match="1-dimensional"):
            CoordinateL1Gauge(weights=np.ones((2, 2)))
        with pytest.raises(ValueError, match="finite real numbers"):
            CoordinateL1Gauge(weights=[1.0, float("nan")])
        cg_unweighted = CoordinateL1Gauge()
        with pytest.raises(ValueError, match="finite real numbers"):
            cg_unweighted(np.array([1.0, float("nan")]))
        cg_weighted = CoordinateL1Gauge(weights=[2.0, 3.0])
        val = cg_weighted(np.array([1.0, -2.0]))
        assert val == pytest.approx(2.0 * 1.0 + 3.0 * 2.0)

        # LpGauge edge cases
        from gauges import LpGauge
        with pytest.raises(ValueError, match="p must be a real number"):
            LpGauge(p=float("nan"))
        with pytest.raises(ValueError, match="p must be >= 1.0"):
            LpGauge(p=0.5)
        lp = LpGauge(p=2.0)
        with pytest.raises(ValueError, match="finite real numbers"):
            lp(np.array([1.0, float("nan")]))
        lp_inf = LpGauge(p=float("inf"), scale=2.0)
        assert lp_inf(np.array([3.0, -5.0])) == pytest.approx(10.0)

        # AnisotropicGauge edge cases
        with pytest.raises(ValueError, match="finite real numbers"):
            AnisotropicGauge(np.array([[1.0, float("nan")], [0.0, 1.0]]))
        ag = AnisotropicGauge(np.eye(2))
        with pytest.raises(ValueError, match="finite real numbers"):
            ag(np.array([1.0, float("nan")]))
        with pytest.raises(ValueError, match="Input length 3 does not match matrix dimension 2"):
            ag(np.array([1.0, 2.0, 3.0]))

        # Group actions and audits with explicit rng
        rng = np.random.default_rng(123)
        from gauges import make_signed_permutation
        mat = make_signed_permutation(3, rng=rng)
        assert mat.shape == (3, 3)

        with pytest.raises(ValueError, match="dim must be integer >= 1"):
            audit_so_k_invariance(eg, dim=0)
        res_inv = audit_so_k_invariance(eg, dim=2, num_samples=5, rng=rng)
        assert res_inv["is_so_k_invariant"] is True

        with pytest.raises(ValueError, match="dim must be integer >= 1"):
            audit_sphere_constancy(eg, dim=0)
        with pytest.raises(ValueError, match="radius must be strictly positive"):
            audit_sphere_constancy(eg, dim=2, radius=-1.0)
        res_const = audit_sphere_constancy(eg, dim=2, num_samples=5, rng=rng)
        assert res_const["is_sphere_constant"] is True

    def test_cycle_analytics_edge_cases(self) -> None:
        with pytest.raises(ValueError, match="Edge weights must be finite"):
            analyze_triangle_separation([1.0, float("nan"), 1.0])

        with pytest.raises(ValueError, match="contains non-finite values"):
            compute_holonomy([np.array([[1.0, float("nan")], [0.0, 1.0]])])

        # apply_vertex_gauge_transformation edge cases
        with pytest.raises(ValueError, match="Number of connection matrices must match"):
            apply_vertex_gauge_transformation([np.eye(2)], [np.eye(2)], [(0, 1), (1, 0)])
        with pytest.raises(ValueError, match="Must provide at least one connection matrix"):
            apply_vertex_gauge_transformation([], [], [])
        with pytest.raises(ValueError, match="Connection matrices must be square"):
            apply_vertex_gauge_transformation([np.ones((2, 3))], [np.eye(2)], [(0, 0)])
        with pytest.raises(ValueError, match="Vertex gauge 0 has shape"):
            apply_vertex_gauge_transformation([np.eye(2)], [np.eye(3)], [(0, 0)])
        with pytest.raises(ValueError, match="Vertex gauge 0 contains non-finite"):
            apply_vertex_gauge_transformation(
                [np.eye(2)], [np.array([[1.0, float("nan")], [0.0, 1.0]])], [(0, 0)]
            )
        with pytest.raises(ValueError, match="Vertex gauge 0 has det"):
            apply_vertex_gauge_transformation(
                [np.eye(2)], [np.array([[-1.0, 0.0], [0.0, 1.0]])], [(0, 0)]
            )
        with pytest.raises(ValueError, match="Connection matrix 1 has shape"):
            apply_vertex_gauge_transformation([np.eye(2), np.eye(3)], [np.eye(2)], [(0, 0), (0, 0)])
        with pytest.raises(ValueError, match="Connection matrix 0 contains non-finite"):
            apply_vertex_gauge_transformation(
                [np.array([[1.0, float("nan")], [0.0, 1.0]])], [np.eye(2)], [(0, 0)]
            )
        with pytest.raises(ValueError, match="Connection matrix 0 is not orthogonal"):
            apply_vertex_gauge_transformation([2.0 * np.eye(2)], [np.eye(2)], [(0, 0)])
        with pytest.raises(ValueError, match="Connection matrix 0 has det"):
            apply_vertex_gauge_transformation(
                [np.array([[-1.0, 0.0], [0.0, 1.0]])], [np.eye(2)], [(0, 0)]
            )

    def test_carrier_edge_cases(self) -> None:
        with pytest.raises(ValueError, match="Degree must be 0, 1, or 2"):
            Cochain(np.zeros((2, 2)), degree=3)
        with pytest.raises(ValueError, match="must be 1D or 2D"):
            Cochain(np.zeros((2, 2, 2, 2)), degree=1)
        with pytest.raises(ValueError, match="finite real numbers"):
            Cochain([1.0, float("nan")])

        with pytest.raises(ValueError, match="Edge 0 must be a 2-tuple"):
            GraphComplex(3, edges=["not_tuple"])  # type: ignore[list-item]
        with pytest.raises(ValueError, match="endpoints must be integers"):
            GraphComplex(3, edges=[("a", "b")])  # type: ignore[list-item]
        with pytest.raises(ValueError, match="Face 0 must be a sequence"):
            GraphComplex(3, [(0, 1), (1, 2), (2, 0)], faces=["not_seq"])  # type: ignore[list-item]
        with pytest.raises(ValueError, match="Face 0 term must be a pair"):
            GraphComplex(3, [(0, 1), (1, 2), (2, 0)], faces=[["not_pair"]])  # type: ignore[list-item]
        with pytest.raises(ValueError, match="Face weights must be finite"):
            GraphComplex(
                3,
                [(0, 1), (1, 2), (2, 0)],
                faces=[[(0, 1), (1, 1), (2, 1)]],
                face_weights=[float("nan")],
            )
        with pytest.raises(ValueError, match="cycle_len must be >= 3"):
            GraphComplex.create_cycle_graph(cycle_len=2)

    def test_socp_certifier_edge_cases(self) -> None:
        tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        certifier = SOCPCertifier(tri)
        with pytest.raises(ValueError, match="Orientations length must match number of edges"):
            certifier._simple_cycle_orientation_signs([1, 1])
        with pytest.raises(ValueError, match="Orientation sign must be"):
            certifier._simple_cycle_orientation_signs([1, 2, 1])

        # Test cycle without face using _walk_simple_cycle_orientation_signs
        tri_noface = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2, with_face=False)
        cert_noface = SOCPCertifier(tri_noface)
        signs = cert_noface._simple_cycle_orientation_signs(None)
        assert len(signs) == 3

        # Test cycle_closed_form with zero circulation
        zero_omega = Cochain(np.zeros((3, 2)))
        cert_zero = certifier._solve_cycle_closed_form(zero_omega)
        assert cert_zero.primal_value == pytest.approx(0.0)

        # Test tree graph under _solve_general_socp (B == 0)
        tree = GraphComplex(num_vertices=3, edges=[(0, 1), (1, 2)], stalk_dim=2)
        tree_certifier = SOCPCertifier(tree)
        tree_omega = Cochain(np.array([[1.0, 2.0], [3.0, 4.0]]))
        cert_tree = tree_certifier._solve_general_socp(tree_omega)
        assert cert_tree.solver_method == "zero_circulation"
        assert cert_tree.is_optimal is True

        # CycleClosedFormCertifier on a non-cycle must reject
        with pytest.raises(ValueError, match="requires a simple directed cycle"):
            CycleClosedFormCertifier(tree)

        # CycleClosedFormCertifier certify execution
        cf_cert = CycleClosedFormCertifier(tri)
        res = cf_cert.certify(Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])))
        assert res.is_optimal is True

    def test_falsification_edge_cases(self) -> None:
        from falsification import InvasiveAdversary
        # Test with stalk_dim=3 to cover k > 2 branches
        tri_3d = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=3)
        adv = InvasiveAdversary(tri_3d)
        res_repair = adv.test_connection_corruption_and_direct_repair(theta_angle=0.4)
        assert res_repair.recovery_successful is True

        res_conjugacy = adv.test_vertex_gauge_transformation_conjugacy(theta_angle=0.4)
        assert res_conjugacy.recovery_successful is True

        # Test backward-compatibility alias
        res_alias = adv.test_holonomy_curvature_injection_and_recovery(theta_angle=0.4)
        assert res_alias.recovery_successful is True

    def test_solver_edge_cases(self) -> None:
        tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
        solver = MixedNormSolver(tri)
        # Test exact=True explicitly
        cert = solver.solve(omega, exact=True)
        assert cert.is_optimal is True

    def test_secondary_fail_fast_gaps(self) -> None:
        """Verify all secondary fail-fast gaps identified in Section 11.4 of the review."""
        from cycle_analytics import analyze_dimension_scaling
        from gauges import (
            make_random_sok_rotation,
            make_signed_permutation,
            make_so2_rotation,
            audit_sphere_constancy,
            audit_so_k_invariance,
            EuclideanGauge,
        )

        # 1. Zero-edge complex rejected at construction
        with pytest.raises(ValueError, match="must have at least one edge"):
            GraphComplex(num_vertices=1, edges=[])

        # 2. Boolean endpoints rejected at construction
        with pytest.raises(ValueError, match="endpoints must be integers"):
            GraphComplex(2, [(False, True)])

        with pytest.raises(ValueError, match="num_vertices must be integer >= 1"):
            GraphComplex(num_vertices=True, edges=[(0, 1)])  # type: ignore[arg-type]

        with pytest.raises(ValueError, match="stalk_dim must be integer >= 1"):
            GraphComplex(num_vertices=2, edges=[(0, 1)], stalk_dim=True)  # type: ignore[arg-type]

        # 3. analyze_dimension_scaling rejects k < 1 and boolean dimensions
        with pytest.raises(ValueError, match="Stalk dimension k must be positive integer >= 1"):
            analyze_dimension_scaling([0])

        with pytest.raises(ValueError, match="Stalk dimension k must be positive integer >= 1"):
            analyze_dimension_scaling([True])  # type: ignore[list-item]

        # 4. make_random_sok_rotation rejects k < 1 and boolean
        with pytest.raises(ValueError, match="k must be non-boolean integer >= 1"):
            make_random_sok_rotation(0)

        with pytest.raises(ValueError, match="k must be non-boolean integer >= 1"):
            make_random_sok_rotation(True)  # type: ignore[arg-type]

        with pytest.raises(ValueError, match="k must be non-boolean integer >= 1"):
            make_signed_permutation(0)

        # 5. make_so2_rotation rejects non-finite angle and boolean
        with pytest.raises(ValueError, match="Angle theta must be a finite real number"):
            make_so2_rotation(float("nan"))

        with pytest.raises(ValueError, match="Angle theta must be a finite real number"):
            make_so2_rotation(float("inf"))

        with pytest.raises(ValueError, match="Angle theta must be a finite real number"):
            make_so2_rotation(True)  # type: ignore[arg-type]

        # 6. audit_sphere_constancy rejects non-finite / non-positive radius and tolerance
        g = EuclideanGauge(1.0)
        with pytest.raises(ValueError, match="radius must be strictly positive and finite"):
            audit_sphere_constancy(g, dim=2, radius=float("nan"))

        with pytest.raises(ValueError, match="radius must be strictly positive and finite"):
            audit_sphere_constancy(g, dim=2, radius=0.0)

        with pytest.raises(ValueError, match="tolerance must be nonnegative and finite"):
            audit_sphere_constancy(g, dim=2, tol=float("nan"))

        with pytest.raises(ValueError, match="tolerance must be nonnegative and finite"):
            audit_sphere_constancy(g, dim=2, tol=-1.0)

        with pytest.raises(ValueError, match="tolerance must be nonnegative and finite"):
            audit_so_k_invariance(g, dim=2, tol=float("nan"))

        # 7. CycleClosedFormCertifier.certify validates shape and orientations
        tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
        cf = CycleClosedFormCertifier(tri)
        with pytest.raises(ValueError, match="Omega shape"):
            cf.certify(Cochain(np.array([[1.0, 0.0], [0.0, 1.0]])))

        with pytest.raises(ValueError, match="Orientations length must match number of edges"):
            cf.certify(
                Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])),
                orientations=[1, 1],
            )

        with pytest.raises(ValueError, match="Orientation sign must be"):
            cf.certify(
                Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])),
                orientations=[2, 1, 1],
            )

