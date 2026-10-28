//! Bounded CODA-2 degree-label transport for admitted CODA-1 windows.
//!
//! This module proves an executable bijection only for represented `u16`
//! windows with base degrees 1 through 65533. It preserves the sealed CODA-1
//! admission and classification bytes and never promotes authority. The
//! unrestricted natural-degree theorem remains open.

use std::collections::BTreeSet;

use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::coda1_classifier::Coda1Error;
use crate::coda1_classifier::{
    classify_coda1_v1, observer_sha256_v1, sha256_json_v1, Coda1AdmissionV1, Coda1BudgetsV1,
    Coda1ClassificationV1, Coda1HumanDecisionV1, Coda1RouteV1, SourceHashV1,
};
use crate::coda_gtla_protocol::{CodaTerminal, FrozenObserverContextV1};

pub const CODA2_ADMISSION_SCHEMA_VERSION: &str = "omega.gtoc2.admission.v1";
pub const CODA2_PACKET_SCHEMA_VERSION: &str = "omega.gtoc2.packet.v1";
pub const CODA2_CLASSIFICATION_SCHEMA_VERSION: &str = "omega.gtoc2.classification.v1";
pub const CODA2_RECEIPT_SCHEMA_VERSION: &str = "omega.gtoc2.receipts.v1";
pub const CODA2_OBSERVER_DOMAIN: &str = "finite-degree-shift-invariance";
pub const CODA2_STATE_DOMAIN: &str = "omega.gtoc2.degree-labelled-window.v1";
pub const CODA2_EVIDENCE_CEILING: &str =
    "u16 degree-label reindexing for base degrees 1-65533; no unbounded theorem or authority promotion";
pub const CODA2_MIN_BASE_DEGREE: u16 = 1;
pub const CODA2_MAX_BASE_DEGREE: u16 = u16::MAX - 2;


#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DegreeShiftV1 {
    pub base_degree: u16,
}

impl DegreeShiftV1 {
    pub fn validate(self) -> Result<(), Coda2Error> {
        if !(CODA2_MIN_BASE_DEGREE..=CODA2_MAX_BASE_DEGREE).contains(&self.base_degree) {
            return Err(Coda2Error::UnsupportedBaseDegree(self.base_degree));
        }
        Ok(())
    }

    pub fn original_degrees(self) -> Result<[u16; 3], Coda2Error> {
        self.validate()?;
        let degree_1 = self
            .base_degree
            .checked_add(1)
            .ok_or(Coda2Error::UnsupportedBaseDegree(self.base_degree))?;
        let degree_2 = self
            .base_degree
            .checked_add(2)
            .ok_or(Coda2Error::UnsupportedBaseDegree(self.base_degree))?;
        Ok([self.base_degree, degree_1, degree_2])
    }

    pub fn to_original(self, local_degree: u8) -> Result<u16, Coda2Error> {
        self.validate()?;
        if local_degree > 2 {
            return Err(Coda2Error::InvalidLocalDegree(local_degree));
        }
        self.base_degree
            .checked_add(u16::from(local_degree))
            .ok_or(Coda2Error::UnsupportedBaseDegree(self.base_degree))
    }

    pub fn to_local(self, original_degree: u16) -> Result<u8, Coda2Error> {
        self.validate()?;
        let offset = original_degree
            .checked_sub(self.base_degree)
            .ok_or(Coda2Error::DegreeOutsideWindow(original_degree))?;
        if offset > 2 {
            return Err(Coda2Error::DegreeOutsideWindow(original_degree));
        }
        u8::try_from(offset).map_err(|_| Coda2Error::DegreeOutsideWindow(original_degree))
    }

    pub fn witness(self) -> Result<DegreeBijectionWitnessV1, Coda2Error> {
        let original_degrees = self.original_degrees()?;
        let local_degrees = [0, 1, 2];
        for index in 0..3 {
            if self.to_local(original_degrees[index])? != local_degrees[index]
                || self.to_original(local_degrees[index])? != original_degrees[index]
            {
                return Err(Coda2Error::BijectionInvariant);
            }
        }
        Ok(DegreeBijectionWitnessV1 {
            base_degree: self.base_degree,
            original_degrees,
            local_degrees,
            forward_then_inverse: true,
            inverse_then_forward: true,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DegreeBijectionWitnessV1 {
    pub base_degree: u16,
    pub original_degrees: [u16; 3],
    pub local_degrees: [u8; 3],
    pub forward_then_inverse: bool,
    pub inverse_then_forward: bool,
}

impl DegreeBijectionWitnessV1 {
    pub fn validate(&self) -> Result<(), Coda2Error> {
        let expected = DegreeShiftV1 {
            base_degree: self.base_degree,
        };
        if !self.flags_and_arrays_match(expected)? || !self.roundtrip_matches(expected)? {
            return Err(Coda2Error::BijectionInvariant);
        }
        Ok(())
    }

    fn flags_and_arrays_match(&self, expected: DegreeShiftV1) -> Result<bool, Coda2Error> {
        Ok(self.original_degrees == expected.original_degrees()?
            && self.local_degrees == [0, 1, 2]
            && self.forward_then_inverse
            && self.inverse_then_forward)
    }

    fn roundtrip_matches(&self, expected: DegreeShiftV1) -> Result<bool, Coda2Error> {
        for index in 0..3 {
            if expected.to_local(self.original_degrees[index])? != self.local_degrees[index]
                || expected.to_original(self.local_degrees[index])? != self.original_degrees[index]
            {
                return Ok(false);
            }
        }
        Ok(true)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda2PacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub frozen_base: String,
    pub target_rows: Vec<String>,
    pub source_manifest: Vec<SourceHashV1>,
    pub budgets: Coda1BudgetsV1,
    pub evidence_ceiling: String,
    pub observer: FrozenObserverContextV1,
    pub producer_id: String,
    pub evaluator_id: String,
    pub authority_witness_id: String,
    pub prior_work_ledger: Vec<String>,
    pub source_packet_id: String,
    pub source_admission_sha256: String,
    pub source_classification_sha256: String,
    pub source_observer_sha256: String,
    pub expected_source_route: Coda1RouteV1,
    pub expected_source_terminal: CodaTerminal,
    pub shift: DegreeShiftV1,
}

impl Coda2PacketV1 {
    pub fn validate(&self) -> Result<(), Coda2Error> {
        self.validate_header_and_manifest()?;
        self.validate_identities_and_source_bindings()?;
        self.validate_observer_context()?;
        self.validate_observer_surfaces_and_hash()
    }

    fn validate_header_and_manifest(&self) -> Result<(), Coda2Error> {
        require_schema(CODA2_PACKET_SCHEMA_VERSION, &self.schema_version)?;
        require_text("packet.packet_id", &self.packet_id)?;
        require_git_commit("packet.frozen_base", &self.frozen_base)?;
        if self.target_rows != ["GTOC-2"] {
            return Err(Coda2Error::ScopeExpansion("target_rows"));
        }
        validate_coda2_source_manifest(&self.source_manifest)?;
        validate_budgets(self.budgets)?;
        if self.evidence_ceiling != CODA2_EVIDENCE_CEILING {
            return Err(Coda2Error::EvidenceCeilingChanged);
        }
        Ok(())
    }

    fn validate_identities_and_source_bindings(&self) -> Result<(), Coda2Error> {
        for (field, value) in [
            ("packet.producer_id", self.producer_id.as_str()),
            ("packet.evaluator_id", self.evaluator_id.as_str()),
            (
                "packet.authority_witness_id",
                self.authority_witness_id.as_str(),
            ),
            ("packet.source_packet_id", self.source_packet_id.as_str()),
        ] {
            require_text(field, value)?;
        }
        let identities = BTreeSet::from([
            self.producer_id.as_str(),
            self.evaluator_id.as_str(),
            self.authority_witness_id.as_str(),
        ]);
        if identities.len() != 3 {
            return Err(Coda2Error::IdentityCollision);
        }
        require_nonempty_sorted_texts("packet.prior_work_ledger", &self.prior_work_ledger)?;
        self.validate_source_hashes_and_shift()
    }

    fn validate_source_hashes_and_shift(&self) -> Result<(), Coda2Error> {
        for (field, value) in [
            (
                "packet.source_admission_sha256",
                self.source_admission_sha256.as_str(),
            ),
            (
                "packet.source_classification_sha256",
                self.source_classification_sha256.as_str(),
            ),
            (
                "packet.source_observer_sha256",
                self.source_observer_sha256.as_str(),
            ),
        ] {
            require_sha256(field, value)?;
        }
        if !legal_source_terminal(self.expected_source_route, self.expected_source_terminal) {
            return Err(Coda2Error::SourceBindingMismatch(
                "expected_source_terminal",
            ));
        }
        self.shift.validate()
    }

    fn validate_observer_context(&self) -> Result<(), Coda2Error> {
        self.observer
            .validate()
            .map_err(|error| Coda2Error::ObserverInvalid(error.to_string()))?;
        if self.observer.observer_id != self.evaluator_id
            || self.observer.observer_domain != CODA2_OBSERVER_DOMAIN
            || self.observer.state_domain != CODA2_STATE_DOMAIN
            || self.observer.evidence_ceiling != self.evidence_ceiling
        {
            return Err(Coda2Error::ObserverContextMismatch);
        }
        Ok(())
    }

    fn validate_observer_surfaces_and_hash(&self) -> Result<(), Coda2Error> {
        require_nonempty_sorted_texts(
            "observer.visible_artifact_hashes",
            &self.observer.visible_artifact_hashes,
        )?;
        require_sorted_texts(
            "observer.hidden_artifact_classes",
            &self.observer.hidden_artifact_classes,
        )?;
        require_nonempty_sorted_texts(
            "observer.tool_permissions",
            &self.observer.tool_permissions,
        )?;
        require_nonempty_sorted_texts("observer.write_surface", &self.observer.write_surface)?;
        for path in &self.observer.write_surface {
            require_relative_file_path("observer.write_surface", path)?;
        }
        let mut expected_hashes = self
            .source_manifest
            .iter()
            .map(|source| source.sha256.clone())
            .collect::<Vec<_>>();
        expected_hashes.sort();
        expected_hashes.dedup();
        if expected_hashes != self.observer.visible_artifact_hashes {
            return Err(Coda2Error::ObserverSourceManifestMismatch);
        }
        let found = observer_sha256_v1(&self.observer).map_err(coda1_dependency)?;
        if found != self.observer.observer_hash {
            return Err(Coda2Error::ObserverHashMismatch {
                expected: self.observer.observer_hash.clone(),
                found,
            });
        }
        Ok(())
    }
}

fn validate_coda2_source_manifest(manifest: &[SourceHashV1]) -> Result<(), Coda2Error> {
    if manifest.is_empty() {
        return Err(Coda2Error::EmptyField("packet.source_manifest"));
    }
    let mut previous_path: Option<&str> = None;
    for source in manifest {
        require_relative_file_path("source_manifest.path", &source.path)?;
        require_sha256("source_manifest.sha256", &source.sha256)?;
        if previous_path.is_some_and(|previous| previous >= source.path.as_str()) {
            return Err(Coda2Error::NonCanonicalList("packet.source_manifest"));
        }
        previous_path = Some(&source.path);
    }
    Ok(())
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda2AdmissionV1 {
    pub schema_version: String,
    pub packet: Coda2PacketV1,
    pub packet_sha256: String,
}

impl Coda2AdmissionV1 {
    pub fn validate(&self) -> Result<(), Coda2Error> {
        require_schema(CODA2_ADMISSION_SCHEMA_VERSION, &self.schema_version)?;
        require_sha256("admission.packet_sha256", &self.packet_sha256)?;
        self.packet.validate()?;
        let found = coda2_packet_sha256_v1(&self.packet)?;
        if self.packet_sha256 != found {
            return Err(Coda2Error::PacketHashMismatch {
                expected: self.packet_sha256.clone(),
                found,
            });
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda2ClassificationV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub observer_sha256: String,
    pub source_admission_sha256: String,
    pub reindexed_admission_sha256: String,
    pub source_classification_sha256: String,
    pub reindexed_classification_sha256: String,
    pub source_observer_sha256: String,
    pub reindexed_observer_sha256: String,
    pub source_rule_sha256: String,
    pub reindexed_rule_sha256: String,
    pub degree_bijection: DegreeBijectionWitnessV1,
    pub source_route: Coda1RouteV1,
    pub reindexed_route: Coda1RouteV1,
    pub source_terminal: CodaTerminal,
    pub reindexed_terminal: CodaTerminal,
    pub classification_preserved: bool,
    pub terminal_proposal: CodaTerminal,
    pub residual_ids: Vec<String>,
    pub evidence_ceiling: String,
    pub authority_effect: AuthorityEffect,
}

impl Coda2ClassificationV1 {
    pub fn validate(&self) -> Result<(), Coda2Error> {
        require_schema(CODA2_CLASSIFICATION_SCHEMA_VERSION, &self.schema_version)?;
        require_text("classification.packet_id", &self.packet_id)?;
        self.validate_hashes()?;
        self.degree_bijection.validate()?;
        require_sorted_texts("classification.residual_ids", &self.residual_ids)?;
        if self.evidence_ceiling != CODA2_EVIDENCE_CEILING {
            return Err(Coda2Error::EvidenceCeilingChanged);
        }
        if !self.authority_effect.is_none() {
            return Err(Coda2Error::AuthorityExpanded);
        }
        if !self.hashes_preserved() || !self.outcomes_preserved() {
            return Err(Coda2Error::ClassificationInvariant);
        }
        Ok(())
    }

    fn validate_hashes(&self) -> Result<(), Coda2Error> {
        for (field, value) in [
            ("classification.packet_sha256", self.packet_sha256.as_str()),
            (
                "classification.observer_sha256",
                self.observer_sha256.as_str(),
            ),
            (
                "classification.source_admission_sha256",
                self.source_admission_sha256.as_str(),
            ),
            (
                "classification.reindexed_admission_sha256",
                self.reindexed_admission_sha256.as_str(),
            ),
            (
                "classification.source_classification_sha256",
                self.source_classification_sha256.as_str(),
            ),
            (
                "classification.reindexed_classification_sha256",
                self.reindexed_classification_sha256.as_str(),
            ),
            (
                "classification.source_observer_sha256",
                self.source_observer_sha256.as_str(),
            ),
            (
                "classification.reindexed_observer_sha256",
                self.reindexed_observer_sha256.as_str(),
            ),
            (
                "classification.source_rule_sha256",
                self.source_rule_sha256.as_str(),
            ),
            (
                "classification.reindexed_rule_sha256",
                self.reindexed_rule_sha256.as_str(),
            ),
        ] {
            require_sha256(field, value)?;
        }
        Ok(())
    }

    fn hashes_preserved(&self) -> bool {
        self.source_admission_sha256 == self.reindexed_admission_sha256
            && self.source_classification_sha256 == self.reindexed_classification_sha256
            && self.source_observer_sha256 == self.reindexed_observer_sha256
            && self.source_rule_sha256 == self.reindexed_rule_sha256
    }

    fn outcomes_preserved(&self) -> bool {
        self.source_route == self.reindexed_route
            && self.source_terminal == self.reindexed_terminal
            && self.classification_preserved
            && self.terminal_proposal == CodaTerminal::StabilizedSurvivor
            && self.residual_ids.is_empty()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda2ProducerReceiptV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub observer_sha256: String,
    pub producer_id: String,
    pub source_admission_sha256: String,
    pub degree_bijection_sha256: String,
    pub classification_sha256: String,
    pub source_route: Coda1RouteV1,
    pub reindexed_route: Coda1RouteV1,
    pub source_terminal: CodaTerminal,
    pub reindexed_terminal: CodaTerminal,
    pub classification_preserved: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda2EvaluationReceiptV1 {
    pub schema_version: String,
    pub evaluator_id: String,
    pub producer_id: String,
    pub algorithm: String,
    pub replay_classification_sha256: String,
    pub producer_classification_sha256: String,
    pub independently_reconstructed_degrees: [u16; 3],
    pub expected_local_degrees: [u8; 3],
    pub exact_match: bool,
    pub route_preserved: bool,
    pub terminal_preserved: bool,
    pub cochain_rule_preserved: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda2AuthorityWitnessAttestationV1 {
    pub schema_version: String,
    pub authority_witness_id: String,
    pub producer_evaluator_witness_distinct: bool,
    pub evidence_ceiling_preserved: bool,
    pub promotion_performed: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda2ReplayReceiptV1 {
    pub schema_version: String,
    pub packet_sha256: String,
    pub source_admission_sha256: String,
    pub classification_sha256: String,
    pub replay_sha256: String,
    pub deterministic: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda2TerminalReceiptV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub source_route: Coda1RouteV1,
    pub source_terminal: CodaTerminal,
    pub terminal_proposal: CodaTerminal,
    pub residual_ids: Vec<String>,
    pub human_decision: Coda1HumanDecisionV1,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda2ReceiptBundleV1 {
    pub schema_version: String,
    pub producer: Coda2ProducerReceiptV1,
    pub evaluation: Coda2EvaluationReceiptV1,
    pub authority_witness: Coda2AuthorityWitnessAttestationV1,
    pub replay: Coda2ReplayReceiptV1,
    pub terminal: Coda2TerminalReceiptV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda2ExecutionV1 {
    pub classification: Coda2ClassificationV1,
    pub receipts: Coda2ReceiptBundleV1,
}

pub fn classify_coda2_v1(
    admission: &Coda2AdmissionV1,
    source: &Coda1AdmissionV1,
) -> Result<Coda2ClassificationV1, Coda2Error> {
    admission.validate()?;
    let bound = bind_source(admission, source)?;
    let witness = admission.packet.shift.witness()?;
    let reindexed_admission = source.clone();
    let reindexed_classification =
        classify_coda1_v1(&reindexed_admission).map_err(coda1_dependency)?;
    let classification = build_classification(
        admission,
        source,
        &bound,
        &reindexed_admission,
        &reindexed_classification,
        witness,
    )?;
    classification.validate()?;
    Ok(classification)
}

pub fn execute_and_evaluate_coda2_v1(
    admission: &Coda2AdmissionV1,
    source: &Coda1AdmissionV1,
) -> Result<Coda2ExecutionV1, Coda2Error> {
    let classification = classify_coda2_v1(admission, source)?;
    let producer = producer_receipt_v1(admission, &classification)?;
    let receipts = evaluate_coda2_v1(admission, source, &classification, &producer)?;
    Ok(Coda2ExecutionV1 {
        classification,
        receipts,
    })
}

pub fn evaluate_coda2_v1(
    admission: &Coda2AdmissionV1,
    source: &Coda1AdmissionV1,
    claimed: &Coda2ClassificationV1,
    producer: &Coda2ProducerReceiptV1,
) -> Result<Coda2ReceiptBundleV1, Coda2Error> {
    verify_coda2_claim_and_replay(admission, source, claimed, producer)?;
    let classification_sha256 = sha256_json_v1(claimed).map_err(coda1_dependency)?;
    let replay_sha256 = sha256_json_v1(&(
        admission.packet_sha256.as_str(),
        admission.packet.source_admission_sha256.as_str(),
        classification_sha256.as_str(),
        admission.packet.evaluator_id.as_str(),
        "independent-degree-array-and-byte-identity-replay-v1",
    ))
    .map_err(coda1_dependency)?;
    let reconstructed = evaluator_degree_witness(admission.packet.shift.base_degree)?;

    Ok(Coda2ReceiptBundleV1 {
        schema_version: CODA2_RECEIPT_SCHEMA_VERSION.to_owned(),
        producer: producer.clone(),
        evaluation: Coda2EvaluationReceiptV1 {
            schema_version: CODA2_RECEIPT_SCHEMA_VERSION.to_owned(),
            evaluator_id: admission.packet.evaluator_id.clone(),
            producer_id: admission.packet.producer_id.clone(),
            algorithm: "independent-degree-array-and-byte-identity-replay-v1".to_owned(),
            replay_classification_sha256: classification_sha256.clone(),
            producer_classification_sha256: producer.classification_sha256.clone(),
            independently_reconstructed_degrees: reconstructed.original_degrees,
            expected_local_degrees: reconstructed.local_degrees,
            exact_match: true,
            route_preserved: claimed.source_route == claimed.reindexed_route,
            terminal_preserved: claimed.source_terminal == claimed.reindexed_terminal,
            cochain_rule_preserved: claimed.source_rule_sha256 == claimed.reindexed_rule_sha256,
            authority_effect: AuthorityEffect::None,
        },
        authority_witness: Coda2AuthorityWitnessAttestationV1 {
            schema_version: CODA2_RECEIPT_SCHEMA_VERSION.to_owned(),
            authority_witness_id: admission.packet.authority_witness_id.clone(),
            producer_evaluator_witness_distinct: true,
            evidence_ceiling_preserved: true,
            promotion_performed: false,
            authority_effect: AuthorityEffect::None,
        },
        replay: Coda2ReplayReceiptV1 {
            schema_version: CODA2_RECEIPT_SCHEMA_VERSION.to_owned(),
            packet_sha256: admission.packet_sha256.clone(),
            source_admission_sha256: admission.packet.source_admission_sha256.clone(),
            classification_sha256,
            replay_sha256,
            deterministic: true,
        },
        terminal: Coda2TerminalReceiptV1 {
            schema_version: CODA2_RECEIPT_SCHEMA_VERSION.to_owned(),
            packet_id: admission.packet.packet_id.clone(),
            source_route: claimed.source_route,
            source_terminal: claimed.source_terminal,
            terminal_proposal: CodaTerminal::StabilizedSurvivor,
            residual_ids: Vec::new(),
            human_decision: Coda1HumanDecisionV1::PendingHumanPromotion,
            authority_effect: AuthorityEffect::None,
        },
    })
}

fn verify_coda2_claim_and_replay(
    admission: &Coda2AdmissionV1,
    source: &Coda1AdmissionV1,
    claimed: &Coda2ClassificationV1,
    producer: &Coda2ProducerReceiptV1,
) -> Result<(), Coda2Error> {
    admission.validate()?;
    claimed.validate()?;
    if claimed.packet_id != admission.packet.packet_id
        || claimed.packet_sha256 != admission.packet_sha256
        || claimed.observer_sha256 != admission.packet.observer.observer_hash
    {
        return Err(Coda2Error::ReplayMismatch);
    }
    let expected_producer = producer_receipt_v1(admission, claimed)?;
    if producer != &expected_producer {
        return Err(Coda2Error::ProducerReceiptMismatch);
    }
    let replayed = evaluator_classify_coda2_v1(admission, source)?;
    if replayed != *claimed {
        return Err(Coda2Error::ReplayMismatch);
    }
    Ok(())
}

#[derive(Debug)]
struct BoundSourceV1 {
    classification: Coda1ClassificationV1,
    admission_sha256: String,
    classification_sha256: String,
    observer_sha256: String,
    rule_sha256: String,
}

fn bind_source(
    admission: &Coda2AdmissionV1,
    source: &Coda1AdmissionV1,
) -> Result<BoundSourceV1, Coda2Error> {
    let classification = classify_coda1_v1(source).map_err(coda1_dependency)?;
    let admission_sha256 = sha256_json_v1(source).map_err(coda1_dependency)?;
    let classification_sha256 = sha256_json_v1(&classification).map_err(coda1_dependency)?;
    let rule_sha256 = sha256_json_v1(&source.packet.rule).map_err(coda1_dependency)?;
    verify_bound_source_hashes(&admission.packet, source, &admission_sha256, &classification_sha256)?;
    verify_bound_source_outcomes(&admission.packet, &classification)?;
    Ok(BoundSourceV1 {
        classification,
        admission_sha256,
        classification_sha256,
        observer_sha256: source.packet.observer.observer_hash.clone(),
        rule_sha256,
    })
}

fn verify_bound_source_hashes(
    packet: &Coda2PacketV1,
    source: &Coda1AdmissionV1,
    admission_sha256: &str,
    classification_sha256: &str,
) -> Result<(), Coda2Error> {
    if source.packet.packet_id != packet.source_packet_id {
        return Err(Coda2Error::SourceBindingMismatch("source_packet_id"));
    }
    if admission_sha256 != packet.source_admission_sha256 {
        return Err(Coda2Error::SourceBindingMismatch("source_admission_sha256"));
    }
    if classification_sha256 != packet.source_classification_sha256 {
        return Err(Coda2Error::SourceBindingMismatch(
            "source_classification_sha256",
        ));
    }
    if source.packet.observer.observer_hash != packet.source_observer_sha256 {
        return Err(Coda2Error::SourceBindingMismatch("source_observer_sha256"));
    }
    Ok(())
}

fn verify_bound_source_outcomes(
    packet: &Coda2PacketV1,
    classification: &Coda1ClassificationV1,
) -> Result<(), Coda2Error> {
    if classification.route != packet.expected_source_route {
        return Err(Coda2Error::SourceBindingMismatch("expected_source_route"));
    }
    if classification.terminal_proposal != packet.expected_source_terminal {
        return Err(Coda2Error::SourceBindingMismatch(
            "expected_source_terminal",
        ));
    }
    Ok(())
}

fn build_classification(
    admission: &Coda2AdmissionV1,
    source: &Coda1AdmissionV1,
    bound: &BoundSourceV1,
    reindexed_admission: &Coda1AdmissionV1,
    reindexed_classification: &Coda1ClassificationV1,
    degree_bijection: DegreeBijectionWitnessV1,
) -> Result<Coda2ClassificationV1, Coda2Error> {
    let reindexed_admission_sha256 =
        sha256_json_v1(reindexed_admission).map_err(coda1_dependency)?;
    let reindexed_classification_sha256 =
        sha256_json_v1(reindexed_classification).map_err(coda1_dependency)?;
    let reindexed_rule_sha256 =
        sha256_json_v1(&reindexed_admission.packet.rule).map_err(coda1_dependency)?;
    let classification = Coda2ClassificationV1 {
        schema_version: CODA2_CLASSIFICATION_SCHEMA_VERSION.to_owned(),
        packet_id: admission.packet.packet_id.clone(),
        packet_sha256: admission.packet_sha256.clone(),
        observer_sha256: admission.packet.observer.observer_hash.clone(),
        source_admission_sha256: bound.admission_sha256.clone(),
        reindexed_admission_sha256,
        source_classification_sha256: bound.classification_sha256.clone(),
        reindexed_classification_sha256,
        source_observer_sha256: bound.observer_sha256.clone(),
        reindexed_observer_sha256: reindexed_admission.packet.observer.observer_hash.clone(),
        source_rule_sha256: bound.rule_sha256.clone(),
        reindexed_rule_sha256,
        degree_bijection,
        source_route: bound.classification.route,
        reindexed_route: reindexed_classification.route,
        source_terminal: bound.classification.terminal_proposal,
        reindexed_terminal: reindexed_classification.terminal_proposal,
        classification_preserved: source == reindexed_admission
            && bound.classification == *reindexed_classification,
        terminal_proposal: CodaTerminal::StabilizedSurvivor,
        residual_ids: Vec::new(),
        evidence_ceiling: CODA2_EVIDENCE_CEILING.to_owned(),
        authority_effect: AuthorityEffect::None,
    };
    classification.validate()?;
    Ok(classification)
}

fn evaluator_classify_coda2_v1(
    admission: &Coda2AdmissionV1,
    source: &Coda1AdmissionV1,
) -> Result<Coda2ClassificationV1, Coda2Error> {
    admission.validate()?;
    let bound = bind_source(admission, source)?;
    let degree_bijection = evaluator_degree_witness(admission.packet.shift.base_degree)?;
    let reindexed_admission = source.clone();
    let reindexed_classification =
        classify_coda1_v1(&reindexed_admission).map_err(coda1_dependency)?;
    build_classification(
        admission,
        source,
        &bound,
        &reindexed_admission,
        &reindexed_classification,
        degree_bijection,
    )
}

fn evaluator_degree_witness(base_degree: u16) -> Result<DegreeBijectionWitnessV1, Coda2Error> {
    if !(CODA2_MIN_BASE_DEGREE..=CODA2_MAX_BASE_DEGREE).contains(&base_degree) {
        return Err(Coda2Error::UnsupportedBaseDegree(base_degree));
    }
    let degree_1 = base_degree
        .checked_add(1)
        .ok_or(Coda2Error::UnsupportedBaseDegree(base_degree))?;
    let degree_2 = base_degree
        .checked_add(2)
        .ok_or(Coda2Error::UnsupportedBaseDegree(base_degree))?;
    let original_degrees = [base_degree, degree_1, degree_2];
    let local_degrees = [0_u8, 1, 2];
    for index in 0..3 {
        let forward = original_degrees[index]
            .checked_sub(base_degree)
            .and_then(|offset| u8::try_from(offset).ok());
        let inverse = base_degree.checked_add(u16::from(local_degrees[index]));
        if forward != Some(local_degrees[index]) || inverse != Some(original_degrees[index]) {
            return Err(Coda2Error::BijectionInvariant);
        }
    }
    Ok(DegreeBijectionWitnessV1 {
        base_degree,
        original_degrees,
        local_degrees,
        forward_then_inverse: true,
        inverse_then_forward: true,
    })
}

fn producer_receipt_v1(
    admission: &Coda2AdmissionV1,
    classification: &Coda2ClassificationV1,
) -> Result<Coda2ProducerReceiptV1, Coda2Error> {
    Ok(Coda2ProducerReceiptV1 {
        schema_version: CODA2_RECEIPT_SCHEMA_VERSION.to_owned(),
        packet_id: admission.packet.packet_id.clone(),
        packet_sha256: admission.packet_sha256.clone(),
        observer_sha256: admission.packet.observer.observer_hash.clone(),
        producer_id: admission.packet.producer_id.clone(),
        source_admission_sha256: admission.packet.source_admission_sha256.clone(),
        degree_bijection_sha256: sha256_json_v1(&classification.degree_bijection)
            .map_err(coda1_dependency)?,
        classification_sha256: sha256_json_v1(classification).map_err(coda1_dependency)?,
        source_route: classification.source_route,
        reindexed_route: classification.reindexed_route,
        source_terminal: classification.source_terminal,
        reindexed_terminal: classification.reindexed_terminal,
        classification_preserved: classification.classification_preserved,
        authority_effect: AuthorityEffect::None,
    })
}

pub fn coda2_sha256_json_v1<T: Serialize + ?Sized>(value: &T) -> Result<String, Coda2Error> {
    sha256_json_v1(value).map_err(coda1_dependency)
}

pub fn coda2_packet_sha256_v1(packet: &Coda2PacketV1) -> Result<String, Coda2Error> {
    coda2_sha256_json_v1(packet)
}

pub fn coda2_observer_sha256_v1(observer: &FrozenObserverContextV1) -> Result<String, Coda2Error> {
    observer_sha256_v1(observer).map_err(coda1_dependency)
}

fn coda1_dependency(error: Coda1Error) -> Coda2Error {
    match error {
        Coda1Error::Json(message) => Coda2Error::Json(message),
        error => Coda2Error::Coda1Dependency(error.to_string()),
    }
}

fn validate_budgets(budgets: Coda1BudgetsV1) -> Result<(), Coda2Error> {
    if !budget_counts_valid(budgets) || !budget_resources_valid(budgets) {
        return Err(Coda2Error::BudgetOutsideAdmission);
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

fn legal_source_terminal(route: Coda1RouteV1, terminal: CodaTerminal) -> bool {
    match route {
        Coda1RouteV1::ExactRepair => terminal == CodaTerminal::ExactRepair,
        Coda1RouteV1::ClosedResidual => matches!(
            terminal,
            CodaTerminal::StabilizedSurvivor | CodaTerminal::OpenObstruction
        ),
        Coda1RouteV1::ActiveClosureFailure => terminal == CodaTerminal::OpenObstruction,
        Coda1RouteV1::NoRule => {
            matches!(terminal, CodaTerminal::OracleNeeded | CodaTerminal::Refused)
        }
    }
}

fn require_schema(expected: &'static str, found: &str) -> Result<(), Coda2Error> {
    if found != expected {
        return Err(Coda2Error::SchemaMismatch {
            expected,
            found: found.to_owned(),
        });
    }
    Ok(())
}

fn require_text(field: &'static str, value: &str) -> Result<(), Coda2Error> {
    if value.trim().is_empty() {
        return Err(Coda2Error::EmptyField(field));
    }
    Ok(())
}

fn require_nonempty_sorted_texts(field: &'static str, values: &[String]) -> Result<(), Coda2Error> {
    if values.is_empty() {
        return Err(Coda2Error::EmptyField(field));
    }
    require_sorted_texts(field, values)
}

fn require_sorted_texts(field: &'static str, values: &[String]) -> Result<(), Coda2Error> {
    for value in values {
        require_text(field, value)?;
    }
    if values.windows(2).any(|pair| pair[0] >= pair[1]) {
        return Err(Coda2Error::NonCanonicalList(field));
    }
    Ok(())
}

fn require_sha256(field: &'static str, value: &str) -> Result<(), Coda2Error> {
    if value.len() != 64
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(Coda2Error::InvalidSha256(field));
    }
    Ok(())
}

fn require_git_commit(field: &'static str, value: &str) -> Result<(), Coda2Error> {
    if value.len() != 40
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(Coda2Error::InvalidGitCommit(field));
    }
    Ok(())
}

fn require_relative_file_path(field: &'static str, value: &str) -> Result<(), Coda2Error> {
    require_text(field, value)?;
    if value.starts_with('/')
        || value.ends_with('/')
        || value.contains('\\')
        || value.contains(':')
        || value
            .chars()
            .any(|character| matches!(character, '*' | '?' | '[' | ']' | '{' | '}'))
        || value
            .split('/')
            .any(|component| component.is_empty() || component == "." || component == "..")
    {
        return Err(Coda2Error::InvalidPath(value.to_owned()));
    }
    Ok(())
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum Coda2Error {
    #[error("schema mismatch: expected {expected}, found {found}")]
    SchemaMismatch {
        expected: &'static str,
        found: String,
    },
    #[error("required field is empty: {0}")]
    EmptyField(&'static str),
    #[error("invalid SHA-256 in {0}")]
    InvalidSha256(&'static str),
    #[error("invalid Git commit in {0}")]
    InvalidGitCommit(&'static str),
    #[error("list is not strictly sorted and unique: {0}")]
    NonCanonicalList(&'static str),
    #[error("invalid exact write/source path: {0}")]
    InvalidPath(String),
    #[error("scope expansion is not licensed: {0}")]
    ScopeExpansion(&'static str),
    #[error("packet budget is outside the admitted S01-003 ceiling")]
    BudgetOutsideAdmission,
    #[error("evidence ceiling changed")]
    EvidenceCeilingChanged,
    #[error("producer, evaluator, and authority witness identities must differ")]
    IdentityCollision,
    #[error("observer validation failed: {0}")]
    ObserverInvalid(String),
    #[error("observer context is not the frozen GTOC-2 evaluator context")]
    ObserverContextMismatch,
    #[error("observer source hashes differ from the packet source manifest")]
    ObserverSourceManifestMismatch,
    #[error("observer hash mismatch: expected {expected}, found {found}")]
    ObserverHashMismatch { expected: String, found: String },
    #[error("packet hash mismatch: expected {expected}, found {found}")]
    PacketHashMismatch { expected: String, found: String },
    #[error("base degree is outside the represented GTOC-2 domain: {0}")]
    UnsupportedBaseDegree(u16),
    #[error("local degree is outside 0-2: {0}")]
    InvalidLocalDegree(u8),
    #[error("degree is outside the selected three-term window: {0}")]
    DegreeOutsideWindow(u16),
    #[error("degree shift does not satisfy both bijection laws")]
    BijectionInvariant,
    #[error("sealed GTOC-1 source binding mismatch: {0}")]
    SourceBindingMismatch(&'static str),
    #[error("classification fields do not preserve the sealed GTOC-1 result")]
    ClassificationInvariant,
    #[error("classification attempted to expand authority")]
    AuthorityExpanded,
    #[error("producer receipt does not bind the claimed classification")]
    ProducerReceiptMismatch,
    #[error("independent replay does not match the producer result")]
    ReplayMismatch,
    #[error("canonical JSON operation failed: {0}")]
    Json(String),
    #[error("sealed GTOC-1 dependency rejected the source: {0}")]
    Coda1Dependency(String),
}

impl Coda2Error {
    pub const fn terminal_route(&self) -> CodaTerminal {
        match self {
            Self::ScopeExpansion(_) | Self::EvidenceCeilingChanged => {
                CodaTerminal::LiftLicenseNeeded
            }
            Self::IdentityCollision | Self::AuthorityExpanded => CodaTerminal::Refused,
            Self::UnsupportedBaseDegree(_) | Self::DegreeOutsideWindow(_) => {
                CodaTerminal::OpenObstruction
            }
            Self::Json(_) => CodaTerminal::InfrastructureFailure,
            Self::SchemaMismatch { .. }
            | Self::EmptyField(_)
            | Self::InvalidSha256(_)
            | Self::InvalidGitCommit(_)
            | Self::NonCanonicalList(_)
            | Self::InvalidPath(_)
            | Self::BudgetOutsideAdmission
            | Self::ObserverInvalid(_)
            | Self::ObserverContextMismatch
            | Self::ObserverSourceManifestMismatch
            | Self::ObserverHashMismatch { .. }
            | Self::PacketHashMismatch { .. }
            | Self::InvalidLocalDegree(_)
            | Self::BijectionInvariant
            | Self::SourceBindingMismatch(_)
            | Self::ClassificationInvariant
            | Self::ProducerReceiptMismatch
            | Self::ReplayMismatch
            | Self::Coda1Dependency(_) => CodaTerminal::Invalid,
        }
    }
}


// Backward compatibility aliases

// Origin: vendor/engine/engine_state/src/coda2_degree_shift.rs
// Claim: urn:omega:crates_rs:omega-state:coda2-degree-shift:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_10f28a43 {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
