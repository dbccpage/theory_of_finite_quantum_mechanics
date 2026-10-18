//! Primitive difference domain types.
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PrimitiveDifference {
    pub label: String,
    pub delta: i64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DifferenceError {
    Overflow,
    Cocycle,
    Antisymmetry,
}

impl PrimitiveDifference {
    /// `D(x, y) = y - x`, stored with the given label.
    pub fn between(label: impl Into<String>, x: i64, y: i64) -> Result<Self, DifferenceError> {
        let delta = y.checked_sub(x).ok_or(DifferenceError::Overflow)?;
        Ok(Self {
            label: label.into(),
            delta,
        })
    }

    /// Evaluate the primitive difference on a pair.
    pub fn evaluate(x: i64, y: i64) -> Result<i64, DifferenceError> {
        y.checked_sub(x).ok_or(DifferenceError::Overflow)
    }

    /// Scale a stored sample difference by an integer.
    pub fn scale(&self, factor: i64) -> Result<i64, DifferenceError> {
        self.delta.checked_mul(factor).ok_or(DifferenceError::Overflow)
    }
}

/// Antisymmetry `D(x,y) + D(y,x) = 0` and the cocycle `D(x,y)+D(y,z) = D(x,z)`.
pub fn sample_cocycle() -> Result<(), DifferenceError> {
    let points = [0i64, 1, 3, 7, 12];
    for &x in &points {
        for &y in &points {
            let forward = PrimitiveDifference::evaluate(x, y)?;
            let backward = PrimitiveDifference::evaluate(y, x)?;
            if forward.checked_add(backward).ok_or(DifferenceError::Overflow)? != 0 {
                return Err(DifferenceError::Antisymmetry);
            }
            let stored = PrimitiveDifference::between("sample", x, y)?;
            if stored.delta != forward {
                return Err(DifferenceError::Cocycle);
            }
            for &z in &points {
                let along = forward
                    .checked_add(PrimitiveDifference::evaluate(y, z)?)
                    .ok_or(DifferenceError::Overflow)?;
                let direct = PrimitiveDifference::evaluate(x, z)?;
                if along != direct {
                    return Err(DifferenceError::Cocycle);
                }
            }
        }
    }
    Ok(())
}
