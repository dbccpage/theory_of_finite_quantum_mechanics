//! `omega_finite_probability` -- exact finite probability for the Omega Engine.
//!
//! Finite probability is pure mathematics, so it lives below the physics and the programme
//! crates that use it. Every quantity is exact: masses, kernels, tables and majorization
//! data are `BigRational`; entropies are exact rational combinations of logarithms of
//! primes; there is no floating point and no tolerance anywhere. Failures are typed values
//! and no function panics on caller data.
//!
//! | module | content |
//! |---|---|
//! | [`classical_instrument`] | finite classical instruments (composition, coarse-graining, adaptive control) and conditional boxes with no-signalling and hidden-variable questions kept apart |
//! | [`error`] | the refusals of the finite-set, simplex and kernel layer |
//! | [`finite_set`] | the carrier `Fin n` |
//! | [`joint_table`] | joint tables: marginals, conditionals, independence decided several independent ways, couplings and Frechet bounds, local maps |
//! | [`log_form`] | entropies as exact rational combinations of logarithms of primes: Shannon, relative, Renyi, mutual; certified enclosures and ordering |
//! | [`majorization`] | the majorization preorder on probability vectors, thermal ladders, Nielsen's criterion, T-transform chains |
//! | [`markov_chain`] | finite chains: classes, recurrence, period, stationary laws, absorption, hitting and return times, exact mixing |
//! | [`simplex`] | probability simplices: events, expectations, total variation, products, mixtures |
//! | [`stochastic_map`] | row-stochastic maps: the category of finite kernels, its monoidal (Markov) structure, Bayesian inversion, the Dobrushin coefficient |
//!
//! Exact linear algebra (rank, kernel, `solve_in_image`) is `omega_linear_algebra`'s; the
//! exact scalar is `omega_number_theory`'s. This crate owns the probabilistic structure built
//! on them and carries no private copy of either.
//!
//! AuthorityEffect: None.

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

/// Verifies that a rational probability distribution sums to exactly 1.
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
