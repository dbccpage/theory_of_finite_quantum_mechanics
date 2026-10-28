//! Adversarial Empirical Stress Test Suite for Rust Native L1 Solvers and Certifiers.
//!
//! Epistemic Firewall:
//! AuthorityEffect: None.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use engine_certifiers::phi1_certifier::{
    CertificateError, Phi1FormCertificate, Phi1FormError, Phi1Verifier,
};
use engine_number_theory::rational::{ri, rq};
use engine_solvers::solver_lp_exact_simplex::{
    solve_weighted_l1_projection, L1LpError, L1ProjectionSolution,
};
use engine_solvers::solver_flow_network_simplex::NetworkSimplexError;
use engine_solvers::solver_flow_network_simplex::Arc;
use engine_solvers::solver_flow_network_simplex::NetworkSimplex;
use engine_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge};

fn q_big(num: &str, den: &str) -> BigRational {
    let n: BigInt = num.parse().unwrap();
    let d: BigInt = den.parse().unwrap();
    BigRational::new(n, d)
}

fn assert_dual_invariants(
    solution: &L1ProjectionSolution,
    target: &[BigRational],
    weights: &[BigRational],
    map_rows: &[Vec<BigRational>],
) {
    let m = target.len();
    let k = map_rows.first().map(Vec::len).unwrap_or(0);

    // 1. Dual annihilates column space: M^T y = 0
    for j in 0..k {
        let col_dot: BigRational = (0..m)
            .map(|i| map_rows[i][j].clone() * solution.dual[i].clone())
            .sum();
        assert!(
            col_dot.is_zero(),
            "Dual must annihilate column {j}, got {col_dot}"
        );
    }

    // 2. Dual satisfies infinity-norm bound: |y_e| <= w_e
    for e in 0..m {
        assert!(
            solution.dual[e].abs() <= weights[e],
            "Dual at {e} exceeds weight bound: |{}| > {}",
            solution.dual[e],
            weights[e]
        );
    }

    // 3. Zero duality gap: <y, target> = optimal value
    let pairing: BigRational = solution
        .dual
        .iter()
        .zip(target)
        .map(|(y, t)| y.clone() * t.clone())
        .sum();
    assert_eq!(
        pairing, solution.value,
        "Duality gap detected: <y, target> = {pairing}, value = {}",
        solution.value
    );

    // 4. Primal residual matches definition: z = target - M gamma
    for e in 0..m {
        let mapped: BigRational = (0..k)
            .map(|j| map_rows[e][j].clone() * solution.coefficients[j].clone())
            .sum();
        let expected_residual = &target[e] - &mapped;
        assert_eq!(
            solution.residual[e], expected_residual,
            "Residual mismatch at coordinate {e}"
        );
    }

    // 5. Primal objective matches weighted L1 norm of residual: ||z||_{1,w}
    let computed_norm: BigRational = solution
        .residual
        .iter()
        .zip(weights)
        .map(|(z, w)| z.abs() * w.clone())
        .sum();
    assert_eq!(
        solution.value, computed_norm,
        "Objective value does not match computed weighted L1 norm"
    );
}

// =========================================================================
// 1. Sparse Revised Simplex Adversarial Stress Tests
// =========================================================================

#[test]
fn test_simplex_zero_target_degeneracy() {
    // Zero target vector causes x_B = 0 everywhere (complete degeneracy from step 0).
    let target = vec![ri(0), ri(0), ri(0)];
    let weights = vec![ri(1), ri(2), ri(3)];
    let map = vec![vec![ri(1), ri(-1)], vec![ri(0), ri(1)], vec![ri(-1), ri(0)]];
    let solution = solve_weighted_l1_projection(&target, &weights, &map, 1024)
        .expect("Zero target must solve cleanly");
    assert_eq!(solution.value, ri(0));
    assert!(solution.residual.iter().all(BigRational::is_zero));
    assert_dual_invariants(&solution, &target, &weights, &map);
}

#[test]
fn test_simplex_collinear_and_redundant_generators() {
    // Map with redundant and collinear columns:
    // col 1 = 2 * col 0
    // col 2 = -col 0
    // col 3 = col 0 + col 1 = 3 * col 0
    let map = vec![
        vec![ri(1), ri(2), ri(-1), ri(3)],
        vec![ri(-1), ri(-2), ri(1), ri(-3)],
        vec![ri(2), ri(4), ri(-2), ri(6)],
    ];
    let target = vec![ri(5), ri(1), ri(-2)];
    let weights = vec![ri(1), ri(1), ri(1)];
    let solution = solve_weighted_l1_projection(&target, &weights, &map, 1024)
        .expect("Redundant generators must solve without cycling or singular panic");
    assert_dual_invariants(&solution, &target, &weights, &map);
}

#[test]
fn test_simplex_beale_style_degenerate_cycling_resistance() {
    // Construct an overdetermined system where many basic solutions share x_B[i] = 0,
    // stressing degeneracy tracking and Bland's smallest-index rule.
    let m = 6;
    let k = 4;
    let mut map = vec![vec![ri(0); k]; m];
    // Fill with rank-deficient subspace
    map[0][0] = ri(1);
    map[0][1] = ri(0);
    map[0][2] = ri(1);
    map[0][3] = ri(1);
    map[1][0] = ri(0);
    map[1][1] = ri(1);
    map[1][2] = ri(1);
    map[1][3] = ri(-1);
    map[2][0] = ri(1);
    map[2][1] = ri(1);
    map[2][2] = ri(2);
    map[2][3] = ri(0);
    map[3][0] = ri(1);
    map[3][1] = ri(-1);
    map[3][2] = ri(0);
    map[3][3] = ri(2);
    map[4][0] = ri(2);
    map[4][1] = ri(0);
    map[4][2] = ri(2);
    map[4][3] = ri(2);
    map[5][0] = ri(0);
    map[5][1] = ri(2);
    map[5][2] = ri(2);
    map[5][3] = ri(-2);

    let target = vec![ri(1), ri(-1), ri(0), ri(2), ri(1), ri(-3)];
    let weights = vec![ri(1), ri(2), ri(1), ri(3), ri(2), ri(1)];

    let solution = solve_weighted_l1_projection(&target, &weights, &map, 2048)
        .expect("Degenerate instance must terminate via Bland rule");
    assert_dual_invariants(&solution, &target, &weights, &map);
}

#[test]
fn test_simplex_extreme_rational_scale() {
    // Stress big integers (> 64-bit numerators/denominators)
    let big_num_1 = "100000000000000000000000000001";
    let big_den_1 = "300000000000000000000000000007";
    let big_num_2 = "700000000000000000000000000003";
    let big_den_2 = "110000000000000000000000000009";

    let target = vec![
        q_big(big_num_1, big_den_1),
        q_big(big_num_2, big_den_2),
        ri(-1),
    ];
    let weights = vec![ri(1), ri(1), ri(1)];
    let map = vec![vec![ri(1), ri(0)], vec![ri(0), ri(1)], vec![ri(1), ri(1)]];
    let solution = solve_weighted_l1_projection(&target, &weights, &map, 1024)
        .expect("Large rational arithmetic must preserve exactness without overflow");
    assert_dual_invariants(&solution, &target, &weights, &map);
}

#[test]
fn test_simplex_invalid_inputs_fail_closed() {
    let target = vec![ri(1), ri(2)];
    let weights_non_pos = vec![ri(1), ri(0)]; // zero weight is invalid
    let map = vec![vec![ri(1)], vec![ri(1)]];

    assert!(matches!(
        solve_weighted_l1_projection(&target, &weights_non_pos, &map, 100),
        Err(L1LpError::NonPositiveWeight(1))
    ));

    let weights_neg = vec![ri(1), ri(-5)];
    assert!(matches!(
        solve_weighted_l1_projection(&target, &weights_neg, &map, 100),
        Err(L1LpError::NonPositiveWeight(1))
    ));

    let weights_len_mismatch = vec![ri(1)];
    assert!(matches!(
        solve_weighted_l1_projection(&target, &weights_len_mismatch, &map, 100),
        Err(L1LpError::DimensionMismatch { target: 2, rows: 1 })
    ));

    let ragged_map = vec![vec![ri(1), ri(2)], vec![ri(1)]];
    assert!(matches!(
        solve_weighted_l1_projection(&target, &vec![ri(1), ri(1)], &ragged_map, 100),
        Err(L1LpError::RaggedMap {
            row: 1,
            expected: 2,
            actual: 1
        })
    ));
}

// =========================================================================
// 2. Network Simplex Adversarial Stress Tests
// =========================================================================

#[test]
fn test_network_simplex_large_directed_cycle() {
    // 6-cycle with alternating unit circulation
    let edges = vec![
        BoundaryEdge {
            tail: 0,
            head: 1,
            weight: 2,
        },
        BoundaryEdge {
            tail: 1,
            head: 2,
            weight: 3,
        },
        BoundaryEdge {
            tail: 2,
            head: 3,
            weight: 1,
        },
        BoundaryEdge {
            tail: 3,
            head: 4,
            weight: 4,
        },
        BoundaryEdge {
            tail: 4,
            head: 5,
            weight: 2,
        },
        BoundaryEdge {
            tail: 5,
            head: 0,
            weight: 5,
        },
    ];
    let boundary = Boundary1 {
        num_vertices: 6,
        edges,
    };
    let omega = vec![1, 1, 1, 1, 1, 1]; // unit 1-chain
    let sol = solve_phi1(&boundary, &omega).expect("Network simplex must solve 6-cycle");
    assert!(sol.objective >= 0);
    assert_eq!(sol.vertex_potential.len(), 6);
}

#[test]
fn test_network_simplex_unbalanced_demand_refused() {
    let arcs = vec![Arc {
        tail: 0,
        head: 1,
        cost: 1,
        lower: 0,
        upper: None,
        original_edge: None,
        orientation_sign: 1,
    }];
    let unbalanced_demand = vec![10, -5]; // sum = 5 != 0
    let mut ns = NetworkSimplex::new(2, arcs, unbalanced_demand).unwrap();
    assert!(matches!(
        ns.solve(),
        Err(NetworkSimplexError::UnbalancedDemand { sum: 5 })
    ));
}

#[test]
fn test_network_simplex_empty_boundary_refused() {
    let empty_boundary = Boundary1 {
        num_vertices: 0,
        edges: vec![],
    };
    assert!(matches!(
        solve_phi1(&empty_boundary, &[]),
        Err(NetworkSimplexError::InvalidCarrier { .. })
    ));

    // Standalone NetworkSimplex on 0 nodes trivial network solves with 0 objective
    let mut ns = NetworkSimplex::new(0, vec![], vec![]).unwrap();
    let sol = ns
        .solve()
        .expect("Trivial 0-node network solves with zero cost");
    assert_eq!(sol.objective, 0);
    assert!(sol.flow.is_empty());
}

// =========================================================================
// 3. Phi1 Form Certificate Adversarial Falsification Matrix
// =========================================================================

#[test]
fn test_phi1_falsified_dual_weight_violation_rejected() {
    let weights = vec![ri(2), ri(3), ri(1)];
    let residual = vec![ri(1), ri(1), ri(1)];
    // Falsified: coordinate 0 has |phi_0| = 5/2 > w_0 = 2
    let falsified_dual = vec![rq(5, 2), ri(1), ri(1)];
    let coboundaries = vec![vec![ri(0), ri(0), ri(0)]];
    let cert = Phi1FormCertificate {
        weights,
        residual_at_achiever: residual,
        dual: falsified_dual,
        coboundaries,
    };
    assert!(matches!(
        cert.verify(),
        Err(Phi1FormError::DualExceedsWeight { index: 0 })
    ));
}

#[test]
fn test_phi1_falsified_dual_not_perpendicular_rejected() {
    let weights = vec![ri(1), ri(1), ri(1)];
    let residual = vec![ri(1), ri(1), ri(1)];
    // Dual witness that does not annihilate coboundary:
    // coboundary = (1, -1, 0)
    // dual = (1, 1, 0) -> <phi, coboundary> = 1 - 1*(-1)? No, 1*1 + 1*(-1) = 0.
    // Let dual = (1, 0, 0) -> <phi, coboundary> = 1 != 0
    let dual = vec![ri(1), ri(0), ri(0)];
    let coboundaries = vec![vec![ri(1), ri(-1), ri(0)]];
    let cert = Phi1FormCertificate {
        weights,
        residual_at_achiever: residual,
        dual,
        coboundaries,
    };
    assert!(matches!(
        cert.verify(),
        Err(Phi1FormError::DualNotPerpendicular {
            coboundary_index: 0
        })
    ));
}

#[test]
fn test_phi1_falsified_duality_gap_rejected() {
    let weights = vec![ri(1), ri(1), ri(1)];
    let residual = vec![ri(2), ri(2), ri(2)];
    // Dual is bounded and orthogonal to coboundary, but doesn't attain ||r||_{1,w}:
    // wl1 = 1*2 + 1*2 + 1*2 = 6.
    // dual = (0, 0, 0) -> <phi, r> = 0 != 6.
    let dual = vec![ri(0), ri(0), ri(0)];
    let coboundaries = vec![vec![ri(1), ri(-1), ri(0)]];
    let cert = Phi1FormCertificate {
        weights,
        residual_at_achiever: residual,
        dual,
        coboundaries,
    };
    assert!(matches!(
        cert.verify(),
        Err(Phi1FormError::DualityGapNonZero)
    ));
}

#[test]
fn test_phi1_dimension_mismatches_rejected() {
    let cert_wrong_residual = Phi1FormCertificate {
        weights: vec![ri(1), ri(1)],
        residual_at_achiever: vec![ri(1)],
        dual: vec![ri(1), ri(1)],
        coboundaries: vec![],
    };
    assert!(matches!(
        cert_wrong_residual.verify(),
        Err(Phi1FormError::DimensionMismatch {
            expected: 2,
            actual: 1
        })
    ));

    let cert_wrong_dual = Phi1FormCertificate {
        weights: vec![ri(1), ri(1)],
        residual_at_achiever: vec![ri(1), ri(1)],
        dual: vec![ri(1), ri(1), ri(1)],
        coboundaries: vec![],
    };
    assert!(matches!(
        cert_wrong_dual.verify(),
        Err(Phi1FormError::DimensionMismatch {
            expected: 2,
            actual: 3
        })
    ));

    let cert_wrong_coboundary = Phi1FormCertificate {
        weights: vec![ri(1), ri(1)],
        residual_at_achiever: vec![ri(1), ri(1)],
        dual: vec![ri(1), ri(1)],
        coboundaries: vec![vec![ri(1)]],
    };
    assert!(matches!(
        cert_wrong_coboundary.verify(),
        Err(Phi1FormError::DimensionMismatch {
            expected: 2,
            actual: 1
        })
    ));
}

// =========================================================================
// 4. Phi1Verifier LP Max-Form Duality Checker Tests
// =========================================================================

#[test]
fn test_phi1_verifier_valid_lp_certificate() {
    // Maximize 2 x1 + 3 x2
    // Subject to:
    // x1 + x2 <= 4
    // x1 + 2 x2 <= 5
    // x1, x2 >= 0
    // Optimum: x1 = 3, x2 = 1, value = 9.
    // Dual: minimize 4 y1 + 5 y2
    // Subject to:
    // y1 + y2 >= 2
    // y1 + 2 y2 >= 3
    // y1, y2 >= 0
    // Dual optimum: y1 = 1, y2 = 1, value = 4*1 + 5*1 = 9.
    let primal = vec![ri(3), ri(1)];
    let dual = vec![ri(1), ri(1)];
    let a = vec![vec![ri(1), ri(1)], vec![ri(1), ri(2)]];
    let b = vec![ri(4), ri(5)];
    let c = vec![ri(2), ri(3)];

    let cert = Phi1Verifier::verify(&primal, &dual, &a, &b, &c)
        .expect("Valid LP certificate must verify cleanly");
    assert_eq!(*cert.primal_objective(), ri(9));
    assert_eq!(*cert.dual_objective(), ri(9));
}

#[test]
fn test_phi1_verifier_falsified_duality_gap() {
    let primal = vec![ri(3), ri(1)];
    // Perturbed dual: y1 = 2, y2 = 1 -> dual obj = 4*2 + 5*1 = 13 != 9
    let dual = vec![ri(2), ri(1)];
    let a = vec![vec![ri(1), ri(1)], vec![ri(1), ri(2)]];
    let b = vec![ri(4), ri(5)];
    let c = vec![ri(2), ri(3)];

    assert!(matches!(
        Phi1Verifier::verify(&primal, &dual, &a, &b, &c),
        Err(CertificateError::DualityGapDetected)
    ));
}

#[test]
fn test_phi1_verifier_primal_infeasible() {
    // Violates x1 + x2 <= 4: x1 = 3, x2 = 2 -> 5 <= 4 false
    let primal = vec![ri(3), ri(2)];
    let dual = vec![ri(1), ri(1)];
    let a = vec![vec![ri(1), ri(1)], vec![ri(1), ri(2)]];
    let b = vec![ri(4), ri(5)];
    let c = vec![ri(2), ri(3)];

    assert!(matches!(
        Phi1Verifier::verify(&primal, &dual, &a, &b, &c),
        Err(CertificateError::Infeasible)
    ));
}

#[test]
fn test_phi1_verifier_dual_infeasible() {
    let primal = vec![ri(3), ri(1)];
    // Violates y1 + 2 y2 >= 3: y1 = 1, y2 = 0 -> 1 >= 3 false
    let dual = vec![ri(1), ri(0)];
    let a = vec![vec![ri(1), ri(1)], vec![ri(1), ri(2)]];
    let b = vec![ri(4), ri(5)];
    let c = vec![ri(2), ri(3)];

    assert!(matches!(
        Phi1Verifier::verify(&primal, &dual, &a, &b, &c),
        Err(CertificateError::Infeasible)
    ));
}
