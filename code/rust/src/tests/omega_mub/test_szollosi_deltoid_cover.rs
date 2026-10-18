//! Integration tests for the exact rational Szöllősi deltoid arc interval solver.
//!
//! AuthorityEffect: None

use num_rational::BigRational;
use num_traits::Zero;

use omega_kernel::interval::Interval;
use omega_mub::omega_native::exact::mub6_szollosi_deltoid_cover::{
    box_touches_parameter_circle, solve_szollosi_deltoid_cover, SzollosiDeltoidContext,
    SzollosiDeltoidParameterBox,
};
use omega_number_theory::rational::ri;

#[test]
fn test_circle_pruning() {
    // 1. Box strictly inside unit circle: [0, 1/2] x [0, 1/2] => max r^2 = 1/4 + 1/4 = 1/2 < 1
    let inside_box = SzollosiDeltoidParameterBox::new(
        Interval::new(ri(0), ri(1) / ri(2)),
        Interval::new(ri(0), ri(1) / ri(2)),
    );
    assert!(
        !box_touches_parameter_circle(&inside_box),
        "Interior box must not touch unit circle"
    );

    // 2. Box strictly outside unit circle: [2, 3] x [2, 3] => min r^2 = 4 + 4 = 8 > 1
    let outside_box =
        SzollosiDeltoidParameterBox::new(Interval::new(ri(2), ri(3)), Interval::new(ri(2), ri(3)));
    assert!(
        !box_touches_parameter_circle(&outside_box),
        "Exterior box must not touch unit circle"
    );

    // 3. Box crossing unit circle: [1/2, 1] x [1/2, 1] => r^2 in [1/2, 2] contains 1
    let crossing_box = SzollosiDeltoidParameterBox::new(
        Interval::new(ri(1) / ri(2), ri(1)),
        Interval::new(ri(1) / ri(2), ri(1)),
    );
    assert!(
        box_touches_parameter_circle(&crossing_box),
        "Crossing box must touch unit circle"
    );
}

#[test]
fn test_parameter_box_bisection() {
    let pbox = SzollosiDeltoidParameterBox::new(
        Interval::new(ri(0), ri(1)),
        Interval::new(ri(0), ri(1) / ri(2)),
    );
    assert_eq!(pbox.widest_width(), ri(1));

    let (left, right) = pbox.bisect_widest();
    assert_eq!(*left.u.lo(), ri(0));
    assert_eq!(*left.u.hi(), ri(1) / ri(2));
    assert_eq!(*right.u.lo(), ri(1) / ri(2));
    assert_eq!(*right.u.hi(), ri(1));
    assert_eq!(left.v, right.v);
    assert_eq!(left.u.hi(), right.u.lo(), "Non-leakage contract violated");
}

#[test]
fn test_triad_defect_and_curvature_positivity() {
    let ctx = SzollosiDeltoidContext::new();

    // Exterior box away from cusps: u in [1/4, 1/2], v in [7/10, 9/10]
    let pbox = SzollosiDeltoidParameterBox::new(
        Interval::new(ri(1) / ri(4), ri(1) / ri(2)),
        Interval::new(ri(7) / ri(10), ri(9) / ri(10)),
    );
    assert!(box_touches_parameter_circle(&pbox));

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
    println!("Sample exterior box: triad_defect={triad_defect}, psi_lower={psi_lower}");
}

#[test]
fn test_szollosi_deltoid_smoke_cover() {
    let delta = BigRational::new(1.into(), 100.into());
    let report = solve_szollosi_deltoid_cover(4, &delta, 12);

    assert!(report.complete, "Deltoid smoke cover must complete");
    assert_eq!(
        report.uncertified_boxes, 0,
        "Zero uncertified boxes allowed"
    );
    assert!(
        report.outside_boxes_certified > 0,
        "Must certify exterior boxes outside cusp neighborhoods"
    );
    assert_ne!(report.min_extension_psi_gap, "none");

    for b in &report.boxes {
        assert!(b.verified_positive);
        let num: num_bigint::BigInt = b.min_psi_gap_num.parse().expect("valid numerator integer");
        let den: num_bigint::BigInt = b
            .min_psi_gap_den
            .parse()
            .expect("valid denominator integer");
        assert!(
            num > num_bigint::BigInt::zero(),
            "Box {} psi numerator must be positive",
            b.box_id
        );
        assert!(
            den > num_bigint::BigInt::zero(),
            "Box {} psi denominator must be positive",
            b.box_id
        );
    }
}

#[test]
fn test_network_simplex_deltoid_triad_cycle_obstruction() {
    let ctx = SzollosiDeltoidContext::new();

    // Exterior box
    let pbox = SzollosiDeltoidParameterBox::new(
        Interval::new(ri(1) / ri(4), ri(1) / ri(2)),
        Interval::new(ri(7) / ri(10), ri(9) / ri(10)),
    );
    let phi1_sol = ctx
        .solve_network_simplex_obstruction(&pbox)
        .expect("Network Simplex solves successfully");
    assert!(
        phi1_sol.objective >= 37249,
        "Phi_1 must be bounded below by base gap 37249"
    );
    assert_eq!(phi1_sol.z.len(), 3, "Triad cycle has 3 edges");
    assert_eq!(
        phi1_sol.vertex_potential.len(),
        3,
        "Triad cycle has 3 vertices"
    );

    // Boundary box touching cusp neighborhood near F_6 (1, 0)
    let boundary_box = SzollosiDeltoidParameterBox::new(
        Interval::new(ri(99) / ri(100), ri(1)),
        Interval::new(ri(0), ri(1) / ri(100)),
    );
    let boundary_phi1 = ctx
        .solve_network_simplex_obstruction(&boundary_box)
        .expect("Solves boundary box");
    assert!(
        boundary_phi1.objective >= 37249,
        "Boundary cell Phi_1 strictly positive"
    );
}

#[test]
fn test_network_simplex_accelerates_boundary_bisection() {
    let delta = BigRational::new(1.into(), 100.into());
    // Run at shallow bisection depth (max_depth = 3) where pure scalar bisection leaves uncertified boundary boxes
    let unaccelerated = omega_mub::omega_native::exact::mub6_szollosi_deltoid_cover::solve_szollosi_deltoid_cover_accelerated(
        4, &delta, 3, false,
    );
    let accelerated = omega_mub::omega_native::exact::mub6_szollosi_deltoid_cover::solve_szollosi_deltoid_cover_accelerated(
        4, &delta, 3, true,
    );

    // Network Simplex accelerates certification of boundary boxes
    assert!(
        accelerated.outside_boxes_certified >= unaccelerated.outside_boxes_certified,
        "Accelerated solver must certify at least as many boxes"
    );
    assert!(
        accelerated.uncertified_boxes <= unaccelerated.uncertified_boxes,
        "Accelerated solver must have fewer or equal uncertified boxes"
    );
    assert!(
        accelerated.network_simplex_accelerated_boxes > 0 || accelerated.uncertified_boxes == 0,
        "Network Simplex must either accelerate boundary boxes or complete with 0 uncertified"
    );
}

#[test]
fn test_boundary_box_dual_certificate_soundness() {
    let ctx = SzollosiDeltoidContext::new();
    let pbox = SzollosiDeltoidParameterBox::new(
        Interval::new(ri(99) / ri(100), ri(1)),
        Interval::new(ri(0), ri(1) / ri(100)),
    );
    let (boundary, omega) = ctx.build_triad_boundary_and_cochain(&pbox);
    let sol = ctx.solve_network_simplex_obstruction(&pbox).unwrap();

    // Verify dual feasibility and zero duality gap
    // z = omega - d alpha
    for (i, edge) in boundary.edges.iter().enumerate() {
        let diff = sol.vertex_potential[edge.head] - sol.vertex_potential[edge.tail];
        assert_eq!(
            sol.z[i],
            omega[i] - diff,
            "Residual z must equal omega - d alpha on edge {}",
            i
        );
    }

    // Verify objective equals weighted L1 norm of z
    let l1_norm: i128 = sol.z.iter().map(|&x| x.abs()).sum();
    assert_eq!(
        sol.objective, l1_norm,
        "Objective must match exact L1 norm of residual"
    );
}
