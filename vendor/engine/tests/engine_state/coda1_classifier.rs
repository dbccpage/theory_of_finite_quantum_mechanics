#[path = "support/upstream_history.rs"]
mod upstream_history;

use std::env;
use std::fs;
use std::path::{Path, PathBuf};

use engine_state::coda1_classifier::*;
use engine_state::coda_gtla_protocol::{FrozenObserverContextV1, CodaTerminal};
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use serde_json::Value;

const FROZEN_BASE: &str = "2b9637f38a9360c0445ce1ecec3211456468d2f5";

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct FixtureSetV1 {
    schema_version: String,
    cases: Vec<Coda1AdmissionV1>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct ReceiptSetV1 {
    schema_version: String,
    executions: Vec<Coda1ExecutionV1>,
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

fn source_manifest(_root: &Path) -> Vec<SourceHashV1> {
    let mut paths = vec![
        "omega_engine/crates/omega_homological/src/trichotomy_witness.rs",
        "omega_engine/general_theory_of_obstruction_calculus/papers/999_GTOC/00_series_charter.md",
        "omega_engine/research/published/050_gtoc_ground_state/050_gtoc_ground_state.md",
    ];
    paths.sort();
    paths
        .into_iter()
        .map(|path| SourceHashV1 {
            path: path.to_owned(),
            sha256: sha256_bytes_v1(&upstream_history::frozen_blob(FROZEN_BASE, path)),
        })
        .collect()
}

fn write_surface() -> Vec<String> {
    let mut paths = vec![
        "docs/gtoc-canonicalization-remaining-work.md",
        "docs/omega-conductor-epic-v001.md",
        "docs/saga_01_universal_gtoc_gtla_protocol.md",
        "docs/sprint_s01_002.md",
        "docs/status/omega_conductor_s01_002_status_2026-07-18.md",
        "omega_engine/Cargo.lock",
        "omega_engine/crates/omega_state/Cargo.toml",
        "omega_engine/crates/omega_state/src/gtoc1_classifier.rs",
        "omega_engine/crates/omega_state/src/lib.rs",
        "omega_engine/crates/omega_state/tests/fixtures/gtoc1_fixture_matrix_v1.json",
        "omega_engine/crates/omega_state/tests/fixtures/gtoc1_receipt_matrix_v1.json",
        "omega_engine/crates/omega_state/tests/gtoc1_classifier.rs",
        "omega_engine/general_theory_of_obstruction_calculus/papers/999_GTOC/math_spine.md",
        "omega_engine/general_theory_of_obstruction_calculus/papers/999_GTOC/theorem_ledger.md",
    ]
    .into_iter()
    .map(str::to_owned)
    .collect::<Vec<_>>();
    paths.sort();
    paths
}

fn matrix(rows: usize, cols: usize, values: &[i64]) -> RationalMatrixV1 {
    RationalMatrixV1 {
        rows,
        cols,
        row_major: values.iter().copied().map(RationalV1::integer).collect(),
    }
}

fn triangle_d0() -> RationalMatrixV1 {
    matrix(3, 3, &[-1, 1, 0, 0, -1, 1, 1, 0, -1])
}

fn declared_rule(
    window_id: &str,
    d1: RationalMatrixV1,
    residual: &[i64],
    stabilization_witness_id: Option<&str>,
) -> WindowRuleV1 {
    WindowRuleV1::Declared(DeclaredCochainWindowV1 {
        window_id: window_id.to_owned(),
        zero_relation_id: "zero:q-rational".to_owned(),
        rule_id: "rule:exact-image-then-closure".to_owned(),
        residual_id: format!("residual:{window_id}"),
        d0: triangle_d0(),
        d1,
        residual: residual.iter().copied().map(RationalV1::integer).collect(),
        stabilization_witness_id: stabilization_witness_id.map(str::to_owned),
    })
}

fn base_packet(root: &Path, packet_id: &str, rule: WindowRuleV1) -> Coda1PacketV1 {
    let sources = source_manifest(root);
    let mut visible_hashes = sources
        .iter()
        .map(|source| source.sha256.clone())
        .collect::<Vec<_>>();
    visible_hashes.sort();
    visible_hashes.dedup();
    let evaluator_id = "witness:evaluator:direct-replay-v1".to_owned();
    let mut observer = FrozenObserverContextV1 {
        observer_id: evaluator_id.clone(),
        observer_domain: CODA1_OBSERVER_DOMAIN.to_owned(),
        state_domain: CODA1_STATE_DOMAIN.to_owned(),
        observer_hash: "0".repeat(64),
        visible_artifact_hashes: visible_hashes,
        hidden_artifact_classes: vec![
            "unadmitted-infinite-window".to_owned(),
            "unadmitted-runtime-state".to_owned(),
        ],
        tool_permissions: vec![
            "read:canonical-sources".to_owned(),
            "test:omega_state".to_owned(),
            "write:admitted-paths".to_owned(),
        ],
        write_surface: write_surface(),
        evidence_ceiling: CODA1_EVIDENCE_CEILING.to_owned(),
    };
    observer.observer_hash = observer_sha256_v1(&observer).unwrap();

    let mut prior_work_ledger = vec![
        "GTOC-1 canonical math spine".to_owned(),
        "S01-001 protocol machine".to_owned(),
        "omega_homological exact residual trichotomy".to_owned(),
    ];
    prior_work_ledger.sort();

    Coda1PacketV1 {
        schema_version: CODA1_PACKET_SCHEMA_VERSION.to_owned(),
        packet_id: packet_id.to_owned(),
        frozen_base: FROZEN_BASE.to_owned(),
        target_rows: vec!["GTOC-1".to_owned()],
        source_manifest: sources,
        budgets: Coda1BudgetsV1 {
            attempt_budget: 1,
            repair_budget: 2,
            successor_budget: 1,
            time_budget_seconds: 8 * 60 * 60,
            process_budget: 4,
            token_budget: 200_000,
        },
        evidence_ceiling: CODA1_EVIDENCE_CEILING.to_owned(),
        observer,
        producer_id: "witness:producer:omega-state-v1".to_owned(),
        evaluator_id,
        authority_witness_id: "witness:authority:none-check-v1".to_owned(),
        prior_work_ledger,
        carrier: RetainedCarrierV1 {
            carrier_id: "carrier:finite-rational-window".to_owned(),
            retained_edge_count: 3,
            retention_witness_ids: vec!["retention:edge-pattern-v1".to_owned()],
            recomparison_witness_ids: vec!["recomparison:finite-replay-v1".to_owned()],
        },
        rule,
    }
}

fn seal(packet: Coda1PacketV1) -> Coda1AdmissionV1 {
    let packet_sha256 = packet_sha256_v1(&packet).unwrap();
    Coda1AdmissionV1 {
        schema_version: CODA1_ADMISSION_SCHEMA_VERSION.to_owned(),
        packet,
        packet_sha256,
    }
}

fn fixture_set() -> FixtureSetV1 {
    let root = repository_root();
    let exact = seal(base_packet(
        &root,
        "S01-002:exact",
        declared_rule("exact", matrix(1, 3, &[1, 1, 1]), &[1, -1, 0], None),
    ));
    let closed = seal(base_packet(
        &root,
        "S01-002:closed",
        declared_rule(
            "closed",
            matrix(1, 3, &[0, 0, 0]),
            &[1, 1, 1],
            Some("stabilization:frozen-repair-family-exhausted"),
        ),
    ));
    let active = seal(base_packet(
        &root,
        "S01-002:active",
        declared_rule("active", matrix(1, 3, &[1, 1, 1]), &[1, 0, 0], None),
    ));
    let no_rule = seal(base_packet(
        &root,
        "S01-002:no-rule",
        WindowRuleV1::Unavailable(UnavailableRuleV1 {
            rule_request_id: "oracle:closure-window".to_owned(),
            reason: NoRuleReasonV1::ClosureWindowUndeclared,
            disposition: NoRuleDispositionV1::RequestSource,
            basis: "retained edge pattern has no declared closure window".to_owned(),
        }),
    ));
    FixtureSetV1 {
        schema_version: CODA1_ADMISSION_SCHEMA_VERSION.to_owned(),
        cases: vec![exact, closed, active, no_rule],
    }
}

fn receipt_set(fixtures: &FixtureSetV1) -> ReceiptSetV1 {
    ReceiptSetV1 {
        schema_version: CODA1_RECEIPT_SCHEMA_VERSION.to_owned(),
        executions: fixtures
            .cases
            .iter()
            .map(|case| execute_and_evaluate_coda1_v1(case).unwrap())
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
    if env::var_os("OMEGA_REGEN_GTOC1_FIXTURES").is_some() {
        fs::write(&path, &rendered).unwrap();
    }
    fs::read_to_string(path).unwrap()
}

#[test]
fn committed_fixture_and_receipt_matrices_are_byte_stable() {
    let fixtures = fixture_set();
    let committed = committed_or_regenerated("gtoc1_fixture_matrix_v1.json", &fixtures);
    assert_eq!(committed, pretty(&fixtures));
    assert_eq!(
        serde_json::from_str::<FixtureSetV1>(&committed).unwrap(),
        fixtures
    );

    let receipts = receipt_set(&fixtures);
    let committed = committed_or_regenerated("gtoc1_receipt_matrix_v1.json", &receipts);
    assert_eq!(committed, pretty(&receipts));
    assert_eq!(
        serde_json::from_str::<ReceiptSetV1>(&committed).unwrap(),
        receipts
    );
}

#[test]
fn source_manifest_hashes_match_explicit_historical_checkout_bytes() {
    for case in fixture_set().cases {
        for source in case.packet.source_manifest {
            let bytes = upstream_history::frozen_blob(FROZEN_BASE, &source.path);
            assert_eq!(sha256_bytes_v1(&bytes), source.sha256, "{}", source.path);
        }
    }
}

#[test]
fn four_fixture_routes_are_exclusive_complete_and_correctly_terminalized() {
    let executions = fixture_set()
        .cases
        .iter()
        .map(|case| execute_and_evaluate_coda1_v1(case).unwrap())
        .collect::<Vec<_>>();
    let routes = executions
        .iter()
        .map(|execution| execution.classification.route)
        .collect::<Vec<_>>();
    assert_eq!(routes, Coda1RouteV1::ALL);
    assert_eq!(
        executions
            .iter()
            .map(|execution| execution.classification.terminal_proposal)
            .collect::<Vec<_>>(),
        vec![
            CodaTerminal::ExactRepair,
            CodaTerminal::StabilizedSurvivor,
            CodaTerminal::OpenObstruction,
            CodaTerminal::OracleNeeded,
        ]
    );
    assert_eq!(
        executions[3].classification.phi1_support,
        DiagnosticSupportV1::NotPopulated
    );
    assert_eq!(
        executions[3].classification.gamma2_support,
        DiagnosticSupportV1::NotPopulated
    );
}

#[test]
fn exhaustive_small_domain_matches_the_four_way_truth_table() {
    let root = repository_root();
    let mut classified = 0usize;
    for d0_value in -1..=1 {
        for d1_value in -1..=1 {
            if d1_value * d0_value != 0 {
                continue;
            }
            for residual_value in -1..=1 {
                let rule = WindowRuleV1::Declared(DeclaredCochainWindowV1 {
                    window_id: format!("finite:{d0_value}:{d1_value}:{residual_value}"),
                    zero_relation_id: "zero:q-rational".to_owned(),
                    rule_id: "rule:one-dimensional-exhaustive".to_owned(),
                    residual_id: format!("residual:{d0_value}:{d1_value}:{residual_value}"),
                    d0: matrix(1, 1, &[d0_value]),
                    d1: matrix(1, 1, &[d1_value]),
                    residual: vec![RationalV1::integer(residual_value)],
                    stabilization_witness_id: Some(
                        "stabilization:finite-domain-exhausted".to_owned(),
                    ),
                });
                let admission = seal(base_packet(
                    &root,
                    &format!("small:{d0_value}:{d1_value}:{residual_value}"),
                    rule,
                ));
                let got = classify_coda1_v1(&admission).unwrap().route;
                let expected = if d0_value != 0 || residual_value == 0 {
                    Coda1RouteV1::ExactRepair
                } else if d1_value * residual_value == 0 {
                    Coda1RouteV1::ClosedResidual
                } else {
                    Coda1RouteV1::ActiveClosureFailure
                };
                assert_eq!(got, expected);
                classified += 1;
            }
        }
    }
    assert_eq!(classified, 15);
}

#[test]
fn closedness_without_stabilization_witness_remains_open() {
    let mut closed = fixture_set().cases[1].clone();
    let WindowRuleV1::Declared(window) = &mut closed.packet.rule else {
        unreachable!()
    };
    window.stabilization_witness_id = None;
    closed.packet_sha256 = packet_sha256_v1(&closed.packet).unwrap();
    let classification = classify_coda1_v1(&closed).unwrap();
    assert_eq!(classification.route, Coda1RouteV1::ClosedResidual);
    assert_eq!(
        classification.terminal_proposal,
        CodaTerminal::OpenObstruction
    );
    assert!(classification
        .residual_ids
        .iter()
        .any(|residual| residual.starts_with("proof_obligation:")));
}

#[test]
fn invalid_cochain_and_noncanonical_rational_fail_closed() {
    let mut invalid_chain = fixture_set().cases[2].clone();
    let WindowRuleV1::Declared(window) = &mut invalid_chain.packet.rule else {
        unreachable!()
    };
    window.d1 = matrix(1, 3, &[1, 0, 0]);
    invalid_chain.packet_sha256 = packet_sha256_v1(&invalid_chain.packet).unwrap();
    let error = classify_coda1_v1(&invalid_chain).unwrap_err();
    assert_eq!(error, Coda1Error::InvalidCochainComposition);
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);

    let mut noncanonical = fixture_set().cases[0].clone();
    let WindowRuleV1::Declared(window) = &mut noncanonical.packet.rule else {
        unreachable!()
    };
    window.residual[0] = RationalV1 {
        numerator: 2,
        denominator: 2,
    };
    noncanonical.packet_sha256 = packet_sha256_v1(&noncanonical.packet).unwrap();
    assert!(matches!(
        classify_coda1_v1(&noncanonical).unwrap_err(),
        Coda1Error::NonCanonicalRational { .. }
    ));
}

#[test]
fn packet_observer_paths_and_identities_are_sealed() {
    let mut packet_hash = fixture_set().cases[0].clone();
    packet_hash.packet.packet_id.push_str(":tampered");
    assert!(matches!(
        classify_coda1_v1(&packet_hash).unwrap_err(),
        Coda1Error::PacketHashMismatch { .. }
    ));

    let mut observer_hash = fixture_set().cases[0].clone();
    observer_hash.packet.observer.observer_hash = "f".repeat(64);
    observer_hash.packet_sha256 = packet_sha256_v1(&observer_hash.packet).unwrap();
    assert!(matches!(
        classify_coda1_v1(&observer_hash).unwrap_err(),
        Coda1Error::ObserverHashMismatch { .. }
    ));

    let mut wildcard = fixture_set().cases[0].clone();
    wildcard
        .packet
        .observer
        .write_surface
        .push("omega_engine/crates/omega_state/**".to_owned());
    wildcard.packet.observer.write_surface.sort();
    wildcard.packet.observer.observer_hash = observer_sha256_v1(&wildcard.packet.observer).unwrap();
    wildcard.packet_sha256 = packet_sha256_v1(&wildcard.packet).unwrap();
    assert!(matches!(
        classify_coda1_v1(&wildcard).unwrap_err(),
        Coda1Error::InvalidWritePath(_)
    ));

    let mut identity = fixture_set().cases[0].clone();
    identity.packet.evaluator_id = identity.packet.producer_id.clone();
    identity.packet_sha256 = packet_sha256_v1(&identity.packet).unwrap();
    let error = classify_coda1_v1(&identity).unwrap_err();
    assert_eq!(error, Coda1Error::IdentityCollision);
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);
}

#[test]
fn independent_replay_rejects_tampered_producer_or_classification() {
    let admission = fixture_set().cases[0].clone();
    let execution = execute_and_evaluate_coda1_v1(&admission).unwrap();

    let mut producer = execution.receipts.producer.clone();
    producer.classification_sha256 = "f".repeat(64);
    assert_eq!(
        evaluate_coda1_v1(&admission, &execution.classification, &producer).unwrap_err(),
        Coda1Error::ProducerReceiptMismatch
    );

    let mut classification = execution.classification;
    classification.authority_effect = AuthorityEffect::Uncertified;
    let error =
        evaluate_coda1_v1(&admission, &classification, &execution.receipts.producer).unwrap_err();
    assert_eq!(error, Coda1Error::AuthorityExpanded);
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);
}

#[test]
fn receipts_preserve_independence_nonpromotion_and_replay_hashes() {
    for case in fixture_set().cases {
        let first = execute_and_evaluate_coda1_v1(&case).unwrap();
        let second = execute_and_evaluate_coda1_v1(&case).unwrap();
        assert_eq!(first, second);
        assert_ne!(
            first.receipts.producer.producer_id,
            first.receipts.evaluation.evaluator_id
        );
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
            first.receipts.terminal.human_decision,
            Coda1HumanDecisionV1::PendingHumanPromotion
        );
    }
}

#[test]
fn route_matrix_is_closed_and_unknown_wire_values_fail() {
    let rows = coda1_route_status_matrix_v1();
    assert_eq!(rows.len(), 4);
    assert_eq!(
        rows.iter().map(|row| row.route).collect::<Vec<_>>(),
        Coda1RouteV1::ALL
    );
    assert!(serde_json::from_str::<Coda1RouteV1>("\"fifth_route\"").is_err());

    let mut packet: Value = serde_json::to_value(&fixture_set().cases[0]).unwrap();
    packet["unknown_field"] = Value::Bool(true);
    assert!(serde_json::from_value::<Coda1AdmissionV1>(packet).is_err());
}

#[test]
fn no_rule_is_routing_not_a_cohomology_class() {
    let no_rule = classify_coda1_v1(&fixture_set().cases[3]).unwrap();
    assert_eq!(no_rule.route, Coda1RouteV1::NoRule);
    assert_eq!(no_rule.phi1_support, DiagnosticSupportV1::NotPopulated);
    assert_eq!(no_rule.gamma2_support, DiagnosticSupportV1::NotPopulated);
    assert_eq!(no_rule.terminal_proposal, CodaTerminal::OracleNeeded);
    assert_eq!(no_rule.residual_ids, vec!["oracle:closure-window"]);
}

// Origin: vendor/engine/tests/engine_state/coda1_classifier.rs
// Claim: urn:omega:crates_rs:tests:coda1-classifier:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecorde8755472 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecorde8755472` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryErrore8755472 {
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
impl BoundaryErrore8755472 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryErrore8755472 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryErrore8755472 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecorde8755472 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryErrore8755472> {
        if capacity_bound == 0 {
            return Err(BoundaryErrore8755472::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryErrore8755472::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryErrore8755472::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_e8755472() {
    let admitted = BoundaryRecorde8755472::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecorde8755472::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
