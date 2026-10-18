
use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum TetradError {
    SingularTetrad,
    DimensionMismatch,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiscreteTetrad {
    pub dim: usize,
    pub entries: Vec<Vec<Ratio<i64>>>,
}

impl DiscreteTetrad {
    pub fn identity(dim: usize) -> Self {
        let mut entries = vec![vec![Ratio::zero(); dim]; dim];
        for i in 0..dim {
            entries[i][i] = Ratio::one();
        }
        Self { dim, entries }
    }

    pub fn new(entries: Vec<Vec<Ratio<i64>>>) -> Result<Self, TetradError> {
        let dim = entries.len();
        for row in &entries {
            if row.len() != dim {
                return Err(TetradError::DimensionMismatch);
            }
        }
        Ok(Self { dim, entries })
    }

    pub fn reconstruct_metric(&self) -> Vec<Vec<Ratio<i64>>> {
        let n = self.dim;
        let mut g = vec![vec![Ratio::zero(); n]; n];
        let eta = |a: usize| if a == 0 { -Ratio::one() } else { Ratio::one() };

        for mu in 0..n {
            for nu in 0..n {
                let mut sum = Ratio::zero();
                for a in 0..n {
                    sum += self.entries[a][mu] * self.entries[a][nu] * eta(a);
                }
                g[mu][nu] = sum;
            }
        }
        g
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tetrad_metric_recovery() {
        let tetrad = DiscreteTetrad::identity(4);
        let g = tetrad.reconstruct_metric();
        assert_eq!(g[0][0], -Ratio::one());
        assert_eq!(g[1][1], Ratio::one());
        assert_eq!(g[2][2], Ratio::one());
        assert_eq!(g[3][3], Ratio::one());
        assert_eq!(g[0][1], Ratio::zero());
    }
}
