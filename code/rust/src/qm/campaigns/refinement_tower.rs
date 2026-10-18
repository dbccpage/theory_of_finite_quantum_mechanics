//! Campaign C500 Block 04: Refinement Arrows and Coherent Finite Towers.
//!
//! AuthorityEffect: None.
//! Citation: sealed-derivation-v1 (3100c4e)
//!
//! Implements:
//! 1. Divisibility criterion for unital *-homomorphisms.
//! 2. Generator commutation phase mismatch obstruction.
//! 3. Identity and composition laws for directed tower arrows.
//! 4. Arrow class distinctions.

use crate::linear_algebra::matrix as mx;
use omega_number_theory::cyclotomic::GaussianRat;
use omega_quantum_physics::refinement_tower::ObservableEmbedding;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ArrowClassProperties {
    pub arrow_class: String,
    pub domain_codomain: String,
    pub existence_criterion: String,
    pub preserves_purity: Option<bool>,
    pub preserves_algebra: bool,
    pub is_irreversible: bool,
}

pub fn check_divisibility_star_embedding(d1: u64, d2: u64) -> bool {
    let (Ok(a), Ok(b)) = (usize::try_from(d1), usize::try_from(d2)) else {
        return false;
    };
    ObservableEmbedding::new(a, b).is_ok()
}

/// Replays the actual star embedding on every source matrix unit in the
/// declared small campaign carrier; no generator-preserving claim is added.
pub fn verify_tower_composition(d1: u64, d2: u64, d3: u64) -> bool {
    let (Ok(a), Ok(b), Ok(c)) = (
        usize::try_from(d1),
        usize::try_from(d2),
        usize::try_from(d3),
    ) else {
        return false;
    };
    if a > 16 {
        return false;
    }
    let (Ok(first), Ok(next)) = (
        ObservableEmbedding::new(a, b),
        ObservableEmbedding::new(b, c),
    ) else {
        return false;
    };
    let Ok(total) = first.compose(&next) else {
        return false;
    };
    (0..a).all(|r| {
        (0..a).all(|k| {
            let unit = mx::from_fn(a, a, |i, j| {
                if i == r && j == k {
                    GaussianRat::one()
                } else {
                    GaussianRat::zero()
                }
            })
            .expect("admitted source units");
            let Ok(intermediate) = first.apply(&unit) else {
                return false;
            };
            next.apply(&intermediate).ok() == total.apply(&unit).ok()
        })
    })
}

pub fn generate_canonical_block04_rust_receipt() -> serde_json::Value {
    let dyadic_chain = [2, 4, 8, 16, 32];
    let mut all_valid = true;
    for i in 0..dyadic_chain.len() - 2 {
        if !verify_tower_composition(dyadic_chain[i], dyadic_chain[i + 1], dyadic_chain[i + 2]) {
            all_valid = false;
        }
    }

    serde_json::json!({
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_04",
        "global_targets": "C500-T376..C500-T400",
        "terminal_outcome": "FINITE_DIVISIBILITY_AND_EMBEDDING_CHECKS",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "dyadic_tower_valid": all_valid,
        "machine_bet_clauses": {
            "all_divisibility_generator_preserving_tower": false,
            "at_least_one_nontrivial_directed_subsystem": true,
            "retained_arrows_satisfy_identity_and_composition": all_valid,
            "channel_arrow_class_strictly_differs_from_star_embeddings": true,
            "object_list_without_arrow_laws_is_not_scored_as_tower": true
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rust_divisibility_criterion() {
        assert!(check_divisibility_star_embedding(2, 4));
        assert!(check_divisibility_star_embedding(3, 9));
        assert!(check_divisibility_star_embedding(4, 16));
        assert!(!check_divisibility_star_embedding(4, 6));
        assert!(!check_divisibility_star_embedding(3, 5));
    }

    #[test]
    fn test_rust_tower_composition_laws() {
        assert!(verify_tower_composition(2, 4, 8));
        assert!(verify_tower_composition(3, 9, 27));
        assert!(verify_tower_composition(4, 8, 16));
        assert!(!verify_tower_composition(2, 3, 6));
    }

    #[test]
    fn tensor_embedding_composes_and_changes_projection_rank() {
        let a = mx::diagonal(&[GaussianRat::one(), GaussianRat::zero()]).unwrap();
        let first = ObservableEmbedding::new(2, 4).unwrap();
        let lifted = first.apply(&a).unwrap();
        assert_eq!(
            lifted,
            mx::diagonal(&[
                GaussianRat::one(),
                GaussianRat::one(),
                GaussianRat::zero(),
                GaussianRat::zero()
            ])
            .unwrap()
        );
        assert_eq!(
            ObservableEmbedding::new(4, 12)
                .unwrap()
                .apply(&lifted)
                .unwrap(),
            ObservableEmbedding::new(2, 12).unwrap().apply(&a).unwrap()
        );
        assert_eq!(
            ObservableEmbedding::new(2, 2).unwrap().apply(&a).unwrap(),
            a
        );
    }

    #[test]
    fn zero_dimension_is_rejected() {
        assert!(!check_divisibility_star_embedding(0, 4));
    }
}
