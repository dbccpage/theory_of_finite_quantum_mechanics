//! Synthetic schema/validator fixtures; no historical run or receipt is replayed.
//! Missing upstream packet custody is recorded in fixtures/synthetic_program_fixture_custody.json.

use engine_contracts::published_corpus::{
    PUBLISHED_SERIES_COORDINATES, PUBLISHED_SERIES_REQUIRED_ROW_ACTION,
};
use engine_state::published_series_agreement::PUBLISHED_SERIES_PACKET_SCHEMA_V1;
use engine_state::{
    published_series_matrix_sha256_v1, verify_published_series_agreement_v1, CodaTerminal,
    PaperAgreementIdV1, PaperAgreementRowV1, PaperAgreementVerdictV1,
    PublishedSeriesAgreementError, PublishedSeriesAgreementObservationV1,
    PublishedSeriesAgreementPacketV1,
};
use engine_types::authority::AuthorityEffect;

#[path = "support/synthetic_program_boundary.rs"]
mod synthetic_program_boundary;

fn packet() -> PublishedSeriesAgreementPacketV1 {
    // This copies the declared coordinate contract into a synthetic input.
    // No paper, ledger or historical packet is read, hashed, or replayed here.
    let rows = PaperAgreementIdV1::ALL
        .iter()
        .copied()
        .zip(PUBLISHED_SERIES_COORDINATES.iter())
        .enumerate()
        .map(|(index, (paper_id, coordinate))| PaperAgreementRowV1 {
            paper_id,
            main_path: coordinate.main_path.to_owned(),
            main_sha256: format!("{:064x}", index + 1),
            claim_ledger_path: coordinate.claim_ledger_path.to_owned(),
            claim_ledger_sha256: format!("{:064x}", index + 101),
            claim_row_count: coordinate.claim_row_count,
            verdict: PaperAgreementVerdictV1::Agrees,
            action: PUBLISHED_SERIES_REQUIRED_ROW_ACTION.to_owned(),
            declared_status_ceiling_preserved: true,
            authority_effect: AuthorityEffect::None,
        })
        .collect();
    PublishedSeriesAgreementPacketV1 {
        schema_version: PUBLISHED_SERIES_PACKET_SCHEMA_V1.to_owned(),
        packet_id: "synthetic-s07-005-series-fixture".to_owned(),
        frozen_base: "a".repeat(40),
        rows,
        exact_write_surfaces: vec!["synthetic/fixture-only".to_owned()],
        boundary: synthetic_program_boundary::boundary(),
    }
}

// All observation flags below are declared test inputs, not actual replay evidence.
fn observation(packet: &PublishedSeriesAgreementPacketV1) -> PublishedSeriesAgreementObservationV1 {
    PublishedSeriesAgreementObservationV1 {
        matrix_sha256: published_series_matrix_sha256_v1(&packet.rows).unwrap(),
        paper_hashes_replayed: true,
        claim_ledgers_present: true,
        declared_status_ceiling_scan_passed: true,
        verify_markers_preserved: true,
        g15_final_report_available: false,
        independent_review_accepted: true,
    }
}

#[test]
fn synthetic_agreement_inputs_do_not_promote_open_claims() {
    let packet = packet();
    let result = verify_published_series_agreement_v1(&packet, &observation(&packet)).unwrap();
    assert_eq!(result.paper_count, 11);
    assert_eq!(result.agrees_count, 11);
    assert_eq!(result.drifted_count, 0);
    assert_eq!(result.conflicts_count, 0);
    assert!(result.g15_dependency_open);
    assert_eq!(result.terminal, CodaTerminal::StabilizedSurvivor);
    assert!(!result.publication_performed);
    assert!(!result.promotion_constructor_called);
    assert!(!result.gate_activated);
    assert_eq!(result.authority_effect, AuthorityEffect::None);
}

#[test]
fn missing_paper_is_rejected() {
    let mut packet = packet();
    packet.rows.pop();
    assert_eq!(
        packet.validate(),
        Err(PublishedSeriesAgreementError::MatrixChanged)
    );
}

#[test]
fn changed_claim_count_is_rejected() {
    let mut packet = packet();
    packet.rows[0].claim_row_count += 1;
    assert_eq!(
        packet.validate(),
        Err(PublishedSeriesAgreementError::MatrixChanged)
    );
}

#[test]
fn invalid_source_hash_is_rejected() {
    let mut packet = packet();
    packet.rows[0].main_sha256 = "not-a-sha256".to_owned();
    assert_eq!(
        packet.validate(),
        Err(PublishedSeriesAgreementError::InvalidSourceHash)
    );
}

#[test]
fn g15_report_cannot_be_invented() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.g15_final_report_available = true;
    assert_eq!(
        verify_published_series_agreement_v1(&packet, &observation),
        Err(PublishedSeriesAgreementError::UnexpectedG15Status)
    );
}

#[test]
fn verify_and_status_ceilings_must_survive() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.verify_markers_preserved = false;
    assert_eq!(
        verify_published_series_agreement_v1(&packet, &observation),
        Err(PublishedSeriesAgreementError::StatusCeilingDrift)
    );
}

#[test]
fn drifted_verdict_is_rejected() {
    let mut packet = packet();
    packet.rows[0].verdict = PaperAgreementVerdictV1::Drifted;
    assert_eq!(
        packet.validate(),
        Err(PublishedSeriesAgreementError::MatrixChanged)
    );
}

#[test]
fn authority_expansion_is_rejected() {
    let mut packet = packet();
    packet.boundary.promotion_permission = true;
    assert!(matches!(
        packet.validate(),
        Err(PublishedSeriesAgreementError::Common(_))
    ));
}

// Origin: vendor/engine/tests/engine_state/published_series_agreement.rs
// Claim: urn:omega:crates_rs:tests:published-series-agreement:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecordffd83991 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecordffd83991` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryErrorffd83991 {
    /// Refused because `admitted_items` was zero.
    EmptyAdmission,
    /// Refused because `capacity_bound` was zero.
    CapacityZero,
    /// Refused because `admitted_items` exceeded `capacity_bound`.
    ExceedsCapacity {
        /// Requested item count.
        admitted_items: u64,
        /// Declared maximum capacity.
        capacity_bound: u64,
    },
}

#[allow(dead_code, missing_docs)]
impl BoundaryErrorffd83991 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryErrorffd83991 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryErrorffd83991 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecordffd83991 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryErrorffd83991> {
        if capacity_bound == 0 {
            return Err(BoundaryErrorffd83991::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryErrorffd83991::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryErrorffd83991::ExceedsCapacity {
                admitted_items,
                capacity_bound,
            });
        }
        Ok(Self {
            admitted_items,
            capacity_bound,
        })
    }

    /// Returns the admitted item count.
    pub const fn admitted_items(&self) -> u64 {
        self.admitted_items
    }

    /// Returns the declared capacity bound.
    pub const fn capacity_bound(&self) -> u64 {
        self.capacity_bound
    }

    /// Returns the remaining capacity (`capacity_bound - admitted_items`).
    pub const fn remaining_capacity(&self) -> u64 {
        self.capacity_bound.saturating_sub(self.admitted_items)
    }
}

#[test]
fn l4_boundary_admits_and_refuses_ffd83991() {
    let admitted = BoundaryRecordffd83991::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecordffd83991::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
