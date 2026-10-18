//! Shared inversion for power-basis number fields `Q[t]/(f)`.
//!
//! Every cyclotomic type in this crate stores an element as the coefficient vector
//! of a polynomial in a primitive root `t`, reduced modulo the cyclotomic
//! polynomial. The inverse of `x` is the unique `y` with `x * y = 1`, i.e. the
//! solution of the linear system `M_x y = e_0`, where column `j` of `M_x` holds the
//! coefficients of `x * t^j`. That system is solved exactly by
//! `linear_algebra::solve_in_image`, so no type carries its own elimination.
//!
//! AuthorityEffect: None.

use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::linear_algebra::image_kernel::{solve_in_image, ImageMembership};
use num_traits::{One, Zero};

use crate::rational::Rational;

/// Coefficients of `x^{-1}`, or `None` when `x` is zero (not invertible).
///
/// `column(j)` must return the `dim` coefficients of `x * t^j`.
pub fn invert_by_multiplication_matrix(
    dim: usize,
    column: impl Fn(usize) -> Vec<Rational>,
) -> Option<Vec<Rational>> {
    if dim == 0 {
        return None;
    }
    let mut data = vec![Rational::zero(); dim * dim];
    for j in 0..dim {
        let col = column(j);
        if col.len() != dim {
            return None;
        }
        for (i, c) in col.into_iter().enumerate() {
            data[i * dim + j] = c;
        }
    }
    let matrix = BasicMatrix::from_row_major(dim, dim, data).ok()?;
    let mut unit = vec![Rational::zero(); dim];
    unit[0] = Rational::one();
    match solve_in_image(&matrix, &unit).ok()? {
        ImageMembership::InImage(witness) => Some(witness.potential),
        ImageMembership::NotInImage { .. } => None,
    }
}
