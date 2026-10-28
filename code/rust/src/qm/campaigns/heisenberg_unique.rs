use engine_lie_theory::heisenberg::FiniteHeisenberg;
#[cfg(test)]
use engine_lie_theory::heisenberg::HeisenbergElement;
use serde::{Deserialize, Serialize};
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CentralCharacterCensus {
    pub prime: u64,
    pub group_order: u64,
    pub center_order: u64,
    pub num_conjugacy_classes: u64,
    pub num_1d_irreps: u64,
    pub num_higher_irreps: u64,
    pub higher_irrep_dimension: u64,
    pub sum_of_squares: u64,
    pub uniqueness_per_nontrivial_character: bool,
    pub classification_evidence: String,
}

pub fn compute_central_character_census(p: u64) -> CentralCharacterCensus {
    let _group = FiniteHeisenberg::new(p).expect("validated finite prime fixture");
    let group_order = p
        .checked_mul(p)
        .and_then(|v| v.checked_mul(p))
        .expect("Census group order exceeds u64 range");
    let num_1d = p * p;
    let num_higher = p - 1;
    let sum_sq = num_1d + num_higher * (p * p);

    CentralCharacterCensus {
        prime: p,
        group_order,
        center_order: p,
        num_conjugacy_classes: p * p + p - 1,
        num_1d_irreps: num_1d,
        num_higher_irreps: num_higher,
        higher_irrep_dimension: p,
        sum_of_squares: sum_sq,
        uniqueness_per_nontrivial_character: true,
        classification_evidence: "DECLARED_THEOREM_INPUT_NOT_PROVED_HERE".into(),
    }
}

pub fn generate_canonical_block03_rust_receipt() -> serde_json::Value {
    let census: Vec<CentralCharacterCensus> = [3, 5, 7, 11]
        .iter()
        .map(|&p| compute_central_character_census(p))
        .collect();
    let representation_law_checks: Vec<_> = [3, 5]
        .into_iter()
        .flat_map(|p| {
            (0..p).map(move |c| {
                serde_json::json!({"prime": p, "central_character": c,
            "all_pairs_and_basis": true, "passed": FiniteHeisenberg::new(p).expect("prime fixture").check_representation_law(c).expect("small exhaustive fixture")})
            })
        })
        .collect();

    serde_json::json!({
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_03",
        "global_targets": "C500-T351..C500-T375",
        "terminal_outcome": "FINITE_REPRESENTATION_CHECKS_WITH_DECLARED_CENSUS",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "central_character_census": census,
        "representation_law_checks": representation_law_checks,
        "open_obligations": ["irreducibility", "intertwiner uniqueness", "general classification proof or exact theorem import"],
        "machine_bet_clauses": {
            "odd_prime_fixed_character_uniqueness": "DECLARED_THEOREM_INPUT_OPEN_VERIFICATION",
            "nontrivial_central_character_is_required": true,
            "characteristic_two_handled_separately": false,
            "composite_modulus_status": "SPLITS_BY_BASE_RING",
            "cited_theorem_hypotheses_are_machine_mapped": false
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    fn heisenberg_multiply(
        g: HeisenbergElement,
        h: HeisenbergElement,
        p: u64,
    ) -> HeisenbergElement {
        FiniteHeisenberg::new(p).unwrap().multiply(g, h).unwrap()
    }
    fn check_schroedinger_representation_law(p: u64, c: u64) -> bool {
        FiniteHeisenberg::new(p)
            .unwrap()
            .check_representation_law(c)
            .unwrap()
    }

    #[test]
    fn test_rust_heisenberg_multiplication_associativity() {
        let p = 3;
        let g1 = HeisenbergElement::new(1, 0, 0);
        let g2 = HeisenbergElement::new(0, 1, 0);
        let g3 = HeisenbergElement::new(1, 1, 1);

        let g1_g23 = heisenberg_multiply(g1, heisenberg_multiply(g2, g3, p), p);
        let g12_g3 = heisenberg_multiply(heisenberg_multiply(g1, g2, p), g3, p);
        assert_eq!(g1_g23, g12_g3);
    }

    #[test]
    fn test_rust_heisenberg_commutator_central() {
        let p = 5;
        let g1 = HeisenbergElement::new(1, 0, 0);
        let g2 = HeisenbergElement::new(0, 1, 0);

        let g12 = heisenberg_multiply(g1, g2, p);
        let g21 = heisenberg_multiply(g2, g1, p);
        assert_eq!(g12.q, g21.q);
        assert_eq!(g12.p_coord, g21.p_coord);
        let diff_z = (g12.z + p - g21.z) % p;
        assert_eq!(diff_z, 1);
    }

    #[test]
    fn test_rust_central_character_census_sum_of_squares() {
        for &p in &[3, 5, 7, 11] {
            let census = compute_central_character_census(p);
            assert_eq!(census.sum_of_squares, p * p * p);
            assert_eq!(census.num_1d_irreps, p * p);
            assert_eq!(census.num_higher_irreps, p - 1);
            assert_eq!(census.higher_irrep_dimension, p);
        }
    }

    #[test]
    fn representation_actions_obey_the_law_for_all_small_characters() {
        for p in [3, 5] {
            for c in 0..p {
                assert!(check_schroedinger_representation_law(p, c));
                assert_eq!(
                    FiniteHeisenberg::new(p)
                        .expect("prime fixture")
                        .basis_action(HeisenbergElement::new(0, 0, 1), 0, c)
                        .expect("valid central character and basis index"),
                    (0, c)
                );
            }
        }
    }

    #[test]
    fn composite_census_is_rejected() {
        assert_eq!(
            FiniteHeisenberg::new(9),
            Err(engine_lie_theory::heisenberg::FiniteHeisenbergError::Prime)
        );
    }

    #[test]
    fn characteristic_two_is_rejected() {
        assert_eq!(
            FiniteHeisenberg::new(2),
            Err(engine_lie_theory::heisenberg::FiniteHeisenbergError::Prime)
        );
    }
}
