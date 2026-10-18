//! Exact scalar data associated with a residual. AuthorityEffect: None.
//! This record carries a nonnegative mass; it does not certify a functor,
//! construct a density matrix, or prove the rank of an operator.

use num_rational::BigRational;
use num_traits::Zero;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DensityMatrixFunctorWitness {
    residual_label: String,
    rank_one_weight: BigRational,
}

impl DensityMatrixFunctorWitness {
    pub fn new(residual_label: &str, rank_one_weight: BigRational) -> Result<Self, &'static str> {
        if residual_label.trim().is_empty() {
            return Err("empty residual label");
        }
        if rank_one_weight.denom() <= &0.into() || rank_one_weight < BigRational::zero() {
            return Err("weight must be a defined nonnegative rational");
        }
        Ok(Self {
            residual_label: residual_label.into(),
            rank_one_weight,
        })
    }
    pub fn residual_label(&self) -> &str {
        &self.residual_label
    }
    pub fn rank_one_weight(&self) -> &BigRational {
        &self.rank_one_weight
    }
}
