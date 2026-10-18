//! function shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// A single domain→codomain pair tag (not a formal graph).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct MappingPair {
    pub domain_element: String,
    pub codomain_element: String,
}

/// Best-effort shell for a labeled function between labeled sets.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Function {
    pub label: String,
    pub domain_label: String,
    pub codomain_label: String,
    /// Optional explicit pairs (diagnostic; not a total-function certificate).
    pub pairs: Vec<MappingPair>,
    pub notes: Vec<String>,
}

impl Function {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            domain_label: String::new(),
            codomain_label: String::new(),
            pairs: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        domain_label: impl Into<String>,
        codomain_label: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            domain_label: domain_label.into(),
            codomain_label: codomain_label.into(),
            pairs: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_pair(
        &mut self,
        domain_element: impl Into<String>,
        codomain_element: impl Into<String>,
    ) {
        self.pairs.push(MappingPair {
            domain_element: domain_element.into(),
            codomain_element: codomain_element.into(),
        });
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.domain_label.is_empty() {
            return Err("empty domain_label".into());
        }
        if self.codomain_label.is_empty() {
            return Err("empty codomain_label".into());
        }
        for (i, p) in self.pairs.iter().enumerate() {
            if p.domain_element.is_empty() || p.codomain_element.is_empty() {
                return Err(format!("empty mapping tag at pair index {i}"));
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
        assert!(Function::between("f", "A", "B").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Function::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_domain() {
        let f = Function::new("f");
        assert!(f.validate_shell().is_err());
    }

    #[test]
    fn with_pair_ok() {
        let mut f = Function::between("f", "A", "B");
        f.with_pair("a", "b");
        assert_eq!(f.pairs.len(), 1);
        assert!(f.validate_shell().is_ok());
    }
}
