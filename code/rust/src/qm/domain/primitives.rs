//! Foundational finite QM primitives.
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PrimitiveAxiom {
    pub id: String,
    pub description: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AxiomError {
    Empty,
    Overflow,
    Normalization,
}

impl PrimitiveAxiom {
    /// Normalization axiom: the integer weights sum to one common total,
    /// computed from both ends.
    pub fn normalization(weights: &[i64]) -> Result<Self, AxiomError> {
        let total = normalization_two_ways(weights)?;
        Ok(Self {
            id: "normalization".to_string(),
            description: format!("sum={total}"),
        })
    }
}

/// Left-to-right sum, right-to-left sum, and `sum(2 w_i) / 2` agree.
pub fn normalization_two_ways(weights: &[i64]) -> Result<i64, AxiomError> {
    if weights.is_empty() {
        return Err(AxiomError::Empty);
    }
    let mut forward = 0i64;
    for weight in weights {
        forward = forward.checked_add(*weight).ok_or(AxiomError::Overflow)?;
    }
    let mut backward = 0i64;
    for weight in weights.iter().rev() {
        backward = backward.checked_add(*weight).ok_or(AxiomError::Overflow)?;
    }
    let mut doubled = 0i64;
    for weight in weights {
        doubled = doubled
            .checked_add(weight.checked_mul(2).ok_or(AxiomError::Overflow)?)
            .ok_or(AxiomError::Overflow)?;
    }
    if forward != backward || doubled / 2 != forward || doubled % 2 != 0 {
        return Err(AxiomError::Normalization);
    }
    Ok(forward)
}
