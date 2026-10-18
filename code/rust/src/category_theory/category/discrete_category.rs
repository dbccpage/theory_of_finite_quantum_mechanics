//! discrete_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Disc(S): objects = S; only identity morphisms.

use serde::{Deserialize, Serialize};

use super::category::MorphismTriple;

/// Best-effort discrete category shell on an object set.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiscreteCategoryShell {
    pub label: String,
    pub objects: Vec<String>,
    /// Morphisms as (src, dst, name) triples — for a discrete category these
    /// should be identities only (src == dst); validated best-effort.
    pub morphisms: Vec<MorphismTriple>,
    pub notes: Vec<String>,
}

impl DiscreteCategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            objects: Vec::new(),
            morphisms: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn on_objects(label: impl Into<String>, objects: Vec<String>) -> Self {
        let morphisms = objects
            .iter()
            .map(|o| MorphismTriple::new(o.clone(), o.clone(), format!("id_{o}")))
            .collect();
        Self {
            label: label.into(),
            objects,
            morphisms,
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        for (i, o) in self.objects.iter().enumerate() {
            if o.is_empty() {
                return Err(format!("empty object tag at index {i}"));
            }
        }
        for (i, m) in self.morphisms.iter().enumerate() {
            if m.source.is_empty() || m.target.is_empty() || m.name.is_empty() {
                return Err(format!("empty morphism field at index {i}"));
            }
            if m.source != m.target {
                return Err(format!(
                    "non-identity morphism at index {i}: {} → {} ({})",
                    m.source, m.target, m.name
                ));
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
        assert!(DiscreteCategoryShell::new("Disc").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(DiscreteCategoryShell::new("").validate_shell().is_err());
    }

    #[test]
    fn on_objects_ok() {
        let d = DiscreteCategoryShell::on_objects("D", vec!["a".into(), "b".into()]);
        assert_eq!(d.morphisms.len(), 2);
        assert!(d.validate_shell().is_ok());
    }

    #[test]
    fn rejects_non_identity() {
        let mut d = DiscreteCategoryShell::on_objects("D", vec!["a".into()]);
        d.morphisms.push(MorphismTriple::new("a", "b", "f"));
        assert!(d.validate_shell().is_err());
    }
}
