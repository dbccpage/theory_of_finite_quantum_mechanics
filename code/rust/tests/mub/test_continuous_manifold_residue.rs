//! Integration test for the exact rational continuous Diță manifold residue solver.
//!
//! AuthorityEffect: None

use num_rational::BigRational;
use omega_kernel::interval::Interval;
use tfqm_mub::native::exact::mub6_continuous_manifold_residue::{
    all_6_genuine_seeds, box_touches_parameter_torus, seed_coordinate_ivals,
    solve_continuous_manifold_residue, triad_unbiasedness_defect_lower, DitaContinuousParameterBox,
};
use tfqm_mub::native::exact::mub6_cyclotomic_enclosure::SqrtBox;
use omega_number_theory::rational::ri;

#[test]
fn test_genuine_seeds_inventory_and_properties() {
    let seeds = all_6_genuine_seeds();
    assert_eq!(seeds.len(), 6);
    let q1_count = seeds.iter().filter(|s| s.qa == 1).count();
    let q2_count = seeds.iter().filter(|s| s.qa == 2).count();
    assert_eq!(q1_count, 3);
    assert_eq!(q2_count, 3);

    let sb = SqrtBox::standard();
    let one = ri(1);
    for s in &seeds {
        let (ua, va, ub, vb) = seed_coordinate_ivals(s, &sb);
        let norm_sq_a = ua.sq().add(&va.sq());
        let norm_sq_b = ub.sq().add(&vb.sq());
        assert!(
            norm_sq_a.contains(&one),
            "seed {} alpha not on circle",
            s.name
        );
        assert!(
            norm_sq_b.contains(&one),
            "seed {} beta not on circle",
            s.name
        );
    }
}

#[test]
fn test_torus_pruning_and_box_bisection() {
    let cube = DitaContinuousParameterBox::full_unit_cube();
    assert!(box_touches_parameter_torus(&cube));

    // Off-torus box: u in [0, 0.1], v in [0, 0.1]
    let tiny = Interval::new(ri(0), ri(1) / ri(10));
    let off_torus = DitaContinuousParameterBox::new(tiny.clone(), tiny.clone(), tiny.clone(), tiny);
    assert!(!box_touches_parameter_torus(&off_torus));

    // Closed bisection leaves no interface gap
    let (b1, b2) = cube.bisect_widest();
    assert_eq!(b1.u_alpha.hi(), b2.u_alpha.lo());
}

#[test]
fn test_continuous_manifold_residue_triad_defect_semantics() {
    let sb = SqrtBox::standard();
    let seeds = all_6_genuine_seeds();

    // At genuine Seed 1 (orbit Y2 x Q1): triad defect is zero for qa=1
    let (ua, va, ub, vb) = seed_coordinate_ivals(&seeds[0], &sb);
    let pbox_seed = DitaContinuousParameterBox::new(ua, va, ub, vb);
    let defect_seed = triad_unbiasedness_defect_lower(&pbox_seed, seeds[0].qa, &sb);
    assert_eq!(defect_seed, BigRational::from_integer(0.into()));

    // Away from seeds: triad defect is strictly positive
    let pbox_away = DitaContinuousParameterBox::new(
        Interval::new(ri(0), ri(2) / ri(10)),
        Interval::new(ri(95) / ri(100), ri(1)),
        Interval::new(ri(0), ri(2) / ri(10)),
        Interval::new(ri(95) / ri(100), ri(1)),
    );
    let defect_away = triad_unbiasedness_defect_lower(&pbox_away, 1, &sb);
    assert!(defect_away > BigRational::from_integer(0.into()));
}

#[test]
fn test_continuous_manifold_residue_smoke_cover() {
    let delta = BigRational::new(1.into(), 10.into());
    let report = solve_continuous_manifold_residue(4, &delta, 6);

    assert_eq!(report.firewall, "stated region only; mints no authority");
    assert_eq!(report.authority_effect, "None");
    assert!(report.total_boxes_explored > 0);
    assert!(report.off_torus_boxes_pruned > 0);
    assert!(report.outside_boxes_certified > 0);
}

#[test]
fn test_outside_boxes_triad_defect_positivity() {
    use tfqm_mub::native::exact::mub6_continuous_manifold_residue::ContinuousManifoldContext;
    let ctx = ContinuousManifoldContext::new();
    let pbox_wide = DitaContinuousParameterBox::new(
        Interval::new(ri(3) / ri(5), ri(1)),
        Interval::new(ri(3) / ri(5), ri(1)),
        Interval::new(ri(3) / ri(5), ri(1)),
        Interval::new(ri(3) / ri(5), ri(1)),
    );
    let (b1, _) = pbox_wide.bisect_widest();
    let (b2, _) = b1.bisect_widest();
    let (b3, _) = b2.bisect_widest();
    let (b4, _) = b3.bisect_widest();
    let t1 = ctx.triad_defect_lower(&b4, 1);
    let t2 = ctx.triad_defect_lower(&b4, 2);
    assert!(t1 > ri(0));
    assert!(t2 > ri(0));
}
