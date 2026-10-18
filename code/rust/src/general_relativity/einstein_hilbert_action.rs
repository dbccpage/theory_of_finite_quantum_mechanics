//! f64 face of a discrete Einstein–Hilbert action. Not the exact proxy
//! (the sum of area_squared times kappa).
//!
//! Continuum EH ∫ R √|g| is not this file. The f64 stand-in follows
//! `S = Σ_v ε_v` ([`crate::regge_calculus::ReggeCalculus::regge_action_2d`]),
//! where 2D hinges are vertices and V_h = 1.
//!
//! AuthorityEffect: None. Not continuum EH. Not PROVED.

use crate::regge_calculus::{ReggeCalculus, ReggeError};

/// f64 face. Not the exact proxy (the sum of area_squared times kappa).
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; f64 face; not the exact proxy (the sum of area_squared times kappa).";

/// Discrete Einstein–Hilbert / Regge action value.
#[derive(Debug, Clone, PartialEq)]
pub struct EinsteinHilbertAction {
    /// Action scalar S.
    pub value: f64,
    /// Label.
    pub label: String,
}

impl EinsteinHilbertAction {
    /// Scaffold: value = degree as f64 (legacy proxy).
    pub fn new(degree: usize, label: impl Into<String>) -> Self {
        Self {
            value: degree as f64,
            label: label.into(),
        }
    }

    /// From 2D Regge geometry.
    pub fn try_from_regge(
        regge: &ReggeCalculus,
        label: impl Into<String>,
    ) -> Result<Self, ReggeError> {
        Ok(Self {
            value: regge.regge_action_2d()?,
            label: label.into(),
        })
    }

    pub fn degree(&self) -> usize {
        self.value.abs() as usize
    }

    pub fn authority_fence() -> &'static str {
        AUTHORITY_FENCE
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::regge_calculus::ReggeCalculus;

    #[test]
    fn action_matches_sum_of_deficits() {
        let g = ReggeCalculus::equilateral_fan(3, 1.0).unwrap();
        let s = EinsteinHilbertAction::try_from_regge(&g, "S").unwrap();
        let sum: f64 = g.vertex_deficits().unwrap().into_iter().sum();
        assert!((s.value - sum).abs() < 1e-10);
    }

    #[test]
    fn new_and_fence() {
        let x = EinsteinHilbertAction::new(1, "test");
        assert!(EinsteinHilbertAction::authority_fence().contains("AuthorityEffect None"));
        assert_eq!(x.value, 1.0);
    }
}
