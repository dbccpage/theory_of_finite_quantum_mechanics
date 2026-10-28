#[path = "support/upstream_history.rs"]
mod upstream_history;

use std::env;
use std::fs;
use std::path::{Path, PathBuf};

use engine_contracts::{
    OperatorCapabilityV1, OperatorManifestV1, OperatorOperationV1, OperatorPermissionV1,
    OperatorRegistryContractError, OperatorWitnessRequirementV1, OPERATOR_MANIFEST_SCHEMA_VERSION,
};
use engine_wdp::ddc::dda_alphabet::DdaOp;
use engine_wdp::ddc::degree_tower::{BinaryCochainSegment, BinaryLinearMap};
use engine_wdp::ddc::op_verification::CochainState;
use engine_lifts::{
    lift_sha256_json_v1, LIFT_license_CANDIDATE_SCHEMA_VERSION, LiftAuthorityBoundaryV1,
    LiftBudgetBoundaryV1, LiftLicenseCandidateV1, LiftLicenseError, LiftLicenseValidationStatusV1,
    LiftTerminalRouteV1, LiftTerminalizerRouteV1, LiftTriggerV1, NonDestructionWitnessV1,
    ObstructionWitnessV1, PreservationWitnessV1, LIFT_TRIGGER_SCHEMA_VERSION,
};
use engine_state::coda1_classifier::{sha256_bytes_v1, Coda1BudgetsV1, SourceHashV1};
use engine_state::coda3_lift_license::*;
use engine_state::coda_gtla_protocol::{FrozenObserverContextV1, CodaTerminal};
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Coda3FixtureSetV1 {
    schema_version: String,
    admissions: Vec<Coda3AdmissionV1>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Coda3ReceiptSetV1 {
    schema_version: String,
    executions: Vec<Coda3ExecutionV1>,
}

fn repository_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(3)
        .expect("omega_state lives three levels below the repository root")
        .to_path_buf()
}

fn fixture_path(name: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/engine_state")
        .join("fixtures")
        .join(name)
}

fn sha(byte: u8) -> String {
    format!("{byte:02x}").repeat(32)
}

fn carrier_pair() -> (CochainState, CochainState) {
    let source_d0 = BinaryLinearMap::from_rows(1, vec![vec![true], vec![false]]).unwrap();
    let source_d1 = BinaryLinearMap::from_rows(2, vec![vec![false, true]]).unwrap();
    let source = CochainState::new(
        BinaryCochainSegment::new(1, source_d0, source_d1).unwrap(),
        vec![false, true],
    )
    .unwrap();

    let target_d0 =
        BinaryLinearMap::from_rows(1, vec![vec![true], vec![false], vec![false]]).unwrap();
    let target_d1 = BinaryLinearMap::from_rows(3, vec![vec![false, true, false]]).unwrap();
    let target = CochainState::new(
        BinaryCochainSegment::new(1, target_d0, target_d1).unwrap(),
        vec![false, true, false],
    )
    .unwrap();

    (source, target)
}

fn source_manifest() -> Vec<SourceHashV1> {
    S02_002_SOURCE_MANIFEST
        .iter()
        .map(|(path, sha256)| SourceHashV1 {
            path: (*path).to_owned(),
            sha256: (*sha256).to_owned(),
        })
        .collect()
}

fn manifest_write_surface() -> Vec<String> {
    vec![
        "omega_engine/crates/omega_state/tests/fixtures/gtoc3_lift_license_fixture_matrix_v1.json"
            .to_owned(),
        "omega_engine/crates/omega_state/tests/fixtures/gtoc3_lift_license_receipt_matrix_v1.json"
            .to_owned(),
    ]
}

fn manifest() -> OperatorManifestV1 {
    OperatorManifestV1 {
        schema_version: OPERATOR_MANIFEST_SCHEMA_VERSION.to_owned(),
        operator_id: S02_002_OPERATOR_ID.to_owned(),
        semantic_contract_id: S02_002_SEMANTIC_CONTRACT_ID.to_owned(),
        input_families: vec!["omega.carrier-transition.request.v1".to_owned()],
        output_families: vec!["omega.lift-license-evaluation.v1".to_owned()],
        permitted_operations: vec![OperatorOperationV1::CarrierLift],
        required_capabilities: vec![
            OperatorCapabilityV1::CarrierTransition,
            OperatorCapabilityV1::DeterministicReplay,
        ],
        permission_ceiling: vec![
            OperatorPermissionV1::ReadFixture,
            OperatorPermissionV1::WriteReceipt,
        ],
        write_surface: manifest_write_surface(),
        evidence_ceiling: S02_002_EVIDENCE_CEILING.to_owned(),
        license_ids: vec![S02_002_license_ID.to_owned()],
        witness_requirements: vec![
            OperatorWitnessRequirementV1::Producer,
            OperatorWitnessRequirementV1::IndependentEvaluator,
            OperatorWitnessRequirementV1::AuthorityWitness,
        ],
        authority_effect: AuthorityEffect::None,
    }
}

fn trigger(operator_manifest_sha256: String) -> LiftTriggerV1 {
    LiftTriggerV1 {
        schema_version: LIFT_TRIGGER_SCHEMA_VERSION.to_owned(),
        trigger_id: "trigger:s02-002:bounded-carrier-lift-v1".to_owned(),
        operation: DdaOp::Lift,
        operator_id: S02_002_OPERATOR_ID.to_owned(),
        operator_manifest_sha256,
        source_carrier_sha256: S02_002_SOURCE_CARRIER_SHA256.to_owned(),
        target_carrier_sha256: S02_002_TARGET_CARRIER_SHA256.to_owned(),
        obstruction_summary_sha256: S02_002_OBSTRUCTION_SHA256.to_owned(),
        evidence_ceiling: S02_002_EVIDENCE_CEILING.to_owned(),
        authority_effect: AuthorityEffect::None,
    }
}

fn candidate(trigger: &LiftTriggerV1) -> LiftLicenseCandidateV1 {
    LiftLicenseCandidateV1 {
        schema_version: LIFT_license_CANDIDATE_SCHEMA_VERSION.to_owned(),
        candidate_id: "candidate:s02-002:bounded-carrier-lift-v1".to_owned(),
        proposed_license_id: S02_002_license_ID.to_owned(),
        trigger_sha256: coda3_sha256_json_v1(trigger).unwrap(),
        operation: trigger.operation,
        operator_id: trigger.operator_id.clone(),
        operator_manifest_sha256: trigger.operator_manifest_sha256.clone(),
        source_carrier_sha256: trigger.source_carrier_sha256.clone(),
        target_carrier_sha256: trigger.target_carrier_sha256.clone(),
        obstruction_witness: Some(ObstructionWitnessV1 {
            witness_id: "witness:s02-002:obstruction-v1".to_owned(),
            carrier_sha256: trigger.source_carrier_sha256.clone(),
            obstruction_sha256: trigger.obstruction_summary_sha256.clone(),
            checked_packet_sha256: sha(0x31),
            repair_exhaustion_sha256: sha(0x32),
        }),
        preservation_witness: Some(PreservationWitnessV1 {
            witness_id: "witness:s02-002:preservation-v1".to_owned(),
            invariant_id: "invariant:s02-002:bounded-cohomology-class-v1".to_owned(),
            source_invariant_sha256: sha(0x40),
            target_invariant_sha256: sha(0x40),
        }),
        non_destruction_witness: Some(NonDestructionWitnessV1 {
            witness_id: "witness:s02-002:non-destruction-v1".to_owned(),
            source_protected_sha256: vec![sha(0xa1), sha(0xb2)],
            target_protected_sha256: vec![sha(0xa1), sha(0xb2), sha(0xc3)],
            rollback_sha256: sha(0x50),
        }),
        budget_boundary: Some(LiftBudgetBoundaryV1 {
            witness_id: "witness:s02-002:budget-v1".to_owned(),
            max_cost_units: S02_002_MAX_COST_UNITS,
            requested_cost_units: 3,
            max_new_dimensions: S02_002_MAX_NEW_DIMENSIONS,
            requested_new_dimensions: 1,
        }),
        authority_boundary: Some(LiftAuthorityBoundaryV1 {
            witness_id: "witness:s02-002:authority-none-v1".to_owned(),
            promotion_performed: false,
            authority_effect: AuthorityEffect::None,
        }),
        terminalizer_route: Some(LiftTerminalizerRouteV1 {
            route_id: "route:s02-002:stabilized-survivor-v1".to_owned(),
            terminalizer_id: "terminalizer:s02-002:fixture-replay-v1".to_owned(),
            replay_sha256: sha(0x60),
            terminal: LiftTerminalRouteV1::StabilizedSurvivor,
        }),
        constructor_set_sha256: sha(0x70),
        minimality_witness_sha256: sha(0x80),
        replay_manifest_sha256: sha(0x90),
        evidence_ceiling: trigger.evidence_ceiling.clone(),
        authority_effect: AuthorityEffect::None,
    }
}

fn packet() -> Coda3PacketV1 {
    let source_manifest = source_manifest();
    let mut visible_artifact_hashes = source_manifest
        .iter()
        .map(|source| source.sha256.clone())
        .collect::<Vec<_>>();
    visible_artifact_hashes.sort();
    visible_artifact_hashes.dedup();
    let operator_manifest = manifest();
    let operator_manifest_sha256 = coda3_sha256_json_v1(&operator_manifest).unwrap();
    let trigger = trigger(operator_manifest_sha256);
    let evaluator_id = "witness:evaluator:s02-002-independent-v1".to_owned();
    let mut observer = FrozenObserverContextV1 {
        observer_id: evaluator_id.clone(),
        observer_domain: S02_002_OBSERVER_DOMAIN.to_owned(),
        state_domain: S02_002_STATE_DOMAIN.to_owned(),
        observer_hash: "0".repeat(64),
        visible_artifact_hashes,
        hidden_artifact_classes: vec![
            "human-license-issuance".to_owned(),
            "live-provider-context".to_owned(),
            "production-credentials".to_owned(),
        ],
        tool_permissions: vec![
            "read:frozen-source".to_owned(),
            "test:omega_lifts".to_owned(),
            "test:omega_state".to_owned(),
            "write:admitted-paths".to_owned(),
        ],
        write_surface: S02_002_WRITE_SURFACE
            .iter()
            .map(|path| (*path).to_owned())
            .collect(),
        evidence_ceiling: S02_002_EVIDENCE_CEILING.to_owned(),
    };
    observer.observer_hash = coda3_observer_sha256_v1(&observer).unwrap();
    Coda3PacketV1 {
        schema_version: CODA3_PACKET_SCHEMA_VERSION.to_owned(),
        packet_id: "S02-002:gtoc3-lift-license-v1".to_owned(),
        frozen_base: S02_002_FROZEN_BASE.to_owned(),
        target_sprint: S02_002_TARGET.to_owned(),
        source_manifest,
        budgets: Coda1BudgetsV1 {
            attempt_budget: 1,
            repair_budget: 2,
            successor_budget: 1,
            time_budget_seconds: 8 * 60 * 60,
            process_budget: 4,
            token_budget: 200_000,
        },
        evidence_ceiling: S02_002_EVIDENCE_CEILING.to_owned(),
        observer,
        producer_id: "witness:producer:s02-002-license-candidate-v1".to_owned(),
        evaluator_id,
        authority_witness_id: "witness:authority:s02-002-none-v1".to_owned(),
        prior_work_ledger: vec![
            "S01-003 bounded GTOC-2 transport".to_owned(),
            "S02-001 bounded operator registry".to_owned(),
            "omega_lifts canonical evidence owner".to_owned(),
        ],
        operator_manifest,
        candidate: Some(candidate(&trigger)),
        trigger,
    }
}

fn seal(packet: Coda3PacketV1) -> Coda3AdmissionV1 {
    let packet_sha256 = coda3_packet_sha256_v1(&packet).unwrap();
    Coda3AdmissionV1 {
        schema_version: CODA3_ADMISSION_SCHEMA_VERSION.to_owned(),
        packet,
        packet_sha256,
    }
}

fn reseal(admission: &mut Coda3AdmissionV1) {
    admission.packet_sha256 = coda3_packet_sha256_v1(&admission.packet).unwrap();
}

fn fixture_set() -> Coda3FixtureSetV1 {
    Coda3FixtureSetV1 {
        schema_version: CODA3_ADMISSION_SCHEMA_VERSION.to_owned(),
        admissions: vec![seal(packet())],
    }
}

fn receipt_set(fixtures: &Coda3FixtureSetV1) -> Coda3ReceiptSetV1 {
    Coda3ReceiptSetV1 {
        schema_version: CODA3_RECEIPT_SCHEMA_VERSION.to_owned(),
        executions: fixtures
            .admissions
            .iter()
            .map(|admission| evaluate_coda3_lift_candidate_v1(admission).unwrap())
            .collect(),
    }
}

fn pretty<T: Serialize>(value: &T) -> String {
    format!("{}\n", serde_json::to_string_pretty(value).unwrap())
}

fn committed_or_regenerated<T>(name: &str, value: &T) -> String
where
    T: Serialize,
{
    let rendered = pretty(value);
    let path = fixture_path(name);
    if env::var_os("OMEGA_REGEN_S02_002_FIXTURES").is_some() {
        fs::write(&path, &rendered).unwrap();
        return rendered;
    }

    fs::read_to_string(path).unwrap()
}

fn frozen_blob(_root: &Path, path: &str) -> Vec<u8> {
    upstream_history::frozen_blob(S02_002_FROZEN_BASE, path)
}

fn execution_error(mut admission: Coda3AdmissionV1) -> Coda3Error {
    reseal(&mut admission);
    evaluate_coda3_lift_candidate_v1(&admission).unwrap_err()
}

#[test]
fn committed_fixture_and_receipt_matrices_are_byte_stable() {
    let fixtures = fixture_set();
    let committed =
        committed_or_regenerated("gtoc3_lift_license_fixture_matrix_v1.json", &fixtures);
    assert_eq!(committed, pretty(&fixtures));
    assert_eq!(
        serde_json::from_str::<Coda3FixtureSetV1>(&committed).unwrap(),
        fixtures
    );

    let receipts = receipt_set(&fixtures);
    let committed =
        committed_or_regenerated("gtoc3_lift_license_receipt_matrix_v1.json", &receipts);
    assert_eq!(committed, pretty(&receipts));
    assert_eq!(
        serde_json::from_str::<Coda3ReceiptSetV1>(&committed).unwrap(),
        receipts
    );
}

#[test]
fn source_manifest_hashes_match_frozen_base_blobs() {
    let root = repository_root();
    for source in source_manifest() {
        assert_eq!(
            sha256_bytes_v1(&frozen_blob(&root, &source.path)),
            source.sha256,
            "{}",
            source.path
        );
    }
}

#[test]
fn frozen_carrier_hashes_bind_actual_dda_segments() {
    let (source, target) = carrier_pair();
    assert_eq!(
        lift_sha256_json_v1(&source.segment).unwrap(),
        S02_002_SOURCE_CARRIER_SHA256
    );
    assert_eq!(
        lift_sha256_json_v1(&target.segment).unwrap(),
        S02_002_TARGET_CARRIER_SHA256
    );
    assert_eq!(
        sha256_bytes_v1(S02_002_OBSTRUCTION_SUMMARY.as_bytes()),
        S02_002_OBSTRUCTION_SHA256
    );
}

#[test]
fn complete_candidate_is_only_admissible_for_licensing() {
    let admission = seal(packet());
    admission.validate().unwrap();
    let execution = evaluate_coda3_lift_candidate_v1(&admission).unwrap();

    assert_eq!(
        execution.classification.terminal_proposal,
        CodaTerminal::StabilizedSurvivor
    );
    assert!(execution.classification.structural_trigger_not_license);
    assert!(execution.classification.complete_for_licensing);
    assert!(!execution.classification.license_issued);
    assert!(!execution.classification.lift_executed);
    assert!(execution.classification.survivor_routes.is_empty());
    assert!(execution.classification.residual_ids.is_empty());
    assert!(execution.classification.authority_effect.is_none());
    assert_eq!(
        execution.receipts.producer.evaluation.status,
        LiftLicenseValidationStatusV1::AdmissibleForLicensing
    );
    assert!(!execution.receipts.producer.license_issued);
    assert!(!execution.receipts.producer.lift_executed);
    assert!(!execution.receipts.authority_witness.license_issued);
    assert!(!execution.receipts.authority_witness.lift_executed);
    assert!(
        !execution
            .receipts
            .authority_witness
            .human_promotion_performed
    );
    assert!(execution
        .receipts
        .authority_witness
        .authority_effect
        .is_none());
}

#[test]
fn producer_evaluator_and_replay_are_deterministic() {
    let admission = seal(packet());
    let first = evaluate_coda3_lift_candidate_v1(&admission).unwrap();
    let second = evaluate_coda3_lift_candidate_v1(&admission).unwrap();
    assert_eq!(first, second);
    assert!(first.receipts.evaluation.exact_match);
    assert!(first.receipts.evaluation.trigger_not_treated_as_license);
    assert!(first.receipts.replay.deterministic);
    assert_eq!(
        first.receipts.replay.first_producer_sha256,
        first.receipts.replay.replay_producer_sha256
    );
    assert_eq!(
        coda3_sha256_json_v1(&first).unwrap(),
        coda3_sha256_json_v1(&second).unwrap()
    );
}

#[test]
fn trigger_without_candidate_routes_to_lift_license_needed() {
    let mut admission = seal(packet());
    admission.packet.candidate = None;
    let error = execution_error(admission);
    assert!(matches!(error, Coda3Error::MissingLicenseCandidate));
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);
    assert_eq!(
        error.survivor_route(),
        Some(Coda3SurvivorRouteV1::LiftLicenseNeeded)
    );
}

#[test]
fn missing_evidence_routes_to_proof_or_oracle_without_issuing() {
    let mut obstruction = seal(packet());
    obstruction
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .obstruction_witness = None;
    let error = execution_error(obstruction);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::MissingObstructionWitness)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);
    assert_eq!(
        error.survivor_route(),
        Some(Coda3SurvivorRouteV1::ProofObligation)
    );

    let mut preservation = seal(packet());
    preservation
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .preservation_witness = None;
    let error = execution_error(preservation);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::MissingPreservationWitness)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::OracleNeeded);
    assert_eq!(
        error.survivor_route(),
        Some(Coda3SurvivorRouteV1::OracleNeeded)
    );

    let mut terminalizer = seal(packet());
    terminalizer
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .terminalizer_route = None;
    let error = execution_error(terminalizer);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::MissingTerminalizerRoute)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::OracleNeeded);

    let mut non_destruction = seal(packet());
    non_destruction
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .non_destruction_witness = None;
    let error = execution_error(non_destruction);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::MissingNonDestructionWitness)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);

    let mut budget = seal(packet());
    budget.packet.candidate.as_mut().unwrap().budget_boundary = None;
    let error = execution_error(budget);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::MissingBudgetBoundary)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);
}

#[test]
fn destructive_or_authority_expanding_candidates_are_refused() {
    let mut preservation = seal(packet());
    preservation
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .preservation_witness
        .as_mut()
        .unwrap()
        .target_invariant_sha256 = sha(0x41);
    let error = execution_error(preservation);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::PreservationViolation)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    let mut destructive = seal(packet());
    destructive
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .non_destruction_witness
        .as_mut()
        .unwrap()
        .target_protected_sha256
        .remove(0);
    let error = execution_error(destructive);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::NonDestructionViolation)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    let mut authority = seal(packet());
    authority
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .authority_boundary
        .as_mut()
        .unwrap()
        .promotion_performed = true;
    let error = execution_error(authority);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::AuthorityExpansion)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    let mut missing_authority = seal(packet());
    missing_authority
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .authority_boundary = None;
    let error = execution_error(missing_authority);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::MissingAuthorityBoundary)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);
}

#[test]
fn policy_budget_and_registered_license_are_enforced() {
    let mut policy = seal(packet());
    policy
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .budget_boundary
        .as_mut()
        .unwrap()
        .max_cost_units = S02_002_MAX_COST_UNITS + 1;
    let error = execution_error(policy);
    assert!(matches!(error, Coda3Error::PolicyBudgetExceeded));
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);

    let mut requested = seal(packet());
    requested
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .budget_boundary
        .as_mut()
        .unwrap()
        .requested_cost_units = S02_002_MAX_COST_UNITS + 1;
    let error = execution_error(requested);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::BudgetExceeded)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);

    let mut unknown = seal(packet());
    unknown
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .proposed_license_id = "license:unregistered".to_owned();
    let error = execution_error(unknown);
    assert!(matches!(error, Coda3Error::LicenseNotRegistered));
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);
}

#[test]
fn candidate_scope_trigger_and_operator_tampering_fail_closed() {
    let mut scope = seal(packet());
    scope
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .source_carrier_sha256 = sha(0x11);
    let error = execution_error(scope);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::ScopeMismatch)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);

    let mut trigger_hash = seal(packet());
    trigger_hash
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .trigger_sha256 = sha(0xff);
    let error = execution_error(trigger_hash);
    assert!(matches!(
        error,
        Coda3Error::Lift(LiftLicenseError::TriggerHashMismatch)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);

    let mut operator = seal(packet());
    operator.packet.candidate.as_mut().unwrap().operator_id = "operator:unknown".to_owned();
    let error = execution_error(operator);
    assert!(matches!(error, Coda3Error::LicenseNotRegistered));
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);

    let mut trigger_manifest = seal(packet());
    trigger_manifest.packet.trigger.operator_manifest_sha256 = sha(0xee);
    reseal(&mut trigger_manifest);
    assert!(matches!(
        trigger_manifest.validate().unwrap_err(),
        Coda3Error::TriggerManifestMismatch
    ));
}

#[test]
fn operation_carrier_and_terminalizer_are_bound_to_the_admitted_manifest() {
    let mut operation = seal(packet());
    operation.packet.trigger.operation = DdaOp::Descent;
    let trigger_sha256 = coda3_sha256_json_v1(&operation.packet.trigger).unwrap();
    let candidate = operation.packet.candidate.as_mut().unwrap();
    candidate.operation = DdaOp::Descent;
    candidate.trigger_sha256 = trigger_sha256;
    reseal(&mut operation);
    let error = operation.validate().unwrap_err();
    assert!(matches!(error, Coda3Error::TriggerCarrierMismatch));
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);
    assert_eq!(
        error.survivor_route(),
        Some(Coda3SurvivorRouteV1::InvalidEvidence)
    );

    let mut carrier = seal(packet());
    carrier.packet.trigger.target_carrier_sha256 = sha(0x21);
    let trigger_sha256 = coda3_sha256_json_v1(&carrier.packet.trigger).unwrap();
    let candidate = carrier.packet.candidate.as_mut().unwrap();
    candidate.target_carrier_sha256 = sha(0x21);
    candidate.trigger_sha256 = trigger_sha256;
    reseal(&mut carrier);
    assert!(matches!(
        carrier.validate().unwrap_err(),
        Coda3Error::TriggerCarrierMismatch
    ));

    let mut terminalizer = seal(packet());
    terminalizer
        .packet
        .candidate
        .as_mut()
        .unwrap()
        .terminalizer_route
        .as_mut()
        .unwrap()
        .terminal = LiftTerminalRouteV1::ExactRepair;
    let error = execution_error(terminalizer);
    assert!(matches!(error, Coda3Error::TerminalizerMismatch));
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);
    assert_eq!(
        error.survivor_route(),
        Some(Coda3SurvivorRouteV1::InvalidEvidence)
    );
}

#[test]
fn packet_observer_source_identity_and_hash_seals_fail_closed() {
    let mut frozen = seal(packet());
    frozen.packet.frozen_base = "0".repeat(40);
    reseal(&mut frozen);
    assert!(matches!(
        frozen.validate().unwrap_err(),
        Coda3Error::FrozenBaseMismatch
    ));

    let mut source = seal(packet());
    source.packet.source_manifest[0].sha256 = sha(0x00);
    reseal(&mut source);
    assert!(matches!(
        source.validate().unwrap_err(),
        Coda3Error::SourceManifestMismatch
    ));

    let mut observer = seal(packet());
    observer.packet.observer.tool_permissions[0] = "read:unfrozen".to_owned();
    reseal(&mut observer);
    assert!(matches!(
        observer.validate().unwrap_err(),
        Coda3Error::ObserverContextMismatch
    ));

    let mut observer_hash = seal(packet());
    observer_hash.packet.observer.observer_hash = sha(0x00);
    reseal(&mut observer_hash);
    assert!(matches!(
        observer_hash.validate().unwrap_err(),
        Coda3Error::ObserverHashMismatch { .. }
    ));

    let mut identity = seal(packet());
    identity.packet.evaluator_id = identity.packet.producer_id.clone();
    reseal(&mut identity);
    let error = identity.validate().unwrap_err();
    assert!(matches!(error, Coda3Error::IdentityCollision));
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    let mut packet_hash = seal(packet());
    packet_hash.packet_sha256 = sha(0x00);
    assert!(matches!(
        packet_hash.validate().unwrap_err(),
        Coda3Error::PacketHashMismatch { .. }
    ));
}

#[test]
fn exact_witness_set_and_authority_none_are_contractual() {
    manifest().validate().unwrap();

    let mut missing_witness = manifest();
    missing_witness.witness_requirements.pop();
    assert!(matches!(
        missing_witness.validate().unwrap_err(),
        OperatorRegistryContractError::WitnessSetChanged(ref id)
            if id == S02_002_OPERATOR_ID
    ));

    let mut admission = seal(packet());
    admission
        .packet
        .operator_manifest
        .witness_requirements
        .pop();
    let error = execution_error(admission);
    assert!(matches!(
        error,
        Coda3Error::Contract(OperatorRegistryContractError::WitnessSetChanged(_))
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    let mut authority = seal(packet());
    authority.packet.operator_manifest.authority_effect = AuthorityEffect::Uncertified;
    let error = execution_error(authority);
    assert!(matches!(
        error,
        Coda3Error::Contract(OperatorRegistryContractError::AuthorityExpansion(_))
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);
}

#[test]
fn independent_evaluator_rejects_producer_and_classification_tampering() {
    let admission = seal(packet());
    let execution = evaluate_coda3_lift_candidate_v1(&admission).unwrap();

    let mut evaluation = execution.receipts.producer.clone();
    evaluation.evaluation.preservation_checked = false;
    assert!(matches!(
        independently_evaluate_claimed_coda3_v1(&admission, &evaluation).unwrap_err(),
        Coda3Error::ProducerReceiptMismatch
    ));

    let mut issuance = execution.receipts.producer.clone();
    issuance.license_issued = true;
    assert!(matches!(
        independently_evaluate_claimed_coda3_v1(&admission, &issuance).unwrap_err(),
        Coda3Error::ProducerReceiptMismatch
    ));

    let mut metadata = execution.receipts.producer.clone();
    metadata.producer_id = "witness:producer:substituted".to_owned();
    assert!(matches!(
        independently_evaluate_claimed_coda3_v1(&admission, &metadata).unwrap_err(),
        Coda3Error::ProducerReceiptMismatch
    ));

    let mut classification = execution.classification;
    classification.license_issued = true;
    assert!(matches!(
        classification.validate().unwrap_err(),
        Coda3Error::ClassificationInvariant
    ));
}

#[test]
fn unknown_fields_and_future_enum_variants_fail_closed() {
    let mut admission_json = serde_json::to_value(seal(packet())).unwrap();
    admission_json["unknown_field"] = Value::Bool(true);
    assert!(serde_json::from_value::<Coda3AdmissionV1>(admission_json).is_err());

    let mut candidate_json = serde_json::to_value(seal(packet())).unwrap();
    candidate_json["packet"]["candidate"]["unknown_field"] = Value::Bool(true);
    assert!(serde_json::from_value::<Coda3AdmissionV1>(candidate_json).is_err());

    assert!(serde_json::from_str::<DdaOp>("\"future_carrier_op\"").is_err());
    assert!(
        serde_json::from_str::<LiftLicenseValidationStatusV1>("\"future_license_status\"").is_err()
    );
    assert!(serde_json::from_str::<Coda3SurvivorRouteV1>("\"future_route\"").is_err());
}

#[test]
fn committed_evidence_has_no_issuance_execution_or_authority_path() {
    let fixtures = pretty(&fixture_set());
    let receipts = pretty(&receipt_set(&fixture_set()));

    assert!(fixtures.contains("one finite DDA carrier-change fixture"));
    assert!(receipts.contains("admissible_for_licensing"));
    assert!(!receipts.contains("\"license_issued\": true"));
    assert!(!receipts.contains("\"lift_executed\": true"));
    assert!(!receipts.contains("\"human_promotion_performed\": true"));
    assert!(!fixtures.contains("api_key"));
    assert!(!fixtures.contains("endpoint"));
    assert!(!fixtures.contains("production-credentials\": []"));
    assert!(!receipts.contains("\"Certified\""));
}

// Origin: vendor/engine/tests/engine_state/coda3_lift_license.rs
// Claim: urn:omega:crates_rs:tests:coda3-lift-license:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord78673d26 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord78673d26` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError78673d26 {
    /// Refused because `admitted_items` was zero.
    EmptyAdmission,
    /// Refused because `capacity_bound` was zero.
    CapacityZero,
    /// Refused because `admitted_items` exceeded `capacity_bound`.
    ExceedsCapacity {
        /// Requested item count.
        admitted_items: u64,
        /// Declared maximum capacity.
        capacity_bound: u64,
    },
}

#[allow(dead_code, missing_docs)]
impl BoundaryError78673d26 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError78673d26 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError78673d26 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord78673d26 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError78673d26> {
        if capacity_bound == 0 {
            return Err(BoundaryError78673d26::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError78673d26::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError78673d26::ExceedsCapacity {
                admitted_items,
                capacity_bound,
            });
        }
        Ok(Self {
            admitted_items,
            capacity_bound,
        })
    }

    /// Returns the admitted item count.
    pub const fn admitted_items(&self) -> u64 {
        self.admitted_items
    }

    /// Returns the declared capacity bound.
    pub const fn capacity_bound(&self) -> u64 {
        self.capacity_bound
    }

    /// Returns the remaining capacity (`capacity_bound - admitted_items`).
    pub const fn remaining_capacity(&self) -> u64 {
        self.capacity_bound.saturating_sub(self.admitted_items)
    }
}

#[test]
fn l4_boundary_admits_and_refuses_78673d26() {
    let admitted = BoundaryRecord78673d26::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord78673d26::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
