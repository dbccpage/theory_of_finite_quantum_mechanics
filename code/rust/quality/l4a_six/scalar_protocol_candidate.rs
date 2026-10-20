//! Staged checked scalar protocol. AuthorityEffect: None.
//! Every successful operation agrees with its declared exact arithmetic model.
//! Bounded representations return typed range refusal; they never wrap/clamp.
//! External implementations must uphold validation/closure and return typed
//! failures. Their algebraic laws remain explicit hypotheses, not derived facts.
use num_bigint::BigInt;
use num_integer::Integer;
use num_rational::{BigRational, Rational64};
use num_traits::{One, ToPrimitive, Zero};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Operation {
    Add,
    Subtract,
    Multiply,
    Negate,
    Invert,
    Divide,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ScalarError {
    ZeroDenominator,
    NegativeDenominator,
    NonReduced,
    DivisionByZero,
    OutOfRange {
        operation: Operation,
    },
    InvalidDomain {
        domain: &'static str,
        reason: &'static str,
    },
}
impl std::fmt::Display for ScalarError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}
impl std::error::Error for ScalarError {}
pub type Result<T> = std::result::Result<T, ScalarError>;

/// Partial exact arithmetic on admitted representations, with valid identities.
/// Validation is required even for queries such as zero testing. Implementors
/// must preserve their declared domain on success and report expected failures.
pub trait Semiring: Clone + PartialEq + std::fmt::Debug {
    fn zero() -> Self;
    fn one() -> Self;
    fn validate(&self) -> Result<()>;
    fn try_add(&self, rhs: &Self) -> Result<Self>;
    fn try_mul(&self, rhs: &Self) -> Result<Self>;
    fn try_is_zero(&self) -> Result<bool>;
}
pub trait Ring: Semiring {
    fn try_neg(&self) -> Result<Self>;
    fn try_sub(&self, rhs: &Self) -> Result<Self> {
        self.try_add(&rhs.try_neg()?)
    }
}
/// Field-model representations may refuse unrepresentable results. Integer
/// primitives are excluded: no truncating integer division is a field operation.
/// ```compile_fail
/// use tfqm_checked_scalar_trial::protocol::Field;
/// let _ = Field::try_inv(&1i64);
/// ```
pub trait Field: Ring {
    fn try_inv(&self) -> Result<Self>;
    fn try_div(&self, rhs: &Self) -> Result<Self> {
        self.try_mul(&rhs.try_inv()?)
    }
}
/// ```compile_fail
/// use tfqm_checked_scalar_trial::protocol::Semiring;
/// let _ = Semiring::try_add(&0.5f64, &0.5f64);
/// ```
pub trait ExactRing: Ring {}
pub trait CheckedExactField: Field + ExactRing {}
pub trait Involution: Field + ExactRing {
    fn try_conj(&self) -> Result<Self>;
}

pub fn validate_rational(value: &BigRational) -> Result<()> {
    if value.denom().is_zero() {
        return Err(ScalarError::ZeroDenominator);
    }
    if value.denom() < &BigInt::from(0) {
        return Err(ScalarError::NegativeDenominator);
    }
    if !value.numer().gcd(value.denom()).is_one() {
        return Err(ScalarError::NonReduced);
    }
    Ok(())
}
fn validate_pair<T: Semiring>(left: &T, right: &T) -> Result<()> {
    left.validate()?;
    right.validate()
}

impl Semiring for i64 {
    fn zero() -> Self {
        0
    }
    fn one() -> Self {
        1
    }
    fn validate(&self) -> Result<()> {
        Ok(())
    }
    fn try_add(&self, rhs: &Self) -> Result<Self> {
        self.checked_add(*rhs).ok_or(ScalarError::OutOfRange {
            operation: Operation::Add,
        })
    }
    fn try_mul(&self, rhs: &Self) -> Result<Self> {
        self.checked_mul(*rhs).ok_or(ScalarError::OutOfRange {
            operation: Operation::Multiply,
        })
    }
    fn try_is_zero(&self) -> Result<bool> {
        Ok(*self == 0)
    }
}
impl Ring for i64 {
    fn try_neg(&self) -> Result<Self> {
        self.checked_neg().ok_or(ScalarError::OutOfRange {
            operation: Operation::Negate,
        })
    }
    fn try_sub(&self, rhs: &Self) -> Result<Self> {
        self.checked_sub(*rhs).ok_or(ScalarError::OutOfRange {
            operation: Operation::Subtract,
        })
    }
}
// No ExactRing/Field implementation for bounded native integers.
impl Semiring for BigInt {
    fn zero() -> Self {
        <Self as Zero>::zero()
    }
    fn one() -> Self {
        <Self as One>::one()
    }
    fn validate(&self) -> Result<()> {
        Ok(())
    }
    fn try_add(&self, rhs: &Self) -> Result<Self> {
        Ok(self + rhs)
    }
    fn try_mul(&self, rhs: &Self) -> Result<Self> {
        Ok(self * rhs)
    }
    fn try_is_zero(&self) -> Result<bool> {
        Ok(Zero::is_zero(self))
    }
}
impl Ring for BigInt {
    fn try_neg(&self) -> Result<Self> {
        Ok(-self)
    }
    fn try_sub(&self, rhs: &Self) -> Result<Self> {
        Ok(self - rhs)
    }
}
impl ExactRing for BigInt {}

impl Semiring for BigRational {
    fn zero() -> Self {
        <Self as Zero>::zero()
    }
    fn one() -> Self {
        <Self as One>::one()
    }
    fn validate(&self) -> Result<()> {
        validate_rational(self)
    }
    fn try_add(&self, rhs: &Self) -> Result<Self> {
        validate_pair(self, rhs)?;
        Ok(self + rhs)
    }
    fn try_mul(&self, rhs: &Self) -> Result<Self> {
        validate_pair(self, rhs)?;
        Ok(self * rhs)
    }
    fn try_is_zero(&self) -> Result<bool> {
        self.validate()?;
        Ok(Zero::is_zero(self))
    }
}
impl Ring for BigRational {
    fn try_neg(&self) -> Result<Self> {
        self.validate()?;
        Ok(-self)
    }
    fn try_sub(&self, rhs: &Self) -> Result<Self> {
        validate_pair(self, rhs)?;
        Ok(self - rhs)
    }
}
impl Field for BigRational {
    fn try_inv(&self) -> Result<Self> {
        self.validate()?;
        if Zero::is_zero(self) {
            return Err(ScalarError::DivisionByZero);
        }
        Ok(self.recip())
    }
    fn try_div(&self, rhs: &Self) -> Result<Self> {
        validate_pair(self, rhs)?;
        if Zero::is_zero(rhs) {
            return Err(ScalarError::DivisionByZero);
        }
        Ok(self / rhs)
    }
}
impl ExactRing for BigRational {}
impl CheckedExactField for BigRational {}
impl Involution for BigRational {
    fn try_conj(&self) -> Result<Self> {
        self.validate()?;
        Ok(self.clone())
    }
}

/// Widen raw transport without performing bounded rational arithmetic. The
/// resulting raw BigRational must pass canonical-domain validation before use.
fn wide(value: &Rational64) -> BigRational {
    BigRational::new_raw(BigInt::from(*value.numer()), BigInt::from(*value.denom()))
}
fn narrow(value: BigRational, operation: Operation) -> Result<Rational64> {
    let numerator = value
        .numer()
        .to_i64()
        .ok_or(ScalarError::OutOfRange { operation })?;
    let denominator = value
        .denom()
        .to_i64()
        .ok_or(ScalarError::OutOfRange { operation })?;
    // Successful unbounded operations produce canonical positive-denominator Q.
    Ok(Rational64::new_raw(numerator, denominator))
}
impl Semiring for Rational64 {
    fn zero() -> Self {
        Rational64::from_integer(0)
    }
    fn one() -> Self {
        Rational64::from_integer(1)
    }
    fn validate(&self) -> Result<()> {
        wide(self).validate()
    }
    fn try_add(&self, rhs: &Self) -> Result<Self> {
        narrow(wide(self).try_add(&wide(rhs))?, Operation::Add)
    }
    fn try_mul(&self, rhs: &Self) -> Result<Self> {
        narrow(wide(self).try_mul(&wide(rhs))?, Operation::Multiply)
    }
    fn try_is_zero(&self) -> Result<bool> {
        wide(self).try_is_zero()
    }
}
impl Ring for Rational64 {
    fn try_neg(&self) -> Result<Self> {
        narrow(wide(self).try_neg()?, Operation::Negate)
    }
    fn try_sub(&self, rhs: &Self) -> Result<Self> {
        narrow(wide(self).try_sub(&wide(rhs))?, Operation::Subtract)
    }
}
impl Field for Rational64 {
    fn try_inv(&self) -> Result<Self> {
        narrow(wide(self).try_inv()?, Operation::Invert)
    }
    fn try_div(&self, rhs: &Self) -> Result<Self> {
        narrow(wide(self).try_div(&wide(rhs))?, Operation::Divide)
    }
}
impl ExactRing for Rational64 {}
impl CheckedExactField for Rational64 {}
impl Involution for Rational64 {
    fn try_conj(&self) -> Result<Self> {
        self.validate()?;
        Ok(*self)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn q(n: i64, d: i64) -> BigRational {
        BigRational::new(n.into(), d.into())
    }
    #[test]
    fn native_endpoints_match_wide_integer_models_without_panicking() {
        let values = [
            i64::MIN,
            i64::MIN + 1,
            -9,
            -1,
            0,
            1,
            9,
            i64::MAX - 1,
            i64::MAX,
        ];
        for a in values {
            for b in values {
                for (actual, exact, operation) in [
                    (a.try_add(&b), i128::from(a) + i128::from(b), Operation::Add),
                    (
                        a.try_sub(&b),
                        i128::from(a) - i128::from(b),
                        Operation::Subtract,
                    ),
                    (
                        a.try_mul(&b),
                        i128::from(a) * i128::from(b),
                        Operation::Multiply,
                    ),
                ] {
                    let expected =
                        i64::try_from(exact).map_err(|_| ScalarError::OutOfRange { operation });
                    assert_eq!(actual, expected);
                }
            }
            assert_eq!(
                a.try_neg(),
                i64::try_from(-i128::from(a)).map_err(|_| ScalarError::OutOfRange {
                    operation: Operation::Negate
                })
            );
        }
    }
    #[test]
    fn invalid_q_is_rejected_by_every_operand_role_and_query() {
        for bad in [
            BigRational::new_raw(1.into(), 0.into()),
            BigRational::new_raw(0.into(), 0.into()),
            BigRational::new_raw(1.into(), (-1).into()),
            BigRational::new_raw(2.into(), 4.into()),
        ] {
            assert!(bad.try_is_zero().is_err());
            assert!(bad.try_neg().is_err());
            assert!(bad.try_inv().is_err());
            assert!(bad.try_conj().is_err());
            for (a, b) in [(&bad, &q(0, 1)), (&q(0, 1), &bad)] {
                assert!(a.try_add(b).is_err());
                assert!(a.try_sub(b).is_err());
                assert!(a.try_mul(b).is_err());
                assert!(a.try_div(b).is_err());
            }
        }
        assert_eq!(q(0, 1).try_inv(), Err(ScalarError::DivisionByZero));
    }
    #[test]
    fn bounded_fractions_compute_in_q_then_refuse_unrepresentable_results() {
        let min = Rational64::new_raw(i64::MIN, 1);
        assert_eq!(
            min.try_neg(),
            Err(ScalarError::OutOfRange {
                operation: Operation::Negate
            })
        );
        assert_eq!(
            min.try_inv(),
            Err(ScalarError::OutOfRange {
                operation: Operation::Invert
            })
        );
        let max = Rational64::from_integer(i64::MAX);
        assert_eq!(
            max.try_add(&Rational64::from_integer(1)),
            Err(ScalarError::OutOfRange {
                operation: Operation::Add
            })
        );
        for n in -4..=4 {
            for d in 1..=4 {
                let a = Rational64::new(n, d);
                let b = Rational64::new(1, 3);
                assert_eq!(wide(&a.try_add(&b).unwrap()), q(n, d) + q(1, 3));
                assert_eq!(wide(&a.try_mul(&b).unwrap()), q(n, d) * q(1, 3));
                assert_eq!(wide(&a.try_div(&b).unwrap()), q(n, d) / q(1, 3));
            }
        }
        assert_eq!(
            Rational64::new_raw(1, 0).try_is_zero(),
            Err(ScalarError::ZeroDenominator)
        );
        assert_eq!(
            Rational64::from_integer(0).try_inv(),
            Err(ScalarError::DivisionByZero)
        );
    }
    // A distinct external-style implementation remains possible: the protocol
    // does not replace generic field support with a closed Q-only allowlist.
    #[derive(Debug, Clone, PartialEq, Eq)]
    struct F5(u8);
    impl Semiring for F5 {
        fn zero() -> Self {
            Self(0)
        }
        fn one() -> Self {
            Self(1)
        }
        fn validate(&self) -> Result<()> {
            if self.0 < 5 {
                Ok(())
            } else {
                Err(ScalarError::InvalidDomain {
                    domain: "F5",
                    reason: "noncanonical residue",
                })
            }
        }
        fn try_add(&self, rhs: &Self) -> Result<Self> {
            validate_pair(self, rhs)?;
            Ok(Self((self.0 + rhs.0) % 5))
        }
        fn try_mul(&self, rhs: &Self) -> Result<Self> {
            validate_pair(self, rhs)?;
            Ok(Self((self.0 * rhs.0) % 5))
        }
        fn try_is_zero(&self) -> Result<bool> {
            self.validate()?;
            Ok(self.0 == 0)
        }
    }
    impl Ring for F5 {
        fn try_neg(&self) -> Result<Self> {
            self.validate()?;
            Ok(Self((5 - self.0) % 5))
        }
    }
    impl Field for F5 {
        fn try_inv(&self) -> Result<Self> {
            self.validate()?;
            match self.0 {
                0 => Err(ScalarError::DivisionByZero),
                1 => Ok(Self(1)),
                2 => Ok(Self(3)),
                3 => Ok(Self(2)),
                _ => Ok(Self(4)),
            }
        }
    }
    impl ExactRing for F5 {}
    impl CheckedExactField for F5 {}
    #[test]
    fn generic_field_contract_preserves_modular_support_and_typed_refusal() {
        fn quotient<F: CheckedExactField>(a: &F, b: &F) -> Result<F> {
            a.try_div(b)
        }
        for a in 0..5u8 {
            for b in 0..5u8 {
                assert_eq!(F5(a).try_add(&F5(b)).unwrap(), F5((a + b) % 5));
                assert_eq!(F5(a).try_mul(&F5(b)).unwrap(), F5((a * b) % 5));
                if b == 0 {
                    assert_eq!(quotient(&F5(a), &F5(b)), Err(ScalarError::DivisionByZero));
                } else {
                    let result = quotient(&F5(a), &F5(b)).unwrap();
                    assert_eq!((result.0 * b) % 5, a);
                }
            }
        }
        assert!(quotient(&F5(5), &F5(1)).is_err());
        assert_eq!(quotient(&q(1, 2), &q(1, 3)).unwrap(), q(3, 2));
    }
}
