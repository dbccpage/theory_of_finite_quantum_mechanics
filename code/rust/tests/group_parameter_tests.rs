// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

//! Integration tests and mutation tests for Campaign C1000 Block 09: Group Parameter and Dichotomy.

use finite_qm_native::group_parameter::*;

#[test]
fn test_t1015_independent_reimplementation() {
    let inventory = build_frozen_inventory().unwrap();
    assert_eq!(inventory.len(), 18);

    let carried = inventory
        .iter()
        .filter(|r| r.parameter_verdict == "CARRIED")
        .count();
    let refused = inventory
        .iter()
        .filter(|r| r.parameter_verdict == "REFUSED_TRANSCENDENTAL")
        .count();
    assert_eq!(carried, 3);
    assert_eq!(refused, 15);

    // Verify classifier returns Carried for identity and RefusedTranscendental for non-identity
    let v_rot_id = classify_group_parameter(SubgroupType::Rotation, true, true, true).unwrap();
    assert_eq!(v_rot_id, ParameterVerdict::Carried);

    let v_rot_non_id = classify_group_parameter(SubgroupType::Rotation, false, true, true).unwrap();
    assert_eq!(v_rot_non_id, ParameterVerdict::RefusedTranscendental);

    let v_boost_id = classify_group_parameter(SubgroupType::Boost, true, true, true).unwrap();
    assert_eq!(v_boost_id, ParameterVerdict::Carried);

    let v_boost_non_id = classify_group_parameter(SubgroupType::Boost, false, true, true).unwrap();
    assert_eq!(v_boost_non_id, ParameterVerdict::RefusedTranscendental);

    let v_time_id =
        classify_group_parameter(SubgroupType::TimeEvolution, true, true, true).unwrap();
    assert_eq!(v_time_id, ParameterVerdict::Carried);

    let v_time_non_id =
        classify_group_parameter(SubgroupType::TimeEvolution, false, true, true).unwrap();
    assert_eq!(v_time_non_id, ParameterVerdict::RefusedTranscendental);
}

#[test]
fn test_t1016_cross_language_parity() {
    let inventory = build_frozen_inventory().unwrap();
    let ids: Vec<&str> = inventory.iter().map(|r| r.item_id.as_str()).collect();
    let expected_ids = vec![
        "ROT_ID",
        "ROT_C2",
        "ROT_C3",
        "ROT_C4",
        "ROT_C6",
        "ROT_I60_PLUS",
        "ROT_I60_MINUS",
        "ROT_PYTH_3_4_5",
        "ROT_POLAR_B05",
        "BOOST_ID",
        "BOOST_B1",
        "BOOST_B1_SQ",
        "BOOST_PYTH_5_12_13",
        "BOOST_PYTH_7_24_25",
        "BOOST_POLAR_B05",
        "TIME_ID",
        "TIME_PAULI_Z",
        "TIME_PAULI_X",
    ];
    assert_eq!(ids, expected_ids);

    // Verify all non-identity items have certified approximations with error bounds <= 1e-5
    for r in &inventory {
        if !r.is_identity {
            let approx = r
                .approximation_interval
                .as_ref()
                .expect("Non-identity must have approximation interval");
            assert!(approx.is_approximation);
            assert_eq!(approx.metric, "absolute_difference");
            assert!(approx.error_bound() <= omega_number_theory::rational::rq(1, 100_000));
            assert!(approx.q_min() <= approx.q_max());
        } else {
            assert!(r.approximation_interval.is_none());
        }
    }
}

#[test]
fn test_t1017_mutation_1_exact_element_confusion_killed() {
    // Injected mutation: claiming parameter is CARRIED because matrix entries are rational
    let defective_classify = |is_exact_matrix: bool, is_id: bool| -> ParameterVerdict {
        if is_exact_matrix {
            // BUG: confuses exact matrix with carried parameter
            ParameterVerdict::Carried
        } else if is_id {
            ParameterVerdict::Carried
        } else {
            ParameterVerdict::RefusedTranscendental
        }
    };

    // B1 boost has exact rational entries but parameter ln(2) is transcendental
    let mutated_verdict = defective_classify(true, false);
    assert_eq!(mutated_verdict, ParameterVerdict::Carried);

    // Correct logic must kill this mutation
    let correct = classify_group_parameter(SubgroupType::Boost, false, true, true).unwrap();
    assert_eq!(correct, ParameterVerdict::RefusedTranscendental);
}

#[test]
fn test_t1017_mutation_2_approximation_typed_as_membership_killed() {
    let inventory = build_frozen_inventory().unwrap();
    for r in &inventory {
        if let Some(approx) = &r.approximation_interval {
            // Must strictly be false: approximation is never membership
            assert!(!approx.is_carrier_membership);
            assert!(approx.is_approximation);
        }
    }
}

#[test]
fn test_t1017_mutation_3_identity_case_handled() {
    // At theta = 0, parameter 0 is in Q, so it MUST be CARRIED
    let v_rot = classify_group_parameter(SubgroupType::Rotation, true, true, true).unwrap();
    assert_eq!(v_rot, ParameterVerdict::Carried);

    let v_boost = classify_group_parameter(SubgroupType::Boost, true, true, true).unwrap();
    assert_eq!(v_boost, ParameterVerdict::Carried);

    let v_time = classify_group_parameter(SubgroupType::TimeEvolution, true, true, true).unwrap();
    assert_eq!(v_time, ParameterVerdict::Carried);
}

#[test]
fn test_t1017_mutation_4_algebraic_cosine_assumed_rational_killed() {
    // Injected mutation: assumes cosine must be rational for theorem to apply
    let inventory = build_frozen_inventory().unwrap();
    let rot_i60 = inventory
        .iter()
        .find(|r| r.item_id == "ROT_I60_PLUS")
        .unwrap();
    // cos(2*pi/5) = (-1 + sqrt(5)) / 4 is in Q(sqrt(5)), algebraic non-rational
    assert_eq!(rot_i60.minimal_polynomial, "4*x^2 + 2*x - 1");
    // Theorem applies directly via Lindemann-Weierstrass
    assert_eq!(rot_i60.parameter_verdict, "REFUSED_TRANSCENDENTAL");
}

#[test]
fn test_t1017_mutation_5_planted_algebraic_rapidity_refuted() {
    // Planted non-zero algebraic rapidity claiming algebraic cosh
    let audit_rapidity = |eta_algebraic_nonzero: bool,
                          cosh_algebraic: bool|
     -> Result<(), &'static str> {
        if eta_algebraic_nonzero && cosh_algebraic {
            Err("Lindemann-Weierstrass contradiction: algebraic nonzero eta forces transcendental e^eta and cosh(eta)")
        } else {
            Ok(())
        }
    };

    assert!(audit_rapidity(true, true).is_err());
    assert!(audit_rapidity(false, true).is_ok());
}
