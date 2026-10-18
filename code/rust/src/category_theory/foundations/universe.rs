//! universe shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Related contract (if present): `urn:omega:math:type_universe:v0.1.0`.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a type-universe level record (U_i).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Universe {
    pub label: String,
    /// Non-negative universe level index `i` for `U_i`.
    pub level: u32,
    /// Whether lower-level types are included (cumulative hierarchy flag).
    pub cumulative: bool,
    pub notes: Vec<String>,
}

impl Universe {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            level: 0,
            cumulative: true,
            notes: Vec::new(),
        }
    }

    pub fn at_level(label: impl Into<String>, level: u32) -> Self {
        Self {
            label: label.into(),
            level,
            cumulative: true,
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            Err("empty label".into())
        } else {
            Ok(())
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(Universe::new("x").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Universe::new("").validate_shell().is_err());
    }

    #[test]
    fn at_level_sets_level() {
        let u = Universe::at_level("U", 2);
        assert_eq!(u.level, 2);
        assert!(u.validate_shell().is_ok());
    }
}
