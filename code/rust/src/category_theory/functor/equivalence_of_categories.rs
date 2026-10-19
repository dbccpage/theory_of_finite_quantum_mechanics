//! equivalence_of_categories shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Equivalence C ≃ D via functors + unit/counit refs — shape only, not a proof.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for an equivalence of categories claim.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct EquivalenceOfCategories {
    pub label: String,
    pub left_functor_ref: String,
    pub right_functor_ref: String,
    /// Optional unit natural transformation η : Id ⇒ G F.
    pub unit_nat_trans_ref: String,
    /// Optional counit natural transformation ε : F G ⇒ Id.
    pub counit_nat_trans_ref: String,
    pub notes: Vec<String>,
}

impl EquivalenceOfCategories {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            left_functor_ref: String::new(),
            right_functor_ref: String::new(),
            unit_nat_trans_ref: String::new(),
            counit_nat_trans_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        left_functor_ref: impl Into<String>,
        right_functor_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            left_functor_ref: left_functor_ref.into(),
            right_functor_ref: right_functor_ref.into(),
            unit_nat_trans_ref: String::new(),
            counit_nat_trans_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.left_functor_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty left_functor_ref".into()));
        }
        if self.right_functor_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty right_functor_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(EquivalenceOfCategories::between("eq", "F", "G")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(EquivalenceOfCategories::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_functors() {
        assert!(EquivalenceOfCategories::new("eq").validate_shell().is_err());
    }
}
