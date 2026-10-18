//! density_comonad shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort shell for the density comonad Lan_K K (or denseness data for K).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct DensityComonad {
    pub label: String,
    /// Functor K whose density comonad is formed (typically Lan_K K).
    pub functor_k: String,
    /// Domain category of K.
    pub domain_category_ref: String,
    /// Codomain category of K.
    pub codomain_category_ref: String,
    /// Comonad / extension functor reference when claimed.
    pub comonad_ref: String,
    /// Optional left Kan extension shell label (diagnostic linkage).
    pub lan_ref: String,
    pub notes: Vec<String>,
}

impl DensityComonad {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            functor_k: String::new(),
            domain_category_ref: String::new(),
            codomain_category_ref: String::new(),
            comonad_ref: String::new(),
            lan_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn of_functor(
        label: impl Into<String>,
        functor_k: impl Into<String>,
        domain_category_ref: impl Into<String>,
        codomain_category_ref: impl Into<String>,
        comonad_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            functor_k: functor_k.into(),
            domain_category_ref: domain_category_ref.into(),
            codomain_category_ref: codomain_category_ref.into(),
            comonad_ref: comonad_ref.into(),
            lan_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.functor_k.is_empty() {
            return Err("empty functor_k".into());
        }
        if self.domain_category_ref.is_empty() {
            return Err("empty domain_category_ref".into());
        }
        if self.codomain_category_ref.is_empty() {
            return Err("empty codomain_category_ref".into());
        }
        if self.comonad_ref.is_empty() {
            return Err("empty comonad_ref".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let d = DensityComonad::of_functor("dens", "K", "C", "D", "Lan_K K");
        assert!(d.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(DensityComonad::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_functor() {
        assert!(DensityComonad::new("d").validate_shell().is_err());
    }
}
