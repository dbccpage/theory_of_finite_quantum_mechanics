//! Discrete scalar curvature from Regge deficits (2D).
//!
//! At each vertex, ε_v / (local area measure). For the finite 2D face we report
//! raw deficits as curvature carriers (area measure optional later).
//!
//! AuthorityEffect: None. Not continuum Ricci scalar.

use crate::regge_calculus::{ReggeCalculus, ReggeError};

/// Fence string (proposal).
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; discrete deficit curvature.";

/// Discrete scalar curvature as vertex deficits.
#[derive(Debug, Clone, PartialEq)]
pub struct ScalarCurvature {
    /// Per-vertex deficits ε_v = 2π − Σ angles.
    pub vertex_deficits: Vec<f64>,
    /// Label.
    pub label: String,
}

impl ScalarCurvature {
    /// Scaffold: empty curvature list; degree = length proxy.
    pub fn new(degree: usize, label: impl Into<String>) -> Self {
        Self {
            vertex_deficits: vec![0.0; degree],
            label: label.into(),
        }
    }

    /// From a 2D Regge geometry.
    pub fn try_from_regge(
        regge: &ReggeCalculus,
        label: impl Into<String>,
    ) -> Result<Self, ReggeError> {
        Ok(Self {
            vertex_deficits: regge.vertex_deficits()?,
            label: label.into(),
        })
    }

    /// Total integrated curvature Σ ε_v (= 2D Regge action).
    pub fn total(&self) -> f64 {
        self.vertex_deficits.iter().sum()
    }

    /// Max |ε_v|.
    pub fn max_abs(&self) -> f64 {
        self.vertex_deficits
            .iter()
            .map(|x| x.abs())
            .fold(0.0_f64, f64::max)
    }

    pub fn degree(&self) -> usize {
        self.vertex_deficits.len()
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
    fn flat_fan_total_boundary_only() {
        let g = ReggeCalculus::equilateral_fan(6, 1.0).unwrap();
        let s = ScalarCurvature::try_from_regge(&g, "R").unwrap();
        // Center deficit ~ 0; boundary vertices carry residual deficit mass
        assert!(s.vertex_deficits[0].abs() < 1e-8);
    }

    #[test]
    fn new_and_fence() {
        let x = ScalarCurvature::new(2, "test");
        assert_eq!(x.degree(), 2);
        assert!(ScalarCurvature::authority_fence().contains("AuthorityEffect None"));
    }
}
