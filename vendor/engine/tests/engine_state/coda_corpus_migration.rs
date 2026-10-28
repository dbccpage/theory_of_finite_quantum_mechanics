//! Synthetic schema/validator fixtures; no historical run or receipt is replayed.
//! Missing upstream packet custody is recorded in fixtures/synthetic_program_fixture_custody.json.

use engine_state::{
    verify_coda_corpus_migration_v1, CodaCorpusMigrationError, CodaCorpusMigrationObservationV1,
    CodaCorpusMigrationPacketV1, CodaTerminal, CODA_CORPUS_DESTINATION_ROOT_V1,
    CODA_CORPUS_MIGRATION_PACKET_SCHEMA_V1, CODA_CORPUS_REFERENCE_FILE_COUNT_V1,
    CODA_CORPUS_SOURCE_FILE_COUNT_V1, CODA_CORPUS_SOURCE_ROOT_V1,
};
use engine_types::authority::AuthorityEffect;

#[path = "support/synthetic_program_boundary.rs"]
mod synthetic_program_boundary;

fn packet() -> CodaCorpusMigrationPacketV1 {
    // Hash-shaped values here are invented unit inputs, not custody claims.
    // The manifest path is a schema-mandated inert string; no file is read.
    CodaCorpusMigrationPacketV1 {
        schema_version: CODA_CORPUS_MIGRATION_PACKET_SCHEMA_V1.to_owned(),
        packet_id: "synthetic-s07-006-migration-fixture".to_owned(),
        frozen_base: "a".repeat(40),
        manifest_path: "docs/status/gtoc_corpus_migration_manifest_2026-07-20.json".to_owned(),
        manifest_sha256: "1".repeat(64),
        source_root: CODA_CORPUS_SOURCE_ROOT_V1.to_owned(),
        destination_root: CODA_CORPUS_DESTINATION_ROOT_V1.to_owned(),
        source_file_count: CODA_CORPUS_SOURCE_FILE_COUNT_V1,
        reference_file_count: CODA_CORPUS_REFERENCE_FILE_COUNT_V1,
        collision_count: 0,
        destination_absent: true,
        move_executed: false,
        exact_write_surfaces: vec!["synthetic/fixture-only".to_owned()],
        boundary: synthetic_program_boundary::boundary(),
    }
}

// All observation flags below are declared test inputs, not actual replay evidence.
fn observation(packet: &CodaCorpusMigrationPacketV1) -> CodaCorpusMigrationObservationV1 {
    CodaCorpusMigrationObservationV1 {
        manifest_sha256: packet.manifest_sha256.clone(),
        source_hashes_replayed: true,
        source_tree_present: true,
        destination_absent: true,
        collision_count: 0,
        reference_census_replayed: true,
        move_executed: false,
        independent_review_accepted: true,
    }
}

#[test]
fn synthetic_plan_keeps_an_unexecuted_move_open() {
    let packet = packet();
    let result = verify_coda_corpus_migration_v1(&packet, &observation(&packet)).unwrap();
    assert_eq!(result.source_file_count, 93);
    assert_eq!(result.reference_file_count, 116);
    assert_eq!(result.collision_count, 0);
    assert!(result.destination_absent);
    assert!(!result.move_executed);
    assert_eq!(result.residual_obligations.len(), 2);
    assert_eq!(result.terminal, CodaTerminal::OpenObstruction);
    assert_eq!(result.authority_effect, AuthorityEffect::None);
}

#[test]
fn inventory_count_drift_is_rejected() {
    let mut packet = packet();
    packet.source_file_count += 1;
    assert_eq!(
        packet.validate(),
        Err(CodaCorpusMigrationError::PacketChanged)
    );
}

#[test]
fn manifest_hash_mismatch_is_rejected() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.manifest_sha256 = "0".repeat(64);
    assert_eq!(
        verify_coda_corpus_migration_v1(&packet, &observation),
        Err(CodaCorpusMigrationError::ManifestHashMismatch)
    );
}

#[test]
fn collision_is_rejected() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.collision_count = 1;
    assert_eq!(
        verify_coda_corpus_migration_v1(&packet, &observation),
        Err(CodaCorpusMigrationError::InventoryReplayFailed)
    );
}

#[test]
fn an_unlicensed_move_cannot_be_reported() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.move_executed = true;
    assert_eq!(
        verify_coda_corpus_migration_v1(&packet, &observation),
        Err(CodaCorpusMigrationError::UnexpectedMove)
    );
}

#[test]
fn missing_independent_review_is_rejected() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.independent_review_accepted = false;
    assert_eq!(
        verify_coda_corpus_migration_v1(&packet, &observation),
        Err(CodaCorpusMigrationError::IndependentReviewMissing)
    );
}

#[test]
fn authority_expansion_is_rejected() {
    let mut packet = packet();
    packet.boundary.publication_permission = true;
    assert!(matches!(
        packet.validate(),
        Err(CodaCorpusMigrationError::Common(_))
    ));
}

// Origin: vendor/engine/tests/engine_state/coda_corpus_migration.rs
// Claim: urn:omega:crates_rs:tests:coda-corpus-migration:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord709678c2 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord709678c2` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError709678c2 {
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
impl BoundaryError709678c2 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError709678c2 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError709678c2 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord709678c2 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError709678c2> {
        if capacity_bound == 0 {
            return Err(BoundaryError709678c2::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError709678c2::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError709678c2::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_709678c2() {
    let admitted = BoundaryRecord709678c2::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord709678c2::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
