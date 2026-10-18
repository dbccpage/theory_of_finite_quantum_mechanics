//! limit shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

use super::cone::Cone;

/// Best-effort shell for a limit of a diagram (diagram_ref + limiting cone).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Limit {
    pub label: String,
    /// Opaque reference to the diagram being limited.
    pub diagram_ref: String,
    pub cone: Cone,
    pub notes: Vec<String>,
}

impl Limit {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            diagram_ref: String::new(),
            cone: Cone::default(),
            notes: Vec::new(),
        }
    }

    pub fn of_diagram(
        label: impl Into<String>,
        diagram_ref: impl Into<String>,
        cone: Cone,
    ) -> Self {
        Self {
            label: label.into(),
            diagram_ref: diagram_ref.into(),
            cone,
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
        self.cone
            .validate_shell()
            .map_err(|e| format!("cone: {e}"))?;
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::limits_colimits::cone::Cone;

    #[test]
    fn validate_ok() {
        let cone = Cone::with_apex("lim_cone", "L");
        let lim = Limit::of_diagram("lim", "D", cone);
        assert!(lim.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty_diagram() {
        let cone = Cone::with_apex("lim_cone", "L");
        let lim = Limit::of_diagram("lim", "", cone);
        assert!(lim.validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_empty_label() {
        assert!(Limit::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_bad_cone() {
        let lim = Limit::of_diagram("lim", "D", Cone::new("c"));
        assert!(lim.validate_shell().is_err());
    }
}
