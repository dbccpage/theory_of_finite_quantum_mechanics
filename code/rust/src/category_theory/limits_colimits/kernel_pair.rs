//! kernel_pair shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

/// Best-effort shell for a kernel pair of a morphism f : A → B
/// (pullback of f along itself).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct KernelPair {
    pub label: String,
    /// Kernel-pair object R ⇉ A.
    pub pair_object: String,
    pub source: String,
    pub target: String,
    /// Morphism f : source → target whose kernel pair is taken.
    pub morphism_f: String,
    /// Left projection R → source.
    pub projection_left: String,
    /// Right projection R → source.
    pub projection_right: String,
    pub notes: Vec<String>,
}

impl KernelPair {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            pair_object: String::new(),
            source: String::new(),
            target: String::new(),
            morphism_f: String::new(),
            projection_left: String::new(),
            projection_right: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn of_morphism(
        label: impl Into<String>,
        pair_object: impl Into<String>,
        source: impl Into<String>,
        target: impl Into<String>,
        morphism_f: impl Into<String>,
        projection_left: impl Into<String>,
        projection_right: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            pair_object: pair_object.into(),
            source: source.into(),
            target: target.into(),
            morphism_f: morphism_f.into(),
            projection_left: projection_left.into(),
            projection_right: projection_right.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.pair_object.is_empty() {
            return Err(ArithmosError::InvalidShape("empty pair_object".into()));
        }
        if self.source.is_empty() {
            return Err(ArithmosError::InvalidShape("empty source".into()));
        }
        if self.target.is_empty() {
            return Err(ArithmosError::InvalidShape("empty target".into()));
        }
        if self.morphism_f.is_empty() {
            return Err(ArithmosError::InvalidShape("empty morphism_f".into()));
        }
        if self.projection_left.is_empty() {
            return Err(ArithmosError::InvalidShape("empty projection_left".into()));
        }
        if self.projection_right.is_empty() {
            return Err(ArithmosError::InvalidShape("empty projection_right".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let k = KernelPair::of_morphism("kp", "R", "A", "B", "f", "p₁", "p₂");
        assert!(k.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(KernelPair::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_morphism() {
        assert!(KernelPair::new("kp").validate_shell().is_err());
    }
}
