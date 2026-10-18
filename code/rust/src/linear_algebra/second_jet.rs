//! Exact value/first/second derivative products of square matrix curves.
//! Components are derivatives at zero, not Taylor coefficients.
//! AuthorityEffect: None.

use crate::linear_algebra::basic_matrix::{BasicMatrix, OperationLimits};
use crate::linear_algebra::{
    charge, element_count, matrix as mx, plus, require_same_shape, require_square, times,
    ExactFieldError,
};
use crate::crate::crate::crate::linear_algebra::scalars::{ExactRing, Field};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MatrixJet2<F> {
    derivatives: [BasicMatrix<F>; 3],
}

impl<F: Field + ExactRing> MatrixJet2<F> {
    pub fn new(derivatives: [BasicMatrix<F>; 3]) -> Result<Self, ExactFieldError> {
        require_square("matrix jet", &derivatives[0])?;
        require_same_shape("matrix jet", &derivatives[0], &derivatives[1])?;
        require_same_shape("matrix jet", &derivatives[0], &derivatives[2])?;
        Ok(Self { derivatives })
    }

    pub fn derivatives(&self) -> [&BasicMatrix<F>; 3] {
        [
            &self.derivatives[0],
            &self.derivatives[1],
            &self.derivatives[2],
        ]
    }

    pub fn product(&self, right: &Self) -> Result<Self, ExactFieldError> {
        self.product_with_limits(right, OperationLimits::UNLIMITED)
    }

    /// Whole-product preflight: six matrix products, three additions, one scale.
    /// Each matrix allocation has n^2 elements; scalar calls <=12n^3+4n^2+1.
    pub fn product_with_limits(
        &self,
        right: &Self,
        limits: OperationLimits,
    ) -> Result<Self, ExactFieldError> {
        require_same_shape("jet product", &self.derivatives[0], &right.derivatives[0])?;
        let n = self.derivatives[0].rows();
        let n2 = element_count(n, n)?;
        let cost = plus(plus(times(12, times(n2, n)?)?, times(4, n2)?)?, 1)?;
        charge(limits, n2, cost)?;
        let [a0, a1, a2] = self.derivatives();
        let [b0, b1, b2] = right.derivatives();
        let two = F::one().add(&F::one());
        Self::new([
            mx::multiply(a0, b0)?,
            mx::add(&mx::multiply(a1, b0)?, &mx::multiply(a0, b1)?)?,
            mx::add(
                &mx::add(
                    &mx::multiply(a2, b0)?,
                    &mx::scale(&mx::multiply(a1, b1)?, &two)?,
                )?,
                &mx::multiply(a0, b2)?,
            )?,
        ])
    }
}
