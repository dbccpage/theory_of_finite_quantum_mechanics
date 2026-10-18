
use num_rational::Ratio;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum CdtError {
    NegativeSimplexCount,
    BoundaryMismatch,
    NonPositiveDeficit,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CdtSlab {
    pub time_index: usize,
    pub count_space_like_edges: usize,
    pub count_time_like_edges: usize,
    pub count_d1: usize,
    pub count_1d: usize,
}

impl CdtSlab {
    pub fn new(time_index: usize, count_d1: usize, count_1d: usize) -> Self {
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

    pub fn volume(&self) -> usize {
        self.count_d1 + self.count_1d
    }

    pub fn bare_action(&self, lambda: Ratio<i64>, kappa: Ratio<i64>) -> Result<Ratio<i64>, CdtError> {
        let vol = Ratio::from_integer(self.volume() as i64);
        let n_edges = Ratio::from_integer((self.count_space_like_edges + self.count_time_like_edges) as i64);
        Ok(kappa * vol - lambda * n_edges)
    }

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
        assert_eq!(act, Ratio::from_integer(10));
    }
}
