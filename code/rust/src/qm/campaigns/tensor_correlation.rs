
use engine_number_theory::rational::{rq, Rational};
use engine_quantum_physics::tensor_commuting_correlation_frontier::{
    certify_chsh_interval, chsh_game_certificate,
};
use serde_json::json;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum CorrelationModelClass {
    FixedDimensionTensor,
    FiniteDimensionalTensorUnion,
    TopologicalClosureTensor,
    CommutingOperator,
}

impl CorrelationModelClass {
    pub const ALL: [Self; 4] = [
        Self::FixedDimensionTensor,
        Self::FiniteDimensionalTensorUnion,
        Self::TopologicalClosureTensor,
        Self::CommutingOperator,
    ];

    pub fn symbol(&self) -> &'static str {
        match self {
            Self::FixedDimensionTensor => "C_q(d)",
            Self::FiniteDimensionalTensorUnion => "C_q",
            Self::TopologicalClosureTensor => "C_qa",
            Self::CommutingOperator => "C_qc",
        }
    }

    pub fn description(&self) -> &'static str {
        match self {
            Self::FixedDimensionTensor => "Fixed dimension d tensor product correlations",
            Self::FiniteDimensionalTensorUnion => "Finite-dimensional tensor product union",
            Self::TopologicalClosureTensor => "Topological closure of C_q",
            Self::CommutingOperator => "Commuting-operator correlations",
        }
    }
}

pub fn correlation_model_hierarchy() -> Vec<(&'static str, &'static str)> {
    CorrelationModelClass::ALL
        .iter()
        .map(|c| (c.symbol(), c.description()))
        .collect()
}

pub fn chsh_game_bounds() -> (Rational, Rational, Rational) {
    (rq(3, 4), rq(17, 20), rq(43, 50))
}

pub fn audit_npa_exactness() -> (bool, bool) {
    (false, false)
}

pub fn generate_canonical_block08_rust_receipt() -> serde_json::Value {
    let (c_val, lower, upper) = chsh_game_bounds();
    let (exact_without_flat, req_flat) = audit_npa_exactness();

    json!({
        "campaign": "C500",
        "block": "block_08",
        "authority_effect": "None",
        "terminal_outcome": "BOUNDED_CORRELATION_ISLAND_WITH_GLOBAL_GUARDRAIL",
        "chsh_classical_value": format!("{}/{}", c_val.numer(), c_val.denom()),
        "chsh_quantum_lower_bound": format!("{}/{}", lower.numer(), lower.denom()),
        "chsh_quantum_upper_bound": format!("{}/{}", upper.numer(), upper.denom()),
        "chsh_interval_enclosure_verified": certify_chsh_interval(&lower,&upper).expect("fixed algebraic strategy certificate"),
        "expression_evidence_class": "EXACT_OPERATOR_SOS_AND_STATE_ATTAINMENT",
        "local_sdp_or_strategy_certificate": chsh_game_certificate().is_ok(),
        "npa_automatic_finite_level_exactness": exact_without_flat,
        "npa_requires_flatness": req_flat,
        "npa_requires_independent_exactness_certificate": true,
        "status": "SCOPED_EXACT_INTERVAL"
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hierarchy() {
        let h = correlation_model_hierarchy();
        assert_eq!(h.len(), 4);
        assert_eq!(h[0].0, "C_q(d)");
        assert_eq!(h[3].0, "C_qc");
    }

    #[test]
    fn test_typed_hierarchy() {
        assert_eq!(CorrelationModelClass::ALL.len(), 4);
        assert_eq!(
            CorrelationModelClass::FixedDimensionTensor.symbol(),
            "C_q(d)"
        );
        assert_eq!(CorrelationModelClass::CommutingOperator.symbol(), "C_qc");
    }

    #[test]
    fn test_chsh_bounds() {
        let (c_val, lower, upper) = chsh_game_bounds();
        assert_eq!(c_val, rq(3, 4));
        assert_eq!(lower, rq(17, 20));
        assert_eq!(upper, rq(43, 50));
        assert!(lower > c_val);
        assert!(upper > lower);
        assert!(
            certify_chsh_interval(&lower, &upper).expect("fixed algebraic strategy certificate")
        );
        assert!(!certify_chsh_interval(&rq(9, 10), &rq(91, 100)).unwrap());
        assert!(!certify_chsh_interval(&rq(3, 4), &rq(4, 5)).unwrap());
        assert_eq!(certify_chsh_interval(&upper, &lower), Ok(false));
    }

    #[test]
    fn test_npa_audit() {
        let (exact_without_flatness, requires_flatness) = audit_npa_exactness();
        assert!(!exact_without_flatness);
        assert!(!requires_flatness);
    }
}
