//! hlevel shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Homotopy h-level / n-type classification shell (shape only).

use serde::{Deserialize, Serialize};

/// Best-effort shell for an h-level claim on a type reference.
///
/// Convention: `level` uses the integer n in "is-n-type", with n ≥ -2
/// represented as a signed integer. Shape validation only.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct HLevel {
    pub label: String,
    /// Integer h-level n (caller convention: n ≥ -2).
    pub level: i32,
    /// Optional type reference being classified.
    pub type_ref: String,
    pub notes: Vec<String>,
}

impl HLevel {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            level: 0,
            type_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn for_type(label: impl Into<String>, type_ref: impl Into<String>, level: i32) -> Self {
        Self {
            label: label.into(),
            level,
            type_ref: type_ref.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.level < -2 {
            return Err(format!("h-level {} < -2", self.level));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(HLevel::new("x").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(HLevel::new("").validate_shell().is_err());
    }

    #[test]
    fn rejects_below_minus_two() {
        let h = HLevel::for_type("bad", "A", -3);
        assert!(h.validate_shell().is_err());
    }

    #[test]
    fn contractible_level_ok() {
        let h = HLevel::for_type("contr", "A", -2);
        assert!(h.validate_shell().is_ok());
    }
}
