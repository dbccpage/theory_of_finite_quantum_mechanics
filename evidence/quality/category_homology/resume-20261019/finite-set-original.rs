//! finite_set shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Related contract (if present): `urn:omega:math:finite_set:v0.1.0`.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a finite set with explicit element inventory.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiniteSet {
    pub label: String,
    /// Finite element tags (canonical identifiers or hashes as strings).
    pub elements: Vec<String>,
    /// Declared cardinality; when set, must match `elements.len()` for validation.
    pub declared_cardinality: Option<usize>,
    pub notes: Vec<String>,
}

impl FiniteSet {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            elements: Vec::new(),
            declared_cardinality: Some(0),
            notes: Vec::new(),
        }
    }

    pub fn with_elements(label: impl Into<String>, elements: Vec<String>) -> Self {
        let n = elements.len();
        Self {
            label: label.into(),
            elements,
            declared_cardinality: Some(n),
            notes: Vec::new(),
        }
    }

    pub fn cardinality(&self) -> usize {
        self.elements.len()
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.trim().is_empty() {
            return Err("empty label".into());
        }
        let mut seen = std::collections::BTreeSet::new();
        for (i, e) in self.elements.iter().enumerate() {
            if e.trim().is_empty() {
                return Err(format!("empty element tag at index {i}"));
            }
            if !seen.insert(e) {
                return Err(format!("duplicate element tag at index {i}"));
            }
        }
        if let Some(n) = self.declared_cardinality {
            if n != self.elements.len() {
                return Err(format!(
                    "declared_cardinality {n} != elements.len() {}",
                    self.elements.len()
                ));
            }
        }
        Ok(())
    }
}

/// A finite set whose distinct, nonempty elements and cardinality were checked.
/// The declaration stays mutable until admission; admitted data is immutable.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(try_from = "FiniteSet", into = "FiniteSet")]
pub struct ValidatedFiniteSet {
    declared: FiniteSet,
}

impl TryFrom<FiniteSet> for ValidatedFiniteSet {
    type Error = String;
    fn try_from(declared: FiniteSet) -> Result<Self, String> {
        declared.validate_shell()?;
        Ok(Self { declared })
    }
}

impl From<ValidatedFiniteSet> for FiniteSet {
    fn from(value: ValidatedFiniteSet) -> Self {
        value.declared
    }
}

impl ValidatedFiniteSet {
    pub fn declared(&self) -> &FiniteSet {
        &self.declared
    }
    pub fn label(&self) -> &str {
        &self.declared.label
    }
    pub fn elements(&self) -> &[String] {
        &self.declared.elements
    }
    pub fn cardinality(&self) -> usize {
        self.declared.cardinality()
    }
    pub fn contains(&self, value: &str) -> bool {
        self.declared.elements.iter().any(|e| e == value)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(FiniteSet::new("x").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(FiniteSet::new("").validate_shell().is_err());
    }

    #[test]
    fn with_elements_ok() {
        let s = FiniteSet::with_elements("F", vec!["0".into(), "1".into()]);
        assert_eq!(s.cardinality(), 2);
        assert!(s.validate_shell().is_ok());
    }

    #[test]
    fn rejects_cardinality_mismatch() {
        let mut s = FiniteSet::with_elements("F", vec!["a".into()]);
        s.declared_cardinality = Some(3);
        assert!(s.validate_shell().is_err());
    }
}
