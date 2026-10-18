//! colimit shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

use super::cone::Cocone;

/// Best-effort shell for a colimit of a diagram (diagram_ref + colimiting cocone).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Colimit {
    pub label: String,
    /// Opaque reference to the diagram being colimited.
    pub diagram_ref: String,
    pub cocone: Cocone,
    pub notes: Vec<String>,
}

impl Colimit {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            diagram_ref: String::new(),
            cocone: Cocone::default(),
            notes: Vec::new(),
        }
    }

    pub fn of_diagram(
        label: impl Into<String>,
        diagram_ref: impl Into<String>,
        cocone: Cocone,
    ) -> Self {
        Self {
            label: label.into(),
            diagram_ref: diagram_ref.into(),
            cocone,
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.diagram_ref.is_empty() {
            return Err("empty diagram_ref".into());
        }
        self.cocone
            .validate_shell()
            .map_err(|e| format!("cocone: {e}"))?;
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::limits_colimits::cone::Cocone;

    #[test]
    fn validate_ok() {
        let cocone = Cocone::with_nadir("colim_cocone", "Q");
        let colim = Colimit::of_diagram("colim", "D", cocone);
        assert!(colim.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty_diagram() {
        let cocone = Cocone::with_nadir("colim_cocone", "Q");
        let colim = Colimit::of_diagram("colim", "", cocone);
        assert!(colim.validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_empty_label() {
        assert!(Colimit::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_bad_cocone() {
        let colim = Colimit::of_diagram("colim", "D", Cocone::new("cc"));
        assert!(colim.validate_shell().is_err());
    }
}
