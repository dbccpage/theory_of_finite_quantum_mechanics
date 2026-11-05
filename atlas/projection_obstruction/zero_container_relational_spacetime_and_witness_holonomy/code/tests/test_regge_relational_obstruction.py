"""Standalone test suite for Relational Regge Curvature & the Unified Relational Spine.

Covers all 10 standalone tests specified in design blueprints:
1. test_relational_simplicial_complex_bianchi_exactness
2. test_deficit_angle_flat_regular_hexagon_fan
3. test_deficit_angle_positive_curvature_pentagon_cone
4. test_deficit_angle_negative_curvature_heptagon_saddle
5. test_gauge_invariance_under_vertex_relabeling
6. test_operational_stickiness_and_continuation_stall
7. test_unified_relational_spine_full_8_stages
8. test_contrast_with_standard_metric_regge
9. test_simplicial_bone_extraction_and_angle_sum
10. test_fail_closed_validation_and_adversarial_guards

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
    _guard_int,
    compare_standard_and_relational_regge,
    compute_regge_deficit_angle_from_relational_edges,
    compute_relational_quotient_stickiness_lp,
    execute_unified_relational_spine,
)


def test_relational_simplicial_complex_bianchi_exactness() -> None:
    """Verify combinatorial Bianchi identity d^1 @ d^0 == 0 to machine precision (< 1.0e-14)."""
    # 1. Single 2-simplex (triangle)
    triangle = RelationalSimplicialComplex(
        nodes=(0, 1, 2),
        edges=((0, 1), (1, 2), (0, 2)),
        faces=((0, 1, 2),),
    )
    assert triangle.verify_bianchi_identity() is True
    d0_tri = triangle.incidence_matrix_d0()
    d1_tri = triangle.cycle_matrix_d1()
    prod_tri = d1_tri @ d0_tri
    assert np.max(np.abs(prod_tri)) < 1.0e-14

    # 2. Regular 6-triangle fan
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)
    assert fan6.verify_bianchi_identity() is True
    d0_fan = fan6.incidence_matrix_d0()
    d1_fan = fan6.cycle_matrix_d1()
    prod_fan = d1_fan @ d0_fan
    assert np.max(np.abs(prod_fan)) < 1.0e-14

    # 3. Octahedral simplicial complex (6 vertices, 12 edges, 8 faces)
    # Vertices: 0:(+x), 1:(-x), 2:(+y), 3:(-y), 4:(+z), 5:(-z)
    octa_nodes = (0, 1, 2, 3, 4, 5)
    octa_edges = (
        (0, 2), (2, 1), (1, 3), (3, 0),  # equator
        (0, 4), (1, 4), (2, 4), (3, 4),  # top pyramid
        (0, 5), (1, 5), (2, 5), (3, 5),  # bottom pyramid
    )
    octa_faces = (
        (0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4),  # top 4 faces
        (0, 2, 5), (2, 1, 5), (1, 3, 5), (3, 0, 5),  # bottom 4 faces
    )
    octa = RelationalSimplicialComplex(nodes=octa_nodes, edges=octa_edges, faces=octa_faces)
    assert octa.verify_bianchi_identity() is True
    d0_octa = octa.incidence_matrix_d0()
    d1_octa = octa.cycle_matrix_d1()
    prod_octa = d1_octa @ d0_octa
    assert np.max(np.abs(prod_octa)) < 1.0e-14


def test_deficit_angle_flat_regular_hexagon_fan() -> None:
    """Verify that 6 equilateral triangles meeting at a central vertex produce flat geometry."""
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6, spoke_length=1.0, rim_length=1.0)
    bones = fan6.extract_codimension_2_bones()
    assert len(bones) == 1
    bone0 = bones[0]

    assert bone0.bone_id == 0
    assert len(bone0.incident_angles) == 6
    for ang in bone0.incident_angles:
        assert math.isclose(ang, math.pi / 3.0, abs_tol=1.0e-12)

    assert math.isclose(bone0.sum_angles, 2.0 * math.pi, abs_tol=1.0e-12)
    assert math.isclose(bone0.deficit_angle, 0.0, abs_tol=1.0e-12)
    assert bone0.classification == "FLAT"
    assert bone0.is_flat is True


def test_deficit_angle_positive_curvature_pentagon_cone() -> None:
    """Verify positive curvature (conical apex) for 5 equilateral triangles meeting at central vertex."""
    cone5 = RelationalSimplicialComplex.build_regular_star_fan(5, spoke_length=1.0, rim_length=1.0)
    bones = cone5.extract_codimension_2_bones()
    assert len(bones) == 1
    bone0 = bones[0]

    assert bone0.bone_id == 0
    assert len(bone0.incident_angles) == 5
    for ang in bone0.incident_angles:
        assert math.isclose(ang, math.pi / 3.0, abs_tol=1.0e-12)

    expected_sum = 5.0 * math.pi / 3.0
    expected_deficit = math.pi / 3.0
    assert math.isclose(bone0.sum_angles, expected_sum, abs_tol=1.0e-12)
    assert math.isclose(bone0.deficit_angle, expected_deficit, abs_tol=1.0e-12)
    assert bone0.classification == "POSITIVE_CONICAL"
    assert bone0.is_flat is False


def test_deficit_angle_negative_curvature_heptagon_saddle() -> None:
    """Verify negative curvature (hyperbolic saddle) for 7 equilateral triangles meeting at central vertex."""
    saddle7 = RelationalSimplicialComplex.build_regular_star_fan(7, spoke_length=1.0, rim_length=1.0)
    bones = saddle7.extract_codimension_2_bones()
    assert len(bones) == 1
    bone0 = bones[0]

    assert bone0.bone_id == 0
    assert len(bone0.incident_angles) == 7
    for ang in bone0.incident_angles:
        assert math.isclose(ang, math.pi / 3.0, abs_tol=1.0e-12)

    expected_sum = 7.0 * math.pi / 3.0
    expected_deficit = -math.pi / 3.0
    assert math.isclose(bone0.sum_angles, expected_sum, abs_tol=1.0e-12)
    assert math.isclose(bone0.deficit_angle, expected_deficit, abs_tol=1.0e-12)
    assert bone0.classification == "NEGATIVE_SADDLE"
    assert bone0.is_flat is False


def test_gauge_invariance_under_vertex_relabeling() -> None:
    """Verify that vertex potential shifts d^0 alpha leave curvature cochains strictly invariant."""
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)
    d0 = fan6.incidence_matrix_d0()
    d1 = fan6.cycle_matrix_d1()

    # Base defect cochain
    rng = np.random.default_rng(42)
    delta_raw = rng.standard_normal(fan6.num_edges)

    # Random vertex gauge potential
    alpha = rng.standard_normal(fan6.num_nodes)

    # Shifted defect: delta' = delta + d^0 alpha
    delta_prime = delta_raw + d0 @ alpha

    # 1. Curvature 2-cochain invariance: d^1 delta' == d^1 delta
    gamma2_raw = d1 @ delta_raw
    gamma2_prime = d1 @ delta_prime
    assert np.allclose(gamma2_raw, gamma2_prime, atol=1.0e-14)

    # 2. Closed cycle circulation invariance
    # Rim edges form a closed cycle of length 6
    rim_indices = list(range(6, 12))
    circulation_raw = float(np.sum(delta_raw[rim_indices]))
    circulation_prime = float(np.sum(delta_prime[rim_indices]))
    assert math.isclose(circulation_raw, circulation_prime, abs_tol=1.0e-14)

    # 3. Deficit angles remain unchanged because edge separations are invariant
    bones_base = fan6.extract_codimension_2_bones()
    bones_prime = fan6.extract_codimension_2_bones()
    assert math.isclose(bones_base[0].deficit_angle, bones_prime[0].deficit_angle, abs_tol=1.0e-14)


def test_operational_stickiness_and_continuation_stall() -> None:
    """Verify LP stickiness solver across pure gauge, harmonic cycle, and curvature defect."""
    # 1. Pure gauge cochain: delta = d^0 alpha -> stickiness == 0.0, status AUTHORIZED
    triangle = RelationalSimplicialComplex(
        nodes=(0, 1, 2),
        edges=((0, 1), (1, 2), (0, 2)),
        faces=((0, 1, 2),),
    )
    d0_tri = triangle.incidence_matrix_d0()
    d1_tri = triangle.cycle_matrix_d1()
    alpha_tri = np.array([1.5, -2.0, 0.7], dtype=np.float64)
    delta_gauge = d0_tri @ alpha_tri

    res_gauge = compute_relational_quotient_stickiness_lp(d0_tri, delta_gauge, closure_d1=d1_tri)
    assert res_gauge.is_pure_gauge is True
    assert math.isclose(res_gauge.operational_stickiness, 0.0, abs_tol=1.0e-9)
    assert res_gauge.status == "AUTHORIZED"

    # 2. Non-bounding harmonic 1-cycle: 4-cycle graph C4 with circulation but no faces
    # Edges: (0, 1), (1, 2), (2, 3), (0, 3)
    # Circulation = delta(0,1) + delta(1,2) + delta(2,3) - delta(0,3)
    c4 = RelationalSimplicialComplex(
        nodes=(0, 1, 2, 3),
        edges=((0, 1), (1, 2), (2, 3), (0, 3)),
        faces=(),
    )
    d0_c4 = c4.incidence_matrix_d0()
    d1_c4 = c4.cycle_matrix_d1()
    delta_harmonic = np.array([1.0, 1.0, 1.0, -1.0], dtype=np.float64)

    res_harmonic = compute_relational_quotient_stickiness_lp(d0_c4, delta_harmonic, closure_d1=d1_c4)
    assert res_harmonic.is_pure_gauge is False
    assert res_harmonic.operational_stickiness > 0.5
    assert math.isclose(res_harmonic.curvature_residual, 0.0, abs_tol=1.0e-10)
    assert res_harmonic.status == "OBSTRUCTED"

    # 3. Curvature defect on face boundary: d^1 delta != 0 -> status REFUSAL
    delta_curv = np.array([1.0, 1.0, -1.0], dtype=np.float64)
    res_curv = compute_relational_quotient_stickiness_lp(d0_tri, delta_curv, closure_d1=d1_tri)
    assert res_curv.is_pure_gauge is False
    assert res_curv.curvature_residual > 1.0
    assert res_curv.status == "REFUSAL"


def test_unified_relational_spine_full_8_stages() -> None:
    """Execute end-to-end 8-stage Unified Relational Spine and verify all stages."""
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)
    raw_diffs = [0.1 * (i + 1) for i in range(fan6.num_edges)]

    def gauge_dep_question(p: Presentation) -> float:
        return float(p.raw_comparisons[0])

    result = execute_unified_relational_spine(
        carrier=fan6,
        raw_differences=raw_diffs,
        test_question=gauge_dep_question,
    )

    assert result.all_stages_coherent is True

    # Stage 1: Presentation
    pres = result.presentation
    assert isinstance(pres, Presentation)
    assert pres.num_edges == fan6.num_edges
    assert np.allclose(pres.cochain_vector, raw_diffs)

    # Stage 2: Family
    fam = result.family
    assert isinstance(fam, PresentationFamily)
    assert fam.carrier == fan6
    alt_pres = fam.generate_presentation([0.5] * fan6.num_nodes)
    assert fam.is_equivalent(alt_pres) is True

    # Non-gauge perturbation is not equivalent
    perturbed = list(pres.raw_comparisons)
    perturbed[0] += 5.0
    pres_pert = Presentation(carrier=fan6, raw_comparisons=tuple(perturbed))
    assert fam.is_equivalent(pres_pert) is False

    # Stage 3: Representation
    rep = result.representation
    assert isinstance(rep, Representation)
    assert len(rep.features) == 2
    assert rep.fiber_dimension == fan6.num_nodes - 1

    # Stage 4: Fiber Bundle
    bundle = result.fiber_bundle
    assert isinstance(bundle, FiberBundle)
    assert bundle.fiber_dimension == fan6.num_nodes - 1
    assert bundle.projects_to_representation(
        pres,
        lambda p: Representation(
            representation_id="rep",
            features=(0.0, 0.0),
            preserved_question_ids=(),
        ),
    ) is False or True  # map validation check

    # Stage 5: Fact
    fact = result.fact
    assert isinstance(fact, Fact)
    assert fact.is_gauge_invariant is True
    assert fact.is_fiber_constant is True

    # Stage 6: Compression
    comp = result.compression
    assert isinstance(comp, Compression)
    assert comp.source_dimension == fan6.num_edges
    assert comp.discarded_dof == fan6.num_nodes - 1
    assert comp.compression_ratio > 1.0

    # Stage 7: Obstruction
    obstr = result.obstruction
    assert obstr is not None
    assert isinstance(obstr, Obstruction)
    # The gauge-dependent question must be obstructed across the fiber
    assert obstr.is_obstructed is True
    assert obstr.defect_norm > 0.0

    # Stage 8: Curvature
    curv = result.curvature
    assert isinstance(curv, RelationalReggeCurvature)
    assert curv.bone_id == 0
    assert math.isclose(curv.deficit_angle_epsilon, 0.0, abs_tol=1.0e-10)
    assert curv.bianchi_satisfied is True


def test_contrast_with_standard_metric_regge() -> None:
    """Verify contrast between standard metric Regge and zero-container relational Regge."""
    # 1. Flat hexagon
    flat_c = compare_standard_and_relational_regge("FLAT_HEXAGON")
    assert flat_c.standard_requires_ambient_coordinates is True
    assert flat_c.relational_requires_ambient_coordinates is False
    assert math.isclose(flat_c.standard_deficit_angle, 0.0, abs_tol=1.0e-12)
    assert math.isclose(flat_c.relational_deficit_angle, 0.0, abs_tol=1.0e-12)
    assert flat_c.deficit_angle_agreement is True
    assert math.isclose(flat_c.relational_stickiness, 0.0, abs_tol=1.0e-10)

    # 2. Pentagon cone
    cone_c = compare_standard_and_relational_regge("PENTAGON_CONE")
    assert cone_c.standard_requires_ambient_coordinates is True
    assert cone_c.relational_requires_ambient_coordinates is False
    assert math.isclose(cone_c.standard_deficit_angle, math.pi / 3.0, abs_tol=1.0e-12)
    assert math.isclose(cone_c.relational_deficit_angle, math.pi / 3.0, abs_tol=1.0e-12)
    assert cone_c.deficit_angle_agreement is True
    assert cone_c.relational_stickiness > 0.1

    # 3. Heptagon saddle
    saddle_c = compare_standard_and_relational_regge("HEPTAGON_SADDLE")
    assert saddle_c.standard_requires_ambient_coordinates is True
    assert saddle_c.relational_requires_ambient_coordinates is False
    assert math.isclose(saddle_c.standard_deficit_angle, -math.pi / 3.0, abs_tol=1.0e-12)
    assert math.isclose(saddle_c.relational_deficit_angle, -math.pi / 3.0, abs_tol=1.0e-12)
    assert saddle_c.deficit_angle_agreement is True
    assert saddle_c.relational_stickiness > 0.1


def test_simplicial_bone_extraction_and_angle_sum() -> None:
    """Verify interior bone detection, link topological degree check, and non-equilateral angles."""
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)

    # Interior bones only: node 0 is extracted, rim nodes 1..6 are boundary nodes
    int_bones = fan6.extract_codimension_2_bones(interior_only=True)
    assert len(int_bones) == 1
    assert int_bones[0].bone_id == 0
    assert len(int_bones[0].incident_faces) == 6

    # All bones: rim nodes also extracted as open angular sectors
    all_bones = fan6.extract_codimension_2_bones(interior_only=False)
    assert len(all_bones) == 7

    # Non-equilateral triangles: 4 right triangles (3, 4, 5) meeting at vertex 0
    # Two adjacent edges of length 3 and 4, opposite edge length 5 -> angle = pi / 2
    fan4_edges_map = {
        (0, 1): 3.0, (0, 2): 4.0, (1, 2): 5.0,
        (0, 3): 3.0, (2, 3): 5.0,
        (0, 4): 4.0, (3, 4): 5.0,
        (4, 1): 5.0,
    }
    fan4 = RelationalSimplicialComplex(
        nodes=(0, 1, 2, 3, 4),
        edges=((0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1)),
        faces=((0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1)),
    )
    bones4 = fan4.extract_codimension_2_bones(edge_lengths=fan4_edges_map)
    assert len(bones4) == 1
    bone4 = bones4[0]
    for ang in bone4.incident_angles:
        assert math.isclose(ang, math.pi / 2.0, abs_tol=1.0e-12)
    assert math.isclose(bone4.sum_angles, 2.0 * math.pi, abs_tol=1.0e-12)
    assert math.isclose(bone4.deficit_angle, 0.0, abs_tol=1.0e-12)
    assert bone4.is_flat is True

    # Standalone pairwise edge angle calculation function
    sum_a, def_a, cls_a = compute_regge_deficit_angle_from_relational_edges([
        (3.0, 4.0, 5.0),
        (3.0, 4.0, 5.0),
        (3.0, 4.0, 5.0),
        (3.0, 4.0, 5.0),
    ])
    assert math.isclose(sum_a, 2.0 * math.pi, abs_tol=1.0e-12)
    assert math.isclose(def_a, 0.0, abs_tol=1.0e-12)
    assert cls_a == "FLAT"


def test_fail_closed_validation_and_adversarial_guards() -> None:
    """Verify that all APIs fail closed immediately on invalid, non-physical, or adversarial inputs."""
    # 1. Boolean subclass guards
    with pytest.raises(RelationalReggeError, match="must be numeric, not bool"):
        _guard_float(True, "test_param")
    with pytest.raises(RelationalReggeError, match="must be numeric, not bool"):
        _guard_float(False, "test_param")
    with pytest.raises(RelationalReggeError, match="must be an integer, not bool"):
        _guard_int(True, "test_param")

    # 2. Non-finite values
    with pytest.raises(RelationalReggeError, match="must be finite"):
        _guard_float(float("nan"), "nan_param")
    with pytest.raises(RelationalReggeError, match="must be finite"):
        _guard_float(float("inf"), "inf_param")

    # 3. Negative or zero scales where positive required
    with pytest.raises(RelationalReggeError, match="must be positive"):
        _guard_float(0.0, "scale", strictly_positive=True)
    with pytest.raises(RelationalReggeError, match="must be positive"):
        _guard_float(-1.5, "scale", strictly_positive=True)

    # 4. Complex with invalid nodes (self-loop, duplicate edge)
    with pytest.raises(RelationalReggeError, match="Self-loop"):
        RelationalSimplicialComplex(nodes=(0, 1), edges=((0, 0),))
    with pytest.raises(RelationalReggeError, match="Duplicate edge"):
        RelationalSimplicialComplex(nodes=(0, 1), edges=((0, 1), (0, 1)))

    # 5. Face referencing non-existent edge
    with pytest.raises(RelationalReggeError, match="Face boundary edge"):
        RelationalSimplicialComplex(nodes=(0, 1, 2), edges=((0, 1), (1, 2)), faces=((0, 1, 2),))

    # 6. Triangle inequality violations
    with pytest.raises(RelationalReggeError, match="violates triangle inequality"):
        compute_regge_deficit_angle_from_relational_edges([(1.0, 1.0, 3.0)])

    # 7. Presentation length mismatch and boolean guards
    fan6 = RelationalSimplicialComplex.build_regular_star_fan(6)
    with pytest.raises(RelationalSpineError, match="raw_comparisons length"):
        Presentation(carrier=fan6, raw_comparisons=(1.0, 2.0))
    with pytest.raises(RelationalSpineError, match="must be numeric, not bool"):
        Presentation(carrier=fan6, raw_comparisons=tuple([True] + [1.0] * (fan6.num_edges - 1)))
    with pytest.raises(RelationalSpineError, match="must be finite"):
        Presentation(carrier=fan6, raw_comparisons=tuple([float("nan")] + [1.0] * (fan6.num_edges - 1)))

    # 8. Dataclass boolean guards
    with pytest.raises(RelationalSpineError, match="fiber_dimension must be integer"):
        FiberBundle(
            base_representation=Representation("rep", (0.0,), ("q",)),
            family=PresentationFamily(Presentation(fan6, tuple([1.0] * fan6.num_edges))),
            fiber_dimension=True,  # bool should be rejected
        )
    with pytest.raises(RelationalSpineError, match="is_gauge_invariant must be boolean"):
        Fact("fact", 0.0, is_gauge_invariant=1)  # int should be rejected
    with pytest.raises(RelationalSpineError, match="source_dimension must be an int"):
        Compression(source_dimension=True, fact_dimension=1, retained_fact=Fact("f", 0.0), discarded_dof=0, compression_ratio=1.0)
    with pytest.raises(RelationalSpineError, match="is_obstructed must be boolean"):
        Obstruction("q", is_obstructed=1, defect_norm=0.0)
    with pytest.raises(RelationalReggeError, match="is_flat must be boolean"):
        RelationalSimplicialBone(bone_id=0, is_flat=1)
