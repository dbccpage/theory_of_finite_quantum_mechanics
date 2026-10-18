use serde::{Deserialize, Serialize};

use super::continuum::ContinuumDebt;
use super::errors::QError;
use super::packet::{QPacket, QTerminal};
use omega_types::q_continuum::{
    AuthorityScope, DescentResult, ObstructionKind, QContinuumLedger, Residual,
};

/// What kind of Q candidate is being admitted.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum CandidateKind {
    Theory,
    Representation,
    Analogy,
    Model,
    Source,
    ProbeRequest,
}

/// Admission request attached to one candidate.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct QAdmissionRequest {
    pub candidate_id: String,
    pub kind: CandidateKind,
    pub continuum: ContinuumDebt,
}

impl QAdmissionRequest {
    pub fn new(candidate_id: impl Into<String>, kind: CandidateKind) -> Self {
        Self {
            candidate_id: candidate_id.into(),
            kind,
            continuum: ContinuumDebt::default(),
        }
    }

    pub fn with_finite_shadow(mut self, finite_shadow: impl Into<String>) -> Self {
        self.continuum.finite_shadow = Some(finite_shadow.into());
        self
    }

    pub fn with_refinement_relation(mut self, refinement_relation: impl Into<String>) -> Self {
        self.continuum.refinement_relation = Some(refinement_relation.into());
        self
    }

    pub fn with_declared_topology(mut self, declared_topology: impl Into<String>) -> Self {
        self.continuum.declared_topology = Some(declared_topology.into());
        self
    }

    pub fn with_convergence_certificate_route(
        mut self,
        convergence_certificate_route: impl Into<String>,
    ) -> Self {
        self.continuum.convergence_certificate_route = Some(convergence_certificate_route.into());
        self
    }

    pub fn with_descent_trigger(mut self, descent_trigger: impl Into<String>) -> Self {
        self.continuum.descent_trigger = Some(descent_trigger.into());
        self
    }
}

/// Classification result for a Q admission candidate.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct AdmissionDecision {
    pub candidate_id: String,
    pub kind: CandidateKind,
    pub terminal_status: QTerminal,
    pub obligations: Vec<String>,
    pub residual: Option<Residual>,
}

impl AdmissionDecision {
    /// Records the admission residual as an append-only Q ledger row.
    pub fn record_residual(&self, ledger: &mut QContinuumLedger, scope: AuthorityScope) {
        if let Some(residual) = self.residual.clone() {
            let result =
                DescentResult::failed(format!("admission:{}", self.candidate_id), scope, residual);
            ledger.record_descent_result(self.candidate_id.clone(), result);
        }
    }
}

/// Strict Q admission gate.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct QAdmissionGate;

impl QAdmissionGate {
    pub fn new() -> Self {
        Self
    }

    pub fn classify_admission(
        &self,
        packet: &QPacket,
        request: &QAdmissionRequest,
    ) -> AdmissionDecision {
        let mut obligations = vec![
            "produce finite projection".to_string(),
            "record descent obligation".to_string(),
            "record residual if no witness exists".to_string(),
        ];

        if let Err(error) = packet.validate_mandatory() {
            obligations.push("fix missing mandatory packet fields".to_string());
            return AdmissionDecision {
                candidate_id: request.candidate_id.clone(),
                kind: request.kind,
                terminal_status: QTerminal::OpenResidual,
                obligations,
                residual: Some(residual_for_error(&request.candidate_id, error)),
            };
        }

        let terminal_request = packet.terminal_request.unwrap_or(QTerminal::OpenResidual);
        let mut residual = None;

        let mut derived_status = if terminal_request == QTerminal::TerminalWithinScope {
            obligations.push(
                "TerminalWithinScope requires finite descent evidence with witness support"
                    .to_string(),
            );
            residual = Some(Residual::new(
                format!(
                    "residual:admission:{}:terminal-request",
                    request.candidate_id
                ),
                request.candidate_id.clone(),
                ObstructionKind::MissingWitness,
                "QPacket requested TerminalWithinScope without a finite descent witness",
            ));
            QTerminal::OpenResidual
        } else {
            terminal_request
        };

        let admission_result = if derived_status == QTerminal::QHeld {
            request.continuum.validate_for_qheld()
        } else {
            request.continuum.validate_for_admission()
        };

        if let Err(error) = admission_result {
            obligations.push(format!("admission validation failed: {error}"));
            derived_status = terminal_for_error(&error);
            residual = Some(residual_for_error(&request.candidate_id, error));
        }

        AdmissionDecision {
            candidate_id: request.candidate_id.clone(),
            kind: request.kind,
            terminal_status: derived_status,
            obligations,
            residual,
        }
    }

    pub fn admit_qheld(
        &self,
        packet: &QPacket,
        request: &QAdmissionRequest,
    ) -> Result<AdmissionDecision, QError> {
        packet.validate_mandatory()?;
        request.continuum.validate_for_qheld()?;

        let terminal_request = packet
            .terminal_request
            .expect("validated packet has terminal_request");
        if terminal_request != QTerminal::QHeld {
            return Err(QError::OpenResidual);
        }

        Ok(AdmissionDecision {
            candidate_id: request.candidate_id.clone(),
            kind: request.kind,
            terminal_status: QTerminal::QHeld,
            obligations: vec![
                "produce finite projection".to_string(),
                "record descent obligation".to_string(),
                "record residual if no witness exists".to_string(),
            ],
            residual: None,
        })
    }
}

fn terminal_for_error(error: &QError) -> QTerminal {
    match error {
        QError::RefusedContinuumNoShadow
        | QError::QHeldWithoutFiniteShadow
        | QError::ContinuumClaimWithoutTopology
        | QError::NoGenesisBoundaryViolation => QTerminal::Refused,
        QError::OracleNeededConvergence => QTerminal::OracleNeeded,
        _ => QTerminal::OpenResidual,
    }
}

fn residual_for_error(candidate_id: &str, error: QError) -> Residual {
    let obstruction = match error {
        QError::RefusedContinuumNoShadow
        | QError::QHeldWithoutFiniteShadow
        | QError::ContinuumClaimWithoutTopology
        | QError::NoGenesisBoundaryViolation => ObstructionKind::NonFiniteProjection,
        QError::OracleNeededConvergence => ObstructionKind::ReplayMissing,
        QError::QHeldWithoutRefinementRoute
        | QError::QHeldWithoutDescentTrigger
        | QError::OpenResidual
        | QError::CompositionRuleRequired
        | QError::MissingMandatoryField(_) => ObstructionKind::Underdefined,
    };
    Residual::new(
        format!("residual:admission:{candidate_id}"),
        candidate_id.to_string(),
        obstruction,
        format!("Q admission failed: {error}"),
    )
}

#[cfg(test)]
mod tests {
    use super::super::packet::{ResidualSpec, TransportSpec};
    use super::*;

    fn valid_packet(terminal_request: QTerminal) -> QPacket {
        QPacket::new("q:admission:test")
            .with_carrier("finite carrier")
            .with_composition("declared composition rule")
            .with_observer("declared observer")
            .with_finite_prediction("finite prediction")
            .with_transport(TransportSpec::new("transport into finite shadow"))
            .with_residual(ResidualSpec::new(
                "open residual",
                ObstructionKind::NonFiniteProjection,
            ))
            .with_terminal_request(terminal_request)
    }

    fn complete_qheld_request() -> QAdmissionRequest {
        QAdmissionRequest::new("candidate:admission:test", CandidateKind::Representation)
            .with_finite_shadow("finite shadow")
            .with_refinement_relation("refinement route")
            .with_declared_topology("finite-discrete topology")
            .with_convergence_certificate_route("certificate route")
            .with_descent_trigger("next finite replay")
    }

    #[test]
    fn rejects_qheld_without_finite_shadow() {
        let packet = valid_packet(QTerminal::QHeld);
        let mut request = complete_qheld_request();
        request.continuum.finite_shadow = None;

        assert_eq!(
            QAdmissionGate::new().admit_qheld(&packet, &request),
            Err(QError::QHeldWithoutFiniteShadow)
        );
    }

    #[test]
    fn rejects_qheld_without_refinement_route() {
        let packet = valid_packet(QTerminal::QHeld);
        let mut request = complete_qheld_request();
        request.continuum.refinement_relation = None;

        assert_eq!(
            QAdmissionGate::new().admit_qheld(&packet, &request),
            Err(QError::QHeldWithoutRefinementRoute)
        );
    }

    #[test]
    fn rejects_qheld_without_declared_topology() {
        let packet = valid_packet(QTerminal::QHeld);
        let mut request = complete_qheld_request();
        request.continuum.declared_topology = None;

        assert_eq!(
            QAdmissionGate::new().admit_qheld(&packet, &request),
            Err(QError::ContinuumClaimWithoutTopology)
        );
    }

    #[test]
    fn rejects_qheld_without_convergence_certificate_route() {
        let packet = valid_packet(QTerminal::QHeld);
        let mut request = complete_qheld_request();
        request.continuum.convergence_certificate_route = None;

        assert_eq!(
            QAdmissionGate::new().admit_qheld(&packet, &request),
            Err(QError::QHeldWithoutRefinementRoute)
        );
    }

    #[test]
    fn rejects_qheld_without_descent_trigger() {
        let packet = valid_packet(QTerminal::QHeld);
        let mut request = complete_qheld_request();
        request.continuum.descent_trigger = None;

        assert_eq!(
            QAdmissionGate::new().admit_qheld(&packet, &request),
            Err(QError::QHeldWithoutDescentTrigger)
        );
    }

    #[test]
    fn packet_cannot_self_declare_terminal_within_scope() {
        let packet = valid_packet(QTerminal::TerminalWithinScope);
        let request = complete_qheld_request();

        let decision = QAdmissionGate::new().classify_admission(&packet, &request);
        assert_eq!(decision.terminal_status, QTerminal::OpenResidual);
        assert!(decision.residual.is_some());
    }
}
