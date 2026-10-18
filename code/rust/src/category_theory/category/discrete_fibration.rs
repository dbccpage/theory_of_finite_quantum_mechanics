//! discrete_fibration shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! A discrete fibration p: E → B has unique cartesian lifts of morphisms
//! into each object of E (equivalently: fibers are discrete categories).

use serde::{Deserialize, Serialize};

/// Best-effort discrete fibration shell p: total → base.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiscreteFibrationShell {
    pub label: String,
    pub total_label: String,
    pub base_label: String,
    /// Object map tags: total_object → base_object.
    pub object_map: Vec<(String, String)>,
    pub notes: Vec<String>,
}

impl DiscreteFibrationShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            total_label: String::new(),
            base_label: String::new(),
            object_map: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        total_label: impl Into<String>,
        base_label: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            total_label: total_label.into(),
            base_label: base_label.into(),
            object_map: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.total_label.is_empty() {
            return Err("empty total_label".into());
        }
        if self.base_label.is_empty() {
            return Err("empty base_label".into());
        }
        for (i, (t, b)) in self.object_map.iter().enumerate() {
            if t.is_empty() || b.is_empty() {
                return Err(format!("empty object_map entry at index {i}"));
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
        assert!(DiscreteFibrationShell::between("p", "E", "B")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(DiscreteFibrationShell::new("").validate_shell().is_err());
        assert!(DiscreteFibrationShell::new("p").validate_shell().is_err());
    }
}
