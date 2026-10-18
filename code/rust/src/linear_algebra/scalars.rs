
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
    assert!(d != 0, "denominator cannot be zero");
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
    let reduced = val.reduced();
    hash_bigint(hasher, reduced.numer());
    hash_bigint(hasher, reduced.denom());
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn production_gaussian_rational_arithmetic_and_identities() {
        let i = GaussianRational::from_integers(0, 1);
        let minus_one = GaussianRational::from_integers(-1, 0);
        let one = GaussianRational::from_integers(1, 0);
        let zero = GaussianRational::from_integers(0, 0);

        // i^2 = -1
        assert_eq!(i.mul(&i), minus_one);

        // (1 + i)^(-1) = (1 - i) / 2
        let one_plus_i = GaussianRational::from_integers(1, 1);
        let inv = one_plus_i.try_inv().expect("invertible");
        assert_eq!(inv.real, qr(1, 2));
        assert_eq!(inv.imag, qr(-1, 2));
        assert_eq!(one_plus_i.mul(&inv), one);

        // z * conj(z) = norm_sq(z)
        let z = GaussianRational::new(qr(3, 4), qr(-5, 6));
        let z_conj = z.conjugate();
        let prod = z.mul(&z_conj);
        assert_eq!(prod.imag, qr(0, 1));
        assert_eq!(prod.real, z.norm_sq());

        // zero inversion is None
        assert_eq!(zero.try_inv(), None);

        // conjugation identities
        let z1 = GaussianRational::new(qr(1, 2), qr(3, 4));
        let z2 = GaussianRational::new(qr(-2, 5), qr(7, 3));
        assert_eq!(z1.conjugate().conjugate(), z1);
        assert_eq!(z1.add(&z2).conjugate(), z1.conjugate().add(&z2.conjugate()));
        assert_eq!(z1.mul(&z2).conjugate(), z1.conjugate().mul(&z2.conjugate()));

        // 2x2 rational matrix isomorphism
        // M(a + bi) = [[a, -b], [b, a]]
        let m_mul = |a1: &Q, b1: &Q, a2: &Q, b2: &Q| -> (Q, Q) {
            let r = a1 * a2 - b1 * b2;
            let im = a1 * b2 + b1 * a2;
            (r, im)
        };
        let (mr, mim) = m_mul(&z1.real, &z1.imag, &z2.real, &z2.imag);
        let z_prod = z1.mul(&z2);
        assert_eq!(z_prod.real, mr);
        assert_eq!(z_prod.imag, mim);
    }

    #[test]
    fn production_gaussian_rational_serde() {
        let z = GaussianRational::new(qr(7, 11), qr(-13, 17));
        let serialized = serde_json::to_string(&z).expect("serialize");
        let deserialized: GaussianRational = serde_json::from_str(&serialized).expect("deserialize");
        assert_eq!(z, deserialized);
    }

    #[test]
    fn hash_rational_unreduced_fractions_match() {
        let mut h1 = blake3::Hasher::new();
        hash_rational(&mut h1, &qr(1, 2));
        let mut h2 = blake3::Hasher::new();
        hash_rational(&mut h2, &qr(2, 4));
        assert_eq!(h1.finalize().as_bytes(), h2.finalize().as_bytes());
    }
}
