
use linear_algebra::backend::basic_matrix::MatrixError;
use omega_number_theory::rational::Rational;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ClassicalShadowError {
    #[error("a finite carrier needs at least one point")]
    ZeroCardinality,
    #[error("expected {expected} entries, found {actual}")]
    DimensionMismatch { expected: usize, actual: usize },
    #[error("sizes {left} and {right} do not match")]
    ShapeMismatch { left: usize, right: usize },
    #[error("entry {index} is negative")]
    NegativeEntry { index: usize },
    #[error("entry {index} has a nonpositive rational denominator")]
    InvalidDenominator { index: usize },
    #[error("the masses sum to {sum}, not one")]
    NotNormalized { sum: Rational },
    #[error("row {row} sums to {sum}, not one")]
    RowNotNormalized { row: usize, sum: Rational },
    #[error("no entries were given")]
    Empty,
    #[error("index {index} is outside 0..{bound}")]
    IndexOutOfRange { index: usize, bound: usize },
    #[error("the images are not a permutation: position {position} repeats or leaves the range")]
    NotAPermutation { position: usize },
    #[error("the product of sizes {left} and {right} does not fit in usize")]
    SizeOverflow { left: usize, right: usize },
    #[error("the weights sum to zero, so they cannot be normalised")]
    ZeroTotalWeight,
    #[error("target state {index} has zero mass, so its posterior is undetermined")]
    ZeroMass { index: usize },
    #[error("{what} {requested} exceeds the limit {limit}")]
    LimitExceeded {
        what: &'static str,
        requested: usize,
        limit: usize,
    },
    #[error("matrix storage refusal: {0}")]
    Matrix(#[from] MatrixError),
}
