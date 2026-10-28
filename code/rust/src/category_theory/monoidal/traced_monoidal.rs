//! traced_monoidal shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

/// Best-effort traced monoidal category shell.
/// Trace operator family Tr^X_{A,B} : C(A⊗X, B⊗X) → C(A,B) as a ref.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct TracedMonoidal {
    pub label: String,
    /// Underlying (typically symmetric) monoidal category shell label.
    pub monoidal_ref: String,
    /// Trace operator family ref.
    pub trace_ref: String,
    pub notes: Vec<String>,
}

impl TracedMonoidal {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: String::new(),
            trace_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_trace(
        label: impl Into<String>,
        monoidal_ref: impl Into<String>,
        trace_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: monoidal_ref.into(),
            trace_ref: trace_ref.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.monoidal_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty monoidal_ref".into()));
        }
        if self.trace_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty trace_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(TracedMonoidal::with_trace("Tr", "Sym", "Tr")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(TracedMonoidal::new("").validate_shell().is_err());
    }
}
