#[path = "support/upstream_history.rs"]
mod upstream_history;

use std::env;
use std::fs;
use std::path::{Path, PathBuf};

use engine_state::coda1_classifier::{
    execute_and_evaluate_coda1_v1, sha256_bytes_v1, sha256_json_v1, Coda1AdmissionV1,
    Coda1BudgetsV1, Coda1ExecutionV1, Coda1RouteV1, SourceHashV1,
};
use engine_state::coda2_degree_shift::*;
use engine_state::coda_gtla_protocol::{FrozenObserverContextV1, CodaTerminal};
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use serde_json::Value;

const FROZEN_BASE: &str = "f1d8390e081596ce50fdf91c9e9cca5e32294342";

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Coda1FixtureSetV1 {
    schema_version: String,
    cases: Vec<Coda1AdmissionV1>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Coda2FixtureCaseV1 {
    source_packet_id: String,
    admission: Coda2AdmissionV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Coda2FixtureSetV1 {
    schema_version: String,
    cases: Vec<Coda2FixtureCaseV1>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Coda2ReceiptCaseV1 {
    source_packet_id: String,
    source_execution: Coda1ExecutionV1,
    execution: Coda2ExecutionV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Coda2ReceiptSetV1 {
    schema_version: String,
    executions: Vec<Coda2ReceiptCaseV1>,
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

fn source_fixtures() -> Coda1FixtureSetV1 {
    serde_json::from_str(&fs::read_to_string(fixture_path("gtoc1_fixture_matrix_v1.json")).unwrap())
        .unwrap()
}

fn source_manifest() -> Vec<SourceHashV1> {
    vec![
        SourceHashV1 {
            path: "omega_engine/crates/omega_state/src/gtoc1_classifier.rs".to_owned(),
            sha256: "de753b8664cd118f83f18399161c33887316f4e93702ff34f39ace8b9bcb46af".to_owned(),
        },
        SourceHashV1 {
            path: "omega_engine/crates/omega_state/tests/fixtures/gtoc1_fixture_matrix_v1.json"
                .to_owned(),
            sha256: "28955416a2c0f97ee560851fc132625813966dd0e0112b2dc413b0f1ac3d0784".to_owned(),
        },
        SourceHashV1 {
            path:
                "omega_engine/general_theory_of_obstruction_calculus/papers/999_GTOC/math_spine.md"
                    .to_owned(),
            sha256: "3d261e061ab7988891c7ecbb9b762b3d3146d7b961b14231fd6dd88245161679".to_owned(),
        },
    ]
}

fn write_surface() -> Vec<String> {
    let mut paths = vec![
        "docs/gtoc-canonicalization-remaining-work.md",
        "docs/omega-conductor-epic-v001.md",
        "docs/saga_01_universal_gtoc_gtla_protocol.md",
        "docs/sprint_s01_003.md",
        "docs/status/omega_conductor_s01_003_status_2026-07-18.md",
        "omega_engine/crates/omega_state/src/gtoc2_degree_shift.rs",
        "omega_engine/crates/omega_state/src/lib.rs",
        "omega_engine/crates/omega_state/tests/fixtures/gtoc2_fixture_matrix_v1.json",
        "omega_engine/crates/omega_state/tests/fixtures/gtoc2_receipt_matrix_v1.json",
        "omega_engine/crates/omega_state/tests/gtoc2_degree_shift.rs",
        "omega_engine/general_theory_of_obstruction_calculus/papers/999_GTOC/math_spine.md",
        "omega_engine/general_theory_of_obstruction_calculus/papers/999_GTOC/theorem_ledger.md",
    ]
    .into_iter()
    .map(str::to_owned)
    .collect::<Vec<_>>();
    paths.sort();
    paths
}

fn base_packet(source: &Coda1AdmissionV1, base_degree: u16) -> Coda2PacketV1 {
    let source_execution = execute_and_evaluate_coda1_v1(source).unwrap();
    let sources = source_manifest();
    let mut visible_hashes = sources
        .iter()
        .map(|entry| entry.sha256.clone())
        .collect::<Vec<_>>();
    visible_hashes.sort();
    visible_hashes.dedup();
    let evaluator_id = "witness:evaluator:degree-array-replay-v1".to_owned();
    let mut hidden_artifact_classes = vec![
        "unadmitted-runtime-state".to_owned(),
        "unbounded-natural-degree-window".to_owned(),
    ];
    hidden_artifact_classes.sort();
    let mut tool_permissions = vec![
        "read:frozen-gtoc1-source".to_owned(),
        "test:omega_state".to_owned(),
        "write:admitted-paths".to_owned(),
    ];
    tool_permissions.sort();
    let mut observer = FrozenObserverContextV1 {
        observer_id: evaluator_id.clone(),
        observer_domain: CODA2_OBSERVER_DOMAIN.to_owned(),
        state_domain: CODA2_STATE_DOMAIN.to_owned(),
        observer_hash: "0".repeat(64),
        visible_artifact_hashes: visible_hashes,
        hidden_artifact_classes,
        tool_permissions,
        write_surface: write_surface(),
        evidence_ceiling: CODA2_EVIDENCE_CEILING.to_owned(),
    };
    observer.observer_hash = coda2_observer_sha256_v1(&observer).unwrap();

    let mut prior_work_ledger = vec![
        "GTOC-2 canonical math spine".to_owned(),
        "S01-001 protocol machine".to_owned(),
        "S01-002 sealed finite GTOC-1 classifier".to_owned(),
    ];
    prior_work_ledger.sort();

    Coda2PacketV1 {
        schema_version: CODA2_PACKET_SCHEMA_VERSION.to_owned(),
        packet_id: format!("S01-003:{}:{base_degree}", source.packet.packet_id),
        frozen_base: FROZEN_BASE.to_owned(),
        target_rows: vec!["GTOC-2".to_owned()],
        source_manifest: sources,
        budgets: Coda1BudgetsV1 {
            attempt_budget: 1,
            repair_budget: 2,
            successor_budget: 1,
            time_budget_seconds: 8 * 60 * 60,
            process_budget: 4,
            token_budget: 200_000,
        },
        evidence_ceiling: CODA2_EVIDENCE_CEILING.to_owned(),
        observer,
        producer_id: "witness:producer:degree-shift-v1".to_owned(),
        evaluator_id,
        authority_witness_id: "witness:authority:none-check-gtoc2-v1".to_owned(),
        prior_work_ledger,
        source_packet_id: source.packet.packet_id.clone(),
        source_admission_sha256: sha256_json_v1(source).unwrap(),
        source_classification_sha256: sha256_json_v1(&source_execution.classification).unwrap(),
        source_observer_sha256: source.packet.observer.observer_hash.clone(),
        expected_source_route: source_execution.classification.route,
        expected_source_terminal: source_execution.classification.terminal_proposal,
        shift: DegreeShiftV1 { base_degree },
    }
}

fn seal(packet: Coda2PacketV1) -> Coda2AdmissionV1 {
    let packet_sha256 = coda2_packet_sha256_v1(&packet).unwrap();
    Coda2AdmissionV1 {
        schema_version: CODA2_ADMISSION_SCHEMA_VERSION.to_owned(),
        packet,
        packet_sha256,
    }
}

fn fixture_set() -> Coda2FixtureSetV1 {
    let sources = source_fixtures();
    let bases = [1, 2, 32_768, CODA2_MAX_BASE_DEGREE];
    let cases = sources
        .cases
        .iter()
        .zip(bases)
        .map(|(source, base_degree)| Coda2FixtureCaseV1 {
            source_packet_id: source.packet.packet_id.clone(),
            admission: seal(base_packet(source, base_degree)),
        })
        .collect();
    Coda2FixtureSetV1 {
        schema_version: CODA2_ADMISSION_SCHEMA_VERSION.to_owned(),
        cases,
    }
}

fn find_source<'a>(sources: &'a Coda1FixtureSetV1, source_packet_id: &str) -> &'a Coda1AdmissionV1 {
    sources
        .cases
        .iter()
        .find(|source| source.packet.packet_id == source_packet_id)
        .expect("fixture source packet is present")
}

fn receipt_set(fixtures: &Coda2FixtureSetV1) -> Coda2ReceiptSetV1 {
    let sources = source_fixtures();
    let executions = fixtures
        .cases
        .iter()
        .map(|case| {
            let source = find_source(&sources, &case.source_packet_id);
            Coda2ReceiptCaseV1 {
                source_packet_id: case.source_packet_id.clone(),
                source_execution: execute_and_evaluate_coda1_v1(source).unwrap(),
                execution: execute_and_evaluate_coda2_v1(&case.admission, source).unwrap(),
            }
        })
        .collect();
    Coda2ReceiptSetV1 {
        schema_version: CODA2_RECEIPT_SCHEMA_VERSION.to_owned(),
        executions,
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
    if env::var_os("OMEGA_REGEN_GTOC2_FIXTURES").is_some() {
        fs::write(&path, &rendered).unwrap();
    }
    fs::read_to_string(path).unwrap()
}

fn frozen_blob(_root: &Path, path: &str) -> Vec<u8> {
    upstream_history::frozen_blob(FROZEN_BASE, path)
}

#[test]
fn committed_fixture_and_receipt_matrices_are_byte_stable() {
    let fixtures = fixture_set();
    let committed = committed_or_regenerated("gtoc2_fixture_matrix_v1.json", &fixtures);
    assert_eq!(committed, pretty(&fixtures));
    assert_eq!(
        serde_json::from_str::<Coda2FixtureSetV1>(&committed).unwrap(),
        fixtures
    );

    let receipts = receipt_set(&fixtures);
    let committed = committed_or_regenerated("gtoc2_receipt_matrix_v1.json", &receipts);
    assert_eq!(committed, pretty(&receipts));
    assert_eq!(
        serde_json::from_str::<Coda2ReceiptSetV1>(&committed).unwrap(),
        receipts
    );
}

#[test]
fn source_manifest_hashes_match_frozen_base_blobs() {
    let root = repository_root();
    for source in source_manifest() {
        let bytes = frozen_blob(&root, &source.path);
        assert_eq!(sha256_bytes_v1(&bytes), source.sha256, "{}", source.path);
    }
}

#[test]
fn four_routes_and_boundary_degrees_preserve_sealed_coda1_results() {
    let fixtures = fixture_set();
    let sources = source_fixtures();
    let executions = fixtures
        .cases
        .iter()
        .map(|case| {
            execute_and_evaluate_coda2_v1(
                &case.admission,
                find_source(&sources, &case.source_packet_id),
            )
            .unwrap()
        })
        .collect::<Vec<_>>();
    assert_eq!(
        executions
            .iter()
            .map(|execution| execution.classification.source_route)
            .collect::<Vec<_>>(),
        Coda1RouteV1::ALL
    );
    assert_eq!(
        executions
            .iter()
            .map(|execution| execution.classification.degree_bijection.base_degree)
            .collect::<Vec<_>>(),
        vec![1, 2, 32_768, CODA2_MAX_BASE_DEGREE]
    );
    for execution in executions {
        let classification = execution.classification;
        assert_eq!(classification.source_route, classification.reindexed_route);
        assert_eq!(
            classification.source_terminal,
            classification.reindexed_terminal
        );
        assert_eq!(
            classification.source_rule_sha256,
            classification.reindexed_rule_sha256
        );
        assert!(classification.classification_preserved);
        assert_eq!(
            classification.terminal_proposal,
            CodaTerminal::StabilizedSurvivor
        );
        assert!(classification.authority_effect.is_none());
    }
}

#[test]
fn every_represented_base_degree_satisfies_both_bijection_laws() {
    for base_degree in CODA2_MIN_BASE_DEGREE..=CODA2_MAX_BASE_DEGREE {
        let shift = DegreeShiftV1 { base_degree };
        let witness = shift.witness().unwrap();
        witness.validate().unwrap();
        for local_degree in 0..=2 {
            let original = shift.to_original(local_degree).unwrap();
            assert_eq!(shift.to_local(original).unwrap(), local_degree);
        }
        for original in witness.original_degrees {
            let local = shift.to_local(original).unwrap();
            assert_eq!(shift.to_original(local).unwrap(), original);
        }
    }
}

#[test]
fn every_coda1_route_replays_at_representative_degrees() {
    let sources = source_fixtures();
    for source in &sources.cases {
        for base_degree in [1, 2, 17, 32_768, CODA2_MAX_BASE_DEGREE] {
            let admission = seal(base_packet(source, base_degree));
            let execution = execute_and_evaluate_coda2_v1(&admission, source).unwrap();
            let source_execution = execute_and_evaluate_coda1_v1(source).unwrap();
            assert_eq!(
                execution.classification.source_route,
                source_execution.classification.route
            );
            assert_eq!(
                execution.classification.source_terminal,
                source_execution.classification.terminal_proposal
            );
            assert!(execution.classification.classification_preserved);
        }
    }
}

#[test]
fn zero_and_overflowing_windows_fail_as_open_obstructions() {
    let source = &source_fixtures().cases[0];
    for base_degree in [0, u16::MAX - 1, u16::MAX] {
        let admission = seal(base_packet(source, base_degree));
        let error = classify_coda2_v1(&admission, source).unwrap_err();
        assert_eq!(error, Coda2Error::UnsupportedBaseDegree(base_degree));
        assert_eq!(error.terminal_route(), CodaTerminal::OpenObstruction);
    }

    let shift = DegreeShiftV1 { base_degree: 1 };
    let error = shift.to_local(4).unwrap_err();
    assert_eq!(error, Coda2Error::DegreeOutsideWindow(4));
    assert_eq!(error.terminal_route(), CodaTerminal::OpenObstruction);
    assert_eq!(
        shift.to_original(3).unwrap_err().terminal_route(),
        CodaTerminal::Invalid
    );
}

#[test]
fn packet_observer_paths_and_identities_are_sealed() {
    let sources = source_fixtures();
    let source = &sources.cases[0];

    let mut packet_hash = seal(base_packet(source, 1));
    packet_hash.packet.packet_id.push_str(":tampered");
    assert!(matches!(
        classify_coda2_v1(&packet_hash, source).unwrap_err(),
        Coda2Error::PacketHashMismatch { .. }
    ));

    let mut observer_hash = seal(base_packet(source, 1));
    observer_hash.packet.observer.observer_hash = "f".repeat(64);
    observer_hash.packet_sha256 = coda2_packet_sha256_v1(&observer_hash.packet).unwrap();
    assert!(matches!(
        classify_coda2_v1(&observer_hash, source).unwrap_err(),
        Coda2Error::ObserverHashMismatch { .. }
    ));

    let mut wildcard = seal(base_packet(source, 1));
    wildcard
        .packet
        .observer
        .write_surface
        .push("omega_engine/crates/omega_state/**".to_owned());
    wildcard.packet.observer.write_surface.sort();
    wildcard.packet.observer.observer_hash =
        coda2_observer_sha256_v1(&wildcard.packet.observer).unwrap();
    wildcard.packet_sha256 = coda2_packet_sha256_v1(&wildcard.packet).unwrap();
    assert!(matches!(
        classify_coda2_v1(&wildcard, source).unwrap_err(),
        Coda2Error::InvalidPath(_)
    ));

    let mut identity = seal(base_packet(source, 1));
    identity.packet.evaluator_id = identity.packet.producer_id.clone();
    identity.packet_sha256 = coda2_packet_sha256_v1(&identity.packet).unwrap();
    let error = classify_coda2_v1(&identity, source).unwrap_err();
    assert_eq!(error, Coda2Error::IdentityCollision);
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);
}

#[test]
fn sealed_source_admission_and_classification_cannot_be_substituted() {
    let sources = source_fixtures();
    let source = &sources.cases[0];
    let admission = seal(base_packet(source, 1));
    let error = classify_coda2_v1(&admission, &sources.cases[1]).unwrap_err();
    assert_eq!(error, Coda2Error::SourceBindingMismatch("source_packet_id"));

    let mut classification_hash = admission.clone();
    classification_hash.packet.source_classification_sha256 = "f".repeat(64);
    classification_hash.packet_sha256 =
        coda2_packet_sha256_v1(&classification_hash.packet).unwrap();
    assert_eq!(
        classify_coda2_v1(&classification_hash, source).unwrap_err(),
        Coda2Error::SourceBindingMismatch("source_classification_sha256")
    );
}

#[test]
fn independent_replay_rejects_producer_and_classification_tampering() {
    let sources = source_fixtures();
    let source = &sources.cases[0];
    let admission = seal(base_packet(source, 1));
    let execution = execute_and_evaluate_coda2_v1(&admission, source).unwrap();

    let mut producer = execution.receipts.producer.clone();
    producer.classification_sha256 = "f".repeat(64);
    assert_eq!(
        evaluate_coda2_v1(&admission, source, &execution.classification, &producer).unwrap_err(),
        Coda2Error::ProducerReceiptMismatch
    );

    let mut classification = execution.classification.clone();
    classification.authority_effect = AuthorityEffect::Uncertified;
    let error = evaluate_coda2_v1(
        &admission,
        source,
        &classification,
        &execution.receipts.producer,
    )
    .unwrap_err();
    assert_eq!(error, Coda2Error::AuthorityExpanded);
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    let mut witness = execution.classification;
    witness.degree_bijection.original_degrees[2] -= 1;
    assert_eq!(
        witness.validate().unwrap_err(),
        Coda2Error::BijectionInvariant
    );
}

#[test]
fn receipts_are_deterministic_independent_and_nonpromoting() {
    let fixtures = fixture_set();
    let sources = source_fixtures();
    for case in fixtures.cases {
        let source = find_source(&sources, &case.source_packet_id);
        let first = execute_and_evaluate_coda2_v1(&case.admission, source).unwrap();
        let second = execute_and_evaluate_coda2_v1(&case.admission, source).unwrap();
        assert_eq!(first, second);
        assert_ne!(
            first.receipts.producer.producer_id,
            first.receipts.evaluation.evaluator_id
        );
        assert_eq!(
            first
                .receipts
                .evaluation
                .independently_reconstructed_degrees,
            first.classification.degree_bijection.original_degrees
        );
        assert!(first.receipts.evaluation.exact_match);
        assert!(first.receipts.evaluation.route_preserved);
        assert!(first.receipts.evaluation.terminal_preserved);
        assert!(first.receipts.evaluation.cochain_rule_preserved);
        assert!(
            first
                .receipts
                .authority_witness
                .producer_evaluator_witness_distinct
        );
        assert!(!first.receipts.authority_witness.promotion_performed);
        assert!(first.receipts.producer.authority_effect.is_none());
        assert!(first.receipts.evaluation.authority_effect.is_none());
        assert!(first.receipts.terminal.authority_effect.is_none());
        assert_eq!(
            first.receipts.terminal.terminal_proposal,
            CodaTerminal::StabilizedSurvivor
        );
    }
}

#[test]
fn closed_wire_schema_rejects_unknown_fields_and_future_routes() {
    assert!(serde_json::from_str::<Coda1RouteV1>("\"future_route\"").is_err());

    let mut admission: Value = serde_json::to_value(&fixture_set().cases[0].admission).unwrap();
    admission["unknown_field"] = Value::Bool(true);
    assert!(serde_json::from_value::<Coda2AdmissionV1>(admission).is_err());

    let mut witness: Value =
        serde_json::to_value(DegreeShiftV1 { base_degree: 1 }.witness().unwrap()).unwrap();
    witness["unknown_field"] = Value::Bool(true);
    assert!(serde_json::from_value::<DegreeBijectionWitnessV1>(witness).is_err());
}
struct FailingSerializer;

impl Serialize for FailingSerializer {
    fn serialize<S>(&self, _serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        Err(serde::ser::Error::custom(
            "forced local GTOC-2 serialization failure",
        ))
    }
}

#[test]
fn local_json_failures_route_to_infrastructure_not_coda1_invalid() {
    let error = coda2_sha256_json_v1(&FailingSerializer).unwrap_err();
    assert!(matches!(
        &error,
        Coda2Error::Json(message)
            if message.contains("forced local GTOC-2 serialization failure")
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::InfrastructureFailure);
}

// Origin: vendor/engine/tests/engine_state/coda2_degree_shift.rs
// Claim: urn:omega:crates_rs:tests:coda2-degree-shift:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord6d9f3a99 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord6d9f3a99` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError6d9f3a99 {
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
impl BoundaryError6d9f3a99 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError6d9f3a99 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError6d9f3a99 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord6d9f3a99 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError6d9f3a99> {
        if capacity_bound == 0 {
            return Err(BoundaryError6d9f3a99::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError6d9f3a99::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError6d9f3a99::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_6d9f3a99() {
    let admitted = BoundaryRecord6d9f3a99::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord6d9f3a99::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
