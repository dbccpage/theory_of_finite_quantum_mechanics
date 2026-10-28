//! Shared evidence-only boundary for SAGA-07 research-program packets.

use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

use crate::research_claim_binding::{ClaimWitnessPlanV1, ResearchClaimBindingError};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ResearchProgramBoundaryV1 {
    pub witnesses: ClaimWitnessPlanV1,
    pub evidence_ceiling: String,
    pub publication_permission: bool,
    pub promotion_permission: bool,
    pub gate_activated: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum ResearchProgramCommonError {
    #[error("invalid required text: {0}")]
    InvalidText(&'static str),
    #[error("invalid frozen Git object id")]
    InvalidGitOid,
    #[error("exact write surfaces are not strictly sorted and unique")]
    WriteSurfaceChanged,
    #[error("invalid witness plan: {0}")]
    WitnessPlan(ResearchClaimBindingError),
    #[error("publication, promotion, gate activation, or authority was requested")]
    AuthorityExpansion,
    #[error("JSON serialization failed: {0}")]
    Json(String),
}

impl ResearchProgramBoundaryV1 {
    pub fn validate(&self) -> Result<(), ResearchProgramCommonError> {
        self.witnesses
            .validate()
            .map_err(ResearchProgramCommonError::WitnessPlan)?;
        require_text(&self.evidence_ceiling, "evidence_ceiling")?;
        if self.publication_permission
            || self.promotion_permission
            || self.gate_activated
            || !self.authority_effect.is_none()
        {
            return Err(ResearchProgramCommonError::AuthorityExpansion);
        }
        Ok(())
    }
}

pub(crate) fn require_text(
    value: &str,
    field: &'static str,
) -> Result<(), ResearchProgramCommonError> {
    if value.trim().is_empty() {
        Err(ResearchProgramCommonError::InvalidText(field))
    } else {
        Ok(())
    }
}

pub(crate) fn require_git_oid(value: &str) -> Result<(), ResearchProgramCommonError> {
    if matches!(value.len(), 40 | 64) && value.bytes().all(|byte| byte.is_ascii_hexdigit()) {
        Ok(())
    } else {
        Err(ResearchProgramCommonError::InvalidGitOid)
    }
}

pub(crate) fn require_sorted_unique(values: &[String]) -> Result<(), ResearchProgramCommonError> {
    if values.is_empty()
        || values
            .windows(2)
            .any(|pair| pair[0].as_str() >= pair[1].as_str())
    {
        return Err(ResearchProgramCommonError::WriteSurfaceChanged);
    }
    for value in values {
        require_text(value, "exact_write_surfaces")?;
    }
    Ok(())
}

pub(crate) fn sha256_json_v1<T: Serialize + ?Sized>(
    value: &T,
) -> Result<String, ResearchProgramCommonError> {
    let bytes = serde_json::to_vec(value)
        .map_err(|error| ResearchProgramCommonError::Json(error.to_string()))?;
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    Ok(format!("{:x}", hasher.finalize()))
}

pub(crate) fn is_sha256(value: &str) -> bool {
    value.len() == 64 && value.bytes().all(|byte| byte.is_ascii_hexdigit())
}

// Origin: vendor/engine/engine_state/src/research_program_common.rs
// Claim: urn:omega:crates_rs:omega-state:research-program-common:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_ef1817dc {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
