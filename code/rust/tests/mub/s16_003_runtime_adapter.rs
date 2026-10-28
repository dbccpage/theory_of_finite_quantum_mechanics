use omega_contracts::mub_domain_ownership::{
    validate_mub_ownership_contract_v1, CANONICAL_MUB_DOMAIN_OWNER_V1,
};
use tfqm_mub::runtime_adapter::{
    evaluate_mub6_json, evaluate_mub6_request, Mub6RuntimeEvidenceV1, Mub6RuntimeRequestV1,
};
use omega_policy::trichotomy::ObstructionDiagnosticClass;
use omega_state::CodaTerminal;

fn exact_request(cover_discharged: bool) -> Mub6RuntimeRequestV1 {
    Mub6RuntimeRequestV1 {
        evidence: Mub6RuntimeEvidenceV1::FixedT0 { cover_discharged },
    }
}

#[test]
fn ownership_contract_selects_omega_mub() {
    validate_mub_ownership_contract_v1().unwrap();
    assert_eq!(CANONICAL_MUB_DOMAIN_OWNER_V1, "omega_mub");
}

#[test]
fn fixed_t0_without_cover_is_an_exact_closed_survivor() {
    let result = evaluate_mub6_request(exact_request(false)).unwrap();
    assert_eq!(result.terminal(), CodaTerminal::StabilizedSurvivor);
    assert_eq!(
        result.evaluation().status(),
        ObstructionDiagnosticClass::ClosedResidual
    );
    assert!(!result.cover_discharged());
    assert!(result.authority_effect().is_none());
    assert_eq!(result.tuple_hash().len(), 64);
    assert_eq!(result.replay_hash().len(), 64);
}

#[test]
fn exact_complete_cover_routes_exact_repair() {
    let result = evaluate_mub6_request(exact_request(true)).unwrap();
    assert_eq!(result.terminal(), CodaTerminal::ExactRepair);
    assert_eq!(
        result.evaluation().status(),
        ObstructionDiagnosticClass::ExactRepair
    );
    assert!(result.cover_discharged());
    assert!(result.authority_effect().is_none());
}

#[test]
fn exact_replay_hashes_are_deterministic() {
    let first = evaluate_mub6_request(exact_request(false)).unwrap();
    let second = evaluate_mub6_request(exact_request(false)).unwrap();
    assert_eq!(first.tuple_hash(), second.tuple_hash());
    assert_eq!(first.replay_hash(), second.replay_hash());
}

#[test]
fn floating_diagnostics_are_refused_before_exact_replay() {
    let error = evaluate_mub6_request(Mub6RuntimeRequestV1 {
        evidence: Mub6RuntimeEvidenceV1::FloatingDiagnostic { objective: 0.99 },
    })
    .unwrap_err();
    assert_eq!(error.terminal(), CodaTerminal::Refused);
}

#[test]
fn malformed_json_is_refused() {
    let error = evaluate_mub6_json(br#"{"evidence":{"kind":"fixed_t0"}}"#).unwrap_err();
    assert_eq!(error.terminal(), CodaTerminal::Refused);
}
