// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)
//! Integration tests and negative controls for Campaign C750 Block 01 (C750-T567).

use finite_qm_native::c750_b01_solver::*;
use linear_algebra::exact_field::matrix as mx;
use linear_algebra::linear_algebra::image_kernel::{
    solve_in_image, ExactRowReduction, ImageMembership,
};

#[test]
fn test_mutation_1_float_rejection() {
    assert!(parse_exact_rational("0.5").is_err());
    assert!(parse_exact_rational("1e-5").is_err());
    assert!(parse_exact_rational("3.14159").is_err());
    assert!(parse_exact_rational("1/2").is_ok());
}

#[test]
fn test_mutation_2_zero_log_zero_singularity() {
    // Direct factorization of 0 fails
    assert!(
        omega_number_theory::integer_factorization::factor_positive_rational(
            &r_int(0),
            omega_number_theory::integer_factorization::FactorizationBudget {
                max_operations: 1_000_000
            }
        )
        .is_err()
    );

    // Spectrum with zero eigenvalues handled cleanly under 0 log 0 = 0
    let evals_pure = vec![r_int(1), r_int(0)];
    let res_pure = reduce_multiplicative_dependence(&evals_pure, None).unwrap();
    assert!(res_pure.is_pure);
    assert_eq!(res_pure.verdict, "ZERO_ENTROPY_PURE");

    let evals_mixed = vec![r_frac(1, 2), r_frac(1, 2), r_int(0)];
    let res_mixed = reduce_multiplicative_dependence(&evals_mixed, None).unwrap();
    assert!(!res_mixed.is_pure);
    assert_eq!(res_mixed.verdict, "TRANSCENDENTAL_BY_BAKER");
}

#[test]
fn test_mutation_3_unnormalized_spectrum_rejection() {
    let unnorm = vec![r_frac(1, 2), r_frac(1, 3)]; // sum = 5/6 != 1
    assert!(reduce_multiplicative_dependence(&unnorm, None).is_err());
}

#[test]
fn test_mutation_4_splitting_degree_honesty() {
    // Polynomial x^2 - 2 does not split over Q (roots +-sqrt(2) not in Q)
    // Claiming extension degree = 1 over Q is an illegal fraudulent claim.
    let irrational = finite_qm_native::c750_campaign::splitting_degree_2(&r_int(0), &r_int(-2));
    assert_eq!(irrational, 2);
    assert_eq!(
        finite_qm_native::c750_campaign::splitting_degree_2(&r_int(0), &r_int(-4)),
        1
    );
}

#[test]
fn test_mutation_5_planted_algebraic_mixed_entropy_rejection() {
    // A mixed state has non-vanishing reduced coefficients and is strictly transcendental
    let evals = vec![r_frac(3, 4), r_frac(1, 4)];
    let res = reduce_multiplicative_dependence(&evals, None).unwrap();
    assert!(!res.is_pure);
    assert!(res.entropy_value_exact.is_none());
    assert_eq!(res.verdict, "TRANSCENDENTAL_BY_BAKER");
}

#[test]
fn test_fqmi1_eight_systems_parity_receipt() {
    let receipt = generate_c750_b01_parity_receipt().expect("Receipt generation failed");
    assert_eq!(receipt.total_systems_verified, 8);
    assert!(receipt.all_byte_deterministic);
    assert_eq!(receipt.systems.len(), 8);
}

#[test]
fn parity_cannot_be_claimed_after_any_computed_record_is_changed() {
    let actual = evaluate_fqmi1_system("S1").unwrap();
    assert!(actual.byte_parity_match);
    let mut wrong = actual.clone();
    wrong.purity_p2 = "1/2".into();
    assert!(!parity_against_reference(&actual, &wrong));
    wrong = actual.clone();
    wrong.evidence_sha256 = "0".repeat(64);
    assert!(!parity_against_reference(&actual, &wrong));
    wrong = actual.clone();
    wrong.reduced_coefficients[0] = "3/1".into();
    assert!(!parity_against_reference(&actual, &wrong));
}

#[test]
fn entropy_interval_uses_bounded_precision_and_refuses_bad_arguments() {
    let reduction = reduce_multiplicative_dependence(&[r_frac(3, 4), r_frac(1, 4)], None).unwrap();
    let coarse = approximate_entropy_rational_bounds(&reduction, 16).unwrap();
    let precise = approximate_entropy_rational_bounds(&reduction, 64).unwrap();
    assert!(coarse.0 <= precise.0 && precise.1 <= coarse.1);
    assert!(precise.0 > r_int(0) && precise.1 < r_int(1));
    assert!(rational_log_bounds(1, 32).is_err());
    assert!(rational_log_bounds(2, 0).is_err());
    assert!(rational_log_bounds(2, usize::MAX).is_err());
}

#[test]
fn power_traces_and_entropy_bounds_refuse_multiplicity_or_claim_mutations() {
    assert!(exact_power_trace(&[r_frac(1, 2), r_frac(1, 2)], Some(&[1]), 2).is_err());
    assert!(exact_power_trace(&[r_frac(1, 2), r_frac(1, 2)], Some(&[0, 2]), 2).is_err());
    let mut reduction =
        reduce_multiplicative_dependence(&[r_frac(1, 2), r_frac(1, 2)], None).unwrap();
    reduction.is_pure = true;
    assert!(approximate_entropy_rational_bounds(&reduction, 32).is_err());
    reduction = reduce_multiplicative_dependence(&[r_frac(1, 2), r_frac(1, 2)], None).unwrap();
    reduction.reduced_coefficients[0] = "0/1".into();
    assert!(approximate_entropy_rational_bounds(&reduction, 32).is_err());
}

#[test]
fn malformed_matrices_are_refused_and_inconsistent_systems_remain_distinct() {
    let ragged = vec![vec![r_int(1)], vec![r_int(1), r_int(0)]];
    assert!(mx::from_rows(ragged).is_err());
    let scalar = mx::from_rows(vec![vec![r_int(1)]]).unwrap();
    assert!(solve_in_image(&scalar, &[]).is_err());
    assert!(matches!(
        solve_in_image(&mx::zeros::<Rational>(1, 1).unwrap(), &[r_int(1)]).unwrap(),
        ImageMembership::NotInImage { .. }
    ));
    let kernel = mx::zeros::<Rational>(0, 3).unwrap().kernel_basis().unwrap();
    assert_eq!(kernel.vectors().len(), 3);
    assert!(kernel.vectors().iter().all(|vector| vector.len() == 3));
}
