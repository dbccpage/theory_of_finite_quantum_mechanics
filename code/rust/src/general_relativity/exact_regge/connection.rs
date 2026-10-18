//! Dynamical tetrad transitions in `SO(4, Q)` and hinge holonomy.
//!
//! `pythagorean_so4` is the plane rotation
//! `[[3/5, -4/5, 0, 0], [4/5, 3/5, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]`.
//! Its inverse is its transpose. Both pass `So4::try_new`.
//! Holonomy is a product of certified matrices. The deficit
//! `ε_h = 2π - Σ θ` is not computed.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use super::manifold::ManifoldError;
use linear_algebra::regge_exact::{q_ratio, So4};
use num_rational::BigRational;

pub fn identity_transition() -> So4 {
    So4::identity()
}

pub fn pythagorean_so4() -> So4 {
    So4::try_new(pythagorean_matrix()).expect("3-4-5 rotation is in SO(4,Q)")
}

pub fn pythagorean_so4_inverse() -> So4 {
    let transposed = pythagorean_so4().transpose();
    So4::try_new(transposed.m).expect("3-4-5 rotation is in SO(4,Q)")
}

/// Ordered product of certified `SO(4, Q)` transitions along a hinge.
///
/// The empty word is the identity. A nonempty slice folds `So4::mul` from the
/// left, in slice order: `t0 * t1 * ... * tn`.
/// `ε_h = 2π - Σ θ` is not computed.
///
/// AuthorityEffect: None.
pub fn hinge_holonomy(transitions: &[So4]) -> So4 {
    transitions
        .iter()
        .fold(identity_transition(), |product, step| product.mul(step))
}

pub fn try_transition(matrix: [[BigRational; 4]; 4]) -> Result<So4, ManifoldError> {
    So4::try_new(matrix).map_err(|_| ManifoldError::FrameRejected)
}

fn pythagorean_matrix() -> [[BigRational; 4]; 4] {
    const RAW: [[(i64, i64); 4]; 4] = [
        [(3, 5), (-4, 5), (0, 1), (0, 1)],
        [(4, 5), (3, 5), (0, 1), (0, 1)],
        [(0, 1), (0, 1), (1, 1), (0, 1)],
        [(0, 1), (0, 1), (0, 1), (1, 1)],
    ];
    std::array::from_fn(|row| {
        std::array::from_fn(|column| {
            let (numerator, denominator) = RAW[row][column];
            q_ratio(numerator, denominator).expect("3-4-5 rotation is in SO(4,Q)")
        })
    })
}
