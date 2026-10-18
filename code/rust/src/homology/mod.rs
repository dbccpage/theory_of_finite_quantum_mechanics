//! Exact finite rational homology. AuthorityEffect: None.
//!
//! Runtime certificates establish finite algebraic identities only. The canonical
//! carrier admits shapes, d1*d0=0, positive weights and rank inclusion before use.

use crate::linear_algebra::scalars::hash_rational;
use crate::linear_algebra::{ExactMatrix, Q};
use serde::{Deserialize, Serialize};

pub mod boundary;
pub mod carrier;
pub mod carrier_manifest;
pub mod chain;
pub mod chain_complex;
pub mod coboundary;
pub mod cochain;
pub mod cochain_complex;
pub mod errors;
pub mod exact_carrier;
mod exact_scalar;
pub mod graded_vector;
pub mod hashing;
pub mod ids;
pub mod rank_certificate;
pub mod simplicial;
pub mod witness;

#[cfg(test)]
mod l5a_challenges;

pub use errors::HomologicalError;
pub use hashing::Hash256;

/// Legacy root matrix digest; its tag is retained for existing receipts.
pub fn hash_exact_matrix(m: &ExactMatrix<Q>) -> Hash256 {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"TheoryOfFiniteQM.ExactMatrix<Q>.v1");
    hasher.update(&(m.rows() as u64).to_le_bytes());
    hasher.update(&(m.cols() as u64).to_le_bytes());
    for val in m.as_slice() {
        hash_rational(&mut hasher, val);
    }
    Hash256(*hasher.finalize().as_bytes())
}

/// Compatibility facade over the single admitted carrier. Serialization is data;
/// deserialization recomputes the law, ranks and hashes instead of trusting bytes.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(try_from = "CarrierWire", into = "CarrierWire")]
pub struct Carrier {
    inner: carrier::Carrier,
}

#[derive(Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct CarrierWire {
    c0_dim: usize,
    c1_dim: usize,
    c2_dim: usize,
    d0: ExactMatrix<Q>,
    d1: ExactMatrix<Q>,
    weights: Vec<Q>,
    d0_hash: Hash256,
    d1_hash: Hash256,
}

impl Carrier {
    pub fn new(
        c0_dim: usize,
        c1_dim: usize,
        c2_dim: usize,
        d0: ExactMatrix<Q>,
        d1: ExactMatrix<Q>,
        weights: Vec<Q>,
    ) -> Result<Self, HomologicalError> {
        let provenance =
            cochain_complex::TheoremProvenance::new("runtime exact d1*d0 verification".into())?;
        Ok(Self {
            inner: carrier::Carrier::new(c0_dim, c1_dim, c2_dim, d0.0, d1.0, weights, provenance)?,
        })
    }
    pub fn c0_dim(&self) -> usize {
        self.inner.c0_dim()
    }
    pub fn c1_dim(&self) -> usize {
        self.inner.c1_dim()
    }
    pub fn c2_dim(&self) -> usize {
        self.inner.c2_dim()
    }
    pub fn d0(&self) -> &crate::linear_algebra::BasicMatrix<Q> {
        self.inner.d0()
    }
    pub fn d1(&self) -> &crate::linear_algebra::BasicMatrix<Q> {
        self.inner.d1()
    }
    pub fn weights(&self) -> &[Q] {
        self.inner.weights()
    }
    pub fn rank_d0(&self) -> usize {
        self.inner.rank_d0()
    }
    pub fn rank_d1(&self) -> usize {
        self.inner.rank_d1()
    }
    pub fn dim_q1(&self) -> usize {
        self.c1_dim() - self.rank_d0()
    }
    pub fn dim_h1(&self) -> Result<usize, HomologicalError> {
        self.inner.dim_h1()
    }
}

impl AsRef<carrier::Carrier> for Carrier {
    fn as_ref(&self) -> &carrier::Carrier {
        &self.inner
    }
}

impl From<Carrier> for CarrierWire {
    fn from(value: Carrier) -> Self {
        let d0 = ExactMatrix(value.d0().clone());
        let d1 = ExactMatrix(value.d1().clone());
        Self {
            c0_dim: value.c0_dim(),
            c1_dim: value.c1_dim(),
            c2_dim: value.c2_dim(),
            d0_hash: hash_exact_matrix(&d0),
            d1_hash: hash_exact_matrix(&d1),
            d0,
            d1,
            weights: value.weights().to_vec(),
        }
    }
}

impl TryFrom<CarrierWire> for Carrier {
    type Error = HomologicalError;
    fn try_from(value: CarrierWire) -> Result<Self, Self::Error> {
        verify_hash(&value.d0_hash, &hash_exact_matrix(&value.d0))?;
        verify_hash(&value.d1_hash, &hash_exact_matrix(&value.d1))?;
        Self::new(
            value.c0_dim,
            value.c1_dim,
            value.c2_dim,
            value.d0,
            value.d1,
            value.weights,
        )
    }
}

fn verify_hash(expected: &Hash256, got: &Hash256) -> Result<(), HomologicalError> {
    if expected != got {
        return Err(HomologicalError::HashMismatch {
            expected: expected.to_hex(),
            got: got.to_hex(),
        });
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::scalars::q;

    #[test]
    fn test_triangle_carrier_homology() {
        // Triangle 1-skeleton (cycle of 3 vertices, 3 edges)
        // d0: C0 (3 vertices) -> C1 (3 edges)
        // e0 = (0, 1): v1 - v0
        // e1 = (1, 2): v2 - v1
        // e2 = (2, 0): v0 - v2
        let d0_rows = vec![
            vec![q(-1), q(1), q(0)],
            vec![q(0), q(-1), q(1)],
            vec![q(1), q(0), q(-1)],
        ];
        let d0 = ExactMatrix::from_rows(d0_rows).unwrap();
        // d1: C1 -> C2 (single 2-simplex face with boundary e0 + e1 + e2)
        let d1_rows = vec![vec![q(1), q(1), q(1)]];
        let d1 = ExactMatrix::from_rows(d1_rows).unwrap();
        let weights = vec![q(1), q(1), q(1)];

        let carrier = Carrier::new(3, 3, 1, d0, d1, weights).unwrap();
        assert_eq!(carrier.rank_d0(), 2);
        assert_eq!(carrier.rank_d1(), 1);
        assert_eq!(carrier.dim_q1(), 1);
        // H^1 = ker(d1) - im(d0) = (3 - 1) - 2 = 0
        assert_eq!(carrier.dim_h1().unwrap(), 0);
    }
}
