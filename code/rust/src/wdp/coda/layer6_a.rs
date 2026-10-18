use num_rational::BigRational;
use num_traits::Zero;
use serde_json::json;

use crate::coda::types::{LayerExecutionRecord, LayerId, ProblemInstance};

pub struct Layer6A;

impl Layer6A {
    pub fn evaluate(
        _problem: &ProblemInstance,
        phi1: &BigRational,
        gamma2: &BigRational,
    ) -> (LayerExecutionRecord, bool) {
        let has_residual = phi1 > &BigRational::zero();
        let is_coherent = gamma2.is_zero();

        let msg = if has_residual && is_coherent {
            format!(
                "CODA-A typed residual (Phi_1={}, Gamma_2=0): routed to CLOSED_RESIDUAL, where the firewall registers it as an Anomalon; never promoted",
                phi1
            )
        } else if has_residual {
            format!(
                "CODA-A incoherent residue (Phi_1={}, Gamma_2={}): violates the cocycle condition",
                phi1, gamma2
            )
        } else {
            "CODA-A vanishing residue (Phi_1=0): no leftover class".to_string()
        };

        let record = LayerExecutionRecord::new(LayerId::A, is_coherent, msg, phi1.clone())
            .with_metadata("has_residual", json!(has_residual))
            .with_metadata("is_coherent", json!(is_coherent))
            .with_metadata("residual_retained_in_cokernel", json!(has_residual));

        (record, has_residual)
    }
}
