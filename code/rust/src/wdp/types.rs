// Executable finite evidence; AuthorityEffect: None.
//! Core value objects and types for the Witnessed Difference Programme crate.

use serde::{Deserialize, Serialize};
use std::fmt;

/// Explicit AuthorityEffect enum enforcing constitutional firewall.
/// Under Anomalon doctrine, mathematical evaluations carry AuthorityEffect::None.
#[derive(
    Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize, Default,
)]
pub enum AuthorityEffect {
    #[default]
    None,
}

impl fmt::Display for AuthorityEffect {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::None => write!(f, "None"),
        }
    }
}

/// Computes SHA-256 hex digest for arbitrary byte sequences.
pub fn sha256_digest(bytes: &[u8]) -> String {
    use sha2::{Digest, Sha256};
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    hex::encode(hasher.finalize())
}

/// Computes Blake3 hex digest for arbitrary byte sequences.
pub fn blake3_digest(bytes: &[u8]) -> String {
    let hash = blake3::hash(bytes);
    hash.to_hex().to_string()
}
