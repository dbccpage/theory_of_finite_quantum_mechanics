
use std::hash::Hash;

use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{matrix as mx, ExactFieldError};
use linear_algebra::scalars::{ExactRing, Field};
use num_rational::BigRational;
use omega_number_theory::cyclotomic::{Cyc12, Cyc24, Cyc5, Cyc8, GaussianRat};
use omega_number_theory::cyclotomic_field::Cyclotomic;
use omega_number_theory::rational::{ri, Rational};

pub trait ComplexField: Field + ExactRing + Hash + Eq {
    fn conjugate(&self) -> Self;
    fn from_rational(r: &BigRational) -> Self;
    fn imaginary_unit() -> Option<Self>;
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
    fn imaginary_unit() -> Option<Self> {
        (N % 4 == 0).then(|| Cyclotomic::zeta(i64::try_from(N / 4).expect("a conductor fits i64")))
    }
    fn inverse_sqrt_two() -> Option<Self> {
        (N % 8 == 0).then(|| {
            let k = i64::try_from(N / 8).expect("a conductor fits i64");
            Cyclotomic::zeta(k)
                .add(&Cyclotomic::zeta(-k))
                .scale(&Rational::new(1.into(), 2.into()))
        })
    }
}

pub fn from_integer<F: ComplexField>(n: i64) -> F {
    F::from_rational(&ri(n))
}

pub fn dagger<F: ComplexField>(m: &BasicMatrix<F>) -> Result<BasicMatrix<F>, ExactFieldError> {
    Ok(BasicMatrix::try_from_fn_result::<_, ExactFieldError>(
        m.cols(),
        m.rows(),
        |r, c| Ok(m.get_ref(c, r)?.conjugate()),
    )?)
}

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

pub fn kronecker_all<F: ComplexField>(
    factors: &[BasicMatrix<F>],
) -> Result<BasicMatrix<F>, ExactFieldError> {
    let mut acc = mx::identity::<F>(1)?;
    for factor in factors {
        acc = mx::kronecker(&acc, factor)?;
    }
    Ok(acc)
}

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
