//! Carrier: a finite cochain complex C^0 -> C^1 -> C^2 with weights.
//!
//! This is the core carrier for the MSS-N obstruction calculus.
//! All arithmetic is exact over the canonical coefficient domain
//! `omega_homology::scalar::Q` = `BigRational` (ADR-001, 2026-08-04). It was
//! `Rational64` before the widening; nothing here narrows back. The cochain
//! relation is verified at construction time.
//!
//! This module does NOT emit authority-bearing artifacts.
//! Authority promotion belongs to the contract/checking layer.

use crate::cochain_complex::{CochainComplex, TheoremProvenance};
use crate::errors::HomologicalError;
use crate::linear_algebra::scalars::Q;
use crate::linear_algebra::basic_matrix::BasicMatrix;
use linear_algebra::linear_algebra::image_kernel::ExactRowReduction;
use num_traits::Zero;

/// A finite cochain complex C^0 -> C^1 -> C^2 with C^1 weights.
///
/// Verified at construction: d1*d0=0 and all weights positive.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Carrier {
    complex: CochainComplex,
    weights: Vec<Q>,
}

impl Carrier {
    /// Construct a new carrier, verifying d1*d0=0 and weight positivity.
    pub fn new(
        c0_dim: usize,
        c1_dim: usize,
        c2_dim: usize,
        d0: BasicMatrix<Q>,
        d1: BasicMatrix<Q>,
        weights: Vec<Q>,
        provenance: TheoremProvenance,
    ) -> Result<Self, HomologicalError> {
        // Check weight dimensions
        if weights.len() != c1_dim {
            return Err(HomologicalError::WeightDimensionMismatch {
                expected: c1_dim,
                got: weights.len(),
            });
        }

        // Check weight positivity
        for (i, w) in weights.iter().enumerate() {
            if *w <= Q::zero() {
                return Err(HomologicalError::NonPositiveWeight { index: i });
            }
        }

        // Construct cochain complex (verifies d1*d0=0 and dimensions)
        let complex = CochainComplex::new(c0_dim, c1_dim, c2_dim, d0, d1, provenance)?;

        Ok(Self { complex, weights })
    }

    pub fn c0_dim(&self) -> usize {
        self.complex.c0_dim
    }
    pub fn c1_dim(&self) -> usize {
        self.complex.c1_dim
    }
    pub fn c2_dim(&self) -> usize {
        self.complex.c2_dim
    }
    pub fn d0(&self) -> &BasicMatrix<Q> {
        &self.complex.d0.matrix
    }
    pub fn d1(&self) -> &BasicMatrix<Q> {
        &self.complex.d1.matrix
    }
    pub fn weights(&self) -> &[Q] {
        &self.weights
    }
    pub fn complex(&self) -> &CochainComplex {
        &self.complex
    }

    /// Rank of d0 = dim(im(d0)) = dim(B^1).
    pub fn rank_d0(&self) -> Result<usize, HomologicalError> {
        self.d0()
            .rank()
            .map_err(|e| HomologicalError::UnsupportedOperation(format!("{}", e)))
    }

    /// Rank of d1.
    pub fn rank_d1(&self) -> Result<usize, HomologicalError> {
        self.d1()
            .rank()
            .map_err(|e| HomologicalError::UnsupportedOperation(format!("{}", e)))
    }

    /// Dimension of Q^1 = C^1/B^1 = c1_dim - rank(d0).
    pub fn dim_q1(&self) -> Result<usize, HomologicalError> {
        Ok(self.c1_dim() - self.rank_d0()?)
    }

    /// Dimension of H^1 = ker(d1) / im(d0).
    pub fn dim_h1(&self) -> Result<usize, HomologicalError> {
        let ker_d1_dim = self.c1_dim() - self.rank_d1()?;
        let im_d0_dim = self.rank_d0()?;
        ker_d1_dim
            .checked_sub(im_d0_dim)
            .ok_or(HomologicalError::HomologyDimensionUnderflow {
                ker_dim: ker_d1_dim,
                im_dim: im_d0_dim,
            })
    }

    /// Compute the carrier manifest.
    pub fn manifest(&self) -> Result<crate::carrier_manifest::CarrierManifest, HomologicalError> {
        crate::carrier_manifest::CarrierManifest::from_carrier(self)
    }
}
