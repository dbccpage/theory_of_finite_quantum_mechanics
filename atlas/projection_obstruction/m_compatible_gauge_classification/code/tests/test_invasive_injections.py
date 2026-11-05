"""Adversarial fault-injection and break-and-recover test suite for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

import numpy as np
import pytest

from gs001_gauges import (
    EdgeDiagram,
    InvalidWeightError,
    PresheafRestrictionError,
    l1,
    l2,
    linf,
    anisotropic_gauge,
    evaluate_p1_edgewise_sum,
    cptp_measure_and_prepare,
    is_hermitian_trace_zero,
    exact_induced_operator_norm,
    minkowski_functional,
    polytope_unit_ball_membership,
    probe_minkowski_boundary_continuity,
    stiff_weight_condition_number,
    diagram_connected_components,
    audit_disconnected_component_decoupling,
    validate_presheaf_restrictions,
)
from higher_cochains import (
    SimplicialPoset2D,
    coboundary_d0,
    coboundary_d0_presheaf,
    coboundary_d1_presheaf,
    verify_chain_complex_property,
    verify_presheaf_chain_complex,
    c2_curvature_diagnostic,
    c2_maximal_rigidity_check,
    poset_connected_components,
)
from schatten import (
    schatten_norm,
    ky_fan_norm,
    is_unitarily_invariant,
    cptp_schatten_contractivity_audit,
    singular_values,
)
from galois_lattice import (
    MonoidClass,
    sample_monoid_generators,
    check_bidirectional_reachability,
    monoid_containment_lattice,
)
from perturbations import (
    inject_non_contractive_operator,
    inject_anisotropic_shear,
    inject_negative_edge_weights,
    inject_nan_edge_weights,
    inject_inf_edge_weights,
    inject_presheaf_restriction_defect,
    inject_non_hermitian_noise,
    inject_trace_leakage,
    inject_cptp_dilation,
    audit_gauge_compatibility_violation,
    audit_cptp_trace_preservation,
    recover_hermitian_trace_zero,
    recover_positive_weights,
    recover_cptp_trace_preservation,
)


class TestInvasiveOperatorPerturbations:
    """Test non-contractive operator mutations, detection, and failure modes."""

    def test_non_contractive_operator_injection_and_audit(self):
        # Basis operator on R^2
        r45 = np.array(
            [
                [1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0)],
                [1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
            ]
        )
        x = np.array([1.0, 0.0])
        op_norm = exact_induced_operator_norm(r45, "l2", "l2")

        # Base case is compliant under l2
        compliant, excess = audit_gauge_compatibility_violation(l2, r45, x, op_norm)
        assert compliant
        assert excess == 0.0

        # Invalidate dilation factor validation
        with pytest.raises(ValueError, match="dilation_factor must be > 1.0"):
            inject_non_contractive_operator(r45, 0.9)

        # Inject non-contractive dilation
        t_bad = inject_non_contractive_operator(r45, 1.5)
        # Audit against original op_norm
        compliant, excess = audit_gauge_compatibility_violation(l2, t_bad, x, op_norm)
        assert not compliant
        assert excess > 0.4

    def test_anisotropic_shear_breaks_rotation_invariance(self):
        with pytest.raises(ValueError, match="Dimension must be at least 2"):
            inject_anisotropic_shear(1)

        shear = inject_anisotropic_shear(2, 0.8)
        u = np.array([1.0, 0.0])
        v = np.array([0.0, 1.0])

        # Under l2, ||u|| = ||v|| = 1
        assert l2(u) == l2(v)
        # After shear, u is unchanged but v is sheared to (0.8, 1)
        u_sheared = shear @ u
        v_sheared = shear @ v
        assert l2(u_sheared) != l2(v_sheared)


class TestInvasiveEdgeWeightPerturbations:
    """Test corruption of edge aggregation weights and recovery."""

    def test_negative_edge_weights_break_and_recover(self):
        weights = [1.0, 2.0, 3.0]
        defects = [np.array([1.0, 0.0]), np.array([0.0, 1.0]), np.array([1.0, 1.0])]
        edges = ((0, 1), (1, 2), (0, 2))
        gauges = (l2, l2, l2)

        # Valid baseline diagram
        diag_clean = EdgeDiagram(
            edges=edges, edge_weights=tuple(weights), edge_gauges=gauges
        )
        val_clean = evaluate_p1_edgewise_sum(diag_clean, defects)
        assert val_clean > 0

        # Index out of bounds
        with pytest.raises(IndexError):
            inject_negative_edge_weights(weights, corrupted_idx=5)
        with pytest.raises(ValueError, match="Corrupted value must be <= 0"):
            inject_negative_edge_weights(weights, corrupted_idx=0, corrupted_val=2.5)

        # Inject negative weight
        bad_weights = inject_negative_edge_weights(
            weights, corrupted_idx=1, corrupted_val=-3.0
        )
        assert bad_weights[1] == -3.0

        # Building an EdgeDiagram with bad weights must fail
        with pytest.raises(ValueError, match="Edge weights must be strictly positive"):
            EdgeDiagram(
                edges=edges, edge_weights=tuple(bad_weights), edge_gauges=gauges
            )

        # Recovery validation
        with pytest.raises(ValueError, match="default_weight must be positive"):
            recover_positive_weights(bad_weights, default_weight=-1.0)

        recovered_weights = recover_positive_weights(bad_weights, default_weight=1.0)
        assert all(w > 0 for w in recovered_weights)
        assert recovered_weights[1] == 1.0

        diag_rec = EdgeDiagram(
            edges=edges, edge_weights=tuple(recovered_weights), edge_gauges=gauges
        )
        val_rec = evaluate_p1_edgewise_sum(diag_rec, defects)
        assert val_rec > 0


class TestInvasiveQuantumPerturbations:
    """Test corruption of Hermitian trace-zero operators and CPTP channels."""

    def test_non_hermitian_noise_break_and_recover(self):
        # Clean H_2^0 Pauli-X
        sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
        assert is_hermitian_trace_zero(sigma_x)

        # Inject skew-Hermitian noise
        corrupted = inject_non_hermitian_noise(sigma_x, noise_scale=0.5)
        assert not is_hermitian_trace_zero(corrupted)

        # Measure-and-prepare channel refuses corrupted input
        sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
        with pytest.raises(ValueError, match="Hermitian trace-zero"):
            cptp_measure_and_prepare(corrupted, sigma_z)

        # Recovery projection
        recovered = recover_hermitian_trace_zero(corrupted)
        assert is_hermitian_trace_zero(recovered)
        assert np.allclose(recovered, sigma_x, atol=1e-12)

    def test_trace_leakage_break_and_recover(self):
        sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
        assert is_hermitian_trace_zero(sigma_z)

        # Inject trace leak
        leaked = inject_trace_leakage(sigma_z, leak=1.0)
        assert not is_hermitian_trace_zero(leaked)
        assert abs(np.trace(leaked)) > 0.9

        # Recovery projection
        recovered = recover_hermitian_trace_zero(leaked)
        assert is_hermitian_trace_zero(recovered)
        assert np.allclose(recovered, sigma_z, atol=1e-12)

    def test_cptp_dilation_break_and_recover(self):
        sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
        sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
        _, kraus_ops = cptp_measure_and_prepare(sigma_x, sigma_z)

        # Clean Kraus operators preserve trace
        compliant, dev = audit_cptp_trace_preservation(kraus_ops)
        assert compliant
        assert dev < 1e-8

        # Dilate Kraus operators
        dilated = inject_cptp_dilation(kraus_ops, factor=1.5)
        compliant, dev = audit_cptp_trace_preservation(dilated)
        assert not compliant
        assert dev > 0.4

        # Recovery
        recovered_kraus = recover_cptp_trace_preservation(dilated)
        compliant_rec, dev_rec = audit_cptp_trace_preservation(recovered_kraus)
        assert compliant_rec
        assert dev_rec < 1e-8

        # Edge case: empty kraus list
        empty_c, empty_dev = audit_cptp_trace_preservation([])
        assert not empty_c
        with pytest.raises(ValueError, match="kraus_ops cannot be empty"):
            recover_cptp_trace_preservation([])


class TestHigherCochainsAndCurvature:
    """Test C^2 curvature bicomplex, d1 o d0 = 0, and C^2 maximal rigidity."""

    @pytest.fixture
    def triangle_poset(self) -> SimplicialPoset2D:
        return SimplicialPoset2D(
            num_vertices=3,
            edges=((0, 1), (0, 2), (1, 2)),
            faces=((0, 1, 2),),
        )

    def test_invalid_poset_parameters(self):
        with pytest.raises(ValueError, match="num_vertices must be positive"):
            SimplicialPoset2D(num_vertices=0, edges=(), faces=())
        with pytest.raises(ValueError, match="Invalid edge"):
            SimplicialPoset2D(num_vertices=2, edges=((0, 2),), faces=())
        with pytest.raises(ValueError, match="Invalid face"):
            SimplicialPoset2D(num_vertices=3, edges=((0, 1),), faces=((0, 1, 3),))
        with pytest.raises(ValueError, match="boundary edges missing"):
            SimplicialPoset2D(
                num_vertices=3, edges=((0, 1), (1, 2)), faces=((0, 1, 2),)
            )

    def test_exactness_d1_d0_zero(self, triangle_poset):
        c0 = np.array([2.5, -1.0, 4.0])
        assert verify_chain_complex_property(triangle_poset, c0)

        # Invalid c0 length
        with pytest.raises(ValueError, match="c0 length"):
            coboundary_d0(triangle_poset, np.array([1.0, 2.0]))

    def test_c2_curvature_diagnostic(self, triangle_poset):
        # Non-cocycle 1-cochain
        c1 = np.array([1.0, 0.0, 0.0])
        # (d1 c)(0,1,2) = c(1,2) - c(0,2) + c(0,1) = 0 - 0 + 1 = 1
        curv = c2_curvature_diagnostic(triangle_poset, c1, face_weights=[2.0])
        assert np.isclose(curv, 2.0)

        # Default face weights
        curv_def = c2_curvature_diagnostic(triangle_poset, c1)
        assert np.isclose(curv_def, 1.0)

        # Dimension mismatch or invalid weights
        with pytest.raises(ValueError, match="c1 length"):
            c2_curvature_diagnostic(triangle_poset, np.array([1.0]))
        with pytest.raises(ValueError, match="Weights length"):
            c2_curvature_diagnostic(triangle_poset, c1, face_weights=[1.0, 2.0])
        with pytest.raises(ValueError, match="strictly positive"):
            c2_curvature_diagnostic(triangle_poset, c1, face_weights=[-1.0])

    def test_c2_maximal_rigidity_check(self):
        # Proportional to l2 norm
        assert c2_maximal_rigidity_check(
            face_stalk_dim=2, gauge=lambda x: 3.0 * l2(x), target_norm=l2
        )
        # Anisotropic gauge fails rigidity under End_b
        assert not c2_maximal_rigidity_check(
            face_stalk_dim=2, gauge=anisotropic_gauge, target_norm=l2
        )
        # Zero gauge fails
        assert not c2_maximal_rigidity_check(
            face_stalk_dim=2, gauge=lambda x: 0.0, target_norm=l2
        )
        # Small probe count edge case
        assert not c2_maximal_rigidity_check(
            face_stalk_dim=2, gauge=l2, target_norm=l2, n_probes=1
        )


class TestSchattenAndUnitaryInvariance:
    """Test Schatten p-norms, Ky Fan norms, and CPTP contractivity audit."""

    def test_schatten_p_norms(self):
        # Matrix with singular values 3, 4
        m = np.array([[3.0, 0.0], [0.0, 4.0]], dtype=complex)
        assert np.isclose(schatten_norm(m, p=1.0), 7.0)  # 3 + 4
        assert np.isclose(schatten_norm(m, p=2.0), 5.0)  # sqrt(9 + 16)
        assert np.isclose(schatten_norm(m, p=np.inf), 4.0)  # max(3, 4)
        assert np.isclose(ky_fan_norm(m, k=1), 4.0)
        assert np.isclose(ky_fan_norm(m, k=2), 7.0)

        # 1D array should raise error
        with pytest.raises(ValueError, match="2D matrix"):
            singular_values(np.array([1.0, 2.0]))

        with pytest.raises(ValueError, match="p must be >= 1.0"):
            schatten_norm(m, p=0.5)
        with pytest.raises(ValueError, match="k must be in"):
            ky_fan_norm(m, k=0)
        with pytest.raises(ValueError, match="k must be in"):
            ky_fan_norm(m, k=3)

    def test_unitary_invariance(self):
        # Schatten 2-norm is unitarily invariant
        assert is_unitarily_invariant(
            lambda x: schatten_norm(x, 2.0), dimension=2, n_probes=10
        )
        # Matrix entry norm |X_00| is not unitarily invariant
        assert not is_unitarily_invariant(
            lambda x: float(abs(x[0, 0])), dimension=2, n_probes=10
        )
        # Zero gauge edge case skips probe loop
        assert is_unitarily_invariant(lambda x: 0.0, dimension=2, n_probes=5)

    def test_cptp_schatten_contractivity_audit(self):
        sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
        sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
        channel_fn, _ = cptp_measure_and_prepare(sigma_x, sigma_z)

        audit = cptp_schatten_contractivity_audit(
            channel_fn, sigma_x, p_values=(1.0, 2.0)
        )
        # Trace norm (p=1) must be contractive
        assert audit[1.0][2] is True


class TestGaloisLatticeAndReachability:
    """Test monoid classes, generator sampling, and reachability criteria."""

    def test_monoid_generator_sampling(self):
        with pytest.raises(ValueError, match="Dimension must be at least 2"):
            sample_monoid_generators(MonoidClass.TRIVIAL, 1)

        for m in MonoidClass:
            gens = sample_monoid_generators(m, dimension=2)
            assert len(gens) >= 1
            assert all(g.shape == (2, 2) for g in gens)

    def test_bidirectional_reachability(self):
        u = np.array([1.0, 0.0])
        v = np.array([0.0, 1.0])
        w = np.array([1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)])

        # Full linear connects any equal-norm pair
        assert check_bidirectional_reachability(u, w, MonoidClass.FULL_LINEAR, "l2")
        # Orthogonal connects u and v (both have l2 norm 1)
        assert check_bidirectional_reachability(u, v, MonoidClass.ORTHOGONAL)
        # Signed permutation connects u and v (permutation of coordinates)
        assert check_bidirectional_reachability(u, v, MonoidClass.SIGNED_PERMUTATION)
        # Signed permutation does NOT connect u and w
        assert not check_bidirectional_reachability(
            u, w, MonoidClass.SIGNED_PERMUTATION
        )
        # Permutation connects u and v
        assert check_bidirectional_reachability(u, v, MonoidClass.PERMUTATION)
        # Trivial connects only equal vectors
        assert check_bidirectional_reachability(u, u, MonoidClass.TRIVIAL)
        assert not check_bidirectional_reachability(u, v, MonoidClass.TRIVIAL)
        # Dimension mismatch
        assert not check_bidirectional_reachability(
            u, np.array([1.0, 0.0, 0.0]), MonoidClass.FULL_LINEAR
        )

    def test_monoid_containment_lattice(self):
        lat = monoid_containment_lattice()
        assert MonoidClass.FULL_LINEAR in lat
        assert MonoidClass.ORTHOGONAL in lat[MonoidClass.FULL_LINEAR]
        assert MonoidClass.TRIVIAL in lat[MonoidClass.PERMUTATION]


class TestEdgeCasesAndDeepSanitization:
    """Test boundary conditions, invalid complex types, and corner-case exceptions."""

    def test_edge_diagram_count_mismatches(self):
        with pytest.raises(ValueError, match="edge_gauges"):
            EdgeDiagram(edges=((0, 1),), edge_weights=(1.0,), edge_gauges=())

    def test_linf_complex_refusal(self):
        with pytest.raises(TypeError, match="Real vector space inputs"):
            linf(np.array([1.0 + 2.0j]))

    def test_cptp_non_square_and_invalid_y(self):
        # Non-square matrix in is_hermitian_trace_zero
        assert not is_hermitian_trace_zero(np.zeros((2, 3)))

        sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
        # Non-Hermitian Y
        y_bad = np.array([[1.0, 1.0], [0.0, -1.0]], dtype=complex)
        with pytest.raises(ValueError, match="Y must be a Hermitian trace-zero"):
            cptp_measure_and_prepare(sigma_x, y_bad)

        # Zero matrix X
        zero_mat = np.zeros((2, 2), dtype=complex)
        with pytest.raises(ValueError, match="Matrix X must be non-zero"):
            cptp_measure_and_prepare(zero_mat, zero_mat)

    def test_hahn_banach_rank_one_edge_cases(self):
        from rigidity import construct_hahn_banach_rank_one, is_maximal_end_compatible

        u_zero = np.array([0.0, 0.0])
        v = np.array([1.0, 1.0])
        with pytest.raises(ValueError, match="Source vector u must be non-zero"):
            construct_hahn_banach_rank_one(u_zero, v, l2)

        # Custom gauge_type fallback
        t_custom = construct_hahn_banach_rank_one(
            np.array([1.0, 0.0]), v, l2, gauge_type="custom"
        )
        assert t_custom.shape == (2, 2)

        # Dual pairing zero
        with pytest.raises(ValueError, match="Dual pairing"):
            # Construct a case where pairing is forced to zero (or mockup)
            def zero_gauge(_x):
                return 1.0

            # linf dual on zero max index
            construct_hahn_banach_rank_one(
                np.array([0.0, 0.0, 0.0]), v, zero_gauge, gauge_type="linf"
            )

        # is_maximal_end_compatible with mismatched operator shape
        assert is_maximal_end_compatible(
            l2, dimension=2, probe_operators=[np.zeros((3, 3))]
        )

    def test_gs001_gauges_complex_and_violations(self):
        from gs001_gauges import is_subadditive, is_m_compatible
        from norms import sample_lower_bound_induced_norm

        with pytest.raises(TypeError, match="Real vector inputs required"):
            is_subadditive(l2, [(np.array([1.0j, 0.0]), np.array([0.0, 1.0]))])

        # Subadditivity violation
        assert not is_subadditive(
            lambda x: float(np.sum(x**2)),
            [(np.array([1.0, 0.0]), np.array([1.0, 0.0]))],
        )

        # M-compatibility violation
        bad_op = np.array(
            [[2.0, 0.0], [0.0, 2.0]]
        )  # Op norm 2, but let's test a non-contractive gauge
        assert not is_m_compatible(
            lambda x: 10.0 * float(np.sum(x**2)), [bad_op], ambient_norm=l2
        )

        # Sample lower bound with zero vector skip
        lb, witness = sample_lower_bound_induced_norm(np.eye(2), l2, n_samples=5)
        assert lb > 0


class TestInvasiveFaultInjectionTriad:
    """Explicit tests for FI-007-1 through FI-007-5 mandated by DERIVATIONS_MASTER.md."""

    def test_fi_007_1_non_positive_nan_inf_weights_typed_exceptions(self):
        """FI-007-1: Non-positive or NaN/Inf edge weights validation with typed exceptions."""
        edges = ((0, 1), (1, 2))
        gauges = (l2, l2)

        # 1. Negative weight raises InvalidWeightError (subclass of ValueError)
        with pytest.raises(InvalidWeightError, match="strictly positive"):
            EdgeDiagram(edges, (-1.0, 2.0), gauges)

        # 2. Zero weight raises InvalidWeightError
        with pytest.raises(InvalidWeightError, match="strictly positive"):
            EdgeDiagram(edges, (0.0, 2.0), gauges)

        # 3. NaN weight raises InvalidWeightError
        with pytest.raises(InvalidWeightError, match="NaN"):
            EdgeDiagram(edges, (float("nan"), 2.0), gauges)

        # 4. Infinite weight raises InvalidWeightError
        with pytest.raises(InvalidWeightError, match="infinite"):
            EdgeDiagram(edges, (float("inf"), 2.0), gauges)
        with pytest.raises(InvalidWeightError, match="infinite"):
            EdgeDiagram(edges, (2.0, float("-inf")), gauges)

        # 5. Complex weight raises TypeError
        with pytest.raises(TypeError, match="must be real"):
            EdgeDiagram(edges, (1.0 + 2.0j, 2.0), gauges)

        # 6. Injection helpers for NaN and Inf
        weights = [1.0, 2.0, 3.0]
        nan_w = inject_nan_edge_weights(weights, corrupted_idx=1)
        assert np.isnan(nan_w[1])
        with pytest.raises(IndexError):
            inject_nan_edge_weights(weights, corrupted_idx=10)

        inf_w = inject_inf_edge_weights(weights, corrupted_idx=2)
        assert np.isinf(inf_w[2])
        with pytest.raises(IndexError):
            inject_inf_edge_weights(weights, corrupted_idx=10)
        with pytest.raises(ValueError, match="inf_val must be infinite"):
            inject_inf_edge_weights(weights, corrupted_idx=0, inf_val=5.0)

        # 7. Recovery sanitizes NaN and Inf entries back to valid positive floats
        rec_nan = recover_positive_weights(nan_w, default_weight=1.5)
        assert rec_nan[1] == 1.5
        assert all(w > 0 and np.isfinite(w) for w in rec_nan)

        rec_inf = recover_positive_weights(inf_w, default_weight=2.5)
        assert rec_inf[2] == 2.5
        assert all(w > 0 and np.isfinite(w) for w in rec_inf)

        # Invalid default weight in recovery raises ValueError
        with pytest.raises(ValueError, match="positive and finite"):
            recover_positive_weights(nan_w, default_weight=float("nan"))
        with pytest.raises(ValueError, match="positive and finite"):
            recover_positive_weights(nan_w, default_weight=float("inf"))

        # String weight raises InvalidWeightError
        with pytest.raises(InvalidWeightError, match="not a valid float"):
            EdgeDiagram(edges, ("abc", 2.0), gauges)

        # Non-numeric item in recover_positive_weights
        rec_str = recover_positive_weights([1.0, "bad", 3.0], default_weight=1.0)
        assert rec_str == [1.0, 1.0, 3.0]

        # 8. Face weights in c2_curvature_diagnostic with NaN/Inf
        tri_poset = SimplicialPoset2D(3, ((0, 1), (0, 2), (1, 2)), ((0, 1, 2),))
        c1 = np.array([1.0, 0.0, 0.0])
        with pytest.raises(InvalidWeightError, match="positive and finite"):
            c2_curvature_diagnostic(tri_poset, c1, face_weights=[float("nan")])
        with pytest.raises(InvalidWeightError, match="positive and finite"):
            c2_curvature_diagnostic(tri_poset, c1, face_weights=[float("inf")])

    def test_fi_007_2_stiff_weight_ratio_numerical_stability(self):
        """FI-007-2: Stiff weight ratio (10^9 : 10^-9) numerical stability and compensated summation."""
        w_stiff = 1e9
        w_soft = 1e-9
        edges = ((0, 1), (1, 2))
        gauges = (l2, l2)

        diagram = EdgeDiagram(edges, (w_stiff, w_soft), gauges)
        assert np.isclose(stiff_weight_condition_number(diagram), 1e18)

        # Components with disparate scales
        c_stiff = np.array([1.0, 0.0])  # Contribution: 1e9 * 1 = 1e9
        c_soft = np.array([3.0, 4.0])   # Contribution: 1e-9 * 5 = 5e-9

        val = evaluate_p1_edgewise_sum(diagram, [c_stiff, c_soft])
        assert val >= 1e9

        # Verify soft component evaluated on its own sub-diagram retains full precision
        sub_diag_soft = EdgeDiagram(((1, 2),), (w_soft,), (l2,))
        val_soft = evaluate_p1_edgewise_sum(sub_diag_soft, [c_soft])
        assert np.isclose(val_soft, 5e-9)

        # Scaling equivariance under stiff ratio:
        s = 2.5
        scaled_diag = EdgeDiagram(edges, (w_stiff * s, w_soft * s), gauges)
        val_scaled = evaluate_p1_edgewise_sum(scaled_diag, [c_stiff, c_soft])
        assert np.isclose(val_scaled, s * val, rtol=1e-12)

        # Empty weights edge case in condition number
        empty_diag = EdgeDiagram((), (), ())
        assert stiff_weight_condition_number(empty_diag) == 1.0

    def test_fi_007_3_disconnected_poset_components_gauge_decoupling(self):
        """FI-007-3: Disconnected poset components gauge decoupling."""
        # 4 vertices, 2 disconnected edges: (0, 1) and (2, 3)
        poset = SimplicialPoset2D(
            num_vertices=4,
            edges=((0, 1), (2, 3)),
            faces=(),
        )
        comps = poset_connected_components(poset)
        assert len(comps) == 2
        assert {0, 1} in comps
        assert {2, 3} in comps

        # Edge diagram on the 2 disconnected edges
        edges = ((0, 1), (2, 3))
        weights = (2.0, 5.0)
        gauges = (l2, l2)
        diagram = EdgeDiagram(edges, weights, gauges)

        diag_comps = diagram_connected_components(diagram)
        assert len(diag_comps) == 2
        assert [0] in diag_comps
        assert [1] in diag_comps

        # Initial cochains
        cochain = [np.array([1.0, 0.0]), np.array([0.0, 2.0])]
        perturbation = np.array([0.5, -0.5])

        # Perturb edge 0 (component 0)
        audit0 = audit_disconnected_component_decoupling(
            diagram, cochain, perturbation, target_edge_idx=0
        )
        assert audit0["decoupled"] is True
        assert audit0["target_delta"] > 0.0
        assert audit0["max_other_delta"] == 0.0

        # Perturb edge 1 (component 1)
        audit1 = audit_disconnected_component_decoupling(
            diagram, cochain, perturbation, target_edge_idx=1
        )
        assert audit1["decoupled"] is True
        assert audit1["target_delta"] > 0.0
        assert audit1["max_other_delta"] == 0.0

        # Disconnected poset kernel dimension: d0 s = 0 for independent shifts on components
        s_const_shift = np.array([3.0, 3.0, -7.0, -7.0])  # +3 on comp 1, -7 on comp 2
        c1_shift = coboundary_d0(poset, s_const_shift)
        assert np.allclose(c1_shift, 0.0, atol=1e-12)

        # Error cases
        single_comp_diag = EdgeDiagram(((0, 1), (1, 2)), (1.0, 1.0), (l2, l2))
        with pytest.raises(ValueError, match="at least 2 disconnected components"):
            audit_disconnected_component_decoupling(
                single_comp_diag, cochain, perturbation, target_edge_idx=0
            )

        empty_diag = EdgeDiagram((), (), ())
        assert diagram_connected_components(empty_diag) == []

        with pytest.raises(IndexError, match="not found in diagram components"):
            audit_disconnected_component_decoupling(
                diagram, cochain, perturbation, target_edge_idx=5
            )

    def test_fi_007_4_minkowski_functional_near_boundary_probes(self):
        r"""FI-007-4: Minkowski functional near-boundary probes (x in \partial K \pm 10^-8) continuity."""
        # Test on multiple norms
        test_cases = [
            ("l2", l2, np.array([1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)])),
            ("l1", l1, np.array([0.5, 0.5])),
            ("linf", linf, np.array([1.0, -0.7])),
            ("aniso", lambda v: anisotropic_gauge(v, (1.0, 2.0)), np.array([0.4, 0.3])),
        ]

        for name, norm_fn, boundary_vec in test_cases:
            res = probe_minkowski_boundary_continuity(
                norm_fn, boundary_vec, epsilons=(1e-8, 1e-6, 1e-4), tol=1e-5
            )
            assert res["continuous"] is True, f"Failed continuity for {name}: {res}"
            assert np.isclose(res["base_val"], 1.0, atol=1e-4)

        # Monotonicity test across boundary
        x0 = np.array([1.0, 0.0])  # On unit sphere for l2
        is_in = lambda v: polytope_unit_ball_membership(v, l2)
        j_in = minkowski_functional((1.0 - 1e-8) * x0, is_in)
        j_on = minkowski_functional(x0, is_in)
        j_out = minkowski_functional((1.0 + 1e-8) * x0, is_in)
        assert j_in < j_on < j_out
        assert np.isclose(j_out - j_in, 2e-8, atol=1e-7)

    def test_fi_007_5_presheaf_restriction_failure_validation(self):
        """FI-007-5: Presheaf restriction failure validation and coboundary fault detection."""
        # Simplicial complex with 1 triangle (0, 1, 2)
        poset = SimplicialPoset2D(
            num_vertices=3,
            edges=((0, 1), (0, 2), (1, 2)),
            faces=((0, 1, 2),),
        )

        # Valid coherent restriction maps on 2D stalks: R_{uv}, R_{vw}, R_{uw}
        # R_{uw} = R_{vw} @ R_{uv}
        r_01 = np.array([[1.0, 0.5], [0.0, 1.0]])
        r_12 = np.array([[0.8, 0.0], [0.2, 0.9]])
        r_02 = r_12 @ r_01  # Exact path coherence

        restrictions = {
            (0, 1): r_01,
            (1, 2): r_12,
            (0, 2): r_02,
        }

        # 1. Coherent case passes validation and d1 o d0 = 0
        assert validate_presheaf_restrictions(restrictions, poset.faces)
        c0_sections = {
            0: np.array([1.0, -2.0]),
            1: np.array([0.5, 3.0]),
            2: np.array([-1.0, 0.0]),
        }
        is_exact, max_curv = verify_presheaf_chain_complex(poset, c0_sections, restrictions)
        assert is_exact is True
        assert np.isclose(max_curv, 0.0, atol=1e-12)

        # 2. Inject defect breaking path coherence
        bad_restrictions = inject_presheaf_restriction_defect(
            restrictions, edge=(0, 1), noise_scale=1.0, seed=123
        )
        # Validation must fail with PresheafRestrictionError
        with pytest.raises(PresheafRestrictionError, match="path coherence failure"):
            validate_presheaf_restrictions(bad_restrictions, poset.faces)

        # Coboundary exactness must fail: d1 o d0 != 0
        is_exact_bad, max_curv_bad = verify_presheaf_chain_complex(
            poset, c0_sections, bad_restrictions
        )
        assert is_exact_bad is False
        assert max_curv_bad > 1e-3

        # 3. Missing restriction map raises PresheafRestrictionError
        incomplete_restrictions = {(0, 1): r_01, (1, 2): r_12}
        with pytest.raises(PresheafRestrictionError, match="Missing restriction map"):
            validate_presheaf_restrictions(incomplete_restrictions, poset.faces)

        # Missing (0, 1)
        missing_01 = {(1, 2): r_12, (0, 2): r_02}
        with pytest.raises(PresheafRestrictionError, match=r"Missing restriction map for edge \(0, 1\)"):
            validate_presheaf_restrictions(missing_01, poset.faces)

        # Missing (1, 2)
        missing_12 = {(0, 1): r_01, (0, 2): r_02}
        with pytest.raises(PresheafRestrictionError, match=r"Missing restriction map for edge \(1, 2\)"):
            validate_presheaf_restrictions(missing_12, poset.faces)

        # Incomplete edges in coboundary
        with pytest.raises(PresheafRestrictionError, match="Missing restriction map"):
            coboundary_d0_presheaf(poset, c0_sections, incomplete_restrictions)
        with pytest.raises(PresheafRestrictionError, match="Missing restriction map"):
            coboundary_d1_presheaf(
                poset,
                {(0, 1): np.zeros(2), (0, 2): np.zeros(2), (1, 2): np.zeros(2)},
                incomplete_restrictions,
            )

        # Missing c0 section or missing 1-cochain
        with pytest.raises(ValueError, match="Missing c0 section"):
            coboundary_d0_presheaf(poset, {0: np.zeros(2)}, restrictions)
        with pytest.raises(ValueError, match="Missing 1-cochain"):
            coboundary_d1_presheaf(poset, {}, restrictions)

        # Invalid edge for defect injection
        with pytest.raises(KeyError, match="not in restrictions"):
            inject_presheaf_restriction_defect(restrictions, edge=(2, 0))

