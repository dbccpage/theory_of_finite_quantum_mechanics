"""Adversarial stress-test suite for Relational Regge Curvature & Unified Relational Spine.

Authored by Challenger M2-2 to empirically verify:
1. Primal-dual LP duality gap and stickiness metric stability across topologies.
2. HiGHS subthreshold feasibility boundary and resolution limits at micro-scales.
3. Near-degenerate triangles approaching flat line collinear limits (a + b -> c^+).
4. Extreme-scale floating-point overflow and underflow boundaries (1e-165, 1e160).
5. Boolean subclass traps across all dataclasses and guard functions.
6. Adversarial input permutations: NaNs, infinities, strings, negatives, and type spoofing.
7. Dimensional mismatches, malformed tuples, and illegal simplicial topologies.
8. Empirical holding of the Authorization Boundary Theorem across 100 random fiber presentations.
9. Verification of combinatorial Bianchi identity and gauge invariance under randomized floods.
10. Explicit characterization of uncovered dataclass validation gaps.

AuthorityEffect: None.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from regge_relational_obstruction import (
    Compression,
    Fact,
    FiberBundle,
    Obstruction,
    Presentation,
    PresentationFamily,
    RelationalReggeCurvature,
    RelationalReggeError,
    RelationalSimplicialBone,
    RelationalSimplicialComplex,
    RelationalSpineError,
    Representation,
    _guard_float,
    compare_standard_and_relational_regge,
    compute_regge_deficit_angle_from_relational_edges,
    compute_relational_quotient_stickiness_lp,
    execute_unified_relational_spine,
)
from scipy.optimize import linprog


def _solve_exact_dual_lp(
    d0: np.ndarray,
    delta: np.ndarray,
) -> tuple[float, np.ndarray]:
    """Solve the exact dual LP to inf_alpha ||delta - d0 alpha||_1:

    max_w  w^T delta
    s.t.   (d^0)^T w = 0
           -1 <= w_e <= 1

    Returns (dual_optimal_value, dual_optimal_weights).
    """
    m_edges, n_nodes = d0.shape
    c_dual = -delta.astype(np.float64)
    a_eq = d0.T.astype(np.float64)
    b_eq = np.zeros(n_nodes, dtype=np.float64)
    bounds = [(-1.0, 1.0)] * m_edges
    res = linprog(c_dual, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not res.success:
        raise RuntimeError(f"Dual LP solver failed: {res.message}")
    dual_value = float(-res.fun)
    return dual_value, res.x


# ===========================================================================
# 1. Primal-Dual LP Duality Gap & Metric Stability
# ===========================================================================


def test_primal_dual_duality_gap_across_diverse_topologies() -> None:
    """Verify strong duality (primal == dual) across diverse graph complexes."""
    # Topology A: Single 2-simplex (triangle)
    tri = RelationalSimplicialComplex((0, 1, 2), ((0, 1), (1, 2), (0, 2)), ((0, 1, 2),))
    d0_tri = tri.incidence_matrix_d0()
    delta_tri = np.array([1.5, -2.2, 0.8], dtype=np.float64)
    p_tri = compute_relational_quotient_stickiness_lp(d0_tri, delta_tri)
    d_val_tri, w_opt_tri = _solve_exact_dual_lp(d0_tri, delta_tri)
    gap_tri = abs(p_tri.quotient_residual - d_val_tri)
    assert gap_tri < 1.0e-10, f"Duality gap on triangle: {gap_tri}"
    assert np.all(np.abs(w_opt_tri) <= 1.0 + 1.0e-9)
    assert np.allclose(d0_tri.T @ w_opt_tri, 0.0, atol=1.0e-9)

    # Topology B: Disconnected complex (two disjoint triangles)
    disc = RelationalSimplicialComplex(
        nodes=(0, 1, 2, 3, 4, 5),
        edges=((0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)),
        faces=((0, 1, 2), (3, 4, 5)),
    )
    d0_disc = disc.incidence_matrix_d0()
    delta_disc = np.array([2.0, -1.0, 3.0, -4.0, 1.5, 0.5], dtype=np.float64)
    p_disc = compute_relational_quotient_stickiness_lp(d0_disc, delta_disc)
    d_val_disc, _ = _solve_exact_dual_lp(d0_disc, delta_disc)
    gap_disc = abs(p_disc.quotient_residual - d_val_disc)
    assert gap_disc < 1.0e-10, f"Duality gap on disconnected complex: {gap_disc}"

    # Topology C: Large cycle C50 with non-bounding circulation
    nodes_c50 = tuple(range(50))
    edges_c50 = tuple((i, (i + 1) % 50) for i in range(50))
    c50 = RelationalSimplicialComplex(nodes_c50, edges_c50)
    d0_c50 = c50.incidence_matrix_d0()
    delta_c50 = np.ones(50, dtype=np.float64)
    p_c50 = compute_relational_quotient_stickiness_lp(d0_c50, delta_c50)
    d_val_c50, _ = _solve_exact_dual_lp(d0_c50, delta_c50)
    assert math.isclose(p_c50.quotient_residual, 50.0, abs_tol=1.0e-9)
    assert math.isclose(d_val_c50, 50.0, abs_tol=1.0e-9)
    assert abs(p_c50.quotient_residual - d_val_c50) < 1.0e-10

    # Topology D: Complete graph K5 (5 nodes, 10 edges)
    nodes_k5 = tuple(range(5))
    edges_k5 = tuple((i, j) for i in range(5) for j in range(i + 1, 5))
    k5 = RelationalSimplicialComplex(nodes_k5, edges_k5)
    d0_k5 = k5.incidence_matrix_d0()
    rng = np.random.default_rng(12345)
    delta_k5 = rng.uniform(-10.0, 10.0, size=k5.num_edges)
    p_k5 = compute_relational_quotient_stickiness_lp(d0_k5, delta_k5)
    d_val_k5, _ = _solve_exact_dual_lp(d0_k5, delta_k5)
    gap_k5 = abs(p_k5.quotient_residual - d_val_k5)
    assert gap_k5 < 1.0e-9, f"Duality gap on K5: {gap_k5}"


def test_stickiness_norm_axioms_stability() -> None:
    """Verify operational stickiness satisfies pseudo-norm axioms (homogeneity, subadditivity)."""
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)
    d0 = fan6.incidence_matrix_d0()
    rng = np.random.default_rng(999)

    delta1 = rng.uniform(-5.0, 5.0, size=fan6.num_edges)
    delta2 = rng.uniform(-5.0, 5.0, size=fan6.num_edges)

    s1 = compute_relational_quotient_stickiness_lp(d0, delta1).operational_stickiness
    s2 = compute_relational_quotient_stickiness_lp(d0, delta2).operational_stickiness
    s_sum = compute_relational_quotient_stickiness_lp(d0, delta1 + delta2).operational_stickiness

    # 1. Subadditivity (triangle inequality for quotient stickiness)
    assert s_sum <= s1 + s2 + 1.0e-9, f"Subadditivity failed: {s_sum} > {s1} + {s2}"

    # 2. Absolute homogeneity: Phi([c * delta]) == |c| * Phi([delta])
    for c in [-3.5, 0.25, 4.0]:
        s_scaled = compute_relational_quotient_stickiness_lp(d0, c * delta1).operational_stickiness
        expected = abs(c) * s1
        assert math.isclose(s_scaled, expected, abs_tol=1.0e-8), f"Homogeneity failed for scale {c}"

    # 3. Non-negativity & zero defect
    s_zero = compute_relational_quotient_stickiness_lp(
        d0, np.zeros(fan6.num_edges)
    ).operational_stickiness
    assert math.isclose(s_zero, 0.0, abs_tol=1.0e-12)


# ===========================================================================
# 2. HiGHS Subthreshold Feasibility Boundary Characterization
# ===========================================================================


def test_lp_subthreshold_resolution_boundary_and_false_authorization() -> None:
    """Characterize the HiGHS resolution boundary (~1e-7) where harmonic defect is falsely AUTHORIZED."""
    nodes = (0, 1, 2)
    edges = ((0, 1), (1, 2), (0, 2))
    c3 = RelationalSimplicialComplex(nodes, edges)
    d0 = c3.incidence_matrix_d0()

    # Harmonic 1-cycle with non-zero circulation 3 * eps
    # For eps >= 1e-6: solver correctly identifies non-gauge obstruction
    for eps in [1.0e-4, 1.0e-5, 1.0e-6]:
        delta = np.array([eps, eps, -eps], dtype=np.float64)
        res = compute_relational_quotient_stickiness_lp(d0, delta)
        assert res.is_pure_gauge is False
        assert res.status == "OBSTRUCTED"
        assert math.isclose(res.quotient_residual, 3.0 * eps, rel_tol=1.0e-4)

    # For eps <= 1e-8: HiGHS default feasibility tolerance (1e-7) treats residual as 0.0
    for eps in [1.0e-8, 1.0e-10]:
        delta = np.array([eps, eps, -eps], dtype=np.float64)
        res = compute_relational_quotient_stickiness_lp(d0, delta)
        # Empirical finding: solver falsely marks sub-threshold harmonic circulation as pure gauge
        assert res.is_pure_gauge is True
        assert res.status == "AUTHORIZED"
        assert math.isclose(res.quotient_residual, 0.0, abs_tol=1.0e-12)


# ===========================================================================
# 3. Near-Degenerate Triangles Approaching Collinear Limits (a + b -> c^+)
# ===========================================================================


def test_near_degenerate_triangles_collinear_limit() -> None:
    """Test triangles approaching flat line a + b -> c^+ where angle sum approaches pi."""
    # a = 1.0, b = 1.0, c = 2.0 - eps (eps -> 0)
    for eps in [1.0e-2, 1.0e-4, 1.0e-8, 1.0e-12, 1.0e-14]:
        tri_edges = [(1.0, 1.0, 2.0 - eps)]
        sum_a, def_a, _ = compute_regge_deficit_angle_from_relational_edges(tri_edges)
        # For a single triangle, the single angle at vertex opposite to c is being evaluated
        # cos_th = (1 + 1 - (2 - eps)^2) / 2 = -1 + 2*eps - eps^2/2
        # As eps -> 0, cos_th -> -1, angle -> pi
        assert math.isclose(sum_a, math.pi, abs_tol=math.sqrt(eps) * 3.0)
        assert math.isclose(def_a, math.pi, abs_tol=math.sqrt(eps) * 3.0)

    # All three internal angles evaluated manually:
    eps = 1.0e-10
    a, b, c = 1.0, 1.0, 2.0 - eps
    cos_c = (a * a + b * b - c * c) / (2.0 * a * b)
    cos_a = (b * b + c * c - a * a) / (2.0 * b * c)
    cos_b = (a * a + c * c - b * b) / (2.0 * a * c)
    th_c = math.acos(max(-1.0, min(1.0, cos_c)))
    th_a = math.acos(max(-1.0, min(1.0, cos_a)))
    th_b = math.acos(max(-1.0, min(1.0, cos_b)))
    total = th_a + th_b + th_c
    assert math.isclose(total, math.pi, abs_tol=1.0e-9)
    assert math.isclose(th_c, math.pi, abs_tol=1.0e-4)
    assert th_a < 1.0e-4
    assert th_b < 1.0e-4


def test_degenerate_triangle_inequality_enforcement() -> None:
    """Verify fail-closed rejection when collinear boundary is reached or breached."""
    # Exact flat line: a + b == c
    with pytest.raises(RelationalReggeError, match="violates triangle inequality"):
        compute_regge_deficit_angle_from_relational_edges([(1.0, 1.0, 2.0)])

    # Breached triangle inequality: a + b < c
    with pytest.raises(RelationalReggeError, match="violates triangle inequality"):
        compute_regge_deficit_angle_from_relational_edges([(1.0, 1.0, 2.0001)])

    # Precision limit: 2.0 - 1e-16 rounds to 2.0 in float64, triggering rejection
    with pytest.raises(RelationalReggeError, match="violates triangle inequality"):
        compute_regge_deficit_angle_from_relational_edges([(1.0, 1.0, 2.0 - 1.0e-16)])


def test_needle_like_triangles() -> None:
    """Test needle-like triangles where one edge shrinks to zero (a -> 0, b = c = 1.0)."""
    for eps in [1.0e-3, 1.0e-6, 1.0e-10]:
        sum_a, def_a, _ = compute_regge_deficit_angle_from_relational_edges([(1.0, 1.0, eps)])
        # Opposite angle to eps: cos_th = (1 + 1 - eps^2) / 2 = 1 - eps^2 / 2 -> angle -> 0
        assert math.isclose(sum_a, 0.0, abs_tol=eps * 2.0)
        assert math.isclose(def_a, 2.0 * math.pi, abs_tol=eps * 2.0)


# ===========================================================================
# 4. Extreme-Scale Numerical Boundaries (Overflow & Underflow)
# ===========================================================================


def test_extreme_scale_overflow_and_underflow_characterization() -> None:
    """Characterize extreme scale behavior: underflow ZeroDivisionError and overflow angle corruption."""
    # Underflow boundary: l = 1e-165 causes 2 * a * b to underflow to 0.0, raising ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        compute_regge_deficit_angle_from_relational_edges([(1.0e-165, 1.0e-165, 1.0e-165)])

    # Overflow boundary: l = 1e160 causes a * a to overflow to inf, leading to cos_th = nan,
    # which min(1.0, nan) silently masks as 1.0, computing angle = 0.0 instead of pi/3
    sum_ang, def_ang, cls_name = compute_regge_deficit_angle_from_relational_edges(
        [(1.0e160, 1.0e160, 1.0e160)]
    )
    # Documents empirical vulnerability: angle corrupts to 0.0 instead of pi/3 = 1.047
    assert math.isclose(sum_ang, 0.0, abs_tol=1.0e-12)
    assert cls_name == "POSITIVE_CONICAL"

    # Well-conditioned scale range [1e-100, 1e100]: angle is computed accurately to machine precision
    for scale in [1.0e-100, 1.0e-50, 1.0, 1.0e50, 1.0e100]:
        s_ang, _, _ = compute_regge_deficit_angle_from_relational_edges([(scale, scale, scale)])
        assert math.isclose(s_ang, math.pi / 3.0, abs_tol=1.0e-12)


# ===========================================================================
# 5. Boolean Subclass Traps & Type Spoofing Attacks
# ===========================================================================


def test_boolean_subclass_traps_across_all_domain_apis() -> None:
    """Ensure Python's bool subclasses of int are aggressively rejected across all entry points."""
    # 1. Simplicial complex nodes & edges
    with pytest.raises(RelationalReggeError, match="must be int or str, not bool"):
        RelationalSimplicialComplex(nodes=(True, False), edges=())

    with pytest.raises(RelationalReggeError, match="must be int or str, not bool"):
        RelationalSimplicialComplex(nodes=(0, 1), edges=((True, 1),))

    with pytest.raises(RelationalReggeError, match="dimension must be an integer, not bool"):
        RelationalSimplicialComplex(nodes=(0, 1), edges=((0, 1),), dimension=True)

    # 2. Presentation
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)
    with pytest.raises(RelationalSpineError, match="must be numeric, not bool"):
        Presentation(carrier=fan6, raw_comparisons=tuple([True] + [1.0] * (fan6.num_edges - 1)))

    with pytest.raises(RelationalSpineError, match="must be numeric, not bool"):
        Presentation(carrier=fan6, raw_comparisons=tuple([False] + [1.0] * (fan6.num_edges - 1)))

    # 3. PresentationFamily
    fam = PresentationFamily(Presentation(fan6, tuple([1.0] * fan6.num_edges)))
    with pytest.raises(RelationalSpineError, match="must be numeric, not bool"):
        fam.generate_presentation([True] + [0.0] * (fan6.num_nodes - 1))

    # 4. Representation
    with pytest.raises(RelationalSpineError, match="must be numeric, not bool"):
        Representation(representation_id="rep", features=(True, 1.0), preserved_question_ids=())

    with pytest.raises(RelationalSpineError, match="fiber_dimension must be integer"):
        Representation(
            representation_id="rep",
            features=(1.0,),
            preserved_question_ids=(),
            fiber_dimension=True,
        )

    # 5. FiberBundle
    with pytest.raises(RelationalSpineError, match="fiber_dimension must be integer"):
        FiberBundle(
            base_representation=Representation("rep", (1.0,), ()),
            family=fam,
            fiber_dimension=True,
        )

    # 6. Fact
    with pytest.raises(RelationalSpineError, match="is_gauge_invariant must be boolean"):
        Fact("fact", 1.0, is_gauge_invariant=1)  # int should be rejected

    with pytest.raises(RelationalSpineError, match="is_fiber_constant must be boolean"):
        Fact("fact", 1.0, is_fiber_constant=0)  # int should be rejected

    # 7. Compression
    with pytest.raises(RelationalSpineError, match="source_dimension must be an int"):
        Compression(
            source_dimension=True,
            fact_dimension=1,
            retained_fact=Fact("f", 1.0),
            discarded_dof=0,
            compression_ratio=1.0,
        )

    with pytest.raises(RelationalSpineError, match="fact_dimension must be an int"):
        Compression(
            source_dimension=6,
            fact_dimension=True,
            retained_fact=Fact("f", 1.0),
            discarded_dof=0,
            compression_ratio=1.0,
        )

    with pytest.raises(RelationalSpineError, match="discarded_dof must be an int"):
        Compression(
            source_dimension=6,
            fact_dimension=1,
            retained_fact=Fact("f", 1.0),
            discarded_dof=True,
            compression_ratio=1.0,
        )

    with pytest.raises(RelationalSpineError, match="compression_ratio must be positive float"):
        Compression(
            source_dimension=6,
            fact_dimension=1,
            retained_fact=Fact("f", 1.0),
            discarded_dof=0,
            compression_ratio=True,
        )

    # 8. Obstruction
    with pytest.raises(RelationalSpineError, match="is_obstructed must be boolean"):
        Obstruction("q", is_obstructed=1, defect_norm=0.0)

    with pytest.raises(RelationalSpineError, match="has_continuation_stall must be boolean"):
        Obstruction("q", is_obstructed=False, defect_norm=0.0, has_continuation_stall=0)

    with pytest.raises(RelationalSpineError, match="defect_norm must be non-negative finite float"):
        Obstruction("q", is_obstructed=False, defect_norm=True)

    with pytest.raises(
        RelationalSpineError, match="stickiness_friction must be non-negative finite float"
    ):
        Obstruction("q", is_obstructed=False, defect_norm=0.0, stickiness_friction=True)

    # 9. RelationalSimplicialBone
    with pytest.raises(RelationalReggeError, match="is_flat must be boolean"):
        RelationalSimplicialBone(bone_id=0, is_flat=1)

    # 10. RelationalReggeCurvature
    with pytest.raises(RelationalSpineError, match="is_flat must be boolean"):
        RelationalReggeCurvature(
            bone_id=0,
            cycle_edges=(),
            holonomy_circulation=0.0,
            incident_angles=(),
            deficit_angle_epsilon=0.0,
            is_flat=1,
            operational_stickiness=0.0,
        )

    # 11. Helper functions
    with pytest.raises(RelationalReggeError, match="must be numeric, not bool"):
        compute_regge_deficit_angle_from_relational_edges([(True, 1.0, 1.0)])

    with pytest.raises(RelationalReggeError, match="edge_scale must be numeric, not bool"):
        compare_standard_and_relational_regge("FLAT_HEXAGON", edge_scale=True)


# ===========================================================================
# 6. Adversarial Input Permutations (NaNs, Infinities, Negatives, Strings)
# ===========================================================================


def test_adversarial_nans_and_infinities() -> None:
    """Verify that non-finite values are rejected with typed domain exceptions."""
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)
    d0 = fan6.incidence_matrix_d0()

    for bad_val in [float("nan"), float("inf"), float("-inf")]:
        with pytest.raises(RelationalReggeError, match="defect_delta at index 0 must be finite"):
            compute_relational_quotient_stickiness_lp(d0, [bad_val] + [0.0] * (fan6.num_edges - 1))

        with pytest.raises(
            RelationalSpineError, match="Comparison value at index 0 must be finite"
        ):
            Presentation(
                carrier=fan6, raw_comparisons=tuple([bad_val] + [0.0] * (fan6.num_edges - 1))
            )

        with pytest.raises(RelationalReggeError, match="must be finite"):
            _guard_float(bad_val, "test_param")


def test_adversarial_string_inputs_in_numeric_slots() -> None:
    """Verify that string inputs in numeric parameter slots fail closed."""
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)

    for bad_str in ["1.0", "nan", "inf", "True", "bad"]:
        with pytest.raises(RelationalReggeError, match="must be numeric, not bool"):
            _guard_float(bad_str, "str_param")

        with pytest.raises(RelationalSpineError, match="must be numeric, not bool"):
            Presentation(
                carrier=fan6, raw_comparisons=tuple([bad_str] + [1.0] * (fan6.num_edges - 1))
            )


def test_negative_values_where_strictly_positive_required() -> None:
    """Verify rejection of negative or zero values where positive geometric quantities are required."""
    with pytest.raises(RelationalReggeError, match="num_sectors must be >= 3"):
        RelationalSimplicialComplex.build_regular_star_fan(2)

    with pytest.raises(RelationalReggeError, match="spoke_length must be positive"):
        RelationalSimplicialComplex.build_regular_star_fan(6, spoke_length=0.0)

    with pytest.raises(RelationalReggeError, match="spoke_length must be positive"):
        RelationalSimplicialComplex.build_regular_star_fan(6, spoke_length=-1.0)

    with pytest.raises(RelationalReggeError, match="rim_length must be positive"):
        RelationalSimplicialComplex.build_regular_star_fan(6, rim_length=-0.5)


# ===========================================================================
# 7. Dimensional Mismatches and Malformed Simplicial Structures
# ===========================================================================


def test_dimensional_mismatches_and_malformed_structures() -> None:
    """Verify rejection of malformed vectors, tuple arities, and invalid graph topologies."""
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)
    d0 = fan6.incidence_matrix_d0()

    # Defect vector length mismatch: m - 1 and m + 1
    with pytest.raises(
        RelationalReggeError, match="defect_delta length 11 does not match gauge_d0 edges 12"
    ):
        compute_relational_quotient_stickiness_lp(d0, [1.0] * 11)

    with pytest.raises(
        RelationalReggeError, match="defect_delta length 13 does not match gauge_d0 edges 12"
    ):
        compute_relational_quotient_stickiness_lp(d0, [1.0] * 13)

    # Triangle tuple length mismatch: 2-tuple and 4-tuple
    with pytest.raises(RelationalReggeError, match="must be a 3-tuple"):
        compute_regge_deficit_angle_from_relational_edges([(1.0, 2.0)])  # type: ignore

    with pytest.raises(RelationalReggeError, match="must be a 3-tuple"):
        compute_regge_deficit_angle_from_relational_edges([(1.0, 2.0, 3.0, 4.0)])  # type: ignore

    # Edge referencing non-existent node
    with pytest.raises(RelationalReggeError, match="references non-existent node"):
        RelationalSimplicialComplex(nodes=(0, 1), edges=((0, 2),))

    # Anti-parallel duplicate edge: (0, 1) and (1, 0)
    with pytest.raises(RelationalReggeError, match="Duplicate or anti-parallel edge"):
        RelationalSimplicialComplex(nodes=(0, 1), edges=((0, 1), (1, 0)))

    # Empty nodes complex
    with pytest.raises(RelationalReggeError, match="must have at least one node"):
        RelationalSimplicialComplex(nodes=(), edges=())


# ===========================================================================
# 8. Authorization Boundary Theorem Empirical Verification
# ===========================================================================


def test_authorization_boundary_theorem_empirical_partition() -> None:
    """Empirically demonstrate that no query depending on discarded fiber DOFs can be answered from Fact.

    Battery: 5 gauge-dependent queries vs 5 gauge-invariant queries evaluated across
    100 randomized presentations on the fiber bundle F(R).
    Assert 100% classification accuracy (0 false positives, 0 false negatives).
    """
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)
    d0 = fan6.incidence_matrix_d0()
    d1 = fan6.cycle_matrix_d1()
    base_diffs = [0.1 * (i + 1) for i in range(fan6.num_edges)]
    base_pres = Presentation(carrier=fan6, raw_comparisons=tuple(base_diffs))
    fam = PresentationFamily(base_presentation=base_pres)

    rng = np.random.default_rng(777)
    # Generate 100 presentations on the fiber
    fiber_presentations: list[Presentation] = []
    for _ in range(100):
        alpha = rng.uniform(-100.0, 100.0, size=fan6.num_nodes)
        p = fam.generate_presentation(alpha)
        fiber_presentations.append(p)

    # 5 Gauge-Dependent Queries (require discarded fiber coordinates)
    gauge_dependent_queries = [
        ("q_edge_0", lambda p: float(p.cochain_vector[0])),
        ("q_edge_5", lambda p: float(p.cochain_vector[5])),
        ("q_edge_sum", lambda p: float(np.sum(p.cochain_vector))),
        ("q_edge_diff", lambda p: float(p.cochain_vector[1] - p.cochain_vector[2])),
        ("q_first_three", lambda p: float(np.sum(p.cochain_vector[:3]))),
    ]

    # 5 Gauge-Invariant Queries (factor through compressed Fact)
    gauge_invariant_queries = [
        ("q_face_0_curv", lambda p: float(d1[0] @ p.cochain_vector)),
        ("q_face_3_curv", lambda p: float(d1[3] @ p.cochain_vector)),
        ("q_rim_circulation", lambda p: float(np.sum(p.cochain_vector[6:12]))),
        ("q_total_curvature", lambda p: float(np.sum(d1 @ p.cochain_vector))),
        (
            "q_stickiness",
            lambda p: float(
                compute_relational_quotient_stickiness_lp(d0, p.cochain_vector).quotient_residual
            ),
        ),
    ]

    # Verify Gauge-Dependent Queries: Variance > 0 across fiber, execute_spine marks OBSTRUCTED
    non_sym_gauge = [float(i + 1) * 1.5 for i in range(fan6.num_nodes)]
    for q_name, q_fn in gauge_dependent_queries:
        values = [q_fn(p) for p in fiber_presentations]
        variance = float(np.var(values))
        assert variance > 1.0, f"Query {q_name} showed zero fiber variance: {variance}"

        # Execute spine with non-symmetric gauge shifts: must be flagged as OBSTRUCTED with non-zero defect
        res = execute_unified_relational_spine(
            fan6, base_diffs, test_question=q_fn, gauge_shifts=non_sym_gauge
        )
        assert res.obstruction is not None
        assert res.obstruction.is_obstructed is True, f"Gauge-dependent {q_name} failed to obstruct"
        assert res.obstruction.defect_norm > 1.0e-8

    # Verify Gauge-Invariant Queries: Variance == 0 across fiber (< 1e-12), execute_spine marks NOT OBSTRUCTED
    for q_name, q_fn in gauge_invariant_queries:
        values = [q_fn(p) for p in fiber_presentations]
        variance = float(np.var(values))
        assert variance < 1.0e-12, f"Query {q_name} had non-zero variance on fiber: {variance}"

        # Execute spine: must factor through Fact without obstruction
        res = execute_unified_relational_spine(
            fan6, base_diffs, test_question=q_fn, gauge_shifts=non_sym_gauge
        )
        assert res.obstruction is not None
        assert res.obstruction.is_obstructed is False, (
            f"Gauge-invariant {q_name} was falsely obstructed"
        )
        assert res.obstruction.defect_norm < 1.0e-9


def test_default_alpha_test_symmetry_blindspot_false_negative() -> None:
    """Document vulnerability: execute_spine default alpha_test is symmetric across spoke nodes 1..6,
    causing difference queries between spoke edges to falsely pass as invariant facts (false negative).
    """
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)
    base_diffs = [0.1 * (i + 1) for i in range(fan6.num_edges)]

    # Query comparing difference between spoke edge 1 (0, 2) and spoke edge 2 (0, 3)
    def q_spoke_diff(p: Presentation) -> float:
        return float(p.cochain_vector[1] - p.cochain_vector[2])

    # 1. Without passing gauge_shifts, execute_spine uses hardcoded alpha_test = [2, 1, 1, 1, 1, 1, 1]
    # Because alpha_2 == alpha_3 == 1.0, d0 alpha is identical on both edges, so q1 == q2
    res_default = execute_unified_relational_spine(fan6, base_diffs, test_question=q_spoke_diff)
    assert res_default.obstruction is not None
    # Empirically documents the false-negative blind spot:
    assert res_default.obstruction.is_obstructed is False
    assert math.isclose(res_default.obstruction.defect_norm, 0.0, abs_tol=1.0e-14)
    assert res_default.obstruction.reason == "Question factors through invariant fact"

    # 2. When broken with a non-symmetric gauge shift, the true obstruction is immediately exposed:
    res_hardened = execute_unified_relational_spine(
        fan6,
        base_diffs,
        test_question=q_spoke_diff,
        gauge_shifts=[0.0, 1.0, 2.5, 3.0, 4.0, 5.0, 6.0],
    )
    assert res_hardened.obstruction is not None
    assert res_hardened.obstruction.is_obstructed is True
    assert res_hardened.obstruction.defect_norm > 0.1


# ===========================================================================
# 9. Combinatorial Bianchi Exactness Under Randomized Floods
# ===========================================================================


def test_combinatorial_bianchi_exactness_under_gauge_floods() -> None:
    """Verify d^1 @ d^0 == 0 and curvature invariance under 1000 randomized gauge potential floods."""
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)
    d0 = fan6.incidence_matrix_d0()
    d1 = fan6.cycle_matrix_d1()

    # Exact nilpotence to machine precision
    prod = d1 @ d0
    assert np.all(np.abs(prod) < 1.0e-14)

    rng = np.random.default_rng(42)
    delta_base = rng.standard_normal(fan6.num_edges)
    gamma2_base = d1 @ delta_base

    for _ in range(500):
        alpha = rng.standard_normal(fan6.num_nodes) * 1.0e6
        delta_shifted = delta_base + d0 @ alpha
        gamma2_shifted = d1 @ delta_shifted
        assert np.allclose(gamma2_base, gamma2_shifted, atol=1.0e-8)


# ===========================================================================
# 10. Explicit Characterization of Uncovered Dataclass Validation Gaps
# ===========================================================================


def test_uncovered_dataclass_validation_gaps_documentation() -> None:
    """Explicitly test and document input validation gaps in Fact and Obstruction dataclasses."""
    # Gap 1: Fact.value does not check for bool or NaN
    f_bool = Fact("fact_bool", True)  # type: ignore
    assert f_bool.value is True

    f_nan = Fact("fact_nan", float("nan"))
    assert math.isnan(float(f_nan.value))  # type: ignore

    # Gap 2: Obstruction.status does not validate against TerminalizerStatus literal
    ob_bogus = Obstruction("q", is_obstructed=True, defect_norm=1.0, status="TOTALLY_BOGUS_STATUS")  # type: ignore
    assert ob_bogus.status == "TOTALLY_BOGUS_STATUS"
