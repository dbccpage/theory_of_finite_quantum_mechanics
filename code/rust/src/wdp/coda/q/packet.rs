use serde::{Deserialize, Serialize};

use super::errors::{QError, QPacketField};
use engine_types::q_continuum::{ObstructionKind, TerminalStatus};

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum QTerminal {
    Refused,
    OpenResidual,
    OracleNeeded,
    QHeld,
    ConditionalSupport,
    TerminalWithinScope,
}

impl QTerminal {
    pub fn to_terminal_status(self) -> TerminalStatus {
        match self {
            Self::Refused => TerminalStatus::Refused,
            Self::OpenResidual | Self::OracleNeeded | Self::QHeld | Self::TerminalWithinScope => {
                TerminalStatus::Residual
            }
            Self::ConditionalSupport => TerminalStatus::ConditionallySupported,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TransportSpec {
    pub route: String,
    pub equivalence_scope: Option<String>,
    pub failure_mode: Option<String>,
}

impl TransportSpec {
    pub fn new(route: impl Into<String>) -> Self {
        Self {
            route: route.into(),
            equivalence_scope: None,
            failure_mode: None,
        }
    }

    pub fn with_equivalence_scope(mut self, scope: impl Into<String>) -> Self {
        self.equivalence_scope = Some(scope.into());
        self
    }

    pub fn with_failure_mode(mut self, failure_mode: impl Into<String>) -> Self {
        self.failure_mode = Some(failure_mode.into());
        self
    }

    pub fn is_declared(&self) -> bool {
        has_text(&self.route)
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ResidualSpec {
    pub description: String,
    pub obstruction: ObstructionKind,
    pub next_probe_hint: Option<String>,
}

impl ResidualSpec {
    pub fn new(description: impl Into<String>, obstruction: ObstructionKind) -> Self {
        Self {
            description: description.into(),
            obstruction,
            next_probe_hint: None,
        }
    }

    pub fn with_next_probe_hint(mut self, hint: impl Into<String>) -> Self {
        self.next_probe_hint = Some(hint.into());
        self
    }

    pub fn is_declared(&self) -> bool {
        has_text(&self.description)
    }
}

#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct QPacket {
    pub id: String,
    pub carrier: Option<String>,
    pub composition: Option<String>,
    pub observer: Option<String>,
    pub finite_predictions: Vec<String>,
    pub transport: Option<TransportSpec>,
    pub residual: Option<ResidualSpec>,
    pub terminal_request: Option<QTerminal>,
}

impl QPacket {
    pub fn new(id: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            ..Self::default()
        }
    }

    pub fn with_carrier(mut self, carrier: impl Into<String>) -> Self {
        self.carrier = Some(carrier.into());
        self
    }

    pub fn with_composition(mut self, composition: impl Into<String>) -> Self {
        self.composition = Some(composition.into());
        self
    }

    pub fn with_observer(mut self, observer: impl Into<String>) -> Self {
        self.observer = Some(observer.into());
        self
    }

    pub fn with_finite_prediction(mut self, prediction: impl Into<String>) -> Self {
        self.finite_predictions.push(prediction.into());
        self
    }

    pub fn with_transport(mut self, transport: TransportSpec) -> Self {
        self.transport = Some(transport);
        self
    }

    pub fn with_residual(mut self, residual: ResidualSpec) -> Self {
        self.residual = Some(residual);
        self
    }

    pub fn with_terminal_request(mut self, terminal_request: QTerminal) -> Self {
        self.terminal_request = Some(terminal_request);
        self
    }

    pub fn missing_mandatory_fields(&self) -> Vec<QPacketField> {
        let mut missing = Vec::new();

        if !option_has_text(&self.carrier) {
            missing.push(QPacketField::Carrier);
        }
        if !option_has_text(&self.composition) {
            missing.push(QPacketField::Composition);
        }
        if !option_has_text(&self.observer) {
            missing.push(QPacketField::Observer);
        }
        if !self
            .finite_predictions
            .iter()
            .any(|prediction| has_text(prediction))
        {
            missing.push(QPacketField::FinitePredictions);
        }
        if !self
            .transport
            .as_ref()
            .is_some_and(TransportSpec::is_declared)
        {
            missing.push(QPacketField::Transport);
        }
        if !self
            .residual
            .as_ref()
            .is_some_and(ResidualSpec::is_declared)
        {
            missing.push(QPacketField::Residual);
        }
        if self.terminal_request.is_none() {
            missing.push(QPacketField::TerminalRequest);
        }

        missing
    }

    pub fn validate_mandatory(&self) -> Result<(), QError> {
        match self.missing_mandatory_fields().first().copied() {
            Some(field) => Err(QError::MissingMandatoryField(field)),
            None => Ok(()),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ValidatedQPacket {
    packet: QPacket,
}

impl ValidatedQPacket {
    pub fn packet(&self) -> &QPacket {
        &self.packet
    }

    pub fn into_packet(self) -> QPacket {
        self.packet
    }
}

impl TryFrom<QPacket> for ValidatedQPacket {
    type Error = QError;

    fn try_from(packet: QPacket) -> Result<Self, Self::Error> {
        packet.validate_mandatory()?;
        Ok(Self { packet })
    }
}

pub(crate) fn has_text(value: &str) -> bool {
    !value.trim().is_empty()
}

pub(crate) fn option_has_text(value: &Option<String>) -> bool {
    value.as_deref().is_some_and(has_text)
}
