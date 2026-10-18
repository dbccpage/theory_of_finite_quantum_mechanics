//! Native Rust implementation modules for the MUB(6) formal verification campaign.
//!
//! Origin: papers/derivations/mub/rust/src/omega_native/mod.rs
//! Claim: MUB6-NATIVE-SUB-001
//! AuthorityEffect: None.

pub mod campaign;
pub mod census;
pub mod exact;
pub mod float_check;
pub mod mub6_continuous_chaining;
pub mod mub6_firewall;

use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum NativeSubsystemError {
    DimensionMismatch,
    NonCompositeDimension,
    InvariantViolation(String),
}

/// Evaluator for omega_native subsystem invariants in dimension d=6.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct OmegaNativeSubsystem {
    pub dimension: usize,
    pub label: String,
}

impl OmegaNativeSubsystem {
    pub fn d6() -> Self {
        Self {
            dimension: 6,
            label: "d6_native_engine".to_string(),
        }
    }

    /// Verifies that dimension 6 is non-prime-power: 6 = 2 * 3.
    pub fn verify_algebraic_profile(&self) -> Result<(), NativeSubsystemError> {
        let d = self.dimension;
        if d != 6 {
            return Err(NativeSubsystemError::DimensionMismatch);
        }
        // 6 is divisible by both 2 and 3, hence composite and not a prime power
        if d % 2 != 0 || d % 3 != 0 {
            return Err(NativeSubsystemError::NonCompositeDimension);
        }
        Ok(())
    }

    /// Exact rational target overlap 1/d = 1/6.
    pub fn target_overlap(&self) -> Ratio<i64> {
        Ratio::new(1, self.dimension as i64)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_omega_native_d6() {
        let sub = OmegaNativeSubsystem::d6();
        assert!(sub.verify_algebraic_profile().is_ok());
        assert_eq!(sub.target_overlap(), Ratio::new(1, 6));
    }
}
