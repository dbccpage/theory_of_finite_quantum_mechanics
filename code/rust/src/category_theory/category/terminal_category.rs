//! terminal_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! 1: one object, one identity morphism (terminal object of Cat).

use serde::{Deserialize, Serialize};

/// Best-effort terminal category shell (one object, one id).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct TerminalCategoryShell {
    pub label: String,
    /// The unique object tag (default "∗").
    pub object: String,
    /// The unique identity morphism name (default "id").
    pub identity: String,
    pub notes: Vec<String>,
}

impl TerminalCategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            object: "∗".into(),
            identity: "id".into(),
            notes: Vec::new(),
        }
    }

    pub fn with_object(label: impl Into<String>, object: impl Into<String>) -> Self {
        let object = object.into();
        Self {
            label: label.into(),
            identity: format!("id_{object}"),
            object,
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
        if self.identity.is_empty() {
            return Err("empty identity".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(TerminalCategoryShell::new("1").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(TerminalCategoryShell::new("").validate_shell().is_err());
    }

    #[test]
    fn with_object_ok() {
        let t = TerminalCategoryShell::with_object("1", "star");
        assert_eq!(t.object, "star");
        assert!(t.validate_shell().is_ok());
    }
}
