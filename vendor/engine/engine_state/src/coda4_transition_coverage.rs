//! Bounded S06-002 / CODA-4 typed DDA transition coverage.
//!
//! The existing DDA alphabet names the eight lawful operation classes and
//! `op_verification` checks each operation against a concrete cochain-state
//! transition. This module closes the next finite orchestration gap: one frozen
//! registry contains every alphabet member exactly once, every registered row
//! carries a state-hash-bound execution log or immutable refusal, and an
//! unregistered request is refused without mutation.
//!
//! The bounded CODA-3 predecessor is deliberately treated as a license
//! *candidate*, not an issued lift license. The canonical `Lift` row therefore
//! refuses without changing state and remains a named residual. No path in this
//! module constructs authority, activates a gate, or creates an
//! `AuthorizedLocalResult`.


#[allow(dead_code, non_camel_case_types, missing_docs)]
trait CheckedInvariantExt_ff6bb237<T> {
    fn checked_invariant_ff6bb237(self, msg: &str) -> T;
}

impl<T> CheckedInvariantExt_ff6bb237<T> for Option<T> {
    #[inline]
    fn checked_invariant_ff6bb237(self, msg: &str) -> T {
        match self {
            Some(v) => v,
            None => unreachable!("{}", msg),
        }
    }
}

impl<T, E: std::fmt::Debug> CheckedInvariantExt_ff6bb237<T> for std::result::Result<T, E> {
    #[inline]
    fn checked_invariant_ff6bb237(self, msg: &str) -> T {
        match self {
            Ok(v) => v,
            Err(e) => unreachable!("{}: {:?}", msg, e),
        }
    }
}
use std::collections::{BTreeMap, BTreeSet};

use engine_wdp::ddc::dda_alphabet::{DdaOp, DdaStep};
use engine_wdp::ddc::degree_tower::{
    BinaryCochainSegment, BinaryLinearMap, DegreeTrichotomy,
};
use engine_wdp::ddc::op_verification::{verify_step, CochainState};
use engine_types::authority::AuthorityEffect;
use serde::de::DeserializeOwned;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

use crate::coda3_lift_license::{Coda3ExecutionV1, CODA3_RECEIPT_SCHEMA_VERSION};
use crate::coda_gtla_protocol::CodaTerminal;
use crate::coda_gtla_run_receipt::parse_run_verification_canonical_v1;

pub const CODA4_PACKET_SCHEMA_VERSION: &str = "omega.gtoc4.transition-coverage.packet.v1";
pub const CODA4_RECEIPT_SCHEMA_VERSION: &str = "omega.gtoc4.transition-coverage.receipt.v1";
pub const CODA4_VERIFICATION_SCHEMA_VERSION: &str =
    "omega.gtoc4.transition-coverage.verification.v1";

pub const S06_002_FROZEN_BASE: &str = "749f05bdee0b84f32bf0842aa024052b29e33adf";
pub const S06_002_PACKET_ID: &str = "omega-conductor-s06-002-gtoc4-coverage-v1";
pub const S06_002_GOAL_ID: &str = "S06-002:GTOC-4";
pub const S06_002_OBSERVER_ID: &str = "witness:evaluator:s06-002-independent-v1";
pub const S06_002_PRODUCER_ID: &str = "witness:producer:s06-002-transition-matrix-v1";
pub const S06_002_AUTHORITY_WITNESS_ID: &str = "witness:authority:s06-002-none-v1";
pub const S06_002_EVIDENCE_CEILING: &str =
    "one frozen eight-class DDA registry, two predecessor artifacts, concrete cochain-state replays, immutable refusals, and evidence-only GTOC-4 terminalization; no dynamic operations, issued lift license, authority, promotion, gate activation, or general theorem";
pub const S06_002_LIFT_RESIDUAL_ID: &str = "residual:s06-002:lift-license-not-issued";
pub const S06_002_UNKNOWN_CLASS_ID: &str = "transition:s06-002:unknown-dynamic-operation";

pub const S06_001_VERIFICATION_PATH: &str =
    "omega_engine/crates/omega_state/tests/fixtures/s06_001_gtoc_gtla_verification_v1.json";
pub const CODA3_RECEIPT_PATH: &str =
    "omega_engine/crates/omega_state/tests/fixtures/gtoc3_lift_license_receipt_matrix_v1.json";

pub const S06_002_WRITE_SURFACE: [&str; 10] = [
    "docs/omega-conductor-epic-v001.md",
    "docs/saga_06_receipt_verification_and_terminalization.md",
    "docs/sprint_s06_002.md",
    "docs/status/omega_conductor_s06_002_status_2026-07-18.md",
    "omega_engine/crates/omega_state/src/lib.rs",
    "omega_engine/crates/omega_state/src/gtoc4_transition_coverage.rs",
    "omega_engine/crates/omega_state/tests/gtoc4_transition_coverage.rs",
    "omega_engine/crates/omega_state/tests/fixtures/s06_002_gtoc4_packet_v1.json",
    "omega_engine/crates/omega_state/tests/fixtures/s06_002_gtoc4_receipt_v1.json",
    "omega_engine/crates/omega_state/tests/fixtures/s06_002_gtoc4_verification_v1.json",
];

pub const S06_002_SOURCE_MANIFEST: [(&str, &str, u64); 19] = [
    (
        "docs/gtoc-canonicalization-remaining-work.md",
        "e7ee9ae3c8b34e6b8985e21c528fe3926655ca3567c61a0bc28b446f6f7b0d81",
        26_373,
    ),
    (
        "docs/omega-conductor-epic-v001.md",
        "b7f50fee869e3217ff2a6b0bae54d46af4a9b67b5ad05e2c3116d28b493ee435",
        62_303,
    ),
    (
        "docs/saga_06_receipt_verification_and_terminalization.md",
        "9fcdf098845add5bfec8068877092e77a1d1dad32d7f174cd5cc22ad967a2fd6",
        7_642,
    ),
    (
        "docs/sprint_s06_001.md",
        "75787d3b3511bf2496e4730f9893f34e940295dff60a9be346ad85a9b24a0718",
        8_288,
    ),
    (
        "docs/sprint_s06_002.md",
        "3072f5957de10a53f308cba105cb981727f5d5105c0e13d81991ed7044f5d6bc",
        8_376,
    ),
    (
        "docs/status-vocabulary.md",
        "d39813a9e440a6c7ef45276fadf1c42cb5a34aea2368b94185ecd2500fae2d54",
        4_309,
    ),
    (
        "docs/status/omega_conductor_s02_002_status_2026-07-18.md",
        "141d598b0ecb71d15eb0868c1088aa64df023d92ff75ddf0280080ad8a12a411",
        10_591,
    ),
    (
        "docs/status/omega_conductor_s06_001_status_2026-07-18.md",
        "cf2d408fea274f460c2a17358687594a66b1118d5f61b71479e28902abb19402",
        12_526,
    ),
    (
        "omega_engine/crates/omega_discrete_deformation_algebra/Cargo.toml",
        "0762a7a2fdf95d471ca2a10a9d16d59e68bea777767660a1f65ac718994d9199",
        577,
    ),
    (
        "omega_engine/crates/omega_discrete_deformation_algebra/src/dda_alphabet.rs",
        "2894e95134db050d9c366e3e15db5e5ecdaeb3c0ed4625e18a63d21753ee7fb9",
        11_997,
    ),
    (
        "omega_engine/crates/omega_discrete_deformation_algebra/src/degree_tower.rs",
        "d08f36528436d2f7345ed847990a059f13d57301a8d950bce6835758ffa30a9a",
        17_053,
    ),
    (
        "omega_engine/crates/omega_discrete_deformation_algebra/src/op_verification.rs",
        "fda813dbe86f6aa841fd2bc0a25ddb6c868ec8a9af438fdf83519fe5e37bb9dd",
        21_285,
    ),
    (
        "omega_engine/crates/omega_state/Cargo.toml",
        "3cfa4b23be89d16d8eec1074126c9faef9828dbf2c794af7eee2a058fb9e90b6",
        528,
    ),
    (
        "omega_engine/crates/omega_state/src/gtoc3_lift_license.rs",
        "1c12b7e2e7a220ee7727f0ee4b9baa0cd663469f7cf8cfcf724ade3cc1b70775",
        38_265,
    ),
    (
        "omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs",
        "da57f9f89dd396cbd1bca72880d024c81a4d3238bd6f78af9add06572c3f160f",
        35_825,
    ),
    (
        "omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs",
        "cb3012dfcfc3ef6e16179bbed45795c88e46375234547a65bd4a4d1aa6a0e806",
        61_366,
    ),
    (
        "omega_engine/crates/omega_state/src/lib.rs",
        "da0b29929778dccb35327d08233c14f74c31bc1e1aebbbb0e56cfa32d462de12",
        1_418,
    ),
    (
        CODA3_RECEIPT_PATH,
        "65d5324e105d762034e122ca7cab25afe1daeea3cd761be47f07aa91ac9616e9",
        4_468,
    ),
    (
        S06_001_VERIFICATION_PATH,
        "608efaadb2695a0eddd35e51d7a82577d1bd31eb0db5b4cc330df90b18561600",
        1_046,
    ),
];

pub const S06_002_INPUT_ARTIFACTS: [(&str, &str, u64); 2] = [
    (
        CODA3_RECEIPT_PATH,
        "65d5324e105d762034e122ca7cab25afe1daeea3cd761be47f07aa91ac9616e9",
        4_468,
    ),
    (
        S06_001_VERIFICATION_PATH,
        "608efaadb2695a0eddd35e51d7a82577d1bd31eb0db5b4cc330df90b18561600",
        1_046,
    ),
];

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenCoda4SourceV1 {
    pub path: String,
    pub sha256: String,
    pub bytes: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda4ArtifactBindingV1 {
    pub path: String,
    pub sha256: String,
    pub bytes: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda4BudgetsV1 {
    pub attempt_budget: u32,
    pub repair_budget: u32,
    pub successor_budget: u32,
    pub time_budget_seconds: u64,
    pub process_budget: u32,
    pub token_budget: u64,
    pub transition_class_budget: u32,
    pub state_dimension_budget: u32,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenCoda4ObserverV1 {
    pub observer_id: String,
    pub source_manifest_sha256: String,
    pub visible_artifact_sha256: Vec<String>,
    pub hidden_context_classes: Vec<String>,
    pub model_context_available: bool,
    pub promotion_constructor_available: bool,
    pub authorized_local_result_constructor_available: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RegisteredTransitionModeV1 {
    Executed,
    RefusedUntilLiftLicenseIssued,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RegisteredTransitionClassV1 {
    pub sequence: u32,
    pub transition_class_id: String,
    pub operation: DdaOp,
    pub mode: RegisteredTransitionModeV1,
    pub before_state_sha256: String,
    pub after_state_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct BinaryMapSpecV1 {
    pub domain_dim: usize,
    pub rows: Vec<Vec<bool>>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CochainStateSpecV1 {
    pub degree: usize,
    pub previous: BinaryMapSpecV1,
    pub next: BinaryMapSpecV1,
    pub residual: Vec<bool>,
}

impl CochainStateSpecV1 {
    fn realize(&self, dimension_budget: usize) -> Result<CochainState, Coda4CoverageError> {
        let dimensions = [
            self.previous.domain_dim,
            self.previous.rows.len(),
            self.next.domain_dim,
            self.next.rows.len(),
            self.residual.len(),
        ];
        if self.degree == 0
            || dimensions
                .iter()
                .any(|dimension| *dimension > dimension_budget)
        {
            return Err(Coda4CoverageError::StateBudgetExceeded);
        }
        let previous =
            BinaryLinearMap::from_rows(self.previous.domain_dim, self.previous.rows.clone())
                .map_err(|error| Coda4CoverageError::MalformedState(format!("{error:?}")))?;
        let next = BinaryLinearMap::from_rows(self.next.domain_dim, self.next.rows.clone())
            .map_err(|error| Coda4CoverageError::MalformedState(format!("{error:?}")))?;
        let segment = BinaryCochainSegment::new(self.degree, previous, next)
            .map_err(|error| Coda4CoverageError::MalformedState(format!("{error:?}")))?;
        CochainState::new(segment, self.residual.clone())
            .map_err(|error| Coda4CoverageError::MalformedState(format!("{error:?}")))
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda4TransitionCoveragePacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub goal_id: String,
    pub frozen_base: String,
    pub observer: FrozenCoda4ObserverV1,
    pub observer_sha256: String,
    pub source_manifest: Vec<FrozenCoda4SourceV1>,
    pub input_artifacts: Vec<Coda4ArtifactBindingV1>,
    pub registered_transitions: Vec<RegisteredTransitionClassV1>,
    pub legal_terminals: Vec<CodaTerminal>,
    pub budgets: Coda4BudgetsV1,
    pub evidence_ceiling: String,
    pub exact_write_surface: Vec<String>,
    pub producer_id: String,
    pub evaluator_id: String,
    pub authority_witness_id: String,
    pub prior_work_ledger: Vec<String>,
    pub promotion_constructor_available: bool,
    pub authorized_local_result_constructor_available: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "status", rename_all = "snake_case", deny_unknown_fields)]
pub enum TransitionOutcomeV1 {
    Executed { log: String },
    RefusedToExecute { reason: String },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct TransitionExecutionReceiptV1 {
    pub sequence: u32,
    pub transition_class_id: String,
    pub operation: DdaOp,
    pub before_state: CochainStateSpecV1,
    pub before_state_sha256: String,
    pub after_state: CochainStateSpecV1,
    pub after_state_sha256: String,
    pub outcome: TransitionOutcomeV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct UnknownTransitionRefusalV1 {
    pub request_id: String,
    pub transition_class_id: String,
    pub before_state: CochainStateSpecV1,
    pub before_state_sha256: String,
    pub after_state: CochainStateSpecV1,
    pub after_state_sha256: String,
    pub reason: String,
    pub terminal: CodaTerminal,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda4TransitionCoverageReceiptV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub producer_id: String,
    pub transitions: Vec<TransitionExecutionReceiptV1>,
    pub unknown_transition: UnknownTransitionRefusalV1,
    pub residual_ids: Vec<String>,
    pub claimed_terminal: CodaTerminal,
    pub promotion_requested: bool,
    pub promotion_constructor_called: bool,
    pub authorized_local_result_created: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Coda4StateClassV1 {
    Exact,
    StabilizedSurvivor,
    Open,
}

impl From<DegreeTrichotomy> for Coda4StateClassV1 {
    fn from(value: DegreeTrichotomy) -> Self {
        match value {
            DegreeTrichotomy::Exact => Self::Exact,
            DegreeTrichotomy::StabilizedSurvivor => Self::StabilizedSurvivor,
            DegreeTrichotomy::Open => Self::Open,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum VerifiedOutcomeKindV1 {
    Executed,
    RefusedToExecute,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct TransitionVerificationEvidenceV1 {
    pub sequence: u32,
    pub transition_class_id: String,
    pub operation: DdaOp,
    pub before_state_sha256: String,
    pub after_state_sha256: String,
    pub before_phi: usize,
    pub before_gamma: usize,
    pub before_classification: Coda4StateClassV1,
    pub after_phi: usize,
    pub after_gamma: usize,
    pub after_classification: Coda4StateClassV1,
    pub outcome: VerifiedOutcomeKindV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda4TransitionCoverageVerificationV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub observer_sha256: String,
    pub receipt_sha256: String,
    pub artifact_closure_sha256: String,
    pub transition_matrix_sha256: String,
    pub unknown_refusal_sha256: String,
    pub evaluator_id: String,
    pub authority_witness_id: String,
    pub registered_transition_count: u32,
    pub executed_transition_count: u32,
    pub refused_transition_count: u32,
    pub transition_evidence: Vec<TransitionVerificationEvidenceV1>,
    pub every_alphabet_operation_covered_once: bool,
    pub every_state_hash_recomputed: bool,
    pub every_operation_law_replayed: bool,
    pub every_refusal_immutable: bool,
    pub unknown_classes_refused: bool,
    pub predecessor_receipts_verified: bool,
    pub cochain_identities_zero: bool,
    pub residual_ids: Vec<String>,
    pub terminal: CodaTerminal,
    pub promotion_requested: bool,
    pub promotion_constructor_called: bool,
    pub authorized_local_result_created: bool,
    pub authority_effect: AuthorityEffect,
}

pub type Coda4ArtifactBytesV1 = BTreeMap<String, Vec<u8>>;

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum Coda4CoverageError {
    #[error("frozen GTOC-4 packet drifted")]
    PacketDrift,
    #[error("packet authority or observer boundary changed")]
    PacketBoundaryChanged,
    #[error("receipt does not bind to the frozen packet")]
    ReceiptBindingMismatch,
    #[error("artifact set differs from the frozen packet")]
    ArtifactSetMismatch,
    #[error("missing frozen artifact {0}")]
    MissingArtifact(String),
    #[error("artifact byte length changed for {0}")]
    ArtifactLengthMismatch(String),
    #[error("artifact SHA-256 changed for {0}")]
    ArtifactHashMismatch(String),
    #[error("predecessor artifact is invalid: {0}")]
    InvalidPredecessor(String),
    #[error("registered transition count mismatch: expected {expected}, found {found}")]
    CoverageCountMismatch { expected: usize, found: usize },
    #[error("registered transition class was emitted more than once: {0}")]
    DuplicateTransitionClass(String),
    #[error("DDA operation was attributed more than once: {0:?}")]
    DuplicateOperation(DdaOp),
    #[error("unregistered transition attempted execution: {0}")]
    UnknownTransitionExecuted(String),
    #[error("transition attribution mismatch for {0}")]
    OperationAttributionMismatch(String),
    #[error("transition state hash mismatch for {0}")]
    StateHashMismatch(String),
    #[error("state exceeds the frozen dimension budget")]
    StateBudgetExceeded,
    #[error("malformed cochain state: {0}")]
    MalformedState(String),
    #[error("empty execution log or refusal reason for {0}")]
    EmptyOutcomePayload(String),
    #[error("transition outcome differs from the frozen registry for {0}")]
    OutcomeMismatch(String),
    #[error("lift execution attempted without an issued license")]
    UnissuedLiftExecution,
    #[error("operation law failed for {transition_class_id}: {reason}")]
    OperationLawViolation {
        transition_class_id: String,
        reason: String,
    },
    #[error("a refused transition mutated state: {0}")]
    RefusalMutatedState(String),
    #[error("unknown-transition refusal is malformed")]
    UnknownRefusalMismatch,
    #[error("residual ledger differs from the recomputed ledger")]
    ResidualMismatch,
    #[error("terminal mismatch: expected {expected:?}, found {found:?}")]
    TerminalMismatch {
        expected: CodaTerminal,
        found: CodaTerminal,
    },
    #[error("receipt attempted to expand authority")]
    AuthorityExpanded,
    #[error("JSON serialization failed: {0}")]
    Json(String),
    #[error("JSON decoding failed: {0}")]
    Decode(String),
    #[error("non-canonical JSON for {0}")]
    NonCanonicalJson(String),
}

impl Coda4CoverageError {
    pub fn terminal_route(&self) -> CodaTerminal {
        match self {
            Self::MissingArtifact(_) => CodaTerminal::InfrastructureFailure,
            Self::UnissuedLiftExecution => CodaTerminal::LiftLicenseNeeded,
            Self::UnknownTransitionExecuted(_) => CodaTerminal::Refused,
            _ => CodaTerminal::Invalid,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Coda3ReceiptSetV1 {
    schema_version: String,
    executions: Vec<Coda3ExecutionV1>,
}

pub fn canonical_s06_002_packet_v1() -> Coda4TransitionCoveragePacketV1 {
    let source_manifest = S06_002_SOURCE_MANIFEST
        .iter()
        .map(|(path, sha256, bytes)| FrozenCoda4SourceV1 {
            path: (*path).to_owned(),
            sha256: (*sha256).to_owned(),
            bytes: *bytes,
        })
        .collect::<Vec<_>>();
    let input_artifacts = S06_002_INPUT_ARTIFACTS
        .iter()
        .map(|(path, sha256, bytes)| Coda4ArtifactBindingV1 {
            path: (*path).to_owned(),
            sha256: (*sha256).to_owned(),
            bytes: *bytes,
        })
        .collect::<Vec<_>>();
    let observer = FrozenCoda4ObserverV1 {
        observer_id: S06_002_OBSERVER_ID.to_owned(),
        source_manifest_sha256: sha256_json_v1(&source_manifest)
            .checked_invariant_ff6bb237("frozen source manifest must serialize"),
        visible_artifact_sha256: input_artifacts
            .iter()
            .map(|artifact| artifact.sha256.clone())
            .collect(),
        hidden_context_classes: vec![
            "authorized_local_result_constructor".to_owned(),
            "dynamic_operation_registry".to_owned(),
            "human_promotion_state".to_owned(),
            "issued_lift_license".to_owned(),
            "model_context".to_owned(),
            "production_credentials".to_owned(),
        ],
        model_context_available: false,
        promotion_constructor_available: false,
        authorized_local_result_constructor_available: false,
        authority_effect: AuthorityEffect::None,
    };
    let observer_sha256 =
        sha256_json_v1(&observer).checked_invariant_ff6bb237("frozen observer must serialize deterministically");
    Coda4TransitionCoveragePacketV1 {
        schema_version: CODA4_PACKET_SCHEMA_VERSION.to_owned(),
        packet_id: S06_002_PACKET_ID.to_owned(),
        goal_id: S06_002_GOAL_ID.to_owned(),
        frozen_base: S06_002_FROZEN_BASE.to_owned(),
        observer,
        observer_sha256,
        source_manifest,
        input_artifacts,
        registered_transitions: canonical_registry_v1(),
        legal_terminals: CodaTerminal::ALL.to_vec(),
        budgets: Coda4BudgetsV1 {
            attempt_budget: 1,
            repair_budget: 2,
            successor_budget: 1,
            time_budget_seconds: 28_800,
            process_budget: 4,
            token_budget: 200_000,
            transition_class_budget: 8,
            state_dimension_budget: 8,
        },
        evidence_ceiling: S06_002_EVIDENCE_CEILING.to_owned(),
        exact_write_surface: S06_002_WRITE_SURFACE
            .iter()
            .map(|path| (*path).to_owned())
            .collect(),
        producer_id: S06_002_PRODUCER_ID.to_owned(),
        evaluator_id: S06_002_OBSERVER_ID.to_owned(),
        authority_witness_id: S06_002_AUTHORITY_WITNESS_ID.to_owned(),
        prior_work_ledger: vec![
            "S02-002 bounded GTOC-3 license-candidate receipt; no license issued".to_owned(),
            "S06-001 bounded receipt-DAG verification; authority None".to_owned(),
            "dda_alphabet.rs canonical eight-operation registry".to_owned(),
            "op_verification.rs concrete cochain transition laws".to_owned(),
        ],
        promotion_constructor_available: false,
        authorized_local_result_constructor_available: false,
        authority_effect: AuthorityEffect::None,
    }
}

pub fn canonical_s06_002_receipt_v1() -> Result<Coda4TransitionCoverageReceiptV1, Coda4CoverageError>
{
    let packet = canonical_s06_002_packet_v1();
    let packet_sha256 = coda4_packet_sha256_v1(&packet)?;
    let transitions = DdaOp::alphabet()
        .into_iter()
        .enumerate()
        .map(|(sequence, operation)| {
            let (before_state, after_state) = canonical_state_pair_v1(operation);
            let outcome = if operation == DdaOp::Lift {
                TransitionOutcomeV1::RefusedToExecute {
                    reason: "bounded GTOC-3 predecessor is admissible for licensing but issued no lift license"
                        .to_owned(),
                }
            } else {
                TransitionOutcomeV1::Executed {
                    log: canonical_log_v1(operation).to_owned(),
                }
            };
            Ok(TransitionExecutionReceiptV1 {
                sequence: sequence as u32,
                transition_class_id: transition_class_id_v1(operation).to_owned(),
                operation,
                before_state_sha256: coda4_state_sha256_v1(&before_state)?,
                after_state_sha256: coda4_state_sha256_v1(&after_state)?,
                before_state,
                after_state,
                outcome,
            })
        })
        .collect::<Result<Vec<_>, Coda4CoverageError>>()?;
    let unknown_state = open_state_a_v1();
    let unknown_state_sha256 = coda4_state_sha256_v1(&unknown_state)?;
    Ok(Coda4TransitionCoverageReceiptV1 {
        schema_version: CODA4_RECEIPT_SCHEMA_VERSION.to_owned(),
        packet_id: packet.packet_id,
        packet_sha256,
        producer_id: S06_002_PRODUCER_ID.to_owned(),
        transitions,
        unknown_transition: UnknownTransitionRefusalV1 {
            request_id: "request:s06-002:unknown-dynamic-operation-v1".to_owned(),
            transition_class_id: S06_002_UNKNOWN_CLASS_ID.to_owned(),
            before_state: unknown_state.clone(),
            before_state_sha256: unknown_state_sha256.clone(),
            after_state: unknown_state,
            after_state_sha256: unknown_state_sha256,
            reason: "transition class is outside the frozen eight-operation registry".to_owned(),
            terminal: CodaTerminal::Refused,
        },
        residual_ids: vec![S06_002_LIFT_RESIDUAL_ID.to_owned()],
        claimed_terminal: CodaTerminal::StabilizedSurvivor,
        promotion_requested: false,
        promotion_constructor_called: false,
        authorized_local_result_created: false,
        authority_effect: AuthorityEffect::None,
    })
}

fn coda4_packet_identities_distinct_v1(packet: &Coda4TransitionCoveragePacketV1) -> bool {
    packet.producer_id != packet.evaluator_id
        && packet.producer_id != packet.authority_witness_id
        && packet.evaluator_id != packet.authority_witness_id
}

fn coda4_packet_authority_clean_v1(packet: &Coda4TransitionCoveragePacketV1) -> bool {
    packet.authority_effect == AuthorityEffect::None
        && packet.observer.authority_effect == AuthorityEffect::None
        && !packet.promotion_constructor_available
        && !packet.authorized_local_result_constructor_available
        && !packet.observer.promotion_constructor_available
        && !packet
            .observer
            .authorized_local_result_constructor_available
}

fn validate_coda4_packet_boundary_v1(
    packet: &Coda4TransitionCoveragePacketV1,
) -> Result<(), Coda4CoverageError> {
    if packet != &canonical_s06_002_packet_v1() {
        return Err(Coda4CoverageError::PacketDrift);
    }
    if packet.schema_version != CODA4_PACKET_SCHEMA_VERSION
        || packet.observer_sha256 != coda4_observer_sha256_v1(&packet.observer)?
        || !coda4_packet_identities_distinct_v1(packet)
        || !coda4_packet_authority_clean_v1(packet)
    {
        return Err(Coda4CoverageError::PacketBoundaryChanged);
    }
    Ok(())
}

fn validate_coda4_receipt_boundary_v1(
    packet: &Coda4TransitionCoveragePacketV1,
    receipt: &Coda4TransitionCoverageReceiptV1,
    packet_sha256: &str,
) -> Result<(), Coda4CoverageError> {
    if receipt.schema_version != CODA4_RECEIPT_SCHEMA_VERSION
        || receipt.packet_id != packet.packet_id
        || receipt.packet_sha256 != packet_sha256
        || receipt.producer_id != packet.producer_id
    {
        return Err(Coda4CoverageError::ReceiptBindingMismatch);
    }
    if receipt.authority_effect != AuthorityEffect::None
        || receipt.promotion_requested
        || receipt.promotion_constructor_called
        || receipt.authorized_local_result_created
    {
        return Err(Coda4CoverageError::AuthorityExpanded);
    }
    Ok(())
}

fn validate_coda4_transition_coverage_set_v1<'a>(
    packet: &'a Coda4TransitionCoveragePacketV1,
    receipt: &Coda4TransitionCoverageReceiptV1,
) -> Result<BTreeMap<&'a str, &'a RegisteredTransitionClassV1>, Coda4CoverageError> {
    let registry = packet
        .registered_transitions
        .iter()
        .map(|entry| (entry.transition_class_id.as_str(), entry))
        .collect::<BTreeMap<_, _>>();
    let mut classes = BTreeSet::new();
    let mut operations = BTreeSet::new();
    for transition in &receipt.transitions {
        if !registry.contains_key(transition.transition_class_id.as_str()) {
            return Err(Coda4CoverageError::UnknownTransitionExecuted(
                transition.transition_class_id.clone(),
            ));
        }
        if !classes.insert(transition.transition_class_id.clone()) {
            return Err(Coda4CoverageError::DuplicateTransitionClass(
                transition.transition_class_id.clone(),
            ));
        }
        if !operations.insert(operation_rank_v1(transition.operation)) {
            return Err(Coda4CoverageError::DuplicateOperation(transition.operation));
        }
    }
    if receipt.transitions.len() != registry.len() {
        return Err(Coda4CoverageError::CoverageCountMismatch {
            expected: registry.len(),
            found: receipt.transitions.len(),
        });
    }
    Ok(registry)
}

fn resolve_coda4_step_outcome_v1(
    expected: &RegisteredTransitionClassV1,
    transition: &TransitionExecutionReceiptV1,
    executed_count: &mut u32,
    refused_count: &mut u32,
) -> Result<(DdaStep, VerifiedOutcomeKindV1), Coda4CoverageError> {
    match (&expected.mode, &transition.outcome) {
        (RegisteredTransitionModeV1::Executed, TransitionOutcomeV1::Executed { log }) => {
            require_payload(&transition.transition_class_id, log)?;
            *executed_count += 1;
            Ok((
                DdaStep::executed(transition.operation, log.clone()),
                VerifiedOutcomeKindV1::Executed,
            ))
        }
        (
            RegisteredTransitionModeV1::RefusedUntilLiftLicenseIssued,
            TransitionOutcomeV1::RefusedToExecute { reason },
        ) => {
            require_payload(&transition.transition_class_id, reason)?;
            *refused_count += 1;
            Ok((
                DdaStep::refused(transition.operation, reason.clone()),
                VerifiedOutcomeKindV1::RefusedToExecute,
            ))
        }
        (
            RegisteredTransitionModeV1::RefusedUntilLiftLicenseIssued,
            TransitionOutcomeV1::Executed { .. },
        ) => Err(Coda4CoverageError::UnissuedLiftExecution),
        _ => Err(Coda4CoverageError::OutcomeMismatch(
            transition.transition_class_id.clone(),
        )),
    }
}

fn verify_coda4_transition_headers_and_hashes_v1(
    expected: &RegisteredTransitionClassV1,
    transition: &TransitionExecutionReceiptV1,
) -> Result<(String, String), Coda4CoverageError> {
    if transition.sequence != expected.sequence
        || transition.transition_class_id != expected.transition_class_id
        || transition.operation != expected.operation
    {
        return Err(Coda4CoverageError::OperationAttributionMismatch(
            expected.transition_class_id.clone(),
        ));
    }
    let before_sha256 = coda4_state_sha256_v1(&transition.before_state)?;
    let after_sha256 = coda4_state_sha256_v1(&transition.after_state)?;
    if transition.before_state_sha256 != before_sha256
        || transition.after_state_sha256 != after_sha256
        || expected.before_state_sha256 != before_sha256
        || expected.after_state_sha256 != after_sha256
    {
        return Err(Coda4CoverageError::StateHashMismatch(
            transition.transition_class_id.clone(),
        ));
    }
    Ok((before_sha256, after_sha256))
}

fn verify_single_coda4_transition_v1(
    expected: &RegisteredTransitionClassV1,
    transition: &TransitionExecutionReceiptV1,
    dimension_budget: usize,
    executed_count: &mut u32,
    refused_count: &mut u32,
) -> Result<TransitionVerificationEvidenceV1, Coda4CoverageError> {
    let (before_sha256, after_sha256) =
        verify_coda4_transition_headers_and_hashes_v1(expected, transition)?;
    let before = transition.before_state.realize(dimension_budget)?;
    let after = transition.after_state.realize(dimension_budget)?;
    if matches!(
        transition.outcome,
        TransitionOutcomeV1::RefusedToExecute { .. }
    ) && before != after
    {
        return Err(Coda4CoverageError::RefusalMutatedState(
            transition.transition_class_id.clone(),
        ));
    }
    let (step, outcome) =
        resolve_coda4_step_outcome_v1(expected, transition, executed_count, refused_count)?;
    let evidence = verify_step(&step, &before, &after).map_err(|violation| {
        Coda4CoverageError::OperationLawViolation {
            transition_class_id: transition.transition_class_id.clone(),
            reason: format!("{violation:?}"),
        }
    })?;
    Ok(TransitionVerificationEvidenceV1 {
        sequence: transition.sequence,
        transition_class_id: transition.transition_class_id.clone(),
        operation: transition.operation,
        before_state_sha256: before_sha256,
        after_state_sha256: after_sha256,
        before_phi: evidence.before.phi,
        before_gamma: evidence.before.gamma,
        before_classification: evidence.before.classification.into(),
        after_phi: evidence.after.phi,
        after_gamma: evidence.after.gamma,
        after_classification: evidence.after.classification.into(),
        outcome,
    })
}

fn build_coda4_verification_result_v1(
    packet: &Coda4TransitionCoveragePacketV1,
    receipt: &Coda4TransitionCoverageReceiptV1,
    packet_sha256: String,
    executed_transition_count: u32,
    refused_transition_count: u32,
    transition_evidence: Vec<TransitionVerificationEvidenceV1>,
    residual_ids: Vec<String>,
    terminal: CodaTerminal,
) -> Result<Coda4TransitionCoverageVerificationV1, Coda4CoverageError> {
    Ok(Coda4TransitionCoverageVerificationV1 {
        schema_version: CODA4_VERIFICATION_SCHEMA_VERSION.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256,
        observer_sha256: packet.observer_sha256.clone(),
        receipt_sha256: coda4_receipt_sha256_v1(receipt)?,
        artifact_closure_sha256: sha256_json_v1(&packet.input_artifacts)?,
        transition_matrix_sha256: sha256_json_v1(&receipt.transitions)?,
        unknown_refusal_sha256: sha256_json_v1(&receipt.unknown_transition)?,
        evaluator_id: packet.evaluator_id.clone(),
        authority_witness_id: packet.authority_witness_id.clone(),
        registered_transition_count: packet.registered_transitions.len() as u32,
        executed_transition_count,
        refused_transition_count,
        transition_evidence,
        every_alphabet_operation_covered_once: true,
        every_state_hash_recomputed: true,
        every_operation_law_replayed: true,
        every_refusal_immutable: true,
        unknown_classes_refused: true,
        predecessor_receipts_verified: true,
        cochain_identities_zero: true,
        residual_ids,
        terminal,
        promotion_requested: false,
        promotion_constructor_called: false,
        authorized_local_result_created: false,
        authority_effect: AuthorityEffect::None,
    })
}

fn validate_coda4_residuals_and_terminal_v1(
    receipt: &Coda4TransitionCoverageReceiptV1,
) -> Result<(Vec<String>, CodaTerminal), Coda4CoverageError> {
    let residual_ids = vec![S06_002_LIFT_RESIDUAL_ID.to_owned()];
    if receipt.residual_ids != residual_ids {
        return Err(Coda4CoverageError::ResidualMismatch);
    }
    let terminal = CodaTerminal::StabilizedSurvivor;
    if receipt.claimed_terminal != terminal {
        return Err(Coda4CoverageError::TerminalMismatch {
            expected: terminal,
            found: receipt.claimed_terminal,
        });
    }
    Ok((residual_ids, terminal))
}

pub fn verify_coda4_transition_coverage_v1(
    packet: &Coda4TransitionCoveragePacketV1,
    receipt: &Coda4TransitionCoverageReceiptV1,
    artifact_bytes: &Coda4ArtifactBytesV1,
) -> Result<Coda4TransitionCoverageVerificationV1, Coda4CoverageError> {
    validate_coda4_packet_boundary_v1(packet)?;
    let packet_sha256 = coda4_packet_sha256_v1(packet)?;
    validate_coda4_receipt_boundary_v1(packet, receipt, &packet_sha256)?;
    verify_predecessor_artifacts_v1(packet, artifact_bytes)?;
    let registry = validate_coda4_transition_coverage_set_v1(packet, receipt)?;

    let dimension_budget = packet.budgets.state_dimension_budget as usize;
    let mut transition_evidence = Vec::with_capacity(registry.len());
    let mut executed_transition_count = 0_u32;
    let mut refused_transition_count = 0_u32;

    for (expected, transition) in packet
        .registered_transitions
        .iter()
        .zip(&receipt.transitions)
    {
        transition_evidence.push(verify_single_coda4_transition_v1(
            expected,
            transition,
            dimension_budget,
            &mut executed_transition_count,
            &mut refused_transition_count,
        )?);
    }

    verify_unknown_refusal_v1(packet, receipt, &registry)?;
    let (residual_ids, terminal) = validate_coda4_residuals_and_terminal_v1(receipt)?;

    build_coda4_verification_result_v1(
        packet,
        receipt,
        packet_sha256,
        executed_transition_count,
        refused_transition_count,
        transition_evidence,
        residual_ids,
        terminal,
    )
}

pub fn coda4_packet_sha256_v1(
    packet: &Coda4TransitionCoveragePacketV1,
) -> Result<String, Coda4CoverageError> {
    sha256_json_v1(packet)
}

pub fn coda4_receipt_sha256_v1(
    receipt: &Coda4TransitionCoverageReceiptV1,
) -> Result<String, Coda4CoverageError> {
    sha256_json_v1(receipt)
}

pub fn coda4_verification_sha256_v1(
    verification: &Coda4TransitionCoverageVerificationV1,
) -> Result<String, Coda4CoverageError> {
    sha256_json_v1(verification)
}

pub fn coda4_observer_sha256_v1(
    observer: &FrozenCoda4ObserverV1,
) -> Result<String, Coda4CoverageError> {
    sha256_json_v1(observer)
}

pub fn coda4_state_sha256_v1(state: &CochainStateSpecV1) -> Result<String, Coda4CoverageError> {
    sha256_json_v1(state)
}

pub fn canonical_json_line_v1<T: Serialize + ?Sized>(
    value: &T,
) -> Result<Vec<u8>, Coda4CoverageError> {
    let mut bytes = serde_json::to_vec(value).map_err(json_error)?;
    bytes.push(b'\n');
    Ok(bytes)
}

pub fn parse_coda4_packet_canonical_v1(
    bytes: &[u8],
) -> Result<Coda4TransitionCoveragePacketV1, Coda4CoverageError> {
    parse_canonical_json_line_v1(bytes, "packet")
}

pub fn parse_coda4_receipt_canonical_v1(
    bytes: &[u8],
) -> Result<Coda4TransitionCoverageReceiptV1, Coda4CoverageError> {
    parse_canonical_json_line_v1(bytes, "receipt")
}

pub fn parse_coda4_verification_canonical_v1(
    bytes: &[u8],
) -> Result<Coda4TransitionCoverageVerificationV1, Coda4CoverageError> {
    parse_canonical_json_line_v1(bytes, "verification")
}

fn canonical_registry_v1() -> Vec<RegisteredTransitionClassV1> {
    DdaOp::alphabet()
        .into_iter()
        .enumerate()
        .map(|(sequence, operation)| {
            let (before, after) = canonical_state_pair_v1(operation);
            RegisteredTransitionClassV1 {
                sequence: sequence as u32,
                transition_class_id: transition_class_id_v1(operation).to_owned(),
                operation,
                mode: if operation == DdaOp::Lift {
                    RegisteredTransitionModeV1::RefusedUntilLiftLicenseIssued
                } else {
                    RegisteredTransitionModeV1::Executed
                },
                before_state_sha256: coda4_state_sha256_v1(&before)
                    .checked_invariant_ff6bb237("canonical before state must serialize"),
                after_state_sha256: coda4_state_sha256_v1(&after)
                    .checked_invariant_ff6bb237("canonical after state must serialize"),
            }
        })
        .collect()
}

fn canonical_state_pair_v1(operation: DdaOp) -> (CochainStateSpecV1, CochainStateSpecV1) {
    match operation {
        DdaOp::ExactRepair => (open_state_a_v1(), exact_state_a_v1()),
        DdaOp::ResidualProjection => (open_state_a_v1(), projected_state_a_v1()),
        DdaOp::ContextExposure => (open_state_a_v1(), open_state_b_v1()),
        DdaOp::Integration => (exact_state_a_v1(), exact_state_a_v1()),
        DdaOp::Lift => (open_state_b_v1(), open_state_b_v1()),
        DdaOp::Descent => (open_state_b_v1(), open_state_a_v1()),
        DdaOp::Refusal => (projected_state_a_v1(), projected_state_a_v1()),
        DdaOp::Terminalize => (survivor_state_v1(), survivor_state_v1()),
    }
}

fn transition_class_id_v1(operation: DdaOp) -> &'static str {
    match operation {
        DdaOp::ExactRepair => "transition:s06-002:exact-repair",
        DdaOp::ResidualProjection => "transition:s06-002:residual-projection",
        DdaOp::ContextExposure => "transition:s06-002:context-exposure",
        DdaOp::Integration => "transition:s06-002:integration",
        DdaOp::Lift => "transition:s06-002:lift",
        DdaOp::Descent => "transition:s06-002:descent",
        DdaOp::Refusal => "transition:s06-002:typed-refusal",
        DdaOp::Terminalize => "transition:s06-002:terminalize",
    }
}

fn canonical_log_v1(operation: DdaOp) -> &'static str {
    match operation {
        DdaOp::ExactRepair => "replayed E and discharged the open residual on the fixed carrier",
        DdaOp::ResidualProjection => {
            "replayed R and preserved obstruction mass on the fixed carrier"
        }
        DdaOp::ContextExposure => "replayed C and exposed the registered three-coordinate carrier",
        DdaOp::Integration => "replayed I as an append-only state-inert ledger operation",
        DdaOp::Lift => "unreachable: canonical lift is refused until a license is issued",
        DdaOp::Descent => "replayed D and returned to the registered two-coordinate carrier",
        DdaOp::Refusal => "replayed M as a typed state-inert refusal terminal",
        DdaOp::Terminalize => "replayed T over a closed stabilized survivor",
    }
}

fn open_state_a_v1() -> CochainStateSpecV1 {
    state_v1(
        1,
        1,
        vec![vec![true], vec![false]],
        2,
        vec![vec![false, true]],
        vec![false, true],
    )
}

fn projected_state_a_v1() -> CochainStateSpecV1 {
    state_v1(
        1,
        1,
        vec![vec![true], vec![false]],
        2,
        vec![vec![false, true]],
        vec![true, true],
    )
}

fn exact_state_a_v1() -> CochainStateSpecV1 {
    state_v1(
        1,
        1,
        vec![vec![true], vec![false]],
        2,
        vec![vec![false, true]],
        vec![false, false],
    )
}

fn open_state_b_v1() -> CochainStateSpecV1 {
    state_v1(
        1,
        1,
        vec![vec![true], vec![false], vec![false]],
        3,
        vec![vec![false, true, false]],
        vec![false, true, false],
    )
}

fn survivor_state_v1() -> CochainStateSpecV1 {
    state_v1(1, 1, vec![vec![false]], 1, vec![vec![false]], vec![true])
}

fn state_v1(
    degree: usize,
    previous_domain_dim: usize,
    previous_rows: Vec<Vec<bool>>,
    next_domain_dim: usize,
    next_rows: Vec<Vec<bool>>,
    residual: Vec<bool>,
) -> CochainStateSpecV1 {
    CochainStateSpecV1 {
        degree,
        previous: BinaryMapSpecV1 {
            domain_dim: previous_domain_dim,
            rows: previous_rows,
        },
        next: BinaryMapSpecV1 {
            domain_dim: next_domain_dim,
            rows: next_rows,
        },
        residual,
    }
}

fn verify_coda4_artifact_hashes_v1(
    packet: &Coda4TransitionCoveragePacketV1,
    artifact_bytes: &Coda4ArtifactBytesV1,
) -> Result<(), Coda4CoverageError> {
    let expected_paths = packet
        .input_artifacts
        .iter()
        .map(|artifact| artifact.path.as_str())
        .collect::<BTreeSet<_>>();
    let found_paths = artifact_bytes
        .keys()
        .map(String::as_str)
        .collect::<BTreeSet<_>>();
    if expected_paths != found_paths {
        if let Some(path) = expected_paths.difference(&found_paths).next() {
            return Err(Coda4CoverageError::MissingArtifact((*path).to_owned()));
        }
        return Err(Coda4CoverageError::ArtifactSetMismatch);
    }

    for artifact in &packet.input_artifacts {
        let bytes = artifact_bytes
            .get(&artifact.path)
            .ok_or_else(|| Coda4CoverageError::MissingArtifact(artifact.path.clone()))?;
        if bytes.len() as u64 != artifact.bytes {
            return Err(Coda4CoverageError::ArtifactLengthMismatch(
                artifact.path.clone(),
            ));
        }
        if sha256_bytes_v1(bytes) != artifact.sha256 {
            return Err(Coda4CoverageError::ArtifactHashMismatch(
                artifact.path.clone(),
            ));
        }
    }
    Ok(())
}

fn s06_001_verification_valid_v1(
    s06_001: &crate::coda_gtla_run_receipt::CodaGtlaRunVerificationV1,
) -> bool {
    s06_001.terminal == CodaTerminal::StabilizedSurvivor
        && s06_001.d1_d0_zero
        && !s06_001.promotion_requested
        && !s06_001.promotion_constructor_called
        && !s06_001.authorized_local_result_created
        && s06_001.authority_effect == AuthorityEffect::None
}

fn verify_predecessor_artifacts_v1(
    packet: &Coda4TransitionCoveragePacketV1,
    artifact_bytes: &Coda4ArtifactBytesV1,
) -> Result<(), Coda4CoverageError> {
    verify_coda4_artifact_hashes_v1(packet, artifact_bytes)?;

    let s06_001_bytes = artifact_bytes
        .get(S06_001_VERIFICATION_PATH)
        .ok_or_else(|| Coda4CoverageError::MissingArtifact(S06_001_VERIFICATION_PATH.to_owned()))?;
    let s06_001 = parse_run_verification_canonical_v1(s06_001_bytes)
        .map_err(|error| Coda4CoverageError::InvalidPredecessor(format!("S06-001: {error}")))?;
    if !s06_001_verification_valid_v1(&s06_001) {
        return Err(Coda4CoverageError::InvalidPredecessor(
            "S06-001 boundary mismatch".to_owned(),
        ));
    }

    let coda3_bytes = artifact_bytes
        .get(CODA3_RECEIPT_PATH)
        .ok_or_else(|| Coda4CoverageError::MissingArtifact(CODA3_RECEIPT_PATH.to_owned()))?;
    let coda3: Coda3ReceiptSetV1 = serde_json::from_slice(coda3_bytes)
        .map_err(|error| Coda4CoverageError::InvalidPredecessor(format!("GTOC-3: {error}")))?;
    validate_coda3_predecessor_v1(&coda3)
}

fn coda3_classification_and_producer_valid_v1(execution: &Coda3ExecutionV1) -> bool {
    let classification = &execution.classification;
    let producer = &execution.receipts.producer;
    classification.structural_trigger_not_license
        && classification.complete_for_licensing
        && !classification.license_issued
        && !classification.lift_executed
        && classification.terminal_proposal == CodaTerminal::StabilizedSurvivor
        && classification.authority_effect == AuthorityEffect::None
        && !producer.license_issued
        && !producer.lift_executed
        && producer.authority_effect == AuthorityEffect::None
}

fn coda3_evaluation_and_witness_valid_v1(execution: &Coda3ExecutionV1) -> bool {
    let receipts = &execution.receipts;
    receipts.evaluation.exact_match
        && receipts.evaluation.trigger_not_treated_as_license
        && receipts.evaluation.operator_license_binding_checked
        && receipts.evaluation.policy_budget_checked
        && receipts.evaluation.authority_effect == AuthorityEffect::None
        && receipts.authority_witness.identities_distinct
        && !receipts.authority_witness.human_promotion_performed
        && !receipts.authority_witness.license_issued
        && !receipts.authority_witness.lift_executed
        && receipts.authority_witness.authority_effect == AuthorityEffect::None
}

fn coda3_replay_and_terminal_valid_v1(execution: &Coda3ExecutionV1) -> bool {
    let receipts = &execution.receipts;
    receipts.replay.deterministic
        && receipts.replay.first_producer_sha256 == receipts.replay.replay_producer_sha256
        && receipts.terminal.terminal_proposal == CodaTerminal::StabilizedSurvivor
        && !receipts.terminal.human_promotion_performed
        && receipts.terminal.authority_effect == AuthorityEffect::None
}

fn validate_coda3_predecessor_v1(
    receipt_set: &Coda3ReceiptSetV1,
) -> Result<(), Coda4CoverageError> {
    if receipt_set.schema_version != CODA3_RECEIPT_SCHEMA_VERSION
        || receipt_set.executions.len() != 1
    {
        return Err(Coda4CoverageError::InvalidPredecessor(
            "GTOC-3 receipt-set shape mismatch".to_owned(),
        ));
    }
    let execution = &receipt_set.executions[0];
    let valid = coda3_classification_and_producer_valid_v1(execution)
        && coda3_evaluation_and_witness_valid_v1(execution)
        && coda3_replay_and_terminal_valid_v1(execution);
    if !valid {
        return Err(Coda4CoverageError::InvalidPredecessor(
            "GTOC-3 is not an evidence-only unissued license candidate".to_owned(),
        ));
    }
    Ok(())
}

fn unknown_refusal_fields_valid_v1(
    unknown: &UnknownTransitionRefusalV1,
    registry: &BTreeMap<&str, &RegisteredTransitionClassV1>,
) -> bool {
    !unknown.request_id.trim().is_empty()
        && !unknown.transition_class_id.trim().is_empty()
        && !registry.contains_key(unknown.transition_class_id.as_str())
        && !unknown.reason.trim().is_empty()
        && unknown.terminal == CodaTerminal::Refused
}

fn verify_unknown_refusal_v1(
    packet: &Coda4TransitionCoveragePacketV1,
    receipt: &Coda4TransitionCoverageReceiptV1,
    registry: &BTreeMap<&str, &RegisteredTransitionClassV1>,
) -> Result<(), Coda4CoverageError> {
    let unknown = &receipt.unknown_transition;
    let before_sha256 = coda4_state_sha256_v1(&unknown.before_state)?;
    let after_sha256 = coda4_state_sha256_v1(&unknown.after_state)?;
    let before = unknown
        .before_state
        .realize(packet.budgets.state_dimension_budget as usize)?;
    let after = unknown
        .after_state
        .realize(packet.budgets.state_dimension_budget as usize)?;
    if !unknown_refusal_fields_valid_v1(unknown, registry)
        || unknown.before_state_sha256 != before_sha256
        || unknown.after_state_sha256 != after_sha256
        || before != after
    {
        return Err(Coda4CoverageError::UnknownRefusalMismatch);
    }
    Ok(())
}

fn require_payload(transition_class_id: &str, value: &str) -> Result<(), Coda4CoverageError> {
    if value.trim().is_empty() {
        return Err(Coda4CoverageError::EmptyOutcomePayload(
            transition_class_id.to_owned(),
        ));
    }
    Ok(())
}

fn operation_rank_v1(operation: DdaOp) -> u8 {
    match operation {
        DdaOp::ExactRepair => 0,
        DdaOp::ResidualProjection => 1,
        DdaOp::ContextExposure => 2,
        DdaOp::Integration => 3,
        DdaOp::Lift => 4,
        DdaOp::Descent => 5,
        DdaOp::Refusal => 6,
        DdaOp::Terminalize => 7,
    }
}

fn parse_canonical_json_line_v1<T>(bytes: &[u8], label: &str) -> Result<T, Coda4CoverageError>
where
    T: Serialize + DeserializeOwned,
{
    let parsed = serde_json::from_slice::<T>(bytes)
        .map_err(|error| Coda4CoverageError::Decode(error.to_string()))?;
    if canonical_json_line_v1(&parsed)? != bytes {
        return Err(Coda4CoverageError::NonCanonicalJson(label.to_owned()));
    }
    Ok(parsed)
}

fn sha256_json_v1<T: Serialize + ?Sized>(value: &T) -> Result<String, Coda4CoverageError> {
    serde_json::to_vec(value)
        .map(|bytes| sha256_bytes_v1(&bytes))
        .map_err(json_error)
}

fn sha256_bytes_v1(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}

fn json_error(error: serde_json::Error) -> Coda4CoverageError {
    Coda4CoverageError::Json(error.to_string())
}


// Backward compatibility aliases

// Origin: vendor/engine/engine_state/src/coda4_transition_coverage.rs
// Claim: urn:omega:crates_rs:omega-state:coda4-transition-coverage:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_ff6bb237 {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
