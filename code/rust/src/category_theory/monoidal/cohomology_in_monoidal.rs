//! cohomology_in_monoidal shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort shell for cohomology computed in / valued in a monoidal category.
/// Diagnostic inventory only — not a spectral-sequence certificate.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct CohomologyInMonoidal {
    pub label: String,
    /// Ambient monoidal category shell label (coefficients / target).
    pub monoidal_ref: String,
    /// Cochain / chain complex ref.
    pub complex_ref: String,
    /// Degree index tag (e.g. "n", "2").
    pub degree: String,
    /// Optional cohomology object / group label at that degree.
    pub cohomology_object: String,
    pub notes: Vec<String>,
}

impl CohomologyInMonoidal {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: String::new(),
            complex_ref: String::new(),
            degree: String::new(),
            cohomology_object: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn at_degree(
        label: impl Into<String>,
        monoidal_ref: impl Into<String>,
        complex_ref: impl Into<String>,
        degree: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: monoidal_ref.into(),
            complex_ref: complex_ref.into(),
            degree: degree.into(),
            cohomology_object: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.monoidal_ref.is_empty() {
            return Err("empty monoidal_ref".into());
        }
        if self.complex_ref.is_empty() {
            return Err("empty complex_ref".into());
        }
        if self.degree.is_empty() {
            return Err("empty degree".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(CohomologyInMonoidal::at_degree("H", "Ab", "Cdot", "2")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(CohomologyInMonoidal::new("").validate_shell().is_err());
    }
}
