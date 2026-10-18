//! coproduct shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a (binary or multi-summand) coproduct.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Coproduct {
    pub label: String,
    /// Coproduct object.
    pub coproduct_object: String,
    /// Summand object labels.
    pub summands: Vec<String>,
    /// Injection morphism labels (aligned with summands when both present).
    pub injections: Vec<String>,
    pub notes: Vec<String>,
}

impl Coproduct {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            coproduct_object: String::new(),
            summands: Vec::new(),
            injections: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn binary(
        label: impl Into<String>,
        coproduct_object: impl Into<String>,
        left: impl Into<String>,
        right: impl Into<String>,
        injection_left: impl Into<String>,
        injection_right: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            coproduct_object: coproduct_object.into(),
            summands: vec![left.into(), right.into()],
            injections: vec![injection_left.into(), injection_right.into()],
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.coproduct_object.is_empty() {
            return Err("empty coproduct_object".into());
        }
        if self.summands.is_empty() {
            return Err("empty summands".into());
        }
        for (i, s) in self.summands.iter().enumerate() {
            if s.is_empty() {
                return Err(format!("empty summand at index {i}"));
            }
        }
        for (i, j) in self.injections.iter().enumerate() {
            if j.is_empty() {
                return Err(format!("empty injection at index {i}"));
            }
        }
        if !self.injections.is_empty() && self.injections.len() != self.summands.len() {
            return Err("injections length must match summands length".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let c = Coproduct::binary("A+B", "A+B", "A", "B", "ι₁", "ι₂");
        assert!(c.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Coproduct::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_mismatched_injections() {
        let mut c = Coproduct::binary("S", "S", "A", "B", "ι₁", "ι₂");
        c.injections.pop();
        assert!(c.validate_shell().is_err());
    }
}
