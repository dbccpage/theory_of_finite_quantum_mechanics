//! Integration and unit tests for Target 4: Quantitative Lipschitz Gap Propagation & Uniform Derivative Bounds.
//!
//! AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::Zero;

use tfqm_mub::native::exact::mub6_constants::{
    base_gap, delta_certified, delta_crit, lipschitz_bound,
};
use tfqm_mub::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use tfqm_mub::native::exact::mub6_gap_propagation::{
    erosion_certified, generate_target4_receipt, margin_certified, partition_2d_periodic_collar,
    GapPropagationError, LipschitzParameters, RationalPoint2D,
};
use omega_number_theory::rational::rq;

#[test]
fn test_canonical_parameters_exact_values() {
    let eps = base_gap();
    let l = lipschitz_bound();
    let d_crit = delta_crit();
    let d_cert = delta_certified();
    let erosion = erosion_certified();
    let margin = margin_certified();

    // 1. Check exact fractions
    assert_eq!(eps, rq(37249, 90000));
    assert_eq!(l, rq(85, 9));
    assert_eq!(d_crit, rq(37249, 850000));
    assert_eq!(d_cert, rq(1, 1000));
    assert_eq!(erosion, rq(17, 1800));
    assert_eq!(margin, rq(12133, 30000));

    // 2. Critical threshold equality: d_crit = eps / L
    assert_eq!(&eps / &l, d_crit);

    // 3. Certified mesh step strictly smaller than critical threshold
    assert!(d_cert < d_crit);

    // 4. Certified erosion equality: L * d_cert = 17 / 1800
    assert_eq!(&l * &d_cert, erosion);

    // 5. Certified margin equality: eps - erosion = 12133 / 30000
    assert_eq!(&eps - &erosion, margin);
    assert!(margin > BigRational::zero());
}

#[test]
fn test_lipschitz_parameters_constructor() {
    let params = LipschitzParameters::canonical();
    assert_eq!(params.base_gap, rq(37249, 90000));
    assert_eq!(params.lipschitz_bound, rq(85, 9));
    assert_eq!(params.mesh_step, rq(1, 1000));
    assert_eq!(params.critical_mesh_step(), rq(37249, 850000));
    assert_eq!(params.erosion(), rq(17, 1800));
    assert_eq!(params.propagated_margin(), rq(12133, 30000));
}

#[test]
fn test_rational_point_2d_distances() {
    let p1 = RationalPoint2D::new(rq(1, 4), rq(1, 4));
    let p2 = RationalPoint2D::new(rq(1, 2), rq(3, 4));

    // Chebyshev distance: max(|1/4 - 1/2|, |1/4 - 3/4|) = max(1/4, 2/4) = 1/2
    assert_eq!(p1.l_inf_distance(&p2), rq(1, 2));

    // Manhattan distance: |1/4 - 1/2| + |1/4 - 3/4| = 1/4 + 1/2 = 3/4
    assert_eq!(p1.l_1_distance(&p2), rq(3, 4));
}

#[test]
fn test_grid_partition_and_margin_positivity() {
    // 500 divisions per axis gives half_width = 1 / 1000 = delta_certified
    let params = LipschitzParameters::canonical();
    let partition = partition_2d_periodic_collar(500, &params)
        .expect("Grid partition with 500 divisions must succeed");

    assert_eq!(partition.divisions_per_axis, 500);
    assert_eq!(partition.total_cells, 250_000);
    assert_eq!(partition.mesh_step, rq(1, 1000));
    assert_eq!(partition.min_margin, rq(12133, 30000));
    assert!(partition.all_positive);
    assert!(partition.verify_partition().is_ok());

    // Check first cell bounds and center
    let cell0 = &partition.cells[0];
    assert_eq!(cell0.bounds[0], (rq(0, 1), rq(1, 500)));
    assert_eq!(cell0.bounds[1], (rq(0, 1), rq(1, 500)));
    assert_eq!(cell0.center, [rq(1, 1000), rq(1, 1000)]);
    assert_eq!(cell0.margin, rq(12133, 30000));
    assert!(cell0.is_positive);

    // Verify worst-case bound on corner point of cell0
    let corner = RationalPoint2D::new(rq(0, 1), rq(0, 1));
    let worst_bound = cell0.evaluate_point_bound(&corner, &params.lipschitz_bound);
    assert_eq!(worst_bound, rq(12133, 30000));
    assert!(worst_bound > BigRational::zero());
}

#[test]
fn test_point_containment_and_evaluation() {
    let params = LipschitzParameters::canonical();
    let partition = partition_2d_periodic_collar(500, &params).unwrap();

    let pt = [rq(3, 1000), rq(7, 1000)];
    let cell = partition
        .find_cell(&pt)
        .expect("Point must be inside a cell");
    assert!(cell.contains(&pt));

    let rat_pt = RationalPoint2D::new(pt[0].clone(), pt[1].clone());
    let bound = cell.evaluate_point_bound(&rat_pt, &params.lipschitz_bound);
    assert!(bound >= partition.min_margin);
    assert!(bound > BigRational::zero());
}

#[test]
fn test_generate_target4_receipt() {
    let params = LipschitzParameters::canonical();
    let receipt =
        generate_target4_receipt(&params, 500).expect("Target 4 receipt generation must succeed");

    assert_eq!(
        receipt.schema_version,
        "omega.mub.target-4-gap-propagation.v1"
    );
    assert_eq!(receipt.firewall, FIREWALL);
    assert_eq!(receipt.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(receipt.base_gap, "37249/90000");
    assert_eq!(receipt.lipschitz_bound, "85/9");
    assert_eq!(receipt.mesh_step, "1/1000");
    assert_eq!(receipt.delta_crit, "37249/850000");
    assert_eq!(receipt.margin, "12133/30000");
    assert_eq!(receipt.divisions_per_axis, 500);
    assert_eq!(receipt.total_cells, 250000);
    assert!(receipt.all_margins_positive);
    assert!(receipt.verified);
}

#[test]
fn test_negative_controls_oversized_mesh_step() {
    // 1. Constructor rejection when delta >= delta_crit
    let eps = rq(37249, 90000);
    let l = rq(85, 9);
    let crit = rq(37249, 850000);

    // Exact crit threshold rejected
    assert!(matches!(
        LipschitzParameters::new(eps.clone(), l.clone(), crit.clone()),
        Err(GapPropagationError::OversizedMeshStep { .. })
    ));

    // Exceeding crit threshold rejected
    let oversized = rq(1, 10);
    assert!(matches!(
        LipschitzParameters::new(eps.clone(), l.clone(), oversized),
        Err(GapPropagationError::OversizedMeshStep { .. })
    ));

    // 2. Partitioner rejection when cell half-width exceeds allowed mesh_step
    let params = LipschitzParameters::new(eps, l, rq(1, 2000)).unwrap();
    // With N = 100, half_width is 1/200, which exceeds mesh_step 1/2000
    assert!(matches!(
        partition_2d_periodic_collar(100, &params),
        Err(GapPropagationError::OversizedMeshStep { .. })
    ));
}

#[test]
fn test_negative_controls_nonpositive_parameters() {
    let eps = rq(37249, 90000);
    let l = rq(85, 9);
    let d = rq(1, 1000);

    // Zero / negative base gap
    assert!(matches!(
        LipschitzParameters::new(BigRational::zero(), l.clone(), d.clone()),
        Err(GapPropagationError::InvalidParameter(_))
    ));
    assert!(matches!(
        LipschitzParameters::new(rq(-1, 10), l.clone(), d.clone()),
        Err(GapPropagationError::InvalidParameter(_))
    ));

    // Zero / negative lipschitz
    assert!(matches!(
        LipschitzParameters::new(eps.clone(), BigRational::zero(), d.clone()),
        Err(GapPropagationError::InvalidParameter(_))
    ));
    assert!(matches!(
        LipschitzParameters::new(eps.clone(), rq(-85, 9), d.clone()),
        Err(GapPropagationError::InvalidParameter(_))
    ));

    // Zero / negative mesh step
    assert!(matches!(
        LipschitzParameters::new(eps.clone(), l.clone(), BigRational::zero()),
        Err(GapPropagationError::InvalidParameter(_))
    ));
    assert!(matches!(
        LipschitzParameters::new(eps.clone(), l.clone(), rq(-1, 1000)),
        Err(GapPropagationError::InvalidParameter(_))
    ));
}

#[test]
fn test_negative_controls_point_out_of_bounds() {
    let params = LipschitzParameters::canonical();
    let partition = partition_2d_periodic_collar(500, &params).unwrap();

    let outside_pt = [rq(3, 2), rq(1, 2)];
    assert!(matches!(
        partition.find_cell(&outside_pt),
        Err(GapPropagationError::PointOutOfBounds { .. })
    ));
}

#[test]
fn test_ast_zero_float_discipline() {
    let src = include_str!("../../omega_mub/src/native/mub6_gap_propagation.rs");
    assert!(
        !src.contains("f32"),
        "mub6_gap_propagation.rs must contain zero f32 occurrences"
    );
    assert!(
        !src.contains("f64"),
        "mub6_gap_propagation.rs must contain zero f64 occurrences"
    );
}
