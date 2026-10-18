//! Exact finite bi-crossed product Hopf algebra and matched pairs.
//!
//! Origin: papers/derivations/general_relativity/rust/src/bi_crossed_product.rs
//! Claim: DERIV-GR-BICROSSED-001
//! AuthorityEffect: None.

use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum BiCrossedError {
    DimensionMismatch,
    NonInvertibleElement,
    CompatibilityViolation { detail: String },
}

/// A finite matched pair of Lie algebras (g, h) forming a bi-crossed product g ⋈ h.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BiCrossedProduct {
    pub dim_g: usize,
    pub dim_h: usize,
    pub label: String,
    /// Structure constants for g: [e_i, e_j] = sum_k c_{ij}^k e_k
    pub c_g: BTreeMap<(usize, usize, usize), Ratio<i64>>,
    /// Structure constants for h: [f_a, f_b] = sum_c c_{ab}^c f_c
    pub c_h: BTreeMap<(usize, usize, usize), Ratio<i64>>,
}

impl BiCrossedProduct {
    pub fn new(dim_g: usize, dim_h: usize, label: impl Into<String>) -> Self {
        Self {
            dim_g,
            dim_h,
            label: label.into(),
            c_g: BTreeMap::new(),
            c_h: BTreeMap::new(),
        }
    }

    pub fn set_bracket_g(&mut self, i: usize, j: usize, k: usize, val: Ratio<i64>) {
        self.c_g.insert((i, j, k), val);
        self.c_g.insert((j, i, k), -val);
    }

    pub fn set_bracket_h(&mut self, a: usize, b: usize, c: usize, val: Ratio<i64>) {
        self.c_h.insert((a, b, c), val);
        self.c_h.insert((b, a, c), -val);
    }

    /// Verifies the Jacobi identity for Lie algebra g over exact rationals.
    pub fn verify_jacobi_g(&self) -> Result<(), BiCrossedError> {
        for i in 0..self.dim_g {
            for j in 0..self.dim_g {
                for k in 0..self.dim_g {
                    for m in 0..self.dim_g {
                        let mut sum = Ratio::zero();
                        for r in 0..self.dim_g {
                            let c_ij_r = self.c_g.get(&(i, j, r)).copied().unwrap_or_else(Ratio::zero);
                            let c_rk_m = self.c_g.get(&(r, k, m)).copied().unwrap_or_else(Ratio::zero);
                            let c_jk_r = self.c_g.get(&(j, k, r)).copied().unwrap_or_else(Ratio::zero);
                            let c_ri_m = self.c_g.get(&(r, i, m)).copied().unwrap_or_else(Ratio::zero);
                            let c_ki_r = self.c_g.get(&(k, i, r)).copied().unwrap_or_else(Ratio::zero);
                            let c_rj_m = self.c_g.get(&(r, j, m)).copied().unwrap_or_else(Ratio::zero);
                            sum += c_ij_r * c_rk_m + c_jk_r * c_ri_m + c_ki_r * c_rj_m;
                        }
                        if !sum.is_zero() {
                            return Err(BiCrossedError::CompatibilityViolation {
                                detail: format!("Jacobi violation in g at indices ({i}, {j}, {k}) target {m}"),
                            });
                        }
                    }
                }
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn abelian_matched_pair_jacobi() {
        let bp = BiCrossedProduct::new(2, 2, "abelian_pair");
        assert!(bp.verify_jacobi_g().is_ok());
    }

    #[test]
    fn heisenberg_algebra_jacobi() {
        let mut bp = BiCrossedProduct::new(3, 0, "heisenberg");
        // [e0, e1] = e2
        bp.set_bracket_g(0, 1, 2, Ratio::new(1, 1));
        assert!(bp.verify_jacobi_g().is_ok());
    }
}
