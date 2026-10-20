use linear_algebra::backend::basic_matrix::MatrixError;
use thiserror::Error;

use crate::braided::BraidedDefect;
use crate::fusion_category::CategoryDefect;
use crate::fusion_ring::RingDefect;
use crate::modular::ModularDefect;

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum FusionError {
    #[error(transparent)]
    ExactField(#[from] linear_algebra::exact_field::ExactFieldError),
    #[error(transparent)]
    AlgebraicReal(#[from] omega_number_theory::algebraic_real::AlgebraicRealError),
    #[error(transparent)]
    Scalar(#[from] omega_number_theory::scalar::ScalarError),
    #[error("rank {rank} is outside 1..={max}")]
    RankOutOfRange { rank: usize, max: usize },

    #[error("a fusion table of rank {rank} needs {expected} entries, got {got}")]
    TableShape {
        rank: usize,
        expected: usize,
        got: usize,
    },

    #[error("expected {expected} {what}, got {got}")]
    ListLength {
        what: &'static str,
        expected: usize,
        got: usize,
    },

    #[error("label {label} is outside 0..{rank}")]
    Label { label: usize, rank: usize },

    #[error("fusion ring: {0}")]
    Ring(RingDefect),

    #[error("fusion category: {0}")]
    Category(CategoryDefect),

    #[error("braided fusion category: {0}")]
    Braided(BraidedDefect),

    #[error("modular data: {0}")]
    Modular(ModularDefect),

    #[error("arithmetic overflow while {context}")]
    Overflow { context: &'static str },

    #[error("{what} of size {requested} exceeds the budget {limit}")]
    Budget {
        what: &'static str,
        requested: u128,
        limit: u128,
    },

    #[error("matrix storage: {0}")]
    Matrix(#[from] MatrixError),

    #[error("{operation}: incompatible shapes {left:?} and {right:?}")]
    Shape {
        operation: &'static str,
        left: (usize, usize),
        right: (usize, usize),
    },

    #[error("{operation} needs a square matrix, got {rows}x{cols}")]
    NotSquare {
        operation: &'static str,
        rows: usize,
        cols: usize,
    },

    #[error("{context}: the matrix is singular")]
    Singular { context: &'static str },

    #[error("{context}: no multiplicative inverse")]
    NoInverse { context: &'static str },

    #[error("the coefficient field does not contain {needed}")]
    FieldTooSmall { needed: &'static str },

    #[error("{what} is not {expected} in this field")]
    NotInSubfield {
        what: &'static str,
        expected: &'static str,
    },

    #[error("polynomial: {0}")]
    Polynomial(&'static str),

    #[error("the sign of {context} could not be decided exactly")]
    SignUndecided { context: &'static str },

    #[error("internal inconsistency: {context}")]
    Inconsistent { context: &'static str },
}

impl From<RingDefect> for FusionError {
    fn from(defect: RingDefect) -> Self {
        Self::Ring(defect)
    }
}

impl From<CategoryDefect> for FusionError {
    fn from(defect: CategoryDefect) -> Self {
        Self::Category(defect)
    }
}

impl From<BraidedDefect> for FusionError {
    fn from(defect: BraidedDefect) -> Self {
        Self::Braided(defect)
    }
}

impl From<ModularDefect> for FusionError {
    fn from(defect: ModularDefect) -> Self {
        Self::Modular(defect)
    }
}
