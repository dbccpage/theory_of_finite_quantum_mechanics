// AuthorityEffect: None.

//! Finite toggle dynamics and rational unitary evolution.
//!
//! Formalizes Band D (Steps 31–38) in Rust:
//! - Toggle square root obstruction: det(X) = -1 has no real matrix square root.
//! - Exact complex square root in Z[i] at scale 4: M^2 = 4*X.
//! - Cayley rational transform: cay_tau(X) = ((1 - tau^2)*I - 2*i*tau*X) / (1 + tau^2)
//!   producing exact rational unitaries over Q(i) without floats or continuum approximations.
//! - Abelian group composition: tau_comp = (tau1 + tau2) / (1 - tau1 * tau2).

use omega_number_theory::rational::Rational;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct CayleyUnitary2x2 {
    pub tau: Rational,
    pub diag_re: Rational,
    pub offdiag_im: Rational,
    pub norm_sq: Rational,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ToggleSquareRootReport {
    pub det_x: i64,
    pub has_real_matrix_sqrt: bool,
    pub scale4_complex_sqrt_verified: bool,
    pub interpolant_not_unique: bool,
}

/// Computes the exact rational Cayley unitary for toggle X = [[0, 1], [1, 0]].
pub fn cayley_transform_toggle(tau: Rational) -> CayleyUnitary2x2 {
    let scalar = omega_lie_theory::cayley::unit_from_parameter(&(-tau.clone()));
    let diag_re = scalar.re;
    let offdiag_im = scalar.im;
    let norm_sq = &diag_re * &diag_re + &offdiag_im * &offdiag_im;

    CayleyUnitary2x2 {
        tau,
        diag_re,
        offdiag_im,
        norm_sq,
    }
}

/// Verifies toggle square root algebraic obstruction.
pub fn verify_toggle_square_roots() -> ToggleSquareRootReport {
    // 1. det(X) = -1. det(M^2) = det(M)^2 = -1 has no real root.
    let det_x = -1i64;
    let has_real = false;

    // 2. Exact scale-4 square root in Z[i]:
    // M = [[1+i, 1-i], [1-i, 1+i]]
    // Diagonal: (1+i)^2 + (1-i)^2 = 2i - 2i = 0
    // Off-diagonal: (1+i)(1-i) + (1-i)(1+i) = 2 + 2 = 4
    let roots = crate::finite_report_dynamics::swap_interpolants(4).expect("positive scale");
    let verified = roots.len() == 4
        && roots.iter().all(|r| {
            linear_algebra::exact_field::matrix::multiply_with_limits(
                &(r),
                r,
                linear_algebra::backend::basic_matrix::OperationLimits {
                    max_elements: 1 << 20,
                    max_scalar_ops: 1 << 24,
                },
            )
            .expect("validated finite matrix shape and budget")
                == linear_algebra::exact_field::matrix::from_rows(vec![
                    vec![
                        crate::exact_hermitian::gi(0, 0),
                        crate::exact_hermitian::gi(4, 0),
                    ],
                    vec![
                        crate::exact_hermitian::gi(4, 0),
                        crate::exact_hermitian::gi(0, 0),
                    ],
                ])
                .expect("fixed square matrix")
        });

    ToggleSquareRootReport {
        det_x,
        has_real_matrix_sqrt: has_real,
        scale4_complex_sqrt_verified: verified,
        interpolant_not_unique: roots.len() > 1,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_number_theory::rational::{rq, One, Zero};

    #[test]
    fn test_cayley_toggle_unitarity_and_pythagorean_triples() {
        // tau = 0 -> a = 1, b = 0
        let c0 = cayley_transform_toggle(Rational::zero());
        assert_eq!(c0.diag_re, Rational::one());
        assert_eq!(c0.offdiag_im, Rational::zero());
        assert_eq!(c0.norm_sq, Rational::one());

        // tau = 1/2 -> a = (1 - 1/4)/(1 + 1/4) = 3/5, b = -1/(5/4) = -4/5
        let c_half = cayley_transform_toggle(rq(1, 2));
        assert_eq!(c_half.diag_re, rq(3, 5));
        assert_eq!(c_half.offdiag_im, rq(-4, 5));
        assert_eq!(c_half.norm_sq, Rational::one());

        // tau = 3/4 -> a = (1 - 9/16)/(1 + 9/16) = 7/25, b = (-3/2)/(25/16) = -24/25
        let c_three_quarters = cayley_transform_toggle(rq(3, 4));
        assert_eq!(c_three_quarters.diag_re, rq(7, 25));
        assert_eq!(c_three_quarters.offdiag_im, rq(-24, 25));
        assert_eq!(c_three_quarters.norm_sq, Rational::one());
    }

    #[test]
    fn test_cayley_composition_group_law() {
        // tau1 = 1/2, tau2 = 1/3 -> tau_comp = (1/2 + 1/3) / (1 - 1/6) = (5/6)/(5/6) = 1
        let tau1 = rq(1, 2);
        let tau2 = rq(1, 3);
        let comp =
            omega_lie_theory::cayley::compactified_circle_composition(Some(&tau1), Some(&tau2))
                .unwrap();
        assert_eq!(comp, Rational::one());

        let c_comp = cayley_transform_toggle(comp);
        assert_eq!(c_comp.diag_re, Rational::zero());
        assert_eq!(c_comp.offdiag_im, rq(-1, 1));
        assert_eq!(c_comp.norm_sq, Rational::one());
    }

    #[test]
    fn test_toggle_square_root_properties() {
        let rep = verify_toggle_square_roots();
        assert_eq!(rep.det_x, -1);
        assert!(!rep.has_real_matrix_sqrt);
        assert!(rep.scale4_complex_sqrt_verified);
        assert!(rep.interpolant_not_unique);
    }
}
