//! adjoint functor theorem shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Records hypothesis/conclusion labels for an AFT-style claim
//! (e.g. solution-set condition ⇒ right adjoint exists). Shape only.

use serde::{Deserialize, Serialize};

/// Best-effort shell for an adjoint-functor-theorem claim record.
///
/// Does not prove existence of adjoints. Diagnostic inventory of
/// stated hypotheses and the claimed adjoint label.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct AdjointFunctorTheoremShell {
    pub label: String,
    /// Functor claimed to admit an adjoint.
    pub functor_ref: String,
    /// Direction: "left" or "right" adjoint sought (free string tag).
    pub adjoint_side: String,
    /// Ambient category / completeness hypotheses (tags).
    pub hypotheses: Vec<String>,
    /// Optional solution-set / solution-object condition tag.
    pub solution_set_condition: String,
    /// Claimed adjoint functor label (if named).
    pub claimed_adjoint: String,
    pub notes: Vec<String>,
}

impl AdjointFunctorTheoremShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            functor_ref: String::new(),
            adjoint_side: String::new(),
            hypotheses: Vec::new(),
            solution_set_condition: String::new(),
            claimed_adjoint: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn for_functor(
        label: impl Into<String>,
        functor_ref: impl Into<String>,
        adjoint_side: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            functor_ref: functor_ref.into(),
            adjoint_side: adjoint_side.into(),
            hypotheses: Vec::new(),
            solution_set_condition: String::new(),
            claimed_adjoint: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_hypothesis(mut self, hypothesis: impl Into<String>) -> Self {
        self.hypotheses.push(hypothesis.into());
        self
    }

    pub fn with_solution_set(mut self, condition: impl Into<String>) -> Self {
        self.solution_set_condition = condition.into();
        self
    }

    pub fn with_claimed_adjoint(mut self, claimed: impl Into<String>) -> Self {
        self.claimed_adjoint = claimed.into();
        self
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.functor_ref.is_empty() {
            return Err("empty functor_ref".into());
        }
        if self.adjoint_side.is_empty() {
            return Err("empty adjoint_side".into());
        }
        for (i, h) in self.hypotheses.iter().enumerate() {
            if h.is_empty() {
                return Err(format!("empty hypothesis tag at index {i}"));
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
        let a = AdjointFunctorTheoremShell::for_functor("aft", "U", "left");
        assert!(a.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(AdjointFunctorTheoremShell::new("")
            .validate_shell()
            .is_err());
    }

    #[test]
    fn with_hypotheses_ok() {
        let a = AdjointFunctorTheoremShell::for_functor("aft", "U", "left")
            .with_hypothesis("complete_codomain")
            .with_solution_set("solution_set_condition")
            .with_claimed_adjoint("F");
        assert_eq!(a.hypotheses.len(), 1);
        assert!(a.validate_shell().is_ok());
    }

    #[test]
    fn rejects_empty_hypothesis() {
        let a = AdjointFunctorTheoremShell::for_functor("aft", "U", "left").with_hypothesis("");
        assert!(a.validate_shell().is_err());
    }
}
