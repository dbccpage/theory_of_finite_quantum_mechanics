//! Imported agreement schema with unresolved manuscript custody in CODA.
//! Tests of supplied observation flags are conditional protocol controls; the
//! 22 foreign paper/ledger coordinates remain OPEN_UNAVAILABLE_SOURCE.

//! S07-005 paper-by-paper agreement matrix for published papers 000-010.

#[allow(dead_code, non_camel_case_types, missing_docs)]
trait CheckedInvariantExt_e5dcf325<T> {
    fn checked_invariant_e5dcf325(self, msg: &str) -> T;
}

impl<T> CheckedInvariantExt_e5dcf325<T> for Option<T> {
    #[inline]
    fn checked_invariant_e5dcf325(self, msg: &str) -> T {
        match self {
            Some(v) => v,
            None => unreachable!("{}", msg),
        }
    }
}

impl<T, E: std::fmt::Debug> CheckedInvariantExt_e5dcf325<T> for std::result::Result<T, E> {
    #[inline]
    fn checked_invariant_e5dcf325(self, msg: &str) -> T {
        match self {
            Ok(v) => v,
            Err(e) => unreachable!("{}: {:?}", msg, e),
        }
    }
}
use engine_contracts::published_corpus::{
    PUBLISHED_SERIES_COORDINATES, PUBLISHED_SERIES_REQUIRED_ROW_ACTION,
};
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::coda_gtla_protocol::CodaTerminal;
use crate::research_program_common::{
    is_sha256, require_git_oid, require_sorted_unique, require_text, sha256_json_v1,
    ResearchProgramBoundaryV1, ResearchProgramCommonError,
};

pub const PUBLISHED_SERIES_PACKET_SCHEMA_V1: &str = "omega.published-series-agreement.packet.v1";
pub const PUBLISHED_SERIES_VERIFICATION_SCHEMA_V1: &str =
    "omega.published-series-agreement.verification.v1";

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum PaperAgreementIdV1 {
    #[serde(rename = "paper000")]
    PaperFOC000,
    #[serde(rename = "paper001")]
    PaperPO000,
    #[serde(rename = "paper002")]
    PaperGS001,
    #[serde(rename = "paper003")]
    PaperGS002,
    #[serde(rename = "paper004")]
    PaperGS003,
    #[serde(rename = "paper005")]
    PaperQF000,
    #[serde(rename = "paper006")]
    PaperFOC003,
    #[serde(rename = "paper007")]
    PaperFOC004,
    #[serde(rename = "paper008")]
    PaperFOC005,
    #[serde(rename = "paper009")]
    PaperQF001,
    #[serde(rename = "paper010")]
    PaperQF002,
}

impl PaperAgreementIdV1 {
    pub const ALL: [Self; 11] = [
        Self::PaperFOC000,
        Self::PaperPO000,
        Self::PaperGS001,
        Self::PaperGS002,
        Self::PaperGS003,
        Self::PaperQF000,
        Self::PaperFOC003,
        Self::PaperFOC004,
        Self::PaperFOC005,
        Self::PaperQF001,
        Self::PaperQF002,
    ];
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum PaperAgreementVerdictV1 {
    Agrees,
    Drifted,
    Conflicts,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PaperAgreementRowV1 {
    pub paper_id: PaperAgreementIdV1,
    pub main_path: String,
    pub main_sha256: String,
    pub claim_ledger_path: String,
    pub claim_ledger_sha256: String,
    pub claim_row_count: usize,
    pub verdict: PaperAgreementVerdictV1,
    pub action: String,
    pub declared_status_ceiling_preserved: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PublishedSeriesAgreementPacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub frozen_base: String,
    pub rows: Vec<PaperAgreementRowV1>,
    pub exact_write_surfaces: Vec<String>,
    pub boundary: ResearchProgramBoundaryV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PublishedSeriesAgreementObservationV1 {
    pub matrix_sha256: String,
    pub paper_hashes_replayed: bool,
    pub claim_ledgers_present: bool,
    pub declared_status_ceiling_scan_passed: bool,
    pub verify_markers_preserved: bool,
    pub g15_final_report_available: bool,
    pub independent_review_accepted: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PublishedSeriesAgreementVerificationV1 {
    pub schema_version: String,
    pub packet_sha256: String,
    pub matrix_sha256: String,
    pub paper_count: usize,
    pub agrees_count: usize,
    pub drifted_count: usize,
    pub conflicts_count: usize,
    pub g15_dependency_open: bool,
    pub verify_markers_preserved: bool,
    pub human_decision_recorded: bool,
    pub publication_performed: bool,
    pub promotion_constructor_called: bool,
    pub gate_activated: bool,
    pub terminal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum PublishedSeriesAgreementError {
    #[error(transparent)]
    Common(#[from] ResearchProgramCommonError),
    #[error("the canonical paper 000-010 matrix changed")]
    MatrixChanged,
    #[error("a paper or claim-ledger SHA-256 is invalid")]
    InvalidSourceHash,
    #[error("matrix observation hash mismatch")]
    ObservationHashMismatch,
    #[error("paper or claim-ledger replay failed")]
    SourceReplayFailed,
    #[error("a declared status ceiling or VERIFY marker disappeared")]
    StatusCeilingDrift,
    #[error("the unavailable G15 final report was reported present")]
    UnexpectedG15Status,
    #[error("independent evaluation was not accepted")]
    IndependentReviewMissing,
}
/// The `paper_id` token this enum variant carries in the contract corpus.
///
/// Derived from the explicitly preserved v1 wire token. Rust variant names
/// may describe the imported paper taxonomy without changing receipt identity.
fn paper_id_token(id: PaperAgreementIdV1) -> String {
    serde_json::to_value(id)
        .ok()
        .and_then(|v| v.as_str().map(str::to_owned))
        .checked_invariant_e5dcf325("PaperAgreementIdV1 serializes as a string")
}

impl PublishedSeriesAgreementPacketV1 {
    pub fn validate(&self) -> Result<(), PublishedSeriesAgreementError> {
        if self.schema_version != PUBLISHED_SERIES_PACKET_SCHEMA_V1 {
            return Err(ResearchProgramCommonError::InvalidText("schema_version").into());
        }
        require_text(&self.packet_id, "packet_id")?;
        require_git_oid(&self.frozen_base)?;
        validate_published_series_matrix_v1(&self.rows)?;
        require_sorted_unique(&self.exact_write_surfaces)?;
        self.boundary.validate()?;
        Ok(())
    }
}

pub fn validate_published_series_matrix_v1(
    rows: &[PaperAgreementRowV1],
) -> Result<(), PublishedSeriesAgreementError> {
    let coordinates = PUBLISHED_SERIES_COORDINATES;
    if rows.len() != coordinates.len() {
        return Err(PublishedSeriesAgreementError::MatrixChanged);
    }
    for (row, expected) in rows.iter().zip(coordinates.iter()) {
        if !row_coordinate_matches(row, expected) || !row_disposition_matches(row) {
            return Err(PublishedSeriesAgreementError::MatrixChanged);
        }
        if !is_sha256(&row.main_sha256) || !is_sha256(&row.claim_ledger_sha256) {
            return Err(PublishedSeriesAgreementError::InvalidSourceHash);
        }
    }
    Ok(())
}

fn row_coordinate_matches(
    row: &PaperAgreementRowV1,
    expected: &engine_contracts::published_corpus::PublishedPaperCoordinate,
) -> bool {
    paper_id_token(row.paper_id) == expected.paper_id
        && row.main_path == expected.main_path
        && row.claim_ledger_path == expected.claim_ledger_path
        && row.claim_row_count == expected.claim_row_count
}

fn row_disposition_matches(row: &PaperAgreementRowV1) -> bool {
    row.verdict == PaperAgreementVerdictV1::Agrees
        && row.action == PUBLISHED_SERIES_REQUIRED_ROW_ACTION
        && row.declared_status_ceiling_preserved
        && row.authority_effect.is_none()
}

// Origin: vendor/engine/engine_state/src/published_series_agreement.rs
// Claim: urn:omega:crates_rs:omega-state:published-series-agreement:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: no source-bound mutation campaign run for this repair; ratio=null.

#[cfg(test)]
#[path = "../../tests/engine_state/support/upstream_history.rs"]
mod historical_test_custody;

#[cfg(test)]
mod coordinate_manifest_tests {
    use super::*;
    use std::path::PathBuf;

    /// `<repo>/omega_engine/crates/engine_state` -> `<repo>`.
    fn repo_root() -> PathBuf {
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("..")
            .join("..")
            .join("..")
    }

    /// Binds this crate's enum to the contract corpus. If a paper is added to
    /// one and not the other, or the orders diverge, this fails.
    #[test]
    fn contract_covers_every_paper_id_in_order() {
        assert_eq!(
            PUBLISHED_SERIES_COORDINATES.len(),
            PaperAgreementIdV1::ALL.len(),
            "the coordinates contract must carry exactly one row per declared paper id"
        );
        // Order is load-bearing: validate_published_series_matrix_v1 zips packet
        // rows against this slice positionally.
        for (coordinate, expected_id) in PUBLISHED_SERIES_COORDINATES
            .iter()
            .zip(PaperAgreementIdV1::ALL.iter())
        {
            assert_eq!(
                coordinate.paper_id,
                paper_id_token(*expected_id),
                "contract rows must stay ascending by paper_id"
            );
        }
    }

    /// CODA has not imported the manuscripts at these foreign coordinates.
    /// Require an explicit OPEN census instead of treating synthetic matrix
    /// inputs as disk replay or inventing local publication evidence.
    #[test]
    fn every_foreign_coordinate_has_an_explicit_unavailable_source_disposition() {
        let root = repo_root();
        let mut paths = std::collections::BTreeSet::new();
        for coordinate in PUBLISHED_SERIES_COORDINATES {
            for path in [coordinate.main_path, coordinate.claim_ledger_path] {
                assert!(paths.insert(path), "coordinate aliases another source");
                let disposition = historical_test_custody::unavailable_coordinate(path)
                    .expect("every absent source needs an explicit custody disposition");
                assert_eq!(disposition.status, "OPEN_UNAVAILABLE_SOURCE");
                assert!(
                    !root.join(path).is_file(),
                    "new source bytes need custody review"
                );
            }
        }
        let declared = historical_test_custody::manifest()
            .unavailable_published_coordinates
            .iter()
            .map(|entry| entry.path.as_str())
            .collect::<std::collections::BTreeSet<_>>();
        assert_eq!(
            paths, declared,
            "the unresolved census must match the compiled coordinate contract"
        );
    }

    #[test]
    fn historical_wire_tokens_survive_rust_variant_names() {
        for (index, paper) in PaperAgreementIdV1::ALL.into_iter().enumerate() {
            let token = format!("paper{index:03}");
            assert_eq!(serde_json::to_value(paper).unwrap(), token);
            assert_eq!(
                serde_json::from_value::<PaperAgreementIdV1>(serde_json::json!(token)).unwrap(),
                paper
            );
        }
        assert!(serde_json::from_str::<PaperAgreementIdV1>("\"paper-f-o-c000\"").is_err());
    }
}

pub fn published_series_matrix_sha256_v1(
    rows: &[PaperAgreementRowV1],
) -> Result<String, PublishedSeriesAgreementError> {
    validate_published_series_matrix_v1(rows)?;
    Ok(sha256_json_v1(rows)?)
}

pub fn published_series_packet_sha256_v1(
    packet: &PublishedSeriesAgreementPacketV1,
) -> Result<String, PublishedSeriesAgreementError> {
    Ok(sha256_json_v1(packet)?)
}

pub fn verify_published_series_agreement_v1(
    packet: &PublishedSeriesAgreementPacketV1,
    observation: &PublishedSeriesAgreementObservationV1,
) -> Result<PublishedSeriesAgreementVerificationV1, PublishedSeriesAgreementError> {
    packet.validate()?;
    let matrix_sha256 = published_series_matrix_sha256_v1(&packet.rows)?;
    validate_published_series_observation(observation, &matrix_sha256)?;

    Ok(PublishedSeriesAgreementVerificationV1 {
        schema_version: PUBLISHED_SERIES_VERIFICATION_SCHEMA_V1.to_owned(),
        packet_sha256: published_series_packet_sha256_v1(packet)?,
        matrix_sha256,
        paper_count: packet.rows.len(),
        agrees_count: packet.rows.len(),
        drifted_count: 0,
        conflicts_count: 0,
        g15_dependency_open: true,
        verify_markers_preserved: true,
        human_decision_recorded: false,
        publication_performed: false,
        promotion_constructor_called: false,
        gate_activated: false,
        terminal: CodaTerminal::StabilizedSurvivor,
        authority_effect: AuthorityEffect::None,
    })
}

fn validate_published_series_observation(
    observation: &PublishedSeriesAgreementObservationV1,
    matrix_sha256: &str,
) -> Result<(), PublishedSeriesAgreementError> {
    if observation.matrix_sha256 != matrix_sha256 {
        return Err(PublishedSeriesAgreementError::ObservationHashMismatch);
    }
    if !observation.paper_hashes_replayed || !observation.claim_ledgers_present {
        return Err(PublishedSeriesAgreementError::SourceReplayFailed);
    }
    if !observation.declared_status_ceiling_scan_passed || !observation.verify_markers_preserved {
        return Err(PublishedSeriesAgreementError::StatusCeilingDrift);
    }
    if observation.g15_final_report_available {
        return Err(PublishedSeriesAgreementError::UnexpectedG15Status);
    }
    if !observation.independent_review_accepted {
        return Err(PublishedSeriesAgreementError::IndependentReviewMissing);
    }
    Ok(())
}
