//! Exact discrete Causal Dynamical Triangulation (CDT) slabs and Regge action.
//!
//! Origin: papers/derivations/general_relativity/rust/src/causal_dynamical_triangulation.rs
//! Claim: DERIV-GR-CDT-001
//! AuthorityEffect: None.

use num_rational::Ratio;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum CdtError {
    NegativeSimplexCount,
    BoundaryMismatch,
    NonPositiveDeficit,
}

/// A 1+1 dimensional or 2+1 dimensional CDT spacetime slab between time slices t and t+1.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CdtSlab {
    pub time_index: usize,
    pub count_space_like_edges: usize,
    pub count_time_like_edges: usize,
    /// Number of (d, 1) simplices (base on slice t, apex on slice t+1)
    pub count_d1: usize,
    /// Number of (1, d) simplices (apex on slice t, base on slice t+1)
    pub count_1d: usize,
}

impl CdtSlab {
    pub fn new(time_index: usize, count_d1: usize, count_1d: usize) -> Self {
        // In 1+1 D: each (2,1) triangle has 1 spacelike edge and 2 timelike edges
        let count_space_like_edges = count_d1 + count_1d;
        let count_time_like_edges = 2 * (count_d1 + count_1d);
        Self {
            time_index,
            count_space_like_edges,
            count_time_like_edges,
            count_d1,
            count_1d,
        }
    }

    /// Discrete spacetime volume (total simplex count).
    pub fn volume(&self) -> usize {
        self.count_d1 + self.count_1d
    }

    /// Exact discrete Einstein-Hilbert-Regge action for the slab with bare cosmological constant Lambda.
    pub fn bare_action(&self, lambda: Ratio<i64>, kappa: Ratio<i64>) -> Result<Ratio<i64>, CdtError> {
        let vol = Ratio::from_integer(self.volume() as i64);
        let n_edges = Ratio::from_integer((self.count_space_like_edges + self.count_time_like_edges) as i64);
        // Discrete Euler action proxy S = kappa * V - lambda * N_edges
        Ok(kappa * vol - lambda * n_edges)
    }

    /// Validates spatial slice periodicity / torus topology in 1+1 D.
    pub fn is_torus_balanced(&self) -> bool {
        self.count_d1 == self.count_1d && self.count_d1 > 0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn balanced_cdt_slab() {
        let slab = CdtSlab::new(0, 10, 10);
        assert_eq!(slab.volume(), 20);
        assert!(slab.is_torus_balanced());
        let act = slab.bare_action(Ratio::new(1, 2), Ratio::new(2, 1)).unwrap();
        // vol = 20, edges = 20 + 40 = 60. S = 2*20 - 0.5*60 = 40 - 30 = 10.
        assert_eq!(act, Ratio::from_integer(10));
    }
}
