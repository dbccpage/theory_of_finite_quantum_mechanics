use engine_number_theory::rational::Rational;
use engine_quantum_physics::quantum_walk::{
    simulate_walk_s3_exact, simulate_walk_s4_exact, QuantumWalkError,
};
use serde::{Deserialize, Serialize};
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct BallisticWalkReceipt {
    pub group_name: String,
    pub steps: usize,
    pub order: usize,
    pub degree: usize,
    pub is_ballistic_scaling: bool,
    pub finite_light_cone_window_observed: bool,
    pub ballistic_ratio: Rational,
}

impl BallisticWalkReceipt {
    pub fn try_evaluate(group: &str, steps: usize) -> Result<Self, QuantumWalkError> {
        let res = match group {
            "S3" => simulate_walk_s3_exact(steps)?,
            "S4" => simulate_walk_s4_exact(steps)?,
            _ => return Err(QuantumWalkError::UnsupportedGroup(group.to_string())),
        };
        Ok(Self {
            group_name: res.group_name,
            steps: res.steps,
            order: res.order,
            degree: res.degree,
            is_ballistic_scaling: false,
            finite_light_cone_window_observed: res.is_ballistic,
            ballistic_ratio: res.ballistic_ratio,
        })
    }

    pub fn evaluate(group: &str, steps: usize) -> Result<Self, QuantumWalkError> {
        Self::try_evaluate(group, steps)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn an_unsupported_receipt_group_is_a_typed_refusal() {
        assert_eq!(
            BallisticWalkReceipt::try_evaluate("S5", 3).unwrap_err(),
            QuantumWalkError::UnsupportedGroup("S5".into())
        );
    }
}
