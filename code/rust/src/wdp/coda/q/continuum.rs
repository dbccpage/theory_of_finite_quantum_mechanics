use serde::{Deserialize, Serialize};

use super::errors::QError;
use super::packet::option_has_text;

/// Continuum admission debt required before a candidate may be Q-held.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct ContinuumDebt {
    pub finite_shadow: Option<String>,
    pub refinement_relation: Option<String>,
    pub declared_topology: Option<String>,
    pub convergence_certificate_route: Option<String>,
    pub descent_trigger: Option<String>,
}

impl ContinuumDebt {
    pub fn has_finite_shadow(&self) -> bool {
        option_has_text(&self.finite_shadow)
    }

    pub fn has_refinement_route(&self) -> bool {
        option_has_text(&self.refinement_relation)
            && option_has_text(&self.convergence_certificate_route)
    }

    pub fn has_declared_topology(&self) -> bool {
        option_has_text(&self.declared_topology)
    }

    pub fn has_descent_trigger(&self) -> bool {
        option_has_text(&self.descent_trigger)
    }

    pub fn validate_for_qheld(&self) -> Result<(), QError> {
        if !self.has_finite_shadow() {
            return Err(QError::QHeldWithoutFiniteShadow);
        }
        if !self.has_refinement_route() {
            return Err(QError::QHeldWithoutRefinementRoute);
        }
        if !self.has_declared_topology() {
            return Err(QError::ContinuumClaimWithoutTopology);
        }
        if !self.has_descent_trigger() {
            return Err(QError::QHeldWithoutDescentTrigger);
        }
        Ok(())
    }

    pub fn validate_for_admission(&self) -> Result<(), QError> {
        if !self.has_finite_shadow() {
            return Err(QError::RefusedContinuumNoShadow);
        }
        if !self.has_declared_topology() {
            return Err(QError::ContinuumClaimWithoutTopology);
        }
        if !option_has_text(&self.convergence_certificate_route) {
            return Err(QError::OracleNeededConvergence);
        }
        if !option_has_text(&self.refinement_relation) || !self.has_descent_trigger() {
            return Err(QError::OpenResidual);
        }
        Ok(())
    }
}
