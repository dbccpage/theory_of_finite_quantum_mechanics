use serde::{Deserialize, Serialize};

use super::errors::{QError, QPacketField};
use super::packet::{has_text, option_has_text, QTerminal};

/// Audit packet for representation transport candidates.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct RepresentationTransportPacket {
    pub candidate_id: String,
    pub carrier: String,
    pub composition_rule: Option<String>,
    pub observer_measurement_pairing: Option<String>,
    pub finite_predictions: Vec<String>,
    pub representation_transport: Option<String>,
    pub equivalence_scope: Option<String>,
    pub failure_mode: Option<String>,
    pub residual_selector: Option<String>,
    pub terminal_status_request: Option<QTerminal>,
}

impl RepresentationTransportPacket {
    pub fn real_complex_qm(carrier: impl Into<String>, candidate_id: impl Into<String>) -> Self {
        Self {
            candidate_id: candidate_id.into(),
            carrier: carrier.into(),
            ..Self::default()
        }
    }

    pub fn with_composition_rule(mut self, composition_rule: impl Into<String>) -> Self {
        self.composition_rule = Some(composition_rule.into());
        self
    }

    pub fn with_observer_measurement_pairing(mut self, pairing: impl Into<String>) -> Self {
        self.observer_measurement_pairing = Some(pairing.into());
        self
    }

    pub fn with_finite_prediction(mut self, prediction: impl Into<String>) -> Self {
        self.finite_predictions.push(prediction.into());
        self
    }

    pub fn with_representation_transport(mut self, transport: impl Into<String>) -> Self {
        self.representation_transport = Some(transport.into());
        self
    }

    pub fn with_equivalence_scope(mut self, scope: impl Into<String>) -> Self {
        self.equivalence_scope = Some(scope.into());
        self
    }

    pub fn with_failure_mode(mut self, failure_mode: impl Into<String>) -> Self {
        self.failure_mode = Some(failure_mode.into());
        self
    }

    pub fn with_residual_selector(mut self, residual_selector: impl Into<String>) -> Self {
        self.residual_selector = Some(residual_selector.into());
        self
    }

    pub fn with_terminal_status_request(mut self, terminal_status_request: QTerminal) -> Self {
        self.terminal_status_request = Some(terminal_status_request);
        self
    }

    pub fn with_terminal_status(self, terminal_status_request: QTerminal) -> Self {
        self.with_terminal_status_request(terminal_status_request)
    }

    /// Full transport validation for any representation transport candidate (including real/complex QM).
    pub fn validate_full_transport_packet(&self) -> Result<(), QError> {
        if !has_text(&self.carrier) {
            return Err(QError::MissingMandatoryField(QPacketField::Carrier));
        }
        if !option_has_text(&self.composition_rule) {
            return Err(QError::CompositionRuleRequired);
        }
        if !option_has_text(&self.observer_measurement_pairing) {
            return Err(QError::MissingMandatoryField(QPacketField::Observer));
        }
        if self.finite_predictions.is_empty()
            || !self.finite_predictions.iter().any(|p| has_text(p))
        {
            return Err(QError::MissingMandatoryField(
                QPacketField::FinitePredictions,
            ));
        }
        if !option_has_text(&self.representation_transport) {
            return Err(QError::MissingMandatoryField(QPacketField::Transport));
        }
        if !option_has_text(&self.equivalence_scope) {
            return Err(QError::MissingMandatoryField(QPacketField::Transport));
        }
        if !option_has_text(&self.failure_mode) {
            return Err(QError::MissingMandatoryField(QPacketField::Transport));
        }
        if !option_has_text(&self.residual_selector) {
            return Err(QError::MissingMandatoryField(QPacketField::Residual));
        }
        if self.terminal_status_request.is_none() {
            return Err(QError::MissingMandatoryField(QPacketField::TerminalRequest));
        }
        Ok(())
    }
}
