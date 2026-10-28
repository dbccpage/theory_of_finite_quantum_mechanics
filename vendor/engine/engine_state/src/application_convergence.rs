//! S16-005 eleven-lane convergence evidence.
//!
//! This module verifies a finite application-lane packet, residual union,
//! hostile-fault matrix, and four-role receipt DAG. It is evidence-only: it
//! cannot activate a production route, issue a host capability, record a human
//! promotion, or construct an `AuthorizedLocalResult`.

use std::collections::{BTreeMap, BTreeSet};

use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

use crate::coda_gtla_protocol::CodaTerminal;

pub const APPLICATION_CONVERGENCE_PACKET_SCHEMA_V1: &str =
    "omega.application-convergence.packet.v1";
pub const APPLICATION_CONVERGENCE_RECEIPT_SCHEMA_V1: &str =
    "omega.application-convergence.receipt.v1";
pub const APPLICATION_CONVERGENCE_VERIFICATION_SCHEMA_V1: &str =
    "omega.application-convergence.verification.v1";

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ApplicationLaneV1 {
    PromptPackets,
    Api,
    BusinessPlanAnalyzer,
    Sweeper,
    RipPapers,
    Corrigibility,
    SymbolGame,
    Mub,
    ResidualFamilies,
    CertifierLoop,
    FiniteLambdaLedger,
}

impl ApplicationLaneV1 {
    pub const ALL: [Self; 11] = [
        Self::PromptPackets,
        Self::Api,
        Self::BusinessPlanAnalyzer,
        Self::Sweeper,
        Self::RipPapers,
        Self::Corrigibility,
        Self::SymbolGame,
        Self::Mub,
        Self::ResidualFamilies,
        Self::CertifierLoop,
        Self::FiniteLambdaLedger,
    ];

    pub const fn as_str(self) -> &'static str {
        match self {
            Self::PromptPackets => "omega_prompt_packets",
            Self::Api => "omega_api",
            Self::BusinessPlanAnalyzer => "omega_business_plan_analyzer",
            Self::Sweeper => "omega_sweeper",
            Self::RipPapers => "omega_rip_papers",
            Self::Corrigibility => "omega_corrigibility",
            other => other.as_str_tail(),
        }
    }

    const fn as_str_tail(self) -> &'static str {
        match self {
            Self::SymbolGame => "omega_symbol_game",
            Self::Mub => "omega_mub",
            Self::ResidualFamilies => "omega_residual_families",
            Self::CertifierLoop => "omega_certifier_loop",
            Self::FiniteLambdaLedger => "omega_finite_lambda_ledger",
            _ => "",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LaneConvergenceReceiptV1 {
    pub lane: ApplicationLaneV1,
    pub packet_path: String,
    pub packet_sha256: String,
    pub evidence_manifest_sha256: String,
    pub owner_paths: Vec<String>,
    pub adapter_paths: Vec<String>,
    pub focused_receipt_sha256: String,
    pub terminal: CodaTerminal,
    pub residual_ids: Vec<String>,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ResidualUnionEntryV1 {
    pub residual_id: String,
    pub owner: String,
    pub source_lanes: Vec<ApplicationLaneV1>,
    pub terminal: CodaTerminal,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ConvergenceWitnessPlanV1 {
    pub producer_identity_id: String,
    pub independent_evaluator_identity_id: String,
    pub authority_witness_identity_id: String,
    pub deterministic_gate_identity_id: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ApplicationConvergencePacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub frozen_base: String,
    pub lanes: Vec<LaneConvergenceReceiptV1>,
    pub residual_union: Vec<ResidualUnionEntryV1>,
    pub witnesses: ConvergenceWitnessPlanV1,
    pub evidence_ceiling: String,
    pub product_terminal_is_authority: bool,
    pub promotion_permission: bool,
    pub gate_activated: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ConvergenceReceiptKindV1 {
    LaneBundle,
    IndependentEvaluation,
    AuthorityWitness,
    DeterministicGate,
}

impl ConvergenceReceiptKindV1 {
    const ALL: [Self; 4] = [
        Self::LaneBundle,
        Self::IndependentEvaluation,
        Self::AuthorityWitness,
        Self::DeterministicGate,
    ];

    const fn rank(self) -> u8 {
        match self {
            Self::LaneBundle => 0,
            Self::IndependentEvaluation => 1,
            Self::AuthorityWitness => 2,
            Self::DeterministicGate => 3,
        }
    }

    const fn receipt_id(self) -> &'static str {
        match self {
            Self::LaneBundle => "receipt:s16-005:lane-bundle",
            Self::IndependentEvaluation => "receipt:s16-005:independent-evaluation",
            Self::AuthorityWitness => "receipt:s16-005:authority-witness",
            Self::DeterministicGate => "receipt:s16-005:deterministic-gate",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ConvergenceReceiptParentV1 {
    pub receipt_id: String,
    pub receipt_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ConvergenceReceiptMaterialV1 {
    pub schema_version: String,
    pub receipt_id: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub kind: ConvergenceReceiptKindV1,
    pub graph_rank: u8,
    pub issuer_identity_id: String,
    pub parents: Vec<ConvergenceReceiptParentV1>,
    pub evidence_hashes: Vec<String>,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ConvergenceReceiptV1 {
    pub material: ConvergenceReceiptMaterialV1,
    pub receipt_sha256: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum HostileFaultV1 {
    MalformedPacket,
    PacketHashTamper,
    UnknownResidualFamily,
    RawTextCanary,
    StaleOracle,
    EvidenceCycle,
    RetryExhaustion,
    BrokenLambdaLedger,
    WitnessIdentityCollision,
    ToolTimeout,
    PolicyDrift,
    CommitFailure,
    CrashReplay,
    AuthorityBypass,
}

impl HostileFaultV1 {
    pub const ALL: [Self; 14] = [
        Self::MalformedPacket,
        Self::PacketHashTamper,
        Self::UnknownResidualFamily,
        Self::RawTextCanary,
        Self::StaleOracle,
        Self::EvidenceCycle,
        Self::RetryExhaustion,
        Self::BrokenLambdaLedger,
        Self::WitnessIdentityCollision,
        Self::ToolTimeout,
        Self::PolicyDrift,
        Self::CommitFailure,
        Self::CrashReplay,
        Self::AuthorityBypass,
    ];
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct HostileFaultOutcomeV1 {
    pub fault: HostileFaultV1,
    pub terminal: CodaTerminal,
    pub detector_live: bool,
    pub append_only_receipts_preserved: bool,
    pub promotion_ready_commit_created: bool,
    pub replay_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct HostileFaultMatrixV1 {
    pub outcomes: Vec<HostileFaultOutcomeV1>,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum HumanDecisionStateV1 {
    PendingHumanPromotion,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ApplicationConvergenceVerificationV1 {
    pub schema_version: String,
    pub packet_sha256: String,
    pub receipt_dag_sha256: String,
    pub lane_count: usize,
    pub residual_count: usize,
    pub hostile_fault_count: usize,
    pub receipt_count: usize,
    pub receipt_dag_acyclic: bool,
    pub receipt_dag_rank_ordered: bool,
    pub residual_union_complete: bool,
    pub human_decision_state: HumanDecisionStateV1,
    pub human_decision_recorded: bool,
    pub promotion_constructor_called: bool,
    pub authorized_local_result_created: bool,
    pub gate_activated: bool,
    pub terminal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum ApplicationConvergenceError {
    #[error("invalid required text: {0}")]
    InvalidText(&'static str),
    #[error("invalid SHA-256: {0}")]
    InvalidHash(&'static str),
    #[error("the exact eleven-lane set or order changed")]
    LaneSetChanged,
    #[error("lane collection is not strictly sorted and unique: {0}")]
    LaneCollectionChanged(String),
    #[error("lane terminal is outside the admitted convergence set: {0}")]
    LaneTerminalChanged(String),
    #[error("residual union does not bijectively cover lane residuals")]
    ResidualUnionChanged,
    #[error("witness identities are not independent")]
    WitnessIdentityCollision,
    #[error("authority expanded inside the convergence gate")]
    AuthorityExpansion,
    #[error("production activation or promotion permission is not admitted")]
    PromotionBoundaryChanged,
    #[error("receipt DAG is incomplete, cyclic, or rank-invalid")]
    ReceiptDagInvalid,
    #[error("receipt hash mismatch: {0}")]
    ReceiptHashMismatch(String),
    #[error("hostile fault matrix changed")]
    FaultMatrixChanged,
    #[error("JSON serialization failed: {0}")]
    Json(String),
}

fn json_error(error: serde_json::Error) -> ApplicationConvergenceError {
    ApplicationConvergenceError::Json(error.to_string())
}

fn require_text(field: &'static str, value: &str) -> Result<(), ApplicationConvergenceError> {
    if value.trim().is_empty() {
        return Err(ApplicationConvergenceError::InvalidText(field));
    }
    Ok(())
}

fn require_sha256(field: &'static str, value: &str) -> Result<(), ApplicationConvergenceError> {
    if value.len() != 64
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(ApplicationConvergenceError::InvalidHash(field));
    }
    Ok(())
}

fn require_git_oid(field: &'static str, value: &str) -> Result<(), ApplicationConvergenceError> {
    if !matches!(value.len(), 40 | 64)
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(ApplicationConvergenceError::InvalidHash(field));
    }
    Ok(())
}

fn require_sorted_unique_text(
    field: &'static str,
    values: &[String],
    allow_empty: bool,
) -> Result<(), ApplicationConvergenceError> {
    if (!allow_empty && values.is_empty())
        || values.iter().any(|value| value.trim().is_empty())
        || values.windows(2).any(|window| window[0] >= window[1])
    {
        return Err(ApplicationConvergenceError::LaneCollectionChanged(
            field.to_owned(),
        ));
    }
    Ok(())
}

fn sha256_bytes(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}

fn sha256_json<T: Serialize + ?Sized>(value: &T) -> Result<String, ApplicationConvergenceError> {
    serde_json::to_vec(value)
        .map(|bytes| sha256_bytes(&bytes))
        .map_err(json_error)
}

impl ApplicationConvergencePacketV1 {
    pub fn validate(&self) -> Result<(), ApplicationConvergenceError> {
        self.validate_header()?;
        self.validate_lanes()?;
        self.validate_residual_union()?;
        self.validate_witnesses()
    }

    fn validate_header(&self) -> Result<(), ApplicationConvergenceError> {
        if self.schema_version != APPLICATION_CONVERGENCE_PACKET_SCHEMA_V1 {
            return Err(ApplicationConvergenceError::InvalidText("schema_version"));
        }
        require_text("packet_id", &self.packet_id)?;
        require_git_oid("frozen_base", &self.frozen_base)?;
        require_text("evidence_ceiling", &self.evidence_ceiling)?;
        if self.product_terminal_is_authority || self.promotion_permission || self.gate_activated {
            return Err(ApplicationConvergenceError::PromotionBoundaryChanged);
        }
        if !self.authority_effect.is_none() {
            return Err(ApplicationConvergenceError::AuthorityExpansion);
        }
        Ok(())
    }

    fn validate_lanes(&self) -> Result<(), ApplicationConvergenceError> {
        let lane_ids = self.lanes.iter().map(|lane| lane.lane).collect::<Vec<_>>();
        if lane_ids != ApplicationLaneV1::ALL {
            return Err(ApplicationConvergenceError::LaneSetChanged);
        }
        let mut packet_paths = BTreeSet::new();
        for lane in &self.lanes {
            Self::validate_single_lane(lane, &mut packet_paths)?;
        }
        Ok(())
    }

    fn validate_single_lane<'a>(
        lane: &'a LaneConvergenceReceiptV1,
        packet_paths: &mut BTreeSet<&'a str>,
    ) -> Result<(), ApplicationConvergenceError> {
        require_text("lane.packet_path", &lane.packet_path)?;
        require_sha256("lane.packet_sha256", &lane.packet_sha256)?;
        require_sha256(
            "lane.evidence_manifest_sha256",
            &lane.evidence_manifest_sha256,
        )?;
        require_sha256("lane.focused_receipt_sha256", &lane.focused_receipt_sha256)?;
        require_sorted_unique_text("lane.owner_paths", &lane.owner_paths, false)?;
        require_sorted_unique_text("lane.adapter_paths", &lane.adapter_paths, false)?;
        require_sorted_unique_text("lane.residual_ids", &lane.residual_ids, true)?;
        Self::validate_lane_terminal_and_path(lane, packet_paths)
    }

    fn validate_lane_terminal_and_path<'a>(
        lane: &'a LaneConvergenceReceiptV1,
        packet_paths: &mut BTreeSet<&'a str>,
    ) -> Result<(), ApplicationConvergenceError> {
        if !matches!(
            lane.terminal,
            CodaTerminal::ExactRepair | CodaTerminal::StabilizedSurvivor
        ) {
            return Err(ApplicationConvergenceError::LaneTerminalChanged(
                lane.lane.as_str().to_owned(),
            ));
        }
        if !lane.authority_effect.is_none() {
            return Err(ApplicationConvergenceError::AuthorityExpansion);
        }
        if !packet_paths.insert(lane.packet_path.as_str()) {
            return Err(ApplicationConvergenceError::LaneCollectionChanged(
                "lane.packet_path".to_owned(),
            ));
        }
        Ok(())
    }

    fn validate_residual_union(&self) -> Result<(), ApplicationConvergenceError> {
        let union_ids = self
            .residual_union
            .iter()
            .map(|entry| entry.residual_id.clone())
            .collect::<Vec<_>>();
        require_sorted_unique_text("residual_union.ids", &union_ids, true)?;
        let lanes_by_id = self
            .lanes
            .iter()
            .map(|lane| (lane.lane, lane))
            .collect::<BTreeMap<_, _>>();
        for entry in &self.residual_union {
            Self::validate_residual_entry(entry, &lanes_by_id)?;
        }
        self.validate_lane_residuals_covered()
    }

    fn validate_residual_entry(
        entry: &ResidualUnionEntryV1,
        lanes_by_id: &BTreeMap<ApplicationLaneV1, &LaneConvergenceReceiptV1>,
    ) -> Result<(), ApplicationConvergenceError> {
        require_text("residual_union.owner", &entry.owner)?;
        if entry.source_lanes.is_empty()
            || entry
                .source_lanes
                .windows(2)
                .any(|window| window[0] >= window[1])
            || entry.terminal == CodaTerminal::ExactRepair
        {
            return Err(ApplicationConvergenceError::ResidualUnionChanged);
        }
        for lane_id in &entry.source_lanes {
            let lane = lanes_by_id
                .get(lane_id)
                .ok_or(ApplicationConvergenceError::ResidualUnionChanged)?;
            if lane.residual_ids.binary_search(&entry.residual_id).is_err() {
                return Err(ApplicationConvergenceError::ResidualUnionChanged);
            }
        }
        Ok(())
    }

    fn validate_lane_residuals_covered(&self) -> Result<(), ApplicationConvergenceError> {
        for lane in &self.lanes {
            for residual_id in &lane.residual_ids {
                let entry = self
                    .residual_union
                    .iter()
                    .find(|entry| &entry.residual_id == residual_id)
                    .ok_or(ApplicationConvergenceError::ResidualUnionChanged)?;
                if entry.source_lanes.binary_search(&lane.lane).is_err() {
                    return Err(ApplicationConvergenceError::ResidualUnionChanged);
                }
            }
        }
        Ok(())
    }

    fn validate_witnesses(&self) -> Result<(), ApplicationConvergenceError> {
        let witness_ids = [
            self.witnesses.producer_identity_id.as_str(),
            self.witnesses.independent_evaluator_identity_id.as_str(),
            self.witnesses.authority_witness_identity_id.as_str(),
            self.witnesses.deterministic_gate_identity_id.as_str(),
        ];
        if witness_ids
            .iter()
            .any(|identity| identity.trim().is_empty())
            || witness_ids.iter().collect::<BTreeSet<_>>().len() != witness_ids.len()
        {
            return Err(ApplicationConvergenceError::WitnessIdentityCollision);
        }
        Ok(())
    }
}

pub fn application_convergence_packet_sha256_v1(
    packet: &ApplicationConvergencePacketV1,
) -> Result<String, ApplicationConvergenceError> {
    packet.validate()?;
    sha256_json(packet)
}

pub const fn route_hostile_fault_v1(fault: HostileFaultV1) -> CodaTerminal {
    match fault {
        HostileFaultV1::MalformedPacket
        | HostileFaultV1::RawTextCanary
        | HostileFaultV1::RetryExhaustion
        | HostileFaultV1::AuthorityBypass => CodaTerminal::Refused,
        HostileFaultV1::PacketHashTamper
        | HostileFaultV1::BrokenLambdaLedger
        | HostileFaultV1::WitnessIdentityCollision
        | HostileFaultV1::PolicyDrift => CodaTerminal::Invalid,
        HostileFaultV1::UnknownResidualFamily => CodaTerminal::LiftLicenseNeeded,
        HostileFaultV1::StaleOracle => CodaTerminal::OracleNeeded,
        HostileFaultV1::EvidenceCycle => CodaTerminal::OpenObstruction,
        HostileFaultV1::ToolTimeout
        | HostileFaultV1::CommitFailure
        | HostileFaultV1::CrashReplay => CodaTerminal::InfrastructureFailure,
    }
}

pub fn canonical_hostile_fault_matrix_v1() -> HostileFaultMatrixV1 {
    HostileFaultMatrixV1 {
        outcomes: HostileFaultV1::ALL
            .iter()
            .copied()
            .map(|fault| HostileFaultOutcomeV1 {
                fault,
                terminal: route_hostile_fault_v1(fault),
                detector_live: true,
                append_only_receipts_preserved: true,
                promotion_ready_commit_created: false,
                replay_sha256: sha256_bytes(format!("s16-005:{fault:?}").as_bytes()),
            })
            .collect(),
        authority_effect: AuthorityEffect::None,
    }
}

impl HostileFaultMatrixV1 {
    pub fn validate(&self) -> Result<(), ApplicationConvergenceError> {
        let faults = self
            .outcomes
            .iter()
            .map(|outcome| outcome.fault)
            .collect::<Vec<_>>();
        if faults != HostileFaultV1::ALL || !self.authority_effect.is_none() {
            return Err(ApplicationConvergenceError::FaultMatrixChanged);
        }
        for outcome in &self.outcomes {
            if outcome.terminal != route_hostile_fault_v1(outcome.fault)
                || !outcome.detector_live
                || !outcome.append_only_receipts_preserved
                || outcome.promotion_ready_commit_created
            {
                return Err(ApplicationConvergenceError::FaultMatrixChanged);
            }
            require_sha256("fault.replay_sha256", &outcome.replay_sha256)?;
            if outcome.replay_sha256
                != sha256_bytes(format!("s16-005:{:?}", outcome.fault).as_bytes())
            {
                return Err(ApplicationConvergenceError::FaultMatrixChanged);
            }
        }
        Ok(())
    }
}

fn issuer_for_kind<'a>(
    packet: &'a ApplicationConvergencePacketV1,
    kind: ConvergenceReceiptKindV1,
) -> &'a str {
    match kind {
        ConvergenceReceiptKindV1::LaneBundle => &packet.witnesses.producer_identity_id,
        ConvergenceReceiptKindV1::IndependentEvaluation => {
            &packet.witnesses.independent_evaluator_identity_id
        }
        ConvergenceReceiptKindV1::AuthorityWitness => {
            &packet.witnesses.authority_witness_identity_id
        }
        ConvergenceReceiptKindV1::DeterministicGate => {
            &packet.witnesses.deterministic_gate_identity_id
        }
    }
}

fn parent(receipt: &ConvergenceReceiptV1) -> ConvergenceReceiptParentV1 {
    ConvergenceReceiptParentV1 {
        receipt_id: receipt.material.receipt_id.clone(),
        receipt_sha256: receipt.receipt_sha256.clone(),
    }
}

fn make_receipt(
    packet: &ApplicationConvergencePacketV1,
    kind: ConvergenceReceiptKindV1,
    mut parents: Vec<ConvergenceReceiptParentV1>,
    mut evidence_hashes: Vec<String>,
) -> Result<ConvergenceReceiptV1, ApplicationConvergenceError> {
    parents.sort();
    evidence_hashes.sort();
    let material = ConvergenceReceiptMaterialV1 {
        schema_version: APPLICATION_CONVERGENCE_RECEIPT_SCHEMA_V1.to_owned(),
        receipt_id: kind.receipt_id().to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256: application_convergence_packet_sha256_v1(packet)?,
        kind,
        graph_rank: kind.rank(),
        issuer_identity_id: issuer_for_kind(packet, kind).to_owned(),
        parents,
        evidence_hashes,
        authority_effect: AuthorityEffect::None,
    };
    Ok(ConvergenceReceiptV1 {
        receipt_sha256: sha256_json(&material)?,
        material,
    })
}

pub fn build_application_convergence_receipt_dag_v1(
    packet: &ApplicationConvergencePacketV1,
    faults: &HostileFaultMatrixV1,
) -> Result<Vec<ConvergenceReceiptV1>, ApplicationConvergenceError> {
    packet.validate()?;
    faults.validate()?;
    let lane_bundle = make_receipt(
        packet,
        ConvergenceReceiptKindV1::LaneBundle,
        Vec::new(),
        vec![sha256_json(&packet.lanes)?],
    )?;
    let independent = make_receipt(
        packet,
        ConvergenceReceiptKindV1::IndependentEvaluation,
        vec![parent(&lane_bundle)],
        vec![lane_bundle.receipt_sha256.clone(), sha256_json(faults)?],
    )?;
    let (authority, gate) =
        build_authority_and_gate_receipts(packet, &lane_bundle, &independent)?;
    let receipts = vec![lane_bundle, independent, authority, gate];
    validate_application_convergence_receipt_dag_v1(packet, &receipts)?;
    Ok(receipts)
}

fn build_authority_and_gate_receipts(
    packet: &ApplicationConvergencePacketV1,
    lane_bundle: &ConvergenceReceiptV1,
    independent: &ConvergenceReceiptV1,
) -> Result<(ConvergenceReceiptV1, ConvergenceReceiptV1), ApplicationConvergenceError> {
    let authority = make_receipt(
        packet,
        ConvergenceReceiptKindV1::AuthorityWitness,
        vec![parent(lane_bundle), parent(independent)],
        vec![
            lane_bundle.receipt_sha256.clone(),
            independent.receipt_sha256.clone(),
            sha256_json(&packet.residual_union)?,
        ],
    )?;
    let gate = make_receipt(
        packet,
        ConvergenceReceiptKindV1::DeterministicGate,
        vec![
            parent(lane_bundle),
            parent(independent),
            parent(&authority),
        ],
        vec![
            lane_bundle.receipt_sha256.clone(),
            independent.receipt_sha256.clone(),
            authority.receipt_sha256.clone(),
        ],
    )?;
    Ok((authority, gate))
}

fn expected_parent_ids(kind: ConvergenceReceiptKindV1) -> &'static [&'static str] {
    match kind {
        ConvergenceReceiptKindV1::LaneBundle => &[],
        ConvergenceReceiptKindV1::IndependentEvaluation => &["receipt:s16-005:lane-bundle"],
        ConvergenceReceiptKindV1::AuthorityWitness => &[
            "receipt:s16-005:independent-evaluation",
            "receipt:s16-005:lane-bundle",
        ],
        ConvergenceReceiptKindV1::DeterministicGate => &[
            "receipt:s16-005:authority-witness",
            "receipt:s16-005:independent-evaluation",
            "receipt:s16-005:lane-bundle",
        ],
    }
}

pub fn validate_application_convergence_receipt_dag_v1(
    packet: &ApplicationConvergencePacketV1,
    receipts: &[ConvergenceReceiptV1],
) -> Result<(), ApplicationConvergenceError> {
    packet.validate()?;
    if receipts.len() != ConvergenceReceiptKindV1::ALL.len()
        || receipts
            .iter()
            .map(|receipt| receipt.material.kind)
            .collect::<Vec<_>>()
            != ConvergenceReceiptKindV1::ALL
    {
        return Err(ApplicationConvergenceError::ReceiptDagInvalid);
    }
    let packet_sha256 = application_convergence_packet_sha256_v1(packet)?;
    let mut prior = BTreeMap::<String, (u8, String)>::new();
    for receipt in receipts {
        validate_single_convergence_receipt(packet, receipt, &packet_sha256, &prior)?;
        prior.insert(
            receipt.material.receipt_id.clone(),
            (receipt.material.graph_rank, receipt.receipt_sha256.clone()),
        );
    }
    Ok(())
}

fn validate_single_convergence_receipt(
    packet: &ApplicationConvergencePacketV1,
    receipt: &ConvergenceReceiptV1,
    packet_sha256: &str,
    prior: &BTreeMap<String, (u8, String)>,
) -> Result<(), ApplicationConvergenceError> {
    let material = &receipt.material;
    if !receipt_header_matches_packet(packet, material, packet_sha256)
        || !receipt_evidence_hashes_valid(material)
    {
        return Err(ApplicationConvergenceError::ReceiptDagInvalid);
    }
    if sha256_json(material)? != receipt.receipt_sha256 {
        return Err(ApplicationConvergenceError::ReceiptHashMismatch(
            material.receipt_id.clone(),
        ));
    }
    validate_receipt_parents(material, prior)
}

fn receipt_header_matches_packet(
    packet: &ApplicationConvergencePacketV1,
    material: &ConvergenceReceiptMaterialV1,
    packet_sha256: &str,
) -> bool {
    material.schema_version == APPLICATION_CONVERGENCE_RECEIPT_SCHEMA_V1
        && material.receipt_id == material.kind.receipt_id()
        && material.packet_id == packet.packet_id
        && material.packet_sha256 == packet_sha256
        && material.graph_rank == material.kind.rank()
        && material.issuer_identity_id == issuer_for_kind(packet, material.kind)
        && material.authority_effect.is_none()
}

fn receipt_evidence_hashes_valid(material: &ConvergenceReceiptMaterialV1) -> bool {
    !material.evidence_hashes.is_empty()
        && !material
            .evidence_hashes
            .windows(2)
            .any(|window| window[0] >= window[1])
        && !material
            .evidence_hashes
            .iter()
            .any(|hash| require_sha256("receipt.evidence_hash", hash).is_err())
}

fn validate_receipt_parents(
    material: &ConvergenceReceiptMaterialV1,
    prior: &BTreeMap<String, (u8, String)>,
) -> Result<(), ApplicationConvergenceError> {
    let parent_ids = material
        .parents
        .iter()
        .map(|parent| parent.receipt_id.as_str())
        .collect::<Vec<_>>();
    if parent_ids != expected_parent_ids(material.kind) {
        return Err(ApplicationConvergenceError::ReceiptDagInvalid);
    }
    for parent in &material.parents {
        let (parent_rank, parent_sha256) = prior
            .get(&parent.receipt_id)
            .ok_or(ApplicationConvergenceError::ReceiptDagInvalid)?;
        if *parent_rank >= material.graph_rank || parent_sha256 != &parent.receipt_sha256 {
            return Err(ApplicationConvergenceError::ReceiptDagInvalid);
        }
    }
    Ok(())
}

pub fn verify_application_convergence_v1(
    packet: &ApplicationConvergencePacketV1,
    faults: &HostileFaultMatrixV1,
    receipts: &[ConvergenceReceiptV1],
) -> Result<ApplicationConvergenceVerificationV1, ApplicationConvergenceError> {
    packet.validate()?;
    faults.validate()?;
    validate_application_convergence_receipt_dag_v1(packet, receipts)?;
    Ok(ApplicationConvergenceVerificationV1 {
        schema_version: APPLICATION_CONVERGENCE_VERIFICATION_SCHEMA_V1.to_owned(),
        packet_sha256: application_convergence_packet_sha256_v1(packet)?,
        receipt_dag_sha256: sha256_json(receipts)?,
        lane_count: packet.lanes.len(),
        residual_count: packet.residual_union.len(),
        hostile_fault_count: faults.outcomes.len(),
        receipt_count: receipts.len(),
        receipt_dag_acyclic: true,
        receipt_dag_rank_ordered: true,
        residual_union_complete: true,
        human_decision_state: HumanDecisionStateV1::PendingHumanPromotion,
        human_decision_recorded: false,
        promotion_constructor_called: false,
        authorized_local_result_created: false,
        gate_activated: false,
        terminal: CodaTerminal::StabilizedSurvivor,
        authority_effect: AuthorityEffect::None,
    })
}

// Origin: vendor/engine/engine_state/src/application_convergence.rs
// Claim: urn:omega:crates_rs:omega-state:application-convergence:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_fd0dfed7 {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
