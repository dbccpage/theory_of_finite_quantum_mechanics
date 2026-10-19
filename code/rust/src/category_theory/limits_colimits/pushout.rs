//! pushout shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for a pushout of a span A ← C → B.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Pushout {
    pub label: String,
    pub pushout_object: String,
    /// Span left leg codomain A (f : C → A).
    pub left_target: String,
    /// Span right leg codomain B (g : C → B).
    pub right_target: String,
    /// Span base C.
    pub span_base: String,
    /// Span morphism f : C → A.
    pub morphism_f: String,
    /// Span morphism g : C → B.
    pub morphism_g: String,
    pub injection_left: String,
    pub injection_right: String,
    pub notes: Vec<String>,
}

impl Pushout {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            pushout_object: String::new(),
            left_target: String::new(),
            right_target: String::new(),
            span_base: String::new(),
            morphism_f: String::new(),
            morphism_g: String::new(),
            injection_left: String::new(),
            injection_right: String::new(),
            notes: Vec::new(),
        }
    }

    #[allow(clippy::too_many_arguments)]
    pub fn of_span(
        label: impl Into<String>,
        pushout_object: impl Into<String>,
        left_target: impl Into<String>,
        right_target: impl Into<String>,
        span_base: impl Into<String>,
        morphism_f: impl Into<String>,
        morphism_g: impl Into<String>,
        injection_left: impl Into<String>,
        injection_right: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            pushout_object: pushout_object.into(),
            left_target: left_target.into(),
            right_target: right_target.into(),
            span_base: span_base.into(),
            morphism_f: morphism_f.into(),
            morphism_g: morphism_g.into(),
            injection_left: injection_left.into(),
            injection_right: injection_right.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.pushout_object.is_empty() {
            return Err(ArithmosError::InvalidShape("empty pushout_object".into()));
        }
        if self.left_target.is_empty() {
            return Err(ArithmosError::InvalidShape("empty left_target".into()));
        }
        if self.right_target.is_empty() {
            return Err(ArithmosError::InvalidShape("empty right_target".into()));
        }
        if self.span_base.is_empty() {
            return Err(ArithmosError::InvalidShape("empty span_base".into()));
        }
        if self.morphism_f.is_empty() {
            return Err(ArithmosError::InvalidShape("empty morphism_f".into()));
        }
        if self.morphism_g.is_empty() {
            return Err(ArithmosError::InvalidShape("empty morphism_g".into()));
        }
        if self.injection_left.is_empty() {
            return Err(ArithmosError::InvalidShape("empty injection_left".into()));
        }
        if self.injection_right.is_empty() {
            return Err(ArithmosError::InvalidShape("empty injection_right".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let po = Pushout::of_span("po", "P", "A", "B", "C", "f", "g", "i₁", "i₂");
        assert!(po.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Pushout::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_span() {
        assert!(Pushout::new("po").validate_shell().is_err());
    }
}
