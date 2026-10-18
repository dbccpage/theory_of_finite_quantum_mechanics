
use num_bigint::BigInt;
use num_rational::BigRational;
use serde::{Deserialize, Serialize};

pub use ::linear_algebra::exact_field::involution::Involution;
pub use ::linear_algebra::scalars::{CheckedExactField, ExactRing, Field, Ring, Semiring};

pub type Q = BigRational;

#[inline]
pub fn q(n: i64) -> Q {
    BigRational::from_integer(BigInt::from(n))
}

#[inline]
pub fn qr(n: i64, d: i64) -> Q {
    BigRational::new(BigInt::from(n), BigInt::from(d))
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct GaussianRational {
    pub real: Q,
    pub imag: Q,
}

impl GaussianRational {
    pub fn new(real: Q, imag: Q) -> Self {
        Self { real, imag }
    }

    pub fn from_integers(r: i64, i: i64) -> Self {
        Self {
            real: q(r),
            imag: q(i),
        }
    }

    pub fn norm_sq(&self) -> Q {
        &self.real * &self.real + &self.imag * &self.imag
    }
}

impl Semiring for GaussianRational {
    fn zero() -> Self {
        Self {
            real: num_traits::Zero::zero(),
            imag: num_traits::Zero::zero(),
        }
    }
    fn one() -> Self {
        Self {
            real: num_traits::One::one(),
            imag: num_traits::Zero::zero(),
        }
    }
    fn add(&self, rhs: &Self) -> Self {
        Self {
            real: &self.real + &rhs.real,
            imag: &self.imag + &rhs.imag,
        }
    }
    fn mul(&self, rhs: &Self) -> Self {
        Self {
            real: &self.real * &rhs.real - &self.imag * &rhs.imag,
            imag: &self.real * &rhs.imag + &self.imag * &rhs.real,
        }
    }
    fn is_zero(&self) -> bool {
        num_traits::Zero::is_zero(&self.real) && num_traits::Zero::is_zero(&self.imag)
    }
}

impl Ring for GaussianRational {
    fn neg(&self) -> Self {
        Self {
            real: -&self.real,
            imag: -&self.imag,
        }
    }
}

impl Field for GaussianRational {
    fn try_inv(&self) -> Option<Self> {
        let n = self.norm_sq();
        if num_traits::Zero::is_zero(&n) {
            None
        } else {
            Some(Self {
                real: &self.real / &n,
                imag: -&self.imag / &n,
            })
        }
    }
}

impl ExactRing for GaussianRational {}

impl Involution for GaussianRational {
    fn conjugate(&self) -> Self {
        Self {
            real: self.real.clone(),
            imag: -&self.imag,
        }
    }
}

pub fn hash_bigint(hasher: &mut blake3::Hasher, value: &BigInt) {
    let bytes = value.to_signed_bytes_le();
    hasher.update(&(bytes.len() as u64).to_le_bytes());
    hasher.update(&bytes);
}

pub fn hash_rational(hasher: &mut blake3::Hasher, val: &Q) {
    hash_bigint(hasher, val.numer());
    hash_bigint(hasher, val.denom());
}