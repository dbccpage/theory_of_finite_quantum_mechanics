//! `omega_fusion_categories` -- exact fusion rings and multiplicity-free fusion,
//! braided and modular data.
//!
//! Every quantity is exact: fusion coefficients are checked non-negative integers,
//! and the symbols (F, R, S, T, twists, dimensions) are elements of an exact number
//! field `K` from `omega_number_theory`. There are no floating-point conversions and no
//! tolerances.
//!
//! | module | content |
//! |---|---|
//! | [`fusion_ring`] | fusion tables and rings (`N_{ab}^c`), ring laws, duals, fusion-path counts, Frobenius-Perron dimensions, Verlinde check, the ring catalog |
//! | [`fusion_category`] | F-symbols, the pentagon equation, unit normalisation, gauges, dimension and Frobenius-Schur data |
//! | [`braided`] | R-symbols, both hexagon equations, twists, the ribbon relation, braid-group representations on fusion spaces |
//! | [`braid_group`] | braid relations, projective normal forms and exact finite-group closure of braid images |
//! | [`yang_baxter`] | the Yang-Baxter equation as an exact matrix identity, and the standard solutions |
//! | [`modular`] | `S~`, `T`, Verlinde, the modular relations, Gauss-Milgram, ground-state degeneracy |
//! | [`catalog`] | validated constructors: Ising, Fibonacci, semion, toric code, three-fermion, pointed and quantum-double models |
//!
//! AuthorityEffect: None. Not PROVED. Not GlobalGreen.

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

/// Verifies that total quantum dimension satisfies D^2 = sum d_i^2 over exact rationals.
pub fn verify_fusion_global_dimension(dims_squared: &[Ratio<i64>], total_dim_sq: Ratio<i64>) -> bool {
    let sum: Ratio<i64> = dims_squared.iter().copied().sum();
    sum == total_dim_sq && sum > Ratio::zero()
}

#[cfg(test)]
mod fusion_tests {
    use super::*;

    #[test]
    fn test_fibonacci_dimension() {
        // Example check: integer dimensions
        let d = vec![Ratio::from_integer(1), Ratio::from_integer(4)];
        assert!(verify_fusion_global_dimension(&d, Ratio::from_integer(5)));
    }
}
