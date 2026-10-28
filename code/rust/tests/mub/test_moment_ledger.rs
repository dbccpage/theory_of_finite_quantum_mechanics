//! Exact diagnostics, negative controls, and cross-runtime fingerprint verification
//! for Target Q5: Exact Moment SDP Hierarchy Ledger and Benchmark Suite.
//!
//! AuthorityEffect: None.

use linear_algebra::exact_ldlt::{
    ldlt_decomposition_rational, ldlt_pivots_strictly_positive_rational,
};
use num_rational::BigRational;
use num_traits::{One, Zero};

use tfqm_mub::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use tfqm_mub::native::exact::mub6_moment_ledger::{
    build_candidate_gramians, build_degree_k_moment_matrix, build_degree_matrices,
    canonical_matrix_payload, certify_flat_extension_rank_gap, certify_universal_mub6_nonexistence,
    claim_universal_mub6_nonexistence, compute_matrix_fingerprint, evaluate_degree_benchmark,
    evaluate_moment_sdp_hierarchy_ledger, load_canonical_fixtures, rational_from_pair,
    repeated_basis_gramian, solve_target_q5_moment_certificate,
    solve_target_q5_moment_certificate_for_degree, verify_canonical_fixtures,
    verify_moment_sdp_ledger_fixtures, DEGREE_2_S6_TRACE, DEGREE_2_X0_TRACE, DEGREE_4_S6_TRACE,
    DEGREE_4_X0_EVALUATED_TRACE, DEGREE_4_X0_NOMINAL_TRACE, DEGREE_6_S6_TRACE, DEGREE_6_X0_TRACE,
    DEGREE_8_S6_TRACE, DEGREE_8_X0_TRACE, SCHEMA_VERSION, SCOPE_STRING,
    STATUS_CERTIFIED_CANDIDATE_REFUTATION, STATUS_MISSING_PROOF_OBLIGATION, SUPPORTED_DEGREES,
};
use tfqm_mub::native::exact::mub6_quad_sdp::{DIM_HILBERT, GRAMIAN_DIM};
use omega_number_theory::cyclotomic::Cyc24;

#[test]
fn test_basis_gramians_and_dimensions() {
    let rep = repeated_basis_gramian();
    assert_eq!(rep.len(), GRAMIAN_DIM);
    assert_eq!(rep[0].len(), GRAMIAN_DIM);

    // Verify repeated basis identity structure
    for i in 0..GRAMIAN_DIM {
        for j in 0..GRAMIAN_DIM {
            if i % DIM_HILBERT == j % DIM_HILBERT {
                assert_eq!(rep[i][j], Cyc24::rat(BigRational::one()));
            } else {
                assert_eq!(rep[i][j], Cyc24::zero());
            }
        }
    }

    let candidates = build_candidate_gramians();
    assert_eq!(candidates.len(), 3);
    assert!(candidates.contains_key("x0"));
    assert!(candidates.contains_key("s6"));
    assert!(candidates.contains_key("repeated"));
}

#[test]
fn test_trace_formulas_degree_2() {
    let entry = evaluate_degree_benchmark(2, None).expect("Degree 2 benchmark failed");
    assert_eq!(entry.degree, 2);
    assert_eq!(entry.level, 1);
    assert_eq!(entry.status, STATUS_CERTIFIED_CANDIDATE_REFUTATION);
    assert_eq!(
        entry.candidate_refutation_status,
        STATUS_CERTIFIED_CANDIDATE_REFUTATION
    );
    assert_eq!(entry.global_search_status, STATUS_MISSING_PROOF_OBLIGATION);
    assert_eq!(
        entry.x0_receipt.status,
        STATUS_CERTIFIED_CANDIDATE_REFUTATION
    );
    assert_eq!(
        entry.s6_receipt.status,
        STATUS_CERTIFIED_CANDIDATE_REFUTATION
    );

    let expected_x0 = rational_from_pair(DEGREE_2_X0_TRACE);
    let expected_s6 = rational_from_pair(DEGREE_2_S6_TRACE);

    let actual_x0 = BigRational::new(
        entry.x0_receipt.inner_product_num.parse().unwrap(),
        entry.x0_receipt.inner_product_den.parse().unwrap(),
    );
    let actual_s6 = BigRational::new(
        entry.s6_receipt.inner_product_num.parse().unwrap(),
        entry.s6_receipt.inner_product_den.parse().unwrap(),
    );

    assert_eq!(actual_x0, expected_x0, "Degree 2 X=0 trace mismatch");
    assert_eq!(actual_s6, expected_s6, "Degree 2 S_6 trace mismatch");
    assert!(entry.x0_receipt.strictly_negative);
    assert!(entry.s6_receipt.strictly_negative);
}

#[test]
fn test_trace_formulas_degree_4() {
    let entry = evaluate_degree_benchmark(4, None).expect("Degree 4 benchmark failed");
    assert_eq!(entry.degree, 4);
    assert_eq!(entry.level, 2);
    assert_eq!(entry.status, STATUS_CERTIFIED_CANDIDATE_REFUTATION);
    assert_eq!(
        entry.candidate_refutation_status,
        STATUS_CERTIFIED_CANDIDATE_REFUTATION
    );
    assert_eq!(entry.global_search_status, STATUS_MISSING_PROOF_OBLIGATION);
    assert_eq!(
        entry.x0_receipt.status,
        STATUS_CERTIFIED_CANDIDATE_REFUTATION
    );
    assert_eq!(
        entry.s6_receipt.status,
        STATUS_CERTIFIED_CANDIDATE_REFUTATION
    );

    let expected_x0_eval = rational_from_pair(DEGREE_4_X0_EVALUATED_TRACE);
    let expected_x0_nom = rational_from_pair(DEGREE_4_X0_NOMINAL_TRACE);
    let expected_s6 = rational_from_pair(DEGREE_4_S6_TRACE);

    let actual_x0 = BigRational::new(
        entry.x0_receipt.inner_product_num.parse().unwrap(),
        entry.x0_receipt.inner_product_den.parse().unwrap(),
    );
    let actual_s6 = BigRational::new(
        entry.s6_receipt.inner_product_num.parse().unwrap(),
        entry.s6_receipt.inner_product_den.parse().unwrap(),
    );

    assert_eq!(
        actual_x0, expected_x0_eval,
        "Degree 4 X=0 evaluated trace mismatch"
    );
    assert_eq!(
        entry.x0_nominal_trace.as_deref(),
        Some("-33/50"),
        "Degree 4 nominal trace bound mismatch"
    );
    assert_eq!(
        rational_from_pair((-33, 50)),
        expected_x0_nom,
        "Degree 4 nominal constant mismatch"
    );
    assert_eq!(actual_s6, expected_s6, "Degree 4 S_6 trace mismatch");
    assert!(entry.x0_receipt.strictly_negative);
    assert!(entry.s6_receipt.strictly_negative);
}

#[test]
fn test_trace_formulas_degree_6() {
    let entry = evaluate_degree_benchmark(6, None).expect("Degree 6 benchmark failed");
    assert_eq!(entry.degree, 6);
    assert_eq!(entry.level, 3);
    assert_eq!(entry.status, STATUS_MISSING_PROOF_OBLIGATION);
    assert_eq!(
        entry.candidate_refutation_status,
        STATUS_MISSING_PROOF_OBLIGATION
    );
    assert_eq!(entry.global_search_status, STATUS_MISSING_PROOF_OBLIGATION);
    assert_eq!(entry.x0_receipt.status, STATUS_MISSING_PROOF_OBLIGATION);
    assert_eq!(entry.s6_receipt.status, STATUS_MISSING_PROOF_OBLIGATION);

    let expected_x0 = rational_from_pair(DEGREE_6_X0_TRACE);
    let expected_s6 = rational_from_pair(DEGREE_6_S6_TRACE);

    let actual_x0 = BigRational::new(
        entry.x0_receipt.inner_product_num.parse().unwrap(),
        entry.x0_receipt.inner_product_den.parse().unwrap(),
    );
    let actual_s6 = BigRational::new(
        entry.s6_receipt.inner_product_num.parse().unwrap(),
        entry.s6_receipt.inner_product_den.parse().unwrap(),
    );

    assert_eq!(actual_x0, expected_x0, "Degree 6 X=0 trace mismatch");
    assert_eq!(actual_s6, expected_s6, "Degree 6 S_6 trace mismatch");
    assert!(entry.x0_receipt.strictly_negative);
    assert!(entry.s6_receipt.strictly_negative);
}

#[test]
fn test_trace_formulas_degree_8() {
    let entry = evaluate_degree_benchmark(8, None).expect("Degree 8 benchmark failed");
    assert_eq!(entry.degree, 8);
    assert_eq!(entry.level, 4);
    assert_eq!(entry.status, STATUS_MISSING_PROOF_OBLIGATION);
    assert_eq!(
        entry.candidate_refutation_status,
        STATUS_MISSING_PROOF_OBLIGATION
    );
    assert_eq!(entry.global_search_status, STATUS_MISSING_PROOF_OBLIGATION);
    assert_eq!(entry.x0_receipt.status, STATUS_MISSING_PROOF_OBLIGATION);
    assert_eq!(entry.s6_receipt.status, STATUS_MISSING_PROOF_OBLIGATION);

    let expected_x0 = rational_from_pair(DEGREE_8_X0_TRACE);
    let expected_s6 = rational_from_pair(DEGREE_8_S6_TRACE);

    let actual_x0 = BigRational::new(
        entry.x0_receipt.inner_product_num.parse().unwrap(),
        entry.x0_receipt.inner_product_den.parse().unwrap(),
    );
    let actual_s6 = BigRational::new(
        entry.s6_receipt.inner_product_num.parse().unwrap(),
        entry.s6_receipt.inner_product_den.parse().unwrap(),
    );

    assert_eq!(actual_x0, expected_x0, "Degree 8 X=0 trace mismatch");
    assert_eq!(actual_s6, expected_s6, "Degree 8 S_6 trace mismatch");
    assert!(entry.x0_receipt.strictly_negative);
    assert!(entry.s6_receipt.strictly_negative);
}

#[test]
fn test_all_dual_witness_pivots_strictly_positive() {
    for &d in SUPPORTED_DEGREES {
        let entry = evaluate_degree_benchmark(d, None).expect("Benchmark failed");
        assert!(
            entry.x0_receipt.pivots_strictly_positive,
            "Degree {d} X=0 witness pivots not all positive"
        );
        assert!(
            entry.s6_receipt.pivots_strictly_positive,
            "Degree {d} S_6 witness pivots not all positive"
        );

        for (idx, p_str) in entry.x0_receipt.pivots.iter().enumerate() {
            let parts: Vec<&str> = p_str.split('/').collect();
            let p = if parts.len() == 1 {
                BigRational::from_integer(parts[0].parse().unwrap())
            } else {
                BigRational::new(parts[0].parse().unwrap(), parts[1].parse().unwrap())
            };
            assert!(
                p > BigRational::zero(),
                "Degree {d} X=0 pivot at {idx} is not strictly positive: {p}"
            );
        }

        for (idx, p_str) in entry.s6_receipt.pivots.iter().enumerate() {
            let parts: Vec<&str> = p_str.split('/').collect();
            let p = if parts.len() == 1 {
                BigRational::from_integer(parts[0].parse().unwrap())
            } else {
                BigRational::new(parts[0].parse().unwrap(), parts[1].parse().unwrap())
            };
            assert!(
                p > BigRational::zero(),
                "Degree {d} S_6 pivot at {idx} is not strictly positive: {p}"
            );
        }
    }
}

#[test]
fn test_cross_runtime_fixture_fingerprints_exact_match() {
    let fixtures = load_canonical_fixtures().expect("Failed to load canonical fixtures");
    assert_eq!(
        fixtures.schema_version,
        "omega.mub.moment-sdp-ledger-fixtures.v1"
    );
    assert_eq!(fixtures.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(fixtures.firewall, FIREWALL);
    assert_eq!(
        fixtures.fingerprints.len(),
        21,
        "Expected exactly 21 canonical fingerprints"
    );

    // Verify all 21 precomputed fingerprints against live calculation
    let candidates = build_candidate_gramians();
    for &d in SUPPORTED_DEGREES {
        for (c_name, g) in &candidates {
            let m_dict = build_degree_matrices(d, g).expect("build_degree_matrices failed");
            for (m_type, m) in m_dict {
                let key = format!("deg{}_{}_{}", d, m_type, c_name);
                let expected = fixtures.fingerprints.get(&key).unwrap_or_else(|| {
                    panic!("Key '{key}' not found in canonical fixture fingerprints");
                });
                let computed = compute_matrix_fingerprint(&m);
                assert_eq!(
                    &computed, expected,
                    "Fingerprint mismatch for key '{key}': computed {computed} != expected {expected}"
                );
            }
        }
    }

    // Also run unified verifier
    let verified = verify_moment_sdp_ledger_fixtures(&fixtures).expect("Verification failed");
    assert!(verified);

    let canon_verified = verify_canonical_fixtures().expect("Canonical verify failed");
    assert!(canon_verified);
}

#[test]
fn test_evaluate_moment_sdp_hierarchy_ledger_complete_structure() {
    let ledger = evaluate_moment_sdp_hierarchy_ledger().expect("Ledger evaluation failed");

    assert_eq!(ledger.schema_version, SCHEMA_VERSION);
    assert_eq!(ledger.firewall, FIREWALL);
    assert_eq!(ledger.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(ledger.scope, SCOPE_STRING);
    assert_eq!(ledger.degrees, vec![2, 4, 6, 8]);
    assert_eq!(ledger.entries.len(), 4);

    // Schema metadata distinguishing candidate vs global
    assert_eq!(ledger.status, STATUS_MISSING_PROOF_OBLIGATION);
    assert_eq!(
        ledger.candidate_refutation_status,
        STATUS_CERTIFIED_CANDIDATE_REFUTATION
    );
    assert_eq!(ledger.global_search_status, STATUS_MISSING_PROOF_OBLIGATION);

    // Epistemic firewall verification: never claim complete
    assert!(!ledger.complete);
    assert!(ledger.diagnostics_complete);
    assert!(!ledger.moment_semantics_verified);

    // Verify each degree entry is present
    for &d in SUPPORTED_DEGREES {
        let entry = ledger
            .entries
            .get(&d)
            .expect("Missing degree entry in ledger");
        assert_eq!(entry.degree, d);
        assert_eq!(entry.level, d / 2);
        assert_eq!(entry.global_search_status, STATUS_MISSING_PROOF_OBLIGATION);
        if d <= 4 {
            assert_eq!(entry.status, STATUS_CERTIFIED_CANDIDATE_REFUTATION);
            assert_eq!(
                entry.candidate_refutation_status,
                STATUS_CERTIFIED_CANDIDATE_REFUTATION
            );
            assert_eq!(
                entry.x0_receipt.status,
                STATUS_CERTIFIED_CANDIDATE_REFUTATION
            );
            assert_eq!(
                entry.s6_receipt.status,
                STATUS_CERTIFIED_CANDIDATE_REFUTATION
            );
        } else {
            assert_eq!(entry.status, STATUS_MISSING_PROOF_OBLIGATION);
            assert_eq!(
                entry.candidate_refutation_status,
                STATUS_MISSING_PROOF_OBLIGATION
            );
            assert_eq!(entry.x0_receipt.status, STATUS_MISSING_PROOF_OBLIGATION);
            assert_eq!(entry.s6_receipt.status, STATUS_MISSING_PROOF_OBLIGATION);
        }
        assert!(entry.x0_receipt.strictly_negative);
        assert!(entry.s6_receipt.strictly_negative);
        assert!(entry.x0_receipt.pivots_strictly_positive);
        assert!(entry.s6_receipt.pivots_strictly_positive);
    }
}

#[test]
fn test_negative_controls() {
    // 1. Non-symmetric matrix
    let m_asym = vec![
        vec![BigRational::one(), BigRational::from_integer(2.into())],
        vec![BigRational::zero(), BigRational::one()],
    ];
    let res = ldlt_decomposition_rational(&m_asym);
    assert!(res.is_err());
    assert!(res.unwrap_err().contains("not symmetric"));

    // 2. Indefinite matrix
    let m_indef = vec![
        vec![BigRational::one(), BigRational::from_integer(2.into())],
        vec![BigRational::from_integer(2.into()), BigRational::one()],
    ];
    let res = ldlt_pivots_strictly_positive_rational(&m_indef);
    assert!(res.is_err());
    assert!(res.unwrap_err().contains("not strictly positive"));

    // 3. Unsupported degree
    let g = build_candidate_gramians()["x0"].clone();
    assert!(build_degree_matrices(3, &g).is_err());
    assert!(build_degree_matrices(10, &g).is_err());
    assert!(evaluate_degree_benchmark(5, None).is_err());

    // 4. Invalid Gramian dimensions
    let g_bad = vec![vec![Cyc24::zero(); 10]; 10];
    assert!(build_degree_matrices(2, &g_bad).is_err());
}

#[test]
fn test_fail_closed_apis() {
    // solve_target_q5_moment_certificate must fail closed with MissingProofObligation
    let cert_res = solve_target_q5_moment_certificate();
    assert!(cert_res.is_err());
    let err = cert_res.unwrap_err();
    assert!(
        err.starts_with("MissingProofObligation:"),
        "Error must start with MissingProofObligation, got: {err}"
    );

    // solve_target_q5_moment_certificate_for_degree across all degrees must fail closed
    for d in [2, 4, 6, 8] {
        let cert_deg = solve_target_q5_moment_certificate_for_degree(d);
        assert!(cert_deg.is_err());
        let err = cert_deg.unwrap_err();
        assert!(
            err.starts_with("MissingProofObligation:"),
            "Error must start with MissingProofObligation for degree d={d}, got: {err}"
        );
    }

    // claim_universal_mub6_nonexistence must fail closed
    let claim_res = claim_universal_mub6_nonexistence(Some(4));
    assert!(claim_res.is_err());
    assert!(claim_res.unwrap_err().contains("MissingProofObligation"));

    // certify_universal_mub6_nonexistence must fail closed
    let certify_res = certify_universal_mub6_nonexistence(Some(8));
    assert!(certify_res.is_err());
    assert!(certify_res.unwrap_err().contains("MissingProofObligation"));

    // build_degree_k_moment_matrix must fail closed
    let g = build_candidate_gramians()["x0"].clone();
    for k in [2, 4, 6, 8, 10] {
        let mat_res = build_degree_k_moment_matrix(k, &g);
        assert!(mat_res.is_err());
        let err = mat_res.unwrap_err();
        assert!(
            err.starts_with("MissingProofObligation:"),
            "Error must start with MissingProofObligation for degree k={k}, got: {err}"
        );
    }
}

#[test]
fn test_payload_and_fingerprint_deterministic() {
    let m = vec![
        vec![
            BigRational::new(1.into(), 2.into()),
            BigRational::new(3.into(), 4.into()),
        ],
        vec![
            BigRational::new(3.into(), 4.into()),
            BigRational::new(5.into(), 6.into()),
        ],
    ];
    let payload = canonical_matrix_payload(&m);
    assert_eq!(payload, "1/2\n3/4\n3/4\n5/6\n");

    let fp1 = compute_matrix_fingerprint(&m);
    let fp2 = compute_matrix_fingerprint(&m);
    assert_eq!(fp1, fp2);
    assert_eq!(fp1.len(), 64);
}

#[test]
fn test_negative_control_universal_mub6_claim_rejected_across_all_degrees() {
    // Across all degrees (2, 4, 6, 8, etc.), any claim of universal MUB(6) non-existence
    // or operator-algebraic completeness must be rejected fail-closed.
    for deg in [2, 4, 6, 8, 10, 12] {
        let res = claim_universal_mub6_nonexistence(Some(deg));
        assert!(res.is_err());
        let err = res.unwrap_err();
        assert!(
            err.contains("MissingProofObligation"),
            "Degree {deg} claim_universal_mub6_nonexistence did not reject fail-closed: {err}"
        );
        assert!(
            err.contains("mints no authority"),
            "Degree {deg} rejection did not cite firewall: {err}"
        );

        let cert_deg = solve_target_q5_moment_certificate_for_degree(deg);
        assert!(cert_deg.is_err());
        let err_cert = cert_deg.unwrap_err();
        assert!(
            err_cert.contains("MissingProofObligation"),
            "Degree {deg} solve_target_q5_moment_certificate_for_degree did not reject fail-closed: {err_cert}"
        );
    }

    let global_cert = certify_universal_mub6_nonexistence(None);
    assert!(global_cert.is_err());
    let err_global = global_cert.unwrap_err();
    assert!(err_global.contains("MissingProofObligation"));
}

#[test]
fn test_negative_control_schema_metadata_distinguishes_candidate_vs_global() {
    let ledger = evaluate_moment_sdp_hierarchy_ledger().expect("Ledger evaluation failed");

    // The ledger itself must NOT have status CERTIFIED_CANDIDATE_REFUTATION for global search
    assert_eq!(
        ledger.status, STATUS_MISSING_PROOF_OBLIGATION,
        "Ledger global status must be MISSING_PROOF_OBLIGATION"
    );
    assert_eq!(
        ledger.global_search_status, STATUS_MISSING_PROOF_OBLIGATION,
        "Ledger global_search_status must be MISSING_PROOF_OBLIGATION"
    );
    assert_eq!(
        ledger.candidate_refutation_status, STATUS_CERTIFIED_CANDIDATE_REFUTATION,
        "Ledger candidate_refutation_status must be CERTIFIED_CANDIDATE_REFUTATION"
    );

    // Degrees 2 and 4 have certified candidate refutations for fixed matrices, but global search remains missing proof obligation
    for deg in [2, 4] {
        let entry = ledger.entries.get(&deg).unwrap();
        assert_eq!(
            entry.status, STATUS_CERTIFIED_CANDIDATE_REFUTATION,
            "Degree {deg} candidate entry status must be CERTIFIED_CANDIDATE_REFUTATION"
        );
        assert_eq!(
            entry.candidate_refutation_status, STATUS_CERTIFIED_CANDIDATE_REFUTATION,
            "Degree {deg} candidate_refutation_status must be CERTIFIED_CANDIDATE_REFUTATION"
        );
        assert_eq!(
            entry.global_search_status, STATUS_MISSING_PROOF_OBLIGATION,
            "Degree {deg} global_search_status must be MISSING_PROOF_OBLIGATION"
        );
        assert_eq!(
            entry.x0_receipt.status, STATUS_CERTIFIED_CANDIDATE_REFUTATION,
            "Degree {deg} x0_receipt status must be CERTIFIED_CANDIDATE_REFUTATION"
        );
        assert_eq!(
            entry.s6_receipt.status, STATUS_CERTIFIED_CANDIDATE_REFUTATION,
            "Degree {deg} s6_receipt status must be CERTIFIED_CANDIDATE_REFUTATION"
        );
    }

    // Degrees 6 and 8 remain missing proof obligation
    for deg in [6, 8] {
        let entry = ledger.entries.get(&deg).unwrap();
        assert_eq!(
            entry.status, STATUS_MISSING_PROOF_OBLIGATION,
            "Degree {deg} entry status must be MISSING_PROOF_OBLIGATION"
        );
        assert_eq!(
            entry.candidate_refutation_status, STATUS_MISSING_PROOF_OBLIGATION,
            "Degree {deg} candidate_refutation_status must be MISSING_PROOF_OBLIGATION"
        );
        assert_eq!(
            entry.global_search_status, STATUS_MISSING_PROOF_OBLIGATION,
            "Degree {deg} global_search_status must be MISSING_PROOF_OBLIGATION"
        );
        assert_eq!(
            entry.x0_receipt.status, STATUS_MISSING_PROOF_OBLIGATION,
            "Degree {deg} x0_receipt status must be MISSING_PROOF_OBLIGATION"
        );
        assert_eq!(
            entry.s6_receipt.status, STATUS_MISSING_PROOF_OBLIGATION,
            "Degree {deg} s6_receipt status must be MISSING_PROOF_OBLIGATION"
        );
    }
}

#[test]
fn test_flat_extension_rank_gap_certification() {
    let receipt =
        certify_flat_extension_rank_gap(1).expect("Level 1 flat extension certification failed");
    assert_eq!(receipt.level, 1);
    assert_eq!(receipt.rank_d, 21);
    assert_eq!(receipt.rank_d_minus_1, 1);
    assert_eq!(receipt.rank_gap, 20);
    assert!(receipt.is_obstructed);
    assert_eq!(receipt.status, "FLAT_EXTENSION_OBSTRUCTED");
    assert_eq!(receipt.firewall, FIREWALL);
    assert_eq!(receipt.authority_effect, AUTHORITY_EFFECT);

    // Negative control: unsupported level must return error
    let err = certify_flat_extension_rank_gap(2);
    assert!(err.is_err());
    assert!(err
        .unwrap_err()
        .contains("Exact flat extension certified only for level 1"));
}
