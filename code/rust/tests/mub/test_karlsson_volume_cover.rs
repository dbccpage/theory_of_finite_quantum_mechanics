//! Integration tests for the exact rational Karlsson 3-parameter volume interval solver.
//!
//! AuthorityEffect: None

use num_rational::BigRational;
use num_traits::Zero;

use engine_kernel::interval::Interval;
use tfqm_mub::native::exact::d6_exact_curvature_cochain::D;
use tfqm_mub::native::exact::mub6_karlsson_volume_cover::{
    box_touches_parameter_torus, overlap_abs_sq, solve_karlsson_volume_cover,
    KarlssonVolumeContext, KarlssonVolumeParameterBox,
};
use engine_number_theory::rational::ri;

#[test]
fn test_torus_pruning() {
    // 1. Box strictly inside unit circle for x: [0, 1/2] x [0, 1/2] => max r^2 = 1/2 < 1
    let inside_box = KarlssonVolumeParameterBox::new(
        Interval::new(ri(0), ri(1) / ri(2)),
        Interval::new(ri(0), ri(1) / ri(2)),
        Interval::new(ri(0), ri(1)),
        Interval::new(ri(0), ri(1)),
        Interval::new(ri(0), ri(1)),
        Interval::new(ri(0), ri(1)),
    );
    assert!(
        !box_touches_parameter_torus(&inside_box),
        "Interior box must not touch 3-torus"
    );

    // 2. Box strictly outside unit circle for y: [2, 3] x [2, 3] => min r^2 = 8 > 1
    let outside_box = KarlssonVolumeParameterBox::new(
        Interval::new(ri(0), ri(1)),
        Interval::new(ri(0), ri(1)),
        Interval::new(ri(2), ri(3)),
        Interval::new(ri(2), ri(3)),
        Interval::new(ri(0), ri(1)),
        Interval::new(ri(0), ri(1)),
    );
    assert!(
        !box_touches_parameter_torus(&outside_box),
        "Exterior box must not touch 3-torus"
    );

    // 3. Box crossing all 3 circles
    let crossing_box = KarlssonVolumeParameterBox::new(
        Interval::new(ri(1) / ri(2), ri(1)),
        Interval::new(ri(1) / ri(2), ri(1)),
        Interval::new(ri(1) / ri(2), ri(1)),
        Interval::new(ri(1) / ri(2), ri(1)),
        Interval::new(ri(1) / ri(2), ri(1)),
        Interval::new(ri(1) / ri(2), ri(1)),
    );
    assert!(
        box_touches_parameter_torus(&crossing_box),
        "Crossing box must touch 3-torus"
    );
}

#[test]
fn test_parameter_box_bisection() {
    let pbox = KarlssonVolumeParameterBox::new(
        Interval::new(ri(0), ri(1)),
        Interval::new(ri(0), ri(1) / ri(2)),
        Interval::new(ri(0), ri(1) / ri(4)),
        Interval::new(ri(0), ri(1) / ri(4)),
        Interval::new(ri(0), ri(1) / ri(4)),
        Interval::new(ri(0), ri(1) / ri(4)),
    );
    assert_eq!(pbox.widest_width(), ri(1));

    let (left, right) = pbox.bisect_widest();
    assert_eq!(*left.u_x.lo(), ri(0));
    assert_eq!(*left.u_x.hi(), ri(1) / ri(2));
    assert_eq!(*right.u_x.lo(), ri(1) / ri(2));
    assert_eq!(*right.u_x.hi(), ri(1));
    assert_eq!(left.v_x, right.v_x);
    assert_eq!(left.u_y, right.u_y);
    assert_eq!(
        left.u_x.hi(),
        right.u_x.lo(),
        "Non-leakage contract violated"
    );
}

#[test]
fn test_seed_excision_and_boundaries() {
    let ctx = KarlssonVolumeContext::new();
    let delta = BigRational::new(1.into(), 1000.into());

    // 1. Box inside Diță slab: v_z in [-1/2000, 1/2000]
    let dita_box = KarlssonVolumeParameterBox::new(
        Interval::new(ri(9) / ri(10), ri(1)),
        Interval::new(ri(0), ri(1) / ri(10)),
        Interval::new(ri(9) / ri(10), ri(1)),
        Interval::new(ri(0), ri(1) / ri(10)),
        Interval::new(ri(9) / ri(10), ri(1)),
        Interval::new(ri(-1) / ri(2000), ri(1) / ri(2000)),
    );
    assert!(ctx.is_inside_seed_neighborhoods(&dita_box, &delta));
    assert!(!ctx.is_strictly_outside_seeds(&dita_box, &delta));

    // 2. Box strictly outside Diță slab: v_z in [1/500, 1/100]
    let outside_box = KarlssonVolumeParameterBox::new(
        Interval::new(ri(9) / ri(10), ri(1)),
        Interval::new(ri(0), ri(1) / ri(10)),
        Interval::new(ri(9) / ri(10), ri(1)),
        Interval::new(ri(0), ri(1) / ri(10)),
        Interval::new(ri(9) / ri(10), ri(1)),
        Interval::new(ri(1) / ri(500), ri(1) / ri(100)),
    );
    assert!(ctx.is_strictly_outside_seeds(&outside_box, &delta));
    assert!(!ctx.is_inside_seed_neighborhoods(&outside_box, &delta));

    // 3. Box straddling Diță slab boundary at delta: v_z in [0, 2/1000]
    let straddling_box = KarlssonVolumeParameterBox::new(
        Interval::new(ri(9) / ri(10), ri(1)),
        Interval::new(ri(0), ri(1) / ri(10)),
        Interval::new(ri(9) / ri(10), ri(1)),
        Interval::new(ri(0), ri(1) / ri(10)),
        Interval::new(ri(9) / ri(10), ri(1)),
        Interval::new(ri(0), ri(2) / ri(1000)),
    );
    let cut = ctx.find_seed_boundary_cut(&straddling_box, &delta);
    assert!(cut.is_some());
    let (coord, cut_pt) = cut.unwrap();
    assert_eq!(coord, 5, "Cut must be on v_z coordinate");
    assert_eq!(cut_pt, delta, "Cut point must match delta");
}

#[test]
fn test_orthogonality_and_curvature_positivity() {
    let ctx = KarlssonVolumeContext::new();

    // Exterior box away from seeds: u_x in [1/4, 1/2], v_x in [7/10, 9/10], same for y, z
    let pbox = KarlssonVolumeParameterBox::new(
        Interval::new(ri(1) / ri(4), ri(1) / ri(2)),
        Interval::new(ri(7) / ri(10), ri(9) / ri(10)),
        Interval::new(ri(1) / ri(4), ri(1) / ri(2)),
        Interval::new(ri(7) / ri(10), ri(9) / ri(10)),
        Interval::new(ri(1) / ri(4), ri(1) / ri(2)),
        Interval::new(ri(7) / ri(10), ri(9) / ri(10)),
    );
    assert!(box_touches_parameter_torus(&pbox));

    let k_cols = ctx.karlsson_columns(&pbox);
    assert_eq!(k_cols.len(), D);

    // Columns are normalized by 1/sqrt(6); self-overlap should be close to 1
    for c in 0..D {
        let norm_sq = overlap_abs_sq(&k_cols[c], &k_cols[c]);
        assert!(norm_sq.lo() <= &(ri(1) + ri(1) / ri(5)) && ri(1) - ri(1) / ri(5) <= *norm_sq.hi());
    }

    let triad_defect = ctx.triad_defect_lower(&pbox);
    let psi_lower = ctx.extension_psi_lower(&pbox);

    let base_gap = BigRational::new(37249.into(), 90000.into());
    assert!(
        psi_lower >= base_gap,
        "Extension psi lower bound must be at least the base gap 37249/90000"
    );
    assert!(
        psi_lower > BigRational::zero(),
        "Extension psi lower bound must be strictly positive"
    );
    println!("Exterior box: triad_defect={triad_defect}, psi_lower={psi_lower}");
}

#[test]
fn test_karlsson_volume_smoke_cover() {
    let delta = BigRational::new(1.into(), 1000.into());
    let report = solve_karlsson_volume_cover(2, &delta, 24);

    assert!(report.complete, "Karlsson volume cover must complete");
    assert_eq!(
        report.uncertified_boxes, 0,
        "Zero uncertified boxes allowed"
    );
    assert!(
        report.outside_boxes_certified > 0,
        "Must certify positive number of exterior boxes"
    );
    assert!(
        report.seed_neighborhood_boxes > 0,
        "Must identify seed neighborhood boxes"
    );

    let overall_min = BigRational::new(
        report.overall_min_psi_num.parse().unwrap(),
        report.overall_min_psi_den.parse().unwrap(),
    );
    assert!(
        overall_min > BigRational::zero(),
        "Overall minimum psi gap must be strictly positive"
    );

    println!("Karlsson smoke cover complete:");
    println!("  Total explored:   {}", report.total_boxes_explored);
    println!("  Off-torus pruned: {}", report.off_torus_boxes_pruned);
    println!("  Seed boxes:       {}", report.seed_neighborhood_boxes);
    println!("  Certified boxes:  {}", report.outside_boxes_certified);
    println!("  Overall min gap:  {overall_min}");
}
