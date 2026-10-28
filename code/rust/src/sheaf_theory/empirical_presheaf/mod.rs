
mod descent;
mod lp;
mod model;
mod observer;
mod parity;
mod presheaf;

pub use descent::*;
pub use lp::*;
pub use model::*;
pub use observer::*;
pub use parity::*;
pub use presheaf::*;

use num_bigint::BigInt;
use num_rational::BigRational;
use tfqm_category_theory::finite_report_descent::DescentError;
use omega_solvers::solver_lp_standard_form::StandardLpError;
use thiserror::Error;

pub type Q = BigRational;

pub const AUTHORITY_EFFECT: &str = "None";
pub const DEFAULT_PIVOT_BUDGET: usize = 200_000;
pub const MAX_GLOBAL_ASSIGNMENTS: usize = 1 << 20;
pub const MAX_LP_ENTRIES: usize = 1 << 22;

fn q(n: i64) -> Q {
    Q::from_integer(BigInt::from(n))
}

fn qr(n: i64, d: i64) -> Q {
    Q::new(BigInt::from(n), BigInt::from(d))
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum EmpiricalError {
    #[error("a scenario needs between one and 64 measurements, each in some context")]
    CarrierSize,
    #[error("measurement {measurement} has arity below two")]
    Arity { measurement: usize },
    #[error("context {index} is empty, unsorted, repeated or outside the carrier")]
    Context { index: usize },
    #[error("context {index} is contained in context {other}; the cover lists maximal contexts")]
    NonMaximalContext { index: usize, other: usize },
    #[error("distribution count or length does not match the scenario")]
    Shape,
    #[error("distribution {context} has a negative entry or does not sum to one")]
    NotADistribution { context: usize },
    #[error("global assignment enumeration exceeds the declared limit {limit}")]
    EnumerationLimit { limit: usize },
    #[error("a dense LP matrix would exceed the declared limit of {limit} entries")]
    LpSizeLimit { limit: usize },
    #[error("descent refusal: {0}")]
    Descent(DescentError),
    #[error("LP refusal: {0}")]
    Lp(StandardLpError),
    #[error("certified Phi_1 refusal: {0}")]
    CertifiedPhi1(String),
    #[error("the sections at {from:#x} do not restrict into the sections at {into:#x}")]
    NotClosedUnderRestriction { from: u64, into: u64 },
    #[error("the model signals; marginalisation defines no restriction")]
    Signalling,
    #[error("the cover is not GYO-acyclic; no product-formula gluing is attempted")]
    NotAcyclic,
    #[error("the product formula does not reproduce distribution {context}")]
    ProductFormulaMismatch { context: usize },
    #[error("observer component `{0}` is undeclared; no receipt is issued")]
    UndeclaredObserverComponent(&'static str),
    #[error("observer component `{component}` declares `{declared}`, which this evaluator does not implement; no receipt is issued")]
    UnsupportedObserverComponent {
        component: &'static str,
        declared: String,
    },
    #[error("a parity cycle needs at least three contexts")]
    CycleTooShort,
    #[error("parity cycle target {index} is not 0 or 1")]
    ParityTarget { index: usize },
    #[error("rational denominator is zero")]
    ZeroDenominator,
}

impl From<DescentError> for EmpiricalError {
    fn from(error: DescentError) -> Self {
        EmpiricalError::Descent(error)
    }
}

impl From<StandardLpError> for EmpiricalError {
    fn from(error: StandardLpError) -> Self {
        EmpiricalError::Lp(error)
    }
}

pub fn positions(mask: u64) -> Vec<usize> {
    (0..64).filter(|&i| mask >> i & 1 == 1).collect()
}

pub fn mask(positions: &[usize]) -> Result<u64, EmpiricalError> {
    let mut bits = 0u64;
    for &position in positions {
        if position >= 64 {
            return Err(EmpiricalError::CarrierSize);
        }
        bits |= 1u64 << position;
    }
    Ok(bits)
}
