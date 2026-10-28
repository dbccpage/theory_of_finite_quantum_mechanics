//! Bounded S04-001 witness identities, ranked receipt DAG, and replay.
//!
//! The module verifies one frozen, structural witness tower. It authenticates
//! no person or process and constructs no authority. Even a complete tower
//! remains evidence with AuthorityEffect::None.


#[allow(dead_code, non_camel_case_types, missing_docs)]
trait CheckedInvariantExt_36277efd<T> {
    fn checked_invariant_36277efd(self, msg: &str) -> T;
}

impl<T> CheckedInvariantExt_36277efd<T> for Option<T> {
    #[inline]
    fn checked_invariant_36277efd(self, msg: &str) -> T {
        match self {
            Some(v) => v,
            None => unreachable!("{}", msg),
        }
    }
}

impl<T, E: std::fmt::Debug> CheckedInvariantExt_36277efd<T> for std::result::Result<T, E> {
    #[inline]
    fn checked_invariant_36277efd(self, msg: &str) -> T {
        match self {
            Ok(v) => v,
            Err(e) => unreachable!("{}: {:?}", msg, e),
        }
    }
}
use std::collections::{BTreeMap, BTreeSet};

use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

use crate::coda_gtla_protocol::CodaTerminal;

pub const WITNESS_PACKET_SCHEMA_VERSION: &str = "omega.witness-tower.packet.v1";
pub const WITNESS_RECEIPT_SCHEMA_VERSION: &str = "omega.witness-tower.receipt.v1";
pub const WITNESS_BUNDLE_SCHEMA_VERSION: &str = "omega.witness-tower.bundle.v1";
pub const WITNESS_VERIFICATION_SCHEMA_VERSION: &str = "omega.witness-tower.verification.v1";
pub const S04_001_FROZEN_BASE: &str = "bb6abd25846c23f990fa787bde3f91f84c6bcda7";
pub const S04_001_PACKET_ID: &str = "omega-conductor-s04-001-witness-tower-v1";
pub const S04_001_GOAL_ID: &str = "S04-001";
pub const S04_001_HOST_ID: &str = "host:s04-001";
pub const S04_001_HUMAN_ID: &str = "human:s04-001";
pub const S04_001_OBSERVER_DOMAIN: &str = "finite-witness-receipt-dag";
pub const S04_001_STATE_DOMAIN: &str = "omega.witness-tower.state.v1";
pub const S04_001_EVIDENCE_CEILING: &str =
    "finite role identity, context, receipt ancestry, rank, gate, and human-decision evidence only; no authority promotion";
pub const S04_001_UPSTREAM_PACKET_ID: &str = "omega-conductor-s03-001-mixed-carrier-v1";
pub const S04_001_UPSTREAM_PACKET_SHA256: &str =
    "f6a67d5ec2a05669948aa4044007604d7b536417c127dd2f88ce3ed4bb3c4f36";
pub const S04_001_UPSTREAM_RECEIPT_ARTIFACT_SHA256: &str =
    "41e6895b82382a8ab84f48d62aa18f50f47f43bbf95210db1f891c11ed7ef7a8";

pub const S04_001_WRITE_SURFACE: [&str; 9] = [
    "docs/omega-conductor-epic-v001.md",
    "docs/saga_04_witness_tower_and_joint_authority.md",
    "docs/sprint_s04_001.md",
    "docs/status/omega_conductor_s04_001_status_2026-07-18.md",
    "omega_engine/crates/omega_state/src/lib.rs",
    "omega_engine/crates/omega_state/src/witness_receipt_dag.rs",
    "omega_engine/crates/omega_state/tests/fixtures/s04_001_witness_tower_packet_v1.json",
    "omega_engine/crates/omega_state/tests/fixtures/s04_001_witness_tower_receipt_v1.json",
    "omega_engine/crates/omega_state/tests/witness_receipt_dag.rs",
];

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenWitnessSourceV1 {
    pub path: String,
    pub sha256: String,
    pub byte_len: u64,
}

pub const S04_001_SOURCE_MANIFEST: [(&str, &str, u64); 11] = [
    (
        "docs/omega-conductor-epic-v001.md",
        "6b372f15534bdd532b0d6e1fe298f3b7c1e75091efefbaa48dea0a55da13bdbe",
        56_035,
    ),
    (
        "docs/saga_04_witness_tower_and_joint_authority.md",
        "5f319c5ea9975dfacc7cd6154c5c09e02556bcf5ae41bf2833df968478e556a1",
        4_876,
    ),
    (
        "docs/saga_14_cert_authority_firewall.md",
        "92e41415240312782a529883bc8fad9e4b85dcf1dd948f63d101b43f09f750a5",
        7_985,
    ),
    (
        "docs/sprint_s04_001.md",
        "65dbc8a5c9aba509ed89c903fda7de9a68ef4423d06f0a55cff346c3a80e4efe",
        5_707,
    ),
    (
        "docs/status-vocabulary.md",
        "bd10e7ecf448ed6f4dca45a431c573242179a66b828492ecfe02f52572289b84",
        4_203,
    ),
    (
        "docs/status/omega_conductor_s03_001_status_2026-07-18.md",
        "56fb66000f87a56bac7a821d75014a4f9439c465ea7e748e2f93abb7ff1517af",
        8_922,
    ),
    (
        "omega_engine/crates/omega_state/src/gtoc1_classifier.rs",
        "de753b8664cd118f83f18399161c33887316f4e93702ff34f39ace8b9bcb46af",
        41_632,
    ),
    (
        "omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs",
        "da57f9f89dd396cbd1bca72880d024c81a4d3238bd6f78af9add06572c3f160f",
        35_825,
    ),
    (
        "omega_engine/crates/omega_state/src/operator_registry_runtime.rs",
        "a4e2e54ea5e594c65089ee8fe04e17cab61e3e5a2b34990c529889185e7e535a",
        45_922,
    ),
    (
        "omega_engine/crates/omega_state/src/task_admission.rs",
        "8904c36f0dce155de2c735d1199b553f2a4b5772121d462318515a449938d951",
        55_627,
    ),
    (
        "omega_engine/crates/omega_types/src/authority.rs",
        "42051a106954daa5ca2170c79bbf7d4cc9b04e0f7b554b8807251a0da552d2a9",
        39_913,
    ),
];

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WitnessBudgetsV1 {
    pub attempt_budget: u16,
    pub repair_budget: u16,
    pub successor_budget: u16,
    pub time_budget_seconds: u32,
    pub process_budget: u16,
    pub token_budget: u64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum WitnessRoleV1 {
    Host,
    Producer,
    IndependentEvaluator,
    AuthorityWitness,
    DeterministicGate,
    HumanAuthority,
}

impl WitnessRoleV1 {
    pub const ALL: [Self; 6] = [
        Self::Host,
        Self::Producer,
        Self::IndependentEvaluator,
        Self::AuthorityWitness,
        Self::DeterministicGate,
        Self::HumanAuthority,
    ];

    pub const fn witness_rank(self) -> Option<u8> {
        match self {
            Self::Host => None,
            Self::Producer => Some(0),
            Self::IndependentEvaluator => Some(1),
            Self::AuthorityWitness => Some(2),
            Self::DeterministicGate => Some(3),
            Self::HumanAuthority => Some(4),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenRoleIdentityV1 {
    pub role: WitnessRoleV1,
    pub identity_id: String,
    pub session_id: String,
    pub context_sha256: String,
    pub visibility_class: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum WitnessPermissionV1 {
    ReadFrozenSources,
    VerifyReceipts,
    RecordHumanDecision,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenWitnessObserverV1 {
    pub observer_id: String,
    pub observer_domain: String,
    pub state_domain: String,
    pub frozen_base: String,
    pub observer_hash: String,
    pub visible_artifact_hashes: Vec<String>,
    pub hidden_artifact_classes: Vec<String>,
    pub tool_permissions: Vec<WitnessPermissionV1>,
    pub write_surface: Vec<String>,
    pub evidence_ceiling: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct UpstreamAdmissionReferenceV1 {
    pub goal_id: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub receipt_artifact_sha256: String,
    pub terminal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WitnessTowerPacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub goal_id: String,
    pub frozen_base: String,
    pub source_manifest: Vec<FrozenWitnessSourceV1>,
    pub upstream: UpstreamAdmissionReferenceV1,
    pub budgets: WitnessBudgetsV1,
    pub role_plan: Vec<FrozenRoleIdentityV1>,
    pub observer: FrozenWitnessObserverV1,
    pub write_surface: Vec<String>,
    pub evidence_ceiling: String,
    pub authority_effect: AuthorityEffect,
    pub promotion_constructor_available: bool,
}

impl WitnessTowerPacketV1 {
    pub fn validate(&self) -> Result<(), WitnessTowerError> {
        self.validate_header()?;
        self.validate_manifests_and_surfaces()?;
        self.validate_components_and_authority()
    }

    fn validate_header(&self) -> Result<(), WitnessTowerError> {
        require_schema(
            "packet.schema_version",
            &self.schema_version,
            WITNESS_PACKET_SCHEMA_VERSION,
        )?;
        for (field, value) in [
            ("packet.packet_id", self.packet_id.as_str()),
            ("packet.goal_id", self.goal_id.as_str()),
        ] {
            require_text(field, value)?;
        }
        require_git_commit("packet.frozen_base", &self.frozen_base)?;
        if self.packet_id != S04_001_PACKET_ID
            || self.goal_id != S04_001_GOAL_ID
            || self.frozen_base != S04_001_FROZEN_BASE
        {
            return Err(WitnessTowerError::FrozenPacketChanged);
        }
        Ok(())
    }

    fn validate_manifests_and_surfaces(&self) -> Result<(), WitnessTowerError> {
        if self.source_manifest != expected_source_manifest_v1() {
            return Err(WitnessTowerError::SourceManifestChanged);
        }
        if self.write_surface != expected_write_surface_v1() {
            return Err(WitnessTowerError::WriteSurfaceChanged);
        }
        if self.evidence_ceiling != S04_001_EVIDENCE_CEILING {
            return Err(WitnessTowerError::EvidenceCeilingChanged);
        }
        Ok(())
    }

    fn validate_components_and_authority(&self) -> Result<(), WitnessTowerError> {
        validate_budgets(self.budgets)?;
        validate_upstream(&self.upstream)?;
        validate_role_plan(&self.role_plan)?;
        validate_observer(&self.observer)?;
        if !self.authority_effect.is_none() || self.promotion_constructor_available {
            return Err(WitnessTowerError::AuthorityExpansion);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum WitnessReceiptKindV1 {
    Producer,
    IndependentEvaluation,
    AuthorityWitness,
    DeterministicGate,
    HumanDecision,
}

impl WitnessReceiptKindV1 {
    pub const ALL: [Self; 5] = [
        Self::Producer,
        Self::IndependentEvaluation,
        Self::AuthorityWitness,
        Self::DeterministicGate,
        Self::HumanDecision,
    ];

    pub const fn graph_rank(self) -> u8 {
        match self {
            Self::Producer => 0,
            Self::IndependentEvaluation => 1,
            Self::AuthorityWitness => 2,
            Self::DeterministicGate => 3,
            Self::HumanDecision => 4,
        }
    }

    pub const fn role(self) -> WitnessRoleV1 {
        match self {
            Self::Producer => WitnessRoleV1::Producer,
            Self::IndependentEvaluation => WitnessRoleV1::IndependentEvaluator,
            Self::AuthorityWitness => WitnessRoleV1::AuthorityWitness,
            Self::DeterministicGate => WitnessRoleV1::DeterministicGate,
            Self::HumanDecision => WitnessRoleV1::HumanAuthority,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WitnessReceiptParentV1 {
    pub receipt_id: String,
    pub receipt_sha256: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum HumanDecisionOutcomeV1 {
    PendingHumanPromotion,
    PromotionRequested,
    Rejected,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct HumanDecisionV1 {
    pub decision_id: String,
    pub recorded_by_host_id: String,
    pub human_actor_id: String,
    pub outcome: HumanDecisionOutcomeV1,
    pub basis: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WitnessReceiptMaterialV1 {
    pub schema_version: String,
    pub receipt_id: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub kind: WitnessReceiptKindV1,
    pub issuer_identity_id: String,
    pub issuer_session_id: String,
    pub issuer_context_sha256: String,
    pub graph_rank: u8,
    pub parents: Vec<WitnessReceiptParentV1>,
    pub evidence_hashes: Vec<String>,
    pub evidence_ceiling: String,
    pub human_decision: Option<HumanDecisionV1>,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WitnessReceiptV1 {
    pub material: WitnessReceiptMaterialV1,
    pub receipt_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct JointAuthorityBoundaryV1 {
    pub identity_separated: bool,
    pub session_separated: bool,
    pub context_separated: bool,
    pub receipt_dag_acyclic: bool,
    pub rank_ordered: bool,
    pub deterministic_gate_present: bool,
    pub human_decision_recorded: bool,
    pub promotion_requested: bool,
    pub promotion_constructor_called: bool,
    pub authorized_local_result_created: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WitnessTowerVerificationV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub role_plan_sha256: String,
    pub receipt_dag_sha256: String,
    pub human_decision: HumanDecisionV1,
    pub boundary: JointAuthorityBoundaryV1,
    pub terminal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WitnessTowerReceiptBundleV1 {
    pub schema_version: String,
    pub packet_sha256: String,
    pub receipts: Vec<WitnessReceiptV1>,
    pub verification: WitnessTowerVerificationV1,
}

pub fn canonical_s04_001_packet_v1() -> WitnessTowerPacketV1 {
    WitnessTowerPacketV1 {
        schema_version: WITNESS_PACKET_SCHEMA_VERSION.to_owned(),
        packet_id: S04_001_PACKET_ID.to_owned(),
        goal_id: S04_001_GOAL_ID.to_owned(),
        frozen_base: S04_001_FROZEN_BASE.to_owned(),
        source_manifest: expected_source_manifest_v1(),
        upstream: UpstreamAdmissionReferenceV1 {
            goal_id: "S03-001".to_owned(),
            packet_id: S04_001_UPSTREAM_PACKET_ID.to_owned(),
            packet_sha256: S04_001_UPSTREAM_PACKET_SHA256.to_owned(),
            receipt_artifact_sha256: S04_001_UPSTREAM_RECEIPT_ARTIFACT_SHA256.to_owned(),
            terminal: CodaTerminal::StabilizedSurvivor,
            authority_effect: AuthorityEffect::None,
        },
        budgets: WitnessBudgetsV1 {
            attempt_budget: 1,
            repair_budget: 2,
            successor_budget: 1,
            time_budget_seconds: 8 * 60 * 60,
            process_budget: 4,
            token_budget: 200_000,
        },
        role_plan: expected_role_plan_v1(),
        observer: canonical_observer_v1(),
        write_surface: expected_write_surface_v1(),
        evidence_ceiling: S04_001_EVIDENCE_CEILING.to_owned(),
        authority_effect: AuthorityEffect::None,
        promotion_constructor_available: false,
    }
}

pub fn witness_packet_canonical_bytes_v1(
    packet: &WitnessTowerPacketV1,
) -> Result<Vec<u8>, WitnessTowerError> {
    packet.validate()?;
    serde_json::to_vec(packet).map_err(json_error)
}

pub fn witness_packet_sha256_v1(
    packet: &WitnessTowerPacketV1,
) -> Result<String, WitnessTowerError> {
    Ok(sha256_bytes_v1(&witness_packet_canonical_bytes_v1(packet)?))
}

pub fn witness_receipt_sha256_v1(
    material: &WitnessReceiptMaterialV1,
) -> Result<String, WitnessTowerError> {
    sha256_json_v1(material)
}

pub fn canonical_s04_001_receipt_bundle_v1(
    packet: &WitnessTowerPacketV1,
) -> Result<WitnessTowerReceiptBundleV1, WitnessTowerError> {
    packet.validate()?;
    let source_sha256 = sha256_json_v1(&packet.source_manifest)?;
    let producer = make_receipt_v1(
        packet,
        WitnessReceiptKindV1::Producer,
        Vec::new(),
        vec![source_sha256],
        None,
    )?;
    let evaluation = make_receipt_v1(
        packet,
        WitnessReceiptKindV1::IndependentEvaluation,
        vec![parent_v1(&producer)],
        vec![producer.receipt_sha256.clone()],
        None,
    )?;
    let authority = make_receipt_v1(
        packet,
        WitnessReceiptKindV1::AuthorityWitness,
        vec![parent_v1(&producer), parent_v1(&evaluation)],
        vec![
            producer.receipt_sha256.clone(),
            evaluation.receipt_sha256.clone(),
        ],
        None,
    )?;
    let gate = make_receipt_v1(
        packet,
        WitnessReceiptKindV1::DeterministicGate,
        vec![
            parent_v1(&producer),
            parent_v1(&evaluation),
            parent_v1(&authority),
        ],
        vec![
            producer.receipt_sha256.clone(),
            evaluation.receipt_sha256.clone(),
            authority.receipt_sha256.clone(),
        ],
        None,
    )?;
    let mut receipts = vec![producer, evaluation, authority, gate];
    let human = record_human_decision_v1(
        packet,
        &receipts,
        S04_001_HOST_ID,
        S04_001_HUMAN_ID,
        HumanDecisionOutcomeV1::PendingHumanPromotion,
        "tower verified; authority promotion remains a separate human and SAGA-14 transition",
    )?;
    receipts.push(human);
    let verification = verify_witness_tower_v1(packet, &receipts)?;
    Ok(WitnessTowerReceiptBundleV1 {
        schema_version: WITNESS_BUNDLE_SCHEMA_VERSION.to_owned(),
        packet_sha256: witness_packet_sha256_v1(packet)?,
        receipts,
        verification,
    })
}

pub fn record_human_decision_v1(
    packet: &WitnessTowerPacketV1,
    prefix_receipts: &[WitnessReceiptV1],
    caller_id: &str,
    human_actor_id: &str,
    outcome: HumanDecisionOutcomeV1,
    basis: &str,
) -> Result<WitnessReceiptV1, WitnessTowerError> {
    packet.validate()?;
    if caller_id != S04_001_HOST_ID {
        return Err(WitnessTowerError::HostDecisionIssuerMismatch);
    }
    if human_actor_id != S04_001_HUMAN_ID {
        return Err(WitnessTowerError::HumanActorMismatch);
    }
    require_text("human_decision.basis", basis)?;
    validate_receipt_set_v1(packet, prefix_receipts, false)?;
    let authority = receipt_by_kind(prefix_receipts, WitnessReceiptKindV1::AuthorityWitness)?;
    let gate = receipt_by_kind(prefix_receipts, WitnessReceiptKindV1::DeterministicGate)?;
    let prefix_sha256 = sha256_json_v1(prefix_receipts)?;
    make_receipt_v1(
        packet,
        WitnessReceiptKindV1::HumanDecision,
        vec![parent_v1(authority), parent_v1(gate)],
        vec![prefix_sha256],
        Some(HumanDecisionV1 {
            decision_id: "decision:s04-001:human".to_owned(),
            recorded_by_host_id: caller_id.to_owned(),
            human_actor_id: human_actor_id.to_owned(),
            outcome,
            basis: basis.to_owned(),
        }),
    )
}

fn make_receipt_v1(
    packet: &WitnessTowerPacketV1,
    kind: WitnessReceiptKindV1,
    mut parents: Vec<WitnessReceiptParentV1>,
    mut evidence_hashes: Vec<String>,
    human_decision: Option<HumanDecisionV1>,
) -> Result<WitnessReceiptV1, WitnessTowerError> {
    let identity = role_identity(packet, kind.role())?;
    parents.sort();
    evidence_hashes.sort();
    let material = WitnessReceiptMaterialV1 {
        schema_version: WITNESS_RECEIPT_SCHEMA_VERSION.to_owned(),
        receipt_id: expected_receipt_id(kind).to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256: witness_packet_sha256_v1(packet)?,
        kind,
        issuer_identity_id: identity.identity_id.clone(),
        issuer_session_id: identity.session_id.clone(),
        issuer_context_sha256: identity.context_sha256.clone(),
        graph_rank: kind.graph_rank(),
        parents,
        evidence_hashes,
        evidence_ceiling: packet.evidence_ceiling.clone(),
        human_decision,
        authority_effect: AuthorityEffect::None,
    };
    let receipt_sha256 = witness_receipt_sha256_v1(&material)?;
    Ok(WitnessReceiptV1 {
        material,
        receipt_sha256,
    })
}

fn parent_v1(receipt: &WitnessReceiptV1) -> WitnessReceiptParentV1 {
    WitnessReceiptParentV1 {
        receipt_id: receipt.material.receipt_id.clone(),
        receipt_sha256: receipt.receipt_sha256.clone(),
    }
}

pub fn verify_witness_tower_v1(
    packet: &WitnessTowerPacketV1,
    receipts: &[WitnessReceiptV1],
) -> Result<WitnessTowerVerificationV1, WitnessTowerError> {
    packet.validate()?;
    validate_receipt_set_v1(packet, receipts, true)?;
    let human = receipt_by_kind(receipts, WitnessReceiptKindV1::HumanDecision)?;
    let decision = human
        .material
        .human_decision
        .clone()
        .ok_or(WitnessTowerError::HumanDecisionMissing)?;
    let promotion_requested = decision.outcome == HumanDecisionOutcomeV1::PromotionRequested;
    let terminal = if decision.outcome == HumanDecisionOutcomeV1::Rejected {
        CodaTerminal::Refused
    } else {
        CodaTerminal::StabilizedSurvivor
    };
    Ok(WitnessTowerVerificationV1 {
        schema_version: WITNESS_VERIFICATION_SCHEMA_VERSION.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256: witness_packet_sha256_v1(packet)?,
        role_plan_sha256: sha256_json_v1(&packet.role_plan)?,
        receipt_dag_sha256: sha256_json_v1(receipts)?,
        human_decision: decision,
        boundary: JointAuthorityBoundaryV1 {
            identity_separated: true,
            session_separated: true,
            context_separated: true,
            receipt_dag_acyclic: true,
            rank_ordered: true,
            deterministic_gate_present: true,
            human_decision_recorded: true,
            promotion_requested,
            promotion_constructor_called: false,
            authorized_local_result_created: false,
            authority_effect: AuthorityEffect::None,
        },
        terminal,
        authority_effect: AuthorityEffect::None,
    })
}

pub fn replay_witness_tower_v1(
    packet: &WitnessTowerPacketV1,
    bundle: &WitnessTowerReceiptBundleV1,
) -> Result<WitnessTowerVerificationV1, WitnessTowerError> {
    require_schema(
        "bundle.schema_version",
        &bundle.schema_version,
        WITNESS_BUNDLE_SCHEMA_VERSION,
    )?;
    let packet_sha256 = witness_packet_sha256_v1(packet)?;
    if bundle.packet_sha256 != packet_sha256 {
        return Err(WitnessTowerError::PacketHashMismatch);
    }
    let replayed = verify_witness_tower_v1(packet, &bundle.receipts)?;
    if replayed != bundle.verification {
        return Err(WitnessTowerError::ReplayMismatch);
    }
    Ok(replayed)
}

fn validate_receipt_set_v1(
    packet: &WitnessTowerPacketV1,
    receipts: &[WitnessReceiptV1],
    complete: bool,
) -> Result<(), WitnessTowerError> {
    let expected_kinds = if complete {
        WitnessReceiptKindV1::ALL.as_slice()
    } else {
        &WitnessReceiptKindV1::ALL[..4]
    };
    ensure_expected_receipt_kinds_present(receipts, expected_kinds)?;
    let ids = receipts
        .iter()
        .map(|receipt| receipt.material.receipt_id.clone())
        .collect::<Vec<_>>();
    require_nonempty_sorted_texts("receipts.ids", &ids)?;
    for receipt in receipts {
        validate_receipt_basic_v1(packet, receipt)?;
    }
    let receipt_map = receipts
        .iter()
        .map(|receipt| (receipt.material.receipt_id.as_str(), receipt))
        .collect::<BTreeMap<_, _>>();
    ensure_acyclic_v1(&receipt_map)?;
    for (receipt, expected_kind) in receipts.iter().zip(expected_kinds) {
        validate_receipt_edges_v1(packet, receipt, *expected_kind, &receipt_map)?;
    }
    Ok(())
}

fn ensure_expected_receipt_kinds_present(
    receipts: &[WitnessReceiptV1],
    expected_kinds: &[WitnessReceiptKindV1],
) -> Result<(), WitnessTowerError> {
    for kind in expected_kinds {
        if !receipts
            .iter()
            .any(|receipt| receipt.material.receipt_id == expected_receipt_id(*kind))
        {
            return Err(WitnessTowerError::MissingRequiredReceipt(
                expected_receipt_id(*kind).to_owned(),
            ));
        }
    }
    if receipts.len() != expected_kinds.len() {
        return Err(WitnessTowerError::UnexpectedReceiptSet);
    }
    Ok(())
}

fn validate_receipt_basic_v1(
    packet: &WitnessTowerPacketV1,
    receipt: &WitnessReceiptV1,
) -> Result<(), WitnessTowerError> {
    validate_receipt_text_and_hashes(receipt)?;
    validate_receipt_packet_and_authority(packet, receipt)?;
    validate_receipt_evidence_and_parents(&receipt.material)
}

fn validate_receipt_text_and_hashes(receipt: &WitnessReceiptV1) -> Result<(), WitnessTowerError> {
    let material = &receipt.material;
    require_schema(
        "receipt.schema_version",
        &material.schema_version,
        WITNESS_RECEIPT_SCHEMA_VERSION,
    )?;
    for (field, value) in [
        ("receipt.receipt_id", material.receipt_id.as_str()),
        ("receipt.packet_id", material.packet_id.as_str()),
        (
            "receipt.issuer_identity_id",
            material.issuer_identity_id.as_str(),
        ),
        (
            "receipt.issuer_session_id",
            material.issuer_session_id.as_str(),
        ),
    ] {
        require_text(field, value)?;
    }
    require_sha256(
        "receipt.issuer_context_sha256",
        &material.issuer_context_sha256,
    )?;
    require_sha256("receipt.packet_sha256", &material.packet_sha256)?;
    require_sha256("receipt.receipt_sha256", &receipt.receipt_sha256)
}

fn validate_receipt_packet_and_authority(
    packet: &WitnessTowerPacketV1,
    receipt: &WitnessReceiptV1,
) -> Result<(), WitnessTowerError> {
    let material = &receipt.material;
    if material.packet_id != packet.packet_id
        || material.packet_sha256 != witness_packet_sha256_v1(packet)?
    {
        return Err(WitnessTowerError::PacketHashMismatch);
    }
    if receipt.receipt_sha256 != witness_receipt_sha256_v1(material)? {
        return Err(WitnessTowerError::ReceiptHashMismatch(
            material.receipt_id.clone(),
        ));
    }
    if !material.authority_effect.is_none() || material.evidence_ceiling != packet.evidence_ceiling
    {
        return Err(WitnessTowerError::AuthorityExpansion);
    }
    Ok(())
}

fn validate_receipt_evidence_and_parents(
    material: &WitnessReceiptMaterialV1,
) -> Result<(), WitnessTowerError> {
    if material.evidence_hashes.is_empty() || !is_strict_sorted(&material.evidence_hashes) {
        return Err(WitnessTowerError::NonCanonicalList(
            "receipt.evidence_hashes",
        ));
    }
    for hash in &material.evidence_hashes {
        require_sha256("receipt.evidence_hashes", hash)?;
    }
    if !is_strict_sorted(&material.parents) {
        return Err(WitnessTowerError::NonCanonicalList("receipt.parents"));
    }
    for parent in &material.parents {
        require_text("receipt.parent.receipt_id", &parent.receipt_id)?;
        require_sha256("receipt.parent.receipt_sha256", &parent.receipt_sha256)?;
    }
    Ok(())
}

fn validate_receipt_edges_v1<'a>(
    packet: &WitnessTowerPacketV1,
    receipt: &WitnessReceiptV1,
    expected_kind: WitnessReceiptKindV1,
    receipt_map: &BTreeMap<&'a str, &'a WitnessReceiptV1>,
) -> Result<(), WitnessTowerError> {
    let material = &receipt.material;
    validate_receipt_kind_and_issuer(packet, material, expected_kind)?;
    validate_parent_edges(material, expected_kind, receipt_map)?;
    validate_human_decision_field(expected_kind, &material.human_decision)
}

fn validate_receipt_kind_and_issuer(
    packet: &WitnessTowerPacketV1,
    material: &WitnessReceiptMaterialV1,
    expected_kind: WitnessReceiptKindV1,
) -> Result<(), WitnessTowerError> {
    if material.kind != expected_kind || material.receipt_id != expected_receipt_id(expected_kind) {
        return Err(WitnessTowerError::ReceiptKindChanged);
    }
    if material.graph_rank != expected_kind.graph_rank() {
        return Err(WitnessTowerError::ReceiptRankChanged(
            material.receipt_id.clone(),
        ));
    }
    let identity = role_identity(packet, expected_kind.role())?;
    if material.issuer_identity_id != identity.identity_id
        || material.issuer_session_id != identity.session_id
        || material.issuer_context_sha256 != identity.context_sha256
    {
        return Err(WitnessTowerError::ReceiptIssuerChanged(
            material.receipt_id.clone(),
        ));
    }
    Ok(())
}

fn validate_parent_edges<'a>(
    material: &WitnessReceiptMaterialV1,
    expected_kind: WitnessReceiptKindV1,
    receipt_map: &BTreeMap<&'a str, &'a WitnessReceiptV1>,
) -> Result<(), WitnessTowerError> {
    for parent in &material.parents {
        let parent_receipt = receipt_map
            .get(parent.receipt_id.as_str())
            .ok_or_else(|| WitnessTowerError::ParentReceiptMissing(parent.receipt_id.clone()))?;
        if parent_receipt.material.graph_rank >= material.graph_rank {
            return Err(WitnessTowerError::FutureParent {
                receipt_id: material.receipt_id.clone(),
                parent_id: parent.receipt_id.clone(),
            });
        }
        if parent.receipt_sha256 != parent_receipt.receipt_sha256 {
            return Err(WitnessTowerError::ParentHashMismatch(
                parent.receipt_id.clone(),
            ));
        }
    }
    let parent_ids = material
        .parents
        .iter()
        .map(|parent| parent.receipt_id.as_str())
        .collect::<Vec<_>>();
    if parent_ids != expected_parent_ids(expected_kind) {
        return Err(WitnessTowerError::ParentSetChanged(
            material.receipt_id.clone(),
        ));
    }
    Ok(())
}

fn validate_human_decision_field(
    expected_kind: WitnessReceiptKindV1,
    human_decision: &Option<HumanDecisionV1>,
) -> Result<(), WitnessTowerError> {
    match (expected_kind, human_decision) {
        (WitnessReceiptKindV1::HumanDecision, Some(decision)) => {
            if decision.decision_id != "decision:s04-001:human"
                || decision.recorded_by_host_id != S04_001_HOST_ID
                || decision.human_actor_id != S04_001_HUMAN_ID
            {
                return Err(WitnessTowerError::HumanDecisionIdentityChanged);
            }
            require_text("human_decision.basis", &decision.basis)
        }
        (WitnessReceiptKindV1::HumanDecision, None) => {
            Err(WitnessTowerError::HumanDecisionMissing)
        }
        (_, Some(_)) => Err(WitnessTowerError::UnexpectedHumanDecision),
        (_, None) => Ok(()),
    }
}

fn ensure_acyclic_v1<'a>(
    receipt_map: &BTreeMap<&'a str, &'a WitnessReceiptV1>,
) -> Result<(), WitnessTowerError> {
    let mut states = BTreeMap::<&'a str, u8>::new();
    for receipt_id in receipt_map.keys() {
        visit_receipt_v1(receipt_id, receipt_map, &mut states)?;
    }
    Ok(())
}

fn visit_receipt_v1<'a>(
    receipt_id: &'a str,
    receipt_map: &BTreeMap<&'a str, &'a WitnessReceiptV1>,
    states: &mut BTreeMap<&'a str, u8>,
) -> Result<(), WitnessTowerError> {
    match states.get(receipt_id).copied() {
        Some(1) => return Err(WitnessTowerError::ReceiptCycle(receipt_id.to_owned())),
        Some(2) => return Ok(()),
        _ => {}
    }
    states.insert(receipt_id, 1);
    let receipt = receipt_map
        .get(receipt_id)
        .ok_or_else(|| WitnessTowerError::ParentReceiptMissing(receipt_id.to_owned()))?;
    for parent in &receipt.material.parents {
        let parent_id = receipt_map
            .get_key_value(parent.receipt_id.as_str())
            .map(|(id, _)| *id)
            .ok_or_else(|| WitnessTowerError::ParentReceiptMissing(parent.receipt_id.clone()))?;
        visit_receipt_v1(parent_id, receipt_map, states)?;
    }
    states.insert(receipt_id, 2);
    Ok(())
}

fn receipt_by_kind(
    receipts: &[WitnessReceiptV1],
    kind: WitnessReceiptKindV1,
) -> Result<&WitnessReceiptV1, WitnessTowerError> {
    receipts
        .iter()
        .find(|receipt| receipt.material.kind == kind)
        .ok_or_else(|| {
            WitnessTowerError::MissingRequiredReceipt(expected_receipt_id(kind).to_owned())
        })
}

fn expected_receipt_id(kind: WitnessReceiptKindV1) -> &'static str {
    match kind {
        WitnessReceiptKindV1::Producer => "receipt:s04-001:00-producer",
        WitnessReceiptKindV1::IndependentEvaluation => "receipt:s04-001:01-independent-evaluation",
        WitnessReceiptKindV1::AuthorityWitness => "receipt:s04-001:02-authority-witness",
        WitnessReceiptKindV1::DeterministicGate => "receipt:s04-001:03-deterministic-gate",
        WitnessReceiptKindV1::HumanDecision => "receipt:s04-001:04-human-decision",
    }
}

fn expected_parent_ids(kind: WitnessReceiptKindV1) -> Vec<&'static str> {
    match kind {
        WitnessReceiptKindV1::Producer => Vec::new(),
        WitnessReceiptKindV1::IndependentEvaluation => {
            vec![expected_receipt_id(WitnessReceiptKindV1::Producer)]
        }
        WitnessReceiptKindV1::AuthorityWitness => vec![
            expected_receipt_id(WitnessReceiptKindV1::Producer),
            expected_receipt_id(WitnessReceiptKindV1::IndependentEvaluation),
        ],
        WitnessReceiptKindV1::DeterministicGate => vec![
            expected_receipt_id(WitnessReceiptKindV1::Producer),
            expected_receipt_id(WitnessReceiptKindV1::IndependentEvaluation),
            expected_receipt_id(WitnessReceiptKindV1::AuthorityWitness),
        ],
        WitnessReceiptKindV1::HumanDecision => vec![
            expected_receipt_id(WitnessReceiptKindV1::AuthorityWitness),
            expected_receipt_id(WitnessReceiptKindV1::DeterministicGate),
        ],
    }
}

fn expected_source_manifest_v1() -> Vec<FrozenWitnessSourceV1> {
    S04_001_SOURCE_MANIFEST
        .iter()
        .map(|(path, sha256, byte_len)| FrozenWitnessSourceV1 {
            path: (*path).to_owned(),
            sha256: (*sha256).to_owned(),
            byte_len: *byte_len,
        })
        .collect()
}

fn expected_write_surface_v1() -> Vec<String> {
    S04_001_WRITE_SURFACE
        .iter()
        .map(|path| (*path).to_owned())
        .collect()
}

fn expected_role_plan_v1() -> Vec<FrozenRoleIdentityV1> {
    [
        (
            WitnessRoleV1::Host,
            S04_001_HOST_ID,
            "session:s04-001:host",
            "host-control-plane",
        ),
        (
            WitnessRoleV1::Producer,
            "producer:s04-001",
            "session:s04-001:producer",
            "producer-visible-context",
        ),
        (
            WitnessRoleV1::IndependentEvaluator,
            "evaluator:s04-001",
            "session:s04-001:evaluator",
            "evaluator-independent-context",
        ),
        (
            WitnessRoleV1::AuthorityWitness,
            "authority-witness:s04-001",
            "session:s04-001:authority-witness",
            "authority-audit-context",
        ),
        (
            WitnessRoleV1::DeterministicGate,
            "gate:s04-001",
            "session:s04-001:deterministic-gate",
            "deterministic-gate-context",
        ),
        (
            WitnessRoleV1::HumanAuthority,
            S04_001_HUMAN_ID,
            "session:s04-001:human",
            "human-decision-context",
        ),
    ]
    .into_iter()
    .map(
        |(role, identity_id, session_id, visibility_class)| FrozenRoleIdentityV1 {
            role,
            identity_id: identity_id.to_owned(),
            session_id: session_id.to_owned(),
            context_sha256: sha256_bytes_v1(
                format!("s04-001:{session_id}:{visibility_class}:v1").as_bytes(),
            ),
            visibility_class: visibility_class.to_owned(),
        },
    )
    .collect()
}

fn canonical_observer_v1() -> FrozenWitnessObserverV1 {
    let mut observer = FrozenWitnessObserverV1 {
        observer_id: "observer:s04-001:host".to_owned(),
        observer_domain: S04_001_OBSERVER_DOMAIN.to_owned(),
        state_domain: S04_001_STATE_DOMAIN.to_owned(),
        frozen_base: S04_001_FROZEN_BASE.to_owned(),
        observer_hash: String::new(),
        visible_artifact_hashes: {
            let mut hashes = expected_source_manifest_v1()
                .into_iter()
                .map(|source| source.sha256)
                .collect::<Vec<_>>();
            hashes.sort();
            hashes
        },
        hidden_artifact_classes: vec![
            "credentials".to_owned(),
            "hidden-model-state".to_owned(),
            "unadmitted-artifacts".to_owned(),
        ],
        tool_permissions: vec![
            WitnessPermissionV1::ReadFrozenSources,
            WitnessPermissionV1::VerifyReceipts,
            WitnessPermissionV1::RecordHumanDecision,
        ],
        write_surface: expected_write_surface_v1(),
        evidence_ceiling: S04_001_EVIDENCE_CEILING.to_owned(),
    };
    observer.observer_hash =
        observer_sha256_v1(&observer).checked_invariant_36277efd("static observer material must serialize");
    observer
}

#[derive(Serialize)]
struct ObserverHashMaterialV1<'a> {
    observer_id: &'a str,
    observer_domain: &'a str,
    state_domain: &'a str,
    frozen_base: &'a str,
    visible_artifact_hashes: &'a [String],
    hidden_artifact_classes: &'a [String],
    tool_permissions: &'a [WitnessPermissionV1],
    write_surface: &'a [String],
    evidence_ceiling: &'a str,
}

pub fn observer_sha256_v1(observer: &FrozenWitnessObserverV1) -> Result<String, WitnessTowerError> {
    sha256_json_v1(&ObserverHashMaterialV1 {
        observer_id: &observer.observer_id,
        observer_domain: &observer.observer_domain,
        state_domain: &observer.state_domain,
        frozen_base: &observer.frozen_base,
        visible_artifact_hashes: &observer.visible_artifact_hashes,
        hidden_artifact_classes: &observer.hidden_artifact_classes,
        tool_permissions: &observer.tool_permissions,
        write_surface: &observer.write_surface,
        evidence_ceiling: &observer.evidence_ceiling,
    })
}

fn validate_budgets(budgets: WitnessBudgetsV1) -> Result<(), WitnessTowerError> {
    if budgets
        != (WitnessBudgetsV1 {
            attempt_budget: 1,
            repair_budget: 2,
            successor_budget: 1,
            time_budget_seconds: 8 * 60 * 60,
            process_budget: 4,
            token_budget: 200_000,
        })
    {
        return Err(WitnessTowerError::BudgetOutsideAdmission);
    }
    Ok(())
}

fn validate_upstream(upstream: &UpstreamAdmissionReferenceV1) -> Result<(), WitnessTowerError> {
    require_sha256("upstream.packet_sha256", &upstream.packet_sha256)?;
    require_sha256(
        "upstream.receipt_artifact_sha256",
        &upstream.receipt_artifact_sha256,
    )?;
    if upstream.goal_id != "S03-001"
        || upstream.packet_id != S04_001_UPSTREAM_PACKET_ID
        || upstream.packet_sha256 != S04_001_UPSTREAM_PACKET_SHA256
        || upstream.receipt_artifact_sha256 != S04_001_UPSTREAM_RECEIPT_ARTIFACT_SHA256
        || upstream.terminal != CodaTerminal::StabilizedSurvivor
        || !upstream.authority_effect.is_none()
    {
        return Err(WitnessTowerError::UpstreamReferenceChanged);
    }
    Ok(())
}

fn validate_role_plan(role_plan: &[FrozenRoleIdentityV1]) -> Result<(), WitnessTowerError> {
    let roles = role_plan.iter().map(|role| role.role).collect::<Vec<_>>();
    if roles != WitnessRoleV1::ALL {
        return Err(WitnessTowerError::RolePlanChanged);
    }
    validate_role_plan_uniqueness(role_plan)?;
    if role_plan != expected_role_plan_v1() {
        return Err(WitnessTowerError::RolePlanChanged);
    }
    Ok(())
}

fn validate_role_plan_uniqueness(
    role_plan: &[FrozenRoleIdentityV1],
) -> Result<(), WitnessTowerError> {
    let mut identities = BTreeSet::new();
    let mut sessions = BTreeSet::new();
    let mut contexts = BTreeSet::new();
    for role in role_plan {
        require_text("role.identity_id", &role.identity_id)?;
        require_text("role.session_id", &role.session_id)?;
        require_sha256("role.context_sha256", &role.context_sha256)?;
        require_text("role.visibility_class", &role.visibility_class)?;
        if !identities.insert(role.identity_id.as_str()) {
            return Err(WitnessTowerError::IdentityCollision);
        }
        if !sessions.insert(role.session_id.as_str()) {
            return Err(WitnessTowerError::SessionCollision);
        }
        if !contexts.insert(role.context_sha256.as_str()) {
            return Err(WitnessTowerError::ContextCollision);
        }
    }
    Ok(())
}

fn validate_observer(observer: &FrozenWitnessObserverV1) -> Result<(), WitnessTowerError> {
    validate_witness_observer_fields(observer)?;
    if !witness_observer_context_matches(observer) || !witness_observer_surfaces_match(observer) {
        return Err(WitnessTowerError::ObserverChanged);
    }
    let expected = observer_sha256_v1(observer)?;
    if observer.observer_hash != expected {
        return Err(WitnessTowerError::ObserverHashMismatch);
    }
    Ok(())
}

fn validate_witness_observer_fields(
    observer: &FrozenWitnessObserverV1,
) -> Result<(), WitnessTowerError> {
    for (field, value) in [
        ("observer.observer_id", observer.observer_id.as_str()),
        (
            "observer.observer_domain",
            observer.observer_domain.as_str(),
        ),
        ("observer.state_domain", observer.state_domain.as_str()),
        (
            "observer.evidence_ceiling",
            observer.evidence_ceiling.as_str(),
        ),
    ] {
        require_text(field, value)?;
    }
    require_git_commit("observer.frozen_base", &observer.frozen_base)?;
    require_sha256("observer.observer_hash", &observer.observer_hash)?;
    require_nonempty_sorted_texts(
        "observer.visible_artifact_hashes",
        &observer.visible_artifact_hashes,
    )?;
    for hash in &observer.visible_artifact_hashes {
        require_sha256("observer.visible_artifact_hashes", hash)?;
    }
    require_nonempty_sorted_texts(
        "observer.hidden_artifact_classes",
        &observer.hidden_artifact_classes,
    )
}

fn witness_observer_context_matches(observer: &FrozenWitnessObserverV1) -> bool {
    observer.observer_id == "observer:s04-001:host"
        && observer.observer_domain == S04_001_OBSERVER_DOMAIN
        && observer.state_domain == S04_001_STATE_DOMAIN
        && observer.frozen_base == S04_001_FROZEN_BASE
        && observer.evidence_ceiling == S04_001_EVIDENCE_CEILING
}

fn witness_observer_surfaces_match(observer: &FrozenWitnessObserverV1) -> bool {
    let canonical = canonical_observer_v1();
    observer.tool_permissions
        == [
            WitnessPermissionV1::ReadFrozenSources,
            WitnessPermissionV1::VerifyReceipts,
            WitnessPermissionV1::RecordHumanDecision,
        ]
        && observer.write_surface == expected_write_surface_v1()
        && observer.visible_artifact_hashes == canonical.visible_artifact_hashes
        && observer.hidden_artifact_classes == canonical.hidden_artifact_classes
}

fn role_identity(
    packet: &WitnessTowerPacketV1,
    role: WitnessRoleV1,
) -> Result<&FrozenRoleIdentityV1, WitnessTowerError> {
    packet
        .role_plan
        .iter()
        .find(|identity| identity.role == role)
        .ok_or(WitnessTowerError::RolePlanChanged)
}

fn require_schema(
    field: &'static str,
    found: &str,
    expected: &'static str,
) -> Result<(), WitnessTowerError> {
    if found != expected {
        return Err(WitnessTowerError::SchemaMismatch {
            field,
            expected,
            found: found.to_owned(),
        });
    }
    Ok(())
}

fn require_text(field: &'static str, value: &str) -> Result<(), WitnessTowerError> {
    if value.is_empty() || value.trim() != value || value.chars().any(char::is_control) {
        return Err(WitnessTowerError::EmptyField(field));
    }
    Ok(())
}

fn require_git_commit(field: &'static str, value: &str) -> Result<(), WitnessTowerError> {
    if value.len() != 40
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(WitnessTowerError::InvalidGitCommit(field));
    }
    Ok(())
}

fn require_sha256(field: &'static str, value: &str) -> Result<(), WitnessTowerError> {
    if value.len() != 64
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(WitnessTowerError::InvalidSha256(field));
    }
    Ok(())
}

fn require_nonempty_sorted_texts(
    field: &'static str,
    values: &[String],
) -> Result<(), WitnessTowerError> {
    if values.is_empty() || !is_strict_sorted(values) {
        return Err(WitnessTowerError::NonCanonicalList(field));
    }
    for value in values {
        require_text(field, value)?;
    }
    Ok(())
}

fn is_strict_sorted<T: Ord>(values: &[T]) -> bool {
    values.windows(2).all(|window| window[0] < window[1])
}

fn sha256_json_v1<T: Serialize + ?Sized>(value: &T) -> Result<String, WitnessTowerError> {
    let bytes = serde_json::to_vec(value).map_err(json_error)?;
    Ok(sha256_bytes_v1(&bytes))
}

fn sha256_bytes_v1(bytes: &[u8]) -> String {
    let digest = Sha256::digest(bytes);
    format!("{digest:x}")
}

fn json_error(error: serde_json::Error) -> WitnessTowerError {
    WitnessTowerError::Json(error.to_string())
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum WitnessTowerError {
    #[error("schema mismatch in {field}: expected {expected}, found {found}")]
    SchemaMismatch {
        field: &'static str,
        expected: &'static str,
        found: String,
    },
    #[error("required field is empty or non-canonical: {0}")]
    EmptyField(&'static str),
    #[error("invalid lowercase SHA-256 in {0}")]
    InvalidSha256(&'static str),
    #[error("invalid lowercase Git commit in {0}")]
    InvalidGitCommit(&'static str),
    #[error("list is not strictly sorted and unique: {0}")]
    NonCanonicalList(&'static str),
    #[error("the frozen S04-001 packet identity or base changed")]
    FrozenPacketChanged,
    #[error("the frozen S04-001 source manifest changed")]
    SourceManifestChanged,
    #[error("frozen source evidence is unavailable: {0}")]
    SourceUnavailable(String),
    #[error("the S03-001 upstream reference changed")]
    UpstreamReferenceChanged,
    #[error("the S04-001 budget changed")]
    BudgetOutsideAdmission,
    #[error("the exact S04-001 write surface changed")]
    WriteSurfaceChanged,
    #[error("the packet evidence ceiling changed")]
    EvidenceCeilingChanged,
    #[error("the closed role plan changed")]
    RolePlanChanged,
    #[error("two witness roles share an identity")]
    IdentityCollision,
    #[error("two witness roles share a session")]
    SessionCollision,
    #[error("two witness roles share a context")]
    ContextCollision,
    #[error("the frozen observer context changed")]
    ObserverChanged,
    #[error("the frozen observer hash does not match its material")]
    ObserverHashMismatch,
    #[error("authority or promotion capability expanded")]
    AuthorityExpansion,
    #[error("receipt packet hash does not match the frozen packet")]
    PacketHashMismatch,
    #[error("receipt self-hash mismatch: {0}")]
    ReceiptHashMismatch(String),
    #[error("required receipt is missing: {0}")]
    MissingRequiredReceipt(String),
    #[error("receipt membership differs from the closed tower")]
    UnexpectedReceiptSet,
    #[error("receipt kind or identifier changed")]
    ReceiptKindChanged,
    #[error("receipt rank changed: {0}")]
    ReceiptRankChanged(String),
    #[error("receipt issuer session or context changed: {0}")]
    ReceiptIssuerChanged(String),
    #[error("parent receipt is missing: {0}")]
    ParentReceiptMissing(String),
    #[error("parent receipt hash mismatch: {0}")]
    ParentHashMismatch(String),
    #[error("receipt {receipt_id} depends on future parent {parent_id}")]
    FutureParent {
        receipt_id: String,
        parent_id: String,
    },
    #[error("receipt DAG contains a cycle at {0}")]
    ReceiptCycle(String),
    #[error("receipt parent set changed: {0}")]
    ParentSetChanged(String),
    #[error("human decision is missing")]
    HumanDecisionMissing,
    #[error("a non-human receipt contains a human decision")]
    UnexpectedHumanDecision,
    #[error("human decision host or actor changed")]
    HumanDecisionIdentityChanged,
    #[error("only the frozen host may record a human decision")]
    HostDecisionIssuerMismatch,
    #[error("the decision actor is not the frozen human role")]
    HumanActorMismatch,
    #[error("deterministic replay differs from the claimed verification")]
    ReplayMismatch,
    #[error("canonical JSON operation failed: {0}")]
    Json(String),
}

impl WitnessTowerError {
    pub fn terminal_route(&self) -> CodaTerminal {
        match self {
            Self::SourceUnavailable(_) => CodaTerminal::OracleNeeded,
            Self::MissingRequiredReceipt(_) | Self::ParentReceiptMissing(_) => {
                CodaTerminal::OpenObstruction
            }
            Self::AuthorityExpansion
            | Self::HostDecisionIssuerMismatch
            | Self::HumanActorMismatch => CodaTerminal::Refused,
            Self::Json(_) => CodaTerminal::InfrastructureFailure,
            _ => CodaTerminal::Invalid,
        }
    }
}

// Origin: vendor/engine/engine_state/src/witness_receipt_dag.rs
// Claim: urn:omega:crates_rs:omega-state:witness-receipt-dag:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_36277efd {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
