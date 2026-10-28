//! Integration Tests for Target P5: 2D Nerve Boundary Cocycle & Collar Chaining.
//!
//! AuthorityEffect: None
//!
//! Lev Landau rigor: exact rational arithmetic, Network Simplex duality gap verification,
//! gauge invariance, and comprehensive negative control falsification.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};

use tfqm_mub::native::exact::mub6_constants::certified_margin;
use tfqm_mub::native::exact::mub6_global_gluing::{
    circulation_gamma_threshold, is_nerve1, is_nerve2, ModuliChart5,
};
use tfqm_mub::native::exact::mub6_nerve_chaining::{
    build_canonical_collar_grid, connect_collar_box_to_nerve, evaluate_nerve_chaining,
    solve_triangular_circulation, verify_gauge_invariance, BoundaryNerveTriangle, CollarBox2D,
    CollarNerveChaining, CollarNerveInterfaceType, NerveChainingError, INTEGER_SCALE,
    SCALED_GAMMA_THRESHOLD,
};
use omega_number_theory::rational::rq;

// ==============================================================================
// 1. Certified Topological & Circulation Constants
// ==============================================================================

#[test]
fn test_certified_constants_exact_values() {
    let gamma = circulation_gamma_threshold();
    assert_eq!(*gamma.numer(), BigInt::from(12133));
    assert_eq!(*gamma.denom(), BigInt::from(5000));

    let eps_min = certified_margin();
    assert_eq!(*eps_min.numer(), BigInt::from(12133));
    assert_eq!(*eps_min.denom(), BigInt::from(30000));

    // Fundamental relation: 6 · ε_min = Γ
    let six = BigRational::from_integer(BigInt::from(6));
    assert_eq!(&six * &eps_min, gamma);

    // Scale consistency
    let scale_rat = BigRational::from_integer(BigInt::from(INTEGER_SCALE));
    assert_eq!(
        &gamma * &scale_rat,
        BigRational::from_integer(BigInt::from(SCALED_GAMMA_THRESHOLD))
    );
}

// ==============================================================================
// 2. Boundary Nerve Triangles N_2
// ==============================================================================

#[test]
fn test_boundary_nerve_triangles_structure() {
    let deltoid = BoundaryNerveTriangle::deltoid();
    assert_eq!(
        deltoid.nodes,
        [
            ModuliChart5::SzollosiCurve,
            ModuliChart5::KarlssonManifold,
            ModuliChart5::DeltoidCusps,
        ]
    );
    assert!(is_nerve2(
        deltoid.nodes[0],
        deltoid.nodes[1],
        deltoid.nodes[2]
    ));

    let tao = BoundaryNerveTriangle::tao();
    assert_eq!(
        tao.nodes,
        [
            ModuliChart5::SzollosiCurve,
            ModuliChart5::KarlssonManifold,
            ModuliChart5::TaoConfluence,
        ]
    );
    assert!(is_nerve2(tao.nodes[0], tao.nodes[1], tao.nodes[2]));

    // Check boundary edges
    for &(u, v) in &deltoid.directed_edges() {
        assert!(is_nerve1(u, v));
    }
    for &(u, v) in &tao.directed_edges() {
        assert!(is_nerve1(u, v));
    }

    // Canonical defects sum to Gamma
    let defects_d = deltoid.canonical_edge_defects();
    let sum_d = &defects_d[0] + &defects_d[1] + &defects_d[2];
    assert_eq!(sum_d, circulation_gamma_threshold());

    let defects_t = tao.canonical_edge_defects();
    let sum_t = &defects_t[0] + &defects_t[1] + &defects_t[2];
    assert_eq!(sum_t, circulation_gamma_threshold());
}

// ==============================================================================
// 3. 2D Periodic Collar Coordinate Boxes
// ==============================================================================

#[test]
fn test_collar_box_2d_properties() {
    let unit = CollarBox2D::unit_square();
    assert_eq!(unit.area(), BigRational::one());
    assert_eq!(unit.center(), [rq(1, 2), rq(1, 2)]);
    assert!(unit.contains_point(&[rq(1, 4), rq(3, 4)]));
    assert!(unit.contains_point(&[rq(0, 1), rq(0, 1)]));
    assert!(unit.contains_point(&[rq(1, 1), rq(1, 1)]));
    assert!(!unit.contains_point(&[rq(3, 2), rq(1, 2)]));

    // Splitting
    let (left, right) = unit.split_dim(0, &rq(1, 2)).unwrap();
    assert_eq!(left.area(), rq(1, 2));
    assert_eq!(right.area(), rq(1, 2));
    assert_eq!(&left.area() + &right.area(), BigRational::one());
}

#[test]
fn test_build_canonical_collar_grid_area_conservation() {
    for &div in &[1, 2, 4] {
        let grid = build_canonical_collar_grid(div).unwrap();
        assert_eq!(grid.len(), div * div);
        let mut total_area = BigRational::zero();
        for b in &grid {
            total_area += b.area();
        }
        assert_eq!(total_area, BigRational::one());
    }
}

// ==============================================================================
// 4. Collar-to-Nerve Chaining Connection
// ==============================================================================

#[test]
fn test_collar_to_nerve_connection_and_chaining() {
    let box_d = CollarBox2D::new(
        [(rq(0, 1), rq(1, 4)), (rq(0, 1), rq(1, 4))],
        "box_d".to_string(),
    )
    .unwrap();
    let binding_d = connect_collar_box_to_nerve(box_d, None).unwrap();
    assert_eq!(binding_d.triangle, BoundaryNerveTriangle::deltoid());
    assert_eq!(
        binding_d.interface_type,
        CollarNerveInterfaceType::DeltoidBoundary
    );

    let box_t = CollarBox2D::new(
        [(rq(3, 4), rq(1, 1)), (rq(0, 1), rq(1, 4))],
        "box_t".to_string(),
    )
    .unwrap();
    let binding_t = connect_collar_box_to_nerve(box_t, None).unwrap();
    assert_eq!(binding_t.triangle, BoundaryNerveTriangle::tao());
    assert_eq!(
        binding_t.interface_type,
        CollarNerveInterfaceType::TaoBoundary
    );

    let chaining = CollarNerveChaining::from_grid(2).unwrap();
    assert_eq!(chaining.bindings.len(), 4);
    assert_eq!(chaining.total_area, BigRational::one());
}

// ==============================================================================
// 5. Network Simplex Discrete Cycle Circulation Solver
// ==============================================================================

#[test]
fn test_solve_triangular_circulation_canonical_deltoid() {
    let tri = BoundaryNerveTriangle::deltoid();
    let rep = solve_triangular_circulation(&tri, None, INTEGER_SCALE).unwrap();

    assert_eq!(rep.triangle_name, "delta_deltoid_0_1_2");
    assert_eq!(rep.nodes, [0, 1, 2]);
    assert_eq!(rep.edges, [(0, 1), (1, 2), (2, 0)]);
    assert!(rep.circulation_conserved);
    assert!(rep.dual_gap_zero);
    assert_eq!(rep.coboundary_sum_scaled, 0);
    assert_eq!(rep.phi1_objective_scaled, SCALED_GAMMA_THRESHOLD);
    assert_eq!(rep.net_circulation_scaled, SCALED_GAMMA_THRESHOLD);
    assert_eq!(rep.phi1_rational, circulation_gamma_threshold());
    assert!(rep.phi1_ge_gamma);
}

#[test]
fn test_solve_triangular_circulation_canonical_tao() {
    let tri = BoundaryNerveTriangle::tao();
    let rep = solve_triangular_circulation(&tri, None, INTEGER_SCALE).unwrap();

    assert_eq!(rep.triangle_name, "delta_tao_0_1_4");
    assert_eq!(rep.nodes, [0, 1, 4]);
    assert_eq!(rep.edges, [(0, 1), (1, 4), (4, 0)]);
    assert!(rep.circulation_conserved);
    assert!(rep.dual_gap_zero);
    assert_eq!(rep.coboundary_sum_scaled, 0);
    assert_eq!(rep.phi1_objective_scaled, SCALED_GAMMA_THRESHOLD);
    assert_eq!(rep.net_circulation_scaled, SCALED_GAMMA_THRESHOLD);
    assert_eq!(rep.phi1_rational, circulation_gamma_threshold());
    assert!(rep.phi1_ge_gamma);
}

#[test]
fn test_solve_triangular_circulation_with_custom_positive_defects() {
    let tri = BoundaryNerveTriangle::deltoid();
    // Non-uniform defects with sum = 3 > 12133/5000 = 2.4266
    let custom = [rq(1, 1), rq(1, 1), rq(1, 1)];
    let rep = solve_triangular_circulation(&tri, Some(custom), INTEGER_SCALE).unwrap();

    assert_eq!(rep.phi1_rational, rq(3, 1));
    assert!(rep.phi1_ge_gamma);
    assert!(rep.dual_gap_zero);
    assert!(rep.circulation_conserved);
}

#[test]
fn test_gauge_invariance_under_arbitrary_0_cochain() {
    let tri = BoundaryNerveTriangle::deltoid();
    let test_potentials = [[100, 200, 300], [-500, 1200, 800], [10000, 0, -5000]];

    for &alpha in &test_potentials {
        let invariant = verify_gauge_invariance(&tri, &alpha, None, INTEGER_SCALE).unwrap();
        assert!(invariant);
    }
}

// ==============================================================================
// 6. Master Evaluation & Full Coverage
// ==============================================================================

#[test]
fn test_evaluate_nerve_chaining_master() {
    let master = evaluate_nerve_chaining(2, INTEGER_SCALE).unwrap();
    assert_eq!(master.num_collar_boxes, 4);
    assert!(master.area_conserved);
    assert!(master.all_phi1_ge_gamma);
    assert!(master.all_circulation_conserved);
    assert!(master.all_dual_gaps_zero);
    assert!(master.min_phi1_rational >= master.gamma_threshold);
    assert_eq!(master.triangular_reports.len(), 2);
    assert!(!master.mathematical_certification);
    assert!(!master.collar_overlap_verified);
    assert!(!master.curvature_to_cochain_verified);
}

#[test]
fn test_nonintegral_scaled_defect_is_not_truncated() {
    let tri = BoundaryNerveTriangle::deltoid();
    let defects = [rq(1, 7), rq(1, 1), rq(2, 1)];
    let err = solve_triangular_circulation(&tri, Some(defects), INTEGER_SCALE);
    assert!(matches!(err, Err(NerveChainingError::InvalidParameter(_))));
}

#[test]
fn test_degenerate_chart_triple_is_not_a_nerve_triangle() {
    let nodes = [ModuliChart5::KarlssonManifold; 3];
    assert!(matches!(
        BoundaryNerveTriangle::new("degenerate".to_string(), nodes),
        Err(NerveChainingError::InvalidNerveTriangle(..))
    ));
}

#[test]
fn test_out_of_range_scaled_defect_is_rejected() {
    let tri = BoundaryNerveTriangle::deltoid();
    let huge = BigRational::from_integer(BigInt::from(i128::MAX));
    let err = solve_triangular_circulation(&tri, Some([huge, rq(1, 1), rq(2, 1)]), INTEGER_SCALE);
    assert!(matches!(err, Err(NerveChainingError::InvalidParameter(_))));
}

// ==============================================================================
// 7. Negative Controls & Falsification
// ==============================================================================

#[test]
fn test_negative_control_vanishing_circulation_rejected() {
    let tri = BoundaryNerveTriangle::deltoid();
    let zero_defects = [rq(0, 1), rq(0, 1), rq(0, 1)];
    let err = solve_triangular_circulation(&tri, Some(zero_defects), INTEGER_SCALE);
    assert!(matches!(
        err,
        Err(NerveChainingError::NonPositiveCirculation { .. })
    ));
}

#[test]
fn test_negative_control_sub_threshold_circulation_rejected() {
    let tri = BoundaryNerveTriangle::deltoid();
    // Sum = 1 < 12133/5000
    let sub_defects = [rq(1, 3), rq(1, 3), rq(1, 3)];
    let err = solve_triangular_circulation(&tri, Some(sub_defects), INTEGER_SCALE);
    assert!(matches!(
        err,
        Err(NerveChainingError::SubThresholdCirculation { .. })
    ));
}

#[test]
fn test_negative_control_invalid_nerve2_triangle_rejected() {
    // Charts 2, 3 do not overlap in Nerve1
    let err = BoundaryNerveTriangle::new(
        "invalid_0_2_3".to_string(),
        [
            ModuliChart5::SzollosiCurve,
            ModuliChart5::DeltoidCusps,
            ModuliChart5::HaagerupOrbit,
        ],
    );
    assert!(matches!(
        err,
        Err(NerveChainingError::InvalidNerveTriangle(..))
    ));
}

#[test]
fn test_negative_control_degenerate_collar_box_rejected() {
    // lo >= hi
    let err1 = CollarBox2D::new(
        [(rq(1, 2), rq(1, 4)), (rq(0, 1), rq(1, 1))],
        "bad1".to_string(),
    );
    assert!(matches!(
        err1,
        Err(NerveChainingError::DegenerateBox { .. })
    ));

    // Out of [0, 1]
    let err2 = CollarBox2D::new(
        [(rq(-1, 2), rq(1, 2)), (rq(0, 1), rq(1, 1))],
        "bad2".to_string(),
    );
    assert!(matches!(
        err2,
        Err(NerveChainingError::BoxOutOfBounds { .. })
    ));
}

#[test]
fn test_negative_control_orientation_mismatch_rejected() {
    // Edge (Karlsson, Szollosi) is reversed from canonical orientation
    let mismatched_edges = [
        (ModuliChart5::KarlssonManifold, ModuliChart5::SzollosiCurve),
        (ModuliChart5::KarlssonManifold, ModuliChart5::DeltoidCusps),
        (ModuliChart5::DeltoidCusps, ModuliChart5::SzollosiCurve),
    ];
    let err = BoundaryNerveTriangle::from_directed_edges(
        "mismatched_deltoid".to_string(),
        mismatched_edges,
    );
    assert!(matches!(
        err,
        Err(NerveChainingError::OrientationMismatch(..))
    ));
}
