//! Checked admission for scalar types used by existing QM consumers.
//! Provider Gaussian coefficients are public raw transport. Every operation
//! admits both canonical Q components before invoking closed Q(i) arithmetic.
//! No provider scalar trait is used as evidence of admission. AuthorityEffect: None.
use super::ordered::{HermitianOrdered, OrderedExactField};
use super::scalars::{
    CheckedExactField, ExactRing, Field, Involution, Ring, ScalarError, ScalarResult, Semiring,
};
use engine_number_theory::cyclotomic::GaussianRat;

fn pair(left: &GaussianRat, right: &GaussianRat) -> ScalarResult<()> {
    Semiring::validate(left)?;
    Semiring::validate(right)
}
impl Semiring for GaussianRat {
    fn zero() -> Self {
        GaussianRat::zero()
    }
    fn one() -> Self {
        GaussianRat::one()
    }
    fn validate(&self) -> ScalarResult<()> {
        Semiring::validate(&self.re)?;
        Semiring::validate(&self.im)
    }
    fn try_add(&self, rhs: &Self) -> ScalarResult<Self> {
        pair(self, rhs)?;
        Ok(GaussianRat::add(self, rhs))
    }
    fn try_mul(&self, rhs: &Self) -> ScalarResult<Self> {
        pair(self, rhs)?;
        Ok(GaussianRat::mul(self, rhs))
    }
    fn try_is_zero(&self) -> ScalarResult<bool> {
        Semiring::validate(self)?;
        Ok(GaussianRat::is_zero(self))
    }
}
impl Ring for GaussianRat {
    fn try_neg(&self) -> ScalarResult<Self> {
        Semiring::validate(self)?;
        Ok(GaussianRat::neg(self))
    }
    fn try_sub(&self, rhs: &Self) -> ScalarResult<Self> {
        pair(self, rhs)?;
        Ok(GaussianRat::sub(self, rhs))
    }
}
impl Field for GaussianRat {
    fn try_inv(&self) -> ScalarResult<Self> {
        if Semiring::try_is_zero(self)? {
            return Err(ScalarError::DivisionByZero);
        }
        // Canonical rational a,b with (a,b) != (0,0) have a²+b²>0. Thus the
        // provider's sole zero-norm panic branch is unreachable after admission.
        Ok(GaussianRat::inv(self))
    }
}
impl ExactRing for GaussianRat {}
impl CheckedExactField for GaussianRat {}
impl Involution for GaussianRat {
    fn try_conj(&self) -> ScalarResult<Self> {
        Semiring::validate(self)?;
        Ok(GaussianRat::conj(self))
    }
}
impl HermitianOrdered for GaussianRat {
    fn try_fixed_field_sign(&self) -> ScalarResult<Option<i8>> {
        Semiring::validate(self)?;
        if Semiring::try_is_zero(&self.im)? {
            Ok(Some(OrderedExactField::try_signum(&self.re)?))
        } else {
            Ok(None)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::super::scalars::{q, Q};
    use super::*;
    #[test]
    fn raw_provider_components_are_refused_in_every_role_before_arithmetic() {
        for raw in [
            Q::new_raw(1.into(), 0.into()),
            Q::new_raw(1.into(), (-1).into()),
            Q::new_raw(2.into(), 2.into()),
        ] {
            for bad in [
                GaussianRat {
                    re: raw.clone(),
                    im: q(0),
                },
                GaussianRat {
                    re: q(0),
                    im: raw.clone(),
                },
            ] {
                assert!(bad.try_is_zero().is_err());
                assert!(bad.try_neg().is_err());
                assert!(bad.try_inv().is_err());
                assert!(bad.try_conj().is_err());
                assert!(bad.try_fixed_field_sign().is_err());
                let zero = GaussianRat::zero();
                for (a, b) in [(&bad, &zero), (&zero, &bad)] {
                    assert!(a.try_add(b).is_err());
                    assert!(a.try_sub(b).is_err());
                    assert!(a.try_mul(b).is_err());
                    assert!(a.try_div(b).is_err());
                }
            }
        }
        assert_eq!(
            GaussianRat::zero().try_inv(),
            Err(ScalarError::DivisionByZero)
        );
    }
    #[test]
    fn admitted_provider_gaussians_match_coordinate_oracles_and_matrix_identities() {
        for a in -2..=2 {
            for b in -2..=2 {
                for c in -2..=2 {
                    for d in -2..=2 {
                        let x = GaussianRat::from_ints(a, b);
                        let y = GaussianRat::from_ints(c, d);
                        let product = x.try_mul(&y).unwrap();
                        assert_eq!(product.re, q(a * c - b * d));
                        assert_eq!(product.im, q(a * d + b * c));
                        if a != 0 || b != 0 {
                            assert_eq!(
                                x.try_mul(&x.try_inv().unwrap()).unwrap(),
                                GaussianRat::one()
                            );
                        }
                    }
                }
            }
        }
        let a = super::super::matrix::from_rows(vec![vec![GaussianRat::from_ints(2, 0)]]).unwrap();
        assert!(super::super::ordered::hermitian_is_positive_definite(&a).unwrap());
        let inverse = super::super::elimination::inverse(&a).unwrap();
        assert!(super::super::matrix::is_identity_matrix(
            &super::super::matrix::multiply(&a, &inverse).unwrap()
        )
        .unwrap());
    }
}

// Provider fixed power bases Q[x]/Phi_12 and Q[x]/Phi_24 have canonical Q
// coefficients and irreducible cyclotomic moduli. Their legacy inverse is called
// only after nonzero admission. Provider algorithm correctness, unbounded scalar
// allocations and the nonzero-to-invertible proof remain explicit review duties.
use engine_number_theory::cyclotomic::{Cyc12, Cyc24};
use engine_number_theory::cyclotomic_field::Cyclotomic;
fn admit_coefficients(values: &[super::scalars::Q]) -> ScalarResult<()> {
    for value in values {
        Semiring::validate(value)?;
    }
    Ok(())
}

impl Semiring for Cyc12 {
    fn zero() -> Self {
        Cyc12::zero()
    }
    fn one() -> Self {
        Cyc12::one()
    }
    fn validate(&self) -> ScalarResult<()> {
        admit_coefficients(&self.a)
    }
    fn try_add(&self, rhs: &Self) -> ScalarResult<Self> {
        self.validate()?;
        rhs.validate()?;
        Ok(Cyc12::add(self, rhs))
    }
    fn try_mul(&self, rhs: &Self) -> ScalarResult<Self> {
        self.validate()?;
        rhs.validate()?;
        Ok(Cyc12::mul(self, rhs))
    }
    fn try_is_zero(&self) -> ScalarResult<bool> {
        self.validate()?;
        Ok(Cyc12::is_zero(self))
    }
}
impl Ring for Cyc12 {
    fn try_neg(&self) -> ScalarResult<Self> {
        self.validate()?;
        Ok(Cyc12::neg(self))
    }
    fn try_sub(&self, rhs: &Self) -> ScalarResult<Self> {
        self.validate()?;
        rhs.validate()?;
        Ok(Cyc12::sub(self, rhs))
    }
}
impl Field for Cyc12 {
    fn try_inv(&self) -> ScalarResult<Self> {
        if Semiring::try_is_zero(self)? {
            return Err(ScalarError::DivisionByZero);
        }
        Ok(Cyc12::inv(self))
    }
}
impl ExactRing for Cyc12 {}
impl CheckedExactField for Cyc12 {}
impl Involution for Cyc12 {
    fn try_conj(&self) -> ScalarResult<Self> {
        self.validate()?;
        Ok(Cyc12::conj(self))
    }
}

impl Semiring for Cyc24 {
    fn zero() -> Self {
        Cyc24::zero()
    }
    fn one() -> Self {
        Cyc24::one()
    }
    fn validate(&self) -> ScalarResult<()> {
        admit_coefficients(&self.a)
    }
    fn try_add(&self, rhs: &Self) -> ScalarResult<Self> {
        self.validate()?;
        rhs.validate()?;
        Ok(Cyc24::add(self, rhs))
    }
    fn try_mul(&self, rhs: &Self) -> ScalarResult<Self> {
        self.validate()?;
        rhs.validate()?;
        Ok(Cyc24::mul(self, rhs))
    }
    fn try_is_zero(&self) -> ScalarResult<bool> {
        self.validate()?;
        Ok(Cyc24::is_zero(self))
    }
}
impl Ring for Cyc24 {
    fn try_neg(&self) -> ScalarResult<Self> {
        self.validate()?;
        Ok(Cyc24::neg(self))
    }
    fn try_sub(&self, rhs: &Self) -> ScalarResult<Self> {
        self.validate()?;
        rhs.validate()?;
        Ok(Cyc24::sub(self, rhs))
    }
}
impl Field for Cyc24 {
    fn try_inv(&self) -> ScalarResult<Self> {
        if Semiring::try_is_zero(self)? {
            return Err(ScalarError::DivisionByZero);
        }
        Ok(Cyc24::inv(self))
    }
}
impl ExactRing for Cyc24 {}
impl CheckedExactField for Cyc24 {}
impl Involution for Cyc24 {
    fn try_conj(&self) -> ScalarResult<Self> {
        self.validate()?;
        Ok(Cyc24::conj(self))
    }
}

impl<const N: usize> Semiring for Cyclotomic<N> {
    fn zero() -> Self {
        Cyclotomic::<N>::zero()
    }
    fn one() -> Self {
        Cyclotomic::<N>::one()
    }
    fn validate(&self) -> ScalarResult<()> {
        admit_coefficients(self.coefficients())
    }
    fn try_add(&self, rhs: &Self) -> ScalarResult<Self> {
        self.validate()?;
        rhs.validate()?;
        Ok(Cyclotomic::<N>::add(self, rhs))
    }
    fn try_mul(&self, rhs: &Self) -> ScalarResult<Self> {
        self.validate()?;
        rhs.validate()?;
        Ok(Cyclotomic::<N>::mul(self, rhs))
    }
    fn try_is_zero(&self) -> ScalarResult<bool> {
        self.validate()?;
        Ok(Cyclotomic::<N>::is_zero(self))
    }
}
impl<const N: usize> Ring for Cyclotomic<N> {
    fn try_neg(&self) -> ScalarResult<Self> {
        self.validate()?;
        Ok(Cyclotomic::<N>::neg(self))
    }
    fn try_sub(&self, rhs: &Self) -> ScalarResult<Self> {
        self.validate()?;
        rhs.validate()?;
        Ok(Cyclotomic::<N>::sub(self, rhs))
    }
}
impl<const N: usize> Field for Cyclotomic<N> {
    fn try_inv(&self) -> ScalarResult<Self> {
        if Semiring::try_is_zero(self)? {
            return Err(ScalarError::DivisionByZero);
        }
        Cyclotomic::<N>::inverse(self).ok_or(ScalarError::InversionRefused {
            domain: "Cyclotomic<N>",
        })
    }
}
impl<const N: usize> ExactRing for Cyclotomic<N> {}
impl<const N: usize> CheckedExactField for Cyclotomic<N> {}
impl<const N: usize> Involution for Cyclotomic<N> {
    fn try_conj(&self) -> ScalarResult<Self> {
        self.validate()?;
        Ok(Cyclotomic::<N>::conjugate(self))
    }
}

#[cfg(test)]
mod cyclotomic_challenges {
    use super::super::scalars::{q, Q};
    use super::*;
    fn product_oracle(a: &[i64], b: &[i64]) -> Vec<Q> {
        let n = a.len();
        let mut product = vec![0i128; 2 * n - 1];
        for (i, x) in a.iter().enumerate() {
            for (j, y) in b.iter().enumerate() {
                product[i + j] += i128::from(*x) * i128::from(*y);
            }
        }
        // Both fixed bases have Phi(x)=x^n-x^(n/2)+1.
        for k in (n..product.len()).rev() {
            let coefficient = product[k];
            product[k] = 0;
            product[k - n + n / 2] += coefficient;
            product[k - n] -= coefficient;
        }
        product[..n]
            .iter()
            .map(|value| Q::from_integer((*value).into()))
            .collect()
    }
    fn digits(mut code: usize, n: usize) -> Vec<i64> {
        (0..n)
            .map(|_| {
                let value = (code % 3) as i64 - 1;
                code /= 3;
                value
            })
            .collect()
    }
    fn c12(values: &[i64]) -> Cyc12 {
        Cyc12 {
            a: std::array::from_fn(|i| q(values[i])),
        }
    }
    fn c24(values: &[i64]) -> Cyc24 {
        Cyc24 {
            a: std::array::from_fn(|i| q(values[i])),
        }
    }
    #[test]
    fn fixed_basis_products_match_independent_integer_polynomial_reduction() {
        for a in 0..81 {
            let left = digits(a, 4);
            let x = c12(&left);
            if !x.try_is_zero().unwrap() {
                assert_eq!(x.try_mul(&x.try_inv().unwrap()).unwrap(), Cyc12::one());
            }
            for b in 0..81 {
                let right = digits(b, 4);
                assert_eq!(
                    x.try_mul(&c12(&right)).unwrap().a.as_slice(),
                    product_oracle(&left, &right)
                );
            }
        }
        for a in 0..81 {
            let mut left = digits(a, 8);
            for i in 4..8 {
                left[i] = left[i - 4] * (if i % 2 == 0 { 1 } else { -1 });
            }
            let x = c24(&left);
            if !x.try_is_zero().unwrap() {
                assert_eq!(x.try_mul(&x.try_inv().unwrap()).unwrap(), Cyc24::one());
            }
            for b in 0..16 {
                let mut right = vec![0i64; 8];
                right[b % 8] = if b < 8 { 1 } else { -1 };
                assert_eq!(
                    x.try_mul(&c24(&right)).unwrap().a.as_slice(),
                    product_oracle(&left, &right)
                );
            }
        }
        assert_eq!(
            Cyc12::zeta12(1).try_inv().unwrap().a,
            [q(0), q(1), q(0), q(-1)]
        );
        assert_eq!(
            Cyc24::zeta24(1).try_inv().unwrap().a,
            [q(0), q(0), q(0), q(1), q(0), q(0), q(0), q(-1)]
        );
    }
    fn rejects<F: Field + ExactRing + Involution>(bad: &F, zero: &F) {
        assert!(bad.try_is_zero().is_err());
        assert!(bad.try_neg().is_err());
        assert!(bad.try_inv().is_err());
        assert!(bad.try_conj().is_err());
        for (a, b) in [(bad, zero), (zero, bad)] {
            assert!(a.try_add(b).is_err());
            assert!(a.try_sub(b).is_err());
            assert!(a.try_mul(b).is_err());
            assert!(a.try_div(b).is_err());
        }
    }
    #[test]
    fn every_fixed_coefficient_and_generic_raw_rational_is_admitted_before_queries() {
        for raw in [
            Q::new_raw(1.into(), 0.into()),
            Q::new_raw(1.into(), (-1).into()),
            Q::new_raw(2.into(), 2.into()),
        ] {
            for i in 0..4 {
                let mut bad = Cyc12::zero();
                bad.a[i] = raw.clone();
                rejects(&bad, &Cyc12::zero());
            }
            for i in 0..8 {
                let mut bad = Cyc24::zero();
                bad.a[i] = raw.clone();
                rejects(&bad, &Cyc24::zero());
            }
            rejects(&Cyclotomic::<12>::rational(raw), &Cyclotomic::<12>::zero());
        }
        assert_eq!(Cyc12::zero().try_inv(), Err(ScalarError::DivisionByZero));
        assert_eq!(Cyc24::zero().try_inv(), Err(ScalarError::DivisionByZero));
        assert_eq!(
            Cyclotomic::<12>::zero().try_inv(),
            Err(ScalarError::DivisionByZero)
        );
        let x = Cyclotomic::<12>::zeta(1);
        assert_eq!(
            x.try_mul(&x.try_inv().unwrap()).unwrap(),
            Cyclotomic::<12>::one()
        );
        assert_eq!(
            x.try_inv().unwrap().coefficients(),
            &[q(0), q(1), q(0), q(-1)]
        );
    }
}
