//! Typed refusals of the fusion-category crate.
//!
//! No routine in this crate panics on caller data: every malformed table, symbol
//! array, index or request is one of these variants. The variants carry indices,
//! sizes and static names only, never field elements, so the type does not depend on
//! the coefficient field and can be compared and cloned freely. Routines that also
//! report the offending values (for example the pentagon and hexagon defect lists)
//! return their own generic defect records.
//!
//! AuthorityEffect: None.

use linear_algebra::backend::basic_matrix::MatrixError;
use thiserror::Error;

use crate::braided::BraidedDefect;
use crate::fusion_category::CategoryDefect;
use crate::fusion_ring::RingDefect;
use crate::modular::ModularDefect;

/// Refusals of the fusion-category routines.
#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum FusionError {
    /// Refusal from the canonical exact linear algebra owner.
    #[error(transparent)]
    ExactField(#[from] linear_algebra::exact_field::ExactFieldError),
    /// Refusal from canonical algebraic root certification.
    #[error(transparent)]
    AlgebraicReal(#[from] omega_number_theory::algebraic_real::AlgebraicRealError),
    #[error(transparent)]
    Scalar(#[from] omega_number_theory::scalar::ScalarError),
    /// The rank is zero or above the supported maximum.
    #[error("rank {rank} is outside 1..={max}")]
    RankOutOfRange { rank: usize, max: usize },

    /// A flat multiplicity array of the wrong length.
    #[error("a fusion table of rank {rank} needs {expected} entries, got {got}")]
    TableShape {
        rank: usize,
        expected: usize,
        got: usize,
    },

    /// A list of names or duals of the wrong length.
    #[error("expected {expected} {what}, got {got}")]
    ListLength {
        what: &'static str,
        expected: usize,
        got: usize,
    },

    /// A label outside `0..rank`.
    #[error("label {label} is outside 0..{rank}")]
    Label { label: usize, rank: usize },

    /// A fusion-ring law fails.
    #[error("fusion ring: {0}")]
    Ring(RingDefect),

    /// A law of a fusion category (F-symbols) fails.
    #[error("fusion category: {0}")]
    Category(CategoryDefect),

    /// A law of a braided fusion category (R-symbols, twists) fails.
    #[error("braided fusion category: {0}")]
    Braided(BraidedDefect),

    /// A law of modular data fails.
    #[error("modular data: {0}")]
    Modular(ModularDefect),

    /// Integer arithmetic would overflow; the named operation was not performed.
    #[error("arithmetic overflow while {context}")]
    Overflow { context: &'static str },

    /// A request whose size exceeds the declared budget.
    #[error("{what} of size {requested} exceeds the budget {limit}")]
    Budget {
        what: &'static str,
        requested: u128,
        limit: u128,
    },

    /// Storage or shape refusal from the matrix type.
    #[error("matrix storage: {0}")]
    Matrix(#[from] MatrixError),

    /// Two matrices whose shapes the operation cannot combine.
    #[error("{operation}: incompatible shapes {left:?} and {right:?}")]
    Shape {
        operation: &'static str,
        left: (usize, usize),
        right: (usize, usize),
    },

    /// A square-matrix operation applied to a non-square matrix.
    #[error("{operation} needs a square matrix, got {rows}x{cols}")]
    NotSquare {
        operation: &'static str,
        rows: usize,
        cols: usize,
    },

    /// A matrix without an inverse.
    #[error("{context}: the matrix is singular")]
    Singular { context: &'static str },

    /// A nonzero element of the scalar type without an inverse (the scalar type breaks
    /// its own contract).map_err(FusionError::from), or an inverse of zero requested.
    #[error("{context}: no multiplicative inverse")]
    NoInverse { context: &'static str },

    /// The coefficient field does not contain an object the construction needs
    /// (a root of unity of the stated order, a square root).
    #[error("the coefficient field does not contain {needed}")]
    FieldTooSmall { needed: &'static str },

    /// A request for a value that is not a rational number, or not a root of unity,
    /// in the field.
    #[error("{what} is not {expected} in this field")]
    NotInSubfield {
        what: &'static str,
        expected: &'static str,
    },

    /// A polynomial request outside the supported degree or size.
    #[error("polynomial: {0}")]
    Polynomial(&'static str),

    /// The sign of a real element could not be decided exactly by the scalar type.
    #[error("the sign of {context} could not be decided exactly")]
    SignUndecided { context: &'static str },

    /// An internal consistency check failed (the named invariant does not hold). For
    /// validated inputs this is unreachable; it is reported rather than hidden.
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
