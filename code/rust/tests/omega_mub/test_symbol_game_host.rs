//! Integration Tests for Symbol Game Minimal Host & Three-Layer Verification.
//!
//! Epistemic Firewall:
//! AuthorityEffect: None.

use omega_mub::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_symbol_game_runtime::symbol_game_host::{
    build_mub6_det_cycle, HostMoveOp, HostRefusalCode, SymbolGameHost, UntrustedProposal,
};
use omega_number_theory::rational::ri;

#[test]
fn test_symbol_game_firewall_and_authority() {
    let host_source = include_str!("../../omega_symbol_game_runtime/src/symbol_game_host.rs");
    assert!(
        host_source.contains(&format!("Firewall: {FIREWALL}")),
        "symbol_game_host must declare the shared firewall line"
    );
    assert_eq!(AUTHORITY_EFFECT, "None");
    assert!(FIREWALL.contains("stated region only"));
    assert!(!FIREWALL.contains("NOT MUB(6)=3"));
}

#[test]
fn test_immutable_problem_digest_pinning() {
    let problem = build_mub6_det_cycle(ri(1), ri(1), ri(1), ri(1));
    let mut host = SymbolGameHost::new(problem);

    let proposal = UntrustedProposal {
        proposer_id: "untrusted_agent".to_string(),
        problem_digest: "0000000000000000000000000000000000000000000000000000000000000000"
            .to_string(),
        parent_state_digest: host.current_state_digest.clone(),
        op: HostMoveOp::Cut,
        proposed_section: Some(vec![ri(0), ri(0), ri(0)]),
        dual_witness: None,
        target_property: None,
        target_event_id: None,
        claimed_post_state_digest: "fake".to_string(),
        claimed_defect: None,
        rationale: "Tampered problem digest test".to_string(),
    };

    let verdict = host.process_proposal(&proposal);
    assert!(!verdict.admitted);
    assert!(matches!(
        verdict.refusal_code,
        Some(HostRefusalCode::ProblemDigestMismatch { .. })
    ));
}

#[test]
fn test_parent_state_digest_stale_rejection() {
    let problem = build_mub6_det_cycle(ri(1), ri(1), ri(1), ri(1));
    let mut host = SymbolGameHost::new(problem);

    let proposal = UntrustedProposal {
        proposer_id: "untrusted_agent".to_string(),
        problem_digest: host.problem.digest.clone(),
        parent_state_digest: "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            .to_string(),
        op: HostMoveOp::Cut,
        proposed_section: Some(vec![ri(0), ri(0), ri(0)]),
        dual_witness: None,
        target_property: None,
        target_event_id: None,
        claimed_post_state_digest: "fake".to_string(),
        claimed_defect: None,
        rationale: "Stale parent test".to_string(),
    };

    let verdict = host.process_proposal(&proposal);
    assert!(!verdict.admitted);
    assert!(matches!(
        verdict.refusal_code,
        Some(HostRefusalCode::ParentStateMismatch { .. })
    ));
}

#[test]
fn test_fail_closed_on_defect_increase() {
    // Problem with det = 0: a=1, b=1, c=1, d=1
    // Initial section 0 has defect 0.
    // Proposing section [10, 0, 0] increases defect to 20!
    let problem = build_mub6_det_cycle(ri(1), ri(1), ri(1), ri(1));
    let mut host = SymbolGameHost::new(problem);

    let proposal = UntrustedProposal {
        proposer_id: "untrusted_agent".to_string(),
        problem_digest: host.problem.digest.clone(),
        parent_state_digest: host.current_state_digest.clone(),
        op: HostMoveOp::Cut,
        proposed_section: Some(vec![ri(10), ri(0), ri(0)]),
        dual_witness: None,
        target_property: None,
        target_event_id: None,
        claimed_post_state_digest: "fake".to_string(),
        claimed_defect: None,
        rationale: "Non-monotonic cut test".to_string(),
    };

    let verdict = host.process_proposal(&proposal);
    assert!(!verdict.admitted);
    assert!(matches!(
        verdict.refusal_code,
        Some(HostRefusalCode::DefectIncrease { .. })
    ));
}

#[test]
fn test_fail_closed_on_forged_post_state_digest() {
    // Problem with a=2, b=1, c=1, d=2 -> prod_diff = 3, lin_corr = 2, det = 1
    // Initial defect at section 0 is |3| + |-2| + |0| = 5.
    // Valid cut to section [0, 3, 1] gives defect: |3-3| + |-2-(-2)| + |0-(-1)| = 1 < 5.
    let problem = build_mub6_det_cycle(ri(2), ri(1), ri(1), ri(2));
    let mut host = SymbolGameHost::new(problem);

    let forged_hash =
        "1111222233334444555566667777888899990000aaaabbbbccccddddeeeeffff".to_string();
    let proposal = UntrustedProposal {
        proposer_id: "untrusted_agent".to_string(),
        problem_digest: host.problem.digest.clone(),
        parent_state_digest: host.current_state_digest.clone(),
        op: HostMoveOp::Cut,
        proposed_section: Some(vec![ri(0), ri(3), ri(1)]),
        dual_witness: None,
        target_property: None,
        target_event_id: None,
        claimed_post_state_digest: forged_hash,
        claimed_defect: None,
        rationale: "Forged post state hash test".to_string(),
    };

    let verdict = host.process_proposal(&proposal);
    assert!(!verdict.admitted);
    assert!(matches!(
        verdict.refusal_code,
        Some(HostRefusalCode::PostStateDigestMismatch { .. })
    ));
}

#[test]
fn test_valid_cut_monotonic_descent_and_event_logging() {
    let problem = build_mub6_det_cycle(ri(2), ri(1), ri(1), ri(2));
    let mut host = SymbolGameHost::new(problem.clone());

    let candidate_sec = vec![ri(0), ri(3), ri(1)];
    let defect_after = SymbolGameHost::compute_defect(&problem, &candidate_sec);
    assert_eq!(defect_after, ri(1));

    let expected_post_digest = SymbolGameHost::calculate_state_digest(
        &problem.digest,
        &host.current_state_digest,
        1,
        &candidate_sec,
        &defect_after,
    );

    let proposal = UntrustedProposal {
        proposer_id: "honest_proposer".to_string(),
        problem_digest: problem.digest.clone(),
        parent_state_digest: host.current_state_digest.clone(),
        op: HostMoveOp::Cut,
        proposed_section: Some(candidate_sec.clone()),
        dual_witness: None,
        target_property: None,
        target_event_id: None,
        claimed_post_state_digest: expected_post_digest.clone(),
        claimed_defect: Some(defect_after.clone()),
        rationale: "Valid cut to optimal potential".to_string(),
    };

    let verdict = host.process_proposal(&proposal);
    assert!(verdict.admitted);
    assert_eq!(
        verdict.post_state_digest.as_ref(),
        Some(&expected_post_digest)
    );
    assert_eq!(verdict.verified_defect, Some(ri(1)));
    assert_eq!(host.current_state_digest, expected_post_digest);
    assert_eq!(host.history.len(), 1);

    let ev = &host.history[0];
    assert_eq!(ev.op, HostMoveOp::Cut);
    assert_eq!(ev.verified_defect, ri(1));
}

#[test]
fn test_dual_witness_certification_and_fail_closed_rejections() {
    let problem = build_mub6_det_cycle(ri(2), ri(1), ri(1), ri(2));
    let mut host = SymbolGameHost::new(problem.clone());

    // Cut to optimal potential [0, 3, 1]
    let sec = vec![ri(0), ri(3), ri(1)];
    let defect = SymbolGameHost::compute_defect(&problem, &sec);
    assert_eq!(defect, ri(1));
    host.section = sec.clone();
    host.current_state_digest = SymbolGameHost::calculate_state_digest(
        &problem.digest,
        &host.current_state_digest.clone(),
        1,
        &sec,
        &defect,
    );

    // 1. Dual not perpendicular: z = [1, 0, 0] violates node divergence
    let dual_non_perp = vec![ri(1), ri(0), ri(0)];
    let res_perp = host.verify_dual_witness(&dual_non_perp, &host.section);
    assert!(matches!(
        res_perp,
        Err(HostRefusalCode::DualNotPerpendicular { .. })
    ));

    // 2. Dual exceeds weight: z = [2, 2, 2] exceeds weight 1
    let dual_overweight = vec![ri(2), ri(2), ri(2)];
    let res_weight = host.verify_dual_witness(&dual_overweight, &host.section);
    assert!(matches!(
        res_weight,
        Err(HostRefusalCode::DualExceedsWeight { .. })
    ));

    // 3. Duality gap detected: z = [0, 0, 0] gives pairing 0 != defect 1
    let dual_gap = vec![ri(0), ri(0), ri(0)];
    let res_gap = host.verify_dual_witness(&dual_gap, &host.section);
    assert!(matches!(
        res_gap,
        Err(HostRefusalCode::DualityGapDetected { .. })
    ));

    // 4. Exact dual witness: z = [1, 1, 1] satisfies B^T z = 0, |z_e| <= 1, and <z, r> = 1*0 + 1*0 + 1*1 = 1 == defect!
    let dual_valid = vec![ri(1), ri(1), ri(1)];
    let res_valid = host.verify_dual_witness(&dual_valid, &host.section);
    assert!(res_valid.is_ok());
}

#[test]
fn test_unlicensed_problem_mutation_rejected() {
    let problem = build_mub6_det_cycle(ri(1), ri(1), ri(1), ri(1));
    let mut host = SymbolGameHost::new(problem);

    let proposal = UntrustedProposal {
        proposer_id: "adversary".to_string(),
        problem_digest: host.problem.digest.clone(),
        parent_state_digest: host.current_state_digest.clone(),
        op: HostMoveOp::Assert,
        proposed_section: None,
        dual_witness: None,
        target_property: None,
        target_event_id: None,
        claimed_post_state_digest: "fake".to_string(),
        claimed_defect: None,
        rationale: "Unlicensed assert".to_string(),
    };

    let verdict = host.process_proposal(&proposal);
    assert!(!verdict.admitted);
    assert!(matches!(
        verdict.refusal_code,
        Some(HostRefusalCode::UnlicensedProblemMutation)
    ));
}

#[test]
fn test_retract_restores_exact_previous_state() {
    let problem = build_mub6_det_cycle(ri(2), ri(1), ri(1), ri(2));
    let mut host = SymbolGameHost::new(problem.clone());
    let initial_digest = host.current_state_digest.clone();

    // Perform valid cut
    let candidate_sec = vec![ri(0), ri(3), ri(1)];
    let defect_after = SymbolGameHost::compute_defect(&problem, &candidate_sec);
    let post_digest = SymbolGameHost::calculate_state_digest(
        &problem.digest,
        &initial_digest,
        1,
        &candidate_sec,
        &defect_after,
    );

    let proposal_cut = UntrustedProposal {
        proposer_id: "p1".to_string(),
        problem_digest: problem.digest.clone(),
        parent_state_digest: initial_digest.clone(),
        op: HostMoveOp::Cut,
        proposed_section: Some(candidate_sec),
        dual_witness: None,
        target_property: None,
        target_event_id: None,
        claimed_post_state_digest: post_digest,
        claimed_defect: Some(defect_after),
        rationale: "First cut".to_string(),
    };
    let v_cut = host.process_proposal(&proposal_cut);
    assert!(v_cut.admitted);
    let event_id = v_cut.event_id.unwrap();

    // Restoration is a new checked event; prior evidence remains in the ledger.
    let restored = vec![ri(0), ri(0), ri(0)];
    let restored_defect = SymbolGameHost::compute_defect(&problem, &restored);
    let retract_digest = SymbolGameHost::calculate_state_digest(
        &problem.digest,
        &host.current_state_digest,
        2,
        &restored,
        &restored_defect,
    );
    let proposal_retract = UntrustedProposal {
        proposer_id: "p1".to_string(),
        problem_digest: problem.digest.clone(),
        parent_state_digest: host.current_state_digest.clone(),
        op: HostMoveOp::Retract,
        proposed_section: None,
        dual_witness: None,
        target_property: None,
        target_event_id: Some(event_id),
        claimed_post_state_digest: retract_digest.clone(),
        claimed_defect: None,
        rationale: "Retract step 1".to_string(),
    };

    let mut forged = proposal_retract.clone();
    forged.claimed_post_state_digest = "forged".into();
    assert!(!host.process_proposal(&forged).admitted);
    assert_eq!(host.step_counter, 1);
    assert_eq!(host.history.len(), 1);
    let v_retract = host.process_proposal(&proposal_retract);
    assert!(v_retract.admitted);
    assert_eq!(host.current_state_digest, retract_digest);
    assert_eq!(host.section, vec![ri(0), ri(0), ri(0)]);
    assert_eq!(host.history.len(), 2);
    assert_eq!(host.history[1].op, HostMoveOp::Retract);
}

#[test]
fn problem_digest_separates_delimiters_in_vertex_names() {
    use omega_symbol_game_runtime::symbol_game_host::SymbolGameProblem;
    let a =
        SymbolGameProblem::new("p".into(), vec!["a,b".into(), "c".into()], vec![], vec![]).unwrap();
    let b =
        SymbolGameProblem::new("p".into(), vec!["a".into(), "b,c".into()], vec![], vec![]).unwrap();
    assert_ne!(a.digest, b.digest);
}

#[test]
fn duplicate_vertices_are_rejected() {
    use omega_symbol_game_runtime::symbol_game_host::SymbolGameProblem;
    assert!(
        SymbolGameProblem::new("p".into(), vec!["a".into(), "a".into()], vec![], vec![]).is_err()
    );
}

#[test]
fn test_bootstrap_rejects_tampered_problem_digest() {
    let mut problem = build_mub6_det_cycle(ri(1), ri(1), ri(1), ri(1));
    problem.digest = "0000000000000000000000000000000000000000000000000000000000000000".to_string();

    let try_res = SymbolGameHost::try_new(problem.clone());
    assert!(try_res.is_err());
    assert!(matches!(
        try_res.err(),
        Some(HostRefusalCode::ProblemDigestMismatch { .. })
    ));

    // Assert that new() panics fail-closed on tampered problem digest
    let panic_res = std::panic::catch_unwind(|| {
        SymbolGameHost::new(problem);
    });
    assert!(panic_res.is_err());
}

#[test]
fn test_verified_event_contains_valid_event_digest() {
    let problem = build_mub6_det_cycle(ri(1), ri(1), ri(1), ri(1));
    let mut host = SymbolGameHost::new(problem.clone());

    let proposal = UntrustedProposal {
        proposer_id: "agent".to_string(),
        problem_digest: host.problem.digest.clone(),
        parent_state_digest: host.current_state_digest.clone(),
        op: HostMoveOp::Verify,
        proposed_section: None,
        dual_witness: None,
        target_property: Some("ZERO_OBSTRUCTION".to_string()),
        target_event_id: None,
        claimed_post_state_digest: SymbolGameHost::calculate_state_digest(
            &problem.digest,
            &host.current_state_digest,
            1,
            &host.section,
            &ri(0),
        ),
        claimed_defect: Some(ri(0)),
        rationale: "Verify zero obstruction".to_string(),
    };

    let verdict = host.process_proposal(&proposal);
    assert!(verdict.admitted);
    assert_eq!(host.history.len(), 1);

    let ev = &host.history[0];
    assert!(!ev.event_digest.is_empty());
    assert_eq!(ev.event_digest.len(), 64);

    let recomputed_ev_digest = omega_symbol_game_runtime::symbol_game_host::VerifiedEvent::calculate_event_digest(
        &ev.event_id,
        ev.parent_event_id.as_deref(),
        &ev.problem_digest,
        &ev.parent_state_digest,
        &ev.post_state_digest,
        ev.op,
        &ev.verified_defect,
    );
    assert_eq!(ev.event_digest, recomputed_ev_digest);
}
