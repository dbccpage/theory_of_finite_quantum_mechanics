
use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::scalars::{ExactRing, Field, Ring, Semiring};
use num_bigint::BigInt;
use num_rational::BigRational;

pub(crate) fn q(n: i64, d: i64) -> BigRational {
    BigRational::new(BigInt::from(n), BigInt::from(d))
}

pub(crate) fn m(rows: &[&[i64]]) -> BasicMatrix<BigRational> {
    let cols = rows.first().map_or(0, |r| r.len());
    let data: Vec<BigRational> = rows
        .iter()
        .flat_map(|r| {
            assert_eq!(r.len(), cols, "test matrix literal must be rectangular");
            r.iter().map(|&x| q(x, 1))
        })
        .collect();
    BasicMatrix::from_row_major(rows.len(), cols, data).expect("rectangular literal")
}


#[derive(Debug, Clone)]
pub(crate) struct Rng(u64);

impl Rng {
    pub(crate) fn new(seed: u64) -> Self {
        Rng(seed)
    }

    pub(crate) fn next_u64(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }

    pub(crate) fn range(&mut self, lo: i64, hi: i64) -> i64 {
        assert!(lo <= hi);
        let span = (hi - lo + 1) as u64;
        lo + (self.next_u64() % span) as i64
    }
}

pub(crate) fn random_matrix(
    rng: &mut Rng,
    rows: usize,
    cols: usize,
    max_abs: i64,
) -> BasicMatrix<BigRational> {
    let data = (0..rows * cols)
        .map(|_| q(rng.range(-max_abs, max_abs), rng.range(1, 4)))
        .collect();
    BasicMatrix::from_row_major(rows, cols, data).expect("generated shape")
}

pub(crate) fn random_integer_matrix(
    rng: &mut Rng,
    rows: usize,
    cols: usize,
    max_abs: i64,
) -> BasicMatrix<BigRational> {
    let data = (0..rows * cols)
        .map(|_| q(rng.range(-max_abs, max_abs), 1))
        .collect();
    BasicMatrix::from_row_major(rows, cols, data).expect("generated shape")
}


#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct Fp<const P: u64>(u64);

impl<const P: u64> Fp<P> {
    pub(crate) fn new(x: i64) -> Self {
        Fp(x.rem_euclid(P as i64) as u64)
    }

    fn pow(self, mut exponent: u64) -> Self {
        let mut base = self;
        let mut acc = Fp(1 % P);
        while exponent > 0 {
            if exponent & 1 == 1 {
                acc = Fp(acc.0 * base.0 % P);
            }
            base = Fp(base.0 * base.0 % P);
            exponent >>= 1;
        }
        acc
    }
}

impl<const P: u64> Semiring for Fp<P> {
    fn zero() -> Self {
        Fp(0)
    }
    fn one() -> Self {
        Fp(1 % P)
    }
    fn add(&self, rhs: &Self) -> Self {
        Fp((self.0 + rhs.0) % P)
    }
    fn mul(&self, rhs: &Self) -> Self {
        Fp(self.0 * rhs.0 % P)
    }
    fn is_zero(&self) -> bool {
        self.0 == 0
    }
}

impl<const P: u64> Ring for Fp<P> {
    fn neg(&self) -> Self {
        Fp((P - self.0) % P)
    }
}

impl<const P: u64> Field for Fp<P> {
    fn try_inv(&self) -> Option<Self> {
        if self.0 == 0 {
            None
        } else {
            Some(self.pow(P - 2))
        }
    }
}

impl<const P: u64> ExactRing for Fp<P> {}

impl<const P: u64> std::ops::Add for Fp<P> {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        Semiring::add(&self, &rhs)
    }
}

impl<const P: u64> std::ops::Sub for Fp<P> {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        Ring::sub(&self, &rhs)
    }
}

impl<const P: u64> std::ops::Mul for Fp<P> {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        Semiring::mul(&self, &rhs)
    }
}

impl<const P: u64> num_traits::Zero for Fp<P> {
    fn zero() -> Self {
        Fp(0)
    }
    fn is_zero(&self) -> bool {
        self.0 == 0
    }
}


#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct Z6(u8);

impl Z6 {
    pub(crate) fn new(x: i64) -> Self {
        Z6(x.rem_euclid(6) as u8)
    }
}

impl Semiring for Z6 {
    fn zero() -> Self {
        Z6(0)
    }
    fn one() -> Self {
        Z6(1)
    }
    fn add(&self, rhs: &Self) -> Self {
        Z6((self.0 + rhs.0) % 6)
    }
    fn mul(&self, rhs: &Self) -> Self {
        Z6(self.0 * rhs.0 % 6)
    }
    fn is_zero(&self) -> bool {
        self.0 == 0
    }
}

impl Ring for Z6 {
    fn neg(&self) -> Self {
        Z6((6 - self.0) % 6)
    }
}

impl Field for Z6 {
    fn try_inv(&self) -> Option<Self> {
        match self.0 {
            1 => Some(Z6(1)),
            5 => Some(Z6(5)),
            _ => None,
        }
    }
}

impl ExactRing for Z6 {}


#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct GaussianRational {
    pub(crate) re: BigRational,
    pub(crate) im: BigRational,
}

pub(crate) fn gi(re: i64, im: i64) -> GaussianRational {
    GaussianRational {
        re: q(re, 1),
        im: q(im, 1),
    }
}

pub(crate) fn gq(re: BigRational, im: BigRational) -> GaussianRational {
    GaussianRational { re, im }
}

impl Semiring for GaussianRational {
    fn zero() -> Self {
        gi(0, 0)
    }
    fn one() -> Self {
        gi(1, 0)
    }
    fn add(&self, rhs: &Self) -> Self {
        gq(&self.re + &rhs.re, &self.im + &rhs.im)
    }
    fn mul(&self, rhs: &Self) -> Self {
        gq(
            &self.re * &rhs.re - &self.im * &rhs.im,
            &self.re * &rhs.im + &self.im * &rhs.re,
        )
    }
    fn is_zero(&self) -> bool {
        num_traits::Zero::is_zero(&self.re) && num_traits::Zero::is_zero(&self.im)
    }
}

impl Ring for GaussianRational {
    fn neg(&self) -> Self {
        gq(-&self.re, -&self.im)
    }
}

impl Field for GaussianRational {
    fn try_inv(&self) -> Option<Self> {
        let norm = &self.re * &self.re + &self.im * &self.im;
        if num_traits::Zero::is_zero(&norm) {
            None
        } else {
            Some(gq(&self.re / &norm, -&self.im / &norm))
        }
    }
}

impl ExactRing for GaussianRational {}

impl std::ops::Add for GaussianRational {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        Semiring::add(&self, &rhs)
    }
}

impl std::ops::Sub for GaussianRational {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        Ring::sub(&self, &rhs)
    }
}

impl std::ops::Mul for GaussianRational {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        Semiring::mul(&self, &rhs)
    }
}

impl num_traits::Zero for GaussianRational {
    fn zero() -> Self {
        gi(0, 0)
    }
    fn is_zero(&self) -> bool {
        Semiring::is_zero(self)
    }
}

impl crate::linear_algebra::involution::Involution for GaussianRational {
    fn conjugate(&self) -> Self {
        gq(self.re.clone(), -&self.im)
    }
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct QSqrt2 {
    pub(crate) a: BigRational,
    pub(crate) b: BigRational,
}

pub(crate) fn qs(a: BigRational, b: BigRational) -> QSqrt2 {
    QSqrt2 { a, b }
}

pub(crate) fn qsi(a: i64, b: i64) -> QSqrt2 {
    qs(q(a, 1), q(b, 1))
}

pub(crate) fn sign_of_rational(x: &BigRational) -> i8 {
    match x.numer().sign() {
        num_bigint::Sign::Minus => -1,
        num_bigint::Sign::NoSign => 0,
        num_bigint::Sign::Plus => 1,
    }
}

impl QSqrt2 {
    pub(crate) fn real_sign(&self) -> i8 {
        let (sa, sb) = (sign_of_rational(&self.a), sign_of_rational(&self.b));
        if sa == 0 {
            return sb;
        }
        if sb == 0 || sa == sb {
            return sa;
        }
        let a_squared = &self.a * &self.a;
        let two_b_squared = q(2, 1) * &self.b * &self.b;
        if a_squared > two_b_squared {
            sa
        } else {
            sb
        }
    }
}

impl Semiring for QSqrt2 {
    fn zero() -> Self {
        qsi(0, 0)
    }
    fn one() -> Self {
        qsi(1, 0)
    }
    fn add(&self, rhs: &Self) -> Self {
        qs(&self.a + &rhs.a, &self.b + &rhs.b)
    }
    fn mul(&self, rhs: &Self) -> Self {
        qs(
            &self.a * &rhs.a + q(2, 1) * &self.b * &rhs.b,
            &self.a * &rhs.b + &self.b * &rhs.a,
        )
    }
    fn is_zero(&self) -> bool {
        num_traits::Zero::is_zero(&self.a) && num_traits::Zero::is_zero(&self.b)
    }
}

impl Ring for QSqrt2 {
    fn neg(&self) -> Self {
        qs(-&self.a, -&self.b)
    }
}

impl Field for QSqrt2 {
    fn try_inv(&self) -> Option<Self> {
        let norm = &self.a * &self.a - q(2, 1) * &self.b * &self.b;
        if num_traits::Zero::is_zero(&norm) {
            None
        } else {
            Some(qs(&self.a / &norm, -&self.b / &norm))
        }
    }
}

impl ExactRing for QSqrt2 {}

impl std::ops::Add for QSqrt2 {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        Semiring::add(&self, &rhs)
    }
}

impl std::ops::Sub for QSqrt2 {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        Ring::sub(&self, &rhs)
    }
}

impl std::ops::Mul for QSqrt2 {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        Semiring::mul(&self, &rhs)
    }
}

impl num_traits::Zero for QSqrt2 {
    fn zero() -> Self {
        qsi(0, 0)
    }
    fn is_zero(&self) -> bool {
        Semiring::is_zero(self)
    }
}

impl crate::linear_algebra::involution::Involution for QSqrt2 {
    fn conjugate(&self) -> Self {
        self.clone()
    }
}

impl<const P: u64> crate::linear_algebra::involution::Involution for Fp<P> {
    fn conjugate(&self) -> Self {
        *self
    }
}

impl crate::linear_algebra::ordered::OrderedExactField for QSqrt2 {
    fn signum(&self) -> i8 {
        self.real_sign()
    }
}

impl crate::linear_algebra::ordered::HermitianOrdered for GaussianRational {
    fn fixed_field_sign(&self) -> Option<i8> {
        if num_traits::Zero::is_zero(&self.im) {
            Some(sign_of_rational(&self.re))
        } else {
            None
        }
    }
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Shaky<const MODE: u8>(pub(crate) BigRational);

impl<const MODE: u8> Semiring for Shaky<MODE> {
    fn zero() -> Self {
        Shaky(q(0, 1))
    }
    fn one() -> Self {
        Shaky(q(1, 1))
    }
    fn add(&self, rhs: &Self) -> Self {
        Shaky(&self.0 + &rhs.0)
    }
    fn mul(&self, rhs: &Self) -> Self {
        Shaky(&self.0 * &rhs.0)
    }
    fn is_zero(&self) -> bool {
        num_traits::Zero::is_zero(&self.0)
    }
}

impl<const MODE: u8> Ring for Shaky<MODE> {
    fn neg(&self) -> Self {
        Shaky(-&self.0)
    }
}

impl<const MODE: u8> Field for Shaky<MODE> {
    fn try_inv(&self) -> Option<Self> {
        if num_traits::Zero::is_zero(&self.0) {
            None
        } else if MODE == 8 {
            Some(self.clone())
        } else {
            Some(Shaky(self.0.recip()))
        }
    }
}

impl<const MODE: u8> ExactRing for Shaky<MODE> {}

impl<const MODE: u8> crate::linear_algebra::involution::Involution for Shaky<MODE> {
    fn conjugate(&self) -> Self {
        match MODE {
            3 => Shaky(&self.0 + q(1, 1)),
            4 => Shaky(-&self.0),
            _ => self.clone(),
        }
    }
}

impl<const MODE: u8> crate::linear_algebra::ordered::OrderedExactField for Shaky<MODE> {
    fn signum(&self) -> i8 {
        let sign = sign_of_rational(&self.0);
        match (MODE, sign) {
            (1, 1) => 2,
            (2, 1) => 0,
            (7, 1) => -1,
            _ => sign,
        }
    }
}

impl<const MODE: u8> crate::linear_algebra::ordered::HermitianOrdered for Shaky<MODE> {
    fn fixed_field_sign(&self) -> Option<i8> {
        let sign = sign_of_rational(&self.0);
        match (MODE, sign) {
            (5, 1) => None,
            (6, 1) => Some(2),
            _ => Some(sign),
        }
    }
}

impl crate::linear_algebra::ordered::HermitianOrdered for QSqrt2 {
    fn fixed_field_sign(&self) -> Option<i8> {
        Some(self.real_sign())
    }
}
