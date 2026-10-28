
use std::cmp::Ordering;
use std::fmt;

use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Deserializer, Serialize, Serializer};

use crate::rational::{r_one, r_zero, ri, sqrt_exact, squarefree_part, ArithmeticError, Rational};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum QuadraticError {
    #[error("an enclosure needs a strictly positive width")]
    NonPositiveWidth,
    #[error("quadratic enclosure exceeds the 16384-bit input or precision budget")]
    EnclosureBudget,
    #[error("the radicand 0 does not define a quadratic field")]
    ZeroRadicand,
    #[error(
        "the radicand {radicand} is not squarefree: it is {squarefree} * {root}^2 with root > 1"
    )]
    RadicandNotSquarefree {
        radicand: BigInt,
        squarefree: BigInt,
        root: BigInt,
    },
    #[error("a real surd needs a nonnegative radicand, got {0}")]
    NegativeRadicand(Rational),
    #[error(
        "the operands lie in different quadratic fields, Q(sqrt({left})) and Q(sqrt({right}))"
    )]
    RadicandMismatch { left: BigInt, right: BigInt },
    #[error("c1 sqrt({left}) + c2 sqrt({right}) with different radicands is not a single surd")]
    SurdSumNotSingle { left: BigInt, right: BigInt },
    #[error("Q(sqrt({0})) is not a real field, so its elements have no order")]
    NotReal(BigInt),
    #[error("division by zero")]
    DivisionByZero,
    #[error(transparent)]
    Arithmetic(#[from] ArithmeticError),
}

pub const fn is_valid_radicand(d: i64) -> bool {
    if d == 0 || d == 1 {
        return false;
    }
    let magnitude = d.unsigned_abs();
    let mut p: u64 = 2;
    while p <= magnitude / p {
        if magnitude % (p * p) == 0 {
            return false;
        }
        p += 1;
    }
    true
}

fn half() -> Rational {
    Rational::new(BigInt::one(), BigInt::from(2))
}

fn check_radicand(d: &BigInt) -> Result<(), QuadraticError> {
    if d.is_zero() {
        return Err(QuadraticError::ZeroRadicand);
    }
    let (squarefree, root) = squarefree_part(d)?;
    if !root.is_one() {
        return Err(QuadraticError::RadicandNotSquarefree {
            radicand: d.clone(),
            squarefree,
            root,
        });
    }
    Ok(())
}

fn real_sign(a: &Rational, b: &Rational, d: &Rational) -> Ordering {
    let zero = r_zero();
    match (a.cmp(&zero), b.cmp(&zero)) {
        (Ordering::Equal, Ordering::Equal) => Ordering::Equal,
        (Ordering::Greater, Ordering::Greater)
        | (Ordering::Greater, Ordering::Equal)
        | (Ordering::Equal, Ordering::Greater) => Ordering::Greater,
        (Ordering::Less, Ordering::Less)
        | (Ordering::Less, Ordering::Equal)
        | (Ordering::Equal, Ordering::Less) => Ordering::Less,
        (Ordering::Greater, Ordering::Less) => (a * a).cmp(&(d * b * b)),
        (Ordering::Less, Ordering::Greater) => (d * b * b).cmp(&(a * a)),
    }
}


#[derive(Clone, Copy, PartialEq, Eq, Hash)]
struct Radicand<const D: i64>;

impl<const D: i64> Radicand<D> {
    const VALID: () = assert!(
        is_valid_radicand(D),
        "Quadratic<D> needs a squarefree radicand D other than 0 and 1"
    );

    const fn checked() -> Self {
        let () = Self::VALID;
        Radicand
    }
}

#[derive(Clone, PartialEq, Eq, Hash)]
pub struct Quadratic<const D: i64> {
    pub a: Rational,
    pub b: Rational,
    radicand: Radicand<D>,
}

impl<const D: i64> fmt::Debug for Quadratic<D> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}) + ({})*sqrt({})", self.a, self.b, D)
    }
}

impl<const D: i64> fmt::Display for Quadratic<D> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} + {}*sqrt({})", self.a, self.b, D)
    }
}

#[derive(Serialize, Deserialize)]
struct QuadraticWire {
    a: Rational,
    b: Rational,
}

impl<const D: i64> Serialize for Quadratic<D> {
    fn serialize<S: Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        QuadraticWire {
            a: self.a.clone(),
            b: self.b.clone(),
        }
        .serialize(serializer)
    }
}

impl<'de, const D: i64> Deserialize<'de> for Quadratic<D> {
    fn deserialize<De: Deserializer<'de>>(deserializer: De) -> Result<Self, De::Error> {
        let wire = QuadraticWire::deserialize(deserializer)?;
        Ok(Self::new(wire.a, wire.b))
    }
}

impl<const D: i64> Quadratic<D> {
    pub const RADICAND: i64 = D;

    pub fn new(a: Rational, b: Rational) -> Self {
        Self {
            a,
            b,
            radicand: Radicand::<D>::checked(),
        }
    }

    pub fn from_rational(a: Rational) -> Self {
        Self::new(a, r_zero())
    }

    pub fn from_ints(a: i64, b: i64) -> Self {
        Self::new(ri(a), ri(b))
    }

    pub fn zero() -> Self {
        Self::new(r_zero(), r_zero())
    }

    pub fn one() -> Self {
        Self::new(r_one(), r_zero())
    }

    pub fn sqrt_d() -> Self {
        Self::new(r_zero(), r_one())
    }

    pub fn is_zero(&self) -> bool {
        self.a.is_zero() && self.b.is_zero()
    }

    pub fn is_rational(&self) -> bool {
        self.b.is_zero()
    }

    pub fn add(&self, other: &Self) -> Self {
        Self::new(&self.a + &other.a, &self.b + &other.b)
    }

    pub fn sub(&self, other: &Self) -> Self {
        Self::new(&self.a - &other.a, &self.b - &other.b)
    }

    pub fn neg(&self) -> Self {
        Self::new(-&self.a, -&self.b)
    }

    pub fn mul(&self, other: &Self) -> Self {
        let d = ri(D);
        Self::new(
            &self.a * &other.a + &d * &self.b * &other.b,
            &self.a * &other.b + &self.b * &other.a,
        )
    }

    pub fn scale(&self, c: &Rational) -> Self {
        Self::new(&self.a * c, &self.b * c)
    }

    pub fn conjugate(&self) -> Self {
        Self::new(self.a.clone(), -&self.b)
    }

    pub fn norm(&self) -> Rational {
        &self.a * &self.a - ri(D) * &self.b * &self.b
    }

    pub fn trace(&self) -> Rational {
        &self.a + &self.a
    }

    pub fn inverse(&self) -> Option<Self> {
        let norm = self.norm();
        if norm.is_zero() {
            return None;
        }
        Some(Self::new(&self.a / &norm, -&self.b / &norm))
    }

    pub fn checked_div(&self, other: &Self) -> Option<Self> {
        Some(self.mul(&other.inverse()?))
    }

    pub fn pow(&self, n: u32) -> Self {
        let mut result = Self::one();
        let mut base = self.clone();
        let mut n = n;
        while n > 0 {
            if n & 1 == 1 {
                result = result.mul(&base);
            }
            n >>= 1;
            if n > 0 {
                base = base.mul(&base);
            }
        }
        result
    }

    pub fn sqrt(&self) -> Option<Self> {
        let number = self.to_number();
        let root = number.sqrt_in(&BigInt::from(D)).ok()??;
        Self::from_number(&root)
    }

    pub fn to_number(&self) -> QuadraticNumber {
        QuadraticNumber::normalised(BigInt::from(D), self.a.clone(), self.b.clone())
    }

    pub fn from_number(n: &QuadraticNumber) -> Option<Self> {
        if n.b.is_zero() {
            Some(Self::from_rational(n.a.clone()))
        } else if n.radicand == BigInt::from(D) {
            Some(Self::new(n.a.clone(), n.b.clone()))
        } else {
            None
        }
    }

    const REAL: () = assert!(
        D > 0,
        "the sign and order of Quadratic<D> need a real quadratic field, D > 0"
    );

    pub fn sign(&self) -> Ordering {
        let () = Self::REAL;
        real_sign(&self.a, &self.b, &ri(D))
    }

    pub fn is_positive(&self) -> bool {
        self.sign() == Ordering::Greater
    }

    pub fn is_negative(&self) -> bool {
        self.sign() == Ordering::Less
    }

    pub fn is_nonnegative(&self) -> bool {
        self.sign() != Ordering::Less
    }
}

impl Quadratic<5> {
    pub fn golden_ratio() -> Self {
        Self::new(half(), half())
    }

    pub fn golden_ratio_conjugate() -> Self {
        Self::new(half(), -half())
    }
}

impl Quadratic<2> {
    pub fn silver_ratio() -> Self {
        Self::new(r_one(), r_one())
    }
}

impl<const D: i64> Ord for Quadratic<D> {
    fn cmp(&self, other: &Self) -> Ordering {
        self.sub(other).sign()
    }
}

impl<const D: i64> PartialOrd for Quadratic<D> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl<const D: i64> std::ops::Add for Quadratic<D> {
    type Output = Quadratic<D>;
    fn add(self, rhs: Quadratic<D>) -> Quadratic<D> {
        Quadratic::add(&self, &rhs)
    }
}
impl<'a, 'b, const D: i64> std::ops::Add<&'b Quadratic<D>> for &'a Quadratic<D> {
    type Output = Quadratic<D>;
    fn add(self, rhs: &'b Quadratic<D>) -> Quadratic<D> {
        Quadratic::add(self, rhs)
    }
}
impl<const D: i64> std::ops::Sub for Quadratic<D> {
    type Output = Quadratic<D>;
    fn sub(self, rhs: Quadratic<D>) -> Quadratic<D> {
        Quadratic::sub(&self, &rhs)
    }
}
impl<'a, 'b, const D: i64> std::ops::Sub<&'b Quadratic<D>> for &'a Quadratic<D> {
    type Output = Quadratic<D>;
    fn sub(self, rhs: &'b Quadratic<D>) -> Quadratic<D> {
        Quadratic::sub(self, rhs)
    }
}
impl<const D: i64> std::ops::Mul for Quadratic<D> {
    type Output = Quadratic<D>;
    fn mul(self, rhs: Quadratic<D>) -> Quadratic<D> {
        Quadratic::mul(&self, &rhs)
    }
}
impl<'a, 'b, const D: i64> std::ops::Mul<&'b Quadratic<D>> for &'a Quadratic<D> {
    type Output = Quadratic<D>;
    fn mul(self, rhs: &'b Quadratic<D>) -> Quadratic<D> {
        Quadratic::mul(self, rhs)
    }
}
impl<const D: i64> std::ops::Neg for Quadratic<D> {
    type Output = Quadratic<D>;
    fn neg(self) -> Quadratic<D> {
        Quadratic::neg(&self)
    }
}
impl<'a, const D: i64> std::ops::Neg for &'a Quadratic<D> {
    type Output = Quadratic<D>;
    fn neg(self) -> Quadratic<D> {
        Quadratic::neg(self)
    }
}

impl<const D: i64> Zero for Quadratic<D> {
    fn zero() -> Self {
        Quadratic::new(r_zero(), r_zero())
    }
    fn is_zero(&self) -> bool {
        self.a.is_zero() && self.b.is_zero()
    }
}

impl<const D: i64> One for Quadratic<D> {
    fn one() -> Self {
        Quadratic::new(r_one(), r_zero())
    }
}

impl<const D: i64> linear_algebra::scalars::Semiring for Quadratic<D> {
    fn zero() -> Self {
        Quadratic::new(r_zero(), r_zero())
    }
    fn one() -> Self {
        Quadratic::new(r_one(), r_zero())
    }
    fn add(&self, rhs: &Self) -> Self {
        Quadratic::add(self, rhs)
    }
    fn mul(&self, rhs: &Self) -> Self {
        Quadratic::mul(self, rhs)
    }
    fn is_zero(&self) -> bool {
        Quadratic::is_zero(self)
    }
}

impl<const D: i64> linear_algebra::scalars::Ring for Quadratic<D> {
    fn neg(&self) -> Self {
        Quadratic::neg(self)
    }
}

impl<const D: i64> linear_algebra::scalars::Field for Quadratic<D> {
    fn try_inv(&self) -> Option<Self> {
        self.inverse()
    }
}

impl<const D: i64> linear_algebra::scalars::ExactRing for Quadratic<D> {}

impl<const D: i64> linear_algebra::exact_field::involution::Involution for Quadratic<D> {
    fn conjugate(&self) -> Self {
        if D > 0 {
            self.clone()
        } else {
            Quadratic::conjugate(self)
        }
    }
}

impl<const D: i64> linear_algebra::exact_field::ordered::HermitianOrdered for Quadratic<D> {
    fn fixed_field_sign(&self) -> Option<i8> {
        if D > 0 {
            Some(match real_sign(&self.a, &self.b, &ri(D)) {
                Ordering::Less => -1,
                Ordering::Equal => 0,
                Ordering::Greater => 1,
            })
        } else if self.b.is_zero() {
            Some(linear_algebra::exact_field::ordered::OrderedExactField::signum(&self.a))
        } else {
            None
        }
    }
}


#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub struct Surd {
    coefficient: Rational,
    radicand: BigInt,
}

impl Surd {
    pub fn zero() -> Self {
        Self {
            coefficient: r_zero(),
            radicand: BigInt::one(),
        }
    }

    pub fn one() -> Self {
        Self::rational(r_one())
    }

    pub fn rational(value: Rational) -> Self {
        if value.is_zero() {
            Self::zero()
        } else {
            Self {
                coefficient: value,
                radicand: BigInt::one(),
            }
        }
    }

    pub fn new(coefficient: Rational, square: &Rational) -> Result<Self, QuadraticError> {
        let square = square.reduced();
        if square.is_negative() {
            return Err(QuadraticError::NegativeRadicand(square));
        }
        Self::from_fraction(coefficient, square.numer(), square.denom())
    }

    pub fn from_natural(coefficient: Rational, m: &BigInt) -> Result<Self, QuadraticError> {
        if m.is_negative() {
            return Err(QuadraticError::NegativeRadicand(Rational::from_integer(
                m.clone(),
            )));
        }
        Self::from_fraction(coefficient, m, &BigInt::one())
    }

    fn from_fraction(
        coefficient: Rational,
        p: &BigInt,
        q: &BigInt,
    ) -> Result<Self, QuadraticError> {
        if coefficient.is_zero() || p.is_zero() {
            return Ok(Self::zero());
        }
        let (radicand, root) = squarefree_part(&(p * q))?;
        Ok(Self {
            coefficient: coefficient * Rational::new(root, q.clone()),
            radicand,
        })
    }

    pub fn coefficient(&self) -> &Rational {
        &self.coefficient
    }

    pub fn radicand(&self) -> &BigInt {
        &self.radicand
    }

    pub fn is_zero(&self) -> bool {
        self.coefficient.is_zero()
    }

    pub fn is_rational(&self) -> bool {
        self.radicand.is_one()
    }

    pub fn neg(&self) -> Self {
        Self {
            coefficient: -&self.coefficient,
            radicand: self.radicand.clone(),
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        if self.is_zero() || other.is_zero() {
            return Self::zero();
        }
        let g = num_integer::Integer::gcd(&self.radicand, &other.radicand);
        Self {
            coefficient: &self.coefficient * &other.coefficient * Rational::from_integer(g.clone()),
            radicand: (&self.radicand / &g) * (&other.radicand / &g),
        }
    }

    pub fn inverse(&self) -> Option<Self> {
        if self.is_zero() {
            return None;
        }
        Some(Self {
            coefficient: (&self.coefficient * Rational::from_integer(self.radicand.clone()))
                .recip(),
            radicand: self.radicand.clone(),
        })
    }

    pub fn checked_div(&self, other: &Self) -> Result<Self, QuadraticError> {
        let inverse = other.inverse().ok_or(QuadraticError::DivisionByZero)?;
        Ok(self.mul(&inverse))
    }

    pub fn square(&self) -> Rational {
        &self.coefficient * &self.coefficient * Rational::from_integer(self.radicand.clone())
    }

    pub fn checked_add(&self, other: &Self) -> Result<Self, QuadraticError> {
        if self.is_zero() {
            return Ok(other.clone());
        }
        if other.is_zero() {
            return Ok(self.clone());
        }
        if self.radicand != other.radicand {
            return Err(QuadraticError::SurdSumNotSingle {
                left: self.radicand.clone(),
                right: other.radicand.clone(),
            });
        }
        let sum = &self.coefficient + &other.coefficient;
        if sum.is_zero() {
            return Ok(Self::zero());
        }
        Ok(Self {
            coefficient: sum,
            radicand: self.radicand.clone(),
        })
    }

    pub fn checked_sub(&self, other: &Self) -> Result<Self, QuadraticError> {
        self.checked_add(&other.neg())
    }

    pub fn sign(&self) -> Ordering {
        self.coefficient.cmp(&r_zero())
    }

    pub fn to_number(&self) -> QuadraticNumber {
        QuadraticNumber::normalised(self.radicand.clone(), r_zero(), self.coefficient.clone())
    }
}

impl Ord for Surd {
    fn cmp(&self, other: &Self) -> Ordering {
        let (left, right) = (self.sign(), other.sign());
        if left != right {
            return left.cmp(&right);
        }
        match left {
            Ordering::Equal => Ordering::Equal,
            Ordering::Greater => self.square().cmp(&other.square()),
            Ordering::Less => other.square().cmp(&self.square()),
        }
    }
}

impl PartialOrd for Surd {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl fmt::Display for Surd {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}*sqrt({})", self.coefficient, self.radicand)
    }
}


#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub struct QuadraticNumber {
    radicand: BigInt,
    a: Rational,
    b: Rational,
}

impl QuadraticNumber {
    fn normalised(radicand: BigInt, a: Rational, b: Rational) -> Self {
        if b.is_zero() || radicand.is_one() {
            let a = if radicand.is_one() { a + b } else { a };
            return Self {
                radicand: BigInt::one(),
                a,
                b: r_zero(),
            };
        }
        Self { radicand, a, b }
    }

    pub fn new(radicand: BigInt, a: Rational, b: Rational) -> Result<Self, QuadraticError> {
        check_radicand(&radicand)?;
        Ok(Self::normalised(radicand, a, b))
    }

    pub fn from_rational(a: Rational) -> Self {
        Self::normalised(BigInt::one(), a, r_zero())
    }

    pub fn rational_part(&self) -> &Rational {
        &self.a
    }

    pub fn sqrt_part(&self) -> &Rational {
        &self.b
    }

    pub fn minimal_polynomial(&self) -> Vec<BigInt> {
        let coefficients = if self.is_rational() {
            vec![-self.a.clone(), r_one()]
        } else {
            vec![self.norm(), -(&self.a + &self.a), r_one()]
        };
        crate::polynomial::Polynomial::from_coefficients(coefficients)
            .content_and_primitive_part()
            .1
            .integer_coefficients()
            .1
    }

    pub fn enclosure(
        &self,
        width: &Rational,
    ) -> Result<engine_kernel::interval::Interval, QuadraticError> {
        if !width.is_positive() {
            return Err(QuadraticError::NonPositiveWidth);
        }
        if self.is_rational() {
            return Ok(engine_kernel::interval::Interval::point(self.a.clone()));
        }
        if self.radicand.is_negative() {
            return Err(QuadraticError::NotReal(self.radicand.clone()));
        }
        if [
            self.a.numer(),
            self.a.denom(),
            self.b.numer(),
            self.b.denom(),
            width.numer(),
            width.denom(),
            &self.radicand,
        ]
        .iter()
        .any(|n| n.bits() > 16384)
        {
            return Err(QuadraticError::EnclosureBudget);
        }
        let scale = (self.b.abs() / width)
            .ceil()
            .to_integer()
            .max(BigInt::one());
        if scale.bits() > 16384 {
            return Err(QuadraticError::EnclosureBudget);
        }
        let k = (&self.radicand * &scale * &scale).sqrt();
        let low = Rational::new(k.clone(), scale.clone());
        let high = Rational::new(k + BigInt::one(), scale);
        let (low, high) = if self.b.is_positive() {
            (low, high)
        } else {
            (high, low)
        };
        Ok(engine_kernel::interval::Interval::new(
            &self.a + &self.b * low,
            &self.a + &self.b * high,
        ))
    }

    pub fn radicand(&self) -> &BigInt {
        &self.radicand
    }

    pub fn is_zero(&self) -> bool {
        self.a.is_zero() && self.b.is_zero()
    }

    pub fn is_rational(&self) -> bool {
        self.b.is_zero()
    }

    fn common_radicand(&self, other: &Self) -> Result<BigInt, QuadraticError> {
        if self.b.is_zero() {
            Ok(other.radicand.clone())
        } else if other.b.is_zero() || self.radicand == other.radicand {
            Ok(self.radicand.clone())
        } else {
            Err(QuadraticError::RadicandMismatch {
                left: self.radicand.clone(),
                right: other.radicand.clone(),
            })
        }
    }

    pub fn add(&self, other: &Self) -> Result<Self, QuadraticError> {
        let d = self.common_radicand(other)?;
        Ok(Self::normalised(d, &self.a + &other.a, &self.b + &other.b))
    }

    pub fn sub(&self, other: &Self) -> Result<Self, QuadraticError> {
        let d = self.common_radicand(other)?;
        Ok(Self::normalised(d, &self.a - &other.a, &self.b - &other.b))
    }

    pub fn neg(&self) -> Self {
        Self::normalised(self.radicand.clone(), -&self.a, -&self.b)
    }

    pub fn mul(&self, other: &Self) -> Result<Self, QuadraticError> {
        let d = self.common_radicand(other)?;
        let d_rational = Rational::from_integer(d.clone());
        Ok(Self::normalised(
            d,
            &self.a * &other.a + &d_rational * &self.b * &other.b,
            &self.a * &other.b + &self.b * &other.a,
        ))
    }

    pub fn conjugate(&self) -> Self {
        Self::normalised(self.radicand.clone(), self.a.clone(), -&self.b)
    }

    pub fn norm(&self) -> Rational {
        &self.a * &self.a - Rational::from_integer(self.radicand.clone()) * &self.b * &self.b
    }

    pub fn trace(&self) -> Rational {
        &self.a + &self.a
    }

    pub fn inverse(&self) -> Option<Self> {
        let norm = self.norm();
        if norm.is_zero() {
            return None;
        }
        Some(Self::normalised(
            self.radicand.clone(),
            &self.a / &norm,
            -&self.b / &norm,
        ))
    }

    pub fn checked_div(&self, other: &Self) -> Result<Self, QuadraticError> {
        let inverse = other.inverse().ok_or(QuadraticError::DivisionByZero)?;
        self.mul(&inverse)
    }

    pub fn pow(&self, n: u32) -> Self {
        let mut result = Self::from_rational(r_one());
        let mut base = self.clone();
        let mut n = n;
        while n > 0 {
            if n & 1 == 1 {
                result = Self::normalised(
                    self.radicand.clone(),
                    &result.a * &base.a
                        + Rational::from_integer(self.radicand.clone()) * &result.b * &base.b,
                    &result.a * &base.b + &result.b * &base.a,
                );
            }
            n >>= 1;
            if n > 0 {
                base = Self::normalised(
                    self.radicand.clone(),
                    &base.a * &base.a
                        + Rational::from_integer(self.radicand.clone()) * &base.b * &base.b,
                    &base.a * &base.b + &base.b * &base.a,
                );
            }
        }
        result
    }

    pub fn sign(&self) -> Result<Ordering, QuadraticError> {
        if self.b.is_zero() {
            return Ok(self.a.cmp(&r_zero()));
        }
        if self.radicand.is_negative() {
            return Err(QuadraticError::NotReal(self.radicand.clone()));
        }
        Ok(real_sign(
            &self.a,
            &self.b,
            &Rational::from_integer(self.radicand.clone()),
        ))
    }

    pub fn cmp_real(&self, other: &Self) -> Result<Ordering, QuadraticError> {
        self.sub(other)?.sign()
    }

    fn rational_sqrt_in_field(&self, field: &BigInt, d: &Rational) -> Option<Self> {
        if let Some(root) = sqrt_exact(&self.a) {
            return Some(Self::from_rational(root));
        }
        if !field.is_one() {
            if let Some(z) = sqrt_exact(&(&self.a / d)) {
                return Some(Self::normalised(field.clone(), r_zero(), z));
            }
        }
        None
    }

    pub fn sqrt_in(&self, field: &BigInt) -> Result<Option<Self>, QuadraticError> {
        check_radicand(field)?;
        if !self.b.is_zero() && self.radicand != *field {
            return Err(QuadraticError::RadicandMismatch {
                left: self.radicand.clone(),
                right: field.clone(),
            });
        }
        let d = Rational::from_integer(field.clone());
        if self.b.is_zero() {
            return Ok(self.rational_sqrt_in_field(field, &d));
        }
        let norm = &self.a * &self.a - &d * &self.b * &self.b;
        let Some(r) = sqrt_exact(&norm) else {
            return Ok(None);
        };
        for signed_r in [r.clone(), -r] {
            let half_sum = (&self.a + signed_r) * half();
            if let Some(s) = sqrt_exact(&half_sum) {
                if !s.is_zero() {
                    let v = &self.b / (&s + &s);
                    return Ok(Some(Self::normalised(field.clone(), s, v)));
                }
            }
        }
        Ok(None)
    }

    pub fn is_square_in(&self, field: &BigInt) -> Result<bool, QuadraticError> {
        Ok(self.sqrt_in(field)?.is_some())
    }
}

impl fmt::Display for QuadraticNumber {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.b.is_zero() {
            write!(f, "{}", self.a)
        } else {
            write!(f, "{} + {}*sqrt({})", self.a, self.b, self.radicand)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::cyclotomic::{EisensteinRat, GaussianRat};
    use crate::rational::{integer_sqrt, rq};
    use crate::test_support::{check_field_axioms, Lcg};

    type Q2 = Quadratic<2>;

    #[test]
    fn runtime_quadratics_have_minimal_polynomials_and_certified_bounded_enclosures() {
        let phi = QuadraticNumber::new(BigInt::from(5), rq(1, 2), rq(1, 2)).unwrap();
        assert_eq!(
            phi.minimal_polynomial(),
            vec![(-1).into(), (-1).into(), 1.into()]
        );
        let interval = phi.enclosure(&rq(1, 1_000_000)).unwrap();
        assert!(interval.diam() <= rq(1, 1_000_000));
        let polynomial = |q: &Rational| q * q - q - r_one();
        assert!(polynomial(interval.lo()).is_negative());
        assert!(polynomial(interval.hi()).is_positive());
        let negative = phi.neg().enclosure(&rq(1, 1_000_000)).unwrap();
        assert_eq!(negative.lo(), &-interval.hi());
        assert_eq!(negative.hi(), &-interval.lo());
        assert_eq!(
            QuadraticNumber::from_rational(rq(7, 3)).minimal_polynomial(),
            vec![(-7).into(), 3.into()]
        );
        assert!(matches!(
            phi.enclosure(&r_zero()),
            Err(QuadraticError::NonPositiveWidth)
        ));
        assert!(matches!(
            phi.enclosure(&Rational::new(BigInt::one(), BigInt::one() << 16385usize)),
            Err(QuadraticError::EnclosureBudget)
        ));
        let imaginary = QuadraticNumber::new(BigInt::from(-1), r_zero(), r_one()).unwrap();
        assert!(matches!(
            imaginary.enclosure(&rq(1, 10)),
            Err(QuadraticError::NotReal(_))
        ));
    }
    type Q3 = Quadratic<3>;
    type Q5 = Quadratic<5>;
    type Q7 = Quadratic<7>;

    fn samples<const D: i64>() -> Vec<Quadratic<D>> {
        vec![
            Quadratic::zero(),
            Quadratic::one(),
            Quadratic::sqrt_d(),
            Quadratic::from_ints(3, -4),
            Quadratic::new(rq(1, 2), rq(-2, 3)),
            Quadratic::new(rq(-5, 7), rq(3, 2)),
        ]
    }


    #[test]
    fn the_radicand_predicate_accepts_exactly_the_squarefree_integers_other_than_0_and_1() {
        let accepted = [
            2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23, 26, -1, -2, -3, -5, -6, -7,
        ];
        for d in accepted {
            assert!(is_valid_radicand(d), "{d} is squarefree");
        }
        let refused = [
            0, 1, 4, 8, 9, 12, 16, 18, 20, 24, 25, 27, 28, 32, 36, -4, -8, -9, -12, -16, -18,
        ];
        for d in refused {
            assert!(!is_valid_radicand(d), "{d} is 0, 1 or has a square factor");
        }
        for d in -300i64..=300 {
            let runtime = d != 0
                && d != 1
                && squarefree_part(&BigInt::from(d))
                    .map(|(_, root)| root == BigInt::one())
                    .unwrap_or(false);
            assert_eq!(is_valid_radicand(d), runtime, "d = {d}");
        }
    }


    #[test]
    fn every_quadratic_field_satisfies_the_field_axioms() {
        check_field_axioms(&samples::<2>());
        check_field_axioms(&samples::<3>());
        check_field_axioms(&samples::<5>());
        check_field_axioms(&samples::<7>());
        check_field_axioms(&samples::<-1>());
        check_field_axioms(&samples::<-3>());
        check_field_axioms(&samples::<-7>());
    }

    #[test]
    fn multiplication_reduces_sqrt_d_squared_to_d() {
        assert_eq!(Q2::sqrt_d().mul(&Q2::sqrt_d()), Q2::from_ints(2, 0));
        assert_eq!(Q5::sqrt_d().mul(&Q5::sqrt_d()), Q5::from_ints(5, 0));
        assert_eq!(
            Quadratic::<-1>::sqrt_d().mul(&Quadratic::<-1>::sqrt_d()),
            Quadratic::<-1>::from_ints(-1, 0)
        );
        assert_eq!(
            Q3::from_ints(1, 1).mul(&Q3::from_ints(2, -1)),
            Q3::from_ints(-1, 1)
        );
    }

    #[test]
    fn the_norm_is_multiplicative_and_the_conjugate_is_a_ring_automorphism() {
        let mut rng = Lcg::new(17);
        for _ in 0..60 {
            let x = Q5::new(
                rq(rng.next_signed(9), 1 + rng.next_below(5) as i64),
                rq(rng.next_signed(9), 1 + rng.next_below(5) as i64),
            );
            let y = Q5::new(
                rq(rng.next_signed(9), 1 + rng.next_below(5) as i64),
                rq(rng.next_signed(9), 1 + rng.next_below(5) as i64),
            );
            assert_eq!(x.mul(&y).norm(), x.norm() * y.norm(), "N(xy) = N(x) N(y)");
            assert_eq!(x.mul(&y).conjugate(), x.conjugate().mul(&y.conjugate()));
            assert_eq!(x.add(&y).conjugate(), x.conjugate().add(&y.conjugate()));
            assert_eq!(x.conjugate().conjugate(), x);
            assert_eq!(x.mul(&x.conjugate()), Q5::new(x.norm(), r_zero()));
            assert_eq!(x.add(&x.conjugate()), Q5::new(x.trace(), r_zero()));
        }
    }

    #[test]
    fn inverse_divides_exactly_and_zero_has_none() {
        let x = Q7::new(rq(3, 2), rq(-5, 3));
        assert_eq!(x.mul(&x.inverse().unwrap()), Q7::one());
        assert_eq!(Q7::zero().inverse(), None);
        assert_eq!(Q7::one().checked_div(&Q7::zero()), None);
        let y = Q7::from_ints(2, 1);
        assert_eq!(x.checked_div(&y).unwrap().mul(&y), x);
    }

    #[test]
    fn pow_matches_repeated_multiplication() {
        let x = Q3::from_ints(2, 1);
        let mut acc = Q3::one();
        for n in 0..12u32 {
            assert_eq!(x.pow(n), acc, "x^{n}");
            acc = acc.mul(&x);
        }
    }

    #[test]
    fn std_operators_agree_with_the_inherent_methods() {
        let a = Q5::new(rq(1, 3), rq(2, 5));
        let b = Q5::new(rq(-7, 2), rq(1, 9));
        assert_eq!(a.clone() + b.clone(), a.add(&b));
        assert_eq!(&a - &b, a.sub(&b));
        assert_eq!(a.clone() * b.clone(), a.mul(&b));
        assert_eq!(-a.clone(), a.neg());
        assert_eq!(&a * &b, a.mul(&b));
    }


    #[test]
    fn the_golden_ratio_satisfies_its_defining_identities() {
        let phi = Q5::golden_ratio();
        let psi = Q5::golden_ratio_conjugate();
        assert_eq!(phi.mul(&phi), phi.add(&Q5::one()), "phi^2 = phi + 1");
        assert_eq!(psi.mul(&psi), psi.add(&Q5::one()), "psi^2 = psi + 1");
        assert_eq!(phi.add(&psi), Q5::one(), "phi + psi = 1");
        assert_eq!(phi.mul(&psi), Q5::from_ints(-1, 0), "phi psi = -1");
        assert_eq!(phi.conjugate(), psi);
        assert_eq!(
            phi.inverse().unwrap(),
            phi.sub(&Q5::one()),
            "1/phi = phi - 1"
        );
        assert_eq!(phi.sub(&psi), Q5::sqrt_d(), "phi - psi = sqrt 5");
        assert_eq!(phi.norm(), ri(-1));
        assert_eq!(phi.trace(), ri(1));
    }

    #[test]
    fn powers_of_phi_carry_the_fibonacci_numbers() {
        let phi = Q5::golden_ratio();
        let (mut f_prev, mut f) = (BigInt::from(0), BigInt::from(1));
        for n in 1..=60u32 {
            let expected = Q5::new(Rational::from_integer(f_prev.clone()), r_zero())
                .add(&phi.scale(&Rational::from_integer(f.clone())));
            assert_eq!(phi.pow(n), expected, "phi^{n}");
            let next = &f_prev + &f;
            f_prev = f;
            f = next;
        }
    }

    #[test]
    fn the_silver_ratio_satisfies_its_defining_identities() {
        let delta = Q2::silver_ratio();
        assert_eq!(
            delta.mul(&delta),
            delta.scale(&ri(2)).add(&Q2::one()),
            "delta^2 = 2 delta + 1"
        );
        assert_eq!(
            delta.inverse().unwrap(),
            delta.sub(&Q2::from_ints(2, 0)),
            "1/delta = delta - 2"
        );
        assert_eq!(delta.norm(), ri(-1));
        assert_eq!(delta.conjugate(), Q2::from_ints(1, -1));
    }


    fn sqrt_enclosure(d: i64, digits: u32) -> (Rational, Rational) {
        let scale = BigInt::from(10u8).pow(digits);
        let root = integer_sqrt(&(BigInt::from(d) * &scale * &scale));
        (
            Rational::new(root.clone(), scale.clone()),
            Rational::new(root + BigInt::one(), scale),
        )
    }

    #[test]
    fn exact_sign_agrees_with_an_independent_rational_enclosure_of_the_root() {
        fn check<const D: i64>() {
            let (lo, hi) = sqrt_enclosure(D, 12);
            for a in -12..=12i64 {
                for b in -12..=12i64 {
                    let x = Quadratic::<D>::new(rq(a, 3), rq(b, 2));
                    let (p, q) = (&x.a + &x.b * &lo, &x.a + &x.b * &hi);
                    let expected = if p.is_positive() && q.is_positive() {
                        Ordering::Greater
                    } else if p.is_negative() && q.is_negative() {
                        Ordering::Less
                    } else if a == 0 && b == 0 {
                        Ordering::Equal
                    } else {
                        panic!("bracket straddles zero for {a}/3 + {b}/2 sqrt({D})");
                    };
                    assert_eq!(x.sign(), expected, "sign of {a}/3 + {b}/2 sqrt({D})");
                }
            }
        }
        check::<2>();
        check::<3>();
        check::<5>();
        check::<7>();
        check::<10>();
        check::<11>();
    }

    #[test]
    fn exact_sign_is_correct_where_floating_point_cannot_tell() {
        let (mut x, mut y) = (BigInt::from(3), BigInt::from(2));
        for step in 0..60 {
            let t = Q2::new(
                Rational::from_integer(x.clone()),
                Rational::from_integer(-y.clone()),
            );
            assert!(
                t.is_positive(),
                "step {step}: x - y sqrt 2 > 0 because x^2 - 2y^2 = 1"
            );
            let below = Rational::new(BigInt::one(), BigInt::from(2) * &x);
            let above = Rational::new(BigInt::one(), BigInt::from(2) * &x - BigInt::one());
            assert!(
                t.sub(&Q2::from_rational(below)).is_positive(),
                "step {step}: t > 1/(2x)"
            );
            assert!(
                t.sub(&Q2::from_rational(above)).is_negative(),
                "step {step}: t < 1/(2x - 1)"
            );
            let next_x = BigInt::from(3) * &x + BigInt::from(4) * &y;
            let next_y = BigInt::from(2) * &x + BigInt::from(3) * &y;
            x = next_x;
            y = next_y;
        }
        assert!(
            x > BigInt::from(10u8).pow(40),
            "the loop reached 40-digit solutions"
        );
        assert!(Q2::from_ints(1, -1).is_negative());
        assert!(Q2::from_ints(7, -5).is_negative(), "49 - 50 = -1");
        assert!(Q2::from_ints(7, -5).neg().is_positive());
    }

    #[test]
    fn the_order_is_total_translation_invariant_and_scale_compatible() {
        let mut rng = Lcg::new(99);
        let make = |rng: &mut Lcg| {
            Q3::new(
                rq(rng.next_signed(8), 1 + rng.next_below(4) as i64),
                rq(rng.next_signed(8), 1 + rng.next_below(4) as i64),
            )
        };
        for _ in 0..80 {
            let (x, y, z) = (make(&mut rng), make(&mut rng), make(&mut rng));
            assert_eq!(x.cmp(&y), y.cmp(&x).reverse(), "antisymmetry");
            assert_eq!(
                x.cmp(&y) == Ordering::Equal,
                x == y,
                "cmp agrees with equality"
            );
            assert_eq!(
                x.add(&z).cmp(&y.add(&z)),
                x.cmp(&y),
                "translation invariance"
            );
            if z.is_positive() {
                assert_eq!(x.mul(&z).cmp(&y.mul(&z)), x.cmp(&y), "positive scaling");
            }
            if x < y && y < z {
                assert!(x < z, "transitivity");
            }
        }
    }

    #[test]
    fn the_order_of_known_real_numbers_is_correct() {
        assert!(Q2::sqrt_d() < Q2::new(rq(3, 2), r_zero()));
        assert!(Q3::new(rq(3, 2), r_zero()) < Q3::sqrt_d());
        assert!(Q3::sqrt_d() < Q3::new(rq(7, 4), r_zero()));
        let t = Q5::new(rq(-1, 2), rq(1, 2));
        assert!(t.is_positive());
        assert!(t.conjugate().is_negative());
        assert!(Q5::golden_ratio() > Q5::one());
        assert!(Q5::golden_ratio_conjugate() < Q5::zero());
        assert!(Q5::zero().sign() == Ordering::Equal);
        assert!(
            Q5::zero().is_nonnegative() && !Q5::zero().is_positive() && !Q5::zero().is_negative()
        );
    }


    #[test]
    fn quadratic_minus_one_agrees_with_the_gaussian_rationals() {
        let to_gaussian = |x: &Quadratic<-1>| GaussianRat {
            re: x.a.clone(),
            im: x.b.clone(),
        };
        let mut rng = Lcg::new(5);
        let make = |rng: &mut Lcg| {
            Quadratic::<-1>::new(
                rq(rng.next_signed(6), 1 + rng.next_below(3) as i64),
                rq(rng.next_signed(6), 1 + rng.next_below(3) as i64),
            )
        };
        for _ in 0..50 {
            let (x, y) = (make(&mut rng), make(&mut rng));
            assert_eq!(
                to_gaussian(&x.mul(&y)),
                to_gaussian(&x).mul(&to_gaussian(&y))
            );
            assert_eq!(
                to_gaussian(&x.add(&y)),
                to_gaussian(&x).add(&to_gaussian(&y))
            );
            assert_eq!(to_gaussian(&x.conjugate()), to_gaussian(&x).conj());
            if let Some(inverse) = x.inverse() {
                assert_eq!(to_gaussian(&inverse), to_gaussian(&x).inv());
            }
            assert_eq!(x.norm(), to_gaussian(&x).norm_sq());
        }
    }

    #[test]
    fn quadratic_minus_three_agrees_with_the_eisenstein_rationals() {
        let to_eisenstein = |x: &Quadratic<-3>| EisensteinRat {
            a: &x.a + &x.b,
            b: &x.b + &x.b,
        };
        let mut rng = Lcg::new(6);
        let make = |rng: &mut Lcg| {
            Quadratic::<-3>::new(
                rq(rng.next_signed(6), 1 + rng.next_below(3) as i64),
                rq(rng.next_signed(6), 1 + rng.next_below(3) as i64),
            )
        };
        for _ in 0..50 {
            let (x, y) = (make(&mut rng), make(&mut rng));
            assert_eq!(
                to_eisenstein(&x.mul(&y)),
                to_eisenstein(&x).mul(&to_eisenstein(&y))
            );
            assert_eq!(
                to_eisenstein(&x.add(&y)),
                to_eisenstein(&x).add(&to_eisenstein(&y))
            );
            assert_eq!(to_eisenstein(&x.conjugate()), to_eisenstein(&x).conj());
            assert_eq!(x.norm(), to_eisenstein(&x).norm_sq());
        }
    }


    #[test]
    fn squares_of_elements_have_a_square_root_that_squares_back() {
        let mut rng = Lcg::new(1234);
        for _ in 0..80 {
            let y = Q5::new(
                rq(rng.next_signed(7), 1 + rng.next_below(4) as i64),
                rq(rng.next_signed(7), 1 + rng.next_below(4) as i64),
            );
            let x = y.mul(&y);
            let root = x.sqrt().expect("the square of an element has a root");
            assert_eq!(root.mul(&root), x);
            assert!(
                root == y || root == y.neg(),
                "the root is one of the two roots"
            );
        }
        let mut rng = Lcg::new(4321);
        for _ in 0..40 {
            let y = Quadratic::<-1>::new(
                rq(rng.next_signed(7), 1 + rng.next_below(4) as i64),
                rq(rng.next_signed(7), 1 + rng.next_below(4) as i64),
            );
            let x = y.mul(&y);
            let root = x
                .sqrt()
                .expect("the square of a Gaussian rational has a root");
            assert_eq!(root.mul(&root), x);
        }
    }

    #[test]
    fn square_root_decisions_on_known_cases() {
        assert_eq!(Q2::from_ints(3, 2).sqrt(), Some(Q2::from_ints(1, 1)));
        assert_eq!(Q5::new(rq(3, 2), rq(1, 2)).sqrt(), Some(Q5::golden_ratio()));
        assert_eq!(Q2::from_ints(2, 0).sqrt(), Some(Q2::sqrt_d()));
        assert_eq!(Q3::from_ints(2, 0).sqrt(), None);
        assert_eq!(Q5::from_ints(2, 0).sqrt(), None);
        assert_eq!(
            Quadratic::<-1>::from_ints(-1, 0).sqrt(),
            Some(Quadratic::<-1>::sqrt_d())
        );
        assert_eq!(Q5::from_ints(-1, 0).sqrt(), None);
        assert_eq!(
            Quadratic::<-1>::from_ints(3, 4).sqrt(),
            Some(Quadratic::<-1>::from_ints(2, 1))
        );
        assert_eq!(Q5::zero().sqrt(), Some(Q5::zero()));
        assert_eq!(Q5::one().sqrt(), Some(Q5::one()));
        assert_eq!(
            Q5::new(rq(9, 4), r_zero()).sqrt(),
            Some(Q5::new(rq(3, 2), r_zero()))
        );
        assert_eq!(Q2::from_ints(1, 1).sqrt(), None);
        assert_eq!(Q3::from_ints(2, 1).sqrt(), None);
    }

    #[test]
    fn sqrt_returns_the_root_with_positive_rational_part() {
        let root = Q2::from_ints(3, -2).sqrt().unwrap();
        assert_eq!(root, Q2::from_ints(1, -1));
        assert!(root.a.is_positive());
    }


    #[test]
    fn conversion_between_the_typed_and_runtime_forms_round_trips() {
        let x = Q5::new(rq(2, 3), rq(-1, 7));
        let n = x.to_number();
        assert_eq!(n.radicand(), &BigInt::from(5));
        assert_eq!(Q5::from_number(&n), Some(x.clone()));
        let other = QuadraticNumber::new(BigInt::from(3), ri(1), ri(1)).unwrap();
        assert_eq!(Q5::from_number(&other), None);
        let rational = QuadraticNumber::from_rational(rq(3, 4));
        assert_eq!(
            Q5::from_number(&rational),
            Some(Q5::new(rq(3, 4), r_zero()))
        );
        assert_eq!(
            Q5::from_ints(4, 0).to_number(),
            QuadraticNumber::from_rational(ri(4))
        );
    }

    #[test]
    fn wire_round_trip_and_the_typed_form_keeps_its_radicand() {
        let x = Q7::new(rq(1, 3), rq(-5, 2));
        let text = serde_json::to_string(&x).unwrap();
        let back: Q7 = serde_json::from_str(&text).unwrap();
        assert_eq!(back, x);
    }


    fn surd(c: Rational, square: Rational) -> Surd {
        Surd::new(c, &square).unwrap()
    }

    #[test]
    fn surd_normalisation_extracts_square_factors_and_denominators() {
        let s = surd(ri(1), ri(8));
        assert_eq!((s.coefficient(), s.radicand()), (&ri(2), &BigInt::from(2)));
        let s = surd(ri(1), rq(1, 2));
        assert_eq!(
            (s.coefficient(), s.radicand()),
            (&rq(1, 2), &BigInt::from(2))
        );
        let s = surd(ri(1), rq(2, 9));
        assert_eq!(
            (s.coefficient(), s.radicand()),
            (&rq(1, 3), &BigInt::from(2))
        );
        let scales: Vec<(i64, i64, i64)> = vec![
            (1, 1, 1),
            (2, 3, 3),
            (3, 6, 6),
            (4, 10, 10),
            (5, 15, 15),
            (7, 7, 14),
        ];
        for (l, radicand, denominator) in scales {
            let s = surd(ri(1), rq(2, l * (l + 1)));
            assert_eq!(
                s.radicand(),
                &BigInt::from(radicand),
                "radicand for l = {l}"
            );
            assert_eq!(
                s.coefficient(),
                &rq(1, denominator),
                "coefficient for l = {l}"
            );
        }
    }

    #[test]
    fn surd_zero_has_a_single_normal_form_and_equality_is_mathematical() {
        assert_eq!(surd(ri(0), ri(7)), Surd::zero());
        assert_eq!(surd(ri(5), ri(0)), Surd::zero());
        assert_eq!(surd(ri(1), ri(9)), Surd::rational(ri(3)));
        assert_eq!(surd(ri(2), ri(2)), surd(ri(1), ri(8)), "2 sqrt 2 = sqrt 8");
        assert_eq!(surd(rq(1, 2), ri(8)), surd(ri(1), ri(2)));
        assert!(Surd::zero().is_zero());
        assert!(Surd::rational(ri(3)).is_rational());
        assert!(!surd(ri(1), ri(2)).is_rational());
    }

    #[test]
    fn a_negative_radicand_is_refused_whatever_the_coefficient() {
        assert_eq!(
            Surd::new(ri(0), &ri(-1)),
            Err(QuadraticError::NegativeRadicand(ri(-1)))
        );
        assert_eq!(
            Surd::new(ri(3), &rq(-1, 4)),
            Err(QuadraticError::NegativeRadicand(rq(-1, 4)))
        );
        assert!(matches!(
            Surd::from_natural(ri(1), &BigInt::from(-3)),
            Err(QuadraticError::NegativeRadicand(_))
        ));
        assert!(matches!(
            Surd::new(
                ri(1),
                &num_rational::Ratio::new_raw(BigInt::from(2), BigInt::from(-4))
            ),
            Err(QuadraticError::NegativeRadicand(_))
        ));
    }

    #[test]
    fn surds_multiply_and_invert_in_normal_form() {
        let a = surd(ri(3), ri(2));
        let b = surd(ri(1), ri(6));
        assert_eq!(a.mul(&b), surd(ri(6), ri(3)));
        let r2 = surd(ri(1), ri(2));
        assert_eq!(r2.mul(&r2), Surd::rational(ri(2)));
        assert_eq!(a.square(), ri(18));
        assert_eq!(a.inverse().unwrap(), surd(rq(1, 6), ri(2)));
        assert_eq!(a.mul(&a.inverse().unwrap()), Surd::one());
        assert_eq!(Surd::zero().inverse(), None);
        assert_eq!(
            a.checked_div(&Surd::zero()),
            Err(QuadraticError::DivisionByZero)
        );
        assert_eq!(a.mul(&Surd::zero()), Surd::zero());
    }

    #[test]
    fn surd_sums_exist_only_for_equal_radicands_or_zero() {
        let (a, b) = (surd(ri(1), ri(2)), surd(ri(3), ri(2)));
        assert_eq!(a.checked_add(&b).unwrap(), surd(ri(4), ri(2)));
        assert_eq!(a.checked_sub(&a).unwrap(), Surd::zero());
        assert_eq!(a.checked_add(&Surd::zero()).unwrap(), a);
        assert_eq!(Surd::zero().checked_add(&b).unwrap(), b);
        assert_eq!(
            a.checked_add(&surd(ri(1), ri(3))),
            Err(QuadraticError::SurdSumNotSingle {
                left: BigInt::from(2),
                right: BigInt::from(3)
            })
        );
        assert!(a.checked_add(&Surd::one()).is_err());
    }

    #[test]
    fn surd_order_is_the_order_of_the_real_numbers() {
        let values = [
            surd(ri(-3), ri(2)),
            surd(ri(-1), ri(5)),
            Surd::rational(ri(-2)),
            surd(ri(-1), ri(2)),
            Surd::zero(),
            surd(rq(1, 2), ri(2)),
            surd(ri(1), ri(2)),
            Surd::rational(ri(2)),
            surd(ri(1), ri(5)),
            surd(ri(3), ri(2)),
        ];
        for window in values.windows(2) {
            assert!(window[0] < window[1], "{} < {}", window[0], window[1]);
        }
        for (i, x) in values.iter().enumerate() {
            for (j, y) in values.iter().enumerate() {
                assert_eq!(x.cmp(y), i.cmp(&j));
            }
        }
        assert_eq!(surd(ri(1), ri(2)).sign(), Ordering::Greater);
        assert_eq!(surd(ri(-1), ri(2)).sign(), Ordering::Less);
    }

    #[test]
    fn surd_embeds_into_the_quadratic_number_with_the_same_value() {
        let s = surd(rq(2, 3), ri(5));
        let n = s.to_number();
        assert_eq!(n.radicand(), &BigInt::from(5));
        assert_eq!(n.rational_part(), &r_zero());
        assert_eq!(n.sqrt_part(), &rq(2, 3));
        assert_eq!(
            Surd::rational(ri(4)).to_number(),
            QuadraticNumber::from_rational(ri(4))
        );
    }


    fn number(d: i64, a: Rational, b: Rational) -> QuadraticNumber {
        QuadraticNumber::new(BigInt::from(d), a, b).unwrap()
    }

    #[test]
    fn a_non_squarefree_or_zero_radicand_is_refused() {
        assert_eq!(
            QuadraticNumber::new(BigInt::from(0), ri(1), ri(1)),
            Err(QuadraticError::ZeroRadicand)
        );
        assert_eq!(
            QuadraticNumber::new(BigInt::from(12), ri(1), ri(1)),
            Err(QuadraticError::RadicandNotSquarefree {
                radicand: BigInt::from(12),
                squarefree: BigInt::from(3),
                root: BigInt::from(2)
            })
        );
        assert!(QuadraticNumber::new(BigInt::from(-8), ri(1), ri(1)).is_err());
        assert!(QuadraticNumber::new(BigInt::from(-3), ri(1), ri(1)).is_ok());
        assert!(QuadraticNumber::new(BigInt::from(1), ri(1), ri(1)).is_ok());
    }

    #[test]
    fn rational_elements_have_one_normal_form_whatever_field_they_came_from() {
        assert_eq!(number(5, ri(3), ri(0)), number(2, ri(3), ri(0)));
        assert_eq!(
            number(5, ri(3), ri(0)),
            QuadraticNumber::from_rational(ri(3))
        );
        assert_eq!(number(5, ri(3), ri(0)).radicand(), &BigInt::one());
        assert_eq!(
            number(1, ri(1), ri(2)),
            QuadraticNumber::from_rational(ri(3))
        );
        assert_eq!(number(5, ri(3), ri(1)).radicand(), &BigInt::from(5));
    }

    #[test]
    fn operations_lift_rationals_and_refuse_to_mix_irrational_fields() {
        let x = number(2, ri(1), ri(1));
        let y = number(3, ri(1), ri(1));
        let r = QuadraticNumber::from_rational(rq(1, 2));
        assert_eq!(x.add(&r).unwrap(), number(2, rq(3, 2), ri(1)));
        assert_eq!(r.mul(&x).unwrap(), number(2, rq(1, 2), rq(1, 2)));
        assert_eq!(r.add(&r).unwrap(), QuadraticNumber::from_rational(ri(1)));
        fn mismatch<T>() -> Result<T, QuadraticError> {
            Err(QuadraticError::RadicandMismatch {
                left: BigInt::from(2),
                right: BigInt::from(3),
            })
        }
        assert_eq!(x.add(&y), mismatch());
        assert_eq!(x.mul(&y), mismatch());
        assert_eq!(x.sub(&y), mismatch());
        assert_eq!(x.checked_div(&y), mismatch());
        assert_eq!(x.cmp_real(&y), mismatch());
        assert_eq!(x.sub(&x).unwrap(), QuadraticNumber::from_rational(ri(0)));
    }

    #[test]
    fn quadratic_number_arithmetic_agrees_with_the_compile_time_type() {
        let mut rng = Lcg::new(77);
        for _ in 0..60 {
            let (a, b, c, d) = (
                rq(rng.next_signed(6), 1 + rng.next_below(3) as i64),
                rq(rng.next_signed(6), 1 + rng.next_below(3) as i64),
                rq(rng.next_signed(6), 1 + rng.next_below(3) as i64),
                rq(rng.next_signed(6), 1 + rng.next_below(3) as i64),
            );
            let (tx, ty) = (Q3::new(a.clone(), b.clone()), Q3::new(c.clone(), d.clone()));
            let (nx, ny) = (number(3, a, b), number(3, c, d));
            assert_eq!(nx.mul(&ny).unwrap(), tx.mul(&ty).to_number());
            assert_eq!(nx.add(&ny).unwrap(), tx.add(&ty).to_number());
            assert_eq!(nx.sub(&ny).unwrap(), tx.sub(&ty).to_number());
            assert_eq!(nx.conjugate(), tx.conjugate().to_number());
            assert_eq!(nx.norm(), tx.norm());
            assert_eq!(nx.trace(), tx.trace());
            assert_eq!(nx.inverse(), tx.inverse().map(|t| t.to_number()));
            assert_eq!(nx.sign().unwrap(), tx.sign());
            assert_eq!(nx.pow(5), tx.pow(5).to_number());
        }
    }

    #[test]
    fn signs_of_quadratic_numbers_are_exact_and_imaginary_fields_refuse() {
        assert_eq!(number(2, ri(-1), ri(1)).sign().unwrap(), Ordering::Greater);
        assert_eq!(number(2, ri(-3), ri(2)).sign().unwrap(), Ordering::Less);
        assert_eq!(
            QuadraticNumber::from_rational(ri(-3)).sign().unwrap(),
            Ordering::Less
        );
        assert_eq!(
            number(-1, ri(0), ri(1)).sign(),
            Err(QuadraticError::NotReal(BigInt::from(-1)))
        );
        assert_eq!(number(-3, ri(2), ri(0)).sign().unwrap(), Ordering::Greater);
        assert_eq!(
            number(2, ri(3), ri(0))
                .cmp_real(&number(2, ri(0), ri(2)))
                .unwrap(),
            Ordering::Greater,
            "3 > 2 sqrt 2 = 2.83"
        );
    }

    #[test]
    fn sqrt_in_decides_squares_inside_a_named_field() {
        let field = BigInt::from(5);
        let phi_squared = number(5, rq(3, 2), rq(1, 2));
        let root = phi_squared.sqrt_in(&field).unwrap().unwrap();
        assert_eq!(root, number(5, rq(1, 2), rq(1, 2)));
        assert_eq!(root.mul(&root).unwrap(), phi_squared);
        let five = QuadraticNumber::from_rational(ri(5));
        assert_eq!(five.sqrt_in(&field).unwrap(), Some(number(5, ri(0), ri(1))));
        assert_eq!(five.sqrt_in(&BigInt::one()).unwrap(), None);
        let four = QuadraticNumber::from_rational(ri(4));
        assert_eq!(
            four.sqrt_in(&field).unwrap(),
            Some(QuadraticNumber::from_rational(ri(2)))
        );
        assert_eq!(
            QuadraticNumber::from_rational(ri(2))
                .sqrt_in(&field)
                .unwrap(),
            None
        );
        assert!(phi_squared.is_square_in(&field).unwrap());
        assert!(!QuadraticNumber::from_rational(ri(2))
            .is_square_in(&field)
            .unwrap());
    }

    #[test]
    fn sqrt_in_refuses_a_foreign_field_and_an_invalid_field() {
        let x = number(2, ri(1), ri(1));
        assert_eq!(
            x.sqrt_in(&BigInt::from(3)),
            Err(QuadraticError::RadicandMismatch {
                left: BigInt::from(2),
                right: BigInt::from(3)
            })
        );
        assert_eq!(
            x.sqrt_in(&BigInt::from(0)),
            Err(QuadraticError::ZeroRadicand)
        );
        assert!(matches!(
            x.sqrt_in(&BigInt::from(8)),
            Err(QuadraticError::RadicandNotSquarefree { .. })
        ));
        assert!(x.sqrt_in(&BigInt::one()).is_err());
    }

    #[test]
    fn the_square_root_decision_is_sound_and_complete_on_a_grid() {
        let field = BigInt::from(6);
        let mut roots_found = 0;
        for a in -8..=8i64 {
            for b in -8..=8i64 {
                let x = number(6, rq(a, 2), rq(b, 3));
                let square = x.mul(&x).unwrap();
                let root = square
                    .sqrt_in(&field)
                    .unwrap()
                    .expect("a square has a root");
                assert_eq!(root.mul(&root).unwrap(), square);
                roots_found += 1;
                if let Some(root) = x.sqrt_in(&field).unwrap() {
                    assert_eq!(root.mul(&root).unwrap(), x);
                }
            }
        }
        assert_eq!(roots_found, 17 * 17);
    }

    #[test]
    fn display_forms_are_readable() {
        assert_eq!(format!("{}", number(2, rq(1, 2), ri(3))), "1/2 + 3*sqrt(2)");
        assert_eq!(format!("{}", QuadraticNumber::from_rational(ri(7))), "7");
        assert_eq!(format!("{}", surd(ri(2), ri(3))), "2*sqrt(3)");
        assert_eq!(format!("{}", Q5::from_ints(1, 2)), "1 + 2*sqrt(5)");
    }
}
