//! BQNF terminal routing: 5-fold classification matching `BqnfSignPacket.lean`.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};

/// Five canonical terminal routing outcomes under BQNF normal form,
/// matching `BqnfSignPacket.TerminalRoute` in `BqnfSignPacket.lean`.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum TerminalRoute {
    /// \Phi_1 = 0 or exact involution doublet repair
    ExactRepair,
    /// \Phi_1 > 0, \Gamma_2 = 0, no involution, overlapping weights
    ClosedResidual,
    /// \Gamma_2 > 0 (cochain non-closure)
    OpenSignObstruction,
    /// Disjoint weight spectra / thermal asymmetry
    SplitBrainRefusal,
    /// Broken complex or nilpotence failure (d_1 \circ d_0 != 0)
    ClosureFailure,
}

/// Metric measurements of a finite sign obstruction packet,
/// directly matching `SignPacketMetrics` in `BqnfSignPacket.lean`.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SignPacketMetrics {
    pub is_valid_complex: bool,
    pub disjoint_supports: bool,
    pub closure_defect: BigRational, // \Gamma_2 = ||d_1 c^1||
    pub residual_mass: BigRational,  // \Phi_1 = ||[c^1]||_{Q^1}
    pub has_involution_witness: bool,
}

impl SignPacketMetrics {
    pub fn new(
        is_valid_complex: bool,
        disjoint_supports: bool,
        closure_defect: BigRational,
        residual_mass: BigRational,
        has_involution_witness: bool,
    ) -> Self {
        Self {
            is_valid_complex,
            disjoint_supports,
            closure_defect,
            residual_mass,
            has_involution_witness,
        }
    }
}

/// Deterministic 5-fold routing function for BQNF sign packets,
/// mirror of `BqnfSignPacket.routePacket` in Lean 4.
pub fn route_packet(m: &SignPacketMetrics) -> TerminalRoute {
    if !m.is_valid_complex {
        TerminalRoute::ClosureFailure
    } else if m.disjoint_supports {
        TerminalRoute::SplitBrainRefusal
    } else if m.closure_defect > BigRational::zero() {
        TerminalRoute::OpenSignObstruction
    } else if m.residual_mass.is_zero() || m.has_involution_witness {
        TerminalRoute::ExactRepair
    } else {
        TerminalRoute::ClosedResidual
    }
}

/// Rational cochain complex C^0 -> C^1 -> C^2 with coboundaries d0, d1.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CochainComplex {
    pub dim_c0: usize,
    pub dim_c1: usize,
    pub dim_c2: usize,
    pub d0: Vec<Vec<BigRational>>, // dim_c1 x dim_c0
    pub d1: Vec<Vec<BigRational>>, // dim_c2 x dim_c1
}

impl CochainComplex {
    pub fn new(
        dim_c0: usize,
        dim_c1: usize,
        dim_c2: usize,
        d0: Vec<Vec<BigRational>>,
        d1: Vec<Vec<BigRational>>,
    ) -> Result<Self, &'static str> {
        if d0.len() != dim_c1 {
            return Err("d0 row count mismatch (expected dim_c1)");
        }
        for row in &d0 {
            if row.len() != dim_c0 {
                return Err("d0 column count mismatch (expected dim_c0)");
            }
        }
        if d1.len() != dim_c2 {
            return Err("d1 row count mismatch (expected dim_c2)");
        }
        for row in &d1 {
            if row.len() != dim_c1 {
                return Err("d1 column count mismatch (expected dim_c1)");
            }
        }
        let complex = Self {
            dim_c0,
            dim_c1,
            dim_c2,
            d0,
            d1,
        };
        if !complex.check_nilpotence() {
            return Err("nilpotence failure: d1 . d0 != 0");
        }
        Ok(complex)
    }

    /// Exact check that d1 . d0 = 0.
    pub fn check_nilpotence(&self) -> bool {
        for row in &self.d1 {
            for j in 0..self.dim_c0 {
                let mut sum = BigRational::zero();
                for k in 0..self.dim_c1 {
                    sum = sum + &row[k] * &self.d0[k][j];
                }
                if !sum.is_zero() {
                    return false;
                }
            }
        }
        true
    }

    /// Calculate coboundary d1 . c1.
    pub fn apply_d1(&self, c1: &[BigRational]) -> Result<Vec<BigRational>, &'static str> {
        if c1.len() != self.dim_c1 {
            return Err("c1 length must equal dim_c1");
        }
        let mut d1_c1 = vec![BigRational::zero(); self.dim_c2];
        for (i, row) in self.d1.iter().enumerate() {
            let mut sum = BigRational::zero();
            for (k, val) in row.iter().enumerate() {
                sum = sum + val * &c1[k];
            }
            d1_c1[i] = sum;
        }
        Ok(d1_c1)
    }

    /// L1 norm of a vector over Q: \sum |x_i|.
    pub fn l1_norm(vec: &[BigRational]) -> BigRational {
        let mut sum = BigRational::zero();
        for x in vec {
            sum = sum + x.abs();
        }
        sum
    }

    /// Compute closure defect \Gamma_2 = ||d_1 c^1||_1.
    pub fn compute_closure_defect(&self, c1: &[BigRational]) -> Result<BigRational, &'static str> {
        let d1_c1 = self.apply_d1(c1)?;
        Ok(Self::l1_norm(&d1_c1))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_traits::One;

    #[test]
    fn bqnf_5_fold_routing_theorems() {
        // 1. Invalid complex routes to ClosureFailure
        let m1 = SignPacketMetrics::new(
            false,
            false,
            BigRational::zero(),
            BigRational::zero(),
            false,
        );
        assert_eq!(route_packet(&m1), TerminalRoute::ClosureFailure);

        // 2. Disjoint supports route to SplitBrainRefusal
        let m2 = SignPacketMetrics::new(
            true,
            true,
            BigRational::zero(),
            BigRational::zero(),
            false,
        );
        assert_eq!(route_packet(&m2), TerminalRoute::SplitBrainRefusal);

        // 3. Open defect routes to OpenSignObstruction
        let m3 = SignPacketMetrics::new(
            true,
            false,
            BigRational::one(),
            BigRational::zero(),
            false,
        );
        assert_eq!(route_packet(&m3), TerminalRoute::OpenSignObstruction);

        // 4. Exact zero mass routes to ExactRepair
        let m4 = SignPacketMetrics::new(
            true,
            false,
            BigRational::zero(),
            BigRational::zero(),
            false,
        );
        assert_eq!(route_packet(&m4), TerminalRoute::ExactRepair);

        // 5. Non-zero mass with involution witness routes to ExactRepair
        let m5 = SignPacketMetrics::new(
            true,
            false,
            BigRational::zero(),
            BigRational::one(),
            true,
        );
        assert_eq!(route_packet(&m5), TerminalRoute::ExactRepair);

        // 6. Non-zero mass without involution witness routes to ClosedResidual
        let m6 = SignPacketMetrics::new(
            true,
            false,
            BigRational::zero(),
            BigRational::one(),
            false,
        );
        assert_eq!(route_packet(&m6), TerminalRoute::ClosedResidual);
    }

    #[test]
    fn cochain_nilpotence_check() {
        // C0 -> C1 -> C2
        // d0: 2x1, d1: 1x2, d1 . d0 = [1, -1] * [[1], [1]] = 0
        let d0 = vec![vec![BigRational::one()], vec![BigRational::one()]];
        let d1 = vec![vec![BigRational::one(), -BigRational::one()]];
        let complex = CochainComplex::new(1, 2, 1, d0, d1).unwrap();
        assert!(complex.check_nilpotence());

        let c1_closed = vec![BigRational::one(), BigRational::one()];
        assert_eq!(complex.compute_closure_defect(&c1_closed).unwrap(), BigRational::zero());

        let c1_open = vec![BigRational::one(), BigRational::zero()];
        assert_eq!(complex.compute_closure_defect(&c1_open).unwrap(), BigRational::one());
    }
}
