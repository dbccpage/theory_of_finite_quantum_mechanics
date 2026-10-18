//! cokernel_pair shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a cokernel pair of a morphism f : A → B
/// (pushout of f along itself).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct CokernelPair {
    pub label: String,
    /// Cokernel-pair object B ⇉ Q.
    pub pair_object: String,
    pub source: String,
    pub target: String,
    /// Morphism f : source → target whose cokernel pair is taken.
    pub morphism_f: String,
    /// Left injection target → Q.
    pub injection_left: String,
    /// Right injection target → Q.
    pub injection_right: String,
    pub notes: Vec<String>,
}

impl CokernelPair {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            pair_object: String::new(),
            source: String::new(),
            target: String::new(),
            morphism_f: String::new(),
            injection_left: String::new(),
            injection_right: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn of_morphism(
        label: impl Into<String>,
        pair_object: impl Into<String>,
        source: impl Into<String>,
        target: impl Into<String>,
        morphism_f: impl Into<String>,
        injection_left: impl Into<String>,
        injection_right: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            pair_object: pair_object.into(),
            source: source.into(),
            target: target.into(),
            morphism_f: morphism_f.into(),
            injection_left: injection_left.into(),
            injection_right: injection_right.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.pair_object.is_empty() {
            return Err("empty pair_object".into());
        }
        if self.source.is_empty() {
            return Err("empty source".into());
        }
        if self.target.is_empty() {
            return Err("empty target".into());
        }
        if self.morphism_f.is_empty() {
            return Err("empty morphism_f".into());
        }
        if self.injection_left.is_empty() {
            return Err("empty injection_left".into());
        }
        if self.injection_right.is_empty() {
            return Err("empty injection_right".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let c = CokernelPair::of_morphism("ckp", "Q", "A", "B", "f", "i₁", "i₂");
        assert!(c.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(CokernelPair::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_morphism() {
        assert!(CokernelPair::new("ckp").validate_shell().is_err());
    }
}
