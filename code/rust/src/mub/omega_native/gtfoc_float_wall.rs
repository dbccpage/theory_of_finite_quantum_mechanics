//! Shared f64 helpers for the dimension-6 and dimension-10 wall cross-checks.
//!
//! The dimension lives on the vector length, not in a copied function body.
//! These routines are numerical diagnostics. They mint no MUB authority.

use linear_algebra::linear_algebra::complex_matrix::{CVector, C64};
use std::f64::consts::PI;

type C = C64;
type Vector = CVector;

pub(crate) fn qubit_x_basis() -> Vec<Vector> {
    let s = 1.0 / 2.0_f64.sqrt();
    vec![
        Vector::from_vec(vec![C::new(s, 0.0), C::new(s, 0.0)]),
        Vector::from_vec(vec![C::new(s, 0.0), C::new(-s, 0.0)]),
    ]
}

pub(crate) fn qubit_y_basis() -> Vec<Vector> {
    let s = 1.0 / 2.0_f64.sqrt();
    vec![
        Vector::from_vec(vec![C::new(s, 0.0), C::new(0.0, s)]),
        Vector::from_vec(vec![C::new(s, 0.0), C::new(0.0, -s)]),
    ]
}

pub(crate) fn projected_s_gradient(columns: &[Vector], v: &Vector) -> Vector {
    let dim = v.len();
    let mut grad = zero_vec(dim);
    for c in columns {
        let a = inner(c, v);
        let p = a.norm_sqr();
        for i in 0..dim {
            grad[i] += c[i] * a * (4.0 * p);
        }
    }
    let radial = inner(v, &grad).re;
    for i in 0..dim {
        grad[i] -= v[i] * radial;
    }
    grad
}

pub(crate) fn probabilities(columns: &[Vector], v: &Vector) -> Vec<f64> {
    columns.iter().map(|c| inner(c, v).norm_sqr()).collect()
}

pub(crate) fn residual_square_sum(columns: &[Vector], v: &Vector) -> f64 {
    probabilities(columns, v).iter().map(|p| p * p).sum::<f64>()
}

pub(crate) fn tensor_vec(left: &Vector, right: &Vector) -> Vector {
    let mut out = Vec::with_capacity(left.len() * right.len());
    for l in left.iter() {
        for r in right.iter() {
            out.push(*l * *r);
        }
    }
    Vector::from_vec(out)
}

pub(crate) fn inner(left: &Vector, right: &Vector) -> C {
    left.iter().zip(right).map(|(l, r)| l.conj() * *r).sum()
}

pub(crate) fn norm(v: &Vector) -> f64 {
    v.iter().map(|z| z.norm_sqr()).sum::<f64>().sqrt()
}

pub(crate) fn zero_vec(dim: usize) -> Vector {
    Vector::from_element(dim, C::new(0.0, 0.0))
}

pub(crate) fn seeded_unit_vector(seed: u64, dim: usize) -> Vector {
    let mut state = seed.wrapping_mul(0x9e37_79b9_7f4a_7c15).wrapping_add(1);
    let mut v = zero_vec(dim);
    for item in &mut v {
        state = state
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        let re = unit_from_state(state);
        state = state
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        let im = unit_from_state(state);
        *item = C::new(re, im);
    }
    normalize(&v)
}

pub(crate) fn unit_from_state(state: u64) -> f64 {
    let x = ((state >> 11) as f64) / ((1_u64 << 53) as f64);
    2.0 * x - 1.0
}

pub(crate) fn root_of_unity(order: i32, exponent: i32) -> C {
    let angle = 2.0 * PI * (exponent.rem_euclid(order) as f64) / (order as f64);
    C::new(angle.cos(), angle.sin())
}

fn normalize(v: &Vector) -> Vector {
    let mut out = v.clone();
    let n = norm(&out);
    if n > 0.0 {
        for item in out.iter_mut() {
            *item /= n;
        }
    }
    out
}
