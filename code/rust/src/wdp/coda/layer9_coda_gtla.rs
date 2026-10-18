use num_rational::BigRational;
use num_traits::One;
use serde_json::json;

use crate::coda::types::{
    AuthorityToken, DualWitness, FirewallDecision, LayerExecutionRecord, LayerId,
    MasterNormalFormOutcome, ProblemInstance, ResidualPair, TerminalKind,
};

pub struct Layer9CodaGtla;

impl Layer9CodaGtla {
    #[allow(clippy::too_many_arguments)]
    pub fn terminalize(
        problem: &ProblemInstance,
        phi1: Option<BigRational>,
        gamma2: Option<BigRational>,
        dual_witness: Option<DualWitness>,
        firewall_decision: FirewallDecision,
        _authority_token: Option<AuthorityToken>,
        mut layer_records: Vec<LayerExecutionRecord>,
        custom_reason: Option<String>,
        primal_repair: Option<Vec<BigRational>>,
        evidence_digest: String,
    ) -> MasterNormalFormOutcome {
        let residual_pair = match (&phi1, &gamma2) {
            (Some(p), Some(g)) => Some(ResidualPair::new(p.clone(), g.clone())),
            _ => None,
        };

        let (terminal_kind, default_reason, defect_mass) = match firewall_decision {
            FirewallDecision::RouteClosedResidual => (
                TerminalKind::ClosedResidual,
                "Pipeline terminated in CLOSED_RESIDUAL; non-promoted".to_string(),
                phi1.clone().unwrap_or_else(BigRational::one),
            ),
            _ => (
                TerminalKind::Refused,
                "Pipeline terminated in REFUSED: a halt guard or layer refused".to_string(),
                BigRational::one(),
            ),
        };

        let coda_gtla_record = LayerExecutionRecord::new(
            LayerId::CODA_GTLA,
            true,
            format!("GTLA Terminalization complete: outcome={:?}", terminal_kind),
            defect_mass,
        )
        .with_metadata("terminal_kind", json!(format!("{:?}", terminal_kind)))
        .with_metadata(
            "is_authorized",
            json!(terminal_kind == TerminalKind::Authorized),
        )
        .with_metadata(
            "is_closed_residual",
            json!(terminal_kind == TerminalKind::ClosedResidual),
        )
        .with_metadata("is_refused", json!(terminal_kind == TerminalKind::Refused));

        layer_records.push(coda_gtla_record);

        MasterNormalFormOutcome {
            problem_id: problem.problem_id.clone(),
            terminal_kind,
            residual_pair,
            dual_witness,
            authority_token: None,
            layer_records,
            firewall_decision,
            reason: custom_reason.unwrap_or(default_reason),
            primal_repair,
            evidence_digest,
        }
    }
}
