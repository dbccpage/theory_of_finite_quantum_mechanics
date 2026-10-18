// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

//! Integration tests and mutation kill tests for Campaign C1000 Block 07 Contextuality Obstruction.

use finite_qm_native::campaigns::contextuality_obstruction::evaluate_campaign_block_07;
use omega_quantum_physics::contextuality_obstruction::*;
use omega_quantum_physics::kochen_specker::CABELLO_9_CONTEXTS;

#[test]
fn test_t965_reimplementation_cochain_complex() {
    let x1 = construct_cabello_scenario();
    let cx_x1 = build_cochain_complex(&x1).unwrap();
    assert_eq!(cx_x1.dim_c0, 27);
    assert_eq!(cx_x1.dim_c1, 18);
    assert_eq!(cx_x1.dim_c2, 0);
    assert!(cx_x1.diff_squares_to_zero);

    let res_x1 = compute_obstruction_class(&x1).unwrap();
    assert_eq!(res_x1.rank_delta0, 17);
    assert_eq!(res_x1.dim_h1, 1);
    assert!(!res_x1.obstruction_class_is_zero);
    assert!(res_x1.class_representative.contains("!= 0"));

    let x2 = construct_product_scenario();
    let cx_x2 = build_cochain_complex(&x2).unwrap();
    assert_eq!(cx_x2.dim_c0, 4);
    assert_eq!(cx_x2.dim_c1, 4);
    assert_eq!(cx_x2.dim_c2, 0);
    assert!(cx_x2.diff_squares_to_zero);

    let res_x2 = compute_obstruction_class(&x2).unwrap();
    assert_eq!(res_x2.rank_delta0, 3);
    assert_eq!(res_x2.dim_h1, 1);
    assert!(res_x2.obstruction_class_is_zero);
    assert!(res_x2.global_section_exhibited);
    assert_eq!(res_x2.exhibited_global_section, Some(vec![1, 1, 0, 0]));
}

#[test]
fn test_t966_cross_language_parity() {
    let receipt = evaluate_campaign_block_07().unwrap();
    assert_eq!(receipt.block, 7);
    assert_eq!(receipt.campaign, "C1000");
    assert!(receipt.differential_squares_to_zero_proved);
    assert!(receipt.negative_control_discharged);
    assert!(receipt.every_verdict_names_coefficients);
    assert_eq!(
        receipt.terminal_outcome,
        "OBSTRUCTION_CLASSES_COMPUTED_EXACTLY"
    );

    assert_eq!(receipt.scenarios.len(), 2);
    let x1 = &receipt.scenarios[0];
    assert_eq!(x1.id, "X1");
    assert_eq!(x1.coefficient_group, "Z_2");
    assert_eq!(x1.dim_c0, 27);
    assert_eq!(x1.dim_c1, 18);
    assert_eq!(x1.rank_delta0, 17);
    assert_eq!(x1.dim_h1, 1);
    assert!(!x1.obstruction_class_is_zero);
    assert_eq!(x1.verdict, "CONTEXTUAL_OBSTRUCTION_PRESENT");

    let x2 = &receipt.scenarios[1];
    assert_eq!(x2.id, "X2");
    assert_eq!(x2.coefficient_group, "Z_2");
    assert_eq!(x2.dim_c0, 4);
    assert_eq!(x2.dim_c1, 4);
    assert_eq!(x2.rank_delta0, 3);
    assert_eq!(x2.dim_h1, 1);
    assert!(x2.obstruction_class_is_zero);
    assert_eq!(x2.verdict, "NON_CONTEXTUAL_AT_DECLARED_COEFFICIENTS");
    assert_eq!(x2.exhibited_global_section, Some(vec![1, 1, 0, 0]));
}

#[test]
fn test_t967_mutation_1_differential_not_squaring_to_zero() {
    let x1 = construct_cabello_scenario();
    let mut cx = build_cochain_complex(&x1).unwrap();
    let row = (0..cx.dim_c1)
        .find(|&r| !cx.delta0_matrix.row(r).unwrap().is_zero())
        .unwrap();
    cx.dim_c2 = 1;
    cx.d1_matrix = omega_number_theory::gf2::F2Matrix::zeros(1, cx.dim_c1).unwrap();
    cx.d1_matrix.set(0, row, true).unwrap();
    assert!(cx.checked_complex().is_err());
}

#[test]
fn test_t967_mutation_2_missing_context() {
    let bad_contexts: Vec<Vec<usize>> =
        CABELLO_9_CONTEXTS[2..].iter().map(|c| c.to_vec()).collect();
    let bad_scen = MeasurementScenario {
        name: "missing contexts".to_string(),
        scenario_id: "X1_bad".to_string(),
        ray_count: 18,
        contexts: bad_contexts,
        b_targets: vec![1; 7],
        coefficient_group: "Z_2".to_string(),
        carrier: CARRIER.to_string(),
        conductor: CONDUCTOR,
        declared_global_section: None,
    };
    assert!(bad_scen.validate().is_err());
}

#[test]
fn test_t967_mutation_3_coefficients_switched() {
    let mut bad = construct_cabello_scenario();
    bad.coefficient_group = "Q".into();
    assert!(bad.validate().is_err());
    assert!(compute_obstruction_class(&bad).is_err());
}

#[test]
fn test_t967_mutation_4_x2_reported_nonzero() {
    let x2 = construct_product_scenario();
    let res = compute_obstruction_class(&x2).unwrap();
    assert!(
        res.obstruction_class_is_zero,
        "X2 obstruction class must vanish"
    );
}

#[test]
fn test_t967_mutation_5_invalid_global_section_restriction() {
    let x2 = construct_product_scenario();
    let bad_section = vec![0, 0, 0, 0];
    let (valid, violating) = verify_global_section(&x2, &bad_section);
    assert!(!valid, "Bad section must not be valid");
    assert_eq!(violating.len(), 4);
}
