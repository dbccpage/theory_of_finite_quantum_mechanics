use std::cmp::Ordering;

use linear_algebra::scalars::{ExactRing, Field};
use num_traits::Signed;
use tfqm_number_theory::cyclotomic::{Cyc12, Cyc24, Cyc5, Cyc8, EisensteinRat, GaussianRat};
use tfqm_number_theory::cyclotomic120::Cyc120;
use tfqm_number_theory::cyclotomic28::Cyc28;
use tfqm_number_theory::cyclotomic44::Cyc44;
use tfqm_number_theory::cyclotomic52::Cyc52;
use tfqm_number_theory::cyclotomic_field::{Cyclotomic, CyclotomicNumber};
use tfqm_number_theory::rational::Rational;
use tfqm_number_theory::real_embedding::real_embeddings;

use crate::error::FusionError;

/// Lawful exact fields with rational embedding and compatible conjugation.
/// Implementations advertise a generator of exact order `root_of_unity_order`.
/// This open protocol cannot enforce these algebraic laws for client impls.
/// Root helpers admit orders at most 4096; sign failures remain undecided.
pub trait FusionScalar:
    Field
    + ExactRing
    + linear_algebra::exact_field::involution::Involution
    + tfqm_number_theory::scalar::RationalEmbedding
{
    fn to_rational(&self) -> Option<Rational>;

    fn root_of_unity_order() -> u32;

    fn primitive_root_of_unity() -> Self;

    fn real_sign(&self) -> Option<Ordering> {
        None
    }

    fn root_of_unity(n: u32, k: i64) -> Option<Self>
    where
        Self: Sized,
    {
        let w = Self::root_of_unity_order();
        if n == 0 || w == 0 || w > 4096 || w % n != 0 {
            return None;
        }
        let step = i64::from(w / n);
        // Reduce before scaling: even i64::MIN/MAX have a small residue.
        // 0 <= residue < n and step*n = w <= 4096, so this product fits.
        let exponent = k.rem_euclid(i64::from(n)) * step;
        let exponent = u32::try_from(exponent).ok()?;
        tfqm_number_theory::scalar::power_unsigned(
            &Self::primitive_root_of_unity(),
            u64::from(exponent),
        )
        .ok()
    }
}

pub fn sign_of<K: FusionScalar>(x: &K) -> Result<Ordering, FusionError> {
    x.real_sign().ok_or(FusionError::SignUndecided {
        context: "a real scalar",
    })
}

pub fn root_of_unity<K: FusionScalar>(n: u32, k: i64) -> Result<K, FusionError> {
    K::root_of_unity(n, k).ok_or(FusionError::FieldTooSmall {
        needed: "a primitive root of unity of the requested order",
    })
}

pub fn sqrt_two<K: FusionScalar>() -> Result<K, FusionError> {
    let zeta = K::root_of_unity(8, 1).ok_or(FusionError::FieldTooSmall {
        needed: "sqrt(2) (an eighth root of unity)",
    })?;
    let inverse = K::root_of_unity(8, -1).ok_or(FusionError::FieldTooSmall {
        needed: "sqrt(2) (an eighth root of unity)",
    })?;
    Ok(zeta.add(&inverse))
}

pub fn golden_ratio<K: FusionScalar>() -> Result<K, FusionError> {
    let zeta = K::root_of_unity(10, 1).ok_or(FusionError::FieldTooSmall {
        needed: "the golden ratio (a tenth root of unity)",
    })?;
    let inverse = K::root_of_unity(10, -1).ok_or(FusionError::FieldTooSmall {
        needed: "the golden ratio (a tenth root of unity)",
    })?;
    Ok(zeta.add(&inverse))
}

pub fn root_of_unity_data<K: FusionScalar>(x: &K) -> Option<(u32, u32)> {
    let w = K::root_of_unity_order();
    if w == 0 || w > 4096 {
        return None;
    }
    let generator = K::primitive_root_of_unity();
    let mut current = K::one();
    for k in 0..w {
        if current == *x {
            let g = num_integer::Integer::gcd(&k, &w);
            return Some((w / g, k / g));
        }
        current = current.mul(&generator);
    }
    None
}

fn constant_term(coefficients: &[Rational]) -> Option<Rational> {
    let (first, rest) = coefficients.split_first()?;
    rest.iter()
        .all(num_traits::Zero::is_zero)
        .then(|| first.clone())
}

impl FusionScalar for Rational {
    fn to_rational(&self) -> Option<Rational> {
        Some(self.clone())
    }
    fn root_of_unity_order() -> u32 {
        2
    }
    fn primitive_root_of_unity() -> Self {
        -Rational::from_integer(1.into())
    }
    fn real_sign(&self) -> Option<Ordering> {
        Some(if self.is_positive() {
            Ordering::Greater
        } else if self.is_negative() {
            Ordering::Less
        } else {
            Ordering::Equal
        })
    }
}

impl FusionScalar for GaussianRat {
    fn to_rational(&self) -> Option<Rational> {
        num_traits::Zero::is_zero(&self.im).then(|| self.re.clone())
    }
    fn root_of_unity_order() -> u32 {
        4
    }
    fn primitive_root_of_unity() -> Self {
        GaussianRat::i()
    }
    fn real_sign(&self) -> Option<Ordering> {
        if num_traits::Zero::is_zero(&self.im) {
            FusionScalar::real_sign(&self.re)
        } else {
            None
        }
    }
}

impl FusionScalar for EisensteinRat {
    fn to_rational(&self) -> Option<Rational> {
        num_traits::Zero::is_zero(&self.b).then(|| self.a.clone())
    }
    fn root_of_unity_order() -> u32 {
        6
    }
    fn primitive_root_of_unity() -> Self {
        EisensteinRat::one().add(&EisensteinRat::zeta3())
    }
    fn real_sign(&self) -> Option<Ordering> {
        if num_traits::Zero::is_zero(&self.b) {
            FusionScalar::real_sign(&self.a)
        } else {
            None
        }
    }
}

fn cyclotomic_sign(number: &CyclotomicNumber) -> Option<Ordering> {
    if !number.is_real() {
        return None;
    }
    real_embeddings(number.conductor()).ok()?.sign(number).ok()
}

impl<const N: usize> FusionScalar for Cyclotomic<N> {
    fn to_rational(&self) -> Option<Rational> {
        self.as_rational()
    }
    fn root_of_unity_order() -> u32 {
        if N == 0 || N > tfqm_number_theory::polynomial::MAX_CONDUCTOR {
            return 0;
        }
        let order = if N % 2 == 0 { N } else { 2 * N };
        u32::try_from(order).unwrap_or(u32::MAX)
    }
    fn primitive_root_of_unity() -> Self {
        if N % 2 == 0 {
            Cyclotomic::zeta(1)
        } else {
            let exponent = i64::try_from((N + 1) / 2).unwrap_or(1);
            Cyclotomic::zeta(exponent).neg()
        }
    }
    fn real_sign(&self) -> Option<Ordering> {
        cyclotomic_sign(self.as_number())
    }
}

macro_rules! cyclotomic_scalar {
    ($ty:ty, $order:expr, $root:expr) => {
        impl FusionScalar for $ty {
            fn to_rational(&self) -> Option<Rational> {
                constant_term(&self.a)
            }
            fn root_of_unity_order() -> u32 {
                $order
            }
            fn primitive_root_of_unity() -> Self {
                $root
            }
            fn real_sign(&self) -> Option<Ordering> {
                cyclotomic_sign(&CyclotomicNumber::from(self))
            }
        }
    };
}

cyclotomic_scalar!(Cyc5, 10, {
    let z = Cyc5::zeta5(3);
    Cyc5::zero().sub(&z)
});
cyclotomic_scalar!(Cyc8, 8, Cyc8::zeta8(1));
cyclotomic_scalar!(Cyc12, 12, Cyc12::zeta12(1));
cyclotomic_scalar!(Cyc24, 24, Cyc24::zeta24(1));
cyclotomic_scalar!(Cyc28, 28, Cyc28::zeta(1));
cyclotomic_scalar!(Cyc44, 44, Cyc44::zeta(1));
cyclotomic_scalar!(Cyc52, 52, Cyc52::zeta(1));
cyclotomic_scalar!(Cyc120, 120, Cyc120::zeta(1));

#[cfg(test)]
mod tests {
    use super::*;
    use linear_algebra::exact_field::involution::Involution;
    use tfqm_number_theory::rational::rq;
    use tfqm_number_theory::scalar::RationalEmbedding;
    use tfqm_number_theory::scalar::{from_i64, ScalarError};

    fn check_roots<K: FusionScalar>() {
        let w = K::root_of_unity_order();
        let zeta = K::primitive_root_of_unity();
        assert_eq!(
            tfqm_number_theory::scalar::power_unsigned(&zeta, (w).into()).unwrap(),
            K::one(),
            "zeta^w = 1"
        );
        for d in 1..w {
            if w % d == 0 {
                assert_ne!(
                    tfqm_number_theory::scalar::power_unsigned(&zeta, (d).into()).unwrap(),
                    K::one(),
                    "zeta has no smaller order than w (checked divisor {d})"
                );
            }
        }
        assert_eq!(
            tfqm_number_theory::scalar::power_unsigned(&zeta, (w / 2).into()).unwrap(),
            K::one().neg(),
            "the unique involution is -1"
        );
        assert_eq!(
            zeta.conjugate().mul(&zeta),
            K::one(),
            "conjugation inverts roots of unity"
        );
    }

    #[test]
    fn every_scalar_advertises_a_primitive_root_of_exact_order() {
        check_roots::<Rational>();
        check_roots::<GaussianRat>();
        check_roots::<EisensteinRat>();
        check_roots::<Cyc5>();
        check_roots::<Cyc8>();
        check_roots::<Cyc12>();
        check_roots::<Cyc24>();
        check_roots::<Cyc28>();
    }

    #[test]
    fn roots_of_unity_of_a_divisor_order_are_powers_of_the_generator() {
        let z10 = Cyc5::root_of_unity(10, 1).unwrap();
        assert_eq!(z10, Cyc5::zeta5(3).neg());
        assert_eq!(Cyc5::root_of_unity(5, 1).unwrap(), z10.mul(&z10));
        assert_eq!(Cyc5::root_of_unity(5, 1).unwrap(), Cyc5::zeta5(1));
        assert_eq!(
            Cyc5::root_of_unity(10, -4)
                .unwrap()
                .mul(&Cyc5::root_of_unity(10, 4).unwrap()),
            Cyc5::one()
        );
        assert!(Cyc5::root_of_unity(8, 1).is_none());
        assert!(Rational::root_of_unity(3, 1).is_none());
        assert_eq!(
            Rational::root_of_unity(2, 1),
            Some(-Rational::from_integer(1.into()))
        );
        assert!(Rational::root_of_unity(0, 1).is_none());
    }

    #[test]
    fn root_of_unity_data_reports_the_exact_order() {
        assert_eq!(root_of_unity_data(&Cyc8::zeta8(2)), Some((4, 1)));
        assert_eq!(root_of_unity_data(&Cyc8::zeta8(6)), Some((4, 3)));
        assert_eq!(root_of_unity_data(&Cyc8::zeta8(3)), Some((8, 3)));
        assert_eq!(root_of_unity_data(&Cyc8::one()), Some((1, 0)));
        assert_eq!(root_of_unity_data(&Cyc8::one().neg()), Some((2, 1)));
        assert_eq!(root_of_unity_data(&sqrt_two::<Cyc8>().unwrap()), None);
        assert_eq!(root_of_unity_data(&GaussianRat::i()), Some((4, 1)));
    }

    #[test]
    fn sqrt_two_and_the_golden_ratio_satisfy_their_minimal_polynomials() {
        let s = sqrt_two::<Cyc8>().unwrap();
        assert_eq!(s.mul(&s), from_i64::<Cyc8>(2));
        let phi = golden_ratio::<Cyc5>().unwrap();
        assert_eq!(phi.mul(&phi), phi.add(&Cyc5::one()));
        assert_eq!(
            sqrt_two::<GaussianRat>(),
            Err(FusionError::FieldTooSmall {
                needed: "sqrt(2) (an eighth root of unity)"
            })
        );
        assert!(golden_ratio::<Cyc8>().is_err());
    }

    #[test]
    fn rational_embedding_round_trips_and_detects_non_rationals() {
        let q = rq(-7, 3);
        assert_eq!(Cyc24::from_rational(&q).to_rational(), Some(q.clone()));
        assert_eq!(Cyc5::from_rational(&q).to_rational(), Some(q.clone()));
        assert_eq!(
            <GaussianRat as tfqm_number_theory::scalar::RationalEmbedding>::from_rational(&q)
                .to_rational(),
            Some(q.clone())
        );
        assert_eq!(
            <EisensteinRat as tfqm_number_theory::scalar::RationalEmbedding>::from_rational(&q)
                .to_rational(),
            Some(q)
        );
        assert_eq!(Cyc5::zeta5(1).to_rational(), None);
        assert_eq!(GaussianRat::i().to_rational(), None);
        let a = rq(2, 5);
        let b = rq(-1, 4);
        assert_eq!(
            Cyc12::from_rational(&a).mul(&Cyc12::from_rational(&b)),
            Cyc12::from_rational(&(&a * &b))
        );
    }

    #[test]
    fn powers_handle_negative_exponents_and_refuse_zero() {
        let z = Cyc8::zeta8(1);
        assert_eq!(
            tfqm_number_theory::scalar::power(&z, 8)
                .map_err(FusionError::from)
                .unwrap(),
            Cyc8::one()
        );
        assert_eq!(
            tfqm_number_theory::scalar::power(&z, -1)
                .map_err(FusionError::from)
                .unwrap(),
            z.conjugate()
        );
        assert_eq!(
            tfqm_number_theory::scalar::power(&z, 0)
                .map_err(FusionError::from)
                .unwrap(),
            Cyc8::one()
        );
        assert_eq!(
            tfqm_number_theory::scalar::power(&Cyc8::zero(), -1).map_err(FusionError::from),
            Err(FusionError::Scalar(ScalarError::ZeroInverse))
        );
        assert_eq!(
            tfqm_number_theory::scalar::power(&Cyc8::zero(), 0)
                .map_err(FusionError::from)
                .unwrap(),
            Cyc8::one()
        );
    }
}
