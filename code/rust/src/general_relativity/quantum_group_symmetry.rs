//! Quantum group U_q(sl_2) symmetry with exact rational q-deformations.
//!
//! Origin: papers/derivations/general_relativity/rust/src/quantum_group_symmetry.rs
//! Claim: DERIV-GR-QGROUP-001
//! AuthorityEffect: None.

use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum QuantumGroupError {
    InvalidRootOfUnity,
    DegenerateParameter,
}

/// Exact quantum deformation parameters for U_q(sl_2) at rational q or roots of unity.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct QuantumGroupSl2 {
    pub label: String,
    pub q: Ratio<i64>,
}

impl QuantumGroupSl2 {
    pub fn new(q: Ratio<i64>, label: impl Into<String>) -> Result<Self, QuantumGroupError> {
        if q == Ratio::one() || q == -Ratio::one() || q.is_zero() {
            return Err(QuantumGroupError::DegenerateParameter);
        }
        Ok(Self { label: label.into(), q })
    }

    /// Quantum integer [n]_q = (q^n - q^-n) / (q - q^-1).
    pub fn quantum_int(&self, n: i32) -> Ratio<i64> {
        if n == 0 {
            return Ratio::zero();
        }
        if n == 1 {
            return Ratio::one();
        }
        // Power calculation for rational q
        let q = self.q;
        let q_inv = Ratio::one() / q;
        let mut q_n = Ratio::one();
        let mut q_inv_n = Ratio::one();
        for _ in 0..n.abs() {
            q_n *= q;
            q_inv_n *= q_inv;
        }
        if n > 0 {
            (q_n - q_inv_n) / (q - q_inv)
        } else {
            -(q_n - q_inv_n) / (q - q_inv)
        }
    }

    /// Quantum dimension of spin-j representation: dim_q(j) = [2j + 1]_q.
    pub fn quantum_dimension(&self, two_j: usize) -> Ratio<i64> {
        self.quantum_int((two_j + 1) as i32)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quantum_dimension() {
        let qg = QuantumGroupSl2::new(Ratio::new(2, 1), "q2").unwrap();
        // [1]_q = 1
        assert_eq!(qg.quantum_int(1), Ratio::one());
        // [2]_q = (4 - 1/4)/(2 - 1/2) = (15/4)/(3/2) = 5/2
        assert_eq!(qg.quantum_int(2), Ratio::new(5, 2));
        // dim_q(1/2) = [2]_q = 5/2
        assert_eq!(qg.quantum_dimension(1), Ratio::new(5, 2));
    }
}
