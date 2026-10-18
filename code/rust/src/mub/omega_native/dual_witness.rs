//! Factored rational PSD witness shared by the degree 2, 4, 6, and 8 diagnostics.
//!
//! `W = sum_k weight_k v_k v_k^T`. Every weight is strictly positive, and
//! `trace_inner` requires a symmetric matrix of the witness dimension.

use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct DualWitnessRational {
    pub dim: usize,
    pub num_modes: usize,
    pub vectors: Vec<Vec<BigRational>>,
    pub weights: Vec<BigRational>,
}

impl DualWitnessRational {
    pub fn new(
        dim: usize,
        num_modes: usize,
        vectors: Vec<Vec<BigRational>>,
        weights: Vec<BigRational>,
    ) -> Result<Self, String> {
        let witness = Self {
            dim,
            num_modes,
            vectors,
            weights,
        };
        witness.validate()?;
        Ok(witness)
    }

    pub fn is_valid(&self) -> bool {
        self.validate().is_ok()
    }

    fn validate(&self) -> Result<(), String> {
        if self.dim == 0
            || self.num_modes == 0
            || self.vectors.len() != self.num_modes
            || self.weights.len() != self.num_modes
            || self.vectors.iter().any(|vector| vector.len() != self.dim)
            || self.weights.iter().any(|weight| weight <= &BigRational::zero())
        {
            return Err("Invalid rational PSD witness".into());
        }
        Ok(())
    }

    pub fn to_full_matrix(&self) -> Result<Vec<Vec<BigRational>>, String> {
        self.validate()?;
        let mut matrix = vec![vec![BigRational::zero(); self.dim]; self.dim];
        for mode in 0..self.num_modes {
            let vector = &self.vectors[mode];
            let weight = &self.weights[mode];
            for row in 0..self.dim {
                for column in 0..self.dim {
                    matrix[row][column] += weight * &vector[row] * &vector[column];
                }
            }
        }
        Ok(matrix)
    }

    pub fn trace_inner(&self, matrix: &[Vec<BigRational>]) -> Result<BigRational, String> {
        self.validate()?;
        if matrix.len() != self.dim || matrix.iter().any(|row| row.len() != self.dim) {
            return Err(format!(
                "Matrix dimension must match witness dimension {}",
                self.dim
            ));
        }
        for row in 0..self.dim {
            for column in 0..self.dim {
                if matrix[row][column] != matrix[column][row] {
                    return Err("Matrix must be symmetric".into());
                }
            }
        }
        let mut total = BigRational::zero();
        for mode in 0..self.num_modes {
            let vector = &self.vectors[mode];
            let weight = &self.weights[mode];
            let mut quadratic = BigRational::zero();
            for row in 0..self.dim {
                for column in 0..self.dim {
                    quadratic += &vector[row] * &matrix[row][column] * &vector[column];
                }
            }
            total += weight * quadratic;
        }
        Ok(total)
    }
}
