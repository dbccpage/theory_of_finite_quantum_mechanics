//! cone / cocone shells for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use omega_category_theory::errors::ArithmosError;
use serde::{Deserialize, Serialize};

/// Add shape location while preserving every other typed failure unchanged.
pub(super) fn shape_context(location: &str, error: ArithmosError) -> ArithmosError {
    match error {
        ArithmosError::InvalidShape(detail) => {
            ArithmosError::InvalidShape(format!("{location}: {detail}"))
        }
        other => other,
    }
}

/// One cone/cocone leg: diagram index → morphism label.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct ConeLeg {
    pub index: String,
    pub morphism_label: String,
}

/// Best-effort shell for a cone over a diagram (apex + legs).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Cone {
    pub label: String,
    pub apex: String,
    /// Legs as (index, morphism_label) pairs (apex → diagram object).
    pub legs: Vec<ConeLeg>,
    pub notes: Vec<String>,
}

impl Cone {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            apex: String::new(),
            legs: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_apex(label: impl Into<String>, apex: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            apex: apex.into(),
            legs: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_leg(&mut self, index: impl Into<String>, morphism_label: impl Into<String>) {
        self.legs.push(ConeLeg {
            index: index.into(),
            morphism_label: morphism_label.into(),
        });
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.apex.is_empty() {
            return Err(ArithmosError::InvalidShape("empty apex".into()));
        }
        for (i, leg) in self.legs.iter().enumerate() {
            if leg.index.is_empty() || leg.morphism_label.is_empty() {
                return Err(ArithmosError::InvalidShape(format!(
                    "empty leg tag at index {i}"
                )));
            }
        }
        Ok(())
    }
}

/// Best-effort shell for a cocone under a diagram (nadir + legs).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Cocone {
    pub label: String,
    pub nadir: String,
    /// Legs as (index, morphism_label) pairs (diagram object → nadir).
    pub legs: Vec<ConeLeg>,
    pub notes: Vec<String>,
}

impl Cocone {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            nadir: String::new(),
            legs: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_nadir(label: impl Into<String>, nadir: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            nadir: nadir.into(),
            legs: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_leg(&mut self, index: impl Into<String>, morphism_label: impl Into<String>) {
        self.legs.push(ConeLeg {
            index: index.into(),
            morphism_label: morphism_label.into(),
        });
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.nadir.is_empty() {
            return Err(ArithmosError::InvalidShape("empty nadir".into()));
        }
        for (i, leg) in self.legs.iter().enumerate() {
            if leg.index.is_empty() || leg.morphism_label.is_empty() {
                return Err(ArithmosError::InvalidShape(format!(
                    "empty leg tag at index {i}"
                )));
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn cone_validate_ok() {
        let mut c = Cone::with_apex("c", "L");
        c.with_leg("A", "π₁");
        assert!(c.validate_shell().is_ok());
    }

    #[test]
    fn cone_rejects_empty_apex() {
        assert!(Cone::new("c").validate_shell().is_err());
    }

    #[test]
    fn cone_rejects_empty_label() {
        assert!(Cone::with_apex("", "L").validate_shell().is_err());
    }

    #[test]
    fn cone_rejects_empty_leg() {
        let mut c = Cone::with_apex("c", "L");
        c.with_leg("", "π");
        assert!(c.validate_shell().is_err());
    }

    #[test]
    fn cocone_validate_ok() {
        let mut c = Cocone::with_nadir("cc", "Q");
        c.with_leg("A", "ι₁");
        assert!(c.validate_shell().is_ok());
    }

    #[test]
    fn cocone_rejects_empty_nadir() {
        assert!(Cocone::new("cc").validate_shell().is_err());
    }
}
