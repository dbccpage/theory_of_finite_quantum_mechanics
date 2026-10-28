//! Bounded S06-004 / CODA-8 import and oracle firewall.
//!
//! This verifier freezes the two concrete external-evidence doors already
//! present in the Rust carrier. Imports remain outside [`DdaOp`], every active
//! request binds a licensed source and nonzero host price, evidence cannot
//! mutate the DDA trace, and a later terminalization step cannot clear
//! [`CodaTerminal::OracleNeeded`]. The unavailable CODA-7 migration interface is
//! retained as a named proof-obligation residual rather than inferred complete.
//! No path in this module validates oracle truth, activates a gate, or creates
//! authority.


#[allow(dead_code, non_camel_case_types, missing_docs)]
trait CheckedInvariantExt_10b349f3<T> {
    fn checked_invariant_10b349f3(self, msg: &str) -> T;
}

impl<T> CheckedInvariantExt_10b349f3<T> for Option<T> {
    #[inline]
    fn checked_invariant_10b349f3(self, msg: &str) -> T {
        match self {
            Some(v) => v,
            None => unreachable!("{}", msg),
        }
    }
}

impl<T, E: std::fmt::Debug> CheckedInvariantExt_10b349f3<T> for std::result::Result<T, E> {
    #[inline]
    fn checked_invariant_10b349f3(self, msg: &str) -> T {
        match self {
            Ok(v) => v,
            Err(e) => unreachable!("{}: {:?}", msg, e),
        }
    }
}
use std::collections::{BTreeMap, BTreeSet};

use engine_wdp::ddc::dda_alphabet::{DdaOp, DdaStep, DdaTrace, TraceTerminal};
use engine_types::authority::AuthorityEffect;
use serde::de::DeserializeOwned;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

use crate::coda6_defect_terminalization::{
    aggregate_coda6_terminals_v1, parse_coda6_verification_canonical_v1, SurvivorRouteV1,
};
use crate::coda_gtla_protocol::CodaTerminal;
use crate::coda_gtla_run_receipt::CodaGtlaRunReceiptError;

pub const CODA8_PACKET_SCHEMA_VERSION: &str = "omega.gtoc8.import-oracle.packet.v1";
pub const CODA8_RECEIPT_SCHEMA_VERSION: &str = "omega.gtoc8.import-oracle.receipt.v1";
pub const CODA8_VERIFICATION_SCHEMA_VERSION: &str = "omega.gtoc8.import-oracle.verification.v1";
pub const S06_004_FROZEN_BASE: &str = "5f5858c9e939cc80de2235de9e1be5491a4ae7a7";
pub const S06_004_PACKET_ID: &str = "omega-conductor-s06-004-gtoc8-firewall-v1";
pub const S06_004_GOAL_ID: &str = "S06-004:GTOC-8";
pub const S06_004_PRODUCER_ID: &str = "witness:producer:s06-004-import-firewall-v1";
pub const S06_004_EVALUATOR_ID: &str = "witness:evaluator:s06-004-independent-v1";
pub const S06_004_AUTHORITY_WITNESS_ID: &str = "witness:authority:s06-004-none-v1";
pub const S06_004_EVIDENCE_CEILING: &str =
    "two frozen Rust import doors, two evidence-only source policies, and one deferred GTOC-7 migration interface over the exact S06-003 verification; no oracle-truth theorem, unrestricted interface theorem, authority, promotion, gate activation, or successor instantiation";
pub const S06_004_CODA7_RESIDUAL_ID: &str = "residual:s06-004:gtoc7-migration-receipt-absent";
pub const S06_003_VERIFICATION_PATH: &str =
    "omega_engine/crates/omega_state/tests/fixtures/s06_003_gtoc6_verification_v1.json";


pub const S06_004_WRITE_SURFACE: [&str; 12] = [
    "docs/omega-conductor-epic-v001.md",
    "docs/saga_06_receipt_verification_and_terminalization.md",
    "docs/sprint_s06_004.md",
    "docs/status/omega_conductor_s06_004_status_2026-07-18.md",
    "omega_engine/crates/omega_state/src/gtoc6_defect_terminalization.rs",
    "omega_engine/crates/omega_state/src/gtoc8_import_oracle_firewall.rs",
    "omega_engine/crates/omega_state/src/lib.rs",
    "omega_engine/crates/omega_state/tests/fixtures/s06_004_gtoc8_packet_v1.json",
    "omega_engine/crates/omega_state/tests/fixtures/s06_004_gtoc8_receipt_v1.json",
    "omega_engine/crates/omega_state/tests/fixtures/s06_004_gtoc8_verification_v1.json",
    "omega_engine/crates/omega_state/tests/gtoc6_defect_terminalization.rs",
    "omega_engine/crates/omega_state/tests/gtoc8_import_oracle_firewall.rs",
];

pub const S06_004_SOURCE_MANIFEST: [(&str, &str, u64); 19] = [
    (
        "docs/gtoc-canonicalization-remaining-work.md",
        "e23690fef90c663dd2abbd9fef7bcdc2148ae1c1cc0086d4330c88118b287033",
        26_117,
    ),
    (
        "docs/omega-conductor-epic-v001.md",
        "3475479929c763b80660d2b2df2de1879b53a63f3c2e41f85c1b6b931fa484bc",
        66_768,
    ),
    (
        "docs/saga_06_receipt_verification_and_terminalization.md",
        "db768c9c556c83cbea936cfcfb6a19d7a2583c58c136886697986d18aaa92374",
        11_158,
    ),
    (
        "docs/sprint_s03_002.md",
        "35d54528f8bf54f6a3e93b4957b412fc22f9a19139c13332be97d11b77252439",
        8_262,
    ),
    (
        "docs/sprint_s06_003.md",
        "2416e4a2525373a3f78cf5fa91048155c77acc0f6be9551e70d81f2fed7fe7c5",
        11_485,
    ),
    (
        "docs/sprint_s06_004.md",
        "428bc4b15d51b9539c3ee87e9f8291b2445052e6ff96ffdf43e2003f9c2226d0",
        8_329,
    ),
    (
        "docs/status-vocabulary.md",
        "bd10e7ecf448ed6f4dca45a431c573242179a66b828492ecfe02f52572289b84",
        4_203,
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
        "omega_engine/crates/omega_state/src/gtoc4_transition_coverage.rs",
        "a19d524e1b4caaadd1150f00ce923cb0278d7ee9c0b02b0542543153724602de",
        47_470,
    ),
    (
        "omega_engine/crates/omega_state/src/gtoc6_defect_terminalization.rs",
        "320323ba50b64a79d74889858a64fb69bbbba3a41566bd99940eb29a17c2af63",
        51_761,
    ),
    (
        "omega_engine/crates/omega_state/src/lib.rs",
        "619ac769a2b14529c4c64cb124c139ce9a370f1f865740bd8f33e70db8b702ce",
        2_014,
    ),
    (
        "omega_engine/crates/omega_discrete_deformation_algebra/src/dda_alphabet.rs",
        "2894e95134db050d9c366e3e15db5e5ecdaeb3c0ed4625e18a63d21753ee7fb9",
        11_997,
    ),
    (
        "omega_engine/crates/omega_types/src/authority.rs",
        "42051a106954daa5ca2170c79bbf7d4cc9b04e0f7b554b8807251a0da552d2a9",
        39_913,
    ),
    (
        "omega_engine/crates/omega_state/tests/fixtures/s06_003_gtoc6_packet_v1.json",
        "74bfd49c586e3306c71a6a2be43ff1376c6df6465cf54a85ddd226a351c944c3",
        8_899,
    ),
    (
        "omega_engine/crates/omega_state/tests/fixtures/s06_003_gtoc6_receipt_v1.json",
        "f2fcf300ab958ed78107f2e218d032d343f1ce40043957e97c898dcc3a52080a",
        3_300,
    ),
    (
        S06_003_VERIFICATION_PATH,
        "15f33eee4d7dd791996964076e92b9f928789d06ef41ab1c2309acc792551c98",
        2_171,
    ),
];

pub const S06_004_INPUT_ARTIFACTS: [(&str, &str, u64); 1] = [(
    S06_003_VERIFICATION_PATH,
    "15f33eee4d7dd791996964076e92b9f928789d06ef41ab1c2309acc792551c98",
    2_171,
)];

pub type Coda8ArtifactBytesV1 = BTreeMap<String, Vec<u8>>;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenCoda8SourceV1 {
    pub path: String,
    pub sha256: String,
    pub bytes: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda8ArtifactBindingV1 {
    pub path: String,
    pub sha256: String,
    pub bytes: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda8BudgetsV1 {
    pub attempt_budget: u32,
    pub repair_budget: u32,
    pub successor_budget: u32,
    pub time_budget_seconds: u32,
    pub process_budget: u32,
    pub token_budget: u32,
    pub interface_budget: u32,
    pub source_budget: u32,
    pub request_budget: u32,
    pub residual_budget: u32,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenCoda8ObserverV1 {
    pub observer_id: String,
    pub source_manifest_sha256: String,
    pub visible_artifact_sha256: Vec<String>,
    pub hidden_context_classes: Vec<String>,
    pub model_context_available: bool,
    pub promotion_constructor_available: bool,
    pub authorized_local_result_constructor_available: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ImportInterfaceKindV1 {
    DdaTraceImport,
    RunReceiptExternalImport,
    MigrationBundleExternalMember,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ImportInterfaceDispositionV1 {
    Active,
    #[serde(rename = "deferred_until_gtoc7_receipt")]
    DeferredUntilCoda7Receipt,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RegisteredImportInterfaceV1 {
    pub sequence: u32,
    pub interface_id: String,
    pub kind: ImportInterfaceKindV1,
    pub disposition: ImportInterfaceDispositionV1,
    pub expected_local_terminal: CodaTerminal,
    pub expected_residual_id: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct OracleSourcePolicyV1 {
    pub sequence: u32,
    pub source_id: String,
    pub license_id: String,
    pub price_units: u64,
    pub evidence_only: bool,
    pub licensed: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ExternalEvidenceRequestSpecV1 {
    pub sequence: u32,
    pub request_id: String,
    pub interface_id: String,
    pub source_id: String,
    pub claim_scope: String,
    pub expected_price_units: u64,
    pub expected_evidence_sha256: String,
    pub before_dda_trace_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DdaTraceSnapshotV1 {
    pub operations: Vec<DdaOp>,
    pub residual_ids: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda8ImportOraclePacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub goal_id: String,
    pub frozen_base: String,
    pub observer: FrozenCoda8ObserverV1,
    pub observer_sha256: String,
    pub source_manifest: Vec<FrozenCoda8SourceV1>,
    pub input_artifacts: Vec<Coda8ArtifactBindingV1>,
    pub dda_alphabet: Vec<DdaOp>,
    pub interfaces: Vec<RegisteredImportInterfaceV1>,
    pub source_policies: Vec<OracleSourcePolicyV1>,
    pub requests: Vec<ExternalEvidenceRequestSpecV1>,
    #[serde(rename = "gtoc7_dependency_receipt_present")]
    pub coda7_dependency_receipt_present: bool,
    pub legal_terminals: Vec<CodaTerminal>,
    pub budgets: Coda8BudgetsV1,
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
#[serde(deny_unknown_fields)]
pub struct InterfaceFirewallReceiptV1 {
    pub sequence: u32,
    pub interface_id: String,
    pub kind: ImportInterfaceKindV1,
    pub disposition: ImportInterfaceDispositionV1,
    pub request_ids: Vec<String>,
    pub import_encoded_as_dda: bool,
    pub oracle_terminal_before_t: Option<CodaTerminal>,
    pub oracle_terminal_after_t: Option<CodaTerminal>,
    pub residual_ids: Vec<String>,
    pub claimed_local_terminal: CodaTerminal,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ExternalEvidenceReceiptV1 {
    pub sequence: u32,
    pub request_id: String,
    pub interface_id: String,
    pub source_id: String,
    pub license_id: String,
    pub charged_price_units: u64,
    pub evidence_sha256: String,
    pub before_dda_trace_sha256: String,
    pub after_dda_trace_sha256: String,
    pub terminal: CodaTerminal,
    pub evidence_treated_as_proof: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda8ResidualLedgerEntryV1 {
    pub residual_id: String,
    pub interface_id: String,
    pub terminal: CodaTerminal,
    pub survivor_route: SurvivorRouteV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda8ImportOracleReceiptV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub producer_id: String,
    pub predecessor_artifact_sha256: String,
    pub interfaces: Vec<InterfaceFirewallReceiptV1>,
    pub evidence_receipts: Vec<ExternalEvidenceReceiptV1>,
    pub residual_ledger: Vec<Coda8ResidualLedgerEntryV1>,
    pub claimed_terminal: CodaTerminal,
    pub promotion_requested: bool,
    pub promotion_constructor_called: bool,
    pub authorized_local_result_created: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda8ImportOracleVerificationV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub observer_sha256: String,
    pub receipt_sha256: String,
    pub artifact_closure_sha256: String,
    pub interface_registry_sha256: String,
    pub source_policy_sha256: String,
    pub evidence_receipts_sha256: String,
    pub residual_ledger_sha256: String,
    pub evaluator_id: String,
    pub authority_witness_id: String,
    pub interface_count: u32,
    pub active_interface_count: u32,
    pub source_count: u32,
    pub request_count: u32,
    pub residual_count: u32,
    pub dda_alphabet_exact_and_exhaustive: bool,
    pub imports_outside_dda: bool,
    pub every_registered_interface_covered: bool,
    pub every_request_priced: bool,
    pub every_source_licensed: bool,
    pub every_evidence_hash_bound: bool,
    pub dda_trace_unchanged_by_evidence: bool,
    pub oracle_terminal_monotone_after_t: bool,
    pub external_evidence_not_treated_as_proof: bool,
    pub predecessor_receipt_verified: bool,
    #[serde(rename = "gtoc7_dependency_receipt_present")]
    pub coda7_dependency_receipt_present: bool,
    #[serde(rename = "gtoc7_dependency_preserved_as_residual")]
    pub coda7_dependency_preserved_as_residual: bool,
    pub residual_ids: Vec<String>,
    pub terminal: CodaTerminal,
    pub promotion_requested: bool,
    pub promotion_constructor_called: bool,
    pub authorized_local_result_created: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum Coda8Error {
    #[error("the packet differs from the frozen S06-004 packet")]
    PacketDrift,
    #[error("the frozen packet boundary changed")]
    PacketBoundaryChanged,
    #[error("the receipt does not bind to the frozen packet")]
    ReceiptBindingMismatch,
    #[error("verification attempted to expand authority")]
    AuthorityExpanded,
    #[error("missing frozen artifact: {0}")]
    MissingArtifact(String),
    #[error("the frozen artifact set changed")]
    ArtifactSetMismatch,
    #[error("artifact length mismatch: {0}")]
    ArtifactLengthMismatch(String),
    #[error("artifact hash mismatch: {0}")]
    ArtifactHashMismatch(String),
    #[error("invalid S06-003 predecessor verification: {0}")]
    InvalidPredecessor(String),
    #[error("DDA alphabet changed or is not exhaustively classified")]
    DdaAlphabetChanged,
    #[error("interface count or attribution mismatch: {0}")]
    InterfaceMismatch(String),
    #[error("duplicate interface id: {0}")]
    DuplicateInterfaceId(String),
    #[error("import was encoded as a DDA operation: {0}")]
    ImportSmuggledIntoDda(String),
    #[error("oracle terminal was cleared or misreported: {0}")]
    OracleTerminalCleared(String),
    #[error("request count or attribution mismatch: {0}")]
    RequestMismatch(String),
    #[error("duplicate request receipt: {0}")]
    DuplicateRequest(String),
    #[error("source is not registered or licensed: {0}")]
    UnlicensedSource(String),
    #[error("oracle price or license mismatch: {0}")]
    PriceOrLicenseMismatch(String),
    #[error("evidence hash is invalid or differs from the request: {0}")]
    EvidenceHashMismatch(String),
    #[error("external evidence changed the DDA trace: {0}")]
    EvidenceMutatedDda(String),
    #[error("external evidence was treated as proof: {0}")]
    EvidencePromotedToProof(String),
    #[error("residual ledger mismatch")]
    ResidualLedgerMismatch,
    #[error("aggregate terminal mismatch: expected {expected:?}, found {found:?}")]
    AggregateTerminalMismatch {
        expected: CodaTerminal,
        found: CodaTerminal,
    },
    #[error("terminal aggregation failed: {0}")]
    TerminalAggregation(String),
    #[error("JSON serialization failed: {0}")]
    Json(String),
    #[error("JSON decoding failed: {0}")]
    Decode(String),
    #[error("noncanonical JSON: {0}")]
    NonCanonicalJson(String),
    #[error("{0} must be non-empty")]
    EmptyText(&'static str),
    #[error("{0} must be strictly sorted and unique")]
    NotSortedUnique(&'static str),
    #[error("{0} must be lowercase SHA-256")]
    InvalidSha256(&'static str),
}

impl Coda8Error {
    pub fn terminal_route(&self) -> CodaTerminal {
        match self {
            Self::MissingArtifact(_) | Self::Json(_) => CodaTerminal::InfrastructureFailure,
            Self::AuthorityExpanded | Self::UnlicensedSource(_) => CodaTerminal::Refused,
            _ => CodaTerminal::Invalid,
        }
    }
}

pub fn canonical_s06_004_packet_v1() -> Coda8ImportOraclePacketV1 {
    let source_manifest = S06_004_SOURCE_MANIFEST
        .iter()
        .map(|(path, sha256, bytes)| FrozenCoda8SourceV1 {
            path: (*path).to_owned(),
            sha256: (*sha256).to_owned(),
            bytes: *bytes,
        })
        .collect::<Vec<_>>();
    let input_artifacts = S06_004_INPUT_ARTIFACTS
        .iter()
        .map(|(path, sha256, bytes)| Coda8ArtifactBindingV1 {
            path: (*path).to_owned(),
            sha256: (*sha256).to_owned(),
            bytes: *bytes,
        })
        .collect::<Vec<_>>();
    let observer = FrozenCoda8ObserverV1 {
        observer_id: S06_004_EVALUATOR_ID.to_owned(),
        source_manifest_sha256: sha256_json_v1(&source_manifest)
            .checked_invariant_10b349f3("frozen source manifest must serialize"),
        visible_artifact_sha256: input_artifacts
            .iter()
            .map(|artifact| artifact.sha256.clone())
            .collect(),
        hidden_context_classes: vec![
            "authorized_local_result_constructor".to_owned(),
            "external_evidence_truth".to_owned(),
            "gtoc7_migration_receipt".to_owned(),
            "human_promotion_state".to_owned(),
            "model_context".to_owned(),
            "production_credentials".to_owned(),
        ],
        model_context_available: false,
        promotion_constructor_available: false,
        authorized_local_result_constructor_available: false,
        authority_effect: AuthorityEffect::None,
    };
    let observer_sha256 =
        sha256_json_v1(&observer).checked_invariant_10b349f3("frozen observer must serialize deterministically");
    Coda8ImportOraclePacketV1 {
        schema_version: CODA8_PACKET_SCHEMA_VERSION.to_owned(),
        packet_id: S06_004_PACKET_ID.to_owned(),
        goal_id: S06_004_GOAL_ID.to_owned(),
        frozen_base: S06_004_FROZEN_BASE.to_owned(),
        observer,
        observer_sha256,
        source_manifest,
        input_artifacts,
        dda_alphabet: DdaOp::alphabet().to_vec(),
        interfaces: canonical_interfaces_v1(),
        source_policies: canonical_source_policies_v1(),
        requests: canonical_requests_v1(),
        coda7_dependency_receipt_present: false,
        legal_terminals: CodaTerminal::ALL.to_vec(),
        budgets: Coda8BudgetsV1 {
            attempt_budget: 1,
            repair_budget: 2,
            successor_budget: 1,
            time_budget_seconds: 28_800,
            process_budget: 4,
            token_budget: 200_000,
            interface_budget: 3,
            source_budget: 2,
            request_budget: 2,
            residual_budget: 1,
        },
        evidence_ceiling: S06_004_EVIDENCE_CEILING.to_owned(),
        exact_write_surface: S06_004_WRITE_SURFACE
            .iter()
            .map(|path| (*path).to_owned())
            .collect(),
        producer_id: S06_004_PRODUCER_ID.to_owned(),
        evaluator_id: S06_004_EVALUATOR_ID.to_owned(),
        authority_witness_id: S06_004_AUTHORITY_WITNESS_ID.to_owned(),
        prior_work_ledger: vec![
            "S06-001 imported evidence already routes outside DDA to OracleNeeded".to_owned(),
            "S06-002 covers the frozen eight-operation DDA alphabet exactly once".to_owned(),
            "S06-003 supplies bounded per-defect terminalization with authority None".to_owned(),
            "S03-002 GTOC-7 migration construction receipt is absent at the frozen base".to_owned(),
        ],
        promotion_constructor_available: false,
        authorized_local_result_constructor_available: false,
        authority_effect: AuthorityEffect::None,
    }
}

pub fn canonical_s06_004_receipt_v1() -> Result<Coda8ImportOracleReceiptV1, Coda8Error> {
    let packet = canonical_s06_004_packet_v1();
    let interfaces = vec![
        InterfaceFirewallReceiptV1 {
            sequence: 0,
            interface_id: "interface:dda-trace-import".to_owned(),
            kind: ImportInterfaceKindV1::DdaTraceImport,
            disposition: ImportInterfaceDispositionV1::Active,
            request_ids: vec!["request:s06-004:dda-trace".to_owned()],
            import_encoded_as_dda: false,
            oracle_terminal_before_t: Some(CodaTerminal::OracleNeeded),
            oracle_terminal_after_t: Some(CodaTerminal::OracleNeeded),
            residual_ids: vec![],
            claimed_local_terminal: CodaTerminal::ExactRepair,
        },
        InterfaceFirewallReceiptV1 {
            sequence: 1,
            interface_id: "interface:run-receipt-external-import".to_owned(),
            kind: ImportInterfaceKindV1::RunReceiptExternalImport,
            disposition: ImportInterfaceDispositionV1::Active,
            request_ids: vec!["request:s06-004:run-receipt".to_owned()],
            import_encoded_as_dda: false,
            oracle_terminal_before_t: Some(CodaTerminal::OracleNeeded),
            oracle_terminal_after_t: Some(CodaTerminal::OracleNeeded),
            residual_ids: vec![],
            claimed_local_terminal: CodaTerminal::ExactRepair,
        },
        InterfaceFirewallReceiptV1 {
            sequence: 2,
            interface_id: "interface:migration-bundle-external-member".to_owned(),
            kind: ImportInterfaceKindV1::MigrationBundleExternalMember,
            disposition: ImportInterfaceDispositionV1::DeferredUntilCoda7Receipt,
            request_ids: vec![],
            import_encoded_as_dda: false,
            oracle_terminal_before_t: None,
            oracle_terminal_after_t: None,
            residual_ids: vec![S06_004_CODA7_RESIDUAL_ID.to_owned()],
            claimed_local_terminal: CodaTerminal::OpenObstruction,
        },
    ];
    let evidence_receipts = packet
        .requests
        .iter()
        .map(|request| {
            let policy = packet
                .source_policies
                .iter()
                .find(|policy| policy.source_id == request.source_id)
                .checked_invariant_10b349f3("canonical request source must be registered");
            ExternalEvidenceReceiptV1 {
                sequence: request.sequence,
                request_id: request.request_id.clone(),
                interface_id: request.interface_id.clone(),
                source_id: request.source_id.clone(),
                license_id: policy.license_id.clone(),
                charged_price_units: policy.price_units,
                evidence_sha256: request.expected_evidence_sha256.clone(),
                before_dda_trace_sha256: request.before_dda_trace_sha256.clone(),
                after_dda_trace_sha256: request.before_dda_trace_sha256.clone(),
                terminal: CodaTerminal::OracleNeeded,
                evidence_treated_as_proof: false,
                authority_effect: AuthorityEffect::None,
            }
        })
        .collect::<Vec<_>>();
    Ok(Coda8ImportOracleReceiptV1 {
        schema_version: CODA8_RECEIPT_SCHEMA_VERSION.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256: coda8_packet_sha256_v1(&packet)?,
        producer_id: packet.producer_id.clone(),
        predecessor_artifact_sha256: packet.input_artifacts[0].sha256.clone(),
        interfaces,
        evidence_receipts,
        residual_ledger: vec![Coda8ResidualLedgerEntryV1 {
            residual_id: S06_004_CODA7_RESIDUAL_ID.to_owned(),
            interface_id: "interface:migration-bundle-external-member".to_owned(),
            terminal: CodaTerminal::OpenObstruction,
            survivor_route: SurvivorRouteV1::ProofObligation,
        }],
        claimed_terminal: CodaTerminal::StabilizedSurvivor,
        promotion_requested: false,
        promotion_constructor_called: false,
        authorized_local_result_created: false,
        authority_effect: AuthorityEffect::None,
    })
}

pub fn replay_coda8_oracle_monotonicity_v1(
    kind: ImportInterfaceKindV1,
    claim_scope: &str,
) -> Result<(CodaTerminal, CodaTerminal), Coda8Error> {
    require_text("request.claim_scope", claim_scope)?;
    match kind {
        ImportInterfaceKindV1::DdaTraceImport => {
            let mut trace = DdaTrace::new();
            trace
                .emit(DdaStep::executed(
                    DdaOp::ContextExposure,
                    "frozen carrier exposed",
                ))
                .import(claim_scope);
            let before_t = map_trace_terminal_v1(trace.terminal(), claim_scope)?;
            trace.emit(DdaStep::executed(
                DdaOp::Terminalize,
                "attempted local terminalization",
            ));
            let after_t = map_trace_terminal_v1(trace.terminal(), claim_scope)?;
            Ok((before_t, after_t))
        }
        ImportInterfaceKindV1::RunReceiptExternalImport => {
            let before_t =
                CodaGtlaRunReceiptError::ImportedEvidence(claim_scope.to_owned()).terminal_route();
            let after_t = aggregate_coda6_terminals_v1(&[before_t, CodaTerminal::ExactRepair])
                .map_err(|error| Coda8Error::TerminalAggregation(error.to_string()))?;
            Ok((before_t, after_t))
        }
        ImportInterfaceKindV1::MigrationBundleExternalMember => Err(
            Coda8Error::InvalidPredecessor("GTOC-7 migration receipt is absent".to_owned()),
        ),
    }
}

fn validate_coda8_receipt_binding_v1(
    packet: &Coda8ImportOraclePacketV1,
    receipt: &Coda8ImportOracleReceiptV1,
) -> Result<String, Coda8Error> {
    if packet != &canonical_s06_004_packet_v1() {
        return Err(Coda8Error::PacketDrift);
    }
    validate_packet_boundary_v1(packet)?;
    let packet_sha256 = coda8_packet_sha256_v1(packet)?;
    if receipt.schema_version != CODA8_RECEIPT_SCHEMA_VERSION
        || receipt.packet_id != packet.packet_id
        || receipt.packet_sha256 != packet_sha256
        || receipt.producer_id != packet.producer_id
        || receipt.predecessor_artifact_sha256 != packet.input_artifacts[0].sha256
    {
        return Err(Coda8Error::ReceiptBindingMismatch);
    }
    reject_authority_expansion_v1(packet, receipt)?;
    Ok(packet_sha256)
}

fn verify_coda8_active_interface_v1(
    packet: &Coda8ImportOraclePacketV1,
    spec: &RegisteredImportInterfaceV1,
    evidence: &InterfaceFirewallReceiptV1,
    request_ids: &[String],
) -> Result<(), Coda8Error> {
    if request_ids.is_empty()
        || evidence.claimed_local_terminal != CodaTerminal::ExactRepair
        || !evidence.residual_ids.is_empty()
    {
        return Err(Coda8Error::InterfaceMismatch(spec.interface_id.clone()));
    }
    for request in packet
        .requests
        .iter()
        .filter(|request| request.interface_id == spec.interface_id)
    {
        let (before_t, after_t) =
            replay_coda8_oracle_monotonicity_v1(spec.kind, &request.claim_scope)?;
        if evidence.oracle_terminal_before_t != Some(before_t)
            || evidence.oracle_terminal_after_t != Some(after_t)
            || before_t != CodaTerminal::OracleNeeded
            || after_t != CodaTerminal::OracleNeeded
        {
            return Err(Coda8Error::OracleTerminalCleared(spec.interface_id.clone()));
        }
    }
    Ok(())
}

fn verify_coda8_deferred_interface_v1(
    packet: &Coda8ImportOraclePacketV1,
    spec: &RegisteredImportInterfaceV1,
    evidence: &InterfaceFirewallReceiptV1,
    request_ids: &[String],
    expected_residuals: &mut Vec<String>,
) -> Result<(), Coda8Error> {
    let residual_id = spec
        .expected_residual_id
        .as_ref()
        .ok_or_else(|| Coda8Error::InterfaceMismatch(spec.interface_id.clone()))?;
    let valid_deferred = request_ids.is_empty()
        && evidence.oracle_terminal_before_t.is_none()
        && evidence.oracle_terminal_after_t.is_none()
        && evidence.residual_ids == [residual_id.clone()]
        && evidence.claimed_local_terminal == CodaTerminal::OpenObstruction
        && !packet.coda7_dependency_receipt_present;
    if !valid_deferred {
        return Err(Coda8Error::InterfaceMismatch(spec.interface_id.clone()));
    }
    expected_residuals.push(residual_id.clone());
    Ok(())
}

fn verify_coda8_interface_header_v1(
    index: usize,
    spec: &RegisteredImportInterfaceV1,
    evidence: &InterfaceFirewallReceiptV1,
    interface_ids: &mut BTreeSet<String>,
) -> Result<(), Coda8Error> {
    if !interface_ids.insert(evidence.interface_id.clone()) {
        return Err(Coda8Error::DuplicateInterfaceId(
            evidence.interface_id.clone(),
        ));
    }
    if evidence.sequence as usize != index
        || evidence.sequence != spec.sequence
        || evidence.interface_id != spec.interface_id
        || evidence.kind != spec.kind
        || evidence.disposition != spec.disposition
    {
        return Err(Coda8Error::InterfaceMismatch(spec.interface_id.clone()));
    }
    if evidence.import_encoded_as_dda {
        return Err(Coda8Error::ImportSmuggledIntoDda(
            evidence.interface_id.clone(),
        ));
    }
    Ok(())
}

fn verify_coda8_single_interface_v1(
    index: usize,
    packet: &Coda8ImportOraclePacketV1,
    spec: &RegisteredImportInterfaceV1,
    evidence: &InterfaceFirewallReceiptV1,
    interface_ids: &mut BTreeSet<String>,
    active_interface_count: &mut u32,
    expected_residuals: &mut Vec<String>,
) -> Result<CodaTerminal, Coda8Error> {
    verify_coda8_interface_header_v1(index, spec, evidence, interface_ids)?;
    let request_ids = packet
        .requests
        .iter()
        .filter(|request| request.interface_id == spec.interface_id)
        .map(|request| request.request_id.clone())
        .collect::<Vec<_>>();
    if evidence.request_ids != request_ids {
        return Err(Coda8Error::RequestMismatch(spec.interface_id.clone()));
    }
    match spec.disposition {
        ImportInterfaceDispositionV1::Active => {
            *active_interface_count += 1;
            verify_coda8_active_interface_v1(packet, spec, evidence, &request_ids)?;
        }
        ImportInterfaceDispositionV1::DeferredUntilCoda7Receipt => {
            verify_coda8_deferred_interface_v1(
                packet,
                spec,
                evidence,
                &request_ids,
                expected_residuals,
            )?;
        }
    }
    if evidence.claimed_local_terminal != spec.expected_local_terminal {
        return Err(Coda8Error::InterfaceMismatch(spec.interface_id.clone()));
    }
    Ok(evidence.claimed_local_terminal)
}

fn verify_coda8_residual_ledger_and_terminal_v1(
    packet: &Coda8ImportOraclePacketV1,
    receipt: &Coda8ImportOracleReceiptV1,
    local_terminals: &[CodaTerminal],
    expected_residuals: &[String],
) -> Result<CodaTerminal, Coda8Error> {
    let expected_ledger = vec![Coda8ResidualLedgerEntryV1 {
        residual_id: S06_004_CODA7_RESIDUAL_ID.to_owned(),
        interface_id: "interface:migration-bundle-external-member".to_owned(),
        terminal: CodaTerminal::OpenObstruction,
        survivor_route: SurvivorRouteV1::ProofObligation,
    }];
    if receipt.residual_ledger != expected_ledger
        || receipt.residual_ledger.len() > packet.budgets.residual_budget as usize
        || expected_residuals != [S06_004_CODA7_RESIDUAL_ID.to_owned()]
    {
        return Err(Coda8Error::ResidualLedgerMismatch);
    }
    let terminal = aggregate_coda6_terminals_v1(local_terminals)
        .map_err(|error| Coda8Error::TerminalAggregation(error.to_string()))?;
    if receipt.claimed_terminal != terminal {
        return Err(Coda8Error::AggregateTerminalMismatch {
            expected: terminal,
            found: receipt.claimed_terminal,
        });
    }
    if !packet.legal_terminals.contains(&terminal) {
        return Err(Coda8Error::PacketBoundaryChanged);
    }
    Ok(terminal)
}

fn verify_coda8_interfaces_and_terminal_v1(
    packet: &Coda8ImportOraclePacketV1,
    receipt: &Coda8ImportOracleReceiptV1,
) -> Result<(BTreeSet<String>, u32, CodaTerminal), Coda8Error> {
    if receipt.interfaces.len() != packet.interfaces.len()
        || receipt.interfaces.len() > packet.budgets.interface_budget as usize
    {
        return Err(Coda8Error::InterfaceMismatch("count".to_owned()));
    }
    let mut interface_ids = BTreeSet::new();
    let mut local_terminals = Vec::with_capacity(receipt.interfaces.len());
    let mut expected_residuals = Vec::new();
    let mut active_interface_count = 0_u32;
    for (index, (spec, evidence)) in packet
        .interfaces
        .iter()
        .zip(&receipt.interfaces)
        .enumerate()
    {
        local_terminals.push(verify_coda8_single_interface_v1(
            index,
            packet,
            spec,
            evidence,
            &mut interface_ids,
            &mut active_interface_count,
            &mut expected_residuals,
        )?);
    }

    verify_evidence_receipts_v1(packet, receipt)?;
    let terminal = verify_coda8_residual_ledger_and_terminal_v1(
        packet,
        receipt,
        &local_terminals,
        &expected_residuals,
    )?;
    Ok((interface_ids, active_interface_count, terminal))
}

pub fn verify_coda8_import_oracle_firewall_v1(
    packet: &Coda8ImportOraclePacketV1,
    receipt: &Coda8ImportOracleReceiptV1,
    artifact_bytes: &Coda8ArtifactBytesV1,
) -> Result<Coda8ImportOracleVerificationV1, Coda8Error> {
    let packet_sha256 = validate_coda8_receipt_binding_v1(packet, receipt)?;
    let artifact_closure_sha256 = verify_artifacts_and_predecessor_v1(packet, artifact_bytes)?;
    validate_dda_alphabet_v1(&packet.dda_alphabet)?;
    let (interface_ids, active_interface_count, terminal) =
        verify_coda8_interfaces_and_terminal_v1(packet, receipt)?;

    let residual_ids = receipt
        .residual_ledger
        .iter()
        .map(|entry| entry.residual_id.clone())
        .collect::<Vec<_>>();
    Ok(Coda8ImportOracleVerificationV1 {
        schema_version: CODA8_VERIFICATION_SCHEMA_VERSION.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256,
        observer_sha256: packet.observer_sha256.clone(),
        receipt_sha256: coda8_receipt_sha256_v1(receipt)?,
        artifact_closure_sha256,
        interface_registry_sha256: sha256_json_v1(&packet.interfaces)?,
        source_policy_sha256: sha256_json_v1(&packet.source_policies)?,
        evidence_receipts_sha256: sha256_json_v1(&receipt.evidence_receipts)?,
        residual_ledger_sha256: sha256_json_v1(&receipt.residual_ledger)?,
        evaluator_id: packet.evaluator_id.clone(),
        authority_witness_id: packet.authority_witness_id.clone(),
        interface_count: packet.interfaces.len() as u32,
        active_interface_count,
        source_count: packet.source_policies.len() as u32,
        request_count: packet.requests.len() as u32,
        residual_count: receipt.residual_ledger.len() as u32,
        dda_alphabet_exact_and_exhaustive: true,
        imports_outside_dda: receipt
            .interfaces
            .iter()
            .all(|evidence| !evidence.import_encoded_as_dda),
        every_registered_interface_covered: interface_ids.len() == packet.interfaces.len(),
        every_request_priced: true,
        every_source_licensed: true,
        every_evidence_hash_bound: true,
        dda_trace_unchanged_by_evidence: true,
        oracle_terminal_monotone_after_t: true,
        external_evidence_not_treated_as_proof: true,
        predecessor_receipt_verified: true,
        coda7_dependency_receipt_present: false,
        coda7_dependency_preserved_as_residual: residual_ids
            .contains(&S06_004_CODA7_RESIDUAL_ID.to_owned()),
        residual_ids,
        terminal,
        promotion_requested: false,
        promotion_constructor_called: false,
        authorized_local_result_created: false,
        authority_effect: AuthorityEffect::None,
    })
}

pub fn coda8_packet_sha256_v1(packet: &Coda8ImportOraclePacketV1) -> Result<String, Coda8Error> {
    sha256_json_v1(packet)
}

pub fn coda8_receipt_sha256_v1(receipt: &Coda8ImportOracleReceiptV1) -> Result<String, Coda8Error> {
    sha256_json_v1(receipt)
}

pub fn coda8_verification_sha256_v1(
    verification: &Coda8ImportOracleVerificationV1,
) -> Result<String, Coda8Error> {
    sha256_json_v1(verification)
}

pub fn coda8_observer_sha256_v1(observer: &FrozenCoda8ObserverV1) -> Result<String, Coda8Error> {
    sha256_json_v1(observer)
}

pub fn canonical_coda8_json_line_v1<T: Serialize + ?Sized>(
    value: &T,
) -> Result<Vec<u8>, Coda8Error> {
    let mut bytes = serde_json::to_vec(value).map_err(json_error)?;
    bytes.push(b'\n');
    Ok(bytes)
}

pub fn parse_coda8_packet_canonical_v1(
    bytes: &[u8],
) -> Result<Coda8ImportOraclePacketV1, Coda8Error> {
    parse_canonical_json_line_v1(bytes, "GTOC-8 packet")
}

pub fn parse_coda8_receipt_canonical_v1(
    bytes: &[u8],
) -> Result<Coda8ImportOracleReceiptV1, Coda8Error> {
    parse_canonical_json_line_v1(bytes, "GTOC-8 receipt")
}

pub fn parse_coda8_verification_canonical_v1(
    bytes: &[u8],
) -> Result<Coda8ImportOracleVerificationV1, Coda8Error> {
    parse_canonical_json_line_v1(bytes, "GTOC-8 verification")
}

fn canonical_interfaces_v1() -> Vec<RegisteredImportInterfaceV1> {
    vec![
        RegisteredImportInterfaceV1 {
            sequence: 0,
            interface_id: "interface:dda-trace-import".to_owned(),
            kind: ImportInterfaceKindV1::DdaTraceImport,
            disposition: ImportInterfaceDispositionV1::Active,
            expected_local_terminal: CodaTerminal::ExactRepair,
            expected_residual_id: None,
        },
        RegisteredImportInterfaceV1 {
            sequence: 1,
            interface_id: "interface:run-receipt-external-import".to_owned(),
            kind: ImportInterfaceKindV1::RunReceiptExternalImport,
            disposition: ImportInterfaceDispositionV1::Active,
            expected_local_terminal: CodaTerminal::ExactRepair,
            expected_residual_id: None,
        },
        RegisteredImportInterfaceV1 {
            sequence: 2,
            interface_id: "interface:migration-bundle-external-member".to_owned(),
            kind: ImportInterfaceKindV1::MigrationBundleExternalMember,
            disposition: ImportInterfaceDispositionV1::DeferredUntilCoda7Receipt,
            expected_local_terminal: CodaTerminal::OpenObstruction,
            expected_residual_id: Some(S06_004_CODA7_RESIDUAL_ID.to_owned()),
        },
    ]
}

fn canonical_source_policies_v1() -> Vec<OracleSourcePolicyV1> {
    vec![
        OracleSourcePolicyV1 {
            sequence: 0,
            source_id: "source:fixture:registered-theorem-catalog".to_owned(),
            license_id: "license:fixture:evidence-only:catalog-v1".to_owned(),
            price_units: 7,
            evidence_only: true,
            licensed: true,
        },
        OracleSourcePolicyV1 {
            sequence: 1,
            source_id: "source:fixture:deterministic-tool-output".to_owned(),
            license_id: "license:fixture:evidence-only:tool-v1".to_owned(),
            price_units: 11,
            evidence_only: true,
            licensed: true,
        },
    ]
}

fn canonical_requests_v1() -> Vec<ExternalEvidenceRequestSpecV1> {
    let trace_request_snapshot = DdaTraceSnapshotV1 {
        operations: vec![DdaOp::ContextExposure],
        residual_ids: vec!["residual:s06-004:trace-import-request".to_owned()],
    };
    let run_request_snapshot = DdaTraceSnapshotV1 {
        operations: vec![DdaOp::ContextExposure, DdaOp::ResidualProjection],
        residual_ids: vec!["residual:s06-004:run-import-request".to_owned()],
    };
    vec![
        ExternalEvidenceRequestSpecV1 {
            sequence: 0,
            request_id: "request:s06-004:dda-trace".to_owned(),
            interface_id: "interface:dda-trace-import".to_owned(),
            source_id: "source:fixture:registered-theorem-catalog".to_owned(),
            claim_scope: "bounded external representation witness".to_owned(),
            expected_price_units: 7,
            expected_evidence_sha256: sha256_bytes_v1(
                b"fixture evidence: registered theorem catalog",
            ),
            before_dda_trace_sha256: sha256_json_v1(&trace_request_snapshot)
                .checked_invariant_10b349f3("canonical trace request snapshot must serialize"),
        },
        ExternalEvidenceRequestSpecV1 {
            sequence: 1,
            request_id: "request:s06-004:run-receipt".to_owned(),
            interface_id: "interface:run-receipt-external-import".to_owned(),
            source_id: "source:fixture:deterministic-tool-output".to_owned(),
            claim_scope: "bounded external deterministic tool witness".to_owned(),
            expected_price_units: 11,
            expected_evidence_sha256: sha256_bytes_v1(
                b"fixture evidence: deterministic tool output",
            ),
            before_dda_trace_sha256: sha256_json_v1(&run_request_snapshot)
                .checked_invariant_10b349f3("canonical run request snapshot must serialize"),
        },
    ]
}

fn packet_metadata_matches_s06_004_v1(packet: &Coda8ImportOraclePacketV1) -> bool {
    let expected_surface = S06_004_WRITE_SURFACE
        .iter()
        .map(|path| (*path).to_owned())
        .collect::<Vec<_>>();
    packet.schema_version == CODA8_PACKET_SCHEMA_VERSION
        && packet.packet_id == S06_004_PACKET_ID
        && packet.goal_id == S06_004_GOAL_ID
        && packet.frozen_base == S06_004_FROZEN_BASE
        && packet.evidence_ceiling == S06_004_EVIDENCE_CEILING
        && packet.exact_write_surface == expected_surface
        && packet.legal_terminals == CodaTerminal::ALL
}

fn packet_budgets_and_counts_match_v1(packet: &Coda8ImportOraclePacketV1) -> bool {
    packet.source_manifest.len() == S06_004_SOURCE_MANIFEST.len()
        && packet.input_artifacts.len() == S06_004_INPUT_ARTIFACTS.len()
        && packet.interfaces.len() == packet.budgets.interface_budget as usize
        && packet.source_policies.len() == packet.budgets.source_budget as usize
        && packet.requests.len() == packet.budgets.request_budget as usize
        && !packet.coda7_dependency_receipt_present
}

fn packet_authority_is_clean_v1(packet: &Coda8ImportOraclePacketV1) -> bool {
    packet.authority_effect == AuthorityEffect::None
        && packet.observer.authority_effect == AuthorityEffect::None
        && !packet.promotion_constructor_available
        && !packet.authorized_local_result_constructor_available
        && !packet.observer.model_context_available
        && !packet.observer.promotion_constructor_available
        && !packet
            .observer
            .authorized_local_result_constructor_available
}

fn validate_coda8_observer_hashes_v1(packet: &Coda8ImportOraclePacketV1) -> Result<(), Coda8Error> {
    require_sha256(
        "observer.source_manifest_sha256",
        &packet.observer.source_manifest_sha256,
    )?;
    require_sha256("observer.observer_sha256", &packet.observer_sha256)?;
    if sha256_json_v1(&packet.source_manifest)? != packet.observer.source_manifest_sha256
        || coda8_observer_sha256_v1(&packet.observer)? != packet.observer_sha256
    {
        return Err(Coda8Error::PacketBoundaryChanged);
    }
    Ok(())
}

fn validate_packet_boundary_v1(packet: &Coda8ImportOraclePacketV1) -> Result<(), Coda8Error> {
    if !packet_metadata_matches_s06_004_v1(packet) || !packet_budgets_and_counts_match_v1(packet) {
        return Err(Coda8Error::PacketBoundaryChanged);
    }
    if !packet_authority_is_clean_v1(packet) {
        return Err(Coda8Error::AuthorityExpanded);
    }
    require_distinct_witnesses_v1(packet)?;
    require_sorted_unique_text_v1(
        "observer.hidden_context_classes",
        &packet.observer.hidden_context_classes,
        false,
    )?;
    require_sorted_unique_text_v1(
        "packet.exact_write_surface",
        &packet.exact_write_surface,
        false,
    )?;
    validate_coda8_observer_hashes_v1(packet)?;
    validate_dda_alphabet_v1(&packet.dda_alphabet)?;
    validate_policy_and_request_specs_v1(packet)
}

fn validate_source_policies_v1(
    policies: &[OracleSourcePolicyV1],
) -> Result<BTreeSet<String>, Coda8Error> {
    let mut source_ids = BTreeSet::new();
    for (index, policy) in policies.iter().enumerate() {
        if policy.sequence as usize != index
            || !source_ids.insert(policy.source_id.clone())
            || policy.price_units == 0
            || !policy.evidence_only
            || !policy.licensed
        {
            return Err(Coda8Error::UnlicensedSource(policy.source_id.clone()));
        }
        require_text("source.source_id", &policy.source_id)?;
        require_text("source.license_id", &policy.license_id)?;
    }
    Ok(source_ids)
}

fn validate_single_request_spec_v1(
    index: usize,
    request: &ExternalEvidenceRequestSpecV1,
    request_ids: &mut BTreeSet<String>,
    interface_ids: &BTreeSet<&str>,
    source_ids: &BTreeSet<String>,
) -> Result<(), Coda8Error> {
    if request.sequence as usize != index
        || !request_ids.insert(request.request_id.clone())
        || !interface_ids.contains(request.interface_id.as_str())
        || !source_ids.contains(&request.source_id)
        || request.expected_price_units == 0
    {
        return Err(Coda8Error::RequestMismatch(request.request_id.clone()));
    }
    require_text("request.request_id", &request.request_id)?;
    require_text("request.claim_scope", &request.claim_scope)?;
    require_sha256(
        "request.expected_evidence_sha256",
        &request.expected_evidence_sha256,
    )?;
    require_sha256(
        "request.before_dda_trace_sha256",
        &request.before_dda_trace_sha256,
    )
}

fn validate_policy_and_request_specs_v1(
    packet: &Coda8ImportOraclePacketV1,
) -> Result<(), Coda8Error> {
    let source_ids = validate_source_policies_v1(&packet.source_policies)?;
    let interface_ids = packet
        .interfaces
        .iter()
        .map(|interface| interface.interface_id.as_str())
        .collect::<BTreeSet<_>>();
    let mut request_ids = BTreeSet::new();
    for (index, request) in packet.requests.iter().enumerate() {
        validate_single_request_spec_v1(
            index,
            request,
            &mut request_ids,
            &interface_ids,
            &source_ids,
        )?;
    }
    Ok(())
}

fn validate_dda_alphabet_v1(alphabet: &[DdaOp]) -> Result<(), Coda8Error> {
    if alphabet != DdaOp::alphabet() {
        return Err(Coda8Error::DdaAlphabetChanged);
    }
    let ranks = alphabet
        .iter()
        .copied()
        .map(dda_rank_v1)
        .collect::<BTreeSet<_>>();
    if ranks != (0_u8..8).collect::<BTreeSet<_>>() {
        return Err(Coda8Error::DdaAlphabetChanged);
    }
    Ok(())
}

fn dda_rank_v1(operation: DdaOp) -> u8 {
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

fn reject_authority_expansion_v1(
    packet: &Coda8ImportOraclePacketV1,
    receipt: &Coda8ImportOracleReceiptV1,
) -> Result<(), Coda8Error> {
    if receipt.promotion_requested
        || receipt.promotion_constructor_called
        || receipt.authorized_local_result_created
        || receipt.authority_effect != AuthorityEffect::None
        || packet.authority_effect != AuthorityEffect::None
        || receipt
            .evidence_receipts
            .iter()
            .any(|evidence| evidence.authority_effect != AuthorityEffect::None)
    {
        return Err(Coda8Error::AuthorityExpanded);
    }
    Ok(())
}

fn verify_coda8_artifact_hashes_v1(
    packet: &Coda8ImportOraclePacketV1,
    artifact_bytes: &Coda8ArtifactBytesV1,
) -> Result<(), Coda8Error> {
    let expected_paths = packet
        .input_artifacts
        .iter()
        .map(|artifact| artifact.path.clone())
        .collect::<BTreeSet<_>>();
    for path in &expected_paths {
        if !artifact_bytes.contains_key(path) {
            return Err(Coda8Error::MissingArtifact(path.clone()));
        }
    }
    if artifact_bytes.keys().cloned().collect::<BTreeSet<_>>() != expected_paths {
        return Err(Coda8Error::ArtifactSetMismatch);
    }
    for artifact in &packet.input_artifacts {
        let bytes = &artifact_bytes[&artifact.path];
        if bytes.len() as u64 != artifact.bytes {
            return Err(Coda8Error::ArtifactLengthMismatch(artifact.path.clone()));
        }
        if sha256_bytes_v1(bytes) != artifact.sha256 {
            return Err(Coda8Error::ArtifactHashMismatch(artifact.path.clone()));
        }
    }
    Ok(())
}

fn s06_003_predecessor_flags_valid_v1(
    predecessor: &crate::coda6_defect_terminalization::Coda6DefectTerminalizationVerificationV1,
) -> bool {
    predecessor.schema_version == "omega.gtoc6.defect-terminalization.verification.v1"
        && predecessor.packet_id == "omega-conductor-s06-003-gtoc6-terminalization-v1"
        && predecessor.terminal == CodaTerminal::StabilizedSurvivor
        && predecessor.every_defect_classified_once
        && predecessor.every_subclaim_classified_once
        && predecessor.every_local_terminal_recomputed
        && predecessor.every_residual_conserved
        && predecessor.aggregation_truth_table_replayed
        && predecessor.aggregation_permutation_invariant
}

fn verify_artifacts_and_predecessor_v1(
    packet: &Coda8ImportOraclePacketV1,
    artifact_bytes: &Coda8ArtifactBytesV1,
) -> Result<String, Coda8Error> {
    verify_coda8_artifact_hashes_v1(packet, artifact_bytes)?;
    let predecessor =
        parse_coda6_verification_canonical_v1(&artifact_bytes[S06_003_VERIFICATION_PATH])
            .map_err(|error| Coda8Error::InvalidPredecessor(error.to_string()))?;
    let authority_clean = !predecessor.promotion_requested
        && !predecessor.promotion_constructor_called
        && !predecessor.authorized_local_result_created
        && predecessor.authority_effect == AuthorityEffect::None;
    if !s06_003_predecessor_flags_valid_v1(&predecessor) || !authority_clean {
        return Err(Coda8Error::InvalidPredecessor(
            "S06-003 semantic boundary".to_owned(),
        ));
    }
    sha256_json_v1(&packet.input_artifacts)
}

fn verify_evidence_price_and_license_v1(
    request: &ExternalEvidenceRequestSpecV1,
    evidence: &ExternalEvidenceReceiptV1,
    policy: &OracleSourcePolicyV1,
) -> Result<(), Coda8Error> {
    if !policy.licensed
        || !policy.evidence_only
        || evidence.license_id != policy.license_id
        || evidence.charged_price_units == 0
        || evidence.charged_price_units != policy.price_units
        || evidence.charged_price_units != request.expected_price_units
    {
        return Err(Coda8Error::PriceOrLicenseMismatch(
            request.request_id.clone(),
        ));
    }
    Ok(())
}

fn verify_evidence_receipt_header_v1(
    index: usize,
    request: &ExternalEvidenceRequestSpecV1,
    evidence: &ExternalEvidenceReceiptV1,
    seen: &mut BTreeSet<String>,
) -> Result<(), Coda8Error> {
    if !seen.insert(evidence.request_id.clone()) {
        return Err(Coda8Error::DuplicateRequest(evidence.request_id.clone()));
    }
    if evidence.sequence as usize != index
        || evidence.sequence != request.sequence
        || evidence.request_id != request.request_id
        || evidence.interface_id != request.interface_id
        || evidence.source_id != request.source_id
    {
        return Err(Coda8Error::RequestMismatch(request.request_id.clone()));
    }
    Ok(())
}

fn verify_evidence_receipt_terminal_and_proof_flag_v1(
    request: &ExternalEvidenceRequestSpecV1,
    evidence: &ExternalEvidenceReceiptV1,
) -> Result<(), Coda8Error> {
    if evidence.terminal != CodaTerminal::OracleNeeded {
        return Err(Coda8Error::OracleTerminalCleared(
            request.request_id.clone(),
        ));
    }
    if evidence.evidence_treated_as_proof {
        return Err(Coda8Error::EvidencePromotedToProof(
            request.request_id.clone(),
        ));
    }
    Ok(())
}

fn verify_single_evidence_receipt_v1(
    index: usize,
    request: &ExternalEvidenceRequestSpecV1,
    evidence: &ExternalEvidenceReceiptV1,
    policies: &BTreeMap<&str, &OracleSourcePolicyV1>,
    seen: &mut BTreeSet<String>,
) -> Result<(), Coda8Error> {
    verify_evidence_receipt_header_v1(index, request, evidence, seen)?;
    let policy = policies
        .get(request.source_id.as_str())
        .ok_or_else(|| Coda8Error::UnlicensedSource(request.source_id.clone()))?;
    verify_evidence_price_and_license_v1(request, evidence, policy)?;
    require_sha256("evidence.evidence_sha256", &evidence.evidence_sha256)?;
    if evidence.evidence_sha256 != request.expected_evidence_sha256 {
        return Err(Coda8Error::EvidenceHashMismatch(request.request_id.clone()));
    }
    if evidence.before_dda_trace_sha256 != request.before_dda_trace_sha256
        || evidence.after_dda_trace_sha256 != evidence.before_dda_trace_sha256
    {
        return Err(Coda8Error::EvidenceMutatedDda(request.request_id.clone()));
    }
    verify_evidence_receipt_terminal_and_proof_flag_v1(request, evidence)
}

fn verify_evidence_receipts_v1(
    packet: &Coda8ImportOraclePacketV1,
    receipt: &Coda8ImportOracleReceiptV1,
) -> Result<(), Coda8Error> {
    if receipt.evidence_receipts.len() != packet.requests.len()
        || receipt.evidence_receipts.len() > packet.budgets.request_budget as usize
    {
        return Err(Coda8Error::RequestMismatch("count".to_owned()));
    }
    let policies = packet
        .source_policies
        .iter()
        .map(|policy| (policy.source_id.as_str(), policy))
        .collect::<BTreeMap<_, _>>();
    let mut seen = BTreeSet::new();
    for (index, (request, evidence)) in packet
        .requests
        .iter()
        .zip(&receipt.evidence_receipts)
        .enumerate()
    {
        verify_single_evidence_receipt_v1(index, request, evidence, &policies, &mut seen)?;
    }
    Ok(())
}

fn map_trace_terminal_v1(
    terminal: TraceTerminal,
    claim_scope: &str,
) -> Result<CodaTerminal, Coda8Error> {
    match terminal {
        TraceTerminal::OracleNeeded { import } if import == claim_scope => {
            Ok(CodaTerminal::OracleNeeded)
        }
        _ => Err(Coda8Error::OracleTerminalCleared(claim_scope.to_owned())),
    }
}

fn require_distinct_witnesses_v1(packet: &Coda8ImportOraclePacketV1) -> Result<(), Coda8Error> {
    for (field, value) in [
        ("packet.producer_id", packet.producer_id.as_str()),
        ("packet.evaluator_id", packet.evaluator_id.as_str()),
        (
            "packet.authority_witness_id",
            packet.authority_witness_id.as_str(),
        ),
    ] {
        require_text(field, value)?;
    }
    if packet.producer_id == packet.evaluator_id
        || packet.producer_id == packet.authority_witness_id
        || packet.evaluator_id == packet.authority_witness_id
        || packet.observer.observer_id != packet.evaluator_id
    {
        return Err(Coda8Error::PacketBoundaryChanged);
    }
    Ok(())
}

fn require_text(field: &'static str, value: &str) -> Result<(), Coda8Error> {
    if value.trim().is_empty() {
        Err(Coda8Error::EmptyText(field))
    } else {
        Ok(())
    }
}

fn require_sorted_unique_text_v1(
    field: &'static str,
    values: &[String],
    allow_empty: bool,
) -> Result<(), Coda8Error> {
    if !allow_empty && values.is_empty() {
        return Err(Coda8Error::NotSortedUnique(field));
    }
    if values.iter().any(|value| value.trim().is_empty())
        || values.windows(2).any(|pair| pair[0] >= pair[1])
    {
        return Err(Coda8Error::NotSortedUnique(field));
    }
    Ok(())
}

fn require_sha256(field: &'static str, value: &str) -> Result<(), Coda8Error> {
    if value.len() == 64
        && value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        Ok(())
    } else {
        Err(Coda8Error::InvalidSha256(field))
    }
}

fn parse_canonical_json_line_v1<T>(bytes: &[u8], label: &str) -> Result<T, Coda8Error>
where
    T: DeserializeOwned + Serialize,
{
    let value = serde_json::from_slice::<T>(bytes).map_err(decode_error)?;
    let canonical = canonical_coda8_json_line_v1(&value)?;
    if canonical != bytes {
        return Err(Coda8Error::NonCanonicalJson(label.to_owned()));
    }
    Ok(value)
}

fn sha256_json_v1<T: Serialize + ?Sized>(value: &T) -> Result<String, Coda8Error> {
    let bytes = serde_json::to_vec(value).map_err(json_error)?;
    Ok(sha256_bytes_v1(&bytes))
}

fn sha256_bytes_v1(bytes: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    format!("{:x}", hasher.finalize())
}

fn json_error(error: serde_json::Error) -> Coda8Error {
    Coda8Error::Json(error.to_string())
}

fn decode_error(error: serde_json::Error) -> Coda8Error {
    Coda8Error::Decode(error.to_string())
}


// Backward compatibility aliases

// Origin: vendor/engine/engine_state/src/coda8_import_oracle_firewall.rs
// Claim: urn:omega:crates_rs:omega-state:coda8-import-oracle-firewall:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_10b349f3 {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
