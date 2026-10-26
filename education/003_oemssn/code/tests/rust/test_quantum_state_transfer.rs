//! Integration tests for Exact Gaussian-Rational Quantum Mechanics & Categorical State Transfer.
//!
//! AuthorityEffect: None. GenesisEffect: None.

use mssn_stage_024::quantum_state_transfer::{
    audit_anyon_f_matrix, audit_distillation_step, audit_tripartite_ghz_witness,
    distill_bbpssw, verify_quantum_state_transfer, AnyonModel, DensityMatrix8D,
    GaussianRational, PauliGate, Rational, StateVector, TeleportationError,
};

#[test]
fn test_exact_gaussian_rational_arithmetic() {
    // z1 = 1/2 + 3/4 i
    let z1 = GaussianRational::from_fractions(1, 2, 3, 4);
    // z2 = 2/3 - 1/5 i
    let z2 = GaussianRational::from_fractions(2, 3, -1, 5);

    // Sum: (1/2 + 2/3) + i (3/4 - 1/5) = 7/6 + i 11/20
    let sum = z1.add(&z2);
    assert_eq!(sum.re, Rational::new(7, 6));
    assert_eq!(sum.im, Rational::new(11, 20));

    // Squared modulus: |z1|^2 = (1/2)^2 + (3/4)^2 = 1/4 + 9/16 = 13/16
    let norm_sq = z1.norm_squared();
    assert_eq!(norm_sq, Rational::new(13, 16));

    // Multiplication: (1 + i)(1 - i) = 1 - i^2 = 2
    let a = GaussianRational::from_integers(1, 1);
    let b = GaussianRational::from_integers(1, -1);
    let prod = a.mul(&b);
    assert_eq!(prod.re, Rational::new(2, 1));
    assert_eq!(prod.im, Rational::ZERO);
}

#[test]
fn test_path_a_pythagorean_superposition_unit_norm() {
    // |psi> = 3/5 |0> + 4/5 i |1>
    let c0 = GaussianRational::from_fractions(3, 5, 0, 1);
    let c1 = GaussianRational::from_fractions(0, 1, 4, 5);
    let psi = StateVector::new(vec![c0, c1]);

    // ||psi||^2 = (3/5)^2 + (4/5)^2 = 9/25 + 16/25 = 25/25 = 1 in Q
    assert!(psi.is_exact_unit_norm(), "Pythagorean state must have exact unit norm");
    assert_eq!(psi.norm_squared(), Rational::ONE);
}

#[test]
fn test_path_b_projective_ray_expectation_value() {
    // Unnormalized equal superposition: |psi> = |0> + |1>
    let c0 = GaussianRational::from_integers(1, 0);
    let c1 = GaussianRational::from_integers(1, 0);
    let psi = StateVector::new(vec![c0, c1]);

    // ||psi||^2 = 1^2 + 1^2 = 2 in Q (no square roots needed!)
    assert_eq!(psi.norm_squared(), Rational::new(2, 1));

    // Apply Pauli X operator: X|psi> = X(|0> + |1>) = |1> + |0> = |psi>
    let x_psi = PauliGate::X.apply(&psi);
    // <psi | X | psi> = <psi | psi> = 2
    let num = psi.inner_product(&x_psi);
    // Expectation value <X> = <psi | X | psi> / <psi | psi> = 2 / 2 = 1 in Q
    let exp_val = num.re.div(&psi.norm_squared());
    assert_eq!(exp_val, Rational::ONE, "Expectation value <X> must be exactly 1");
}

#[test]
fn test_teleportation_exact_fidelity_all_branches() {
    // Teleport candidate state: |psi_in> = 3/5 |0> + 4/5 i |1>
    let c0 = GaussianRational::from_fractions(3, 5, 0, 1);
    let c1 = GaussianRational::from_fractions(0, 1, 4, 5);
    let psi_in = StateVector::new(vec![c0, c1]);

    let receipt = verify_quantum_state_transfer(&psi_in, None)
        .expect("Teleportation verification must succeed across all 4 channels");

    assert_eq!(receipt.status, "TELEPORTATION_CERTIFIED");
    assert_eq!(receipt.total_branches, 4);
    assert_eq!(receipt.branches_passed, 4);

    for branch in &receipt.branches {
        assert!(branch.branch_certified);
        assert_eq!(branch.fidelity_rational, "1/1", "Every branch must achieve exact rational fidelity 1/1");
    }

    let json = serde_json::to_string_pretty(&receipt).expect("Receipt must serialize");
    assert!(json.contains("\"TELEPORTATION_CERTIFIED\""));
    assert!(json.contains("\"branches_passed\": 4"));
}

#[test]
fn test_feedforward_mismatch_fails_closed() {
    // Candidate state |0>
    let psi_in = StateVector::new(vec![
        GaussianRational::from_integers(1, 0),
        GaussianRational::ZERO,
    ]);

    // Corrupt branch (1, 0): apply X instead of Z
    let corrupted_feedforward = [
        (0, 0, PauliGate::I),
        (1, 0, PauliGate::X), // WRONG: should be Z
        (0, 1, PauliGate::X),
        (1, 1, PauliGate::XZ),
    ];

    let err = verify_quantum_state_transfer(&psi_in, Some(corrupted_feedforward))
        .expect_err("Corrupted feedforward must fail closed");

    match err {
        TeleportationError::FeedforwardFidelityDefect(msg) => {
            assert!(msg.contains("yielded fidelity"));
            assert!(msg.contains("!= 1"));
        }
        other => panic!("Expected FeedforwardFidelityDefect, got: {:?}", other),
    }
}

#[test]
fn test_bbpssw_distillation_exact_rational_purification() {
    // 1. Initial Noisy Pair: F_0 = 3/5 = 0.60
    let f0 = Rational::new(3, 5);
    let f1 = distill_bbpssw(f0);
    // F_1 = ((3/5)^2 + 1/9 (2/5)^2) / ((3/5)^2 + 2/3 (3/5)(2/5) + 5/9 (2/5)^2)
    // Numerator: 9/25 + 4/225 = 85/225 = 17/45
    // Denominator: 9/25 + 12/75 + 20/225 = 81/225 + 36/225 + 20/225 = 137/225
    // F_1 = (85/225) / (137/225) = 85/137 ~ 0.620438
    assert_eq!(f1, Rational::new(85, 137));
    assert!(f1 > f0, "Distillation must strictly increase fidelity when F > 1/2");

    let receipt0 = audit_distillation_step(f0).expect("Valid distillation input");
    assert_eq!(receipt0.status, "DISTILLATION_PURIFIED");
    assert_eq!(receipt0.terminal_route, "RouteRepair");
    assert!(receipt0.is_purified);
    assert_eq!(receipt0.output_fidelity, "85/137");

    // 2. Second Iteration: F_1 = 85/137
    let f2 = distill_bbpssw(f1);
    assert_eq!(f2, Rational::new(67729, 105065));
    assert!(f2 > f1, "Subsequent distillation step must strictly increase fidelity");

    // 3. Sub-threshold input: F = 1/2 (unpurifiable fixed point)
    let f_half = Rational::new(1, 2);
    let receipt_half = audit_distillation_step(f_half).expect("F=1/2 is in [0, 1]");
    assert_eq!(receipt_half.status, "DISTILLATION_EFFICIENCY_DEFECT");
    assert_eq!(receipt_half.terminal_route, "SplitBrainRefusal");
    assert!(!receipt_half.is_purified);
    assert_eq!(receipt_half.output_fidelity, "1/2"); // Fixed point!

    // 4. Sub-threshold input: F = 1/3 (fidelity decreases!)
    let f_third = Rational::new(1, 3);
    let receipt_third = audit_distillation_step(f_third).expect("F=1/3 is in [0, 1]");
    assert_eq!(receipt_third.status, "DISTILLATION_EFFICIENCY_DEFECT");
    assert_eq!(receipt_third.terminal_route, "SplitBrainRefusal");
    assert!(!receipt_third.is_purified);
}

#[test]
fn test_tripartite_ghz_witness_operator_trace() {
    // 1. GHZ State: |GHZ> = 1/sqrt(2) (|000> + |111>)
    // Density matrix has 1/2 on (0,0), (0,7), (7,0), (7,7)
    let ghz = DensityMatrix8D::ghz_state();
    assert_eq!(ghz.trace(), GaussianRational::ONE);

    let receipt_ghz = audit_tripartite_ghz_witness("state_ghz_tripartite", &ghz);
    assert_eq!(receipt_ghz.status, "ENTANGLED_CERTIFIED");
    assert_eq!(receipt_ghz.terminal_route, "RouteRepair");
    assert!(receipt_ghz.is_entangled);
    // Tr(W * rho_GHZ) = 1/2(1) - 1 = -1/2 < 0
    assert_eq!(receipt_ghz.computed_trace, "-1/2");

    // 2. Separable Product State: |000><000|
    let sep = DensityMatrix8D::separable_zero_state();
    let receipt_sep = audit_tripartite_ghz_witness("state_separable_zero", &sep);
    assert_eq!(receipt_sep.status, "SEPARABLE_DEFECT");
    assert_eq!(receipt_sep.terminal_route, "SplitBrainRefusal");
    assert!(!receipt_sep.is_entangled);
    // Tr(W * rho_sep) = 0/1 >= 0
    assert_eq!(receipt_sep.computed_trace, "0/1");
}

#[test]
fn test_nonabelian_anyon_f_matrix_involution_consistency() {
    // 1. Fibonacci anyon model: F^2 = I_2
    let receipt_fib = audit_anyon_f_matrix(AnyonModel::Fibonacci);
    assert_eq!(receipt_fib.model, "FIBONACCI");
    assert_eq!(receipt_fib.status, "PENTAGON_CONSISTENT");
    assert!(receipt_fib.f_squared_is_identity);
    assert!(receipt_fib.involution_residual_exact_zero);

    // 2. Ising anyon model: F^2 = I_2 (Hadamard involution)
    let receipt_ising = audit_anyon_f_matrix(AnyonModel::Ising);
    assert_eq!(receipt_ising.model, "ISING");
    assert_eq!(receipt_ising.status, "PENTAGON_CONSISTENT");
    assert!(receipt_ising.f_squared_is_identity);
    assert!(receipt_ising.involution_residual_exact_zero);
}
