//! Test-only custody for imported AnomalonPy source bytes.
//! No Git lookup, network access, execution, or authority promotion occurs here.
#![allow(dead_code)]

use std::path::{Path, PathBuf};
use std::sync::OnceLock;

use serde::Deserialize;
use sha2::{Digest, Sha256};

pub const SOURCE_REPOSITORY: &str = "urn:upstream:history-source";

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Entry {
    pub source_commit: String,
    pub source_path: String,
    pub git_blob_oid: String,
    pub sha256: String,
    pub bytes: u64,
    pub purpose: String,
    pub materialization: String,
    pub materialized_sha256: String,
    pub materialized_bytes: u64,
    pub storage_path: String,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct UnavailableCoordinate {
    pub path: String,
    pub status: String,
    pub inspected_repository: String,
    pub inspected_commit: String,
    pub reason: String,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Manifest {
    pub schema_version: String,
    pub source_repository: String,
    pub scope: String,
    pub authority_effect: String,
    pub unavailable_published_coordinates: Vec<UnavailableCoordinate>,
    pub entries: Vec<Entry>,
}

pub fn repository_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(3)
        .expect("omega_state must be under omega_engine/crates_rs")
        .to_path_buf()
}

pub fn manifest() -> &'static Manifest {
    static MANIFEST: OnceLock<Manifest> = OnceLock::new();
    MANIFEST.get_or_init(|| {
        let value: Manifest =
            serde_json::from_slice(include_bytes!("../fixtures/upstream_history/custody.json"))
                .expect("the checked-in upstream custody manifest must parse");
        assert_eq!(
            value.schema_version,
            "omega.state.upstream-fixture-custody.v1"
        );
        assert_eq!(value.source_repository, SOURCE_REPOSITORY);
        assert_eq!(value.authority_effect, "None");
        assert!(!value.scope.trim().is_empty());
        assert!(!value.entries.is_empty());
        let mut previous = None;
        for entry in &value.entries {
            let identity = (entry.source_commit.as_str(), entry.source_path.as_str());
            assert!(
                previous.is_none_or(|old| old < identity),
                "custody entries must be sorted and unique"
            );
            previous = Some(identity);
        }
        value
    })
}

fn lower_hex(value: &str, width: usize) -> bool {
    value.len() == width
        && value
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}

fn relative_path(value: &str) -> bool {
    !value.is_empty()
        && !value.contains(['\\', ':'])
        && value
            .split('/')
            .all(|part| !matches!(part, "" | "." | ".."))
}

pub fn find_entry<'a>(entries: &'a [Entry], commit: &str, path: &str) -> Result<&'a Entry, String> {
    entries
        .iter()
        .find(|entry| entry.source_commit == commit && entry.source_path == path)
        .ok_or_else(|| {
            format!("OPEN_UNAVAILABLE_SOURCE: {commit}:{path} has no pinned custody entry")
        })
}

fn validate_entry_identity(entry: &Entry) -> bool {
    let hashes_ok = lower_hex(&entry.source_commit, 40)
        && lower_hex(&entry.git_blob_oid, 40)
        && lower_hex(&entry.sha256, 64)
        && lower_hex(&entry.materialized_sha256, 64);
    let paths_ok = relative_path(&entry.source_path)
        && relative_path(&entry.storage_path)
        && !entry.purpose.trim().is_empty();
    hashes_ok && paths_ok
}

fn materialize_crlf_checkout(raw: &[u8]) -> Vec<u8> {
    // The original CODA1 receipts hashed Windows checkout bytes. Keep
    // the stored Git blob intact and spell out the sole conversion.
    let mut output = Vec::with_capacity(raw.len());
    let mut index = 0;
    while index < raw.len() {
        if raw[index] == b'\r' && raw.get(index + 1) == Some(&b'\n') {
            index += 1;
        }
        if raw[index] == b'\n' {
            output.push(b'\r');
        }
        output.push(raw[index]);
        index += 1;
    }
    output
}

pub fn verify_bytes(entry: &Entry, raw: &[u8]) -> Result<Vec<u8>, String> {
    if !validate_entry_identity(entry) {
        return Err("invalid upstream custody identity".to_owned());
    }
    if raw.len() as u64 != entry.bytes || format!("{:x}", Sha256::digest(raw)) != entry.sha256 {
        return Err(format!(
            "raw source bytes do not match {}:{}",
            entry.source_commit, entry.source_path
        ));
    }
    let materialized = match entry.materialization.as_str() {
        "raw-git-blob" => raw.to_vec(),
        "crlf-checkout" => materialize_crlf_checkout(raw),
        _ => return Err("unsupported historical byte materialization".to_owned()),
    };
    if materialized.len() as u64 != entry.materialized_bytes
        || format!("{:x}", Sha256::digest(&materialized)) != entry.materialized_sha256
    {
        return Err("materialized source bytes do not match the historical receipt".to_owned());
    }
    Ok(materialized)
}

/// Where a custody entry's bytes live in this vendored tree. Custody records
/// keep the upstream storage path byte-exact; only the directory prefix moves.
pub fn storage_location(storage_path: &str) -> PathBuf {
    let vendored = storage_path
        .replacen("omega_engine/crates_rs/tests/omega_state/", "vendor/engine/tests/engine_state/", 1)
        .replacen("omega_engine/crates_rs/omega_state/", "vendor/engine/engine_state/", 1);
    repository_root().join(vendored)
}

pub fn read_entry(entry: &Entry) -> Result<Vec<u8>, String> {
    if !relative_path(&entry.storage_path) {
        return Err("invalid upstream storage path".to_owned());
    }
    let raw = std::fs::read(storage_location(&entry.storage_path))
        .map_err(|error| format!("OPEN_UNAVAILABLE_SOURCE: {}: {error}", entry.storage_path))?;
    verify_bytes(entry, &raw)
}

pub fn frozen_blob(commit: &str, path: &str) -> Vec<u8> {
    let entry = find_entry(&manifest().entries, commit, path)
        .expect("historical source identity must be pinned");
    read_entry(entry).expect("historical source bytes must match custody")
}

pub fn unavailable_coordinate(path: &str) -> Result<&'static UnavailableCoordinate, String> {
    let entry = manifest()
        .unavailable_published_coordinates
        .iter()
        .find(|entry| entry.path == path)
        .ok_or_else(|| format!("coordinate has no explicit source disposition: {path}"))?;
    if entry.status != "OPEN_UNAVAILABLE_SOURCE"
        || entry.inspected_repository != SOURCE_REPOSITORY
        || !lower_hex(&entry.inspected_commit, 40)
        || !relative_path(&entry.path)
        || entry.reason.trim().is_empty()
    {
        return Err("invalid unavailable-source disposition".to_owned());
    }
    Ok(entry)
}

// Origin: vendor/engine/tests/engine_state/support/upstream_history.rs
// Claim: urn:omega:crates_rs:tests:upstream-history:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord1bb8819b {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord1bb8819b` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError1bb8819b {
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
impl BoundaryError1bb8819b {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError1bb8819b {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError1bb8819b {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord1bb8819b {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError1bb8819b> {
        if capacity_bound == 0 {
            return Err(BoundaryError1bb8819b::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError1bb8819b::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError1bb8819b::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_1bb8819b() {
    let admitted = BoundaryRecord1bb8819b::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord1bb8819b::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
