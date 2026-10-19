//! terminal_object shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for a terminal object (limit of the empty diagram).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct TerminalObject {
    pub label: String,
    /// Object claimed to be terminal.
    pub object: String,
    /// Ambient category reference (diagnostic).
    pub category_ref: String,
    pub notes: Vec<String>,
}

impl TerminalObject {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            object: String::new(),
            category_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn in_category(
        label: impl Into<String>,
        object: impl Into<String>,
        category_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            object: object.into(),
            category_ref: category_ref.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.object.is_empty() {
            return Err(ArithmosError::InvalidShape("empty object".into()));
        }
        if self.category_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty category_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(TerminalObject::in_category("1", "1", "C")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(TerminalObject::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_object() {
        assert!(TerminalObject::new("t").validate_shell().is_err());
    }
}
