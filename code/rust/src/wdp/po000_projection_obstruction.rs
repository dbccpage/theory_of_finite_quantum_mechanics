//! PO-000 declared projection diagnostics, bound to their complete source data.
//! This wrapper makes no finite-time exponential or operational-QM assertion.
//! Exact matrix arithmetic and leakage calculations live in their math owners.

use crate::types::AuthorityEffect;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use num_rational::BigRational;
use omega_functional::projection_leakage::{
    evaluate_projection_leakage, ProjectionLeakage, ProjectionLeakageError,
};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredProjectionProblem {
    pub first: BasicMatrix<BigRational>,
    pub second: BasicMatrix<BigRational>,
    pub generator: BasicMatrix<BigRational>,
    pub elapsed: BigRational,
    pub state: Vec<BigRational>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProjectionObstructionReceipt {
    pub problem: DeclaredProjectionProblem,
    pub diagnostic: ProjectionLeakage,
    pub authority_effect: AuthorityEffect,
}

impl DeclaredProjectionProblem {
    pub fn evaluate(&self) -> Result<ProjectionObstructionReceipt, ProjectionLeakageError> {
        let diagnostic = evaluate_projection_leakage(
            &self.first,
            &self.second,
            &self.generator,
            &self.elapsed,
            &self.state,
        )?;
        Ok(ProjectionObstructionReceipt {
            problem: self.clone(),
            diagnostic,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn verify(
        &self,
        candidate: &ProjectionObstructionReceipt,
    ) -> Result<bool, ProjectionLeakageError> {
        Ok(*candidate == self.evaluate()?)
    }
}
