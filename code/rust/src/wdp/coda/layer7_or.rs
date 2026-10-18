use num_rational::BigRational;
use num_traits::Zero;
use serde_json::json;

use crate::coda::types::{LayerExecutionRecord, LayerId, ProblemInstance};

pub struct Layer7Or;

impl Layer7Or {
    pub fn evaluate(
        problem: &ProblemInstance,
        gamma2: &BigRational,
    ) -> (LayerExecutionRecord, bool) {
        let mut reasons = Vec::new();

        let admitted: Vec<&String> = problem
            .candidate_sieve
            .iter()
            .filter(|s| !s.trim().is_empty())
            .collect();

        if admitted.is_empty() {
            reasons.push(
                "Empty support sieve: no admitted (non-blank) candidate hypothesis (OR-T5)"
                    .to_string(),
            );
        }

        let incompatible: Vec<(&(String, String), &bool)> =
            problem.overlaps.iter().filter(|(_, &comp)| !comp).collect();

        if !incompatible.is_empty() {
            reasons.push(format!(
                "Incompatible boundary overlaps detected: {:?} (OR-T3)",
                incompatible
                    .iter()
                    .map(|(pair, _)| pair)
                    .collect::<Vec<_>>()
            ));
        }

        if !gamma2.is_zero() {
            reasons.push(format!("Cocycle gluing failure: Gamma_2={} != 0", gamma2));
        }

        let is_refused = !reasons.is_empty();
        let msg = if is_refused {
            format!("OR Hard Refusal triggered: {}", reasons.join("; "))
        } else {
            "OR Refusal sieve passed: candidate sieve inhabited, overlaps compatible, Gamma_2 == 0"
                .to_string()
        };

        let record = LayerExecutionRecord::new(
            LayerId::OR,
            !is_refused,
            msg,
            BigRational::from_integer((reasons.len() as i64).into()),
        )
        .with_metadata("is_refused", json!(is_refused))
        .with_metadata("reasons", json!(reasons))
        .with_metadata("sieve_size", json!(admitted.len()));

        (record, is_refused)
    }
}
