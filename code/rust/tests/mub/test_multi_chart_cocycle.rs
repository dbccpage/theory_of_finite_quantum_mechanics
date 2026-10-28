//! Integration and unit tests for Target A3 multi-chart transition cocycle circulation evaluation.
//!
//! AuthorityEffect: None

use num_rational::BigRational;
use tfqm_mub::native::exact::mub6_multi_chart_cocycle::{
    evaluate_multi_chart_circulation_extension, AffineCorner4D, ChartTransition4D,
    MultiChartCycle4D,
};
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::ri;

fn rat(n: i64, d: i64) -> Cyc24 {
    Cyc24::rat(ri(n) / ri(d))
}

#[test]
fn test_trivial_cocycle_circulation_obstruction_conserved() {
    // 3 charts in the 4D moduli space
    let chart0 = AffineCorner4D::new(
        Cyc24::zeta24(4),
        Cyc24::zeta24(8),
        Cyc24::zeta24(12),
        Cyc24::zeta24(16),
    );
    let chart1 = AffineCorner4D::new(
        Cyc24::zeta24(2),
        Cyc24::zeta24(6),
        Cyc24::zeta24(10),
        Cyc24::zeta24(14),
    );
    let chart2 = AffineCorner4D::new(
        Cyc24::zeta24(1),
        Cyc24::zeta24(3),
        Cyc24::zeta24(5),
        Cyc24::zeta24(7),
    );

    assert!(chart0.is_regular(), "Chart 0 must be regular");
    assert!(chart1.is_regular(), "Chart 1 must be regular");
    assert!(chart2.is_regular(), "Chart 2 must be regular");

    // Trivial transition cocycle: g01 = phase(zeta^8, zeta^16), g12 = phase(zeta^16, zeta^8), g20 = id
    // Product = phase(zeta^24, zeta^24) = phase(1, 1) = I_3
    let g01 = ChartTransition4D::phases(Cyc24::zeta24(8), Cyc24::zeta24(16));
    let g12 = ChartTransition4D::phases(Cyc24::zeta24(16), Cyc24::zeta24(8));
    let g20 = ChartTransition4D::identity();

    let edge_defects = [
        BigRational::new(37249.into(), 90000.into()),
        BigRational::new(1.into(), 10.into()),
        BigRational::new(1.into(), 5.into()),
    ];

    let cycle = MultiChartCycle4D::new([chart0, chart1, chart2], [g01, g12, g20], edge_defects);

    assert!(
        cycle.is_cocycle_trivial(),
        "Transition cocycle must be trivial (W = I_3)"
    );

    let report = evaluate_multi_chart_circulation_extension(&cycle, 90000, 37249)
        .expect("Evaluation succeeds");

    assert!(report.is_cocycle_trivial, "Report verifies trivial cocycle");
    assert!(
        report.circulation_conserved,
        "Circulation sum (d alpha) around cycle must be 0"
    );
    assert_eq!(
        report.coboundary_sum, 0,
        "Coboundary sum around 3-cycle must vanish identically"
    );
    assert!(
        report.dual_gap_zero,
        "Duality gap must be exactly zero (z = omega - d alpha)"
    );
    assert!(
        report.obstruction_certified,
        "Discrete L1 circulation obstruction must be certified"
    );
    assert!(
        report.phi1_objective >= report.net_circulation,
        "Phi_1 must be >= net circulation"
    );
    assert!(
        report.net_circulation > 0,
        "Net circulation must be positive"
    );
}

#[test]
fn test_twisted_cocycle_compounds_circulation_obstruction() {
    // 3 charts with non-trivial permutation holonomy (twisted transition cocycle)
    let chart0 = AffineCorner4D::new(rat(1, 1), rat(1, 1), rat(1, 1), rat(1, 1));
    let chart1 = AffineCorner4D::new(rat(1, 1), rat(1, 1), rat(1, 1), rat(1, 1));
    let chart2 = AffineCorner4D::new(rat(1, 1), rat(1, 1), rat(1, 1), rat(1, 1));

    // g01 = swap (0, 1), g12 = swap (1, 2), g20 = id -> W = (0 1 2) != I_3
    let g01 = ChartTransition4D::permutation([1, 0, 2]);
    let g12 = ChartTransition4D::permutation([0, 2, 1]);
    let g20 = ChartTransition4D::identity();

    let edge_defects = [
        BigRational::new(37249.into(), 90000.into()),
        BigRational::new(37249.into(), 90000.into()),
        BigRational::new(37249.into(), 90000.into()),
    ];

    let cycle = MultiChartCycle4D::new([chart0, chart1, chart2], [g01, g12, g20], edge_defects);

    assert!(
        !cycle.is_cocycle_trivial(),
        "Transition cocycle with permutation twist must be non-trivial"
    );

    let report = evaluate_multi_chart_circulation_extension(&cycle, 90000, 37249)
        .expect("Evaluation succeeds");

    assert!(
        !report.is_cocycle_trivial,
        "Report verifies non-trivial transition cocycle"
    );
    assert!(
        report.circulation_conserved,
        "Circulation invariance holds even with twisted cocycle"
    );
    assert_eq!(report.coboundary_sum, 0);
    assert!(report.dual_gap_zero);
    assert!(report.obstruction_certified);
    assert!(
        report.phi1_objective >= 3 * 37249,
        "Phi_1 objective bounds circulation"
    );
}

#[test]
fn test_gauge_potential_coboundary_invariance_on_4d_cycle() {
    // Test 100 adversarial 0-cochain potentials alpha in Z^3
    let omega = [37249i128, 45000i128, 52000i128];
    let net_circulation: i128 = omega.iter().sum();

    for i in 0..100 {
        let a0 = (i as i128) * 137 - 5000;
        let a1 = (i as i128) * 311 + 2500;
        let a2 = (i as i128) * (-479) + 1234;
        let alpha = [a0, a1, a2];

        // Coboundary edges:
        // e0 = a1 - a0
        // e1 = a2 - a1
        // e2 = a0 - a2
        let d_alpha = [
            alpha[1] - alpha[0],
            alpha[2] - alpha[1],
            alpha[0] - alpha[2],
        ];

        let coboundary_sum: i128 = d_alpha.iter().sum();
        assert_eq!(
            coboundary_sum, 0,
            "Sum of coboundary around cycle must be identically 0"
        );

        let residual = [
            omega[0] - d_alpha[0],
            omega[1] - d_alpha[1],
            omega[2] - d_alpha[2],
        ];

        let residual_sum: i128 = residual.iter().sum();
        assert_eq!(
            residual_sum, net_circulation,
            "Residual sum after potential shift must equal net circulation"
        );

        let l1_norm: i128 = residual.iter().map(|&x| x.abs()).sum();
        assert!(
            l1_norm >= net_circulation,
            "L1 norm ||omega - d alpha||_1 must be >= net circulation"
        );
    }
}

#[test]
fn test_exact_network_simplex_dual_certificate_on_multi_chart_cycle() {
    let chart0 = AffineCorner4D::new(rat(1, 1), rat(1, 1), rat(1, 1), rat(1, 1));
    let chart1 = AffineCorner4D::new(rat(1, 1), rat(1, 1), rat(1, 1), rat(1, 1));
    let chart2 = AffineCorner4D::new(rat(1, 1), rat(1, 1), rat(1, 1), rat(1, 1));

    let cycle = MultiChartCycle4D::new(
        [chart0, chart1, chart2],
        [
            ChartTransition4D::identity(),
            ChartTransition4D::identity(),
            ChartTransition4D::identity(),
        ],
        [
            BigRational::new(1.into(), 2.into()),
            BigRational::new(1.into(), 3.into()),
            BigRational::new(1.into(), 4.into()),
        ],
    );

    let (boundary, omega) = cycle.build_cycle_boundary_and_cochain(120, 10);
    let sol = cycle
        .solve_network_simplex_obstruction(120, 10)
        .expect("Network Simplex succeeds");

    // Check dual feasibility
    for (i, edge) in boundary.edges.iter().enumerate() {
        let diff = sol.vertex_potential[edge.head] - sol.vertex_potential[edge.tail];
        assert_eq!(
            sol.z[i],
            omega[i] - diff,
            "Residual z must equal omega - d alpha on edge {}",
            i
        );
    }

    // Check zero duality gap: objective == ||z||_1
    let l1_norm: i128 = sol.z.iter().map(|&x| x.abs()).sum();
    assert_eq!(
        sol.objective, l1_norm,
        "Objective must match exact L1 norm of residual"
    );
    assert!(sol.objective > 0, "Phi_1 must be strictly positive");
}
