//! fibered_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! A cloven / fibered category over a base: p: E → B with cartesian lifts
//! (Grothendieck fibration data recorded diagnostically).

use omega_category_theory::errors::ArithmosError;
use serde::{Deserialize, Serialize};

/// Best-effort fibered category shell over a base.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiberedCategoryShell {
    pub label: String,
    pub total_label: String,
    pub base_label: String,
    /// Cleavage claim: cartesian lifts are chosen (diagnostic flag).
    pub cloven: bool,
    /// Optional fiber labels over base objects: (base_object, fiber_label).
    pub fibers: Vec<(String, String)>,
    pub notes: Vec<String>,
}

impl FiberedCategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            total_label: String::new(),
            base_label: String::new(),
            cloven: false,
            fibers: Vec::new(),
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
            fibers: Vec::new(),
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
        for (i, (b, f)) in self.fibers.iter().enumerate() {
            if b.is_empty() || f.is_empty() {
                return Err(ArithmosError::InvalidShape(format!("empty fiber entry at index {i}")));
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
        assert!(FiberedCategoryShell::over("Fib", "E", "B")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(FiberedCategoryShell::new("").validate_shell().is_err());
        assert!(FiberedCategoryShell::new("F").validate_shell().is_err());
    }
}
