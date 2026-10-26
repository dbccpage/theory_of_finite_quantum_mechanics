//! Pillar 3: Exact Gaussian Rationals Q(i) and Discrete Bianchi Holonomies.
//!
//! AuthorityEffect: None. GenesisEffect: None.
//!
//! Implements exact complex arithmetic over Gaussian rationals Q(i) without floating-point error,
//! and evaluates discrete 4D Bianchi identity closures over path-ordered holonomy products.

use num_rational::Rational64;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GaussianRational {
    pub re: Rational64,
    pub im: Rational64,
}

impl GaussianRational {
    pub fn new(re: Rational64, im: Rational64) -> Self {
        Self { re, im }
    }

    pub fn zero() -> Self {
        Self {
            re: Rational64::new(0, 1),
            im: Rational64::new(0, 1),
        }
    }

    pub fn one() -> Self {
        Self {
            re: Rational64::new(1, 1),
            im: Rational64::new(0, 1),
        }
    }

    pub fn i() -> Self {
        Self {
            re: Rational64::new(0, 1),
            im: Rational64::new(1, 1),
        }
    }

    pub fn add(&self, other: &Self) -> Self {
        Self {
            re: self.re + other.re,
            im: self.im + other.im,
        }
    }

    pub fn sub(&self, other: &Self) -> Self {
        Self {
            re: self.re - other.re,
            im: self.im - other.im,
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        Self {
            re: self.re * other.re - self.im * other.im,
            im: self.re * other.im + self.im * other.re,
        }
    }

    pub fn conj(&self) -> Self {
        Self {
            re: self.re,
            im: -self.im,
        }
    }

    pub fn norm_sq(&self) -> Rational64 {
        self.re * self.re + self.im * self.im
    }

    pub fn inv(&self) -> Option<Self> {
        let n = self.norm_sq();
        if n == Rational64::new(0, 1) {
            None
        } else {
            Some(Self {
                re: self.re / n,
                im: -self.im / n,
            })
        }
    }

    pub fn is_one(&self) -> bool {
        self.re == Rational64::new(1, 1) && self.im == Rational64::new(0, 1)
    }

    pub fn is_zero(&self) -> bool {
        self.re == Rational64::new(0, 1) && self.im == Rational64::new(0, 1)
    }
}

/// 4D Simplex Frame Transformation Matrix over Gaussian Rationals.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Simplex4DFrame {
    pub rotation_matrix: [[GaussianRational; 4]; 4],
}

impl Simplex4DFrame {
    pub fn identity() -> Self {
        let mut m = std::array::from_fn(|_| std::array::from_fn(|_| GaussianRational::zero()));
        for idx in 0..4 {
            m[idx][idx] = GaussianRational::one();
        }
        Self { rotation_matrix: m }
    }

    pub fn mul(&self, other: &Self) -> Self {
        let mut out = std::array::from_fn(|_| std::array::from_fn(|_| GaussianRational::zero()));
        for r in 0..4 {
            for c in 0..4 {
                let mut sum = GaussianRational::zero();
                for k in 0..4 {
                    let term = self.rotation_matrix[r][k].mul(&other.rotation_matrix[k][c]);
                    sum = sum.add(&term);
                }
                out[r][c] = sum;
            }
        }
        Self { rotation_matrix: out }
    }

    /// Conjugate transpose (Hermitian adjoint).
    pub fn adjoint(&self) -> Self {
        let mut out = std::array::from_fn(|_| std::array::from_fn(|_| GaussianRational::zero()));
        for r in 0..4 {
            for c in 0..4 {
                out[r][c] = self.rotation_matrix[c][r].conj();
            }
        }
        Self { rotation_matrix: out }
    }

    pub fn is_identity(&self) -> bool {
        for r in 0..4 {
            for c in 0..4 {
                let expected = if r == c {
                    GaussianRational::one()
                } else {
                    GaussianRational::zero()
                };
                if self.rotation_matrix[r][c] != expected {
                    return false;
                }
            }
        }
        true
    }
}

/// Verifies path-ordered discrete Bianchi closure:
/// prod_{k=1}^m (P_k * R_{t_k} * P_k^-1) = I_4.
pub fn verify_bianchi_closure(
    loop_transports: &[(Simplex4DFrame, Simplex4DFrame)], // (P_k, R_{t_k})
) -> bool {
    let mut product = Simplex4DFrame::identity();
    for (p_k, r_tk) in loop_transports {
        let p_inv = p_k.adjoint();
        let transported_hinge = p_k.mul(r_tk).mul(&p_inv);
        product = product.mul(&transported_hinge);
    }
    product.is_identity()
}
