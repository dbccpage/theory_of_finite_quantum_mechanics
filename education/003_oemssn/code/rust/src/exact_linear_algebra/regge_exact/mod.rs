//! Exact rational primitives for 4-dimensional Regge calculus and Bianchi holonomies.
//!
//! Ported from `omega_linear_algebra::regge_exact`.
//! Scalar field: [`num_rational::BigRational`]. There is no `f32` or `f64`.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

pub mod bivector;
pub mod cayley_menger;
pub mod gaussian;
pub mod so4;

use num_bigint::BigInt;
use num_rational::BigRational;

pub use bivector::Bivector4;
pub use cayley_menger::{signed_volume_4, cayley_menger, CayleyMengerResult};
pub use so4::So4;

/// Refusal of an exact rational geometric primitive.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum ExactError {
    DivisionByZero,
    Singular,
    Dimension {
        expected: &'static str,
        got: u8,
    },
    NotOrthogonal,
    NotSpecial,
    Degenerate,
}

impl std::fmt::Display for ExactError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ExactError::DivisionByZero => write!(f, "Division by zero in exact rational arithmetic"),
            ExactError::Singular => write!(f, "Singular matrix encountered during exact solve"),
            ExactError::Dimension { expected, got } => {
                write!(f, "Dimension mismatch: expected {}, got {}", expected, got)
            }
            ExactError::NotOrthogonal => write!(f, "Matrix is not orthogonal over Q"),
            ExactError::NotSpecial => write!(f, "Matrix determinant is not 1 over Q"),
            ExactError::Degenerate => write!(f, "Degenerate geometric configuration"),
        }
    }
}

impl std::error::Error for ExactError {}

/// Integer as an exact rational.
pub fn q_i64(n: i64) -> BigRational {
    BigRational::from_integer(BigInt::from(n))
}

/// `n/d` in lowest terms. `d == 0` is [`ExactError::DivisionByZero`].
pub fn q_frac(n: i64, d: i64) -> Result<BigRational, ExactError> {
    if d == 0 {
        return Err(ExactError::DivisionByZero);
    }
    Ok(BigRational::new(BigInt::from(n), BigInt::from(d)))
}
