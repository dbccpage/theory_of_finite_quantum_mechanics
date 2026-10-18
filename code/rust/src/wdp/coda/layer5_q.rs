use num_rational::BigRational;
use num_traits::Zero;
use serde_json::json;

use crate::coda::types::{LayerExecutionRecord, LayerId, ProblemInstance};

pub struct Layer5Q;

impl Layer5Q {
    pub fn evaluate(problem: &ProblemInstance) -> (LayerExecutionRecord, BigRational) {
        let (lo, hi) = &problem.enclosure_interval;
        if hi < lo {
            let diameter = BigRational::zero();
            let msg = format!("Inverted interval enclosure [{}, {}]", lo, hi);
            let record = LayerExecutionRecord::new(LayerId::Q, false, msg, diameter.clone())
                .with_metadata("interval_lo", json!(lo.to_string()))
                .with_metadata("interval_hi", json!(hi.to_string()))
                .with_metadata("diameter", json!(diameter.to_string()));
            (record, diameter)
        } else {
            let diameter = hi - lo;
            let msg = format!(
                "Enclosure verified: [{}, {}] with diameter {}; midpoint is not exact state",
                lo, hi, diameter
            );
            let record = LayerExecutionRecord::new(LayerId::Q, true, msg, diameter.clone())
                .with_metadata("interval_lo", json!(lo.to_string()))
                .with_metadata("interval_hi", json!(hi.to_string()))
                .with_metadata("diameter", json!(diameter.to_string()));
            (record, diameter)
        }
    }
}
