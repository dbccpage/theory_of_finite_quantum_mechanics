//! Integration tests for MSS-N Obstruction Detector, Active Demand Pressure, and the Two Boxed Laws.
//!
//! AuthorityEffect: None. GenesisEffect: None.

use mssn_stage_024::obstruction_detector::{
    audit_layer_1_topological_chasm, audit_layer_2_circulation_flux,
    audit_layer_3_curvature_deficit, audit_layer_4_epistemic_fence,
    evaluate_two_boxed_laws_gate, CandidateLift, EpistemicContinuumFence,
    ObstructionError, ObstructionState,
};
use std::collections::BTreeSet;

#[test]
fn test_four_gate_factorization_identity() {
    let mut state = ObstructionState::new();
    state.wit.insert((0, 1));
    state.prot.insert((0, 1));
    let mut col0 = BTreeSet::new();
    col0.insert(0);
    col0.insert(1);
    state.obs = Some(vec![col0]);

    // Active obstruction exists: retained, protected, declared, and not separated
    assert!(state.obst_p(0, 1));
    assert!(state.verify_four_gate_factorization(0, 1));

    // Undeclared observation state: obst_p is false, zero_decl_p is vacuously true
    let mut undeclared = state.clone();
    undeclared.obs = None;
    assert!(!undeclared.obst_p(0, 1));
    assert!(undeclared.verify_four_gate_factorization(0, 1));

    // Separated observation: obst_p is false
    let mut separated = state.clone();
    let mut col_a = BTreeSet::new();
    col_a.insert(0);
    let mut col_b = BTreeSet::new();
    col_b.insert(1);
    separated.obs = Some(vec![col_a, col_b]);
    assert!(!separated.obst_p(0, 1));
    assert!(separated.verify_four_gate_factorization(0, 1));
}

#[test]
fn test_layer_1_topological_chasm_0d() {
    let mut state = ObstructionState::new();
    state.wit.insert((0, 1));
    state.prot.insert((0, 1));
    let mut col = BTreeSet::new();
    col.insert(0);
    col.insert(1);
    state.obs = Some(vec![col]);

    // Level 02: 0-dimensional topological chasm detected between distinct points 0 and 1
    let is_chasm = audit_layer_1_topological_chasm(&state, 0, 1).expect("Audit should pass");
    assert!(is_chasm, "Non-separated distinct points must trigger 0D chasm obstruction");

    // Identical points have no chasm
    let self_chasm = audit_layer_1_topological_chasm(&state, 0, 0).expect("Audit should pass");
    assert!(!self_chasm, "Identical points cannot have a topological chasm");
}

#[test]
fn test_layer_2_circulation_flux_and_potential_obstruction() {
    // Triangle cycle a -> b -> c -> a
    // Edge vector x = (1, 0, 0)
    let circ = audit_layer_2_circulation_flux(1, 0, 0).expect("Circulation audit should succeed");
    assert_eq!(circ, 1, "Circulation functional I(x) on unit flux loop must equal 1");

    // Any exact coboundary x = d0 g has vanishing circulation
    // Let g = (g_a=5, g_b=12, g_c=7)
    // x_ab = 12 - 5 = 7
    // x_bc = 7 - 12 = -5
    // x_ca = 5 - 7 = -2
    let coboundary_circ = audit_layer_2_circulation_flux(7, -5, -2).expect("Coboundary audit");
    assert_eq!(
        coboundary_circ, 0,
        "Circulation on exact coboundary d0 g must identically vanish"
    );
}

#[test]
fn test_layer_3_curvature_deficit_obstruction() {
    // Deficit angle != 0 indicates curvature obstruction (hinge / plaquette)
    let is_curved = audit_layer_3_curvature_deficit(1, 4).expect("Curvature audit");
    assert!(is_curved, "Non-zero deficit angle must indicate curvature obstruction");

    let is_flat = audit_layer_3_curvature_deficit(0, 1).expect("Curvature audit");
    assert!(!is_flat, "Zero deficit angle indicates flat trivial connection");
}

#[test]
fn test_layer_4_epistemic_continuum_fences() {
    // Compliant discrete lattice
    let res = audit_layer_4_epistemic_fence(false, false).expect("Discrete lattice is admitted");
    assert_eq!(res, EpistemicContinuumFence::DiscreteLatticeAdmitted);

    // Epistemic firewall blocks unearned continuous real parameters
    let err_smooth = audit_layer_4_epistemic_fence(true, false);
    match err_smooth {
        Err(ObstructionError::ErrEpistemicContinuumFence(msg)) => {
            assert!(msg.contains("Epistemic Firewall: Discrete simplicial complex"));
        }
        _ => panic!("Expected ErrEpistemicContinuumFence on smooth manifold claim"),
    }

    let err_uncountable = audit_layer_4_epistemic_fence(false, true);
    match err_uncountable {
        Err(ObstructionError::ErrEpistemicContinuumFence(msg)) => {
            assert!(msg.contains("Epistemic Firewall: Discrete rational lattice"));
        }
        _ => panic!("Expected ErrEpistemicContinuumFence on uncountable continuum claim"),
    }
}

#[test]
fn test_two_boxed_laws_gate_zero_demand_refuses_lift() {
    // Empty state with no active obstructions (W_n^active = 0)
    let state = ObstructionState::new();
    let domain = vec![(0, 1), (1, 2), (2, 0)];

    let candidate = CandidateLift {
        from_stage: 1,
        to_stage: 2,
        targeted_obstructions: vec![(0, 1)],
        adjoined_structure_description: "Adjoin directed edge verb".to_string(),
        unforced_structure_flag: false,
        verified_retraction: true,
    };

    // Law 1: S(n+1) may contain only structure forced by an unresolved Genesis obstruction at S(n)
    let result = evaluate_two_boxed_laws_gate(&state, &candidate, &domain);
    match result {
        Err(ObstructionError::ErrZeroObstructionDemand(msg)) => {
            assert!(msg.contains("zero active obstruction pressure"));
        }
        _ => panic!("Expected ErrZeroObstructionDemand when W_n^active = 0"),
    }
}

#[test]
fn test_two_boxed_laws_gate_unforced_structure_refusal() {
    // State with active obstruction at (0, 1)
    let mut state = ObstructionState::new();
    state.wit.insert((0, 1));
    state.prot.insert((0, 1));
    let mut col = BTreeSet::new();
    col.insert(0);
    col.insert(1);
    state.obs = Some(vec![col]);
    let domain = vec![(0, 1)];

    // Candidate lift introduces unforced structure (violating Law 2)
    let candidate_unforced = CandidateLift {
        from_stage: 1,
        to_stage: 2,
        targeted_obstructions: vec![(0, 1)],
        adjoined_structure_description: "Adjoin continuous metric tensor without obstruction forcing".to_string(),
        unforced_structure_flag: true,
        verified_retraction: true,
    };

    let result = evaluate_two_boxed_laws_gate(&state, &candidate_unforced, &domain);
    match result {
        Err(ObstructionError::ErrUnforcedStructure(msg)) => {
            assert!(msg.contains("unforced structure"));
        }
        _ => panic!("Expected ErrUnforcedStructure by Law 2"),
    }
}

#[test]
fn test_two_boxed_laws_gate_valid_forced_lift_passes() {
    // State with active obstruction at (0, 1)
    let mut state = ObstructionState::new();
    state.wit.insert((0, 1));
    state.prot.insert((0, 1));
    let mut col = BTreeSet::new();
    col.insert(0);
    col.insert(1);
    state.obs = Some(vec![col]);
    let domain = vec![(0, 1)];

    let candidate_valid = CandidateLift {
        from_stage: 1,
        to_stage: 2,
        targeted_obstructions: vec![(0, 1)],
        adjoined_structure_description: "Adjoin directed relation bridge < to resolve 0D chasm".to_string(),
        unforced_structure_flag: false,
        verified_retraction: true,
    };

    let receipt = evaluate_two_boxed_laws_gate(&state, &candidate_valid, &domain)
        .expect("Valid forced lift must pass gate");
    assert_eq!(receipt.status, "PASS");
    assert_eq!(receipt.active_demand_pressure, 1);
    assert_eq!(receipt.resolved_obstructions, 1);
    assert!(receipt.retraction_verified);
}
