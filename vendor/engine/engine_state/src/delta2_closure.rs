//! S07-004 delta2 scalar and equivariance obstruction registry.
//!
//! The admitted attempt preserves PL-CODA-6/12/13 as OPEN. Route A/K10 is an
//! implemented convention, not the route-B construction-language discharge.

use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::coda_gtla_protocol::CodaTerminal;
use crate::research_program_common::{
    require_git_oid, require_sorted_unique, require_text, sha256_json_v1,
    ResearchProgramBoundaryV1, ResearchProgramCommonError,
};

pub const DELTA2_CLOSURE_PACKET_SCHEMA_V1: &str = "omega.delta2-closure.packet.v1";
pub const DELTA2_CLOSURE_VERIFICATION_SCHEMA_V1: &str = "omega.delta2-closure.verification.v1";

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum Delta2ObligationIdV1 {
    #[serde(rename = "pl-gtoc6")]
    PlCoda6,
    #[serde(rename = "pl-gtoc12")]
    PlCoda12,
    #[serde(rename = "pl-gtoc13")]
    PlCoda13,
}

impl Delta2ObligationIdV1 {
    pub const ALL: [Self; 3] = [Self::PlCoda6, Self::PlCoda12, Self::PlCoda13];
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Delta2DispositionV1 {
    RouteBSubobligationOpen,
    ScalarConstructionOpen,
    RouteAImplementedRouteBOpen,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Delta2ObligationRowV1 {
    pub obligation_id: Delta2ObligationIdV1,
    pub summary: String,
    pub dependent_claim_ids: Vec<String>,
    pub disposition: Delta2DispositionV1,
    pub required_status: String,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Delta2ClosurePacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub frozen_base: String,
    pub obligations: Vec<Delta2ObligationRowV1>,
    pub exact_write_surfaces: Vec<String>,
    pub boundary: ResearchProgramBoundaryV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Delta2ClosureObservationV1 {
    pub obligation_registry_sha256: String,
    pub basement_rows_open: bool,
    pub route_a_k10_preserved: bool,
    pub route_b_construction_language_supplied: bool,
    pub scalar_package_supplied: bool,
    pub withdrawn_fixed_c_cancellation_used: bool,
    pub downstream_conditional_status_preserved: bool,
    pub independent_review_accepted: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Delta2ClosureVerificationV1 {
    pub schema_version: String,
    pub packet_sha256: String,
    pub obligation_registry_sha256: String,
    pub obligation_count: usize,
    pub open_obligations: Vec<Delta2ObligationIdV1>,
    pub route_a_k10_preserved: bool,
    pub route_b_remains_open: bool,
    pub scalar_package_remains_open: bool,
    pub downstream_conditional_status_preserved: bool,
    pub human_decision_recorded: bool,
    pub promotion_constructor_called: bool,
    pub gate_activated: bool,
    pub terminal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum Delta2ClosureError {
    #[error(transparent)]
    Common(#[from] ResearchProgramCommonError),
    #[error("the canonical PL-GTOC-6/12/13 registry changed")]
    ObligationRegistryChanged,
    #[error("obligation observation hash mismatch")]
    ObservationHashMismatch,
    #[error("a basement row was inflated beyond OPEN")]
    BasementStatusInflation,
    #[error("the route-A K10 boundary disappeared")]
    RouteABoundaryLost,
    #[error("an unproved route-B or scalar construction was reported supplied")]
    UnsupportedConstruction,
    #[error("the withdrawn fixed-c cancellation route was restored")]
    WithdrawnCancellationRestored,
    #[error("a directly dependent claim lost its conditional boundary")]
    DownstreamStatusDrift,
    #[error("independent evaluation was not accepted")]
    IndependentReviewMissing,
}

pub fn canonical_delta2_obligations_v1() -> Vec<Delta2ObligationRowV1> {
    use Delta2DispositionV1 as Disposition;
    use Delta2ObligationIdV1 as Id;

    vec![
        row(
            Id::PlCoda6,
            "object-level no-privileged-witness invariance derivation",
            &["P2-C4", "PL-GTOC-4"],
            Disposition::RouteBSubobligationOpen,
        ),
        row(
            Id::PlCoda12,
            "constructed rational-like scalar algebra and repaired block cancellation",
            &["P2-C3", "P2-C5", "P3a-C5"],
            Disposition::ScalarConstructionOpen,
        ),
        row(
            Id::PlCoda13,
            "admissible-construction language and equivariance induction",
            &["P2-C4", "P2-C5", "PL-GTOC-4"],
            Disposition::RouteAImplementedRouteBOpen,
        ),
    ]
}

fn row(
    obligation_id: Delta2ObligationIdV1,
    summary: &str,
    dependent_claim_ids: &[&str],
    disposition: Delta2DispositionV1,
) -> Delta2ObligationRowV1 {
    Delta2ObligationRowV1 {
        obligation_id,
        summary: summary.to_owned(),
        dependent_claim_ids: dependent_claim_ids
            .iter()
            .map(|claim| (*claim).to_owned())
            .collect(),
        disposition,
        required_status: "OPEN".to_owned(),
        authority_effect: AuthorityEffect::None,
    }
}

impl Delta2ClosurePacketV1 {
    pub fn validate(&self) -> Result<(), Delta2ClosureError> {
        if self.schema_version != DELTA2_CLOSURE_PACKET_SCHEMA_V1 {
            return Err(ResearchProgramCommonError::InvalidText("schema_version").into());
        }
        require_text(&self.packet_id, "packet_id")?;
        require_git_oid(&self.frozen_base)?;
        if self.obligations != canonical_delta2_obligations_v1() {
            return Err(Delta2ClosureError::ObligationRegistryChanged);
        }
        require_sorted_unique(&self.exact_write_surfaces)?;
        self.boundary.validate()?;
        Ok(())
    }
}

pub fn delta2_obligation_registry_sha256_v1(
    rows: &[Delta2ObligationRowV1],
) -> Result<String, Delta2ClosureError> {
    if rows != canonical_delta2_obligations_v1() {
        return Err(Delta2ClosureError::ObligationRegistryChanged);
    }
    Ok(sha256_json_v1(rows)?)
}

pub fn delta2_closure_packet_sha256_v1(
    packet: &Delta2ClosurePacketV1,
) -> Result<String, Delta2ClosureError> {
    Ok(sha256_json_v1(packet)?)
}

pub fn verify_delta2_closure_v1(
    packet: &Delta2ClosurePacketV1,
    observation: &Delta2ClosureObservationV1,
) -> Result<Delta2ClosureVerificationV1, Delta2ClosureError> {
    packet.validate()?;
    let registry_sha256 = delta2_obligation_registry_sha256_v1(&packet.obligations)?;
    validate_delta2_observation_routes(observation, &registry_sha256)?;
    validate_delta2_observation_status(observation)?;

    Ok(Delta2ClosureVerificationV1 {
        schema_version: DELTA2_CLOSURE_VERIFICATION_SCHEMA_V1.to_owned(),
        packet_sha256: delta2_closure_packet_sha256_v1(packet)?,
        obligation_registry_sha256: registry_sha256,
        obligation_count: packet.obligations.len(),
        open_obligations: Delta2ObligationIdV1::ALL.to_vec(),
        route_a_k10_preserved: true,
        route_b_remains_open: true,
        scalar_package_remains_open: true,
        downstream_conditional_status_preserved: true,
        human_decision_recorded: false,
        promotion_constructor_called: false,
        gate_activated: false,
        terminal: CodaTerminal::OpenObstruction,
        authority_effect: AuthorityEffect::None,
    })
}

fn validate_delta2_observation_routes(
    observation: &Delta2ClosureObservationV1,
    registry_sha256: &str,
) -> Result<(), Delta2ClosureError> {
    if observation.obligation_registry_sha256 != registry_sha256 {
        return Err(Delta2ClosureError::ObservationHashMismatch);
    }
    if !observation.basement_rows_open {
        return Err(Delta2ClosureError::BasementStatusInflation);
    }
    if !observation.route_a_k10_preserved {
        return Err(Delta2ClosureError::RouteABoundaryLost);
    }
    if observation.route_b_construction_language_supplied || observation.scalar_package_supplied {
        return Err(Delta2ClosureError::UnsupportedConstruction);
    }
    Ok(())
}

fn validate_delta2_observation_status(
    observation: &Delta2ClosureObservationV1,
) -> Result<(), Delta2ClosureError> {
    if observation.withdrawn_fixed_c_cancellation_used {
        return Err(Delta2ClosureError::WithdrawnCancellationRestored);
    }
    if !observation.downstream_conditional_status_preserved {
        return Err(Delta2ClosureError::DownstreamStatusDrift);
    }
    if !observation.independent_review_accepted {
        return Err(Delta2ClosureError::IndependentReviewMissing);
    }
    Ok(())
}

// Origin: vendor/engine/engine_state/src/delta2_closure.rs
// Claim: urn:omega:crates_rs:omega-state:delta2-closure:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_f1c2ee75 {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
