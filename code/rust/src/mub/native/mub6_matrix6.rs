
use serde::{Deserialize, Serialize};

use crate::native::exact::d6_exact_curvature_cochain::D;
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::ri;

pub type Matrix6 = [[Cyc24; D]; D];

pub fn matrix_zero() -> Matrix6 {
    std::array::from_fn(|_| std::array::from_fn(|_| Cyc24::zero()))
}

pub fn matrix_identity() -> Matrix6 {
    let one = Cyc24::rat(ri(1));
    let zero = Cyc24::zero();
    std::array::from_fn(|i| {
        std::array::from_fn(|j| if i == j { one.clone() } else { zero.clone() })
    })
}

pub fn matrix_mul(a: &Matrix6, b: &Matrix6) -> Matrix6 {
    std::array::from_fn(|i| {
        std::array::from_fn(|j| {
            let mut acc = Cyc24::zero();
            for k in 0..D {
                acc = acc.add(&a[i][k].mul(&b[k][j]));
            }
            acc
        })
    })
}

pub fn matrix_adjoint(m: &Matrix6) -> Matrix6 {
    std::array::from_fn(|i| std::array::from_fn(|j| m[j][i].conj()))
}

pub fn eye3() -> [[Cyc24; 3]; 3] {
    let zero = Cyc24::zero();
    let one = Cyc24::rat(ri(1));
    [
        [one.clone(), zero.clone(), zero.clone()],
        [zero.clone(), one.clone(), zero.clone()],
        [zero.clone(), zero, one],
    ]
}

pub fn mul_mat3(a: &[[Cyc24; 3]; 3], b: &[[Cyc24; 3]; 3]) -> [[Cyc24; 3]; 3] {
    std::array::from_fn(|i| {
        std::array::from_fn(|j| {
            let mut acc = Cyc24::zero();
            for k in 0..3 {
                acc = acc.add(&a[i][k].mul(&b[k][j]));
            }
            acc
        })
    })
}

pub const NUM_SUBMATRICES_225: usize = 225;

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct Submatrix2Index {
    pub r0: usize,
    pub r1: usize,
    pub c0: usize,
    pub c1: usize,
}

impl Submatrix2Index {
    pub fn new(r0: usize, r1: usize, c0: usize, c1: usize) -> Self {
        assert!(r0 < r1 && r1 < D, "Invalid row indices");
        assert!(c0 < c1 && c1 < D, "Invalid col indices");
        Self { r0, r1, c0, c1 }
    }
}

fn append_submatrices_for_rows(r0: usize, r1: usize, indices: &mut Vec<Submatrix2Index>) {
    for c0 in 0..D {
        for c1 in (c0 + 1)..D {
            indices.push(Submatrix2Index::new(r0, r1, c0, c1));
        }
    }
}

pub fn enumerate_225_submatrices() -> Vec<Submatrix2Index> {
    let mut indices = Vec::with_capacity(NUM_SUBMATRICES_225);
    for r0 in 0..D {
        for r1 in (r0 + 1)..D {
            append_submatrices_for_rows(r0, r1, &mut indices);
        }
    }
    indices
}

pub fn cross_ratio_at(m: &Matrix6, idx: &Submatrix2Index) -> Cyc24 {
    let a = &m[idx.r0][idx.c0];
    let b = &m[idx.r0][idx.c1];
    let c = &m[idx.r1][idx.c0];
    let d = &m[idx.r1][idx.c1];
    a.mul(d).mul(&b.conj()).mul(&c.conj())
}

pub fn evaluate_all_225_cross_ratios(m: &Matrix6) -> Vec<Cyc24> {
    enumerate_225_submatrices()
        .iter()
        .map(|idx| cross_ratio_at(m, idx))
        .collect()
}

pub fn root24_exponent(z: &Cyc24) -> Option<i64> {
    (0..24).find(|&k| z == &Cyc24::zeta24(k)).map(|k| k as i64)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn identity_is_neutral_for_matrix_mul() {
        let mut m = matrix_zero();
        for i in 0..D {
            for j in 0..D {
                m[i][j] = Cyc24::zeta24(((i * j) % 24) as i32);
            }
        }
        assert_eq!(matrix_mul(&matrix_identity(), &m), m);
        assert_eq!(matrix_mul(&m, &matrix_identity()), m);
        assert_eq!(matrix_mul(&matrix_zero(), &m), matrix_zero());
    }

    #[test]
    fn conjugate_cross_ratio_differs_from_the_quotient_on_a_scaled_entry() {
        let mut m = matrix_identity();
        m[0][1] = Cyc24::zeta24(1).mul(&Cyc24::rat(ri(1) / ri(6)));
        m[1][0] = Cyc24::rat(ri(1));
        let idx = Submatrix2Index::new(0, 1, 0, 1);
        let quotient = m[0][0]
            .mul(&m[1][1])
            .mul(&m[0][1].mul(&m[1][0]).inv());
        assert_ne!(cross_ratio_at(&m, &idx), quotient);
        assert_eq!(enumerate_225_submatrices().len(), NUM_SUBMATRICES_225);
    }
}
