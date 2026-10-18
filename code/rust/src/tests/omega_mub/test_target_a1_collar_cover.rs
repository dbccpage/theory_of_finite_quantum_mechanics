//! Integration and unit tests for Target A1: Full Collar Partition Cover & Network Simplex Acceleration.
//!
//! AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::{One, Zero};

use omega_mub::omega_native::exact::mub6_collar_cover::{
    build_uniform_dyadic_tree, collar_cell_margin, collar_certification_depth,
    evaluate_collar_barrier_margin, generate_collar_cover_report, sample_quadrant_tree,
    solve_collar_cycle_circulation, standard_collar_barrier_margin, CollarBisectionTree,
    CollarCoverError, RationalBox2D,
};
use omega_mub::omega_native::exact::mub6_firewall::FIREWALL;
use omega_number_theory::rational::rq;

#[test]
fn test_rational_box_2d_basic() {
    let unit = RationalBox2D::unit_square();
    assert_eq!(unit.area(), BigRational::one());

    let center = [rq(1, 2), rq(1, 2)];
    assert!(unit.contains_point(&center));

    let outside = [rq(3, 2), rq(1, 2)];
    assert!(!unit.contains_point(&outside));
}

#[test]
fn test_quadrant_tree_partition_cover() {
    let tree = sample_quadrant_tree();
    let unit = RationalBox2D::unit_square();

    // Verification against unit square must pass
    assert!(tree.verify_partition_cover(&unit).is_ok());

    // Exact area conservation
    assert_eq!(tree.total_area(), BigRational::one());
    assert!(tree.verify_volume_conservation(&BigRational::one()).is_ok());

    // Total leaves must be 4
    let leaves = tree.leaves();
    assert_eq!(leaves.len(), 4);
    for leaf in leaves {
        assert_eq!(leaf.area(), rq(1, 4));
    }
}

#[test]
fn test_uniform_dyadic_tree_depth4() {
    // Depth 4 produces 2^4 = 16 leaves
    let tree = build_uniform_dyadic_tree(4);
    let unit = RationalBox2D::unit_square();

    assert!(tree.verify_partition_cover(&unit).is_ok());
    assert_eq!(tree.total_area(), BigRational::one());
    assert_eq!(tree.leaves().len(), 16);

    for leaf in tree.leaves() {
        assert_eq!(leaf.area(), rq(1, 16));
    }
}

#[test]
fn test_collar_barrier_margin_positivity() {
    let margin = standard_collar_barrier_margin();
    assert!(margin > BigRational::zero());
    assert_eq!(margin, rq(12133, 30000));
}

#[test]
fn test_network_simplex_circulation_acceleration() {
    // Triangle cycle with unit edge weights and unit circulation demand
    let weights = [1i128, 1, 1];
    let omega = [1i128, 1, 1];

    let sol = solve_collar_cycle_circulation(&weights, &omega)
        .expect("Network Simplex circulation solve must succeed");

    // Total Phi_1 objective must be exactly 3
    assert_eq!(sol.objective, 3);
    assert_eq!(sol.z, vec![1, 1, 1]);
}

#[test]
fn test_generate_collar_cover_report() {
    // Quadrant cells have radius 1/4, so the Lipschitz erosion (85/9)(1/4)
    // exceeds the 37249/90000 floor: no cell is certified.
    let tree = sample_quadrant_tree();
    let report = generate_collar_cover_report(&tree);

    assert_eq!(report.firewall, FIREWALL);
    assert_eq!(report.total_leaves, 4);
    assert!(report.area_conserved);
    assert!(!report.all_margins_positive);
    assert_eq!(report.min_margin, "-58417/30000");
    assert_eq!(report.certificates.len(), 4);

    for cert in &report.certificates {
        assert!(!cert.certified);
        assert_eq!(cert.margin, "-58417/30000");
    }
}

#[test]
fn test_collar_certification_depth_is_computed() {
    assert_eq!(collar_certification_depth(16), Some(8));

    let coarse = generate_collar_cover_report(&build_uniform_dyadic_tree(7));
    assert!(!coarse.all_margins_positive);

    let fine = generate_collar_cover_report(&build_uniform_dyadic_tree(8));
    assert_eq!(fine.total_leaves, 256);
    assert!(fine.area_conserved);
    assert!(fine.all_margins_positive);
    assert!(fine.certificates.iter().all(|cert| cert.certified));
    // Radius 1/32: 37249/90000 - (85/9)(1/32) = 21373/180000.
    assert_eq!(fine.min_margin, "21373/180000");
    assert_eq!(
        collar_cell_margin(&build_uniform_dyadic_tree(8).leaves()[0]),
        rq(21373, 180000)
    );
}

#[test]
fn test_negative_controls() {
    let unit = RationalBox2D::unit_square();

    // 1. Box geometry mismatch: mutated domain
    let mutated_domain = RationalBox2D::new([(rq(0, 1), rq(9, 10)), (rq(0, 1), rq(1, 1))]).unwrap();
    let tree = sample_quadrant_tree();
    assert!(matches!(
        tree.verify_partition_cover(&mutated_domain),
        Err(CollarCoverError::CutOutOfBounds { .. } | CollarCoverError::BoxMismatch { .. })
    ));

    // 2. Volume mismatch: dropped leaf
    let half = rq(1, 2);
    let (left_d0, _) = unit.subdivide(0, &half).unwrap();
    let incomplete_tree = CollarBisectionTree::Leaf(left_d0);
    assert_eq!(incomplete_tree.total_area(), rq(1, 2));
    assert!(matches!(
        incomplete_tree.verify_volume_conservation(&BigRational::one()),
        Err(CollarCoverError::AreaMismatch { .. })
    ));

    // 3. Cut out of bounds
    assert!(matches!(
        unit.subdivide(0, &rq(2, 1)),
        Err(CollarCoverError::CutOutOfBounds { .. })
    ));

    // 4. Non-positive margin rejection
    assert!(matches!(
        evaluate_collar_barrier_margin(&rq(1, 100), &rq(10, 1), &rq(1, 10)),
        Err(CollarCoverError::NonPositiveMargin { .. })
    ));
}

#[test]
fn test_ast_zero_float_discipline() {
    let src = include_str!("../../omega_mub/src/omega_native/mub6_collar_cover.rs");
    assert!(
        !src.contains("f32"),
        "mub6_collar_cover.rs must contain zero f32 occurrences"
    );
    assert!(
        !src.contains("f64"),
        "mub6_collar_cover.rs must contain zero f64 occurrences"
    );
}
