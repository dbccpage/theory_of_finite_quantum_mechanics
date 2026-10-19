//! truncation shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Related contract (if present): `urn:omega:math:truncation_level:v0.1.0`.

use omega_category_theory::errors::ArithmosError;
use serde::{Deserialize, Serialize};

/// Best-effort shell for an n-truncation claim / level tag.
///
/// Does not implement the truncation HIT; shape / inventory only.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Truncation {
    pub label: String,
    /// Truncation level n (caller convention: n ≥ -2; None = untruncated).
    pub level: Option<i32>,
    /// Optional type reference being truncated.
    pub type_ref: String,
    pub notes: Vec<String>,
}

impl Truncation {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            level: Some(0),
            type_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn at_level(label: impl Into<String>, level: i32) -> Self {
        Self {
            label: label.into(),
            level: Some(level),
            type_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn untruncated(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            level: None,
            type_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if let Some(n) = self.level {
            if n < -2 {
                return Err(ArithmosError::InvalidShape(format!("truncation level {n} < -2")));
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(Truncation::new("x").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Truncation::new("").validate_shell().is_err());
    }

    #[test]
    fn untruncated_ok() {
        assert!(Truncation::untruncated("∞").validate_shell().is_ok());
    }

    #[test]
    fn rejects_below_minus_two() {
        assert!(Truncation::at_level("bad", -3).validate_shell().is_err());
    }
}
