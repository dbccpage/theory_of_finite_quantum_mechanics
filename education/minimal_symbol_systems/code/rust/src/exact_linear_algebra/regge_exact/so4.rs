//! Matrices in `SO(4, Q)`: `Mᵀ M = I` and `det M = 1`, checked entrywise over `Q`.
//!
//! Storage is row-major and acts on column vectors. The induced action on
//! `∧² Q^4` is `c'_ab = Σ_{i<j} c_ij (R_ai R_bj - R_bi R_aj)`.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use super::bivector::Bivector4;
use super::gaussian;
use super::ExactError;
use num_rational::BigRational;
use num_traits::{One, Zero};

const PAIRS: [(usize, usize); 6] = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)];

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct So4 {
    pub m: [[BigRational; 4]; 4],
}

impl So4 {
    pub fn identity() -> Self {
        let mut m = std::array::from_fn(|_| std::array::from_fn(|_| BigRational::zero()));
        for index in 0..4 {
            m[index][index] = BigRational::one();
        }
        Self { m }
    }

    pub fn try_new(m: [[BigRational; 4]; 4]) -> Result<Self, ExactError> {
        for column in 0..4 {
            for row in 0..4 {
                let mut gram = BigRational::zero();
                for k in 0..4 {
                    gram += &m[k][column] * &m[k][row];
                }
                let expected = if column == row {
                    BigRational::one()
                } else {
                    BigRational::zero()
                };
                if gram != expected {
                    return Err(ExactError::NotOrthogonal);
                }
            }
        }
        let det = gaussian::determinant(&m)?;
        if det != BigRational::one() {
            return Err(ExactError::NotSpecial);
        }
        Ok(Self { m })
    }

    pub fn mul(&self, other: &Self) -> Self {
        let mut m = std::array::from_fn(|_| std::array::from_fn(|_| BigRational::zero()));
        for row in 0..4 {
            for column in 0..4 {
                let mut sum = BigRational::zero();
                for k in 0..4 {
                    sum += &self.m[row][k] * &other.m[k][column];
                }
                m[row][column] = sum;
            }
        }
        Self { m }
    }

    pub fn transpose(&self) -> Self {
        let mut m = std::array::from_fn(|_| std::array::from_fn(|_| BigRational::zero()));
        for row in 0..4 {
            for column in 0..4 {
                m[row][column] = self.m[column][row].clone();
            }
        }
        Self { m }
    }

    pub fn act_vector(&self, v: &[BigRational; 4]) -> [BigRational; 4] {
        std::array::from_fn(|row| {
            let mut sum = BigRational::zero();
            for column in 0..4 {
                sum += &self.m[row][column] * &v[column];
            }
            sum
        })
    }

    pub fn act_bivector(&self, bivector: &Bivector4) -> Bivector4 {
        let mut image = [
            BigRational::zero(),
            BigRational::zero(),
            BigRational::zero(),
            BigRational::zero(),
            BigRational::zero(),
            BigRational::zero(),
        ];
        for (out_index, (a, b)) in PAIRS.iter().copied().enumerate() {
            let mut sum = BigRational::zero();
            for (in_index, (i, j)) in PAIRS.iter().copied().enumerate() {
                let coefficient =
                    &self.m[a][i] * &self.m[b][j] - &self.m[b][i] * &self.m[a][j];
                sum += &bivector.c[in_index] * &coefficient;
            }
            image[out_index] = sum;
        }
        Bivector4::from_components(image)
    }

    pub fn frobenius_defect_squared(&self) -> BigRational {
        let mut sum = BigRational::zero();
        for row in 0..4 {
            for column in 0..4 {
                let delta = if row == column {
                    BigRational::one()
                } else {
                    BigRational::zero()
                };
                let diff = &self.m[row][column] - delta;
                sum += &diff * &diff;
            }
        }
        sum
    }

    pub fn is_identity(&self) -> bool {
        self.m.iter().enumerate().all(|(row, entries)| {
            entries.iter().enumerate().all(|(column, entry)| {
                let expected = if row == column {
                    BigRational::one()
                } else {
                    BigRational::zero()
                };
                entry == &expected
            })
        })
    }
}
