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
    pub fn normalization(weights: &[i64]) -> Result<Self, AxiomError> {
        let total = normalization_two_ways(weights)?;
        Ok(Self {
            id: "normalization".to_string(),
            description: format!("sum={total}"),
        })
    }
}

fn sum_iter<'a>(iter: impl Iterator<Item = &'a i64>) -> Result<i64, AxiomError> {
    let mut sum = 0i64;
    for weight in iter {
        sum = sum.checked_add(*weight).ok_or(AxiomError::Overflow)?;
    }
    Ok(sum)
}

fn sum_doubled(weights: &[i64]) -> Result<i64, AxiomError> {
    let mut doubled = 0i64;
    for weight in weights {
        let term = weight.checked_mul(2).ok_or(AxiomError::Overflow)?;
        doubled = doubled.checked_add(term).ok_or(AxiomError::Overflow)?;
    }
    Ok(doubled)
}

pub fn normalization_two_ways(weights: &[i64]) -> Result<i64, AxiomError> {
    if weights.is_empty() {
        return Err(AxiomError::Empty);
    }
    let forward = sum_iter(weights.iter())?;
    let backward = sum_iter(weights.iter().rev())?;
    let doubled = sum_doubled(weights)?;
    if forward != backward || doubled / 2 != forward || doubled % 2 != 0 {
        return Err(AxiomError::Normalization);
    }
    Ok(forward)
}
