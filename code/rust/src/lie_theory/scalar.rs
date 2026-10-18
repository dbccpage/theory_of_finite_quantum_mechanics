//! Exact scalars with a complex conjugation, for unitary and Hermitian constructions.
//!
//! A [`ComplexField`] is an exact field of the `linear_algebra::scalars` tower that is a
//! subfield of `C` closed under complex conjugation, together with the few constants that
//! the constructions of this crate need: the embedding of `Q`, and `i` and `1/sqrt 2` when
//! the field contains them. The implementations are for the fields of
//! `omega_number_theory`: `Q`, `Q(i)`, `Q(zeta_5)`, `Q(zeta_8)`, `Q(zeta_12)`,
//! `Q(zeta_24)` and `Q(zeta_N)` for any compile-time conductor `N`.
//!
//! The adjoint, Hermitian and unitary predicates are here as well; they refuse non-square
//! input with a typed error instead of answering "no".
//!
//! AuthorityEffect: None.

use std::hash::Hash;

use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{matrix as mx, ExactFieldError};
use linear_algebra::scalars::{ExactRing, Field};
use num_rational::BigRational;
use omega_number_theory::cyclotomic::{Cyc12, Cyc24, Cyc5, Cyc8, GaussianRat};
use omega_number_theory::cyclotomic_field::Cyclotomic;
use omega_number_theory::rational::{ri, Rational};

/// An exact subfield of `C` closed under complex conjugation.
pub trait ComplexField: Field + ExactRing + Hash + Eq {
    /// The complex conjugate.
    fn conjugate(&self) -> Self;
    /// The rational `r` as an element of the field.
    fn from_rational(r: &BigRational) -> Self;
    /// `i`, when the field contains it.
    fn imaginary_unit() -> Option<Self>;
    /// `1 / sqrt 2`, when the field contains it.
    fn inverse_sqrt_two() -> Option<Self>;
}

impl ComplexField for BigRational {
    fn conjugate(&self) -> Self {
        self.clone()
    }
    fn from_rational(r: &BigRational) -> Self {
        r.clone()
    }
    fn imaginary_unit() -> Option<Self> {
        None
    }
    fn inverse_sqrt_two() -> Option<Self> {
        None
    }
}

impl ComplexField for GaussianRat {
    fn conjugate(&self) -> Self {
        self.conj()
    }
    fn from_rational(r: &BigRational) -> Self {
        GaussianRat::from_rational(r.clone())
    }
    fn imaginary_unit() -> Option<Self> {
        Some(GaussianRat::i())
    }
    fn inverse_sqrt_two() -> Option<Self> {
        None
    }
}

impl ComplexField for Cyc5 {
    fn conjugate(&self) -> Self {
        self.conj()
    }
    fn from_rational(r: &BigRational) -> Self {
        Cyc5::rat(r.clone())
    }
    fn imaginary_unit() -> Option<Self> {
        None
    }
    fn inverse_sqrt_two() -> Option<Self> {
        None
    }
}

impl ComplexField for Cyc8 {
    fn conjugate(&self) -> Self {
        self.conj()
    }
    fn from_rational(r: &BigRational) -> Self {
        let mut c = Cyc8::zero();
        c.a[0] = r.clone();
        c
    }
    fn imaginary_unit() -> Option<Self> {
        Some(Cyc8::i())
    }
    fn inverse_sqrt_two() -> Option<Self> {
        Some(Cyc8::inv_sqrt2())
    }
}

impl ComplexField for Cyc12 {
    fn conjugate(&self) -> Self {
        self.conj()
    }
    fn from_rational(r: &BigRational) -> Self {
        let mut c = Cyc12::zero();
        c.a[0] = r.clone();
        c
    }
    fn imaginary_unit() -> Option<Self> {
        Some(Cyc12::i())
    }
    fn inverse_sqrt_two() -> Option<Self> {
        None
    }
}

impl ComplexField for Cyc24 {
    fn conjugate(&self) -> Self {
        self.conj()
    }
    fn from_rational(r: &BigRational) -> Self {
        Cyc24::rat(r.clone())
    }
    fn imaginary_unit() -> Option<Self> {
        Some(Cyc24::i())
    }
    fn inverse_sqrt_two() -> Option<Self> {
        Some(Cyc24::inv_sqrt2())
    }
}

impl<const N: usize> ComplexField for Cyclotomic<N> {
    fn conjugate(&self) -> Self {
        Cyclotomic::conjugate(self)
    }
    fn from_rational(r: &BigRational) -> Self {
        Cyclotomic::rational(r.clone())
    }
    /// `i = zeta_N^(N/4)` when `4 | N`.
    fn imaginary_unit() -> Option<Self> {
        (N % 4 == 0).then(|| Cyclotomic::zeta(i64::try_from(N / 4).expect("a conductor fits i64")))
    }
    /// `1/sqrt 2 = (zeta_8 + zeta_8^-1) / 2` when `8 | N`.
    fn inverse_sqrt_two() -> Option<Self> {
        (N % 8 == 0).then(|| {
            let k = i64::try_from(N / 8).expect("a conductor fits i64");
            Cyclotomic::zeta(k)
                .add(&Cyclotomic::zeta(-k))
                .scale(&Rational::new(1.into(), 2.into()))
        })
    }
}

/// The integer `n` as a field element.
pub fn from_integer<F: ComplexField>(n: i64) -> F {
    F::from_rational(&ri(n))
}

/// The adjoint `A† = conj(A)^T`.
pub fn dagger<F: ComplexField>(m: &BasicMatrix<F>) -> Result<BasicMatrix<F>, ExactFieldError> {
    Ok(BasicMatrix::try_from_fn_result::<_, ExactFieldError>(
        m.cols(),
        m.rows(),
        |r, c| Ok(m.get_ref(c, r)?.conjugate()),
    )?)
}

/// `A = A†`; a non-square matrix is refused.
pub fn is_hermitian<F: ComplexField>(m: &BasicMatrix<F>) -> Result<bool, ExactFieldError> {
    if m.rows() != m.cols() {
        return Err(ExactFieldError::NotSquare {
            operation: "is_hermitian",
            rows: m.rows(),
            cols: m.cols(),
        });
    }
    Ok(dagger(m)? == *m)
}

/// `A† A = I`; a non-square matrix is refused.
pub fn is_unitary<F: ComplexField>(m: &BasicMatrix<F>) -> Result<bool, ExactFieldError> {
    if m.rows() != m.cols() {
        return Err(ExactFieldError::NotSquare {
            operation: "is_unitary",
            rows: m.rows(),
            cols: m.cols(),
        });
    }
    mx::is_identity_matrix(&mx::multiply(&dagger(m)?, m)?)
}

/// The Kronecker product of a list of matrices, left to right (the empty list is the `1 x 1` identity).
pub fn kronecker_all<F: ComplexField>(
    factors: &[BasicMatrix<F>],
) -> Result<BasicMatrix<F>, ExactFieldError> {
    let mut acc = mx::identity::<F>(1)?;
    for factor in factors {
        acc = mx::kronecker(&acc, factor)?;
    }
    Ok(acc)
}

/// A bounded root-order query. None means the declared bound was insufficient;
/// use cyclotomic_root_order for a field-wide infinite-order decision.
pub fn multiplicative_order<
    T: linear_algebra::scalars::Field + linear_algebra::scalars::ExactRing,
>(
    z: &T,
    bound: usize,
) -> Option<usize> {
    if bound > 1_000_000 {
        return None;
    }
    let mut power = T::one();
    for n in 1..=bound {
        power = power.mul(z);
        if power == T::one() {
            return Some(n);
        }
    }
    None
}

/// Every root of unity in Q(zeta_N) has order dividing lcm(N,2).
/// This finite field-wide bound therefore distinguishes finite from infinite order.
pub fn cyclotomic_root_order<const N: usize>(z: &Cyclotomic<N>) -> Option<usize> {
    let bound = if N % 2 == 0 { N } else { N.checked_mul(2)? };
    let mut power = Cyclotomic::<N>::one();
    for n in 1..=bound {
        power = power.mul(z);
        if power == Cyclotomic::<N>::one() {
            return Some(n);
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_number_theory::rational::rq;

    fn check_field<F: ComplexField + std::fmt::Debug>() {
        // Conjugation is an involutive ring automorphism on a sample built from the field's constants.
        let half = F::from_rational(&rq(1, 2));
        let third = F::from_rational(&rq(-1, 3));
        let mut sample = vec![half, third, from_integer::<F>(2)];
        if let Some(i) = F::imaginary_unit() {
            sample.push(i.clone());
            sample.push(i.mul(&from_integer::<F>(3)).add(&from_integer::<F>(1)));
        }
        if let Some(s) = F::inverse_sqrt_two() {
            sample.push(s);
        }
        for a in &sample {
            assert_eq!(a.conjugate().conjugate(), *a, "conj is an involution");
            for b in &sample {
                assert_eq!(
                    a.mul(b).conjugate(),
                    a.conjugate().mul(&b.conjugate()),
                    "conj is multiplicative"
                );
                assert_eq!(
                    a.add(b).conjugate(),
                    a.conjugate().add(&b.conjugate()),
                    "conj is additive"
                );
            }
        }
        if let Some(i) = F::imaginary_unit() {
            assert_eq!(i.mul(&i), from_integer::<F>(-1), "i squares to -1");
            assert_eq!(i.conjugate(), i.neg());
        }
        if let Some(s) = F::inverse_sqrt_two() {
            assert_eq!(s.mul(&s), F::from_rational(&rq(1, 2)), "(1/sqrt 2)^2 = 1/2");
            assert_eq!(s.conjugate(), s, "1/sqrt 2 is real");
        }
    }

    #[test]
    fn every_field_satisfies_the_conjugation_axioms_and_its_constants() {
        check_field::<BigRational>();
        check_field::<GaussianRat>();
        check_field::<Cyc5>();
        check_field::<Cyc8>();
        check_field::<Cyc12>();
        check_field::<Cyc24>();
        check_field::<Cyclotomic<8>>();
        check_field::<Cyclotomic<16>>();
        check_field::<Cyclotomic<7>>();
    }

    #[test]
    fn the_constants_exist_exactly_when_the_field_contains_them() {
        assert!(BigRational::imaginary_unit().is_none() && GaussianRat::imaginary_unit().is_some());
        assert!(Cyc5::imaginary_unit().is_none());
        assert!(Cyc12::inverse_sqrt_two().is_none() && Cyc8::inverse_sqrt_two().is_some());
        assert!(Cyclotomic::<7>::imaginary_unit().is_none());
        assert!(
            Cyclotomic::<12>::imaginary_unit().is_some()
                && Cyclotomic::<12>::inverse_sqrt_two().is_none()
        );
        assert!(Cyclotomic::<24>::inverse_sqrt_two().is_some());
    }
}
