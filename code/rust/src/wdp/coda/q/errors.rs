use std::fmt;

use thiserror::Error;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum QPacketField {
    Carrier,
    Composition,
    Observer,
    FinitePredictions,
    Transport,
    Residual,
    TerminalRequest,
}

impl QPacketField {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Carrier => "carrier",
            Self::Composition => "composition",
            Self::Observer => "observer",
            Self::FinitePredictions => "finite_predictions",
            Self::Transport => "transport",
            Self::Residual => "residual",
            Self::TerminalRequest => "terminal_request",
        }
    }
}

impl fmt::Display for QPacketField {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Error)]
pub enum QError {
    #[error("missing mandatory Q packet field: {0}")]
    MissingMandatoryField(QPacketField),
    #[error("QHeld requires a named finite_shadow")]
    QHeldWithoutFiniteShadow,
    #[error("QHeld requires a refinement relation and convergence certificate route")]
    QHeldWithoutRefinementRoute,
    #[error("QHeld requires a live descent_trigger")]
    QHeldWithoutDescentTrigger,
    #[error("continuum claim without declared topology is refused")]
    ContinuumClaimWithoutTopology,
    #[error("candidate refused: no finite shadow was declared")]
    RefusedContinuumNoShadow,
    #[error("candidate requires an oracle/certificate route for convergence")]
    OracleNeededConvergence,
    #[error("candidate remains an open residual")]
    OpenResidual,
    #[error("real/complex QM transport requires an explicit composition rule")]
    CompositionRuleRequired,
    #[error("No-Genesis boundary violation (PCC.core_top): observer creation claimed without declared non-constant observable profile")]
    NoGenesisBoundaryViolation,
}
