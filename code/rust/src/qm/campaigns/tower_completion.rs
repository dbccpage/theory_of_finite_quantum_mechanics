
use num_rational::Ratio;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct FuzzySphereRateRow {
    pub dimension: u64,
    pub commutator_norm: f64,
    pub rate_fraction: String,
    pub commutator_norm_exact: String,
    pub commutator_norm_upper_bound: f64,
    pub casimir_norm: f64,
    pub casimir_norm_exact: String,
}

pub fn compute_fuzzy_sphere_rate(d: u64) -> FuzzySphereRateRow {
    assert!(
        d >= 2,
        "The nontrivial fuzzy-sphere benchmark requires d >= 2"
    );
    let d128 = u128::from(d);
    let norm = Ratio::new(2 * (d128 - 1), d128 * d128);
    let casimir = Ratio::new(d128 * d128 - 1, d128 * d128);
    FuzzySphereRateRow {
        dimension: d,
        commutator_norm: *norm.numer() as f64 / *norm.denom() as f64,
        rate_fraction: format!("2 / {}", d),
        commutator_norm_exact: norm.to_string(),
        commutator_norm_upper_bound: 2.0 / d as f64,
        casimir_norm: *casimir.numer() as f64 / *casimir.denom() as f64,
        casimir_norm_exact: casimir.to_string(),
    }
}

pub fn generate_canonical_block05_rust_receipt() -> serde_json::Value {
    let benchmark: Vec<FuzzySphereRateRow> = [2, 4, 8, 16, 32, 64, 128]
        .iter()
        .map(|&d| compute_fuzzy_sphere_rate(d))
        .collect();

    serde_json::json!({
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_05",
        "global_targets": "C500-T401..C500-T425",
        "terminal_outcome": "FINITE_SPIN_BENCHMARK_WITH_DECLARED_MOMENT_COMPARISON",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "fuzzy_sphere_benchmark": benchmark,
        "machine_bet_clauses": {
            "benchmark_convergence_status": "FINITE_FORMULA_CHECKS_GENERAL_LIMIT_OPEN",
            "topology_is_explicit_input": false,
            "algebraic_union_equals_unqualified_completion": false,
            "topology_choice_changes_at_least_one_verdict": true,
            "all_declared_towers_converge": false,
            "analytic_source_claims_are_not_encoded_as_test_fixtures": false
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rust_fuzzy_sphere_rate() {
        let r2 = compute_fuzzy_sphere_rate(2);
        assert_eq!(r2.rate_fraction, "2 / 2");
        assert_eq!(r2.commutator_norm_exact, "1/2");
        assert_eq!(r2.casimir_norm_exact, "3/4");
        assert!((r2.commutator_norm - 0.5).abs() < 1e-9);

        let r10 = compute_fuzzy_sphere_rate(10);
        assert_eq!(r10.rate_fraction, "2 / 10");
        assert_eq!(r10.commutator_norm_exact, "9/50");
        assert_eq!(r10.casimir_norm_exact, "99/100");
        assert!((r10.commutator_norm - 0.18).abs() < 1e-9);
    }

    #[test]
    #[should_panic(expected = "d >= 2")]
    fn zero_dimension_is_rejected() {
        compute_fuzzy_sphere_rate(0);
    }
}
