//! galois connection shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Order-theoretic adjunction: monotone maps f ⊣ g between posets
//! with f(x) ≤ y ⇔ x ≤ g(y). Diagnostic pair tags only.

use omega_category_theory::errors::ArithmosError;
use serde::{Deserialize, Serialize};

/// A single ordered pair tag (x, y) used as a monotone-map edge.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct MonotonePair {
    pub domain_element: String,
    pub codomain_element: String,
}

impl MonotonePair {
    pub fn new(domain_element: impl Into<String>, codomain_element: impl Into<String>) -> Self {
        Self {
            domain_element: domain_element.into(),
            codomain_element: codomain_element.into(),
        }
    }
}

/// Best-effort shell for a Galois connection between posets.
///
/// `lower` / `upper` are monotone maps stored as Vec of pairs (diagnostic
/// graph edges, not a totality or monotonicity certificate).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct GaloisConnectionShell {
    pub label: String,
    /// Source poset label.
    pub poset_left: String,
    /// Target poset label.
    pub poset_right: String,
    /// Lower adjoint f : left → right (monotone map as pairs).
    pub lower: Vec<MonotonePair>,
    /// Upper adjoint g : right → left (monotone map as pairs).
    pub upper: Vec<MonotonePair>,
    pub notes: Vec<String>,
}

impl GaloisConnectionShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            poset_left: String::new(),
            poset_right: String::new(),
            lower: Vec::new(),
            upper: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        poset_left: impl Into<String>,
        poset_right: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            poset_left: poset_left.into(),
            poset_right: poset_right.into(),
            lower: Vec::new(),
            upper: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_lower_pair(
        mut self,
        domain_element: impl Into<String>,
        codomain_element: impl Into<String>,
    ) -> Self {
        self.lower
            .push(MonotonePair::new(domain_element, codomain_element));
        self
    }

    pub fn with_upper_pair(
        mut self,
        domain_element: impl Into<String>,
        codomain_element: impl Into<String>,
    ) -> Self {
        self.upper
            .push(MonotonePair::new(domain_element, codomain_element));
        self
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.poset_left.is_empty() {
            return Err(ArithmosError::InvalidShape("empty poset_left".into()));
        }
        if self.poset_right.is_empty() {
            return Err(ArithmosError::InvalidShape("empty poset_right".into()));
        }
        for (i, p) in self.lower.iter().enumerate() {
            if p.domain_element.is_empty() || p.codomain_element.is_empty() {
                return Err(ArithmosError::InvalidShape(format!("empty lower pair tag at index {i}")));
            }
        }
        for (i, p) in self.upper.iter().enumerate() {
            if p.domain_element.is_empty() || p.codomain_element.is_empty() {
                return Err(ArithmosError::InvalidShape(format!("empty upper pair tag at index {i}")));
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
        let g = GaloisConnectionShell::between("gal", "P", "Q");
        assert!(g.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(GaloisConnectionShell::new("").validate_shell().is_err());
    }

    #[test]
    fn with_maps_ok() {
        let g = GaloisConnectionShell::between("gal", "P", "Q")
            .with_lower_pair("x", "f(x)")
            .with_upper_pair("y", "g(y)");
        assert_eq!(g.lower.len(), 1);
        assert_eq!(g.upper.len(), 1);
        assert!(g.validate_shell().is_ok());
    }

    #[test]
    fn rejects_empty_pair() {
        let g = GaloisConnectionShell::between("gal", "P", "Q").with_lower_pair("", "y");
        assert!(g.validate_shell().is_err());
    }
}
