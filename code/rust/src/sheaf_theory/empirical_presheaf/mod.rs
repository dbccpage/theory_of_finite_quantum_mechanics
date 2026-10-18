//! Finite empirical presheaves over a context poset, with exact LP witnesses.
//!
//! **AuthorityEffect:** None. Not PROVED; not GlobalGreen.
//!
//! A measurement scenario fixes finitely many measurements with finite
//! outcome sets and a cover by maximal contexts. An empirical model assigns
//! to every maximal context a probability distribution over its joint
//! outcomes (Abramsky–Brandenburger, 2011). Restriction is marginalisation,
//! so the model is a presheaf on the down-closure of the cover exactly when
//! it is no-signalling, and that condition is the Čech 0-cocycle condition
//! `delta0(e) = 0` computed here.
//!
//! Four exact, replayable decisions are provided:
//!
//! 1. a global section of the support presheaf (an assignment consistent with
//!    every support) exists or not — strong contextuality is its absence;
//! 2. the noncontextual fraction LP (Abramsky–Barbosa–Mansfield) with its
//!    Bell-functional dual, certified by the independent primal/dual replay of
//!    `omega_solvers::solver_lp_standard_form`;
//! 3. the L1 distance `min_p ||A p - e||_1` from the noncontextual polytope,
//!    with a dual witness of sup-norm at most one and zero duality gap, and
//!    the quotient evaluator `Phi_1([omega]) = min_alpha ||omega - delta0
//!    alpha||_1` on Čech 1-cochains, delegated to the certified solver of
//!    `omega_solvers` and replayed by `omega_functional`, which owns `Phi_1`;
//! 4. the descent bridge to `omega_category_theory::finite_report_descent`:
//!    locally admissible assignments form a report presheaf whose
//!    `DescentOutcome::NoGlobalExtension` fibers are the local-green,
//!    global-red events, and the Vorob'ev product-formula gluing on a
//!    GYO-acyclic cover.
//!
//! Every receipt carries `authority_effect: "None"`: the evaluator reports a
//! defect and a witness; it never admits or authorises anything.

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
use omega_category_theory::finite_report_descent::DescentError;
use omega_solvers::solver_lp_standard_form::StandardLpError;
use thiserror::Error;

/// Exact rational scalar shared with the LP solver.
pub type Q = BigRational;

/// Every receipt of this module carries this value and nothing else.
pub const AUTHORITY_EFFECT: &str = "None";
/// Declared simplex pivot budget for the exact LPs of this module.
pub const DEFAULT_PIVOT_BUDGET: usize = 200_000;
/// Declared enumeration ceiling for global assignments. Every joint-outcome
/// count of this module is folded with checked multiplication against it, so
/// an oversized carrier is refused as a typed resource record before any
/// vector of that length is allocated or any assignment is enumerated.
pub const MAX_GLOBAL_ASSIGNMENTS: usize = 1 << 20;
/// Declared ceiling on the entries of any dense rational matrix this module
/// allocates (incidence, noncontextual-fraction, L1 and signed-section forms).
/// The pivot budget bounds simplex work, not matrix memory, so this is a
/// separate record.
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

/// Positions set by a bitmask, in increasing order.
pub fn positions(mask: u64) -> Vec<usize> {
    (0..64).filter(|&i| mask >> i & 1 == 1).collect()
}

/// Bitmask of a position list. A position that does not fit in a `u64`
/// is [`EmpiricalError::CarrierSize`] rather than a shift that panics.
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
