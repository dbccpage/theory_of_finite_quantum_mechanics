//! kan_extension shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Left or right Kan extension kind.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum KanExtensionKind {
    /// Left Kan extension Lan_K F.
    #[default]
    Lan,
    /// Right Kan extension Ran_K F.
    Ran,
}

/// Best-effort shell for a (global) Kan extension along a functor.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct KanExtension {
    pub label: String,
    /// Extension kind: left (Lan) or right (Ran).
    pub kind: KanExtensionKind,
    /// Functor F being extended.
    pub functor_f: String,
    /// Functor K along which we extend (Lan_K F / Ran_K F).
    pub along_k: String,
    /// Extension functor (Lan_K F or Ran_K F) reference when claimed.
    pub extension_functor: String,
    /// Unit/counit natural transformation label (diagnostic).
    pub unit_counit_ref: String,
    pub notes: Vec<String>,
}

impl KanExtension {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            kind: KanExtensionKind::Lan,
            functor_f: String::new(),
            along_k: String::new(),
            extension_functor: String::new(),
            unit_counit_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn lan(
        label: impl Into<String>,
        functor_f: impl Into<String>,
        along_k: impl Into<String>,
        extension_functor: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            kind: KanExtensionKind::Lan,
            functor_f: functor_f.into(),
            along_k: along_k.into(),
            extension_functor: extension_functor.into(),
            unit_counit_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn ran(
        label: impl Into<String>,
        functor_f: impl Into<String>,
        along_k: impl Into<String>,
        extension_functor: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            kind: KanExtensionKind::Ran,
            functor_f: functor_f.into(),
            along_k: along_k.into(),
            extension_functor: extension_functor.into(),
            unit_counit_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.functor_f.is_empty() {
            return Err("empty functor_f".into());
        }
        if self.along_k.is_empty() {
            return Err("empty along_k".into());
        }
        if self.extension_functor.is_empty() {
            return Err("empty extension_functor".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn lan_validate_ok() {
        let k = KanExtension::lan("Lan_K F", "F", "K", "Lan");
        assert_eq!(k.kind, KanExtensionKind::Lan);
        assert!(k.validate_shell().is_ok());
    }

    #[test]
    fn ran_validate_ok() {
        let k = KanExtension::ran("Ran_K F", "F", "K", "Ran");
        assert_eq!(k.kind, KanExtensionKind::Ran);
        assert!(k.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(KanExtension::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_functors() {
        assert!(KanExtension::new("k").validate_shell().is_err());
    }

    #[test]
    fn kind_default_is_lan() {
        assert_eq!(KanExtensionKind::default(), KanExtensionKind::Lan);
    }
}
