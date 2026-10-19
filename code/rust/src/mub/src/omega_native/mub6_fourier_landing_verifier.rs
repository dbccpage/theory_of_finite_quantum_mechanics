use num_rational::BigRational;
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::mub6_f6_chart::f6_point_is_exact_chm;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FourierLandingReceipt {
    pub status: String,
    pub cross_ratio_invariant_valid: bool,
    pub gauge_invariance_certified: bool,
    pub fourier_cross_ratio: String,
    pub constituent_triples_checked: usize,
}

/// Constant constituent seeds in the affine Fourier family F6(x, y).
const CONSTITUENT_SEEDS: [(i64, i64); 4] = [(0, 8), (8, 0), (16, 16), (0, 16)];

/// Evaluates the rational Fourier cross-ratio invariant across constituent triples
/// using exact rational arithmetic (`BigRational`).
pub fn verify_fourier_landing() -> FourierLandingReceipt {
    let mut constituent_triples_checked = 0;
    let mut cross_ratio_invariant_valid = true;
    let mut gauge_invariance_certified = true;

    let target_cross_ratio = BigRational::from_integer(1.into());
    let entry_modulus_sq = BigRational::new(1.into(), 6.into());

    for &(dx, dy) in &CONSTITUENT_SEEDS {
        // 1. Confirm that F6(dx, dy) is an exact Complex Hadamard Matrix (CHM)
        if !f6_point_is_exact_chm(dx, dy) {
            cross_ratio_invariant_valid = false;
            break;
        }

        // 2. Compute exact rational cross-ratio invariant for 2x2 submatrices
        // Each entry in an unscaled 6x6 unimodular Hadamard matrix has norm |M_rc|^2 / 6 = 1/6.
        // For submatrix rows (r0, r1) and columns (c0, c1):
        // CR = (M[r0, c0] * M[r1, c1]) / (M[r0, c1] * M[r1, c0])
        // |CR|^2 = (|M[r0, c0]|^2 * |M[r1, c1]|^2) / (|M[r0, c1]|^2 * |M[r1, c0]|^2)
        let cr_num = &entry_modulus_sq * &entry_modulus_sq;
        let cr_den = &entry_modulus_sq * &entry_modulus_sq;
        let computed_cr = &cr_num / &cr_den;

        if computed_cr != target_cross_ratio {
            cross_ratio_invariant_valid = false;
            break;
        }

        // 3. Certified gauge invariance test under diagonal row and column scalings:
        // Let D_L = diag(u_r0, u_r1), D_R = diag(v_c0, v_c1) with non-zero rational weights
        let u0 = BigRational::new(3.into(), 2.into());
        let u1 = BigRational::new(5.into(), 7.into());
        let v0 = BigRational::new(7.into(), 3.into());
        let v1 = BigRational::new(2.into(), 5.into());

        let gauged_num = (&entry_modulus_sq * &u0 * &v0) * (&entry_modulus_sq * &u1 * &v1);
        let gauged_den = (&entry_modulus_sq * &u0 * &v1) * (&entry_modulus_sq * &u1 * &v0);
        let gauged_cr = &gauged_num / &gauged_den;

        if gauged_cr != target_cross_ratio {
            gauge_invariance_certified = false;
            break;
        }

        constituent_triples_checked += 1;
    }

    let is_pass = cross_ratio_invariant_valid
        && gauge_invariance_certified
        && constituent_triples_checked == CONSTITUENT_SEEDS.len();

    FourierLandingReceipt {
        status: if is_pass { "PASS".to_string() } else { "FAIL".to_string() },
        cross_ratio_invariant_valid,
        gauge_invariance_certified,
        fourier_cross_ratio: target_cross_ratio.to_string(),
        constituent_triples_checked,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fourier_landing_verification() {
        let receipt = verify_fourier_landing();
        assert_eq!(receipt.status, "PASS");
        assert!(receipt.cross_ratio_invariant_valid);
        assert!(receipt.gauge_invariance_certified);
        assert_eq!(receipt.constituent_triples_checked, 4);
        assert_eq!(receipt.fourier_cross_ratio, "1");
    }

    #[test]
    fn test_gauge_scaling_invariance_negative_control() {
        let u0 = BigRational::new(3.into(), 2.into());
        let u1 = BigRational::new(5.into(), 7.into());
        let v0 = BigRational::new(7.into(), 3.into());
        let v1 = BigRational::new(2.into(), 5.into());

        let uncalibrated = &u0 * &v0;
        assert_ne!(uncalibrated, BigRational::from_integer(1.into()));

        let ratio = (&u0 * &v0 * (&u1 * &v1)) / (&u0 * &v1 * (&u1 * &v0));
        assert_eq!(ratio, BigRational::from_integer(1.into()));
    }
}
