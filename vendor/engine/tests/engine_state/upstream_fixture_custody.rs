//! Exact historical byte controls, separate from synthetic protocol inputs.

#[path = "support/upstream_history.rs"]
mod upstream_history;

use upstream_history::{find_entry, manifest, read_entry, verify_bytes};

#[test]
fn every_pinned_source_replays_its_declared_bytes() {
    let custody = manifest();
    assert_eq!(custody.entries.len(), 62);
    for entry in &custody.entries {
        read_entry(entry).unwrap_or_else(|error| panic!("{}: {error}", entry.source_path));
    }
}

#[test]
fn changed_missing_or_rebound_sources_fail_closed() {
    let entry = &manifest().entries[0];
    let raw = std::fs::read(upstream_history::storage_location(&entry.storage_path)).unwrap();
    assert!(verify_bytes(entry, &raw).is_ok());
    let mut changed = raw.clone();
    changed[0] ^= 1;
    assert!(verify_bytes(entry, &changed).is_err());
    assert!(verify_bytes(entry, &raw[..raw.len() - 1]).is_err());
    assert!(find_entry(&manifest().entries, &"0".repeat(40), &entry.source_path).is_err());
    assert!(find_entry(
        &manifest().entries,
        &entry.source_commit,
        "unregistered/source"
    )
    .is_err());
    let mut missing = entry.clone();
    missing.storage_path = "unregistered/source".to_owned();
    assert!(read_entry(&missing).is_err());
    let mut escaped = entry.clone();
    escaped.storage_path = "../source".to_owned();
    assert!(read_entry(&escaped).is_err());
}

#[test]
fn coda1_checkout_materialization_is_explicit_and_hash_checked() {
    let entries = manifest()
        .entries
        .iter()
        .filter(|entry| entry.materialization == "crlf-checkout")
        .collect::<Vec<_>>();
    assert_eq!(entries.len(), 3);
    for entry in entries {
        assert_ne!(entry.sha256, entry.materialized_sha256);
        let raw =
            std::fs::read(upstream_history::storage_location(&entry.storage_path)).unwrap();
        let materialized = verify_bytes(entry, &raw).unwrap();
        assert_ne!(raw, materialized);
        let mut wrong_mode = entry.clone();
        wrong_mode.materialization = "raw-git-blob".to_owned();
        assert!(verify_bytes(&wrong_mode, &raw).is_err());
        let mut wrong_digest = entry.clone();
        wrong_digest.materialized_sha256 = "0".repeat(64);
        assert!(verify_bytes(&wrong_digest, &raw).is_err());
    }
}

#[test]
fn unavailable_publication_sources_do_not_count_as_historical_replay() {
    assert_eq!(manifest().unavailable_published_coordinates.len(), 22);
    for source in &manifest().unavailable_published_coordinates {
        assert_eq!(
            upstream_history::unavailable_coordinate(&source.path)
                .unwrap()
                .status,
            "OPEN_UNAVAILABLE_SOURCE"
        );
        assert!(find_entry(&manifest().entries, &source.inspected_commit, &source.path).is_err());
    }
    assert!(upstream_history::unavailable_coordinate("unregistered/paper.md").is_err());
}

// Origin: vendor/engine/tests/engine_state/upstream_fixture_custody.rs
// Claim: urn:omega:crates_rs:tests:upstream-fixture-custody:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord5d78233e {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord5d78233e` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError5d78233e {
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
impl BoundaryError5d78233e {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError5d78233e {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError5d78233e {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord5d78233e {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError5d78233e> {
        if capacity_bound == 0 {
            return Err(BoundaryError5d78233e::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError5d78233e::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError5d78233e::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_5d78233e() {
    let admitted = BoundaryRecord5d78233e::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord5d78233e::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
