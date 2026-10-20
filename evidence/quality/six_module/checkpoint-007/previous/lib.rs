
extern crate self as omega_fusion_categories;
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

use num_rational::Ratio;
use num_traits::Zero;

pub fn verify_fusion_global_dimension(dims_squared: &[Ratio<i64>], total_dim_sq: Ratio<i64>) -> bool {
    let sum: Ratio<i64> = dims_squared.iter().copied().sum();
    sum == total_dim_sq && sum > Ratio::zero()
}

#[cfg(test)]
mod fusion_tests {
    use super::*;

    #[test]
    fn test_fibonacci_dimension() {
        let d = vec![Ratio::from_integer(1), Ratio::from_integer(4)];
        assert!(verify_fusion_global_dimension(&d, Ratio::from_integer(5)));
    }
}
