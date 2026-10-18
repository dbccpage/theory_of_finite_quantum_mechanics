//! coalgebra_for_comonad shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! A coalgebra for a comonad W is a carrier A with structure map k : A → W(A).
//! Shell holds carrier + structure-map labels and a comonad ref.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a labeled W-coalgebra (A, k).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct CoalgebraForComonad {
    pub label: String,
    /// Carrier object label A.
    pub carrier_label: String,
    /// Structure map label k : A → W(A).
    pub structure_map_label: String,
    /// Ref to the ambient comonad W.
    pub comonad_ref: String,
    pub notes: Vec<String>,
}

impl CoalgebraForComonad {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            carrier_label: String::new(),
            structure_map_label: String::new(),
            comonad_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_structure(
        label: impl Into<String>,
        carrier_label: impl Into<String>,
        structure_map_label: impl Into<String>,
        comonad_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            carrier_label: carrier_label.into(),
            structure_map_label: structure_map_label.into(),
            comonad_ref: comonad_ref.into(),
            notes: Vec::new(),
        }
    }

    pub fn with_note(mut self, note: impl Into<String>) -> Self {
        self.notes.push(note.into());
        self
    }

    /// Validate structural emptiness only (shell gate).
    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.carrier_label.is_empty() {
            return Err("empty carrier_label".into());
        }
        if self.structure_map_label.is_empty() {
            return Err("empty structure_map_label".into());
        }
        if self.comonad_ref.is_empty() {
            return Err("empty comonad_ref".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let c = CoalgebraForComonad::with_structure("stream_coalg", "Stream", "k_stream", "Env");
        assert!(c.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(CoalgebraForComonad::new("").validate_shell().is_err());
        assert!(CoalgebraForComonad::new("c").validate_shell().is_err());
    }
}
