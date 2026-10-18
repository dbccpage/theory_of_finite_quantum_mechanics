//! coequalizer shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a coequalizer of a parallel pair.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Coequalizer {
    pub label: String,
    pub coequalizer_object: String,
    pub source: String,
    pub target: String,
    pub morphism_f: String,
    pub morphism_g: String,
    /// Coequalizer morphism q : target → Q with q∘f = q∘g.
    pub coequalizer_morphism: String,
    pub notes: Vec<String>,
}

impl Coequalizer {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            coequalizer_object: String::new(),
            source: String::new(),
            target: String::new(),
            morphism_f: String::new(),
            morphism_g: String::new(),
            coequalizer_morphism: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn of_pair(
        label: impl Into<String>,
        coequalizer_object: impl Into<String>,
        source: impl Into<String>,
        target: impl Into<String>,
        morphism_f: impl Into<String>,
        morphism_g: impl Into<String>,
        coequalizer_morphism: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            coequalizer_object: coequalizer_object.into(),
            source: source.into(),
            target: target.into(),
            morphism_f: morphism_f.into(),
            morphism_g: morphism_g.into(),
            coequalizer_morphism: coequalizer_morphism.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.coequalizer_object.is_empty() {
            return Err("empty coequalizer_object".into());
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
        if self.morphism_g.is_empty() {
            return Err("empty morphism_g".into());
        }
        if self.coequalizer_morphism.is_empty() {
            return Err("empty coequalizer_morphism".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let c = Coequalizer::of_pair("coeq", "Q", "A", "B", "f", "g", "q");
        assert!(c.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Coequalizer::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_morphism() {
        assert!(Coequalizer::new("coeq").validate_shell().is_err());
    }
}
