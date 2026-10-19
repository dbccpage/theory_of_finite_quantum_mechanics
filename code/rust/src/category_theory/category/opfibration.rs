//! opfibration shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! An opfibration (cocartesian fibration) p: E → B has cocartesian lifts
//! of morphisms out of each object of E.

use omega_category_theory::errors::ArithmosError;
use serde::{Deserialize, Serialize};

/// Best-effort opfibration shell p: total → base.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct OpfibrationShell {
    pub label: String,
    pub total_label: String,
    pub base_label: String,
    /// Cleavage claim: cocartesian lifts are chosen (diagnostic flag).
    pub cloven: bool,
    /// Optional cofiber labels over base objects: (base_object, cofiber_label).
    pub cofibers: Vec<(String, String)>,
    pub notes: Vec<String>,
}

impl OpfibrationShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            total_label: String::new(),
            base_label: String::new(),
            cloven: false,
            cofibers: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn over(
        label: impl Into<String>,
        total_label: impl Into<String>,
        base_label: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            total_label: total_label.into(),
            base_label: base_label.into(),
            cloven: false,
            cofibers: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.total_label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty total_label".into()));
        }
        if self.base_label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty base_label".into()));
        }
        for (i, (b, c)) in self.cofibers.iter().enumerate() {
            if b.is_empty() || c.is_empty() {
                return Err(ArithmosError::InvalidShape(format!("empty cofiber entry at index {i}")));
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
        assert!(OpfibrationShell::over("Opf", "E", "B")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(OpfibrationShell::new("").validate_shell().is_err());
        assert!(OpfibrationShell::new("O").validate_shell().is_err());
    }
}
