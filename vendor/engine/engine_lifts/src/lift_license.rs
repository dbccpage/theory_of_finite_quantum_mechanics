//! § 7, Definition 16.10: Licensed Lift
//!
//! A **lift** is a map $F: Q_n \to Q_{n+1}$ together with a **forgetful
//! descent** $U: Q_{n+1} \to Q_n$ such that $U \circ F$ is computable and
//! preserves exact classes. No lift is admissible without an explicit
//! descent map.

use engine_wdp::ddc::dda_alphabet::{DdaOp, DdaStep};
use engine_wdp::ddc::op_verification::{
    verify_step_with_witness, CochainState, OpViolation, StepEvidence, StepWitness,
};
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

/// Legacy metadata record for Definition 16.10.
///
/// This contains the metadata for a lift-descent pair, not the maps
/// themselves. S02-002 does not use this record as proof that a lift is
/// licensed; the closed candidate/evaluation types below carry that boundary.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LiftLicense {
    /// Checked obstruction packet hash.
    pub packet_hash: [u8; 32],
    /// Whether repair exhaustion was certified.
    pub exhaustion_certified: bool,
    /// Finite context witness identifier.
    pub witness_id: String,
    /// Comparison map to the old representation (hash).
    pub comparison_hash: [u8; 32],
    /// Rollback or migration record (hash).
    pub rollback_hash: [u8; 32],
    /// Level being lifted from.
    pub source_level: usize,
    /// Level being lifted to.
    pub target_level: usize,
}

pub const LIFT_TRIGGER_SCHEMA_VERSION: &str = "omega.lift-trigger.v1";
pub const LIFT_license_CANDIDATE_SCHEMA_VERSION: &str = "omega.lift-license-candidate.v1";
pub const LIFT_license_EVALUATION_SCHEMA_VERSION: &str = "omega.lift-license-evaluation.v1";

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum LiftTerminalRouteV1 {
    ExactRepair,
    StabilizedSurvivor,
    OpenObstruction,
    OracleNeeded,
    Refused,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum LiftLicenseValidationStatusV1 {
    AdmissibleForLicensing,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LiftTriggerV1 {
    pub schema_version: String,
    pub trigger_id: String,
    pub operation: DdaOp,
    pub operator_id: String,
    pub operator_manifest_sha256: String,
    pub source_carrier_sha256: String,
    pub target_carrier_sha256: String,
    pub obstruction_summary_sha256: String,
    pub evidence_ceiling: String,
    pub authority_effect: AuthorityEffect,
}

impl LiftTriggerV1 {
    pub fn validate(&self) -> Result<(), LiftLicenseError> {
        require_schema(
            LIFT_TRIGGER_SCHEMA_VERSION,
            &self.schema_version,
            "trigger.schema_version",
        )?;
        for (field, value) in [
            ("trigger.trigger_id", self.trigger_id.as_str()),
            ("trigger.operator_id", self.operator_id.as_str()),
            ("trigger.evidence_ceiling", self.evidence_ceiling.as_str()),
        ] {
            require_text(field, value)?;
        }
        for (field, value) in [
            (
                "trigger.operator_manifest_sha256",
                self.operator_manifest_sha256.as_str(),
            ),
            (
                "trigger.source_carrier_sha256",
                self.source_carrier_sha256.as_str(),
            ),
            (
                "trigger.target_carrier_sha256",
                self.target_carrier_sha256.as_str(),
            ),
            (
                "trigger.obstruction_summary_sha256",
                self.obstruction_summary_sha256.as_str(),
            ),
        ] {
            require_sha256(field, value)?;
        }
        if !matches!(
            self.operation,
            DdaOp::ContextExposure | DdaOp::Descent | DdaOp::Lift
        ) {
            return Err(LiftLicenseError::NotCarrierChanging(self.operation));
        }
        if self.source_carrier_sha256 == self.target_carrier_sha256 {
            return Err(LiftLicenseError::CarrierUnchanged);
        }
        if !self.authority_effect.is_none() {
            return Err(LiftLicenseError::AuthorityExpansion);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ObstructionWitnessV1 {
    pub witness_id: String,
    pub carrier_sha256: String,
    pub obstruction_sha256: String,
    pub checked_packet_sha256: String,
    pub repair_exhaustion_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PreservationWitnessV1 {
    pub witness_id: String,
    pub invariant_id: String,
    pub source_invariant_sha256: String,
    pub target_invariant_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct NonDestructionWitnessV1 {
    pub witness_id: String,
    pub source_protected_sha256: Vec<String>,
    pub target_protected_sha256: Vec<String>,
    pub rollback_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LiftBudgetBoundaryV1 {
    pub witness_id: String,
    pub max_cost_units: u64,
    pub requested_cost_units: u64,
    pub max_new_dimensions: u32,
    pub requested_new_dimensions: u32,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LiftAuthorityBoundaryV1 {
    pub witness_id: String,
    pub promotion_performed: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LiftTerminalizerRouteV1 {
    pub route_id: String,
    pub terminalizer_id: String,
    pub replay_sha256: String,
    pub terminal: LiftTerminalRouteV1,
}

/// Evidence-only proposal for a scope-bound lift license.
///
/// A complete candidate may be evaluated as `AdmissibleForLicensing`; it is
/// not an issued `LiftLicense`, does not execute a DDA step, and carries no
/// authority. Human/licensing-boundary issuance remains separate.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LiftLicenseCandidateV1 {
    pub schema_version: String,
    pub candidate_id: String,
    pub proposed_license_id: String,
    pub trigger_sha256: String,
    pub operation: DdaOp,
    pub operator_id: String,
    pub operator_manifest_sha256: String,
    pub source_carrier_sha256: String,
    pub target_carrier_sha256: String,
    pub obstruction_witness: Option<ObstructionWitnessV1>,
    pub preservation_witness: Option<PreservationWitnessV1>,
    pub non_destruction_witness: Option<NonDestructionWitnessV1>,
    pub budget_boundary: Option<LiftBudgetBoundaryV1>,
    pub authority_boundary: Option<LiftAuthorityBoundaryV1>,
    pub terminalizer_route: Option<LiftTerminalizerRouteV1>,
    pub constructor_set_sha256: String,
    pub minimality_witness_sha256: String,
    pub replay_manifest_sha256: String,
    pub evidence_ceiling: String,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LiftLicenseEvaluationV1 {
    pub schema_version: String,
    pub candidate_id: String,
    pub trigger_sha256: String,
    pub obstruction_checked: bool,
    pub preservation_checked: bool,
    pub non_destruction_checked: bool,
    pub budget_checked: bool,
    pub authority_boundary_checked: bool,
    pub terminalizer_route_checked: bool,
    pub scope_checked: bool,
    pub status: LiftLicenseValidationStatusV1,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct DdaLiftCandidateEvaluationV1 {
    pub structural_evidence: StepEvidence,
    pub license_evaluation: LiftLicenseEvaluationV1,
    pub authority_effect: AuthorityEffect,
}

fn validate_candidate_fields_and_hashes(
    candidate: &LiftLicenseCandidateV1,
) -> Result<(), LiftLicenseError> {
    require_schema(
        LIFT_license_CANDIDATE_SCHEMA_VERSION,
        &candidate.schema_version,
        "candidate.schema_version",
    )?;
    for (field, value) in [
        ("candidate.candidate_id", candidate.candidate_id.as_str()),
        (
            "candidate.proposed_license_id",
            candidate.proposed_license_id.as_str(),
        ),
        ("candidate.operator_id", candidate.operator_id.as_str()),
        (
            "candidate.evidence_ceiling",
            candidate.evidence_ceiling.as_str(),
        ),
    ] {
        require_text(field, value)?;
    }
    for (field, value) in [
        ("candidate.trigger_sha256", candidate.trigger_sha256.as_str()),
        (
            "candidate.operator_manifest_sha256",
            candidate.operator_manifest_sha256.as_str(),
        ),
        (
            "candidate.source_carrier_sha256",
            candidate.source_carrier_sha256.as_str(),
        ),
        (
            "candidate.target_carrier_sha256",
            candidate.target_carrier_sha256.as_str(),
        ),
        (
            "candidate.constructor_set_sha256",
            candidate.constructor_set_sha256.as_str(),
        ),
        (
            "candidate.minimality_witness_sha256",
            candidate.minimality_witness_sha256.as_str(),
        ),
        (
            "candidate.replay_manifest_sha256",
            candidate.replay_manifest_sha256.as_str(),
        ),
    ] {
        require_sha256(field, value)?;
    }
    Ok(())
}

fn validate_candidate_trigger_alignment(
    trigger: &LiftTriggerV1,
    candidate: &LiftLicenseCandidateV1,
) -> Result<String, LiftLicenseError> {
    let trigger_sha256 = lift_sha256_json_v1(trigger)?;
    if candidate.trigger_sha256 != trigger_sha256 {
        return Err(LiftLicenseError::TriggerHashMismatch);
    }
    let matches_scope = candidate.operation == trigger.operation
        && candidate.operator_id == trigger.operator_id
        && candidate.operator_manifest_sha256 == trigger.operator_manifest_sha256
        && candidate.source_carrier_sha256 == trigger.source_carrier_sha256
        && candidate.target_carrier_sha256 == trigger.target_carrier_sha256
        && candidate.evidence_ceiling == trigger.evidence_ceiling;
    if !matches_scope {
        return Err(LiftLicenseError::ScopeMismatch);
    }
    if !candidate.authority_effect.is_none() {
        return Err(LiftLicenseError::AuthorityExpansion);
    }
    Ok(trigger_sha256)
}

fn validate_candidate_witness_bundle(
    trigger: &LiftTriggerV1,
    candidate: &LiftLicenseCandidateV1,
) -> Result<(), LiftLicenseError> {
    let obstruction = candidate
        .obstruction_witness
        .as_ref()
        .ok_or(LiftLicenseError::MissingObstructionWitness)?;
    validate_obstruction_witness(trigger, obstruction)?;

    let preservation = candidate
        .preservation_witness
        .as_ref()
        .ok_or(LiftLicenseError::MissingPreservationWitness)?;
    validate_preservation_witness(preservation)?;

    let non_destruction = candidate
        .non_destruction_witness
        .as_ref()
        .ok_or(LiftLicenseError::MissingNonDestructionWitness)?;
    validate_non_destruction_witness(non_destruction)?;
    Ok(())
}

fn validate_candidate_boundaries_and_route(
    candidate: &LiftLicenseCandidateV1,
) -> Result<(), LiftLicenseError> {
    let budget = candidate
        .budget_boundary
        .as_ref()
        .ok_or(LiftLicenseError::MissingBudgetBoundary)?;
    validate_budget_boundary(budget)?;

    let authority = candidate
        .authority_boundary
        .as_ref()
        .ok_or(LiftLicenseError::MissingAuthorityBoundary)?;
    validate_authority_boundary(authority)?;

    let terminalizer = candidate
        .terminalizer_route
        .as_ref()
        .ok_or(LiftLicenseError::MissingTerminalizerRoute)?;
    validate_terminalizer_route(terminalizer)
}

pub fn evaluate_lift_license_candidate_v1(
    trigger: &LiftTriggerV1,
    candidate: &LiftLicenseCandidateV1,
) -> Result<LiftLicenseEvaluationV1, LiftLicenseError> {
    trigger.validate()?;
    validate_candidate_fields_and_hashes(candidate)?;
    let trigger_sha256 = validate_candidate_trigger_alignment(trigger, candidate)?;
    validate_candidate_witness_bundle(trigger, candidate)?;
    validate_candidate_boundaries_and_route(candidate)?;

    Ok(LiftLicenseEvaluationV1 {
        schema_version: LIFT_license_EVALUATION_SCHEMA_VERSION.to_owned(),
        candidate_id: candidate.candidate_id.clone(),
        trigger_sha256,
        obstruction_checked: true,
        preservation_checked: true,
        non_destruction_checked: true,
        budget_checked: true,
        authority_boundary_checked: true,
        terminalizer_route_checked: true,
        scope_checked: true,
        status: LiftLicenseValidationStatusV1::AdmissibleForLicensing,
        authority_effect: AuthorityEffect::None,
    })
}

/// Bind the evidence-only license evaluation to an actual DDA carrier change.
///
/// This verifies structural transition evidence and candidate completeness. It
/// does not execute the step or issue a license.
pub fn evaluate_dda_lift_candidate_v1(
    trigger: &LiftTriggerV1,
    candidate: &LiftLicenseCandidateV1,
    step: &DdaStep,
    before: &CochainState,
    after: &CochainState,
) -> Result<DdaLiftCandidateEvaluationV1, LiftLicenseError> {
    if !step.is_executed() {
        return Err(LiftLicenseError::DdaStepNotExecuted);
    }
    if step.op != trigger.operation {
        return Err(LiftLicenseError::ScopeMismatch);
    }
    let license_evaluation = evaluate_lift_license_candidate_v1(trigger, candidate)?;
    let witness = StepWitness {
        lift_licence: license_evaluation.status
            == LiftLicenseValidationStatusV1::AdmissibleForLicensing,
        ..StepWitness::default()
    };
    let structural_evidence = verify_step_with_witness(step, before, after, Some(&witness))
        .map_err(LiftLicenseError::DdaStructuralViolation)?;
    if lift_sha256_json_v1(&before.segment)? != trigger.source_carrier_sha256
        || lift_sha256_json_v1(&after.segment)? != trigger.target_carrier_sha256
    {
        return Err(LiftLicenseError::DdaCarrierHashMismatch);
    }
    Ok(DdaLiftCandidateEvaluationV1 {
        structural_evidence,
        license_evaluation,
        authority_effect: AuthorityEffect::None,
    })
}

pub fn lift_sha256_json_v1<T: Serialize + ?Sized>(value: &T) -> Result<String, LiftLicenseError> {
    let bytes =
        serde_json::to_vec(value).map_err(|error| LiftLicenseError::Json(error.to_string()))?;
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    Ok(format!("{:x}", hasher.finalize()))
}

fn validate_obstruction_witness(
    trigger: &LiftTriggerV1,
    witness: &ObstructionWitnessV1,
) -> Result<(), LiftLicenseError> {
    require_text("obstruction.witness_id", &witness.witness_id)?;
    for (field, value) in [
        (
            "obstruction.carrier_sha256",
            witness.carrier_sha256.as_str(),
        ),
        (
            "obstruction.obstruction_sha256",
            witness.obstruction_sha256.as_str(),
        ),
        (
            "obstruction.checked_packet_sha256",
            witness.checked_packet_sha256.as_str(),
        ),
        (
            "obstruction.repair_exhaustion_sha256",
            witness.repair_exhaustion_sha256.as_str(),
        ),
    ] {
        require_sha256(field, value)?;
    }
    if witness.carrier_sha256 != trigger.source_carrier_sha256
        || witness.obstruction_sha256 != trigger.obstruction_summary_sha256
    {
        return Err(LiftLicenseError::ObstructionWitnessMismatch);
    }
    Ok(())
}

fn validate_preservation_witness(witness: &PreservationWitnessV1) -> Result<(), LiftLicenseError> {
    require_text("preservation.witness_id", &witness.witness_id)?;
    require_text("preservation.invariant_id", &witness.invariant_id)?;
    require_sha256(
        "preservation.source_invariant_sha256",
        &witness.source_invariant_sha256,
    )?;
    require_sha256(
        "preservation.target_invariant_sha256",
        &witness.target_invariant_sha256,
    )?;
    if witness.source_invariant_sha256 != witness.target_invariant_sha256 {
        return Err(LiftLicenseError::PreservationViolation);
    }
    Ok(())
}

fn validate_non_destruction_witness(
    witness: &NonDestructionWitnessV1,
) -> Result<(), LiftLicenseError> {
    require_text("non_destruction.witness_id", &witness.witness_id)?;
    require_nonempty_sorted_sha256(
        "non_destruction.source_protected_sha256",
        &witness.source_protected_sha256,
    )?;
    require_nonempty_sorted_sha256(
        "non_destruction.target_protected_sha256",
        &witness.target_protected_sha256,
    )?;
    require_sha256("non_destruction.rollback_sha256", &witness.rollback_sha256)?;
    if !witness
        .source_protected_sha256
        .iter()
        .all(|hash| witness.target_protected_sha256.binary_search(hash).is_ok())
    {
        return Err(LiftLicenseError::NonDestructionViolation);
    }
    Ok(())
}

fn validate_budget_boundary(boundary: &LiftBudgetBoundaryV1) -> Result<(), LiftLicenseError> {
    require_text("budget.witness_id", &boundary.witness_id)?;
    if boundary.max_cost_units == 0
        || boundary.requested_cost_units == 0
        || boundary.max_new_dimensions == 0
        || boundary.requested_new_dimensions == 0
        || boundary.requested_cost_units > boundary.max_cost_units
        || boundary.requested_new_dimensions > boundary.max_new_dimensions
    {
        return Err(LiftLicenseError::BudgetExceeded);
    }
    Ok(())
}

fn validate_authority_boundary(boundary: &LiftAuthorityBoundaryV1) -> Result<(), LiftLicenseError> {
    require_text("authority.witness_id", &boundary.witness_id)?;
    if boundary.promotion_performed || !boundary.authority_effect.is_none() {
        return Err(LiftLicenseError::AuthorityExpansion);
    }
    Ok(())
}

fn validate_terminalizer_route(route: &LiftTerminalizerRouteV1) -> Result<(), LiftLicenseError> {
    require_text("terminalizer.route_id", &route.route_id)?;
    require_text("terminalizer.terminalizer_id", &route.terminalizer_id)?;
    require_sha256("terminalizer.replay_sha256", &route.replay_sha256)
}

fn require_schema(
    expected: &'static str,
    found: &str,
    field: &'static str,
) -> Result<(), LiftLicenseError> {
    if found != expected {
        return Err(LiftLicenseError::SchemaMismatch {
            field,
            expected,
            found: found.to_owned(),
        });
    }
    Ok(())
}

fn require_text(field: &'static str, value: &str) -> Result<(), LiftLicenseError> {
    if value.trim().is_empty() {
        return Err(LiftLicenseError::EmptyField(field));
    }
    Ok(())
}

fn require_sha256(field: &'static str, value: &str) -> Result<(), LiftLicenseError> {
    if value.len() != 64
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(LiftLicenseError::InvalidSha256(field));
    }
    Ok(())
}

fn require_nonempty_sorted_sha256(
    field: &'static str,
    values: &[String],
) -> Result<(), LiftLicenseError> {
    if values.is_empty() {
        return Err(LiftLicenseError::EmptyList(field));
    }
    for value in values {
        require_sha256(field, value)?;
    }
    if values.windows(2).any(|pair| pair[0] >= pair[1]) {
        return Err(LiftLicenseError::NonCanonicalList(field));
    }
    Ok(())
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum LiftLicenseError {
    #[error("schema mismatch in {field}: expected {expected}, found {found}")]
    SchemaMismatch {
        field: &'static str,
        expected: &'static str,
        found: String,
    },
    #[error("required field is empty: {0}")]
    EmptyField(&'static str),
    #[error("required list is empty: {0}")]
    EmptyList(&'static str),
    #[error("list is not strictly sorted and unique: {0}")]
    NonCanonicalList(&'static str),
    #[error("invalid SHA-256 in {0}")]
    InvalidSha256(&'static str),
    #[error("DDA operation is not carrier-changing: {0:?}")]
    NotCarrierChanging(DdaOp),
    #[error("lift trigger source and target carriers are identical")]
    CarrierUnchanged,
    #[error("candidate trigger hash does not match")]
    TriggerHashMismatch,
    #[error("candidate scope does not match the trigger")]
    ScopeMismatch,
    #[error("obstruction witness is missing")]
    MissingObstructionWitness,
    #[error("obstruction witness does not bind the trigger")]
    ObstructionWitnessMismatch,
    #[error("preservation witness is missing")]
    MissingPreservationWitness,
    #[error("declared invariant was not preserved")]
    PreservationViolation,
    #[error("non-destruction witness is missing")]
    MissingNonDestructionWitness,
    #[error("protected source evidence was destroyed")]
    NonDestructionViolation,
    #[error("budget boundary is missing")]
    MissingBudgetBoundary,
    #[error("requested lift exceeds the declared budget")]
    BudgetExceeded,
    #[error("authority boundary is missing")]
    MissingAuthorityBoundary,
    #[error("candidate attempts to promote authority")]
    AuthorityExpansion,
    #[error("terminalizer route is missing")]
    MissingTerminalizerRoute,
    #[error("DDA step was refused or not executed")]
    DdaStepNotExecuted,
    #[error("DDA structural verification failed: {0:?}")]
    DdaStructuralViolation(OpViolation),
    #[error("DDA carrier hashes do not match the frozen trigger")]
    DdaCarrierHashMismatch,
    #[error("canonical JSON operation failed: {0}")]
    Json(String),
}

// Origin: vendor/engine/engine_lifts/src/lift_license.rs
// Claim: urn:omega:crates_rs:omega-lifts:lift-license:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lift_license_construction_and_fields() {
        let license = LiftLicense {
            packet_hash: [0xAB; 32],
            exhaustion_certified: true,
            witness_id: "witness_001".to_string(),
            comparison_hash: [0xCD; 32],
            rollback_hash: [0xEF; 32],
            source_level: 2,
            target_level: 3,
        };
        assert_eq!(license.packet_hash, [0xAB; 32]);
        assert!(license.exhaustion_certified);
        assert_eq!(license.witness_id, "witness_001");
        assert_eq!(license.comparison_hash, [0xCD; 32]);
        assert_eq!(license.rollback_hash, [0xEF; 32]);
        assert_eq!(license.source_level, 2);
        assert_eq!(license.target_level, 3);
    }

    #[test]
    fn test_lift_license_serde_roundtrip() {
        let license = LiftLicense {
            packet_hash: [1; 32],
            exhaustion_certified: false,
            witness_id: "w".to_string(),
            comparison_hash: [2; 32],
            rollback_hash: [3; 32],
            source_level: 0,
            target_level: 1,
        };
        let json = serde_json::to_string(&license).unwrap();
        let restored: LiftLicense = serde_json::from_str(&json).unwrap();
        assert_eq!(restored.witness_id, "w");
        assert_eq!(restored.source_level, 0);
    }

    fn sha(byte: u8) -> String {
        format!("{byte:02x}").repeat(32)
    }

    fn carrier_pair() -> (CochainState, CochainState) {
        use engine_wdp::ddc::degree_tower::{
            BinaryCochainSegment, BinaryLinearMap,
        };

        let source_d0 = BinaryLinearMap::from_rows(1, vec![vec![true], vec![false]]).unwrap();
        let source_d1 = BinaryLinearMap::from_rows(2, vec![vec![false, false]]).unwrap();
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

    fn trigger() -> LiftTriggerV1 {
        let (source, target) = carrier_pair();
        LiftTriggerV1 {
            schema_version: LIFT_TRIGGER_SCHEMA_VERSION.to_owned(),
            trigger_id: "trigger:gtoc3:fixture-lift-v1".to_owned(),
            operation: DdaOp::Lift,
            operator_id: "operator:bounded-carrier-lift-v1".to_owned(),
            operator_manifest_sha256: sha(0x22),
            source_carrier_sha256: lift_sha256_json_v1(&source.segment).unwrap(),
            target_carrier_sha256: lift_sha256_json_v1(&target.segment).unwrap(),
            obstruction_summary_sha256: sha(0x11),
            evidence_ceiling: "finite fixture carrier; evidence only".to_owned(),
            authority_effect: AuthorityEffect::None,
        }
    }

    fn candidate(trigger: &LiftTriggerV1) -> LiftLicenseCandidateV1 {
        LiftLicenseCandidateV1 {
            schema_version: LIFT_license_CANDIDATE_SCHEMA_VERSION.to_owned(),
            candidate_id: "candidate:gtoc3:fixture-lift-v1".to_owned(),
            proposed_license_id: "license:bounded-carrier-lift-v1".to_owned(),
            trigger_sha256: lift_sha256_json_v1(trigger).unwrap(),
            operation: trigger.operation,
            operator_id: trigger.operator_id.clone(),
            operator_manifest_sha256: trigger.operator_manifest_sha256.clone(),
            source_carrier_sha256: trigger.source_carrier_sha256.clone(),
            target_carrier_sha256: trigger.target_carrier_sha256.clone(),
            obstruction_witness: Some(ObstructionWitnessV1 {
                witness_id: "witness:obstruction:fixture-v1".to_owned(),
                carrier_sha256: trigger.source_carrier_sha256.clone(),
                obstruction_sha256: trigger.obstruction_summary_sha256.clone(),
                checked_packet_sha256: sha(0x33),
                repair_exhaustion_sha256: sha(0x44),
            }),
            preservation_witness: Some(PreservationWitnessV1 {
                witness_id: "witness:preservation:fixture-v1".to_owned(),
                invariant_id: "invariant:cohomology-class:fixture-v1".to_owned(),
                source_invariant_sha256: sha(0x55),
                target_invariant_sha256: sha(0x55),
            }),
            non_destruction_witness: Some(NonDestructionWitnessV1 {
                witness_id: "witness:non-destruction:fixture-v1".to_owned(),
                source_protected_sha256: vec![sha(0xa1), sha(0xb2)],
                target_protected_sha256: vec![sha(0xa1), sha(0xb2), sha(0xc3)],
                rollback_sha256: sha(0x66),
            }),
            budget_boundary: Some(LiftBudgetBoundaryV1 {
                witness_id: "witness:budget:fixture-v1".to_owned(),
                max_cost_units: 8,
                requested_cost_units: 3,
                max_new_dimensions: 2,
                requested_new_dimensions: 1,
            }),
            authority_boundary: Some(LiftAuthorityBoundaryV1 {
                witness_id: "witness:authority:none-v1".to_owned(),
                promotion_performed: false,
                authority_effect: AuthorityEffect::None,
            }),
            terminalizer_route: Some(LiftTerminalizerRouteV1 {
                route_id: "route:gtoc3:stabilized-survivor-v1".to_owned(),
                terminalizer_id: "terminalizer:fixture-replay-v1".to_owned(),
                replay_sha256: sha(0x77),
                terminal: LiftTerminalRouteV1::StabilizedSurvivor,
            }),
            constructor_set_sha256: sha(0x88),
            minimality_witness_sha256: sha(0x99),
            replay_manifest_sha256: sha(0xaa),
            evidence_ceiling: trigger.evidence_ceiling.clone(),
            authority_effect: AuthorityEffect::None,
        }
    }

    #[test]
    fn complete_candidate_is_admissible_for_licensing_but_mints_nothing() {
        let trigger = trigger();
        let evaluation =
            evaluate_lift_license_candidate_v1(&trigger, &candidate(&trigger)).unwrap();
        assert_eq!(
            evaluation.status,
            LiftLicenseValidationStatusV1::AdmissibleForLicensing
        );
        assert!(evaluation.authority_effect.is_none());
    }

    #[test]
    fn missing_witnesses_and_terminalizer_fail_closed() {
        let trigger = trigger();
        let mut proposed = candidate(&trigger);
        proposed.obstruction_witness = None;
        assert_eq!(
            evaluate_lift_license_candidate_v1(&trigger, &proposed).unwrap_err(),
            LiftLicenseError::MissingObstructionWitness
        );

        let mut proposed = candidate(&trigger);
        proposed.preservation_witness = None;
        assert_eq!(
            evaluate_lift_license_candidate_v1(&trigger, &proposed).unwrap_err(),
            LiftLicenseError::MissingPreservationWitness
        );

        let mut proposed = candidate(&trigger);
        proposed.terminalizer_route = None;
        assert_eq!(
            evaluate_lift_license_candidate_v1(&trigger, &proposed).unwrap_err(),
            LiftLicenseError::MissingTerminalizerRoute
        );
    }

    #[test]
    fn destructive_over_budget_or_authority_expanding_candidates_are_rejected() {
        let trigger = trigger();
        let mut destructive = candidate(&trigger);
        destructive
            .non_destruction_witness
            .as_mut()
            .unwrap()
            .target_protected_sha256
            .remove(0);
        assert_eq!(
            evaluate_lift_license_candidate_v1(&trigger, &destructive).unwrap_err(),
            LiftLicenseError::NonDestructionViolation
        );

        let mut over_budget = candidate(&trigger);
        over_budget
            .budget_boundary
            .as_mut()
            .unwrap()
            .requested_cost_units = 9;
        assert_eq!(
            evaluate_lift_license_candidate_v1(&trigger, &over_budget).unwrap_err(),
            LiftLicenseError::BudgetExceeded
        );

        let mut authority = candidate(&trigger);
        authority
            .authority_boundary
            .as_mut()
            .unwrap()
            .promotion_performed = true;
        assert_eq!(
            evaluate_lift_license_candidate_v1(&trigger, &authority).unwrap_err(),
            LiftLicenseError::AuthorityExpansion
        );
    }

    #[test]
    fn actual_dda_carrier_change_and_candidate_are_checked_separately() {
        let trigger = trigger();
        let candidate = candidate(&trigger);
        let (source, target) = carrier_pair();
        let step = DdaStep::executed(DdaOp::Lift, "bounded fixture carrier change");
        let evaluation =
            evaluate_dda_lift_candidate_v1(&trigger, &candidate, &step, &source, &target).unwrap();
        assert_eq!(evaluation.structural_evidence.op, DdaOp::Lift);
        assert!(evaluation.authority_effect.is_none());

        let refused = DdaStep::refused(DdaOp::Lift, "host did not issue a license");
        assert_eq!(
            evaluate_dda_lift_candidate_v1(&trigger, &candidate, &refused, &source, &target,)
                .unwrap_err(),
            LiftLicenseError::DdaStepNotExecuted
        );
    }
}
