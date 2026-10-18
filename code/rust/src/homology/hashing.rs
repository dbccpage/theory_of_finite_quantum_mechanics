//! Deterministic BLAKE3 hashing with domain-separated tags.
//!
//! All hashing functions use domain separation to prevent hash collisions
//! between different mathematical objects that might have the same raw data.

use crate::linear_algebra::scalars::{hash_bigint, hash_rational, Q};
use crate::linear_algebra::basic_matrix::BasicMatrix;
use num_bigint::BigInt;

/// A 256-bit hash value.
#[derive(Debug, Clone, PartialEq, Eq, Hash, serde::Serialize, serde::Deserialize)]
pub struct Hash256(pub [u8; 32]);

impl Hash256 {
    pub fn as_bytes(&self) -> &[u8; 32] {
        &self.0
    }

    pub fn to_hex(&self) -> String {
        hex::encode(self.0)
    }
}

impl std::fmt::Display for Hash256 {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}..{}",
            hex::encode(&self.0[..4]),
            hex::encode(&self.0[28..])
        )
    }
}

/// Domain-separated hash for a BasicMatrix<Q>.
pub fn hash_matrix(m: &BasicMatrix<Q>) -> Hash256 {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"MSSN.BasicMatrix<BigRational>.v2");
    hasher.update(&(m.rows() as u64).to_le_bytes());
    hasher.update(&(m.cols() as u64).to_le_bytes());
    for val in m.as_slice() {
        hash_rational(&mut hasher, val);
    }
    Hash256(*hasher.finalize().as_bytes())
}

/// Domain-separated hash for an integer matrix — the ℤ-lattice representation of a
/// boundary map, as fed to Smith normal form.
///
/// Distinct from [`hash_matrix`] by tag: a `BasicMatrix<BigInt>` and the
/// `BasicMatrix<Q>` it was extracted from denote different objects (one is a map of
/// lattices, the other a map of ℚ-vector spaces) even when they carry equal values.
/// Entries are length-prefixed via [`hash_bigint`], since `BigInt` has no fixed
/// width and bare concatenation is not injective.
pub fn hash_integer_matrix(m: &BasicMatrix<BigInt>) -> Hash256 {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"MSSN.BasicMatrix<BigInt>.lattice.v1");
    hasher.update(&(m.rows() as u64).to_le_bytes());
    hasher.update(&(m.cols() as u64).to_le_bytes());
    for val in m.as_slice() {
        hash_bigint(&mut hasher, val);
    }
    Hash256(*hasher.finalize().as_bytes())
}

/// Domain-separated hash for a vector of Q values.
pub fn hash_vector(v: &[Q]) -> Hash256 {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"OMEGA.Vector<BigRational>.v2");
    hasher.update(&(v.len() as u64).to_le_bytes());
    for val in v {
        hash_rational(&mut hasher, val);
    }
    Hash256(*hasher.finalize().as_bytes())
}

/// Domain-separated hash for a chain complex manifest.
pub fn hash_chain_complex_manifest(
    c0_dim: usize,
    c1_dim: usize,
    c2_dim: usize,
    boundary_1_hash: &Hash256,
    boundary_2_hash: &Hash256,
) -> Hash256 {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"OMEGA.ChainComplexManifest.v1");
    hasher.update(&(c0_dim as u64).to_le_bytes());
    hasher.update(&(c1_dim as u64).to_le_bytes());
    hasher.update(&(c2_dim as u64).to_le_bytes());
    hasher.update(boundary_1_hash.as_bytes());
    hasher.update(boundary_2_hash.as_bytes());
    Hash256(*hasher.finalize().as_bytes())
}

/// Domain-separated hash for a cochain complex manifest.
pub fn hash_cochain_complex_manifest(
    c0_dim: usize,
    c1_dim: usize,
    c2_dim: usize,
    d0_hash: &Hash256,
    d1_hash: &Hash256,
) -> Hash256 {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"OMEGA.CochainComplexManifest.v1");
    hasher.update(&(c0_dim as u64).to_le_bytes());
    hasher.update(&(c1_dim as u64).to_le_bytes());
    hasher.update(&(c2_dim as u64).to_le_bytes());
    hasher.update(d0_hash.as_bytes());
    hasher.update(d1_hash.as_bytes());
    Hash256(*hasher.finalize().as_bytes())
}

/// Domain-separated hash for carrier manifest.
pub fn hash_carrier_manifest(
    c0_dim: usize,
    c1_dim: usize,
    c2_dim: usize,
    d0_hash: &Hash256,
    d1_hash: &Hash256,
    weights_hash: &Hash256,
) -> Hash256 {
    let mut hasher = blake3::Hasher::new();
    // v2 (ADR-001). v1 hashed the literal `1u32` while its payload already named
    // BigRational — the version, the tag and the declared domain disagreed. The
    // version fed here is now the same constant the manifest struct emits, so the
    // three cannot drift apart again.
    hasher.update(b"OMEGA.CarrierManifest.v2");
    hasher.update(&crate::carrier_manifest::CARRIER_MANIFEST_VERSION.to_le_bytes());
    hasher.update(d0_hash.as_bytes());
    hasher.update(d1_hash.as_bytes());
    hasher.update(weights_hash.as_bytes());
    hasher.update(&(c0_dim as u64).to_le_bytes());
    hasher.update(&(c1_dim as u64).to_le_bytes());
    hasher.update(&(c2_dim as u64).to_le_bytes());
    // Domain and representation are hashed separately, matching the split in the
    // manifest struct. A representation change must move the hash; recording only
    // one of the two is what made the v1 receipt false.
    hasher.update(crate::carrier_manifest::COEFFICIENT_DOMAIN.as_bytes());
    hasher.update(crate::carrier_manifest::COEFFICIENT_REPRESENTATION.as_bytes());
    Hash256(*hasher.finalize().as_bytes())
}

/// Domain-separated hash for weights vector.
pub fn hash_weights(weights: &[Q]) -> Hash256 {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"MSSN.CarrierWeights<BigRational>.v2");
    hasher.update(&(weights.len() as u64).to_le_bytes());
    for w in weights {
        hash_rational(&mut hasher, w);
    }
    Hash256(*hasher.finalize().as_bytes())
}

/// Domain-separated hash for witness provenance.
pub fn hash_provenance(verification_source: &str) -> Hash256 {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"MSSN.TheoremProvenance.v1");
    hasher.update(verification_source.as_bytes());
    Hash256(*hasher.finalize().as_bytes())
}

/// Domain-separated hash for cochain complex witness.
pub fn hash_cochain_witness(
    d0_shape: (usize, usize),
    d1_shape: (usize, usize),
    provenance_hash: &Hash256,
) -> Hash256 {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"MSSN.CochainComplexWitness.v1");
    hasher.update(&(d0_shape.0 as u64).to_le_bytes());
    hasher.update(&(d0_shape.1 as u64).to_le_bytes());
    hasher.update(&(d1_shape.0 as u64).to_le_bytes());
    hasher.update(&(d1_shape.1 as u64).to_le_bytes());
    hasher.update(provenance_hash.as_bytes());
    Hash256(*hasher.finalize().as_bytes())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::scalars::{q, qr};

    #[test]
    fn test_hash256_display() {
        let h = Hash256([0u8; 32]);
        let s = format!("{}", h);
        // Should show first 4 bytes and last 4 bytes in hex
        assert!(s.contains(".."));
        assert_eq!(s, "00000000..00000000");
    }

    #[test]
    fn test_hash256_to_hex() {
        let h = Hash256([0xAB; 32]);
        let hex_str = h.to_hex();
        assert_eq!(hex_str.len(), 64);
        assert!(hex_str.chars().all(|c| c.is_ascii_hexdigit()));
    }

    #[test]
    fn test_hash_vector_deterministic() {
        let v = vec![q(1), qr(1, 2), q(3)];
        let h1 = hash_vector(&v);
        let h2 = hash_vector(&v);
        assert_eq!(h1, h2);
    }

    #[test]
    fn test_hash_vector_different_values() {
        let v1 = vec![q(1), q(2)];
        let v2 = vec![q(1), q(3)];
        let h1 = hash_vector(&v1);
        let h2 = hash_vector(&v2);
        assert_ne!(h1, h2);
    }

    #[test]
    fn test_hash_provenance_deterministic() {
        let h1 = hash_provenance("omega_homology::test");
        let h2 = hash_provenance("omega_homology::test");
        assert_eq!(h1, h2);
    }

    #[test]
    fn test_hash_provenance_different_sources() {
        let h1 = hash_provenance("source_a");
        let h2 = hash_provenance("source_b");
        assert_ne!(h1, h2);
    }

    #[test]
    fn test_hash_weights_deterministic() {
        let w = vec![qr(1, 2), qr(3, 4)];
        let h1 = hash_weights(&w);
        let h2 = hash_weights(&w);
        assert_eq!(h1, h2);
    }
}
