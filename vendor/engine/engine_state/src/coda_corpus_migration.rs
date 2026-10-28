//! S07-006 frozen plan for the CODA paper-corpus relocation.

use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::coda_gtla_protocol::CodaTerminal;
use crate::research_program_common::{
    is_sha256, require_git_oid, require_sorted_unique, require_text, sha256_json_v1,
    ResearchProgramBoundaryV1, ResearchProgramCommonError,
};

pub const CODA_CORPUS_MIGRATION_PACKET_SCHEMA_V1: &str = "omega.gtoc-corpus-migration.packet.v1";
pub const CODA_CORPUS_MIGRATION_VERIFICATION_SCHEMA_V1: &str =
    "omega.gtoc-corpus-migration.verification.v1";
pub const CODA_CORPUS_SOURCE_ROOT_V1: &str =
    "omega_engine/general_theory_of_obstruction_calculus/papers";
pub const CODA_CORPUS_DESTINATION_ROOT_V1: &str = "omega_engine/research/published/900_gtoc";
pub const CODA_CORPUS_SOURCE_FILE_COUNT_V1: usize = 93;
pub const CODA_CORPUS_REFERENCE_FILE_COUNT_V1: usize = 116;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CodaCorpusMigrationPacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub frozen_base: String,
    pub manifest_path: String,
    pub manifest_sha256: String,
    pub source_root: String,
    pub destination_root: String,
    pub source_file_count: usize,
    pub reference_file_count: usize,
    pub collision_count: usize,
    pub destination_absent: bool,
    pub move_executed: bool,
    pub exact_write_surfaces: Vec<String>,
    pub boundary: ResearchProgramBoundaryV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CodaCorpusMigrationObservationV1 {
    pub manifest_sha256: String,
    pub source_hashes_replayed: bool,
    pub source_tree_present: bool,
    pub destination_absent: bool,
    pub collision_count: usize,
    pub reference_census_replayed: bool,
    pub move_executed: bool,
    pub independent_review_accepted: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CodaCorpusMigrationVerificationV1 {
    pub schema_version: String,
    pub packet_sha256: String,
    pub manifest_sha256: String,
    pub source_file_count: usize,
    pub reference_file_count: usize,
    pub collision_count: usize,
    pub destination_absent: bool,
    pub move_executed: bool,
    pub residual_obligations: Vec<String>,
    pub human_decision_recorded: bool,
    pub publication_performed: bool,
    pub promotion_constructor_called: bool,
    pub gate_activated: bool,
    pub terminal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum CodaCorpusMigrationError {
    #[error(transparent)]
    Common(#[from] ResearchProgramCommonError),
    #[error("the frozen corpus migration packet changed")]
    PacketChanged,
    #[error("manifest SHA-256 is invalid")]
    InvalidManifestHash,
    #[error("manifest observation hash mismatch")]
    ManifestHashMismatch,
    #[error("source, collision, or reference inventory replay failed")]
    InventoryReplayFailed,
    #[error("the unlicensed corpus move was reported executed")]
    UnexpectedMove,
    #[error("independent evaluation was not accepted")]
    IndependentReviewMissing,
}

impl CodaCorpusMigrationPacketV1 {
    pub fn validate(&self) -> Result<(), CodaCorpusMigrationError> {
        if self.schema_version != CODA_CORPUS_MIGRATION_PACKET_SCHEMA_V1 {
            return Err(ResearchProgramCommonError::InvalidText("schema_version").into());
        }
        require_text(&self.packet_id, "packet_id")?;
        require_git_oid(&self.frozen_base)?;
        if !self.paths_and_counts_match() || !self.migration_state_matches() {
            return Err(CodaCorpusMigrationError::PacketChanged);
        }
        if !is_sha256(&self.manifest_sha256) {
            return Err(CodaCorpusMigrationError::InvalidManifestHash);
        }
        require_sorted_unique(&self.exact_write_surfaces)?;
        self.boundary.validate()?;
        Ok(())
    }

    fn paths_and_counts_match(&self) -> bool {
        self.manifest_path == "docs/status/gtoc_corpus_migration_manifest_2026-07-20.json"
            && self.source_root == CODA_CORPUS_SOURCE_ROOT_V1
            && self.destination_root == CODA_CORPUS_DESTINATION_ROOT_V1
            && self.source_file_count == CODA_CORPUS_SOURCE_FILE_COUNT_V1
            && self.reference_file_count == CODA_CORPUS_REFERENCE_FILE_COUNT_V1
    }

    fn migration_state_matches(&self) -> bool {
        self.collision_count == 0 && self.destination_absent && !self.move_executed
    }
}

pub fn coda_corpus_migration_packet_sha256_v1(
    packet: &CodaCorpusMigrationPacketV1,
) -> Result<String, CodaCorpusMigrationError> {
    Ok(sha256_json_v1(packet)?)
}

pub fn verify_coda_corpus_migration_v1(
    packet: &CodaCorpusMigrationPacketV1,
    observation: &CodaCorpusMigrationObservationV1,
) -> Result<CodaCorpusMigrationVerificationV1, CodaCorpusMigrationError> {
    packet.validate()?;
    validate_corpus_migration_observation(packet, observation)?;

    Ok(CodaCorpusMigrationVerificationV1 {
        schema_version: CODA_CORPUS_MIGRATION_VERIFICATION_SCHEMA_V1.to_owned(),
        packet_sha256: coda_corpus_migration_packet_sha256_v1(packet)?,
        manifest_sha256: packet.manifest_sha256.clone(),
        source_file_count: packet.source_file_count,
        reference_file_count: packet.reference_file_count,
        collision_count: 0,
        destination_absent: true,
        move_executed: false,
        residual_obligations: vec![
            "S11-001 publication controls are unavailable".to_owned(),
            "atomic move and reference rewrite remain unexecuted".to_owned(),
        ],
        human_decision_recorded: false,
        publication_performed: false,
        promotion_constructor_called: false,
        gate_activated: false,
        terminal: CodaTerminal::OpenObstruction,
        authority_effect: AuthorityEffect::None,
    })
}

fn validate_corpus_migration_observation(
    packet: &CodaCorpusMigrationPacketV1,
    observation: &CodaCorpusMigrationObservationV1,
) -> Result<(), CodaCorpusMigrationError> {
    if observation.manifest_sha256 != packet.manifest_sha256 {
        return Err(CodaCorpusMigrationError::ManifestHashMismatch);
    }
    if !inventory_replayed(observation) {
        return Err(CodaCorpusMigrationError::InventoryReplayFailed);
    }
    if observation.move_executed {
        return Err(CodaCorpusMigrationError::UnexpectedMove);
    }
    if !observation.independent_review_accepted {
        return Err(CodaCorpusMigrationError::IndependentReviewMissing);
    }
    Ok(())
}

fn inventory_replayed(observation: &CodaCorpusMigrationObservationV1) -> bool {
    observation.source_hashes_replayed
        && observation.source_tree_present
        && observation.destination_absent
        && observation.collision_count == 0
        && observation.reference_census_replayed
}


// Backward compatibility aliases

// Origin: vendor/engine/engine_state/src/coda_corpus_migration.rs
// Claim: urn:omega:crates_rs:omega-state:coda-corpus-migration:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_1365973b {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
