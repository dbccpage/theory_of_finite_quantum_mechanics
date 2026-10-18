//! hom_functor shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Hom-functor Hom(A, −) / Hom(−, A) — shape only.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a Hom-functor on a category reference.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct HomFunctor {
    pub label: String,
    pub category_ref: String,
    /// Fixed object in the Hom-slot.
    pub fixed_object: String,
    /// Variance tag: "covariant" (Hom(A,−)) or "contravariant" (Hom(−,A)).
    pub variance: String,
    pub notes: Vec<String>,
}

impl HomFunctor {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            category_ref: String::new(),
            fixed_object: String::new(),
            variance: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn covariant(
        label: impl Into<String>,
        category_ref: impl Into<String>,
        fixed_object: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            category_ref: category_ref.into(),
            fixed_object: fixed_object.into(),
            variance: "covariant".into(),
            notes: Vec::new(),
        }
    }

    pub fn contravariant(
        label: impl Into<String>,
        category_ref: impl Into<String>,
        fixed_object: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            category_ref: category_ref.into(),
            fixed_object: fixed_object.into(),
            variance: "contravariant".into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.category_ref.is_empty() {
            return Err("empty category_ref".into());
        }
        if self.fixed_object.is_empty() {
            return Err("empty fixed_object".into());
        }
        if self.variance.is_empty() {
            return Err("empty variance".into());
        }
        match self.variance.as_str() {
            "covariant" | "contravariant" => Ok(()),
            other => Err(format!("unknown variance tag: {other}")),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(HomFunctor::covariant("HomA", "C", "A")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(HomFunctor::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_bad_variance() {
        let mut h = HomFunctor::covariant("h", "C", "A");
        h.variance = "both".into();
        assert!(h.validate_shell().is_err());
    }

    #[test]
    fn contravariant_ok() {
        assert!(HomFunctor::contravariant("Hom_A", "C", "A")
            .validate_shell()
            .is_ok());
    }
}
