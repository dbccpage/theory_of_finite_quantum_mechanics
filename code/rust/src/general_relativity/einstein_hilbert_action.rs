
use crate::regge_calculus::{ReggeCalculus, ReggeError};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; f64 face; not the exact proxy (the sum of area_squared times kappa).";

#[derive(Debug, Clone, PartialEq)]
pub struct EinsteinHilbertAction {
    pub value: f64,
    pub label: String,
}

impl EinsteinHilbertAction {
    pub fn new(degree: usize, label: impl Into<String>) -> Self {
        Self {
            value: degree as f64,
            label: label.into(),
        }
    }

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
