use num_rational::BigRational;
use num_traits::{One, Zero};
use serde_json::json;

use crate::coda::types::{
    AuthorityToken, ExternalAuthorityGrant, FirewallDecision, LayerExecutionRecord, LayerId,
    ProblemInstance,
};

pub struct Layer8Fda;

impl Layer8Fda {
    pub fn evaluate(
        _problem: &ProblemInstance,
        phi1: &BigRational,
        gamma2: &BigRational,
        refused_by_or: bool,
    ) -> (
        LayerExecutionRecord,
        FirewallDecision,
        Option<AuthorityToken>,
    ) {
        Self::evaluate_with_grant(_problem, phi1, gamma2, refused_by_or, None)
    }

    pub fn evaluate_with_grant(
        problem: &ProblemInstance,
        phi1: &BigRational,
        gamma2: &BigRational,
        refused_by_or: bool,
        external_grant: Option<&ExternalAuthorityGrant>,
    ) -> (
        LayerExecutionRecord,
        FirewallDecision,
        Option<AuthorityToken>,
    ) {
        if refused_by_or {
            let decision = FirewallDecision::RouteRefused;
            let msg = "FDA gate: upstream refusal".to_string();
            let record = LayerExecutionRecord::new(LayerId::FDA, false, msg, BigRational::one())
                .with_metadata("firewall_decision", json!("ROUTE_REFUSED"))
                .with_metadata("token_issued", json!(false));
            (record, decision, None)
        } else if !gamma2.is_zero() {
            let decision = FirewallDecision::RouteRefused;
            let msg = format!("FDA gate: incoherent cocycle defect Gamma_2={}", gamma2);
            let record = LayerExecutionRecord::new(LayerId::FDA, false, msg, BigRational::one())
                .with_metadata("firewall_decision", json!("ROUTE_REFUSED"))
                .with_metadata("token_issued", json!(false));
            (record, decision, None)
        } else if phi1 > &BigRational::zero() {
            let decision = FirewallDecision::RouteClosedResidual;
            let msg = format!(
                "FDA gate: non-zero quotient defect Phi_1={} retained; non-promotion",
                phi1
            );
            let record = LayerExecutionRecord::new(LayerId::FDA, true, msg, BigRational::one())
                .with_metadata("firewall_decision", json!("ROUTE_CLOSED_RESIDUAL"))
                .with_metadata("token_issued", json!(false));
            (record, decision, None)
        } else if external_grant.is_some() {
            let record = LayerExecutionRecord::new(
                LayerId::FDA,
                false,
                "EXTERNAL_GRANT_VERIFIER_UNAVAILABLE",
                BigRational::one(),
            )
            .with_metadata("token_issued", json!(false));
            (record, FirewallDecision::RouteRefused, None)
        } else {
            let decision = FirewallDecision::RouteClosedResidual;
            let msg = format!(
                "FDA gate: zero defect on {}; authorization requires a verified external grant at the firewall",
                problem.problem_id
            );
            let record = LayerExecutionRecord::new(LayerId::FDA, true, msg, BigRational::one())
                .with_metadata("firewall_decision", json!("ROUTE_CLOSED_RESIDUAL"))
                .with_metadata("token_issued", json!(false));
            (record, decision, None)
        }
    }
}
