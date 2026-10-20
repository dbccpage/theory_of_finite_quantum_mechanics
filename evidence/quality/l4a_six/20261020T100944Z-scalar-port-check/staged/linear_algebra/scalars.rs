use num_bigint::BigInt;
use num_rational::BigRational;
use serde::{Deserialize, Serialize};

pub type Q = BigRational;

// Digest frames use u64 lengths. Reject unsupported wider-pointer platforms
// at compile time so every usize length/dimension cast in the hash consumers fits.
const _: () = assert!(usize::BITS <= u64::BITS);

#[inline]
pub fn q(n: i64) -> Q {
    BigRational::from_integer(BigInt::from(n))
}

#[inline]
pub fn qr(n: i64, d: i64) -> Result<Q, RationalConstructionError> {
    if d == 0 {
        return Err(RationalConstructionError::ZeroDenominator);
    }
    Ok(BigRational::new(BigInt::from(n), BigInt::from(d)))
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, thiserror::Error)]
pub enum RationalConstructionError {
    #[error("rational denominator cannot be zero")]
    ZeroDenominator,
    #[error("canonical rational denominator must be positive")]
    NegativeDenominator,
    #[error("canonical rational must already be reduced")]
    NonReduced,
}

/// Validate the canonical Q domain without performing arithmetic on an invalid
/// denominator. Raw construction does not establish this invariant.
pub fn validate_rational(value: &Q) -> Result<(), RationalConstructionError> {
    if num_traits::Zero::is_zero(value.denom()) {
        return Err(RationalConstructionError::ZeroDenominator);
    }
    if value.denom() < &BigInt::from(0) {
        return Err(RationalConstructionError::NegativeDenominator);
    }
    if !value.numer().gcd(value.denom()).is_one() {
        return Err(RationalConstructionError::NonReduced);
    }
    Ok(())
}

/// Immutable Q(i); constructors and decoding admit both canonical components.
/// No larger scalar extension or bounded integer rational is admitted.
/// ```compile_fail
/// use theory_of_finite_qm::linear_algebra::scalars::{q, GaussianRational};
/// let _ = GaussianRational { real: q(0), imag: q(0) };
/// ```
/// ```
/// use theory_of_finite_qm::linear_algebra::scalars::{q, Field, GaussianRational};
/// let value = GaussianRational::new(q(1), q(1))?;
/// assert!(value.try_inv().is_ok());
/// assert_eq!(value.real(), &q(1));
/// # Ok::<(), theory_of_finite_qm::linear_algebra::scalars::RationalConstructionError>(())
/// ```
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize)]
pub struct GaussianRational {
    real: Q,
    imag: Q,
}

impl GaussianRational {
    pub fn new(real: Q, imag: Q) -> Result<Self, RationalConstructionError> {
        validate_rational(&real)?;
        validate_rational(&imag)?;
        Ok(Self { real, imag })
    }

    pub fn real(&self) -> &Q {
        &self.real
    }

    pub fn imag(&self) -> &Q {
        &self.imag
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

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct GaussianWire {
    real: Q,
    imag: Q,
}

impl<'de> Deserialize<'de> for GaussianRational {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        let wire = GaussianWire::deserialize(deserializer)?;
        Self::new(wire.real, wire.imag).map_err(serde::de::Error::custom)
    }
}

// Staged checked scalar protocol. AuthorityEffect: None.
// Every successful operation agrees with its declared exact arithmetic model.
// Bounded representations return typed range refusal; they never wrap/clamp.
// External implementations must uphold validation/closure and return typed
// failures. Their algebraic laws remain explicit hypotheses, not derived facts.
use num_integer::Integer;
use num_rational::Rational64;
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
    /// A nonzero admitted value was refused by the provider inverse protocol.
    /// This is a backend refusal, not a claim that its domain is invalid.
    InversionRefused {
        domain: &'static str,
    },
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
pub type ScalarResult<T> = std::result::Result<T, ScalarError>;

/// Partial exact arithmetic on admitted representations, with valid identities.
/// Validation is required even for queries such as zero testing. Implementors
/// must preserve their declared domain on success and report expected failures.
pub trait Semiring: Clone + PartialEq + std::fmt::Debug {
    fn zero() -> Self;
    fn one() -> Self;
    fn validate(&self) -> ScalarResult<()>;
    fn try_add(&self, rhs: &Self) -> ScalarResult<Self>;
    fn try_mul(&self, rhs: &Self) -> ScalarResult<Self>;
    fn try_is_zero(&self) -> ScalarResult<bool>;
}
pub trait Ring: Semiring {
    fn try_neg(&self) -> ScalarResult<Self>;
    fn try_sub(&self, rhs: &Self) -> ScalarResult<Self> {
        validate_pair(self, rhs)?;
        self.try_add(&rhs.try_neg()?)
    }
}
/// Field-model representations may refuse unrepresentable results. Integer
/// primitives are excluded: no truncating integer division is a field operation.
/// ```compile_fail
/// use theory_of_finite_qm::linear_algebra::scalars::Field;
/// let _ = Field::try_inv(&1i64);
/// ```
pub trait Field: Ring {
    fn try_inv(&self) -> ScalarResult<Self>;
    fn try_div(&self, rhs: &Self) -> ScalarResult<Self> {
        validate_pair(self, rhs)?;
        self.try_mul(&rhs.try_inv()?)
    }
}
/// ```compile_fail
/// use theory_of_finite_qm::linear_algebra::scalars::Semiring;
/// let _ = Semiring::try_add(&0.5f64, &0.5f64);
/// ```
pub trait ExactRing: Ring {}
pub trait CheckedExactField: Field + ExactRing {}
pub trait Involution: Field + ExactRing {
    fn try_conj(&self) -> ScalarResult<Self>;
}

fn validate_pair<T: Semiring>(left: &T, right: &T) -> ScalarResult<()> {
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
    fn validate(&self) -> ScalarResult<()> {
        Ok(())
    }
    fn try_add(&self, rhs: &Self) -> ScalarResult<Self> {
        self.checked_add(*rhs).ok_or(ScalarError::OutOfRange {
            operation: Operation::Add,
        })
    }
    fn try_mul(&self, rhs: &Self) -> ScalarResult<Self> {
        self.checked_mul(*rhs).ok_or(ScalarError::OutOfRange {
            operation: Operation::Multiply,
        })
    }
    fn try_is_zero(&self) -> ScalarResult<bool> {
        Ok(*self == 0)
    }
}
impl Ring for i64 {
    fn try_neg(&self) -> ScalarResult<Self> {
        self.checked_neg().ok_or(ScalarError::OutOfRange {
            operation: Operation::Negate,
        })
    }
    fn try_sub(&self, rhs: &Self) -> ScalarResult<Self> {
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
    fn validate(&self) -> ScalarResult<()> {
        Ok(())
    }
    fn try_add(&self, rhs: &Self) -> ScalarResult<Self> {
        Ok(self + rhs)
    }
    fn try_mul(&self, rhs: &Self) -> ScalarResult<Self> {
        Ok(self * rhs)
    }
    fn try_is_zero(&self) -> ScalarResult<bool> {
        Ok(Zero::is_zero(self))
    }
}
impl Ring for BigInt {
    fn try_neg(&self) -> ScalarResult<Self> {
        Ok(-self)
    }
    fn try_sub(&self, rhs: &Self) -> ScalarResult<Self> {
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
    fn validate(&self) -> ScalarResult<()> {
        validate_rational(self).map_err(Into::into)
    }
    fn try_add(&self, rhs: &Self) -> ScalarResult<Self> {
        validate_pair(self, rhs)?;
        Ok(self + rhs)
    }
    fn try_mul(&self, rhs: &Self) -> ScalarResult<Self> {
        validate_pair(self, rhs)?;
        Ok(self * rhs)
    }
    fn try_is_zero(&self) -> ScalarResult<bool> {
        self.validate()?;
        Ok(Zero::is_zero(self))
    }
}
impl Ring for BigRational {
    fn try_neg(&self) -> ScalarResult<Self> {
        self.validate()?;
        Ok(-self)
    }
    fn try_sub(&self, rhs: &Self) -> ScalarResult<Self> {
        validate_pair(self, rhs)?;
        Ok(self - rhs)
    }
}
impl Field for BigRational {
    fn try_inv(&self) -> ScalarResult<Self> {
        self.validate()?;
        if Zero::is_zero(self) {
            return Err(ScalarError::DivisionByZero);
        }
        Ok(self.recip())
    }
    fn try_div(&self, rhs: &Self) -> ScalarResult<Self> {
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
    fn try_conj(&self) -> ScalarResult<Self> {
        self.validate()?;
        Ok(self.clone())
    }
}

/// Widen raw transport without performing bounded rational arithmetic. The
/// resulting raw BigRational must pass canonical-domain validation before use.
fn wide(value: &Rational64) -> BigRational {
    BigRational::new_raw(BigInt::from(*value.numer()), BigInt::from(*value.denom()))
}
fn narrow(value: BigRational, operation: Operation) -> ScalarResult<Rational64> {
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
    fn validate(&self) -> ScalarResult<()> {
        wide(self).validate()
    }
    fn try_add(&self, rhs: &Self) -> ScalarResult<Self> {
        narrow(wide(self).try_add(&wide(rhs))?, Operation::Add)
    }
    fn try_mul(&self, rhs: &Self) -> ScalarResult<Self> {
        narrow(wide(self).try_mul(&wide(rhs))?, Operation::Multiply)
    }
    fn try_is_zero(&self) -> ScalarResult<bool> {
        wide(self).try_is_zero()
    }
}
impl Ring for Rational64 {
    fn try_neg(&self) -> ScalarResult<Self> {
        narrow(wide(self).try_neg()?, Operation::Negate)
    }
    fn try_sub(&self, rhs: &Self) -> ScalarResult<Self> {
        narrow(wide(self).try_sub(&wide(rhs))?, Operation::Subtract)
    }
}
impl Field for Rational64 {
    fn try_inv(&self) -> ScalarResult<Self> {
        narrow(wide(self).try_inv()?, Operation::Invert)
    }
    fn try_div(&self, rhs: &Self) -> ScalarResult<Self> {
        narrow(wide(self).try_div(&wide(rhs))?, Operation::Divide)
    }
}
impl ExactRing for Rational64 {}
impl CheckedExactField for Rational64 {}
impl Involution for Rational64 {
    fn try_conj(&self) -> ScalarResult<Self> {
        self.validate()?;
        Ok(*self)
    }
}

impl From<RationalConstructionError> for ScalarError {
    fn from(error: RationalConstructionError) -> Self {
        match error {
            RationalConstructionError::ZeroDenominator => Self::ZeroDenominator,
            RationalConstructionError::NegativeDenominator => Self::NegativeDenominator,
            RationalConstructionError::NonReduced => Self::NonReduced,
        }
    }
}
impl Semiring for GaussianRational {
    fn zero() -> Self {
        Self {
            real: <Q as Zero>::zero(),
            imag: <Q as Zero>::zero(),
        }
    }
    fn one() -> Self {
        Self {
            real: <Q as One>::one(),
            imag: <Q as Zero>::zero(),
        }
    }
    fn validate(&self) -> ScalarResult<()> {
        Ok(())
    }
    fn try_add(&self, rhs: &Self) -> ScalarResult<Self> {
        Ok(Self {
            real: &self.real + &rhs.real,
            imag: &self.imag + &rhs.imag,
        })
    }
    fn try_mul(&self, rhs: &Self) -> ScalarResult<Self> {
        Ok(Self {
            real: &self.real * &rhs.real - &self.imag * &rhs.imag,
            imag: &self.real * &rhs.imag + &self.imag * &rhs.real,
        })
    }
    fn try_is_zero(&self) -> ScalarResult<bool> {
        Ok(Zero::is_zero(&self.real) && Zero::is_zero(&self.imag))
    }
}
impl Ring for GaussianRational {
    fn try_neg(&self) -> ScalarResult<Self> {
        Ok(Self {
            real: -&self.real,
            imag: -&self.imag,
        })
    }
    fn try_sub(&self, rhs: &Self) -> ScalarResult<Self> {
        Ok(Self {
            real: &self.real - &rhs.real,
            imag: &self.imag - &rhs.imag,
        })
    }
}
impl Field for GaussianRational {
    fn try_inv(&self) -> ScalarResult<Self> {
        let norm = self.norm_sq();
        if Zero::is_zero(&norm) {
            return Err(ScalarError::DivisionByZero);
        }
        Ok(Self {
            real: &self.real / &norm,
            imag: -&self.imag / &norm,
        })
    }
}
impl ExactRing for GaussianRational {}
impl CheckedExactField for GaussianRational {}
impl Involution for GaussianRational {
    fn try_conj(&self) -> ScalarResult<Self> {
        Ok(Self {
            real: self.real.clone(),
            imag: -&self.imag,
        })
    }
}

pub fn hash_bigint(hasher: &mut blake3::Hasher, value: &BigInt) {
    let bytes = value.to_signed_bytes_le();
    hasher.update(&(bytes.len() as u64).to_le_bytes());
    hasher.update(&bytes);
}

/// Hash the normalized mathematical rational using the existing byte format.
/// Unlike Gaussian admission, this boundary accepts finite noncanonical raw
/// values and normalizes them. A zero denominator fails before any hasher write.
pub fn hash_rational(
    hasher: &mut blake3::Hasher,
    val: &Q,
) -> Result<(), RationalConstructionError> {
    if num_traits::Zero::is_zero(val.denom()) {
        return Err(RationalConstructionError::ZeroDenominator);
    }
    let reduced = val.reduced();
    hash_bigint(hasher, reduced.numer());
    hash_bigint(hasher, reduced.denom());
    Ok(())
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
        fn validate(&self) -> ScalarResult<()> {
            if self.0 < 5 {
                Ok(())
            } else {
                Err(ScalarError::InvalidDomain {
                    domain: "F5",
                    reason: "noncanonical residue",
                })
            }
        }
        fn try_add(&self, rhs: &Self) -> ScalarResult<Self> {
            validate_pair(self, rhs)?;
            Ok(Self((self.0 + rhs.0) % 5))
        }
        fn try_mul(&self, rhs: &Self) -> ScalarResult<Self> {
            validate_pair(self, rhs)?;
            Ok(Self((self.0 * rhs.0) % 5))
        }
        fn try_is_zero(&self) -> ScalarResult<bool> {
            self.validate()?;
            Ok(self.0 == 0)
        }
    }
    impl Ring for F5 {
        fn try_neg(&self) -> ScalarResult<Self> {
            self.validate()?;
            Ok(Self((5 - self.0) % 5))
        }
    }
    impl Field for F5 {
        fn try_inv(&self) -> ScalarResult<Self> {
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
        fn quotient<F: CheckedExactField>(a: &F, b: &F) -> ScalarResult<F> {
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

#[cfg(test)]
mod gaussian_migration_challenges {
    use super::*;
    #[test]
    fn all_integer_pair_operations_match_coordinate_oracles() {
        for a in -3..=3 {
            for b in -3..=3 {
                for c in -3..=3 {
                    for d in -3..=3 {
                        let left = GaussianRational::from_integers(a, b);
                        let right = GaussianRational::from_integers(c, d);
                        let product = left.try_mul(&right).unwrap();
                        assert_eq!(product.real(), &q(a * c - b * d));
                        assert_eq!(product.imag(), &q(a * d + b * c));
                        let sum = left.try_add(&right).unwrap();
                        assert_eq!(sum.real(), &q(a + c));
                        assert_eq!(sum.imag(), &q(b + d));
                        let norm = a * a + b * b;
                        if norm == 0 {
                            assert_eq!(left.try_inv(), Err(ScalarError::DivisionByZero));
                        } else {
                            let inverse = left.try_inv().unwrap();
                            assert_eq!(inverse.real(), &qr(a, norm).unwrap());
                            assert_eq!(inverse.imag(), &qr(-b, norm).unwrap());
                        }
                        assert_eq!(left.try_conj().unwrap().imag(), &q(-b));
                    }
                }
            }
        }
    }
    #[test]
    fn construction_decoding_and_valid_hash_frames_remain_checked() {
        let raw = Q::new_raw(1.into(), 0.into());
        assert_eq!(
            GaussianRational::new(raw, q(0)),
            Err(RationalConstructionError::ZeroDenominator)
        );
        let valid = GaussianRational::from_integers(1, 2);
        let bytes = serde_json::to_vec(&valid).unwrap();
        assert_eq!(
            serde_json::from_slice::<GaussianRational>(&bytes).unwrap(),
            valid
        );
        let mut h = blake3::Hasher::new();
        hash_rational(&mut h, &Q::new_raw(2.into(), 4.into())).unwrap();
        let mut canonical = blake3::Hasher::new();
        hash_rational(&mut canonical, &qr(1, 2).unwrap()).unwrap();
        assert_eq!(h.finalize(), canonical.finalize());
    }
}
