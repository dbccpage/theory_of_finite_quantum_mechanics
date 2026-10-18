//! Connes discrete spectral triple (A, H, D) over exact rationals.
//!
//! Origin: papers/derivations/general_relativity/rust/src/spectral_triple.rs
//! Claim: DERIV-GR-SPECTRAL-001
//! AuthorityEffect: None.

use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum SpectralError {
    DimensionMismatch,
    NonHermitianDirac,
    ZeroDenominator,
}

/// A finite dimensional spectral triple (A, H, D).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiniteSpectralTriple {
    pub dim: usize,
    pub label: String,
    /// Diagonal elements of Dirac operator D (self-adjoint)
    pub dirac_diag: Vec<Ratio<i64>>,
    /// Off-diagonal symmetric matrix entries (i, j) with i < j
    pub dirac_off: Vec<(usize, usize, Ratio<i64>)>,
}

impl FiniteSpectralTriple {
    pub fn new(dim: usize, dirac_diag: Vec<Ratio<i64>>, label: impl Into<String>) -> Self {
        Self {
            dim,
            label: label.into(),
            dirac_diag,
            dirac_off: Vec::new(),
        }
    }

    pub fn add_off_diagonal(&mut self, i: usize, j: usize, val: Ratio<i64>) {
        if i != j {
            self.dirac_off.push((i.min(j), i.max(j), val));
        }
    }

    /// Evaluates the Connes distance formula d(p, q) for diagonal states.
    /// d(i, j) = |p_i - p_j| / ||[D, a]||
    pub fn connes_distance_two_point(&self, i: usize, j: usize) -> Result<Ratio<i64>, SpectralError> {
        if i >= self.dim || j >= self.dim {
            return Err(SpectralError::DimensionMismatch);
        }
        let d_diff = (self.dirac_diag[i] - self.dirac_diag[j]).abs();
        if d_diff.is_zero() {
            // If identical Dirac eigenvalue, check off-diagonal coupling
            for &(u, v, w) in &self.dirac_off {
                if (u == i && v == j) || (u == j && v == i) {
                    if !w.is_zero() {
                        return Ok(Ratio::one() / w.abs());
                    }
                }
            }
            return Ok(Ratio::zero());
        }
        Ok(Ratio::one() / d_diff)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn two_point_spectral_distance() {
        let mut st = FiniteSpectralTriple::new(
            2,
            vec![Ratio::from_integer(1), Ratio::from_integer(3)],
            "two_point_space",
        );
        st.add_off_diagonal(0, 1, Ratio::new(1, 2));
        let dist = st.connes_distance_two_point(0, 1).unwrap();
        // |3 - 1| = 2 -> d = 1/2
        assert_eq!(dist, Ratio::new(1, 2));
    }
}
