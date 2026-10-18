//! coend shell for omega_category_theory (hierarchical; legacy flat coend.rs remains).
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a coend ∫^c F(c,c) of a bifunctor.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Coend {
    pub label: String,
    /// Bifunctor F : C^op × C → D reference.
    pub bifunctor_ref: String,
    /// Indexing category reference.
    pub indexing_category_ref: String,
    /// Coend object (when claimed).
    pub coend_object: String,
    pub notes: Vec<String>,
}

impl Coend {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            bifunctor_ref: String::new(),
            indexing_category_ref: String::new(),
            coend_object: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn of_bifunctor(
        label: impl Into<String>,
        bifunctor_ref: impl Into<String>,
        indexing_category_ref: impl Into<String>,
        coend_object: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            bifunctor_ref: bifunctor_ref.into(),
            indexing_category_ref: indexing_category_ref.into(),
            coend_object: coend_object.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.bifunctor_ref.is_empty() {
            return Err("empty bifunctor_ref".into());
        }
        if self.indexing_category_ref.is_empty() {
            return Err("empty indexing_category_ref".into());
        }
        if self.coend_object.is_empty() {
            return Err("empty coend_object".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let c = Coend::of_bifunctor("coend_F", "F", "C", "∫^F");
        assert!(c.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Coend::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_bifunctor() {
        assert!(Coend::new("c").validate_shell().is_err());
    }
}
