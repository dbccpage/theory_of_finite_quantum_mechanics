

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct KCellDefectCertificate {
    pub k: usize,
    pub nu_sigma: BigRational,
    pub g: BigRational,
    pub t: BigRational,
    pub lower_bound: BigRational,
    pub t_star: BigRational,
    pub is_valid: bool,
    pub authority_effect: String,
}

pub fn eval_short_time_k_cell_bound(
    nu_sigma: &BigRational,
    k: usize,
    g: &BigRational,
    t: &BigRational,
) -> KCellDefectCertificate {
    if k < 2 || nu_sigma <= &BigRational::zero() || g <= &BigRational::zero() {
        return KCellDefectCertificate {
            k,
            nu_sigma: nu_sigma.clone(),
            g: g.clone(),
            t: t.clone(),
            lower_bound: BigRational::zero(),
            t_star: BigRational::zero(),
            is_valid: false,
            authority_effect: "None".to_string(),
        };
    }

    let k_sq = BigInt::from(k) * BigInt::from(k);
    let c_k = BigRational::from(BigInt::from(6)) * BigRational::from(k_sq.clone());
    let denom_factor = BigRational::from(BigInt::from(12)) * BigRational::from(k_sq);

    let g_sq = g * g;
    let t_star = nu_sigma / (&denom_factor * &g_sq);

    let is_valid = t >= &BigRational::zero() && t <= &t_star;

    let term1 = nu_sigma * t;
    let term2 = &c_k * &g_sq * (t * t);
    let lower_bound = term1 - term2;

    KCellDefectCertificate {
        k,
        nu_sigma: nu_sigma.clone(),
        g: g.clone(),
        t: t.clone(),
        lower_bound,
        t_star,
        is_valid,
        authority_effect: "None".to_string(),
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SimplicialBoundaryMatrix {
    pub rows: usize,
    pub cols: usize,
    pub data: Vec<Vec<i64>>,
}

impl SimplicialBoundaryMatrix {
    pub fn new(rows: usize, cols: usize) -> Self {
        Self {
            rows,
            cols,
            data: vec![vec![0; cols]; rows],
        }
    }

    pub fn multiply(&self, other: &SimplicialBoundaryMatrix) -> Option<SimplicialBoundaryMatrix> {
        if self.cols != other.rows
            || self.data.len() != self.rows
            || other.data.len() != other.rows
            || self.data.iter().any(|row| row.len() != self.cols)
            || other.data.iter().any(|row| row.len() != other.cols)
        {
            return None;
        }
        let mut result = SimplicialBoundaryMatrix::new(self.rows, other.cols);
        for i in 0..self.rows {
            for j in 0..other.cols {
                let mut sum = 0i64;
                for k in 0..self.cols {
                    sum = sum.checked_add(self.data[i][k].checked_mul(other.data[k][j])?)?;
                }
                result.data[i][j] = sum;
            }
        }
        Some(result)
    }

    pub fn is_zero(&self) -> bool {
        self.data.iter().all(|row| row.iter().all(|&x| x == 0))
    }
}

pub fn triangle_simplex_boundaries() -> (SimplicialBoundaryMatrix, SimplicialBoundaryMatrix) {
    let mut b2 = SimplicialBoundaryMatrix::new(3, 1);
    b2.data[0][0] = 1;
    b2.data[1][0] = -1;
    b2.data[2][0] = 1;

    let mut b1 = SimplicialBoundaryMatrix::new(3, 3);
    b1.data[1][0] = -1;
    b1.data[2][0] = 1;

    b1.data[0][1] = -1;
    b1.data[2][1] = 1;

    b1.data[0][2] = -1;
    b1.data[1][2] = 1;

    (b1, b2)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_exact_rational_k_cell_defect_bound() {
        let nu = BigRational::from(BigInt::from(2));
        let k = 3;
        let g = BigRational::from(BigInt::from(1));

        let t = BigRational::new(BigInt::from(1), BigInt::from(200));

        let cert = eval_short_time_k_cell_bound(&nu, k, &g, &t);

        assert_eq!(
            cert.t_star,
            BigRational::new(BigInt::from(1), BigInt::from(54))
        );
        assert!(cert.is_valid);

        assert_eq!(
            cert.lower_bound,
            BigRational::new(BigInt::from(173), BigInt::from(20000))
        );
        assert!(cert.lower_bound > BigRational::zero());
        assert_eq!(cert.authority_effect, "None");
    }

    #[test]
    fn test_simplicial_boundary_nilpotence() {
        let (b1, b2) = triangle_simplex_boundaries();
        let prod = b1.multiply(&b2).expect("Matrix dimensions must match");
        assert_eq!(prod.rows, 3);
        assert_eq!(prod.cols, 1);
        assert!(
            prod.is_zero(),
            "partial_1 @ partial_2 must be identically zero"
        );
    }
}
