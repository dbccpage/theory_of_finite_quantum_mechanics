//! pullback shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a pullback of a cospan A → C ← B.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Pullback {
    pub label: String,
    pub pullback_object: String,
    /// Cospan left leg domain A (f : A → C).
    pub left_source: String,
    /// Cospan right leg domain B (g : B → C).
    pub right_source: String,
    /// Cospan apex C.
    pub cospan_apex: String,
    /// Cospan morphism f : A → C.
    pub morphism_f: String,
    /// Cospan morphism g : B → C.
    pub morphism_g: String,
    pub projection_left: String,
    pub projection_right: String,
    pub notes: Vec<String>,
}

impl Pullback {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            pullback_object: String::new(),
            left_source: String::new(),
            right_source: String::new(),
            cospan_apex: String::new(),
            morphism_f: String::new(),
            morphism_g: String::new(),
            projection_left: String::new(),
            projection_right: String::new(),
            notes: Vec::new(),
        }
    }

    #[allow(clippy::too_many_arguments)]
    pub fn of_cospan(
        label: impl Into<String>,
        pullback_object: impl Into<String>,
        left_source: impl Into<String>,
        right_source: impl Into<String>,
        cospan_apex: impl Into<String>,
        morphism_f: impl Into<String>,
        morphism_g: impl Into<String>,
        projection_left: impl Into<String>,
        projection_right: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            pullback_object: pullback_object.into(),
            left_source: left_source.into(),
            right_source: right_source.into(),
            cospan_apex: cospan_apex.into(),
            morphism_f: morphism_f.into(),
            morphism_g: morphism_g.into(),
            projection_left: projection_left.into(),
            projection_right: projection_right.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.pullback_object.is_empty() {
            return Err("empty pullback_object".into());
        }
        if self.left_source.is_empty() {
            return Err("empty left_source".into());
        }
        if self.right_source.is_empty() {
            return Err("empty right_source".into());
        }
        if self.cospan_apex.is_empty() {
            return Err("empty cospan_apex".into());
        }
        if self.morphism_f.is_empty() {
            return Err("empty morphism_f".into());
        }
        if self.morphism_g.is_empty() {
            return Err("empty morphism_g".into());
        }
        if self.projection_left.is_empty() {
            return Err("empty projection_left".into());
        }
        if self.projection_right.is_empty() {
            return Err("empty projection_right".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let pb = Pullback::of_cospan("pb", "P", "A", "B", "C", "f", "g", "p₁", "p₂");
        assert!(pb.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Pullback::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_cospan() {
        assert!(Pullback::new("pb").validate_shell().is_err());
    }
}
