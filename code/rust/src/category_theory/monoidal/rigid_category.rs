//! rigid_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort rigid (autonomous) monoidal category shell.
/// Left and right duals with zig-zag (snake) identities claimed via refs.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct RigidCategory {
    pub label: String,
    /// Underlying monoidal category shell label.
    pub monoidal_ref: String,
    /// Left dual assignment ref.
    pub left_dual_ref: String,
    /// Right dual assignment ref.
    pub right_dual_ref: String,
    /// Left unit/counit pair refs (η^L, ε^L).
    pub left_unit_ref: String,
    pub left_counit_ref: String,
    /// Right unit/counit pair refs (η^R, ε^R).
    pub right_unit_ref: String,
    pub right_counit_ref: String,
    pub notes: Vec<String>,
}

impl RigidCategory {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: String::new(),
            left_dual_ref: String::new(),
            right_dual_ref: String::new(),
            left_unit_ref: String::new(),
            left_counit_ref: String::new(),
            right_unit_ref: String::new(),
            right_counit_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_duals(
        label: impl Into<String>,
        monoidal_ref: impl Into<String>,
        left_dual_ref: impl Into<String>,
        right_dual_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: monoidal_ref.into(),
            left_dual_ref: left_dual_ref.into(),
            right_dual_ref: right_dual_ref.into(),
            left_unit_ref: String::new(),
            left_counit_ref: String::new(),
            right_unit_ref: String::new(),
            right_counit_ref: String::new(),
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
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(RigidCategory::with_duals("Rigid", "Mon", "AL", "AR")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(RigidCategory::new("").validate_shell().is_err());
    }
}
