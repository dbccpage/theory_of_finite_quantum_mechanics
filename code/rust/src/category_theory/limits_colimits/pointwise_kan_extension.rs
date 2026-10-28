//! pointwise_kan_extension shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use tfqm_category_theory::errors::ArithmosError;
use serde::{Deserialize, Serialize};

use super::kan_extension::KanExtensionKind;

/// Best-effort shell for a pointwise Kan extension (computed objectwise via ends/colimits).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct PointwiseKanExtension {
    pub label: String,
    pub kind: KanExtensionKind,
    /// Functor F being extended.
    pub functor_f: String,
    /// Functor K along which we extend.
    pub along_k: String,
    /// Extension functor reference.
    pub extension_functor: String,
    /// Formula / coend-end construction tag (diagnostic, e.g. "coend" / "end").
    pub pointwise_formula: String,
    pub notes: Vec<String>,
}

impl PointwiseKanExtension {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            kind: KanExtensionKind::Lan,
            functor_f: String::new(),
            along_k: String::new(),
            extension_functor: String::new(),
            pointwise_formula: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn lan_pointwise(
        label: impl Into<String>,
        functor_f: impl Into<String>,
        along_k: impl Into<String>,
        extension_functor: impl Into<String>,
        pointwise_formula: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            kind: KanExtensionKind::Lan,
            functor_f: functor_f.into(),
            along_k: along_k.into(),
            extension_functor: extension_functor.into(),
            pointwise_formula: pointwise_formula.into(),
            notes: Vec::new(),
        }
    }

    pub fn ran_pointwise(
        label: impl Into<String>,
        functor_f: impl Into<String>,
        along_k: impl Into<String>,
        extension_functor: impl Into<String>,
        pointwise_formula: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            kind: KanExtensionKind::Ran,
            functor_f: functor_f.into(),
            along_k: along_k.into(),
            extension_functor: extension_functor.into(),
            pointwise_formula: pointwise_formula.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.functor_f.is_empty() {
            return Err(ArithmosError::InvalidShape("empty functor_f".into()));
        }
        if self.along_k.is_empty() {
            return Err(ArithmosError::InvalidShape("empty along_k".into()));
        }
        if self.extension_functor.is_empty() {
            return Err(ArithmosError::InvalidShape("empty extension_functor".into()));
        }
        if self.pointwise_formula.is_empty() {
            return Err(ArithmosError::InvalidShape("empty pointwise_formula".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn lan_validate_ok() {
        let p = PointwiseKanExtension::lan_pointwise("pLan", "F", "K", "Lan", "coend");
        assert_eq!(p.kind, KanExtensionKind::Lan);
        assert!(p.validate_shell().is_ok());
    }

    #[test]
    fn ran_validate_ok() {
        let p = PointwiseKanExtension::ran_pointwise("pRan", "F", "K", "Ran", "end");
        assert_eq!(p.kind, KanExtensionKind::Ran);
        assert!(p.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(PointwiseKanExtension::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_formula() {
        assert!(PointwiseKanExtension::new("p").validate_shell().is_err());
    }
}
