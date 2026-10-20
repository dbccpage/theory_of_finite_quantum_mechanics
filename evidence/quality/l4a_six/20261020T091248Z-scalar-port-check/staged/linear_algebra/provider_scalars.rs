//! Checked admission for scalar types used by existing QM consumers.
//! Provider Gaussian coefficients are public raw transport. Every operation
//! admits both canonical Q components before invoking closed Q(i) arithmetic.
//! No provider scalar trait is used as evidence of admission. AuthorityEffect: None.
use super::ordered::{HermitianOrdered, OrderedExactField};
use super::scalars::{
    CheckedExactField, ExactRing, Field, Involution, Ring, ScalarError, ScalarResult, Semiring,
};
use omega_number_theory::cyclotomic::GaussianRat;

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
