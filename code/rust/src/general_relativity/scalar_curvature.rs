
use crate::regge_calculus::{ReggeCalculus, ReggeError};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; discrete deficit curvature.";

#[derive(Debug, Clone, PartialEq)]
pub struct ScalarCurvature {
    pub vertex_deficits: Vec<f64>,
    pub label: String,
}

impl ScalarCurvature {
    pub fn new(degree: usize, label: impl Into<String>) -> Self {
        Self {
            vertex_deficits: vec![0.0; degree],
            label: label.into(),
        }
    }

    pub fn try_from_regge(
        regge: &ReggeCalculus,
        label: impl Into<String>,
    ) -> Result<Self, ReggeError> {
        Ok(Self {
            vertex_deficits: regge.vertex_deficits()?,
            label: label.into(),
        })
    }

    pub fn total(&self) -> f64 {
        self.vertex_deficits.iter().sum()
    }

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
        assert!(s.vertex_deficits[0].abs() < 1e-8);
    }

    #[test]
    fn new_and_fence() {
        let x = ScalarCurvature::new(2, "test");
        assert_eq!(x.degree(), 2);
        assert!(ScalarCurvature::authority_fence().contains("AuthorityEffect None"));
    }
}
