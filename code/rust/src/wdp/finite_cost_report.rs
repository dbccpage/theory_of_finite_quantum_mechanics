use num_bigint::{BigInt, BigUint};
use num_rational::BigRational;
use num_traits::{One, Zero};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum CostReportError {
    #[error("a nonempty cost window needs at least one report label")]
    NoLabels,
    #[error("cost is outside the declared window")]
    OutsideWindow,
    #[error("report label is unused or outside the declared budget")]
    UnknownLabel,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteCostReport {
    maximum: BigUint,
    width: BigUint,
    used_labels: BigUint,
}

impl FiniteCostReport {
    pub fn new(maximum: BigUint, label_budget: BigUint) -> Result<Self, CostReportError> {
        if label_budget.is_zero() {
            return Err(CostReportError::NoLabels);
        }
        let width = &maximum / label_budget + BigUint::one();
        let used_labels = &maximum / &width + BigUint::one();
        Ok(Self {
            maximum,
            width,
            used_labels,
        })
    }

    pub fn used_labels(&self) -> &BigUint {
        &self.used_labels
    }

    pub fn report(&self, cost: &BigUint) -> Result<BigUint, CostReportError> {
        if cost > &self.maximum {
            return Err(CostReportError::OutsideWindow);
        }
        Ok(cost / &self.width)
    }

    pub fn fiber(&self, label: &BigUint) -> Result<(BigUint, BigUint), CostReportError> {
        if label >= &self.used_labels {
            return Err(CostReportError::UnknownLabel);
        }
        let lo = label * &self.width;
        let hi = (&lo + &self.width - BigUint::one()).min(self.maximum.clone());
        Ok((lo, hi))
    }

    pub fn decode(&self, label: &BigUint) -> Result<BigRational, CostReportError> {
        let (lo, hi) = self.fiber(label)?;
        Ok(BigRational::new(BigInt::from(lo + hi), 2.into()))
    }

    pub fn optimal_error(&self) -> BigRational {
        BigRational::new(BigInt::from(&self.width - BigUint::one()), 2.into())
    }
}
