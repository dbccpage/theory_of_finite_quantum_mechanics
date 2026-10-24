//! Functor shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Covariant functor F : C → D as a labeled finite record (shape only).

use crate::errors::ArithmosError;
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

/// A labeled declaration, not a certificate of functor laws.
///
/// Maps may be partial: category membership, morphism boundaries, identities,
/// composition and totality are not checked. Morphism pairs without object
/// pairs are allowed. Tags are compared verbatim; validation rejects blank
/// tags but does not trim or normalize them. Notes are unrestricted prose.
///
/// `Default` is an invalid placeholder. Equality compares stored pair order.
/// Deserialization produces an unchecked declaration; call [`Self::validated`]
/// at the admission boundary. Public fields remain mutable after validation.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Functor {
    pub label: String,
    pub source_category: String,
    pub target_category: String,
    /// Diagnostic (source_object, target_object) pairs.
    pub object_map: Vec<(String, String)>,
    /// Diagnostic (source_morphism, target_morphism) pairs.
    pub morphism_map: Vec<(String, String)>,
    pub notes: Vec<String>,
}

impl Functor {
    /// Start an unchecked declaration with categories still unset.
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            source_category: String::new(),
            target_category: String::new(),
            object_map: Vec::new(),
            morphism_map: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        source_category: impl Into<String>,
        target_category: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            source_category: source_category.into(),
            target_category: target_category.into(),
            object_map: Vec::new(),
            morphism_map: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_object_map(mut self, object_map: Vec<(String, String)>) -> Self {
        self.object_map = object_map;
        self
    }

    pub fn with_morphism_map(mut self, morphism_map: Vec<(String, String)>) -> Self {
        self.morphism_map = morphism_map;
        self
    }

    /// Reject blank names/tags and repeated source keys within either pair list.
    ///
    /// Returns the first failure in label, categories, objects, morphisms order.
    /// Repeated target tags are allowed. This does not check functor laws.
    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.trim().is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.source_category.trim().is_empty() {
            return Err(ArithmosError::InvalidShape("empty source_category".into()));
        }
        if self.target_category.trim().is_empty() {
            return Err(ArithmosError::InvalidShape("empty target_category".into()));
        }
        Self::validate_map(&self.object_map, "object_map")?;
        Self::validate_map(&self.morphism_map, "morphism_map")
    }

    fn validate_map(pairs: &[(String, String)], kind: &str) -> Result<(), ArithmosError> {
        let mut seen = HashSet::new();
        for (index, (source, target)) in pairs.iter().enumerate() {
            if source.trim().is_empty() || target.trim().is_empty() {
                return Err(ArithmosError::InvalidShape(format!(
                    "blank {kind} tag at index {index}"
                )));
            }
            if !seen.insert(source.as_str()) {
                return Err(ArithmosError::InvalidShape(format!(
                    "duplicate {kind} source {source:?} at index {index}"
                )));
            }
        }
        Ok(())
    }

    /// Check an owned candidate, including one obtained by deserialization.
    ///
    /// On success the original record is returned unchanged. This establishes
    /// shell validity at this call only; it is not an immutable law certificate.
    pub fn validated(self) -> Result<Self, ArithmosError> {
        self.validate_shell()?;
        Ok(self)
    }

    /// First recorded object image for this exact tag; `None` if absent.
    ///
    /// Unchecked declarations may contain duplicates; validated ones cannot.
    pub fn object_image(&self, source: &str) -> Option<&str> {
        self.object_map
            .iter()
            .find(|(tag, _)| tag == source)
            .map(|(_, image)| image.as_str())
    }

    /// First recorded morphism image for this exact tag; `None` if absent.
    ///
    /// Unchecked declarations may contain duplicates; validated ones cannot.
    pub fn morphism_image(&self, source: &str) -> Option<&str> {
        self.morphism_map
            .iter()
            .find(|(tag, _)| tag == source)
            .map(|(_, image)| image.as_str())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn invalid(candidate: Functor, message: &str) {
        assert_eq!(
            candidate.validate_shell(),
            Err(ArithmosError::InvalidShape(message.into()))
        );
    }

    fn pairs(rows: &[(&str, &str)]) -> Vec<(String, String)> {
        rows.iter()
            .map(|(a, b)| ((*a).into(), (*b).into()))
            .collect()
    }

    #[test]
    fn validate_ok_with_empty_partial_maps() {
        assert!(Functor::between("F", "C", "D").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty_label() {
        invalid(Functor::between("", "C", "D"), "empty label");
    }

    #[test]
    fn validate_rejects_missing_source() {
        invalid(Functor::between("F", "", "D"), "empty source_category");
    }

    #[test]
    fn validate_rejects_missing_target() {
        invalid(Functor::between("F", "C", ""), "empty target_category");
    }

    #[test]
    fn validate_rejects_whitespace_names() {
        for blank in [" ", "\t\n", "\u{2003}"] {
            invalid(Functor::between(blank, "C", "D"), "empty label");
            invalid(Functor::between("F", blank, "D"), "empty source_category");
            invalid(Functor::between("F", "C", blank), "empty target_category");
        }
    }

    #[test]
    fn validate_rejects_blank_object_tags_on_either_side() {
        for blank in ["", " \t", "\u{2003}"] {
            for row in [(blank, "x"), ("a", blank)] {
                invalid(
                    Functor::between("F", "C", "D").with_object_map(pairs(&[("b", "y"), row])),
                    "blank object_map tag at index 1",
                );
            }
        }
    }

    #[test]
    fn validate_rejects_blank_morphism_tags_on_either_side() {
        for blank in ["", " \t", "\u{2003}"] {
            for row in [(blank, "f"), ("u", blank)] {
                invalid(
                    Functor::between("F", "C", "D").with_morphism_map(pairs(&[("v", "g"), row])),
                    "blank morphism_map tag at index 1",
                );
            }
        }
    }

    #[test]
    fn validate_rejects_repeated_object_sources_even_with_the_same_image() {
        for image in ["x", "y"] {
            invalid(
                Functor::between("F", "C", "D").with_object_map(pairs(&[("a", "x"), ("a", image)])),
                "duplicate object_map source \"a\" at index 1",
            );
        }
    }

    #[test]
    fn validate_rejects_repeated_morphism_sources_even_with_the_same_image() {
        for image in ["f", "g"] {
            invalid(
                Functor::between("F", "C", "D")
                    .with_morphism_map(pairs(&[("u", "f"), ("u", image)])),
                "duplicate morphism_map source \"u\" at index 1",
            );
        }
    }

    #[test]
    fn validate_rejects_nonadjacent_object_duplicates() {
        invalid(
            Functor::between("F", "C", "D").with_object_map(pairs(&[
                ("a", "x"),
                ("b", "y"),
                ("a", "z"),
            ])),
            "duplicate object_map source \"a\" at index 2",
        );
    }

    #[test]
    fn validate_rejects_nonadjacent_morphism_duplicates() {
        invalid(
            Functor::between("F", "C", "D").with_morphism_map(pairs(&[
                ("u", "f"),
                ("v", "g"),
                ("u", "h"),
            ])),
            "duplicate morphism_map source \"u\" at index 2",
        );
    }

    #[test]
    fn repeated_targets_and_separate_source_namespaces_are_allowed() {
        let f = Functor::between("F", "C", "D")
            .with_object_map(pairs(&[("a", "x"), ("b", "x")]))
            .with_morphism_map(pairs(&[("a", "f"), ("b", "f")]));
        assert!(f.validate_shell().is_ok());
    }

    #[test]
    fn new_requires_categories_then_accepts_the_populated_record() {
        let mut f = Functor::new("F");
        assert_eq!(
            f.validate_shell(),
            Err(ArithmosError::InvalidShape("empty source_category".into()))
        );
        f.source_category = "C".into();
        f.target_category = "D".into();
        assert!(f.validate_shell().is_ok());
    }

    #[test]
    fn default_is_an_invalid_placeholder() {
        assert!(Functor::default().validated().is_err());
    }

    #[test]
    fn validated_preserves_exact_tags_pair_order_and_notes() {
        let mut f = Functor::between(" F ", " C ", " D ")
            .with_object_map(pairs(&[(" a ", " x "), ("a", "x")]))
            .with_morphism_map(pairs(&[("u", "f")]));
        f.notes = vec!["".into(), "note".into()];
        assert_eq!(f.clone().validated(), Ok(f));
    }

    #[test]
    fn validated_refuses_an_invalid_owned_candidate() {
        let f = Functor::between("F", "C", "D").with_object_map(pairs(&[("a", "x"), ("a", "y")]));
        assert_eq!(
            f.validated(),
            Err(ArithmosError::InvalidShape(
                "duplicate object_map source \"a\" at index 1".into()
            ))
        );
    }

    #[test]
    fn lookups_use_exact_keys_and_report_absence() {
        let f = Functor::between("F", "C", "D")
            .with_object_map(pairs(&[(" a ", " x "), ("a", "x")]))
            .with_morphism_map(pairs(&[("u", "f"), ("v", "g")]));
        assert_eq!(f.object_image(" a "), Some(" x "));
        assert_eq!(f.object_image("a"), Some("x"));
        assert_eq!(f.object_image("missing"), None);
        assert_eq!(f.morphism_image("v"), Some("g"));
        assert_eq!(f.morphism_image(" v "), None);
    }

    #[test]
    fn lookups_on_unchecked_duplicates_return_the_first_recorded_image() {
        let f = Functor::between("F", "C", "D")
            .with_object_map(pairs(&[("a", "x"), ("a", "y")]))
            .with_morphism_map(pairs(&[("u", "f"), ("u", "g")]));
        assert_eq!(f.object_image("a"), Some("x"));
        assert_eq!(f.morphism_image("u"), Some("f"));
        assert!(f.validate_shell().is_err());
    }
}
