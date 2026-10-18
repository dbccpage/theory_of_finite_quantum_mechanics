//! Refusals of the finite-carrier, simplex and stochastic-map layer.
//!
//! Every constructor and operation in [`crate::finite_set`], [`crate::simplex`],
//! [`crate::stochastic_map`] and [`crate::markov_chain`] reports a bad argument as one of
//! these values. None of them panics on caller data, and none is a string: a caller can tell
//! a shape refusal from a normalisation refusal from a limit refusal by matching.
//!
//! AuthorityEffect: None.

use linear_algebra::backend::basic_matrix::MatrixError;
use omega_number_theory::rational::Rational;

/// Construction and operation refusals for `Fin n`, rational simplices and stochastic maps.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ClassicalShadowError {
    /// A carrier, source or target must have at least one point.
    #[error("a finite carrier needs at least one point")]
    ZeroCardinality,
    /// A vector, row or image list has the wrong length.
    #[error("expected {expected} entries, found {actual}")]
    DimensionMismatch { expected: usize, actual: usize },
    /// Sizes that must agree (a source against a target, two simplices) do not.
    #[error("sizes {left} and {right} do not match")]
    ShapeMismatch { left: usize, right: usize },
    /// Entry `index` is negative. For a matrix the index is row-major, `row * cols + col`.
    #[error("entry {index} is negative")]
    NegativeEntry { index: usize },
    /// A caller supplied a raw rational with a zero or negative denominator.
    #[error("entry {index} has a nonpositive rational denominator")]
    InvalidDenominator { index: usize },
    /// The masses do not sum to exactly one.
    #[error("the masses sum to {sum}, not one")]
    NotNormalized { sum: Rational },
    /// A row of a stochastic matrix does not sum to exactly one.
    #[error("row {row} sums to {sum}, not one")]
    RowNotNormalized { row: usize, sum: Rational },
    /// No entries were given where at least one is needed.
    #[error("no entries were given")]
    Empty,
    /// An index lies outside `0..bound`.
    #[error("index {index} is outside 0..{bound}")]
    IndexOutOfRange { index: usize, bound: usize },
    /// The list is not a bijection of `0..n`; `position` is the first entry that repeats an
    /// earlier image or leaves the range.
    #[error("the images are not a permutation: position {position} repeats or leaves the range")]
    NotAPermutation { position: usize },
    /// The product of two sizes does not fit in `usize`.
    #[error("the product of sizes {left} and {right} does not fit in usize")]
    SizeOverflow { left: usize, right: usize },
    /// Weights that must be normalised sum to zero.
    #[error("the weights sum to zero, so they cannot be normalised")]
    ZeroTotalWeight,
    /// A Bayesian inverse needs every target state to carry positive mass.
    #[error("target state {index} has zero mass, so its posterior is undetermined")]
    ZeroMass { index: usize },
    /// A bounded operation was asked for more than its declared limit.
    #[error("{what} {requested} exceeds the limit {limit}")]
    LimitExceeded {
        what: &'static str,
        requested: usize,
        limit: usize,
    },
    /// The dense matrix storage of `omega_linear_algebra` refused a shape.
    #[error("matrix storage refusal: {0}")]
    Matrix(#[from] MatrixError),
}
