//! Bivectors in `∧² Q^4`.
//!
//! Component order: `e01, e02, e03, e12, e13, e23`.
//! `from_wedge_half(u, v)` stores `(1/2)(u_i v_j - u_j v_i)`.
//! The coefficient of the unit 4-vector in `Σ ∧ Σ` is twice the pfaffian
//! `c01 c23 - c02 c13 + c03 c12`. Both vanish together, so simplicity is
//! `pfaffian = 0`.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use num_rational::BigRational;
use num_traits::Zero;

const PAIRS: [(usize, usize); 6] = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)];

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Bivector4 {
    pub c: [BigRational; 6],
}

impl Bivector4 {
    pub fn zero() -> Self {
        Self {
            c: std::array::from_fn(|_| BigRational::zero()),
        }
    }

    pub fn from_components(c: [BigRational; 6]) -> Self {
        Self { c }
    }

    pub fn from_wedge_half(u: &[BigRational; 4], v: &[BigRational; 4]) -> Self {
        let two = BigRational::from_integer(num_bigint::BigInt::from(2));
        Self {
            c: std::array::from_fn(|index| {
                let (i, j) = PAIRS[index];
                (&u[i] * &v[j] - &u[j] * &v[i]) / &two
            }),
        }
    }

    /// Pfaffian `c01 c23 - c02 c13 + c03 c12`.
    pub fn pfaffian(&self) -> BigRational {
        &self.c[0] * &self.c[5] - &self.c[1] * &self.c[4] + &self.c[2] * &self.c[3]
    }

    pub fn is_simple(&self) -> bool {
        self.pfaffian().is_zero()
    }

    pub fn checked_add(&self, other: &Self) -> Self {
        Self {
            c: std::array::from_fn(|index| &self.c[index] + &other.c[index]),
        }
    }

    pub fn checked_scale(&self, scale: &BigRational) -> Self {
        Self {
            c: std::array::from_fn(|index| &self.c[index] * scale),
        }
    }

    pub fn is_zero(&self) -> bool {
        self.c.iter().all(BigRational::is_zero)
    }
}
