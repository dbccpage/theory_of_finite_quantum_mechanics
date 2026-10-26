//! Exact Scalar Traits and Protocols.
//!
//! Ported from `omega_linear_algebra::scalars`.
//!
//! AuthorityEffect: None.

use num_traits::{CheckedAdd, CheckedDiv, CheckedMul, CheckedSub, One, Zero};
use std::fmt;

// ============================================================================
// Semiring: additive commutative monoid + multiplicative monoid + distributivity
// ============================================================================

pub trait Semiring: Clone + PartialEq + fmt::Debug {
    fn zero() -> Self;
    fn one() -> Self;
    fn add(&self, rhs: &Self) -> Self;
    fn mul(&self, rhs: &Self) -> Self;
    fn is_zero(&self) -> bool;
}

// ============================================================================
// Ring: Semiring + additive inverse
// ============================================================================

pub trait Ring: Semiring {
    fn neg(&self) -> Self;

    fn sub(&self, other: &Self) -> Self {
        self.add(&other.neg())
    }
}

// ============================================================================
// Field: Ring + multiplicative inverse (for nonzero elements)
// ============================================================================

pub trait Field: Ring {
    /// Multiplicative inverse. Returns None if zero or non-invertible.
    fn try_inv(&self) -> Option<Self>;

    fn try_div(&self, other: &Self) -> Option<Self> {
        let inv = other.try_inv()?;
        Some(self.mul(&inv))
    }
}

// ============================================================================
// Sealed Checked Exact Field Protocol
// ============================================================================

mod sealed {
    pub trait Sealed {}
    impl Sealed for num_rational::Rational64 {}
    impl Sealed for num_rational::BigRational {}
}

pub trait CheckedExactField:
    sealed::Sealed
    + Clone
    + Eq
    + Zero
    + One
    + CheckedAdd
    + CheckedSub
    + CheckedMul
    + CheckedDiv
    + fmt::Debug
    + 'static
{
    fn checked_neg(&self) -> Option<Self>;
}

impl CheckedExactField for num_rational::Rational64 {
    fn checked_neg(&self) -> Option<Self> {
        Self::zero().checked_sub(self)
    }
}

impl CheckedExactField for num_rational::BigRational {
    fn checked_neg(&self) -> Option<Self> {
        Some(-self.clone())
    }
}

// ============================================================================
// Exact rationals in the scalar tower
// ============================================================================

impl Semiring for num_rational::BigRational {
    fn zero() -> Self {
        <Self as Zero>::zero()
    }
    fn one() -> Self {
        <Self as One>::one()
    }
    fn add(&self, rhs: &Self) -> Self {
        self + rhs
    }
    fn mul(&self, rhs: &Self) -> Self {
        self * rhs
    }
    fn is_zero(&self) -> bool {
        <Self as Zero>::is_zero(self)
    }
}

impl Ring for num_rational::BigRational {
    fn neg(&self) -> Self {
        -self
    }
}

impl Field for num_rational::BigRational {
    fn try_inv(&self) -> Option<Self> {
        if <Self as Zero>::is_zero(self) {
            None
        } else {
            Some(self.recip())
        }
    }
}

pub trait ExactRing: Ring {}
impl ExactRing for num_rational::BigRational {}

impl Semiring for i64 {
    fn zero() -> Self {
        0
    }
    fn one() -> Self {
        1
    }
    fn add(&self, rhs: &Self) -> Self {
        *self + *rhs
    }
    fn mul(&self, rhs: &Self) -> Self {
        *self * *rhs
    }
    fn is_zero(&self) -> bool {
        *self == 0
    }
}

impl Ring for i64 {
    fn neg(&self) -> Self {
        -*self
    }
}

impl ExactRing for i64 {}
