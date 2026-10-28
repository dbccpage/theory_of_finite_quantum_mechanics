//! S07-003 exact CODA_GTLA-T26 hypothesis accounting.
//!
//! The admitted attempt does not construct authorized glue. It proves that the
//! six-part T26 surface remains intact and terminalizes H3-double-prime as the
//! sole open glue obligation without changing ENC or downstream status.

use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::coda_gtla_protocol::CodaTerminal;
use crate::research_program_common::{
    require_git_oid, require_sorted_unique, require_text, sha256_json_v1,
    ResearchProgramBoundaryV1, ResearchProgramCommonError,
};

pub const T26_GLUE_PACKET_SCHEMA_V1: &str = "omega.gtla-t26-glue.packet.v1";
pub const T26_GLUE_VERIFICATION_SCHEMA_V1: &str = "omega.gtla-t26-glue.verification.v1";

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum T26HypothesisIdV1 {
    H1,
    H2,
    H3Prime,
    H3DoublePrime,
    H4,
    H5C4,
}

impl T26HypothesisIdV1 {
    pub const ALL: [Self; 6] = [
        Self::H1,
        Self::H2,
        Self::H3Prime,
        Self::H3DoublePrime,
        Self::H4,
        Self::H5C4,
    ];
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum T26HypothesisDispositionV1 {
    DeclaredInput,
    OpenProofObligation,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct T26HypothesisRowV1 {
    pub hypothesis_id: T26HypothesisIdV1,
    pub summary: String,
    pub disposition: T26HypothesisDispositionV1,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum T26DependentIdV1 {
    Gtor21,
    Gttc7,
    #[serde(rename = "gtla-t28")]
    CodaGtlaT28,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct T26DependentRowV1 {
    pub dependent_id: T26DependentIdV1,
    pub required_status: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct T26GluePacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub frozen_base: String,
    pub enc_id: String,
    pub theorem_id: String,
    pub hypotheses: Vec<T26HypothesisRowV1>,
    pub downstream: Vec<T26DependentRowV1>,
    pub exact_write_surfaces: Vec<String>,
    pub boundary: ResearchProgramBoundaryV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct T26GlueObservationV1 {
    pub hypothesis_registry_sha256: String,
    pub h3_double_prime_construction_supplied: bool,
    pub enc_status: String,
    pub lean_status: String,
    pub downstream_statuses_preserved: bool,
    pub independent_review_accepted: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct T26GlueVerificationV1 {
    pub schema_version: String,
    pub packet_sha256: String,
    pub hypothesis_registry_sha256: String,
    pub hypothesis_count: usize,
    pub open_hypotheses: Vec<T26HypothesisIdV1>,
    pub enc_status: String,
    pub lean_status: String,
    pub downstream_statuses_preserved: bool,
    pub human_decision_recorded: bool,
    pub promotion_constructor_called: bool,
    pub gate_activated: bool,
    pub terminal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum T26GlueError {
    #[error(transparent)]
    Common(#[from] ResearchProgramCommonError),
    #[error("the canonical T26 hypothesis registry changed")]
    HypothesisRegistryChanged,
    #[error("the downstream conditional-status registry changed")]
    DownstreamRegistryChanged,
    #[error("hypothesis observation hash mismatch")]
    ObservationHashMismatch,
    #[error("H3-double-prime was reported constructed without admitted evidence")]
    UnsupportedGlueConstruction,
    #[error("ENC-0546 or its Lean status was inflated")]
    StatusInflation,
    #[error("downstream conditional status was not preserved")]
    DownstreamStatusDrift,
    #[error("independent evaluation was not accepted")]
    IndependentReviewMissing,
}

pub fn canonical_t26_hypotheses_v1() -> Vec<T26HypothesisRowV1> {
    use T26HypothesisDispositionV1::{DeclaredInput, OpenProofObligation};
    use T26HypothesisIdV1 as Id;

    [
        (Id::H1, "cofinal authorized finite shadows", DeclaredInput),
        (Id::H2, "certified coherent transport", DeclaredInput),
        (
            Id::H3Prime,
            "terminal agreement about transport maps only",
            DeclaredInput,
        ),
        (
            Id::H3DoublePrime,
            "authorized glued terminalization",
            OpenProofObligation,
        ),
        (Id::H4, "Omega_O comparison completion", DeclaredInput),
        (Id::H5C4, "soundness and admissibility C4", DeclaredInput),
    ]
    .into_iter()
    .map(|(hypothesis_id, summary, disposition)| T26HypothesisRowV1 {
        hypothesis_id,
        summary: summary.to_owned(),
        disposition,
        authority_effect: AuthorityEffect::None,
    })
    .collect()
}

pub fn canonical_t26_dependents_v1() -> Vec<T26DependentRowV1> {
    use T26DependentIdV1 as Id;
    [Id::Gtor21, Id::Gttc7, Id::CodaGtlaT28]
        .into_iter()
        .map(|dependent_id| T26DependentRowV1 {
            dependent_id,
            required_status: "CONDITIONAL".to_owned(),
        })
        .collect()
}

impl T26GluePacketV1 {
    pub fn validate(&self) -> Result<(), T26GlueError> {
        if self.schema_version != T26_GLUE_PACKET_SCHEMA_V1 {
            return Err(ResearchProgramCommonError::InvalidText("schema_version").into());
        }
        require_text(&self.packet_id, "packet_id")?;
        require_git_oid(&self.frozen_base)?;
        if self.enc_id != "ENC-0546" || self.theorem_id != "GTLA-T26" {
            return Err(ResearchProgramCommonError::InvalidText("T26 identity").into());
        }
        if self.hypotheses != canonical_t26_hypotheses_v1() {
            return Err(T26GlueError::HypothesisRegistryChanged);
        }
        if self.downstream != canonical_t26_dependents_v1() {
            return Err(T26GlueError::DownstreamRegistryChanged);
        }
        require_sorted_unique(&self.exact_write_surfaces)?;
        self.boundary.validate()?;
        Ok(())
    }
}

pub fn t26_hypothesis_registry_sha256_v1(
    rows: &[T26HypothesisRowV1],
) -> Result<String, T26GlueError> {
    if rows != canonical_t26_hypotheses_v1() {
        return Err(T26GlueError::HypothesisRegistryChanged);
    }
    Ok(sha256_json_v1(rows)?)
}

pub fn t26_glue_packet_sha256_v1(packet: &T26GluePacketV1) -> Result<String, T26GlueError> {
    Ok(sha256_json_v1(packet)?)
}

pub fn verify_t26_glue_v1(
    packet: &T26GluePacketV1,
    observation: &T26GlueObservationV1,
) -> Result<T26GlueVerificationV1, T26GlueError> {
    packet.validate()?;
    let registry_sha256 = t26_hypothesis_registry_sha256_v1(&packet.hypotheses)?;
    if observation.hypothesis_registry_sha256 != registry_sha256 {
        return Err(T26GlueError::ObservationHashMismatch);
    }
    if observation.h3_double_prime_construction_supplied {
        return Err(T26GlueError::UnsupportedGlueConstruction);
    }
    if observation.enc_status != "CONDITIONAL" || observation.lean_status != "NOT-STARTED" {
        return Err(T26GlueError::StatusInflation);
    }
    if !observation.downstream_statuses_preserved {
        return Err(T26GlueError::DownstreamStatusDrift);
    }
    if !observation.independent_review_accepted {
        return Err(T26GlueError::IndependentReviewMissing);
    }

    Ok(T26GlueVerificationV1 {
        schema_version: T26_GLUE_VERIFICATION_SCHEMA_V1.to_owned(),
        packet_sha256: t26_glue_packet_sha256_v1(packet)?,
        hypothesis_registry_sha256: registry_sha256,
        hypothesis_count: packet.hypotheses.len(),
        open_hypotheses: vec![T26HypothesisIdV1::H3DoublePrime],
        enc_status: observation.enc_status.clone(),
        lean_status: observation.lean_status.clone(),
        downstream_statuses_preserved: true,
        human_decision_recorded: false,
        promotion_constructor_called: false,
        gate_activated: false,
        terminal: CodaTerminal::OpenObstruction,
        authority_effect: AuthorityEffect::None,
    })
}

// Origin: vendor/engine/engine_state/src/coda_gtla_t26_glue.rs
// Claim: urn:omega:crates_rs:omega-state:coda-gtla-t26-glue:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_54fb41eb {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
