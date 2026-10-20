//! Computed identity of an admitted rational carrier. AuthorityEffect: None.
//!
//! A digest binds data; it does not prove a theorem or authenticate an author.

use super::carrier::Carrier;
use super::errors::HomologicalError;
use super::hashing::{hash_carrier_manifest, hash_matrix, hash_weights, Hash256};
use serde::Serialize;

pub const CARRIER_MANIFEST_VERSION: u32 = 1;
pub const COEFFICIENT_DOMAIN: &str = "Q";
pub const COEFFICIENT_REPRESENTATION: &str = "BigRational";

/// Immutable, computed receipt. Wire data cannot construct a verified manifest.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CarrierManifest {
    version: u32,
    carrier_hash: Hash256,
    d0_hash: Hash256,
    d1_hash: Hash256,
    weights_hash: Hash256,
    dimensions: (usize, usize, usize),
    ranks: (usize, usize),
}

impl CarrierManifest {
    pub fn from_carrier<C: AsRef<Carrier>>(carrier: &C) -> Result<Self, HomologicalError> {
        let carrier = carrier.as_ref();
        let dimensions = (carrier.c0_dim(), carrier.c1_dim(), carrier.c2_dim());
        let d0_hash = hash_matrix(carrier.d0())?;
        let d1_hash = hash_matrix(carrier.d1())?;
        let weights_hash = hash_weights(carrier.weights())?;
        let carrier_hash = hash_carrier_manifest(
            dimensions.0,
            dimensions.1,
            dimensions.2,
            &d0_hash,
            &d1_hash,
            &weights_hash,
        );
        Ok(Self {
            version: CARRIER_MANIFEST_VERSION,
            carrier_hash,
            d0_hash,
            d1_hash,
            weights_hash,
            dimensions,
            ranks: (carrier.rank_d0(), carrier.rank_d1()),
        })
    }

    pub fn carrier_hash(&self) -> &Hash256 {
        &self.carrier_hash
    }
    pub fn d0_hash(&self) -> &Hash256 {
        &self.d0_hash
    }
    pub fn d1_hash(&self) -> &Hash256 {
        &self.d1_hash
    }
    pub fn dimensions(&self) -> (usize, usize, usize) {
        self.dimensions
    }
    pub fn ranks(&self) -> (usize, usize) {
        self.ranks
    }

    /// Recompute every field against the admitted carrier, rather than trust hashes alone.
    pub fn verifies(&self, carrier: &Carrier) -> Result<bool, HomologicalError> {
        Ok(self == &Self::from_carrier(carrier)?)
    }
}
