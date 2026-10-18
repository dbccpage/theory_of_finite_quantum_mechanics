
extern crate self as omega_finite_probability;
pub mod bell_joint_extension;
pub mod classical_instrument;
pub mod error;
pub mod finite_set;
pub mod joint_table;
pub mod log_form;
pub mod majorization;
pub mod markov_chain;
pub mod paired_tests;
pub mod simplex;
pub mod stochastic_map;

#[cfg(test)]
mod test_support;

pub mod finite_valuation;

pub mod local_deterministic;
pub mod marginal_compatibility;
pub mod signed_representation;

use num_rational::Ratio;
use num_traits::Zero;

pub fn verify_distribution_sum(probs: &[Ratio<i64>]) -> bool {
    let mut sum = Ratio::zero();
    for p in probs {
        if *p < Ratio::zero() {
            return false;
        }
        sum += *p;
    }
    sum == Ratio::from_integer(1)
}

#[cfg(test)]
mod prob_tests {
    use super::*;

    #[test]
    fn test_verify_distribution() {
        let dist = vec![Ratio::new(1, 3), Ratio::new(2, 3)];
        assert!(verify_distribution_sum(&dist));
    }
}
