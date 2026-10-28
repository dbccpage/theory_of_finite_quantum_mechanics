//! Integration tests for Szöllősi B6 and Tao S6 MU Triad Compatibility Solver.
//!
//! AuthorityEffect: None

use tfqm_mub::native::exact::d6_exact_curvature_cochain::D;
use tfqm_mub::native::exact::szollosi_triad_solver::{
    check_hadamard_transition, emit_receipt_files, execute_szollosi_triad_search,
    search_discrete_szollosi_chm_points, szollosi_dephased_b6, tao_s6_matrix, verify_chm,
};
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::ri;

#[test]
fn test_tao_s6_exact_hadamard_properties() {
    let s6 = tao_s6_matrix();
    let rep = verify_chm(&s6);
    assert!(
        rep.is_chm,
        "Tao S6 must be an exact complex Hadamard matrix"
    );
    assert!(rep.all_entries_unit_modulus);
    assert!(rep.is_orthogonal);
    assert_eq!(rep.diagonal_norm_sq, "6");
    assert_eq!(rep.max_offdiagonal_norm_sq, "0");

    // Check dephased form: row 0 and col 0 are all 1
    let one = Cyc24::rat(ri(1));
    for k in 0..D {
        assert_eq!(s6[0][k], one);
        assert_eq!(s6[k][0], one);
    }

    // Check symmetry S6[j][k] == S6[k][j]
    for j in 0..D {
        for k in 0..D {
            assert_eq!(s6[j][k], s6[k][j]);
        }
    }
}

#[test]
fn test_szollosi_deltoid_condition_exact() {
    let points = search_discrete_szollosi_chm_points();
    assert!(
        !points.is_empty(),
        "Discrete parameter search must find valid CHM points"
    );

    // Take the first 5 discovered discrete points and verify each builds an exact CHM
    for pt in points.iter().take(5) {
        let b = Cyc24::zeta24(pt.kb as i32);
        let c = Cyc24::zeta24(pt.kc as i32);
        let e = Cyc24::zeta24(pt.ke as i32);
        let f = Cyc24::zeta24(pt.kf as i32);

        let res = szollosi_dephased_b6(&b, &c, &e, &f);
        assert!(
            res.is_ok(),
            "Point ({},{},{},{}) must construct B6",
            pt.kb,
            pt.kc,
            pt.ke,
            pt.kf
        );
        let b6 = res.unwrap();

        let chm_report = verify_chm(&b6);
        assert!(
            chm_report.is_chm,
            "Point ({},{},{},{}) must be exact CHM: {:?}",
            pt.kb, pt.kc, pt.ke, pt.kf, chm_report
        );
    }
}

#[test]
fn test_hadamard_transition_evaluates_exact_obstruction() {
    let s6 = tao_s6_matrix();
    let points = search_discrete_szollosi_chm_points();
    assert!(!points.is_empty());

    let pt = &points[0];
    let b = Cyc24::zeta24(pt.kb as i32);
    let c = Cyc24::zeta24(pt.kc as i32);
    let e = Cyc24::zeta24(pt.ke as i32);
    let f = Cyc24::zeta24(pt.kf as i32);
    let b6 = szollosi_dephased_b6(&b, &c, &e, &f).unwrap();

    let tr = check_hadamard_transition(&s6, &b6);
    // Neither pair is mutually unbiased (obstruction observed)
    assert!(!tr.is_mutually_unbiased);
    assert!(tr.violation_count > 0);
    assert_ne!(tr.min_entry_mod_sq_rat, "6/1");
}

#[test]
fn test_szollosi_triad_search_receipt_conformance() {
    let receipt = execute_szollosi_triad_search();
    assert_eq!(receipt.schema_version, "omega.mub.szollosi-triad-search.v1");
    assert_eq!(receipt.authority_effect, "None");
    assert!(receipt.firewall.contains("stated region only"));
    assert_eq!(
        receipt.terminal_status,
        "VerifiedTriadNonExistenceInDiscreteLoci"
    );

    assert!(receipt.valid_szollosi_discrete_chm_count > 0);
    assert_eq!(receipt.tao_vs_tao_permutations_tested, 21);
    assert_eq!(receipt.tao_vs_tao_mu_triads_found, 0);
    assert_eq!(receipt.tao_vs_szollosi_mu_triads_found, 0);
    assert_eq!(receipt.szollosi_vs_szollosi_mu_triads_found, 0);

    let paths = emit_receipt_files(&receipt).expect("Receipt files must be emitted");
    for p in paths {
        assert!(p.exists());
        let content = std::fs::read_to_string(&p).unwrap();
        assert!(content.contains("omega.mub.szollosi-triad-search.v1"));
        assert!(content.contains("stated region only"));
    }
}
