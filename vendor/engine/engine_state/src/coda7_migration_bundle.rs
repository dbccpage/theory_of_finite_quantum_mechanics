//! Finite CODA-7 migration-bundle preservation for S03-002.
//!
//! The carrier is deliberately closed: three heterogeneous members, two frozen
//! predecessor receipts, and one exact path-pair policy.  It verifies replayed
//! before/after snapshots; it does not discover files or mutate a repository.

#[allow(dead_code, non_camel_case_types, missing_docs)]
trait CheckedInvariantExt_1ec30bbc<T> {
    fn checked_invariant_1ec30bbc(self, msg: &str) -> T;
}

impl<T> CheckedInvariantExt_1ec30bbc<T> for Option<T> {
    #[inline]
    fn checked_invariant_1ec30bbc(self, msg: &str) -> T {
        match self {
            Some(v) => v,
            None => unreachable!("{}", msg),
        }
    }
}

impl<T, E: std::fmt::Debug> CheckedInvariantExt_1ec30bbc<T> for std::result::Result<T, E> {
    #[inline]
    fn checked_invariant_1ec30bbc(self, msg: &str) -> T {
        match self {
            Ok(v) => v,
            Err(e) => unreachable!("{}: {:?}", msg, e),
        }
    }
}
use std::collections::{BTreeMap, BTreeSet};

use engine_types::authority::AuthorityEffect;
use serde::de::DeserializeOwned;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

use crate::coda6_defect_terminalization::{
    aggregate_coda6_terminals_v1, parse_coda6_verification_canonical_v1,
};
use crate::coda_gtla_protocol::CodaTerminal;
use crate::task_admission::TaskAdmissionReceiptV1;

pub const CODA7_PACKET_SCHEMA_VERSION: &str = "omega.gtoc7.migration-bundle.packet.v1";
pub const CODA7_RECEIPT_SCHEMA_VERSION: &str = "omega.gtoc7.migration-bundle.receipt.v1";
pub const CODA7_VERIFICATION_SCHEMA_VERSION: &str = "omega.gtoc7.migration-bundle.verification.v1";
pub const S03_002_FROZEN_BASE: &str = "2cb7db4878a8326a9dc1f706357feeac3bc933e0";
pub const S03_002_PACKET_ID: &str = "omega-conductor-s03-002-gtoc7-migration-bundle-v1";

pub const S03_002_GOAL_ID: &str = "S03-002:GTOC-7";
pub const S03_002_PRODUCER_ID: &str = "witness:producer:s03-002-migration-bundle-v1";
pub const S03_002_EVALUATOR_ID: &str = "witness:evaluator:s03-002-independent-v1";
pub const S03_002_AUTHORITY_WITNESS_ID: &str = "witness:authority:s03-002-none-v1";
pub const S03_002_PATH_POLICY_ID: &str = "policy:s03-002:finite-explicit-pairs-v1";
pub const S03_002_SOURCE_ROOT: &str = "in-memory-snapshot/s03-002/before/";
pub const S03_002_TARGET_ROOT: &str = "in-memory-snapshot/s03-002/after/";
pub const S03_002_PREDECESSOR_RESIDUAL_ID: &str =
    "residual:s03-002:predecessors-not-human-promoted";
pub const S03_002_UNRESTRICTED_FAMILY_RESIDUAL_ID: &str =
    "residual:s03-002:unrestricted-migration-bundle-family-unproved";
pub const S03_001_RECEIPT_PATH: &str =
    "omega_engine/crates/omega_state/tests/fixtures/s03_001_task_admission_receipt_v1.json";
pub const S06_003_VERIFICATION_PATH: &str =
    "omega_engine/crates/omega_state/tests/fixtures/s06_003_gtoc6_verification_v1.json";
pub const S06_004_HISTORICAL_RECEIPT_PATH: &str =
    "omega_engine/crates/omega_state/tests/fixtures/s06_004_gtoc8_receipt_v1.json";
pub const S03_002_EVIDENCE_CEILING: &str =
    "one frozen three-member in-memory Markdown/Rust/JSON byte-preserving relocation carrier with a fifteen-path exact write surface over the exact S03-001 admission receipt and S06-003 verification; predecessor human promotion remains absent; no wildcard discovery, external import, arbitrary repository migration, workspace mutation, authority, gate activation, or successor instantiation";

pub const S03_002_WRITE_SURFACE: [&str; 15] = [
    "docs/archive/omega_conductor_v001/index.md",
    "docs/archive/omega_conductor_v001/sprint_s03_002.md",
    "docs/gtoc-canonicalization-remaining-work.md",
    "docs/omega-conductor-epic-implementation-handoff-2026-07-20.md",
    "docs/omega-conductor-epic-v001.md",
    "docs/saga_03_task_admission_and_carriers.md",
    "docs/sprint_s03_002.md",
    "docs/status/omega_conductor_s03_002_status_2026-07-20.md",
    "omega_engine/crates/omega_state/src/gtoc7_migration_bundle.rs",
    "omega_engine/crates/omega_state/src/lib.rs",
    "omega_engine/crates/omega_state/tests/fixtures/s03_002_gtoc7_packet_v1.json",
    "omega_engine/crates/omega_state/tests/fixtures/s03_002_gtoc7_receipt_v1.json",
    "omega_engine/crates/omega_state/tests/fixtures/s03_002_gtoc7_verification_v1.json",
    "omega_engine/crates/omega_state/tests/gtoc7_migration_bundle.rs",
    "scripts/validate_s03_002.py",
];
pub const S03_002_SOURCE_MANIFEST: [(&str, &str, u64); 16] = [
    (
        "docs/gtoc-canonicalization-remaining-work.md",
        "e09fb35859f3905368df27e0121c05c9a590f7a82bd3f710c0cc0c74a5d5a639",
        27_166,
    ),
    (
        "docs/omega-conductor-epic-v001.md",
        "0d3e2f92f5aec105cdb35daa8599785c1f8db8bc737af18dd77305f9b7a535a2",
        93_378,
    ),
    (
        "docs/saga_03_task_admission_and_carriers.md",
        "fc761eb0c248ad03d7b79c72aa0b3fd1a82a4b46b9f3a956dccfe2de029362bd",
        6_171,
    ),
    (
        "docs/sprint_s03_002.md",
        "35d54528f8bf54f6a3e93b4957b412fc22f9a19139c13332be97d11b77252439",
        8_262,
    ),
    (
        "docs/status-vocabulary.md",
        "264c90fde2814d9197d78258c2ccc948259c895b32f85b70ae64fd70cf48d879",
        4_541,
    ),
    (
        "docs/status/omega_conductor_s03_001_status_2026-07-18.md",
        "56fb66000f87a56bac7a821d75014a4f9439c465ea7e748e2f93abb7ff1517af",
        8_922,
    ),
    (
        "docs/status/omega_conductor_s06_003_status_2026-07-18.md",
        "1309f0b2ac0da28bab2196d34338a40fd254660fda30578f0f0649f5daac14ed",
        14_555,
    ),
    (
        "omega_engine/crates/omega_state/Cargo.toml",
        "cc089b4ad71ef84c75c79a7d5cac8a810e0ea278aba4aaadec252880dcc8eb73",
        512,
    ),
    (
        "omega_engine/crates/omega_state/src/gtoc6_defect_terminalization.rs",
        "4d6d55baf039a57d5ad855a553f5f1437a44ed8732a63cd8a7d628872d279dd1",
        52_168,
    ),
    (
        "omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs",
        "da57f9f89dd396cbd1bca72880d024c81a4d3238bd6f78af9add06572c3f160f",
        35_825,
    ),
    (
        "omega_engine/crates/omega_state/src/lib.rs",
        "9396b64dbd13a13f0def9fe111c0f2a25c4627642ad6f98d0d179d285f107d40",
        6_234,
    ),
    (
        "omega_engine/crates/omega_state/src/task_admission.rs",
        "8904c36f0dce155de2c735d1199b553f2a4b5772121d462318515a449938d951",
        55_627,
    ),
    (
        "omega_engine/crates/omega_state/tests/fixtures/s03_001_task_admission_receipt_v1.json",
        "41e6895b82382a8ab84f48d62aa18f50f47f43bbf95210db1f891c11ed7ef7a8",
        1_655,
    ),
    (
        "omega_engine/crates/omega_state/tests/fixtures/s06_003_gtoc6_verification_v1.json",
        "15f33eee4d7dd791996964076e92b9f928789d06ef41ab1c2309acc792551c98",
        2_171,
    ),
    (
        "omega_engine/crates/omega_state/tests/gtoc6_defect_terminalization.rs",
        "d0deb4b52f734e54016409c7fa7f35cc5265a78d354aa0c745997ce2eae17a8c",
        13_937,
    ),
    (
        "omega_engine/crates/omega_state/tests/task_admission.rs",
        "ecce0b7b1a8bd8565c717fa93e969c8434f63c4c4bb3bcea0f65546336956b48",
        24_256,
    ),
];

const S03_001_RECEIPT_BYTES: &[u8] = include_bytes!(concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../tests/engine_state/fixtures/s03_001_task_admission_receipt_v1.json"
));
const S06_003_VERIFICATION_BYTES: &[u8] = include_bytes!(concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../tests/engine_state/fixtures/s06_003_gtoc6_verification_v1.json"
));
const MEMBER_00_BYTES: &[u8] = b"# finite GTOC-7 carrier\n\nExact member; no discovery.\n";
const MEMBER_01_BYTES: &[u8] = b"pub const GTOC7_FIXTURE_SCOPE: &str = \"finite-explicit\";\n";
const MEMBER_02_BYTES: &[u8] =
    b"{\"member\":\"receipt\",\"schema_version\":\"omega.gtoc7.fixture.v1\"}\n";

/// Packet-local snapshot identifiers mapped to their in-memory bytes.
///
/// The keys are not filesystem paths and verification never reads them from or
/// writes them to a repository.
pub type Coda7ArtifactMapV1 = BTreeMap<String, Vec<u8>>;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenCoda7SourceV1 {
    pub path: String,
    pub sha256: String,
    pub bytes: u64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Coda7ReplayArtifactsV1 {
    pub predecessor_artifacts: Coda7ArtifactMapV1,
    pub before_members: Coda7ArtifactMapV1,
    pub after_members: Coda7ArtifactMapV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda7ArtifactBindingV1 {
    pub artifact_id: String,
    pub path: String,
    pub sha256: String,
    pub bytes: u64,
    pub terminal: CodaTerminal,
    pub human_promotion_recorded: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenCoda7ObserverV1 {
    pub observer_id: String,
    pub source_manifest_sha256: String,
    pub predecessor_manifest_sha256: String,
    pub visible_source_sha256: Vec<String>,
    pub visible_artifact_sha256: Vec<String>,
    pub hidden_context_classes: Vec<String>,
    pub model_context_available: bool,
    pub member_discovery_available: bool,
    pub promotion_constructor_available: bool,
    pub authorized_local_result_constructor_available: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Coda7ArtifactKindV1 {
    Markdown,
    Rust,
    Json,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Coda7MigrationOperationV1 {
    BytePreservingRelocation,
    UnsupportedTransformation,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Coda7MemberStorageV1 {
    InMemorySnapshot,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda7PathPairV1 {
    pub sequence: u32,
    pub member_id: String,
    pub source_path: String,
    pub target_path: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda7PathPolicyV1 {
    pub policy_id: String,
    pub member_storage: Coda7MemberStorageV1,
    pub source_root: String,
    pub target_root: String,
    pub exact_pairs: Vec<Coda7PathPairV1>,
    pub wildcard_members_allowed: bool,
    pub member_discovery_allowed: bool,
    pub external_imports_allowed: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda7MemberSpecV1 {
    pub sequence: u32,
    pub member_id: String,
    pub kind: Coda7ArtifactKindV1,
    pub operation: Coda7MigrationOperationV1,
    pub source_path: String,
    pub source_sha256: String,
    pub source_bytes: u64,
    pub target_path: String,
    pub target_sha256: String,
    pub target_bytes: u64,
    pub dependency_ids: Vec<String>,
    pub path_policy_id: String,
    pub expected_terminal: CodaTerminal,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda7BudgetsV1 {
    pub attempt_budget: u32,
    pub repair_budget: u32,
    pub successor_budget: u32,
    pub time_budget_seconds: u32,
    pub process_budget: u32,
    pub token_budget: u32,
    pub member_budget: u32,
    pub dependency_budget: u32,
    pub residual_budget: u32,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda7MigrationPacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub goal_id: String,
    pub frozen_base: String,
    pub observer: FrozenCoda7ObserverV1,
    pub observer_sha256: String,
    pub source_manifest: Vec<FrozenCoda7SourceV1>,
    pub predecessors: Vec<Coda7ArtifactBindingV1>,
    pub path_policy: Coda7PathPolicyV1,
    pub members: Vec<Coda7MemberSpecV1>,
    pub legal_terminals: Vec<CodaTerminal>,
    pub budgets: Coda7BudgetsV1,
    pub evidence_ceiling: String,
    pub exact_write_surface: Vec<String>,
    pub nonclaims: Vec<String>,
    pub producer_id: String,
    pub evaluator_id: String,
    pub authority_witness_id: String,
    pub human_promotion_artifact_present: bool,
    pub promotion_constructor_available: bool,
    pub authorized_local_result_constructor_available: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda7MemberReceiptV1 {
    pub sequence: u32,
    pub member_id: String,
    pub operation: Coda7MigrationOperationV1,
    pub source_path: String,
    pub source_sha256: String,
    pub target_path: String,
    pub target_sha256: String,
    pub dependency_ids: Vec<String>,
    pub source_consumed_once: bool,
    pub target_produced_once: bool,
    pub content_preserved: bool,
    pub external_import_used: bool,
    pub residual_ids: Vec<String>,
    pub claimed_terminal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Coda7SurvivorRouteV1 {
    HumanDecision,
    ProofObligation,
    OracleNeeded,
    LiftLicenseNeeded,
    TypedRefusal,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda7ResidualLedgerEntryV1 {
    pub residual_id: String,
    pub scope: String,
    pub terminal: CodaTerminal,
    pub survivor_route: Coda7SurvivorRouteV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda7MigrationReceiptV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub producer_id: String,
    pub predecessor_receipts_verified: bool,
    pub predecessor_human_promotion_recorded: bool,
    pub member_receipts: Vec<Coda7MemberReceiptV1>,
    pub residual_ledger: Vec<Coda7ResidualLedgerEntryV1>,
    pub claimed_terminal: CodaTerminal,
    pub workspace_mutated: bool,
    pub wildcard_discovery_used: bool,
    pub external_imports_used: bool,
    pub promotion_requested: bool,
    pub promotion_constructor_called: bool,
    pub authorized_local_result_created: bool,
    pub nonclaims: Vec<String>,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda7MemberVerificationV1 {
    pub sequence: u32,
    pub member_id: String,
    pub kind: Coda7ArtifactKindV1,
    pub source_path: String,
    pub target_path: String,
    pub dependencies_closed: bool,
    pub source_hash_verified: bool,
    pub target_hash_verified: bool,
    pub content_preserved: bool,
    pub terminal: CodaTerminal,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda7MigrationVerificationV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub observer_sha256: String,
    pub receipt_sha256: String,
    pub source_manifest_sha256: String,
    pub predecessor_manifest_sha256: String,
    pub path_policy_sha256: String,
    pub member_registry_sha256: String,
    pub before_snapshot_sha256: String,
    pub after_snapshot_sha256: String,
    pub member_receipts_sha256: String,
    pub residual_ledger_sha256: String,
    pub evaluator_id: String,
    pub authority_witness_id: String,
    pub source_count: u32,
    pub predecessor_count: u32,
    pub member_count: u32,
    pub dependency_edge_count: u32,
    pub residual_count: u32,
    pub member_evidence: Vec<Coda7MemberVerificationV1>,
    pub source_manifest_bound: bool,
    pub every_predecessor_hash_verified: bool,
    pub predecessor_semantics_verified: bool,
    pub predecessor_human_promotion_recorded: bool,
    pub exact_member_bijection_verified: bool,
    pub every_member_hash_verified: bool,
    pub every_dependency_closed: bool,
    pub path_policy_verified: bool,
    pub no_hidden_additions: bool,
    pub every_local_terminal_recomputed: bool,
    pub every_residual_conserved: bool,
    pub historical_s06_004_receipt_outside_write_surface: bool,
    pub residual_ids: Vec<String>,
    pub nonclaims: Vec<String>,
    pub terminal: CodaTerminal,
    pub workspace_mutated: bool,
    pub promotion_requested: bool,
    pub promotion_constructor_called: bool,
    pub authorized_local_result_created: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum Coda7Error {
    #[error("the packet differs from the frozen S03-002 packet")]
    PacketDrift,
    #[error("the frozen packet boundary changed: {0}")]
    PacketBoundaryChanged(String),
    #[error("the receipt does not bind to the frozen packet")]
    ReceiptBindingMismatch,
    #[error("verification attempted to expand authority")]
    AuthorityExpanded,
    #[error("missing frozen predecessor artifact: {0}")]
    MissingPredecessorArtifact(String),
    #[error("the frozen predecessor artifact set changed")]
    PredecessorSetMismatch,
    #[error("predecessor artifact length mismatch: {0}")]
    PredecessorLengthMismatch(String),
    #[error("predecessor artifact hash mismatch: {0}")]
    PredecessorHashMismatch(String),
    #[error("invalid predecessor receipt: {0}")]
    InvalidPredecessor(String),
    #[error("path is not an exact canonical in-memory snapshot identifier in {field}: {path}")]
    NonCanonicalPath { field: &'static str, path: String },
    #[error("wildcard or member discovery is forbidden")]
    WildcardDiscoveryForbidden,
    #[error("external import is outside this carrier: {0}")]
    ExternalImportRequested(String),
    #[error("unsupported migration operation for {0}")]
    UnsupportedMigration(String),
    #[error("member count mismatch: expected {expected}, found {found}")]
    MemberCountMismatch { expected: usize, found: usize },
    #[error("member attribution mismatch: {0}")]
    MemberAttributionMismatch(String),
    #[error("duplicate member id or path: {0}")]
    DuplicateMember(String),
    #[error("member path escapes its exact root: {0}")]
    PathPolicyViolation(String),
    #[error("member artifact kind/path mismatch: {0}")]
    ArtifactKindMismatch(String),
    #[error("dependency closure mismatch: {0}")]
    DependencyClosureMismatch(String),
    #[error("missing {phase} member snapshot: {path}")]
    MissingMemberSnapshot { phase: &'static str, path: String },
    #[error("the {0} member snapshot set changed")]
    MemberSetMismatch(&'static str),
    #[error("member length mismatch: {0}")]
    MemberLengthMismatch(String),
    #[error("member hash mismatch: {0}")]
    MemberHashMismatch(String),
    #[error("member content was not byte-preserved: {0}")]
    ContentNotPreserved(String),
    #[error("member receipt mismatch: {0}")]
    MemberReceiptMismatch(String),
    #[error("residual ledger mismatch")]
    ResidualLedgerMismatch,
    #[error("aggregate terminal mismatch: expected {expected:?}, found {found:?}")]
    AggregateTerminalMismatch {
        expected: CodaTerminal,
        found: CodaTerminal,
    },
    #[error("empty required field: {0}")]
    EmptyField(&'static str),
    #[error("invalid lowercase SHA-256 in {0}")]
    InvalidSha256(&'static str),
    #[error("list is not strictly sorted and unique: {0}")]
    NonCanonicalList(&'static str),
    #[error("JSON operation failed: {0}")]
    Json(String),
    #[error("JSON input is invalid: {0}")]
    Decode(String),
    #[error("{0} is not canonical JSONL")]
    NonCanonicalJson(String),
}

impl Coda7Error {
    pub fn terminal_route(&self) -> CodaTerminal {
        match self {
            Self::MissingPredecessorArtifact(_) | Self::Json(_) => {
                CodaTerminal::InfrastructureFailure
            }
            Self::ExternalImportRequested(_) => CodaTerminal::OracleNeeded,
            Self::UnsupportedMigration(_) => CodaTerminal::LiftLicenseNeeded,
            Self::AuthorityExpanded => CodaTerminal::Refused,
            _ => CodaTerminal::Invalid,
        }
    }
}

pub fn canonical_s03_002_source_manifest_v1() -> Vec<FrozenCoda7SourceV1> {
    S03_002_SOURCE_MANIFEST
        .iter()
        .map(|(path, sha256, bytes)| FrozenCoda7SourceV1 {
            path: (*path).to_owned(),
            sha256: (*sha256).to_owned(),
            bytes: *bytes,
        })
        .collect()
}

pub fn canonical_s03_002_packet_v1() -> Coda7MigrationPacketV1 {
    let source_manifest = canonical_s03_002_source_manifest_v1();
    let predecessors = canonical_predecessors_v1();
    let members = canonical_members_v1();
    let path_policy = Coda7PathPolicyV1 {
        policy_id: S03_002_PATH_POLICY_ID.to_owned(),
        member_storage: Coda7MemberStorageV1::InMemorySnapshot,
        source_root: S03_002_SOURCE_ROOT.to_owned(),
        target_root: S03_002_TARGET_ROOT.to_owned(),
        exact_pairs: members
            .iter()
            .map(|member| Coda7PathPairV1 {
                sequence: member.sequence,
                member_id: member.member_id.clone(),
                source_path: member.source_path.clone(),
                target_path: member.target_path.clone(),
            })
            .collect(),
        wildcard_members_allowed: false,
        member_discovery_allowed: false,
        external_imports_allowed: false,
    };
    let observer = FrozenCoda7ObserverV1 {
        observer_id: S03_002_EVALUATOR_ID.to_owned(),
        source_manifest_sha256: sha256_json_v1(&source_manifest)
            .checked_invariant_1ec30bbc("frozen source manifest must serialize"),
        predecessor_manifest_sha256: sha256_json_v1(&predecessors)
            .checked_invariant_1ec30bbc("frozen predecessor manifest must serialize"),
        visible_source_sha256: source_manifest
            .iter()
            .map(|source| source.sha256.clone())
            .collect(),
        visible_artifact_sha256: predecessors
            .iter()
            .map(|artifact| artifact.sha256.clone())
            .collect(),
        hidden_context_classes: vec![
            "arbitrary_repository_members".to_owned(),
            "external_imports".to_owned(),
            "human_promotion_record".to_owned(),
            "model_context".to_owned(),
            "promotion_constructor".to_owned(),
            "wildcard_member_discovery".to_owned(),
        ],
        model_context_available: false,
        member_discovery_available: false,
        promotion_constructor_available: false,
        authorized_local_result_constructor_available: false,
        authority_effect: AuthorityEffect::None,
    };
    let observer_sha256 = sha256_json_v1(&observer)
        .checked_invariant_1ec30bbc("frozen observer must serialize deterministically");
    Coda7MigrationPacketV1 {
        schema_version: CODA7_PACKET_SCHEMA_VERSION.to_owned(),
        packet_id: S03_002_PACKET_ID.to_owned(),
        goal_id: S03_002_GOAL_ID.to_owned(),
        frozen_base: S03_002_FROZEN_BASE.to_owned(),
        observer,
        observer_sha256,
        source_manifest,
        predecessors,
        path_policy,
        members,
        legal_terminals: CodaTerminal::ALL.to_vec(),
        budgets: Coda7BudgetsV1 {
            attempt_budget: 1,
            repair_budget: 2,
            successor_budget: 1,
            time_budget_seconds: 28_800,
            process_budget: 4,
            token_budget: 200_000,
            member_budget: 3,
            dependency_budget: 3,
            residual_budget: 2,
        },
        evidence_ceiling: S03_002_EVIDENCE_CEILING.to_owned(),
        exact_write_surface: S03_002_WRITE_SURFACE
            .iter()
            .map(|path| (*path).to_owned())
            .collect(),
        nonclaims: canonical_nonclaims_v1(),
        producer_id: S03_002_PRODUCER_ID.to_owned(),
        evaluator_id: S03_002_EVALUATOR_ID.to_owned(),
        authority_witness_id: S03_002_AUTHORITY_WITNESS_ID.to_owned(),
        human_promotion_artifact_present: false,
        promotion_constructor_available: false,
        authorized_local_result_constructor_available: false,
        authority_effect: AuthorityEffect::None,
    }
}

pub fn canonical_s03_002_receipt_v1() -> Result<Coda7MigrationReceiptV1, Coda7Error> {
    let packet = canonical_s03_002_packet_v1();
    let member_receipts = packet
        .members
        .iter()
        .map(|member| Coda7MemberReceiptV1 {
            sequence: member.sequence,
            member_id: member.member_id.clone(),
            operation: member.operation,
            source_path: member.source_path.clone(),
            source_sha256: member.source_sha256.clone(),
            target_path: member.target_path.clone(),
            target_sha256: member.target_sha256.clone(),
            dependency_ids: member.dependency_ids.clone(),
            source_consumed_once: true,
            target_produced_once: true,
            content_preserved: true,
            external_import_used: false,
            residual_ids: Vec::new(),
            claimed_terminal: CodaTerminal::ExactRepair,
            authority_effect: AuthorityEffect::None,
        })
        .collect::<Vec<_>>();
    Ok(Coda7MigrationReceiptV1 {
        schema_version: CODA7_RECEIPT_SCHEMA_VERSION.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256: coda7_packet_sha256_v1(&packet)?,
        producer_id: packet.producer_id.clone(),
        predecessor_receipts_verified: true,
        predecessor_human_promotion_recorded: false,
        member_receipts,
        residual_ledger: canonical_residual_ledger_v1(),
        claimed_terminal: CodaTerminal::StabilizedSurvivor,
        workspace_mutated: false,
        wildcard_discovery_used: false,
        external_imports_used: false,
        promotion_requested: false,
        promotion_constructor_called: false,
        authorized_local_result_created: false,
        nonclaims: packet.nonclaims.clone(),
        authority_effect: AuthorityEffect::None,
    })
}

pub fn canonical_s03_002_replay_artifacts_v1() -> Coda7ReplayArtifactsV1 {
    let mut predecessor_artifacts = BTreeMap::new();
    predecessor_artifacts.insert(
        S03_001_RECEIPT_PATH.to_owned(),
        S03_001_RECEIPT_BYTES.to_vec(),
    );
    predecessor_artifacts.insert(
        S06_003_VERIFICATION_PATH.to_owned(),
        S06_003_VERIFICATION_BYTES.to_vec(),
    );
    let mut before_members = BTreeMap::new();
    let mut after_members = BTreeMap::new();
    for (sequence, extension, bytes) in canonical_member_material_v1() {
        before_members.insert(
            member_path_v1(S03_002_SOURCE_ROOT, sequence, extension),
            bytes.to_vec(),
        );
        after_members.insert(
            member_path_v1(S03_002_TARGET_ROOT, sequence, extension),
            bytes.to_vec(),
        );
    }
    Coda7ReplayArtifactsV1 {
        predecessor_artifacts,
        before_members,
        after_members,
    }
}

pub fn canonical_s03_002_verification_v1() -> Result<Coda7MigrationVerificationV1, Coda7Error> {
    verify_coda7_migration_bundle_v1(
        &canonical_s03_002_packet_v1(),
        &canonical_s03_002_receipt_v1()?,
        &canonical_s03_002_replay_artifacts_v1(),
    )
}

pub fn validate_coda7_packet_v1(packet: &Coda7MigrationPacketV1) -> Result<(), Coda7Error> {
    validate_packet_header_and_identities(packet)?;
    validate_packet_authority_flags(packet)?;
    validate_packet_observer_binding(packet)?;
    validate_source_manifest_v1(&packet.source_manifest)?;
    validate_predecessor_bindings_v1(&packet.predecessors)?;
    validate_path_policy_and_members_v1(packet)?;
    validate_packet_surfaces_and_budgets(packet)
}

fn validate_packet_header_and_identities(
    packet: &Coda7MigrationPacketV1,
) -> Result<(), Coda7Error> {
    for (field, value) in [
        ("packet_id", packet.packet_id.as_str()),
        ("goal_id", packet.goal_id.as_str()),
        ("producer_id", packet.producer_id.as_str()),
        ("evaluator_id", packet.evaluator_id.as_str()),
        ("authority_witness_id", packet.authority_witness_id.as_str()),
        ("evidence_ceiling", packet.evidence_ceiling.as_str()),
    ] {
        require_text(field, value)?;
    }
    if !packet_constants_match(packet) {
        return Err(Coda7Error::PacketBoundaryChanged(
            "schema, identity, base, ceiling, or terminal vocabulary".to_owned(),
        ));
    }
    if !packet_identities_distinct(packet) {
        return Err(Coda7Error::PacketBoundaryChanged(
            "witness identities are not pairwise distinct".to_owned(),
        ));
    }
    Ok(())
}

fn packet_constants_match(packet: &Coda7MigrationPacketV1) -> bool {
    packet.schema_version == CODA7_PACKET_SCHEMA_VERSION
        && packet.packet_id == S03_002_PACKET_ID
        && packet.goal_id == S03_002_GOAL_ID
        && packet.frozen_base == S03_002_FROZEN_BASE
        && packet.evidence_ceiling == S03_002_EVIDENCE_CEILING
        && packet.legal_terminals == CodaTerminal::ALL
}

fn packet_identities_distinct(packet: &Coda7MigrationPacketV1) -> bool {
    packet.producer_id != packet.evaluator_id
        && packet.producer_id != packet.authority_witness_id
        && packet.evaluator_id != packet.authority_witness_id
        && packet.observer.observer_id == packet.evaluator_id
}

fn validate_packet_authority_flags(packet: &Coda7MigrationPacketV1) -> Result<(), Coda7Error> {
    let packet_expanded = !packet.authority_effect.is_none()
        || packet.human_promotion_artifact_present
        || packet.promotion_constructor_available
        || packet.authorized_local_result_constructor_available;
    let observer_expanded = !packet.observer.authority_effect.is_none()
        || packet.observer.model_context_available
        || packet.observer.member_discovery_available
        || packet.observer.promotion_constructor_available
        || packet
            .observer
            .authorized_local_result_constructor_available;
    if packet_expanded || observer_expanded {
        return Err(Coda7Error::AuthorityExpanded);
    }
    Ok(())
}

fn validate_packet_observer_binding(packet: &Coda7MigrationPacketV1) -> Result<(), Coda7Error> {
    let visible_sources = packet
        .source_manifest
        .iter()
        .map(|source| source.sha256.clone())
        .collect::<Vec<_>>();
    let visible_artifacts = packet
        .predecessors
        .iter()
        .map(|artifact| artifact.sha256.clone())
        .collect::<Vec<_>>();
    if packet.observer_sha256 != coda7_observer_sha256_v1(&packet.observer)?
        || packet.observer.source_manifest_sha256 != sha256_json_v1(&packet.source_manifest)?
        || packet.observer.predecessor_manifest_sha256 != sha256_json_v1(&packet.predecessors)?
        || packet.observer.visible_source_sha256 != visible_sources
        || packet.observer.visible_artifact_sha256 != visible_artifacts
    {
        return Err(Coda7Error::PacketBoundaryChanged(
            "observer binding".to_owned(),
        ));
    }
    Ok(())
}

fn validate_packet_surfaces_and_budgets(packet: &Coda7MigrationPacketV1) -> Result<(), Coda7Error> {
    validate_sorted_exact_paths_v1("exact_write_surface", &packet.exact_write_surface)?;
    let expected_writes = S03_002_WRITE_SURFACE
        .iter()
        .map(|path| (*path).to_owned())
        .collect::<Vec<_>>();
    let expected_budgets = Coda7BudgetsV1 {
        attempt_budget: 1,
        repair_budget: 2,
        successor_budget: 1,
        time_budget_seconds: 28_800,
        process_budget: 4,
        token_budget: 200_000,
        member_budget: 3,
        dependency_budget: 3,
        residual_budget: 2,
    };
    if packet.exact_write_surface != expected_writes
        || packet.nonclaims != canonical_nonclaims_v1()
        || packet.budgets != expected_budgets
    {
        return Err(Coda7Error::PacketBoundaryChanged(
            "write surface, nonclaims, or budgets".to_owned(),
        ));
    }
    Ok(())
}

pub fn verify_coda7_migration_bundle_v1(
    packet: &Coda7MigrationPacketV1,
    receipt: &Coda7MigrationReceiptV1,
    artifacts: &Coda7ReplayArtifactsV1,
) -> Result<Coda7MigrationVerificationV1, Coda7Error> {
    validate_coda7_packet_v1(packet)?;
    if packet != &canonical_s03_002_packet_v1() {
        return Err(Coda7Error::PacketDrift);
    }
    let packet_sha256 = coda7_packet_sha256_v1(packet)?;
    validate_coda7_receipt_header_and_flags(packet, receipt, &packet_sha256)?;
    verify_predecessors_v1(packet, &artifacts.predecessor_artifacts)?;
    let (member_evidence, before_snapshot_sha256, after_snapshot_sha256) =
        verify_members_v1(packet, receipt, artifacts)?;
    let terminal = verify_residuals_and_terminal_v1(packet, receipt, &member_evidence)?;
    build_coda7_verification_v1(
        packet,
        packet_sha256,
        receipt,
        before_snapshot_sha256,
        after_snapshot_sha256,
        member_evidence,
        terminal,
    )
}

fn build_coda7_verification_v1(
    packet: &Coda7MigrationPacketV1,
    packet_sha256: String,
    receipt: &Coda7MigrationReceiptV1,
    before_snapshot_sha256: String,
    after_snapshot_sha256: String,
    member_evidence: Vec<Coda7MemberVerificationV1>,
    terminal: CodaTerminal,
) -> Result<Coda7MigrationVerificationV1, Coda7Error> {
    let residual_ids = receipt
        .residual_ledger
        .iter()
        .map(|entry| entry.residual_id.clone())
        .collect::<Vec<_>>();
    let dependency_edge_count = packet
        .members
        .iter()
        .map(|member| member.dependency_ids.len() as u32)
        .sum();
    Ok(Coda7MigrationVerificationV1 {
        schema_version: CODA7_VERIFICATION_SCHEMA_VERSION.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256,
        observer_sha256: packet.observer_sha256.clone(),
        receipt_sha256: coda7_receipt_sha256_v1(receipt)?,
        source_manifest_sha256: sha256_json_v1(&packet.source_manifest)?,
        predecessor_manifest_sha256: sha256_json_v1(&packet.predecessors)?,
        path_policy_sha256: sha256_json_v1(&packet.path_policy)?,
        member_registry_sha256: sha256_json_v1(&packet.members)?,
        before_snapshot_sha256,
        after_snapshot_sha256,
        member_receipts_sha256: sha256_json_v1(&receipt.member_receipts)?,
        residual_ledger_sha256: sha256_json_v1(&receipt.residual_ledger)?,
        evaluator_id: packet.evaluator_id.clone(),
        authority_witness_id: packet.authority_witness_id.clone(),
        source_count: packet.source_manifest.len() as u32,
        predecessor_count: packet.predecessors.len() as u32,
        member_count: packet.members.len() as u32,
        dependency_edge_count,
        residual_count: residual_ids.len() as u32,
        member_evidence,
        source_manifest_bound: true,
        every_predecessor_hash_verified: true,
        predecessor_semantics_verified: true,
        predecessor_human_promotion_recorded: false,
        exact_member_bijection_verified: true,
        every_member_hash_verified: true,
        every_dependency_closed: true,
        path_policy_verified: true,
        no_hidden_additions: true,
        every_local_terminal_recomputed: true,
        every_residual_conserved: true,
        historical_s06_004_receipt_outside_write_surface: !packet
            .exact_write_surface
            .iter()
            .any(|path| path == S06_004_HISTORICAL_RECEIPT_PATH),
        residual_ids,
        nonclaims: packet.nonclaims.clone(),
        terminal,
        workspace_mutated: false,
        promotion_requested: false,
        promotion_constructor_called: false,
        authorized_local_result_created: false,
        authority_effect: AuthorityEffect::None,
    })
}

fn validate_coda7_receipt_header_and_flags(
    packet: &Coda7MigrationPacketV1,
    receipt: &Coda7MigrationReceiptV1,
    packet_sha256: &str,
) -> Result<(), Coda7Error> {
    if receipt.schema_version != CODA7_RECEIPT_SCHEMA_VERSION
        || receipt.packet_id != packet.packet_id
        || receipt.packet_sha256 != packet_sha256
        || receipt.producer_id != packet.producer_id
        || !receipt.predecessor_receipts_verified
        || receipt.predecessor_human_promotion_recorded
        || receipt.nonclaims != packet.nonclaims
    {
        return Err(Coda7Error::ReceiptBindingMismatch);
    }
    validate_coda7_receipt_prohibitions(receipt)
}

fn validate_coda7_receipt_prohibitions(
    receipt: &Coda7MigrationReceiptV1,
) -> Result<(), Coda7Error> {
    if !receipt.authority_effect.is_none()
        || receipt.promotion_requested
        || receipt.promotion_constructor_called
        || receipt.authorized_local_result_created
        || receipt.workspace_mutated
    {
        return Err(Coda7Error::AuthorityExpanded);
    }
    if receipt.wildcard_discovery_used {
        return Err(Coda7Error::WildcardDiscoveryForbidden);
    }
    if receipt.external_imports_used {
        return Err(Coda7Error::ExternalImportRequested(
            "receipt declared an external import".to_owned(),
        ));
    }
    Ok(())
}

fn verify_residuals_and_terminal_v1(
    packet: &Coda7MigrationPacketV1,
    receipt: &Coda7MigrationReceiptV1,
    member_evidence: &[Coda7MemberVerificationV1],
) -> Result<CodaTerminal, Coda7Error> {
    let expected_residuals = canonical_residual_ledger_v1();
    if receipt.residual_ledger != expected_residuals
        || receipt.residual_ledger.len() > packet.budgets.residual_budget as usize
    {
        return Err(Coda7Error::ResidualLedgerMismatch);
    }
    let mut local_terminals = member_evidence
        .iter()
        .map(|member| member.terminal)
        .collect::<Vec<_>>();
    local_terminals.extend(receipt.residual_ledger.iter().map(|entry| entry.terminal));
    let terminal = aggregate_coda6_terminals_v1(&local_terminals)
        .map_err(|error| Coda7Error::PacketBoundaryChanged(error.to_string()))?;
    if receipt.claimed_terminal != terminal {
        return Err(Coda7Error::AggregateTerminalMismatch {
            expected: terminal,
            found: receipt.claimed_terminal,
        });
    }
    Ok(terminal)
}

pub fn coda7_packet_sha256_v1(packet: &Coda7MigrationPacketV1) -> Result<String, Coda7Error> {
    sha256_json_v1(packet)
}

pub fn coda7_receipt_sha256_v1(receipt: &Coda7MigrationReceiptV1) -> Result<String, Coda7Error> {
    sha256_json_v1(receipt)
}

pub fn coda7_verification_sha256_v1(
    verification: &Coda7MigrationVerificationV1,
) -> Result<String, Coda7Error> {
    sha256_json_v1(verification)
}

pub fn coda7_observer_sha256_v1(observer: &FrozenCoda7ObserverV1) -> Result<String, Coda7Error> {
    sha256_json_v1(observer)
}

pub fn canonical_coda7_json_line_v1<T: Serialize + ?Sized>(
    value: &T,
) -> Result<Vec<u8>, Coda7Error> {
    let mut bytes = serde_json::to_vec(value).map_err(json_error)?;
    bytes.push(b'\n');
    Ok(bytes)
}

pub fn parse_coda7_packet_canonical_v1(bytes: &[u8]) -> Result<Coda7MigrationPacketV1, Coda7Error> {
    parse_canonical_json_line_v1(bytes, "GTOC-7 packet")
}

pub fn parse_coda7_receipt_canonical_v1(
    bytes: &[u8],
) -> Result<Coda7MigrationReceiptV1, Coda7Error> {
    parse_canonical_json_line_v1(bytes, "GTOC-7 receipt")
}

pub fn parse_coda7_verification_canonical_v1(
    bytes: &[u8],
) -> Result<Coda7MigrationVerificationV1, Coda7Error> {
    parse_canonical_json_line_v1(bytes, "GTOC-7 verification")
}

fn canonical_predecessors_v1() -> Vec<Coda7ArtifactBindingV1> {
    vec![
        Coda7ArtifactBindingV1 {
            artifact_id: "predecessor:s03-001:task-admission-receipt".to_owned(),
            path: S03_001_RECEIPT_PATH.to_owned(),
            sha256: sha256_bytes_v1(S03_001_RECEIPT_BYTES),
            bytes: S03_001_RECEIPT_BYTES.len() as u64,
            terminal: CodaTerminal::ExactRepair,
            human_promotion_recorded: false,
            authority_effect: AuthorityEffect::None,
        },
        Coda7ArtifactBindingV1 {
            artifact_id: "predecessor:s06-003:gtoc6-verification".to_owned(),
            path: S06_003_VERIFICATION_PATH.to_owned(),
            sha256: sha256_bytes_v1(S06_003_VERIFICATION_BYTES),
            bytes: S06_003_VERIFICATION_BYTES.len() as u64,
            terminal: CodaTerminal::StabilizedSurvivor,
            human_promotion_recorded: false,
            authority_effect: AuthorityEffect::None,
        },
    ]
}

fn canonical_members_v1() -> Vec<Coda7MemberSpecV1> {
    canonical_member_material_v1()
        .into_iter()
        .map(|(sequence, extension, bytes)| {
            let kind = match extension {
                "md" => Coda7ArtifactKindV1::Markdown,
                "rs" => Coda7ArtifactKindV1::Rust,
                "json" => Coda7ArtifactKindV1::Json,
                _ => unreachable!("canonical carrier has three exhaustive kinds"),
            };
            Coda7MemberSpecV1 {
                sequence,
                member_id: format!("member:s03-002:{sequence:02}"),
                kind,
                operation: Coda7MigrationOperationV1::BytePreservingRelocation,
                source_path: member_path_v1(S03_002_SOURCE_ROOT, sequence, extension),
                source_sha256: sha256_bytes_v1(bytes),
                source_bytes: bytes.len() as u64,
                target_path: member_path_v1(S03_002_TARGET_ROOT, sequence, extension),
                target_sha256: sha256_bytes_v1(bytes),
                target_bytes: bytes.len() as u64,
                dependency_ids: match sequence {
                    0 => Vec::new(),
                    1 => vec!["member:s03-002:00".to_owned()],
                    2 => vec![
                        "member:s03-002:00".to_owned(),
                        "member:s03-002:01".to_owned(),
                    ],
                    _ => unreachable!("canonical carrier has exactly three members"),
                },
                path_policy_id: S03_002_PATH_POLICY_ID.to_owned(),
                expected_terminal: CodaTerminal::ExactRepair,
            }
        })
        .collect()
}

fn canonical_member_material_v1() -> Vec<(u32, &'static str, &'static [u8])> {
    vec![
        (0, "md", MEMBER_00_BYTES),
        (1, "rs", MEMBER_01_BYTES),
        (2, "json", MEMBER_02_BYTES),
    ]
}

fn canonical_residual_ledger_v1() -> Vec<Coda7ResidualLedgerEntryV1> {
    vec![
        Coda7ResidualLedgerEntryV1 {
            residual_id: S03_002_PREDECESSOR_RESIDUAL_ID.to_owned(),
            scope: "S03-001 and S06-003 receipts are verified evidence but have no human-promotion record"
                .to_owned(),
            terminal: CodaTerminal::OpenObstruction,
            survivor_route: Coda7SurvivorRouteV1::HumanDecision,
        },
        Coda7ResidualLedgerEntryV1 {
            residual_id: S03_002_UNRESTRICTED_FAMILY_RESIDUAL_ID.to_owned(),
            scope: "the finite three-member carrier does not prove unrestricted migration-bundle preservation"
                .to_owned(),
            terminal: CodaTerminal::OpenObstruction,
            survivor_route: Coda7SurvivorRouteV1::ProofObligation,
        },
    ]
}

fn canonical_nonclaims_v1() -> Vec<String> {
    vec![
        "does not authorize arbitrary repository moves or wildcard members".to_owned(),
        "does not import external artifacts or prove unrestricted GTOC-7".to_owned(),
        "does not mutate a workspace, activate a gate, or instantiate a successor".to_owned(),
        "does not record human promotion, create AuthorizedLocalResult, or mint authority"
            .to_owned(),
        "does not bind or replay the historical S06-004 receipt fixture, whose path is outside this packet's exact write surface"
            .to_owned(),
    ]
}

fn validate_source_manifest_v1(sources: &[FrozenCoda7SourceV1]) -> Result<(), Coda7Error> {
    if sources != canonical_s03_002_source_manifest_v1() {
        return Err(Coda7Error::PacketBoundaryChanged(
            "source manifest closure".to_owned(),
        ));
    }
    let mut previous: Option<&str> = None;
    let mut folded_paths = BTreeSet::new();
    for source in sources {
        require_canonical_snapshot_path("source_manifest.path", &source.path)?;
        require_sha256("source_manifest.sha256", &source.sha256)?;
        if source.bytes == 0
            || previous.is_some_and(|value| value >= source.path.as_str())
            || !folded_paths.insert(source.path.to_ascii_lowercase())
        {
            return Err(Coda7Error::PacketBoundaryChanged(
                "source manifest ordering, case-fold uniqueness, or byte length".to_owned(),
            ));
        }
        previous = Some(&source.path);
    }
    Ok(())
}

fn validate_predecessor_bindings_v1(
    predecessors: &[Coda7ArtifactBindingV1],
) -> Result<(), Coda7Error> {
    if predecessors.len() != 2 {
        return Err(Coda7Error::PacketBoundaryChanged(
            "predecessor count".to_owned(),
        ));
    }
    let mut previous_id: Option<&str> = None;
    let mut paths = BTreeSet::new();
    for predecessor in predecessors {
        validate_single_predecessor_binding(predecessor, previous_id, &mut paths)?;
        previous_id = Some(&predecessor.artifact_id);
    }
    Ok(())
}

fn validate_single_predecessor_binding(
    predecessor: &Coda7ArtifactBindingV1,
    previous_id: Option<&str>,
    paths: &mut BTreeSet<String>,
) -> Result<(), Coda7Error> {
    require_text("predecessor.artifact_id", &predecessor.artifact_id)?;
    require_canonical_snapshot_path("predecessor.path", &predecessor.path)?;
    require_sha256("predecessor.sha256", &predecessor.sha256)?;
    let invalid_order_or_path = previous_id
        .is_some_and(|value| value >= predecessor.artifact_id.as_str())
        || !paths.insert(predecessor.path.to_ascii_lowercase());
    let invalid_flags = predecessor.bytes == 0
        || predecessor.human_promotion_recorded
        || !predecessor.authority_effect.is_none();
    if invalid_order_or_path || invalid_flags {
        return Err(Coda7Error::PacketBoundaryChanged(
            "predecessor binding".to_owned(),
        ));
    }
    Ok(())
}

fn validate_path_policy_and_members_v1(packet: &Coda7MigrationPacketV1) -> Result<(), Coda7Error> {
    let policy = &packet.path_policy;
    validate_path_policy_header(policy)?;
    if packet.members.len() != packet.budgets.member_budget as usize
        || policy.exact_pairs.len() != packet.members.len()
    {
        return Err(Coda7Error::MemberCountMismatch {
            expected: packet.budgets.member_budget as usize,
            found: packet.members.len(),
        });
    }
    let mut ids = BTreeSet::new();
    let mut source_paths = BTreeSet::new();
    let mut target_paths = BTreeSet::new();
    let mut dependency_edges = 0_usize;
    for (index, (member, pair)) in packet.members.iter().zip(&policy.exact_pairs).enumerate() {
        validate_member_spec_and_pair(index, member, pair, policy)?;
        record_member_uniqueness_and_roots(
            member,
            policy,
            &mut ids,
            &mut source_paths,
            &mut target_paths,
        )?;
        validate_kind_extension_v1(member)?;
        dependency_edges += count_and_validate_member_dependencies(member, &ids)?;
    }
    if dependency_edges > packet.budgets.dependency_budget as usize {
        return Err(Coda7Error::DependencyClosureMismatch(
            "dependency budget".to_owned(),
        ));
    }
    Ok(())
}

fn validate_path_policy_header(policy: &Coda7PathPolicyV1) -> Result<(), Coda7Error> {
    require_text("path_policy.policy_id", &policy.policy_id)?;
    validate_canonical_root("path_policy.source_root", &policy.source_root)?;
    validate_canonical_root("path_policy.target_root", &policy.target_root)?;
    if policy.wildcard_members_allowed || policy.member_discovery_allowed {
        return Err(Coda7Error::WildcardDiscoveryForbidden);
    }
    if policy.external_imports_allowed {
        return Err(Coda7Error::ExternalImportRequested(
            "path policy permits external imports".to_owned(),
        ));
    }
    if !path_policy_constants_match(policy) {
        return Err(Coda7Error::PacketBoundaryChanged(
            "path policy identity or roots".to_owned(),
        ));
    }
    Ok(())
}

fn path_policy_constants_match(policy: &Coda7PathPolicyV1) -> bool {
    policy.policy_id == S03_002_PATH_POLICY_ID
        && policy.member_storage == Coda7MemberStorageV1::InMemorySnapshot
        && policy.source_root == S03_002_SOURCE_ROOT
        && policy.target_root == S03_002_TARGET_ROOT
}

fn validate_member_spec_and_pair(
    index: usize,
    member: &Coda7MemberSpecV1,
    pair: &Coda7PathPairV1,
    policy: &Coda7PathPolicyV1,
) -> Result<(), Coda7Error> {
    require_text("member.member_id", &member.member_id)?;
    require_canonical_snapshot_path("member.source_path", &member.source_path)?;
    require_canonical_snapshot_path("member.target_path", &member.target_path)?;
    require_sha256("member.source_sha256", &member.source_sha256)?;
    require_sha256("member.target_sha256", &member.target_sha256)?;
    if member.operation == Coda7MigrationOperationV1::UnsupportedTransformation {
        return Err(Coda7Error::UnsupportedMigration(member.member_id.clone()));
    }
    if !member_pair_matches_spec(index, member, pair, policy)
        || !member_bytes_and_hashes_match(member)
    {
        return Err(Coda7Error::MemberAttributionMismatch(
            member.member_id.clone(),
        ));
    }
    Ok(())
}

fn member_pair_matches_spec(
    index: usize,
    member: &Coda7MemberSpecV1,
    pair: &Coda7PathPairV1,
    policy: &Coda7PathPolicyV1,
) -> bool {
    member.sequence as usize == index
        && pair.sequence == member.sequence
        && pair.member_id == member.member_id
        && pair.source_path == member.source_path
        && pair.target_path == member.target_path
        && member.path_policy_id == policy.policy_id
}

fn member_bytes_and_hashes_match(member: &Coda7MemberSpecV1) -> bool {
    member.source_bytes != 0
        && member.target_bytes != 0
        && member.source_bytes == member.target_bytes
        && member.source_sha256 == member.target_sha256
        && member.expected_terminal == CodaTerminal::ExactRepair
}

fn record_member_uniqueness_and_roots(
    member: &Coda7MemberSpecV1,
    policy: &Coda7PathPolicyV1,
    ids: &mut BTreeSet<String>,
    source_paths: &mut BTreeSet<String>,
    target_paths: &mut BTreeSet<String>,
) -> Result<(), Coda7Error> {
    let source_lower = member.source_path.to_ascii_lowercase();
    let target_lower = member.target_path.to_ascii_lowercase();
    let unique = ids.insert(member.member_id.clone())
        && source_paths.insert(source_lower.clone())
        && target_paths.insert(target_lower.clone())
        && !source_paths.contains(&target_lower)
        && !target_paths.contains(&source_lower);
    if !unique {
        return Err(Coda7Error::DuplicateMember(member.member_id.clone()));
    }
    if !member.source_path.starts_with(&policy.source_root)
        || !member.target_path.starts_with(&policy.target_root)
        || member.source_path == member.target_path
    {
        return Err(Coda7Error::PathPolicyViolation(member.member_id.clone()));
    }
    Ok(())
}

fn count_and_validate_member_dependencies(
    member: &Coda7MemberSpecV1,
    ids: &BTreeSet<String>,
) -> Result<usize, Coda7Error> {
    let mut previous_dependency: Option<&str> = None;
    for dependency_id in &member.dependency_ids {
        if dependency_id == &member.member_id
            || previous_dependency.is_some_and(|value| value >= dependency_id.as_str())
            || !ids.contains(dependency_id)
        {
            return Err(Coda7Error::DependencyClosureMismatch(
                member.member_id.clone(),
            ));
        }
        previous_dependency = Some(dependency_id);
    }
    Ok(member.dependency_ids.len())
}

fn validate_kind_extension_v1(member: &Coda7MemberSpecV1) -> Result<(), Coda7Error> {
    let extension = match member.kind {
        Coda7ArtifactKindV1::Markdown => ".md",
        Coda7ArtifactKindV1::Rust => ".rs",
        Coda7ArtifactKindV1::Json => ".json",
    };
    if !member.source_path.ends_with(extension) || !member.target_path.ends_with(extension) {
        return Err(Coda7Error::ArtifactKindMismatch(member.member_id.clone()));
    }
    Ok(())
}

fn verify_predecessors_v1(
    packet: &Coda7MigrationPacketV1,
    artifacts: &Coda7ArtifactMapV1,
) -> Result<(), Coda7Error> {
    verify_predecessor_paths_and_hashes(packet, artifacts)?;
    verify_s03_predecessor_receipt(artifacts)?;
    verify_s06_predecessor_verification(artifacts)
}

fn verify_predecessor_paths_and_hashes(
    packet: &Coda7MigrationPacketV1,
    artifacts: &Coda7ArtifactMapV1,
) -> Result<(), Coda7Error> {
    let expected_paths = packet
        .predecessors
        .iter()
        .map(|artifact| artifact.path.as_str())
        .collect::<BTreeSet<_>>();
    let found_paths = artifacts
        .keys()
        .map(String::as_str)
        .collect::<BTreeSet<_>>();
    if expected_paths != found_paths {
        if let Some(path) = expected_paths.difference(&found_paths).next() {
            return Err(Coda7Error::MissingPredecessorArtifact((*path).to_owned()));
        }
        return Err(Coda7Error::PredecessorSetMismatch);
    }
    for binding in &packet.predecessors {
        let bytes = artifacts
            .get(&binding.path)
            .ok_or_else(|| Coda7Error::MissingPredecessorArtifact(binding.path.clone()))?;
        if bytes.len() as u64 != binding.bytes {
            return Err(Coda7Error::PredecessorLengthMismatch(binding.path.clone()));
        }
        if sha256_bytes_v1(bytes) != binding.sha256 {
            return Err(Coda7Error::PredecessorHashMismatch(binding.path.clone()));
        }
    }
    Ok(())
}

fn verify_s03_predecessor_receipt(artifacts: &Coda7ArtifactMapV1) -> Result<(), Coda7Error> {
    let s03_receipt = serde_json::from_slice::<TaskAdmissionReceiptV1>(
        artifacts.get(S03_001_RECEIPT_PATH).ok_or_else(|| {
            Coda7Error::MissingPredecessorArtifact(S03_001_RECEIPT_PATH.to_owned())
        })?,
    )
    .map_err(decode_error)?;
    s03_receipt
        .validate()
        .map_err(|error| Coda7Error::InvalidPredecessor(error.to_string()))?;
    if s03_receipt.terminal != CodaTerminal::ExactRepair || !s03_receipt.authority_effect.is_none()
    {
        return Err(Coda7Error::InvalidPredecessor(
            "S03-001 admission boundary mismatch".to_owned(),
        ));
    }
    Ok(())
}

fn verify_s06_predecessor_verification(artifacts: &Coda7ArtifactMapV1) -> Result<(), Coda7Error> {
    let coda6 = parse_coda6_verification_canonical_v1(
        artifacts.get(S06_003_VERIFICATION_PATH).ok_or_else(|| {
            Coda7Error::MissingPredecessorArtifact(S06_003_VERIFICATION_PATH.to_owned())
        })?,
    )
    .map_err(|error| Coda7Error::InvalidPredecessor(error.to_string()))?;
    if !coda6_invariants_hold(&coda6) || !coda6_authority_boundary_holds(&coda6) {
        return Err(Coda7Error::InvalidPredecessor(
            "S06-003 verification boundary mismatch".to_owned(),
        ));
    }
    Ok(())
}

fn coda6_invariants_hold(
    coda6: &crate::coda6_defect_terminalization::Coda6DefectTerminalizationVerificationV1,
) -> bool {
    coda6.terminal == CodaTerminal::StabilizedSurvivor
        && coda6.every_defect_classified_once
        && coda6.every_subclaim_classified_once
        && coda6.every_local_terminal_recomputed
        && coda6.every_residual_conserved
        && coda6.aggregation_truth_table_replayed
        && coda6.aggregation_permutation_invariant
        && coda6.predecessor_receipt_verified
}

fn coda6_authority_boundary_holds(
    coda6: &crate::coda6_defect_terminalization::Coda6DefectTerminalizationVerificationV1,
) -> bool {
    !coda6.promotion_requested
        && !coda6.promotion_constructor_called
        && !coda6.authorized_local_result_created
        && coda6.authority_effect.is_none()
}

fn verify_members_v1(
    packet: &Coda7MigrationPacketV1,
    receipt: &Coda7MigrationReceiptV1,
    artifacts: &Coda7ReplayArtifactsV1,
) -> Result<(Vec<Coda7MemberVerificationV1>, String, String), Coda7Error> {
    if receipt.member_receipts.len() != packet.members.len() {
        return Err(Coda7Error::MemberCountMismatch {
            expected: packet.members.len(),
            found: receipt.member_receipts.len(),
        });
    }
    verify_snapshot_set_v1("before", &packet.members, &artifacts.before_members, true)?;
    verify_snapshot_set_v1("after", &packet.members, &artifacts.after_members, false)?;
    let mut evidence = Vec::with_capacity(packet.members.len());
    for (member, member_receipt) in packet.members.iter().zip(&receipt.member_receipts) {
        evidence.push(verify_single_member_v1(member, member_receipt, artifacts)?);
    }
    Ok((
        evidence,
        snapshot_sha256_v1(&artifacts.before_members)?,
        snapshot_sha256_v1(&artifacts.after_members)?,
    ))
}

fn verify_single_member_v1(
    member: &Coda7MemberSpecV1,
    member_receipt: &Coda7MemberReceiptV1,
    artifacts: &Coda7ReplayArtifactsV1,
) -> Result<Coda7MemberVerificationV1, Coda7Error> {
    if member_receipt.external_import_used {
        return Err(Coda7Error::ExternalImportRequested(
            member.member_id.clone(),
        ));
    }
    if !member_receipt_identity_matches(member, member_receipt)
        || !member_receipt_outcomes_match(member, member_receipt)
    {
        return Err(Coda7Error::MemberReceiptMismatch(member.member_id.clone()));
    }
    let source = artifacts
        .before_members
        .get(&member.source_path)
        .checked_invariant_1ec30bbc("snapshot set was verified");
    let target = artifacts
        .after_members
        .get(&member.target_path)
        .checked_invariant_1ec30bbc("snapshot set was verified");
    if source != target {
        return Err(Coda7Error::ContentNotPreserved(member.member_id.clone()));
    }
    Ok(Coda7MemberVerificationV1 {
        sequence: member.sequence,
        member_id: member.member_id.clone(),
        kind: member.kind,
        source_path: member.source_path.clone(),
        target_path: member.target_path.clone(),
        dependencies_closed: true,
        source_hash_verified: true,
        target_hash_verified: true,
        content_preserved: true,
        terminal: CodaTerminal::ExactRepair,
    })
}

fn member_receipt_identity_matches(
    member: &Coda7MemberSpecV1,
    member_receipt: &Coda7MemberReceiptV1,
) -> bool {
    member_receipt.sequence == member.sequence
        && member_receipt.member_id == member.member_id
        && member_receipt.operation == member.operation
        && member_receipt.source_path == member.source_path
        && member_receipt.source_sha256 == member.source_sha256
        && member_receipt.target_path == member.target_path
        && member_receipt.target_sha256 == member.target_sha256
        && member_receipt.dependency_ids == member.dependency_ids
}

fn member_receipt_outcomes_match(
    member: &Coda7MemberSpecV1,
    member_receipt: &Coda7MemberReceiptV1,
) -> bool {
    member_receipt.source_consumed_once
        && member_receipt.target_produced_once
        && member_receipt.content_preserved
        && member_receipt.residual_ids.is_empty()
        && member_receipt.claimed_terminal == member.expected_terminal
        && member_receipt.authority_effect.is_none()
}

fn verify_snapshot_set_v1(
    phase: &'static str,
    members: &[Coda7MemberSpecV1],
    snapshot: &Coda7ArtifactMapV1,
    before: bool,
) -> Result<(), Coda7Error> {
    let expected_paths = members
        .iter()
        .map(|member| {
            if before {
                member.source_path.as_str()
            } else {
                member.target_path.as_str()
            }
        })
        .collect::<BTreeSet<_>>();
    let found_paths = snapshot.keys().map(String::as_str).collect::<BTreeSet<_>>();
    if expected_paths != found_paths {
        if let Some(path) = expected_paths.difference(&found_paths).next() {
            return Err(Coda7Error::MissingMemberSnapshot {
                phase,
                path: (*path).to_owned(),
            });
        }
        return Err(Coda7Error::MemberSetMismatch(phase));
    }
    for member in members {
        let (path, expected_hash, expected_bytes) = if before {
            (
                &member.source_path,
                &member.source_sha256,
                member.source_bytes,
            )
        } else {
            (
                &member.target_path,
                &member.target_sha256,
                member.target_bytes,
            )
        };
        let bytes = snapshot
            .get(path)
            .checked_invariant_1ec30bbc("snapshot set was verified");
        if bytes.len() as u64 != expected_bytes {
            return Err(Coda7Error::MemberLengthMismatch(path.clone()));
        }
        if sha256_bytes_v1(bytes) != *expected_hash {
            return Err(Coda7Error::MemberHashMismatch(path.clone()));
        }
    }
    Ok(())
}

#[derive(Serialize)]
struct SnapshotBindingV1<'a> {
    path: &'a str,
    sha256: String,
    bytes: u64,
}

fn snapshot_sha256_v1(snapshot: &Coda7ArtifactMapV1) -> Result<String, Coda7Error> {
    let bindings = snapshot
        .iter()
        .map(|(path, bytes)| SnapshotBindingV1 {
            path,
            sha256: sha256_bytes_v1(bytes),
            bytes: bytes.len() as u64,
        })
        .collect::<Vec<_>>();
    sha256_json_v1(&bindings)
}

fn member_path_v1(root: &str, sequence: u32, extension: &str) -> String {
    format!("{root}member_{sequence:02}.{extension}")
}

fn validate_canonical_root(field: &'static str, root: &str) -> Result<(), Coda7Error> {
    if !root.ends_with('/') || root.ends_with("//") {
        return Err(Coda7Error::NonCanonicalPath {
            field,
            path: root.to_owned(),
        });
    }
    require_canonical_snapshot_path(field, root.trim_end_matches('/'))
}

fn validate_sorted_exact_paths_v1(field: &'static str, paths: &[String]) -> Result<(), Coda7Error> {
    if paths.is_empty() {
        return Err(Coda7Error::EmptyField(field));
    }
    let mut previous: Option<&str> = None;
    let mut folded = BTreeSet::new();
    for path in paths {
        require_canonical_snapshot_path(field, path)?;
        if previous.is_some_and(|value| value >= path.as_str())
            || !folded.insert(path.to_ascii_lowercase())
        {
            return Err(Coda7Error::NonCanonicalList(field));
        }
        previous = Some(path);
    }
    Ok(())
}

fn require_canonical_snapshot_path(field: &'static str, path: &str) -> Result<(), Coda7Error> {
    if snapshot_path_has_forbidden_syntax(path) || path.split('/').any(snapshot_segment_is_invalid)
    {
        return Err(Coda7Error::NonCanonicalPath {
            field,
            path: path.to_owned(),
        });
    }
    Ok(())
}

fn snapshot_path_has_forbidden_syntax(path: &str) -> bool {
    path.is_empty()
        || path.trim() != path
        || !path.is_ascii()
        || path.starts_with('/')
        || path.contains('\\')
        || path.contains(':')
        || path
            .chars()
            .any(|character| character.is_control() || "*?[]{}".contains(character))
}

fn snapshot_segment_is_invalid(segment: &str) -> bool {
    segment.is_empty()
        || segment == "."
        || segment == ".."
        || segment.trim() != segment
        || segment.ends_with('.')
        || is_windows_device_segment(segment)
}

fn is_windows_device_segment(segment: &str) -> bool {
    let stem = segment
        .split('.')
        .next()
        .unwrap_or(segment)
        .trim_end_matches(' ')
        .to_ascii_lowercase();
    matches!(stem.as_str(), "con" | "prn" | "aux" | "nul")
        || (stem.len() == 4
            && (stem.starts_with("com") || stem.starts_with("lpt"))
            && matches!(stem.as_bytes()[3], b'1'..=b'9'))
}

fn require_text(field: &'static str, value: &str) -> Result<(), Coda7Error> {
    if value.trim().is_empty() {
        return Err(Coda7Error::EmptyField(field));
    }
    Ok(())
}

fn require_sha256(field: &'static str, value: &str) -> Result<(), Coda7Error> {
    if value.len() != 64
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(Coda7Error::InvalidSha256(field));
    }
    Ok(())
}

fn parse_canonical_json_line_v1<T>(bytes: &[u8], label: &str) -> Result<T, Coda7Error>
where
    T: DeserializeOwned + Serialize,
{
    if bytes.len() < 2 || bytes.last() != Some(&b'\n') || bytes[..bytes.len() - 1].contains(&b'\n')
    {
        return Err(Coda7Error::NonCanonicalJson(label.to_owned()));
    }
    let value = serde_json::from_slice::<T>(&bytes[..bytes.len() - 1]).map_err(decode_error)?;
    if canonical_coda7_json_line_v1(&value)? != bytes {
        return Err(Coda7Error::NonCanonicalJson(label.to_owned()));
    }
    Ok(value)
}

fn sha256_json_v1<T: Serialize + ?Sized>(value: &T) -> Result<String, Coda7Error> {
    let bytes = serde_json::to_vec(value).map_err(json_error)?;
    Ok(sha256_bytes_v1(&bytes))
}

fn sha256_bytes_v1(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}

fn json_error(error: serde_json::Error) -> Coda7Error {
    Coda7Error::Json(error.to_string())
}

fn decode_error(error: serde_json::Error) -> Coda7Error {
    Coda7Error::Decode(error.to_string())
}

// Backward compatibility aliases

// Origin: vendor/engine/engine_state/src/coda7_migration_bundle.rs
// Claim: urn:omega:crates_rs:omega-state:coda7-migration-bundle:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: no source-bound mutation campaign run for this repair; ratio=null.

#[cfg(test)]
mod workspace_repair_tests {
    use super::*;

    #[test]
    fn canonical_snapshot_paths_refuse_windows_separators_and_traversal() {
        for path in [
            r"before\member.rs",
            "../member.rs",
            "/absolute.rs",
            "a//b",
            "a/CON.rs",
            "a/*.rs",
        ] {
            assert!(
                require_canonical_snapshot_path("test", path).is_err(),
                "{path}"
            );
        }
        assert!(require_canonical_snapshot_path("test", "before/member.rs").is_ok());
    }

    #[test]
    fn canonical_replay_verifies_actual_finite_member_bytes() {
        assert!(canonical_s03_002_verification_v1().is_ok());
        let packet = canonical_s03_002_packet_v1();
        let receipt = canonical_s03_002_receipt_v1().unwrap();
        let mut artifacts = canonical_s03_002_replay_artifacts_v1();
        let (_, bytes) = artifacts.after_members.iter_mut().next().unwrap();
        bytes.push(b'!');
        assert!(verify_coda7_migration_bundle_v1(&packet, &receipt, &artifacts).is_err());
    }

    #[test]
    fn a_receipt_cannot_authorize_promotion_or_workspace_mutation() {
        let packet = canonical_s03_002_packet_v1();
        let artifacts = canonical_s03_002_replay_artifacts_v1();
        let mut receipt = canonical_s03_002_receipt_v1().unwrap();
        receipt.promotion_requested = true;
        assert!(verify_coda7_migration_bundle_v1(&packet, &receipt, &artifacts).is_err());
        receipt.promotion_requested = false;
        receipt.workspace_mutated = true;
        assert!(verify_coda7_migration_bundle_v1(&packet, &receipt, &artifacts).is_err());
    }
}
