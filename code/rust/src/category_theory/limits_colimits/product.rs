//! product shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a (binary or multi-factor) product.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Product {
    pub label: String,
    /// Product object.
    pub product_object: String,
    /// Factor object labels.
    pub factors: Vec<String>,
    /// Projection morphism labels (aligned with factors when both present).
    pub projections: Vec<String>,
    pub notes: Vec<String>,
}

impl Product {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            product_object: String::new(),
            factors: Vec::new(),
            projections: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn binary(
        label: impl Into<String>,
        product_object: impl Into<String>,
        left: impl Into<String>,
        right: impl Into<String>,
        projection_left: impl Into<String>,
        projection_right: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            product_object: product_object.into(),
            factors: vec![left.into(), right.into()],
            projections: vec![projection_left.into(), projection_right.into()],
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.product_object.is_empty() {
            return Err("empty product_object".into());
        }
        if self.factors.is_empty() {
            return Err("empty factors".into());
        }
        for (i, f) in self.factors.iter().enumerate() {
            if f.is_empty() {
                return Err(format!("empty factor at index {i}"));
            }
        }
        for (i, p) in self.projections.iter().enumerate() {
            if p.is_empty() {
                return Err(format!("empty projection at index {i}"));
            }
        }
        if !self.projections.is_empty() && self.projections.len() != self.factors.len() {
            return Err("projections length must match factors length".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let p = Product::binary("A×B", "A×B", "A", "B", "π₁", "π₂");
        assert!(p.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Product::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_mismatched_projections() {
        let mut p = Product::binary("P", "P", "A", "B", "π₁", "π₂");
        p.projections.pop();
        assert!(p.validate_shell().is_err());
    }
}
