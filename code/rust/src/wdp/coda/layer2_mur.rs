use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde_json::json;

use crate::coda::types::{LayerExecutionRecord, LayerId, ProblemInstance};

pub struct Layer2Mur;

impl Layer2Mur {
    pub fn evaluate(problem: &ProblemInstance) -> (LayerExecutionRecord, BigRational) {
        let mut loss = BigRational::zero();
        let mut incompatible = Vec::new();
        let mut missing = Vec::new();
        let mut mismatched = Vec::new();

        for ((u, v), compatible) in &problem.overlaps {
            if !compatible {
                incompatible.push((u.clone(), v.clone()));
                loss += BigRational::one();
                continue;
            }

            let su = problem.local_sections.get(u);
            let sv = problem.local_sections.get(v);

            match (su, sv) {
                (Some(su_vec), Some(sv_vec)) => {
                    if su_vec.len() != sv_vec.len() {
                        mismatched.push((u.clone(), v.clone()));
                        continue;
                    }
                    for (a, b) in su_vec.iter().zip(sv_vec.iter()) {
                        loss += (a - b).abs();
                    }
                }
                _ => {
                    missing.push((u.clone(), v.clone()));
                }
            }
        }

        let succeeded = incompatible.is_empty()
            && missing.is_empty()
            && mismatched.is_empty()
            && loss.is_zero();

        let msg = format!(
            "{}Transport loss={}; incompatible overlaps={}, overlaps naming a missing section={}, length mismatches={}",
            if succeeded { "Transport verified: " } else { "Transport failure: " },
            loss,
            incompatible.len(),
            missing.len(),
            mismatched.len()
        );

        let record = LayerExecutionRecord::new(LayerId::MUR, succeeded, msg, loss.clone())
            .with_metadata("incompatible_overlaps", json!(incompatible.len()))
            .with_metadata("missing_section_overlaps", json!(missing.len()))
            .with_metadata("length_mismatches", json!(mismatched.len()))
            .with_metadata("loss_defect", json!(loss.to_string()));

        (record, loss)
    }
}
