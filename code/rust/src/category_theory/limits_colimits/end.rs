//! end shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for an end ∫_c F(c,c) of a bifunctor.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct End {
    pub label: String,
    /// Bifunctor F : C^op × C → D reference.
    pub bifunctor_ref: String,
    /// Indexing category reference.
    pub indexing_category_ref: String,
    /// End object (when claimed).
    pub end_object: String,
    pub notes: Vec<String>,
}

impl End {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            bifunctor_ref: String::new(),
            indexing_category_ref: String::new(),
            end_object: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn of_bifunctor(
        label: impl Into<String>,
        bifunctor_ref: impl Into<String>,
        indexing_category_ref: impl Into<String>,
        end_object: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            bifunctor_ref: bifunctor_ref.into(),
            indexing_category_ref: indexing_category_ref.into(),
            end_object: end_object.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.bifunctor_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty bifunctor_ref".into()));
        }
        if self.indexing_category_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty indexing_category_ref".into()));
        }
        if self.end_object.is_empty() {
            return Err(ArithmosError::InvalidShape("empty end_object".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let e = End::of_bifunctor("end_F", "F", "C", "∫F");
        assert!(e.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(End::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_bifunctor() {
        assert!(End::new("e").validate_shell().is_err());
    }
}
