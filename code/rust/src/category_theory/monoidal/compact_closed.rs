//! compact_closed shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort compact closed category shell.
/// Duals + unit/counit (cup/cap) refs; typically symmetric monoidal.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct CompactClosed {
    pub label: String,
    /// Underlying (symmetric) monoidal category shell label.
    pub monoidal_ref: String,
    /// Left dual assignment ref (A ↦ A*).
    pub left_dual_ref: String,
    /// Right dual assignment ref (often coincides with left).
    pub right_dual_ref: String,
    /// Unit (cup) η : I → A* ⊗ A ref family.
    pub unit_ref: String,
    /// Counit (cap) ε : A ⊗ A* → I ref family.
    pub counit_ref: String,
    pub notes: Vec<String>,
}

impl CompactClosed {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: String::new(),
            left_dual_ref: String::new(),
            right_dual_ref: String::new(),
            unit_ref: String::new(),
            counit_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_duals(
        label: impl Into<String>,
        monoidal_ref: impl Into<String>,
        dual_ref: impl Into<String>,
        unit_ref: impl Into<String>,
        counit_ref: impl Into<String>,
    ) -> Self {
        let d = dual_ref.into();
        Self {
            label: label.into(),
            monoidal_ref: monoidal_ref.into(),
            left_dual_ref: d.clone(),
            right_dual_ref: d,
            unit_ref: unit_ref.into(),
            counit_ref: counit_ref.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.monoidal_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty monoidal_ref".into()));
        }
        if self.left_dual_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty left_dual_ref".into()));
        }
        if self.right_dual_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty right_dual_ref".into()));
        }
        if self.unit_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty unit_ref".into()));
        }
        if self.counit_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty counit_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(
            CompactClosed::with_duals("FdVect", "tensor", "*", "eta", "eps")
                .validate_shell()
                .is_ok()
        );
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(CompactClosed::new("").validate_shell().is_err());
    }
}
