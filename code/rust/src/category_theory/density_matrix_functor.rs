//! Functor-shaped witness from residuals to rank-one density data.

#[derive(Debug, Clone, PartialEq)]
pub struct DensityMatrixFunctorWitness {
    pub residual_label: String,
    pub rank_one_weight: f64,
}

impl DensityMatrixFunctorWitness {
    pub fn new(residual_label: &str, rank_one_weight: f64) -> Self {
        Self {
            residual_label: residual_label.into(),
            rank_one_weight,
        }
    }
}
