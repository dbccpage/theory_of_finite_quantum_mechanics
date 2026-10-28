extern crate self as tfqm_fusion_categories;
pub mod braid_group;
pub mod braided;
pub mod catalog;
pub mod error;
pub mod fusion_category;
pub mod fusion_ring;
pub mod modular;
pub mod scalar;
pub mod su2_level;
pub mod yang_baxter;

use num_bigint::BigInt;
use num_rational::{BigRational, Ratio};
use num_traits::Zero;

/// Check a rational sum against a strictly positive total using exact arithmetic.
/// This aggregate check does not certify each entry as a physical squared
/// dimension. Raw ratios with a zero denominator are refused.
pub fn verify_fusion_global_dimension(
    dims_squared: &[Ratio<i64>],
    total_dim_sq: Ratio<i64>,
) -> bool {
    if *total_dim_sq.denom() == 0 {
        return false;
    }
    let total = BigRational::new(
        BigInt::from(*total_dim_sq.numer()),
        BigInt::from(*total_dim_sq.denom()),
    );
    if total <= BigRational::zero() {
        return false;
    }
    let mut sum = BigRational::zero();
    for value in dims_squared {
        if *value.denom() == 0 {
            return false;
        }
        sum += BigRational::new(BigInt::from(*value.numer()), BigInt::from(*value.denom()));
    }
    sum == total
}

#[cfg(test)]
mod fusion_tests {
    use super::*;

    #[test]
    fn test_positive_rational_aggregate() {
        let d = vec![Ratio::from_integer(1), Ratio::from_integer(4)];
        assert!(verify_fusion_global_dimension(&d, Ratio::from_integer(5)));
    }
}
