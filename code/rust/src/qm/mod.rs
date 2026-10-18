//! Exact finite quantum mechanical states, density operators, observables, and campaigns.

use crate::linear_algebra::{ExactMatrix, GaussianRational, MatrixError, Q};
use crate::crate::crate::crate::linear_algebra::scalars::{q, Semiring};
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum QmError {
    #[error("Dimension mismatch: {0}")]
    DimensionMismatch(String),
    #[error("Matrix error: {0}")]
    Matrix(#[from] MatrixError),
    #[error("State normalization violation: trace is not 1")]
    NormalizationViolation,
    #[error("Hermiticity violation: operator is not self-adjoint")]
    HermiticityViolation,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DensityOperator {
    dim: usize,
    matrix: ExactMatrix<GaussianRational>,
}

impl DensityOperator {
    pub fn new(matrix: ExactMatrix<GaussianRational>) -> Result<Self, QmError> {
        let (rows, cols) = matrix.shape();
        if rows != cols {
            return Err(QmError::DimensionMismatch(format!("Density operator must be square, got {}x{}", rows, cols)));
        }
        if !matrix.is_hermitian()? {
            return Err(QmError::HermiticityViolation);
        }
        let mut tr_real = q(0);
        let mut tr_imag = q(0);
        for i in 0..rows {
            let elem = matrix.get(i, i)?;
            tr_real = tr_real + &elem.real;
            tr_imag = tr_imag + &elem.imag;
        }
        if tr_real != q(1) || tr_imag != q(0) {
            return Err(QmError::NormalizationViolation);
        }
        Ok(Self { dim: rows, matrix })
    }

    pub fn dimension(&self) -> usize {
        self.dim
    }

    pub fn matrix(&self) -> &ExactMatrix<GaussianRational> {
        &self.matrix
    }

    pub fn expectation(&self, observable: &ExactMatrix<GaussianRational>) -> Result<GaussianRational, QmError> {
        if observable.shape() != (self.dim, self.dim) {
            return Err(QmError::DimensionMismatch(format!("Shape mismatch {:?} vs {}", observable.shape(), self.dim)));
        }
        let prod = self.matrix.mul(observable)?;
        let mut tr = GaussianRational::zero();
        for i in 0..self.dim {
            let elem = prod.get(i, i)?;
            tr = tr.add(elem);
        }
        Ok(tr)
    }

    pub fn purity(&self) -> Result<Q, QmError> {
        let sq = self.matrix.mul(&self.matrix)?;
        let mut tr = q(0);
        for i in 0..self.dim {
            let elem = sq.get(i, i)?;
            tr = tr + &elem.real;
        }
        Ok(tr)
    }
}

pub mod domain;
pub mod entrypoints;
pub mod campaigns;
pub mod entropy_solver;
pub mod entropy_bounds;
pub mod finite_witness;
pub mod causal_prices;
pub mod group_param;
pub mod legacy_suites;
pub mod quantum_packet;
pub mod observer_functor;
pub mod obstruction_calc;
pub mod finite_spinfoam;
pub mod evidence_routes;
pub mod packet_protocol;
pub mod report_fiber;
pub mod simplicial_grav;
pub mod suites;
pub mod tower_walk;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_qubit_pure_state_and_pauli_expectation() {
        let rows = vec![
            vec![GaussianRational::one(), GaussianRational::zero()],
            vec![GaussianRational::zero(), GaussianRational::zero()],
        ];
        let mat = ExactMatrix::from_rows(rows).unwrap();
        let rho = DensityOperator::new(mat).unwrap();
        assert_eq!(rho.purity().unwrap(), q(1));

        let sigma_z = ExactMatrix::from_rows(vec![
            vec![GaussianRational::one(), GaussianRational::zero()],
            vec![GaussianRational::zero(), GaussianRational::new(q(-1), q(0))],
        ]).unwrap();

        let exp_z = rho.expectation(&sigma_z).unwrap();
        assert_eq!(exp_z, GaussianRational::one());
    }
}
