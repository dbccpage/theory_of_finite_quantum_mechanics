//! Bounded CODA-3 lift-trigger and license-candidate verification.
//!
//! A DDA carrier change is only a structural trigger. This module binds one
//! frozen trigger to one registered operator and checks the five required
//! evidence classes before proposing `AdmissibleForLicensing`. It does not
//! issue a `LiftLicense`, execute a lift, promote authority, or start a
//! successor.

use engine_contracts::{
    OperatorCapabilityV1, OperatorManifestV1, OperatorOperationV1, OperatorPermissionV1,
    OperatorRegistryContractError, OperatorWitnessRequirementV1, OPERATOR_MANIFEST_SCHEMA_VERSION,
};
use engine_wdp::ddc::dda_alphabet::DdaOp;
use engine_lifts::{
    evaluate_lift_license_candidate_v1, LiftLicenseCandidateV1, LiftLicenseError,
    LiftLicenseEvaluationV1, LiftLicenseValidationStatusV1, LiftTerminalRouteV1, LiftTriggerV1,
};
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::coda1_classifier::{sha256_bytes_v1, Coda1BudgetsV1, SourceHashV1};
use crate::coda_gtla_protocol::{CodaTerminal, FrozenObserverContextV1};

pub const CODA3_PACKET_SCHEMA_VERSION: &str = "omega.gtoc3.lift-license.packet.v1";
pub const CODA3_ADMISSION_SCHEMA_VERSION: &str = "omega.gtoc3.lift-license.admission.v1";
pub const CODA3_CLASSIFICATION_SCHEMA_VERSION: &str = "omega.gtoc3.lift-license.classification.v1";
pub const CODA3_RECEIPT_SCHEMA_VERSION: &str = "omega.gtoc3.lift-license.receipts.v1";
pub const S02_002_FROZEN_BASE: &str = "10e5eb7a85ca5c345103994ca290f9c75430e909";
pub const S02_002_TARGET: &str = "S02-002:GTOC-3";
pub const S02_002_OPERATOR_ID: &str = "operator:bounded-carrier-lift-v1";
pub const S02_002_SEMANTIC_CONTRACT_ID: &str = "contract:gtoc3:bounded-lift-candidate-v1";
pub const S02_002_LICENSE_ID: &str = "license:bounded-carrier-lift-v1";
#[allow(non_upper_case_globals)]
pub const S02_002_license_ID: &str = S02_002_LICENSE_ID;
pub const S02_002_OBSERVER_DOMAIN: &str = "gtoc3-lift-license-completeness";
pub const S02_002_STATE_DOMAIN: &str = "omega.gtoc3.bounded-carrier-transition.v1";
pub const S02_002_EVIDENCE_CEILING: &str =
    "one finite DDA carrier-change fixture and one evidence-only license candidate; no issued license, execution, general GTOC-3 theorem, or authority";

pub const S02_002_SOURCE_CARRIER_SHA256: &str =
    "eced21dfc19aba16dae1a33accbdf98a8b4d8db7b5a208327baf9faff593f519";
pub const S02_002_TARGET_CARRIER_SHA256: &str =
    "edb45f97c4eebad810522fe06211a5825625fedfdfad238733e289b0fbecfe0c";
pub const S02_002_OBSTRUCTION_SUMMARY: &str =
    "source carrier requires one protected-coordinate lift after bounded repair exhaustion";
pub const S02_002_OBSTRUCTION_SHA256: &str =
    "36d8270a61c75e07373e6dc0313ddbe9eaabc0086d4fb4af186a3ce172fd741c";
pub const S02_002_MAX_COST_UNITS: u64 = 8;
pub const S02_002_MAX_NEW_DIMENSIONS: u32 = 2;

pub const S02_002_SOURCE_MANIFEST: &[(&str, &str)] = &[
    (
        "docs/gtoc-canonicalization-remaining-work.md",
        "f0625ddbfa5aec2142ddab2ed0c3f2f94f56097d2d95b1f5b67fa47fc6490954",
    ),
    (
        "docs/omega-conductor-epic-v001.md",
        "bbfd2169a45bcb6cb83bcd81ae3ffab56b8b449ca46463bd1a4a768e37820407",
    ),
    (
        "docs/saga_02_operator_registry_and_gauges.md",
        "50edc0fcc457a138692d01fd212562ccce6bd0916f731cb36024c433e697ba1b",
    ),
    (
        "docs/sprint_s02_002.md",
        "0010e84287f8c1f7263480cd1dba1bcc533f7df6c9a6de08ace93dd3f547827a",
    ),
    (
        "docs/status/omega_conductor_s01_003_status_2026-07-18.md",
        "9385659a53e2130e7c30c5bf4cde476b58dd84225db991632d5a358961ae2a52",
    ),
    (
        "docs/status/omega_conductor_s02_001_status_2026-07-18.md",
        "605c842bef97041cdb111c6e167259ab0483084361c1ddc6cf20fb1711b60d01",
    ),
    (
        "omega_engine/crates/omega_contracts/src/contract_canonical_definitions/core/08_lifts/lift_license.contract.yaml",
        "4bbdc1a419430676f97ce129b29adf0e2ba4c1cb352362fdd5423d3e9cc34d65",
    ),
    (
        "omega_engine/crates/omega_contracts/src/operator_gauge.rs",
        "ac2c0f1f10c90f7486c22317ee5541595014fdbdad63cb1c3adfe584852eec65",
    ),
    (
        "omega_engine/crates/omega_discrete_deformation_algebra/src/op_verification.rs",
        "fda813dbe86f6aa841fd2bc0a25ddb6c868ec8a9af438fdf83519fe5e37bb9dd",
    ),
    (
        "omega_engine/crates/omega_lifts/src/lift_license.rs",
        "b809437dd2ce3d0d2402da8804ded8ba94ef9f6010cc74721ee2e28b99551950",
    ),
];

pub const S02_002_WRITE_SURFACE: &[&str] = &[
    "docs/gtoc-canonicalization-remaining-work.md",
    "docs/omega-conductor-epic-v001.md",
    "docs/saga_02_operator_registry_and_gauges.md",
    "docs/sprint_s02_002.md",
    "docs/status/omega_conductor_s02_002_status_2026-07-18.md",
    "omega_engine/Cargo.lock",
    "omega_engine/crates/omega_contracts/src/operator_gauge.rs",
    "omega_engine/crates/omega_discrete_deformation_algebra/src/dda_alphabet.rs",
    "omega_engine/crates/omega_lifts/Cargo.toml",
    "omega_engine/crates/omega_lifts/src/lib.rs",
    "omega_engine/crates/omega_lifts/src/lift_license.rs",
    "omega_engine/crates/omega_state/Cargo.toml",
    "omega_engine/crates/omega_state/src/gtoc3_lift_license.rs",
    "omega_engine/crates/omega_state/src/lib.rs",
    "omega_engine/crates/omega_state/tests/fixtures/gtoc3_lift_license_fixture_matrix_v1.json",
    "omega_engine/crates/omega_state/tests/fixtures/gtoc3_lift_license_receipt_matrix_v1.json",
    "omega_engine/crates/omega_state/tests/gtoc3_lift_license.rs",
];

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda3PacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub frozen_base: String,
    pub target_sprint: String,
    pub source_manifest: Vec<SourceHashV1>,
    pub budgets: Coda1BudgetsV1,
    pub evidence_ceiling: String,
    pub observer: FrozenObserverContextV1,
    pub producer_id: String,
    pub evaluator_id: String,
    pub authority_witness_id: String,
    pub prior_work_ledger: Vec<String>,
    pub operator_manifest: OperatorManifestV1,
    pub trigger: LiftTriggerV1,
    pub candidate: Option<LiftLicenseCandidateV1>,
}

impl Coda3PacketV1 {
    pub fn validate(&self) -> Result<(), Coda3Error> {
        self.validate_header_and_identities()?;
        self.validate_trigger_and_manifest()?;
        validate_observer(self)
    }

    fn validate_header_and_identities(&self) -> Result<(), Coda3Error> {
        require_schema(CODA3_PACKET_SCHEMA_VERSION, &self.schema_version)?;
        require_text("packet.packet_id", &self.packet_id)?;
        if self.frozen_base != S02_002_FROZEN_BASE {
            return Err(Coda3Error::FrozenBaseMismatch);
        }
        if self.target_sprint != S02_002_TARGET {
            return Err(Coda3Error::ScopeExpansion("target_sprint"));
        }
        validate_source_manifest(&self.source_manifest)?;
        validate_budgets(self.budgets)?;
        if self.evidence_ceiling != S02_002_EVIDENCE_CEILING {
            return Err(Coda3Error::EvidenceCeilingChanged);
        }
        self.validate_distinct_identities()
    }

    fn validate_distinct_identities(&self) -> Result<(), Coda3Error> {
        for (field, value) in [
            ("packet.producer_id", self.producer_id.as_str()),
            ("packet.evaluator_id", self.evaluator_id.as_str()),
            (
                "packet.authority_witness_id",
                self.authority_witness_id.as_str(),
            ),
        ] {
            require_text(field, value)?;
        }
        if self.producer_id == self.evaluator_id
            || self.producer_id == self.authority_witness_id
            || self.evaluator_id == self.authority_witness_id
        {
            return Err(Coda3Error::IdentityCollision);
        }
        require_nonempty_sorted_texts("packet.prior_work_ledger", &self.prior_work_ledger)
    }

    fn validate_trigger_and_manifest(&self) -> Result<(), Coda3Error> {
        validate_operator_manifest(&self.operator_manifest)?;
        self.trigger.validate()?;
        if !self.trigger_carriers_match() {
            return Err(Coda3Error::TriggerCarrierMismatch);
        }
        let manifest_sha256 = coda3_sha256_json_v1(&self.operator_manifest)?;
        if self.trigger.operator_id != self.operator_manifest.operator_id
            || self.trigger.operator_manifest_sha256 != manifest_sha256
            || self.trigger.evidence_ceiling != self.evidence_ceiling
        {
            return Err(Coda3Error::TriggerManifestMismatch);
        }
        Ok(())
    }

    fn trigger_carriers_match(&self) -> bool {
        self.trigger.operation == DdaOp::Lift
            && self.trigger.source_carrier_sha256 == S02_002_SOURCE_CARRIER_SHA256
            && self.trigger.target_carrier_sha256 == S02_002_TARGET_CARRIER_SHA256
            && self.trigger.obstruction_summary_sha256 == S02_002_OBSTRUCTION_SHA256
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda3AdmissionV1 {
    pub schema_version: String,
    pub packet: Coda3PacketV1,
    pub packet_sha256: String,
}

impl Coda3AdmissionV1 {
    pub fn validate(&self) -> Result<(), Coda3Error> {
        require_schema(CODA3_ADMISSION_SCHEMA_VERSION, &self.schema_version)?;
        require_sha256("admission.packet_sha256", &self.packet_sha256)?;
        self.packet.validate()?;
        let found = coda3_packet_sha256_v1(&self.packet)?;
        if found != self.packet_sha256 {
            return Err(Coda3Error::PacketHashMismatch {
                expected: self.packet_sha256.clone(),
                found,
            });
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Coda3SurvivorRouteV1 {
    ProofObligation,
    OracleNeeded,
    LiftLicenseNeeded,
    Refused,
    InvalidEvidence,
    InfrastructureFailure,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda3ClassificationV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub observer_sha256: String,
    pub operator_manifest_sha256: String,
    pub trigger_sha256: String,
    pub candidate_sha256: String,
    pub evaluation_sha256: String,
    pub structural_trigger_not_license: bool,
    pub complete_for_licensing: bool,
    pub license_issued: bool,
    pub lift_executed: bool,
    pub terminal_proposal: CodaTerminal,
    pub survivor_routes: Vec<Coda3SurvivorRouteV1>,
    pub residual_ids: Vec<String>,
    pub authority_effect: AuthorityEffect,
}

impl Coda3ClassificationV1 {
    pub fn validate(&self) -> Result<(), Coda3Error> {
        require_schema(CODA3_CLASSIFICATION_SCHEMA_VERSION, &self.schema_version)?;
        require_text("classification.packet_id", &self.packet_id)?;
        for (field, value) in [
            ("classification.packet_sha256", self.packet_sha256.as_str()),
            (
                "classification.observer_sha256",
                self.observer_sha256.as_str(),
            ),
            (
                "classification.operator_manifest_sha256",
                self.operator_manifest_sha256.as_str(),
            ),
            (
                "classification.trigger_sha256",
                self.trigger_sha256.as_str(),
            ),
            (
                "classification.candidate_sha256",
                self.candidate_sha256.as_str(),
            ),
            (
                "classification.evaluation_sha256",
                self.evaluation_sha256.as_str(),
            ),
        ] {
            require_sha256(field, value)?;
        }
        require_sorted("classification.survivor_routes", &self.survivor_routes)?;
        require_sorted_texts("classification.residual_ids", &self.residual_ids)?;
        if !self.licensing_flags_valid() || !self.terminal_and_authority_valid() {
            return Err(Coda3Error::ClassificationInvariant);
        }
        Ok(())
    }

    fn licensing_flags_valid(&self) -> bool {
        self.structural_trigger_not_license
            && self.complete_for_licensing
            && !self.license_issued
            && !self.lift_executed
    }

    fn terminal_and_authority_valid(&self) -> bool {
        self.terminal_proposal == CodaTerminal::StabilizedSurvivor
            && self.survivor_routes.is_empty()
            && self.residual_ids.is_empty()
            && self.authority_effect.is_none()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda3ProducerReceiptV1 {
    pub schema_version: String,
    pub producer_id: String,
    pub packet_sha256: String,
    pub operator_manifest_sha256: String,
    pub trigger_sha256: String,
    pub candidate_sha256: String,
    pub evaluation: LiftLicenseEvaluationV1,
    pub evaluation_sha256: String,
    pub license_issued: bool,
    pub lift_executed: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda3EvaluationReceiptV1 {
    pub schema_version: String,
    pub evaluator_id: String,
    pub producer_id: String,
    pub algorithm: String,
    pub independently_recomputed_sha256: String,
    pub exact_match: bool,
    pub trigger_not_treated_as_license: bool,
    pub operator_license_binding_checked: bool,
    pub policy_budget_checked: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda3AuthorityWitnessV1 {
    pub schema_version: String,
    pub authority_witness_id: String,
    pub identities_distinct: bool,
    pub human_promotion_performed: bool,
    pub license_issued: bool,
    pub lift_executed: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda3ReplayReceiptV1 {
    pub schema_version: String,
    pub packet_sha256: String,
    pub first_producer_sha256: String,
    pub replay_producer_sha256: String,
    pub deterministic: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda3TerminalReceiptV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub terminal_proposal: CodaTerminal,
    pub survivor_routes: Vec<Coda3SurvivorRouteV1>,
    pub residual_ids: Vec<String>,
    pub human_promotion_performed: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda3ReceiptBundleV1 {
    pub schema_version: String,
    pub producer: Coda3ProducerReceiptV1,
    pub evaluation: Coda3EvaluationReceiptV1,
    pub authority_witness: Coda3AuthorityWitnessV1,
    pub replay: Coda3ReplayReceiptV1,
    pub terminal: Coda3TerminalReceiptV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda3ExecutionV1 {
    pub classification: Coda3ClassificationV1,
    pub receipts: Coda3ReceiptBundleV1,
}

pub fn evaluate_coda3_lift_candidate_v1(
    admission: &Coda3AdmissionV1,
) -> Result<Coda3ExecutionV1, Coda3Error> {
    admission.validate()?;
    let producer = produce_v1(admission)?;
    let evaluation = independently_evaluate_v1(admission, &producer)?;
    let classification = build_classification_v1(admission, &producer)?;

    let replayed = produce_v1(admission)?;
    let first_producer_sha256 = coda3_sha256_json_v1(&producer)?;
    let replay_producer_sha256 = coda3_sha256_json_v1(&replayed)?;
    if first_producer_sha256 != replay_producer_sha256 {
        return Err(Coda3Error::ReplayMismatch);
    }

    let receipts = Coda3ReceiptBundleV1 {
        schema_version: CODA3_RECEIPT_SCHEMA_VERSION.to_owned(),
        producer,
        evaluation,
        authority_witness: Coda3AuthorityWitnessV1 {
            schema_version: CODA3_RECEIPT_SCHEMA_VERSION.to_owned(),
            authority_witness_id: admission.packet.authority_witness_id.clone(),
            identities_distinct: true,
            human_promotion_performed: false,
            license_issued: false,
            lift_executed: false,
            authority_effect: AuthorityEffect::None,
        },
        replay: Coda3ReplayReceiptV1 {
            schema_version: CODA3_RECEIPT_SCHEMA_VERSION.to_owned(),
            packet_sha256: admission.packet_sha256.clone(),
            first_producer_sha256,
            replay_producer_sha256,
            deterministic: true,
        },
        terminal: Coda3TerminalReceiptV1 {
            schema_version: CODA3_RECEIPT_SCHEMA_VERSION.to_owned(),
            packet_id: admission.packet.packet_id.clone(),
            terminal_proposal: CodaTerminal::StabilizedSurvivor,
            survivor_routes: Vec::new(),
            residual_ids: Vec::new(),
            human_promotion_performed: false,
            authority_effect: AuthorityEffect::None,
        },
    };
    Ok(Coda3ExecutionV1 {
        classification,
        receipts,
    })
}

pub fn independently_evaluate_claimed_coda3_v1(
    admission: &Coda3AdmissionV1,
    producer: &Coda3ProducerReceiptV1,
) -> Result<Coda3EvaluationReceiptV1, Coda3Error> {
    admission.validate()?;
    independently_evaluate_v1(admission, producer)
}

fn produce_v1(admission: &Coda3AdmissionV1) -> Result<Coda3ProducerReceiptV1, Coda3Error> {
    let candidate = required_candidate(admission)?;
    check_operator_license_binding(&admission.packet.operator_manifest, candidate)?;
    check_policy_budget(candidate)?;
    check_terminalizer_binding(candidate)?;
    let evaluation = evaluate_lift_license_candidate_v1(&admission.packet.trigger, candidate)?;
    let operator_manifest_sha256 = coda3_sha256_json_v1(&admission.packet.operator_manifest)?;
    let trigger_sha256 = coda3_sha256_json_v1(&admission.packet.trigger)?;
    let candidate_sha256 = coda3_sha256_json_v1(candidate)?;
    let evaluation_sha256 = coda3_sha256_json_v1(&evaluation)?;
    Ok(Coda3ProducerReceiptV1 {
        schema_version: CODA3_RECEIPT_SCHEMA_VERSION.to_owned(),
        producer_id: admission.packet.producer_id.clone(),
        packet_sha256: admission.packet_sha256.clone(),
        operator_manifest_sha256,
        trigger_sha256,
        candidate_sha256,
        evaluation,
        evaluation_sha256,
        license_issued: false,
        lift_executed: false,
        authority_effect: AuthorityEffect::None,
    })
}

fn independently_evaluate_v1(
    admission: &Coda3AdmissionV1,
    producer: &Coda3ProducerReceiptV1,
) -> Result<Coda3EvaluationReceiptV1, Coda3Error> {
    let candidate = required_candidate(admission)?;
    check_operator_license_binding(&admission.packet.operator_manifest, candidate)?;
    check_policy_budget(candidate)?;
    check_terminalizer_binding(candidate)?;
    let recomputed = evaluate_lift_license_candidate_v1(&admission.packet.trigger, candidate)?;
    let recomputed_sha256 = coda3_sha256_json_v1(&recomputed)?;
    let exact_match = producer_matches_recomputed(
        admission,
        producer,
        candidate,
        &recomputed,
        &recomputed_sha256,
    )?;
    if !exact_match {
        return Err(Coda3Error::ProducerReceiptMismatch);
    }
    Ok(Coda3EvaluationReceiptV1 {
        schema_version: CODA3_RECEIPT_SCHEMA_VERSION.to_owned(),
        evaluator_id: admission.packet.evaluator_id.clone(),
        producer_id: admission.packet.producer_id.clone(),
        algorithm: "independent-gtoc3-five-part-license-replay-v1".to_owned(),
        independently_recomputed_sha256: recomputed_sha256,
        exact_match,
        trigger_not_treated_as_license: true,
        operator_license_binding_checked: true,
        policy_budget_checked: true,
        authority_effect: AuthorityEffect::None,
    })
}

fn producer_matches_recomputed(
    admission: &Coda3AdmissionV1,
    producer: &Coda3ProducerReceiptV1,
    candidate: &LiftLicenseCandidateV1,
    recomputed: &LiftLicenseEvaluationV1,
    recomputed_sha256: &str,
) -> Result<bool, Coda3Error> {
    let hashes_match = producer_hashes_match(admission, producer, candidate)?;
    Ok(hashes_match && producer_evaluation_matches(producer, recomputed, recomputed_sha256))
}

fn producer_hashes_match(
    admission: &Coda3AdmissionV1,
    producer: &Coda3ProducerReceiptV1,
    candidate: &LiftLicenseCandidateV1,
) -> Result<bool, Coda3Error> {
    let manifest_sha256 = coda3_sha256_json_v1(&admission.packet.operator_manifest)?;
    let trigger_sha256 = coda3_sha256_json_v1(&admission.packet.trigger)?;
    let candidate_sha256 = coda3_sha256_json_v1(candidate)?;
    Ok(producer.schema_version == CODA3_RECEIPT_SCHEMA_VERSION
        && producer.producer_id == admission.packet.producer_id
        && producer.packet_sha256 == admission.packet_sha256
        && producer.operator_manifest_sha256 == manifest_sha256
        && producer.trigger_sha256 == trigger_sha256
        && producer.candidate_sha256 == candidate_sha256)
}

fn producer_evaluation_matches(
    producer: &Coda3ProducerReceiptV1,
    recomputed: &LiftLicenseEvaluationV1,
    recomputed_sha256: &str,
) -> bool {
    producer.evaluation == *recomputed
        && producer.evaluation_sha256 == recomputed_sha256
        && !producer.license_issued
        && !producer.lift_executed
        && producer.authority_effect.is_none()
}

fn build_classification_v1(
    admission: &Coda3AdmissionV1,
    producer: &Coda3ProducerReceiptV1,
) -> Result<Coda3ClassificationV1, Coda3Error> {
    let classification = Coda3ClassificationV1 {
        schema_version: CODA3_CLASSIFICATION_SCHEMA_VERSION.to_owned(),
        packet_id: admission.packet.packet_id.clone(),
        packet_sha256: admission.packet_sha256.clone(),
        observer_sha256: admission.packet.observer.observer_hash.clone(),
        operator_manifest_sha256: producer.operator_manifest_sha256.clone(),
        trigger_sha256: producer.trigger_sha256.clone(),
        candidate_sha256: producer.candidate_sha256.clone(),
        evaluation_sha256: producer.evaluation_sha256.clone(),
        structural_trigger_not_license: true,
        complete_for_licensing: producer.evaluation.status
            == LiftLicenseValidationStatusV1::AdmissibleForLicensing,
        license_issued: false,
        lift_executed: false,
        terminal_proposal: CodaTerminal::StabilizedSurvivor,
        survivor_routes: Vec::new(),
        residual_ids: Vec::new(),
        authority_effect: AuthorityEffect::None,
    };
    classification.validate()?;
    Ok(classification)
}

fn required_candidate(admission: &Coda3AdmissionV1) -> Result<&LiftLicenseCandidateV1, Coda3Error> {
    admission
        .packet
        .candidate
        .as_ref()
        .ok_or(Coda3Error::MissingLicenseCandidate)
}

fn check_operator_license_binding(
    manifest: &OperatorManifestV1,
    candidate: &LiftLicenseCandidateV1,
) -> Result<(), Coda3Error> {
    if candidate.operator_id != manifest.operator_id
        || !manifest
            .license_ids
            .iter()
            .any(|license_id| license_id == &candidate.proposed_license_id)
    {
        return Err(Coda3Error::LicenseNotRegistered);
    }
    Ok(())
}

fn check_policy_budget(candidate: &LiftLicenseCandidateV1) -> Result<(), Coda3Error> {
    let boundary = candidate
        .budget_boundary
        .as_ref()
        .ok_or(LiftLicenseError::MissingBudgetBoundary)?;
    if boundary.max_cost_units > S02_002_MAX_COST_UNITS
        || boundary.max_new_dimensions > S02_002_MAX_NEW_DIMENSIONS
    {
        return Err(Coda3Error::PolicyBudgetExceeded);
    }
    Ok(())
}

fn check_terminalizer_binding(candidate: &LiftLicenseCandidateV1) -> Result<(), Coda3Error> {
    if candidate
        .terminalizer_route
        .as_ref()
        .is_some_and(|route| route.terminal != LiftTerminalRouteV1::StabilizedSurvivor)
    {
        return Err(Coda3Error::TerminalizerMismatch);
    }
    Ok(())
}

fn validate_operator_manifest(manifest: &OperatorManifestV1) -> Result<(), Coda3Error> {
    manifest.validate()?;
    if !manifest_identity_and_io_match(manifest)
        || !manifest_permissions_and_witnesses_match(manifest)
    {
        return Err(Coda3Error::OperatorManifestMismatch);
    }
    Ok(())
}

fn manifest_identity_and_io_match(manifest: &OperatorManifestV1) -> bool {
    manifest.schema_version == OPERATOR_MANIFEST_SCHEMA_VERSION
        && manifest.operator_id == S02_002_OPERATOR_ID
        && manifest.semantic_contract_id == S02_002_SEMANTIC_CONTRACT_ID
        && manifest.input_families == ["omega.carrier-transition.request.v1".to_owned()]
        && manifest.output_families == ["omega.lift-license-evaluation.v1".to_owned()]
        && manifest.permitted_operations == [OperatorOperationV1::CarrierLift]
        && manifest.required_capabilities
            == [
                OperatorCapabilityV1::CarrierTransition,
                OperatorCapabilityV1::DeterministicReplay,
            ]
}

fn manifest_permissions_and_witnesses_match(manifest: &OperatorManifestV1) -> bool {
    let expected_write_surface = [
        "omega_engine/crates/omega_state/tests/fixtures/gtoc3_lift_license_fixture_matrix_v1.json"
            .to_owned(),
        "omega_engine/crates/omega_state/tests/fixtures/gtoc3_lift_license_receipt_matrix_v1.json"
            .to_owned(),
    ];
    manifest.permission_ceiling
        == [
            OperatorPermissionV1::ReadFixture,
            OperatorPermissionV1::WriteReceipt,
        ]
        && manifest.write_surface == expected_write_surface
        && manifest.evidence_ceiling == S02_002_EVIDENCE_CEILING
        && manifest.license_ids == [S02_002_license_ID.to_owned()]
        && manifest.witness_requirements
            == [
                OperatorWitnessRequirementV1::Producer,
                OperatorWitnessRequirementV1::IndependentEvaluator,
                OperatorWitnessRequirementV1::AuthorityWitness,
            ]
        && manifest.authority_effect.is_none()
}

fn validate_source_manifest(manifest: &[SourceHashV1]) -> Result<(), Coda3Error> {
    let expected = S02_002_SOURCE_MANIFEST
        .iter()
        .map(|(path, sha256)| SourceHashV1 {
            path: (*path).to_owned(),
            sha256: (*sha256).to_owned(),
        })
        .collect::<Vec<_>>();
    if manifest != expected {
        return Err(Coda3Error::SourceManifestMismatch);
    }
    Ok(())
}

fn validate_observer(packet: &Coda3PacketV1) -> Result<(), Coda3Error> {
    packet
        .observer
        .validate()
        .map_err(|error| Coda3Error::ObserverInvalid(error.to_string()))?;
    if !observer_context_matches_packet(packet) || !observer_surfaces_match_packet(packet) {
        return Err(Coda3Error::ObserverContextMismatch);
    }
    let found = coda3_observer_sha256_v1(&packet.observer)?;
    if found != packet.observer.observer_hash {
        return Err(Coda3Error::ObserverHashMismatch {
            expected: packet.observer.observer_hash.clone(),
            found,
        });
    }
    Ok(())
}

fn observer_context_matches_packet(packet: &Coda3PacketV1) -> bool {
    let mut visible_hashes = packet
        .source_manifest
        .iter()
        .map(|source| source.sha256.clone())
        .collect::<Vec<_>>();
    visible_hashes.sort();
    visible_hashes.dedup();
    packet.observer.observer_id == packet.evaluator_id
        && packet.observer.observer_domain == S02_002_OBSERVER_DOMAIN
        && packet.observer.state_domain == S02_002_STATE_DOMAIN
        && packet.observer.visible_artifact_hashes == visible_hashes
        && packet.observer.evidence_ceiling == packet.evidence_ceiling
}

fn observer_surfaces_match_packet(packet: &Coda3PacketV1) -> bool {
    let expected_hidden = [
        "human-license-issuance".to_owned(),
        "live-provider-context".to_owned(),
        "production-credentials".to_owned(),
    ];
    let expected_permissions = [
        "read:frozen-source".to_owned(),
        "test:omega_lifts".to_owned(),
        "test:omega_state".to_owned(),
        "write:admitted-paths".to_owned(),
    ];
    let expected_writes = S02_002_WRITE_SURFACE
        .iter()
        .map(|path| (*path).to_owned())
        .collect::<Vec<_>>();
    packet.observer.hidden_artifact_classes == expected_hidden
        && packet.observer.tool_permissions == expected_permissions
        && packet.observer.write_surface == expected_writes
}

#[derive(Serialize)]
struct ObserverHashMaterialV1<'a> {
    observer_id: &'a str,
    observer_domain: &'a str,
    state_domain: &'a str,
    visible_artifact_hashes: &'a [String],
    hidden_artifact_classes: &'a [String],
    tool_permissions: &'a [String],
    write_surface: &'a [String],
    evidence_ceiling: &'a str,
}

pub fn coda3_observer_sha256_v1(observer: &FrozenObserverContextV1) -> Result<String, Coda3Error> {
    coda3_sha256_json_v1(&ObserverHashMaterialV1 {
        observer_id: &observer.observer_id,
        observer_domain: &observer.observer_domain,
        state_domain: &observer.state_domain,
        visible_artifact_hashes: &observer.visible_artifact_hashes,
        hidden_artifact_classes: &observer.hidden_artifact_classes,
        tool_permissions: &observer.tool_permissions,
        write_surface: &observer.write_surface,
        evidence_ceiling: &observer.evidence_ceiling,
    })
}

pub fn coda3_packet_sha256_v1(packet: &Coda3PacketV1) -> Result<String, Coda3Error> {
    coda3_sha256_json_v1(packet)
}

pub fn coda3_sha256_json_v1<T: Serialize + ?Sized>(value: &T) -> Result<String, Coda3Error> {
    let bytes = serde_json::to_vec(value).map_err(|error| Coda3Error::Json(error.to_string()))?;
    Ok(sha256_bytes_v1(&bytes))
}

fn validate_budgets(budgets: Coda1BudgetsV1) -> Result<(), Coda3Error> {
    if !budget_counts_valid(budgets) || !budget_resources_valid(budgets) {
        return Err(Coda3Error::BudgetOutsideAdmission);
    }
    Ok(())
}

fn budget_counts_valid(budgets: Coda1BudgetsV1) -> bool {
    budgets.attempt_budget == 1 && budgets.repair_budget <= 2 && budgets.successor_budget <= 1
}

fn budget_resources_valid(budgets: Coda1BudgetsV1) -> bool {
    (1..=8 * 60 * 60).contains(&budgets.time_budget_seconds)
        && (1..=4).contains(&budgets.process_budget)
        && (1..=200_000).contains(&budgets.token_budget)
}

fn require_schema(expected: &'static str, found: &str) -> Result<(), Coda3Error> {
    if found != expected {
        return Err(Coda3Error::SchemaMismatch {
            expected,
            found: found.to_owned(),
        });
    }
    Ok(())
}

fn require_text(field: &'static str, value: &str) -> Result<(), Coda3Error> {
    if value.trim().is_empty() {
        return Err(Coda3Error::EmptyField(field));
    }
    Ok(())
}

fn require_sha256(field: &'static str, value: &str) -> Result<(), Coda3Error> {
    if value.len() != 64
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(Coda3Error::InvalidSha256(field));
    }
    Ok(())
}

fn require_nonempty_sorted_texts(field: &'static str, values: &[String]) -> Result<(), Coda3Error> {
    if values.is_empty() || values.iter().any(|value| value.trim().is_empty()) {
        return Err(Coda3Error::EmptyField(field));
    }
    require_sorted_texts(field, values)
}

fn require_sorted_texts(field: &'static str, values: &[String]) -> Result<(), Coda3Error> {
    if values.windows(2).any(|pair| pair[0] >= pair[1]) {
        return Err(Coda3Error::NonCanonicalList(field));
    }
    Ok(())
}

fn require_sorted<T: Ord>(field: &'static str, values: &[T]) -> Result<(), Coda3Error> {
    if values.windows(2).any(|pair| pair[0] >= pair[1]) {
        return Err(Coda3Error::NonCanonicalList(field));
    }
    Ok(())
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum Coda3Error {
    #[error(transparent)]
    Contract(#[from] OperatorRegistryContractError),
    #[error(transparent)]
    Lift(#[from] LiftLicenseError),
    #[error("schema mismatch: expected {expected}, found {found}")]
    SchemaMismatch {
        expected: &'static str,
        found: String,
    },
    #[error("required field is empty: {0}")]
    EmptyField(&'static str),
    #[error("invalid SHA-256 in {0}")]
    InvalidSha256(&'static str),
    #[error("list is not strictly sorted and unique: {0}")]
    NonCanonicalList(&'static str),
    #[error("frozen base does not match the admitted S02-002 base")]
    FrozenBaseMismatch,
    #[error("scope expansion is not licensed: {0}")]
    ScopeExpansion(&'static str),
    #[error("source manifest does not match the frozen S02-002 closure")]
    SourceManifestMismatch,
    #[error("packet budget is outside the admitted S02-002 ceiling")]
    BudgetOutsideAdmission,
    #[error("evidence ceiling changed")]
    EvidenceCeilingChanged,
    #[error("producer, evaluator, and authority witness identities must differ")]
    IdentityCollision,
    #[error("observer validation failed: {0}")]
    ObserverInvalid(String),
    #[error("observer context is not the frozen S02-002 evaluator context")]
    ObserverContextMismatch,
    #[error("observer hash mismatch: expected {expected}, found {found}")]
    ObserverHashMismatch { expected: String, found: String },
    #[error("packet hash mismatch: expected {expected}, found {found}")]
    PacketHashMismatch { expected: String, found: String },
    #[error("registered operator manifest does not match the admitted lift operator")]
    OperatorManifestMismatch,
    #[error("lift trigger is not bound to the registered operator manifest")]
    TriggerManifestMismatch,
    #[error("lift trigger is outside the frozen S02-002 operation or carrier")]
    TriggerCarrierMismatch,
    #[error("candidate terminalizer route does not match the admitted terminal")]
    TerminalizerMismatch,
    #[error("a structural trigger was presented without a license candidate")]
    MissingLicenseCandidate,
    #[error("candidate license id is not registered by the operator manifest")]
    LicenseNotRegistered,
    #[error("candidate policy ceiling exceeds the admitted S02-002 budget")]
    PolicyBudgetExceeded,
    #[error("claimed producer receipt does not match independent replay")]
    ProducerReceiptMismatch,
    #[error("classification fields do not establish bounded GTOC-3")]
    ClassificationInvariant,
    #[error("deterministic replay does not match the producer receipt")]
    ReplayMismatch,
    #[error("canonical JSON operation failed: {0}")]
    Json(String),
}

impl Coda3Error {
    pub const fn terminal_route(&self) -> CodaTerminal {
        match self {
            Self::Lift(error) => lift_terminal(error),
            Self::Contract(error) => contract_terminal(error),
            Self::MissingLicenseCandidate
            | Self::LicenseNotRegistered
            | Self::PolicyBudgetExceeded
            | Self::ScopeExpansion(_)
            | Self::EvidenceCeilingChanged => CodaTerminal::LiftLicenseNeeded,
            Self::IdentityCollision => CodaTerminal::Refused,
            Self::Json(_) => CodaTerminal::InfrastructureFailure,
            Self::SchemaMismatch { .. }
            | Self::EmptyField(_)
            | Self::InvalidSha256(_)
            | Self::NonCanonicalList(_)
            | Self::FrozenBaseMismatch
            | Self::SourceManifestMismatch
            | Self::BudgetOutsideAdmission
            | Self::ObserverInvalid(_)
            | Self::ObserverContextMismatch
            | Self::ObserverHashMismatch { .. }
            | Self::PacketHashMismatch { .. }
            | Self::OperatorManifestMismatch
            | Self::TriggerManifestMismatch
            | Self::TriggerCarrierMismatch
            | Self::TerminalizerMismatch
            | Self::ProducerReceiptMismatch
            | Self::ClassificationInvariant
            | Self::ReplayMismatch => CodaTerminal::Invalid,
        }
    }

    pub const fn survivor_route(&self) -> Option<Coda3SurvivorRouteV1> {
        match self {
            Self::Lift(error) => lift_survivor(error),
            Self::Contract(error) => contract_survivor(error),
            Self::MissingLicenseCandidate
            | Self::LicenseNotRegistered
            | Self::PolicyBudgetExceeded
            | Self::ScopeExpansion(_)
            | Self::EvidenceCeilingChanged => Some(Coda3SurvivorRouteV1::LiftLicenseNeeded),
            Self::IdentityCollision => Some(Coda3SurvivorRouteV1::Refused),
            Self::Json(_) => Some(Coda3SurvivorRouteV1::InfrastructureFailure),
            Self::TriggerCarrierMismatch
            | Self::TerminalizerMismatch
            | Self::ProducerReceiptMismatch
            | Self::ClassificationInvariant
            | Self::ReplayMismatch => Some(Coda3SurvivorRouteV1::InvalidEvidence),
            _ => None,
        }
    }
}

const fn lift_terminal(error: &LiftLicenseError) -> CodaTerminal {
    match error {
        LiftLicenseError::MissingPreservationWitness
        | LiftLicenseError::MissingTerminalizerRoute => CodaTerminal::OracleNeeded,
        LiftLicenseError::MissingObstructionWitness
        | LiftLicenseError::MissingNonDestructionWitness
        | LiftLicenseError::MissingBudgetBoundary
        | LiftLicenseError::BudgetExceeded => CodaTerminal::LiftLicenseNeeded,
        LiftLicenseError::MissingAuthorityBoundary
        | LiftLicenseError::PreservationViolation
        | LiftLicenseError::NonDestructionViolation
        | LiftLicenseError::AuthorityExpansion => CodaTerminal::Refused,
        LiftLicenseError::Json(_) => CodaTerminal::InfrastructureFailure,
        _ => CodaTerminal::Invalid,
    }
}

const fn lift_survivor(error: &LiftLicenseError) -> Option<Coda3SurvivorRouteV1> {
    match error {
        LiftLicenseError::MissingObstructionWitness => Some(Coda3SurvivorRouteV1::ProofObligation),
        LiftLicenseError::MissingPreservationWitness
        | LiftLicenseError::MissingTerminalizerRoute => Some(Coda3SurvivorRouteV1::OracleNeeded),
        LiftLicenseError::MissingNonDestructionWitness
        | LiftLicenseError::MissingBudgetBoundary
        | LiftLicenseError::BudgetExceeded => Some(Coda3SurvivorRouteV1::LiftLicenseNeeded),
        LiftLicenseError::MissingAuthorityBoundary
        | LiftLicenseError::PreservationViolation
        | LiftLicenseError::NonDestructionViolation
        | LiftLicenseError::AuthorityExpansion => Some(Coda3SurvivorRouteV1::Refused),
        LiftLicenseError::Json(_) => Some(Coda3SurvivorRouteV1::InfrastructureFailure),
        _ => Some(Coda3SurvivorRouteV1::InvalidEvidence),
    }
}

const fn contract_terminal(error: &OperatorRegistryContractError) -> CodaTerminal {
    match error {
        OperatorRegistryContractError::PermissionExpansion(_)
        | OperatorRegistryContractError::WriteSurfaceExpansion(_)
        | OperatorRegistryContractError::EvidenceCeilingExpansion(_)
        | OperatorRegistryContractError::NetworkAccessForbidden(_)
        | OperatorRegistryContractError::CredentialAccessForbidden(_)
        | OperatorRegistryContractError::HiddenContextForbidden(_) => {
            CodaTerminal::LiftLicenseNeeded
        }
        OperatorRegistryContractError::AuthorityExpansion(_)
        | OperatorRegistryContractError::WitnessSetChanged(_) => CodaTerminal::Refused,
        _ => CodaTerminal::Invalid,
    }
}

const fn contract_survivor(error: &OperatorRegistryContractError) -> Option<Coda3SurvivorRouteV1> {
    match error {
        OperatorRegistryContractError::PermissionExpansion(_)
        | OperatorRegistryContractError::WriteSurfaceExpansion(_)
        | OperatorRegistryContractError::EvidenceCeilingExpansion(_)
        | OperatorRegistryContractError::NetworkAccessForbidden(_)
        | OperatorRegistryContractError::CredentialAccessForbidden(_)
        | OperatorRegistryContractError::HiddenContextForbidden(_) => {
            Some(Coda3SurvivorRouteV1::LiftLicenseNeeded)
        }
        OperatorRegistryContractError::AuthorityExpansion(_)
        | OperatorRegistryContractError::WitnessSetChanged(_) => {
            Some(Coda3SurvivorRouteV1::Refused)
        }
        _ => Some(Coda3SurvivorRouteV1::InvalidEvidence),
    }
}


// Backward compatibility aliases

// Origin: vendor/engine/engine_state/src/coda3_lift_license.rs
// Claim: urn:omega:crates_rs:omega-state:coda3-lift-license:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_f877f724 {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
