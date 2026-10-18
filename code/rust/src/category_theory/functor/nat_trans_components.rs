//! nat_trans_components shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Explicit component inventory for a natural transformation (shape only).

use serde::{Deserialize, Serialize};

/// Best-effort shell for component data attached to a nat-trans reference.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct NatTransComponents {
    pub label: String,
    pub nat_trans_ref: String,
    /// Component map as (object, morphism) pairs.
    pub components: Vec<(String, String)>,
    pub notes: Vec<String>,
}

impl NatTransComponents {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            nat_trans_ref: String::new(),
            components: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn for_nat_trans(
        label: impl Into<String>,
        nat_trans_ref: impl Into<String>,
        components: Vec<(String, String)>,
    ) -> Self {
        Self {
            label: label.into(),
            nat_trans_ref: nat_trans_ref.into(),
            components,
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.nat_trans_ref.is_empty() {
            return Err("empty nat_trans_ref".into());
        }
        for (i, (obj, mor)) in self.components.iter().enumerate() {
            if obj.is_empty() || mor.is_empty() {
                return Err(format!("empty component tag at index {i}"));
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(
            NatTransComponents::for_nat_trans("comps", "eta", vec![("A".into(), "m".into())])
                .validate_shell()
                .is_ok()
        );
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(NatTransComponents::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_ref() {
        assert!(NatTransComponents::new("x").validate_shell().is_err());
    }
}
