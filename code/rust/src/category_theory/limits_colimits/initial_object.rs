//! initial_object shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort shell for an initial object (colimit of the empty diagram).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct InitialObject {
    pub label: String,
    /// Object claimed to be initial.
    pub object: String,
    /// Ambient category reference (diagnostic).
    pub category_ref: String,
    pub notes: Vec<String>,
}

impl InitialObject {
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

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.object.is_empty() {
            return Err("empty object".into());
        }
        if self.category_ref.is_empty() {
            return Err("empty category_ref".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(InitialObject::in_category("0", "0", "C")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(InitialObject::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_object() {
        assert!(InitialObject::new("i").validate_shell().is_err());
    }
}
