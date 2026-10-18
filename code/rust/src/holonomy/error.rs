//! Strongly typed errors, operational limits, and Soviet allocation helpers for omega_holonomy.
//!
//! AuthorityEffect: None.
//! Governing Rule: RULE[user_global] (claim hygiene, zero floats).

use serde::{Deserialize, Serialize};
use thiserror::Error;

/// Strongly typed error enum for discrete holonomy operations.
///
/// Enforces strict precedence:
/// AllocationFailure > SingularConnection > OpenLoop > VertexNotFound > EdgeNotFound > DimensionMismatch > PathLengthExceeded.
#[derive(Debug, Clone, PartialEq, Eq, Error, Serialize, Deserialize)]
pub enum HolonomyError {
    #[error("resource element count overflows usize")]
    ResourceCountOverflow,
    #[error("Soviet Builder allocation failure: requested {requested} elements ({detail})")]
    AllocationFailure { requested: usize, detail: String },

    #[error("Singular or non-invertible connection matrix on edge ({src}, {tgt}): {detail}")]
    SingularConnection {
        src: String,
        tgt: String,
        detail: String,
    },

    #[error("Loop is open: start vertex '{start}' != end vertex '{end}'")]
    OpenLoop { start: String, end: String },

    #[error("Vertex '{id}' not found in cell complex")]
    VertexNotFound { id: String },

    #[error("Edge ({src}, {tgt}) not found in cell complex connection registry")]
    EdgeNotFound { src: String, tgt: String },

    #[error("Dimension mismatch: expected {expected}, actual {actual}")]
    DimensionMismatch { expected: usize, actual: usize },

    #[error("Path length exceeded: length {length}, limit {limit}")]
    PathLengthExceeded { length: usize, limit: usize },

    #[error("Loop count exceeded: count {count}, limit {limit}")]
    LoopCountExceeded { count: usize, limit: usize },

    #[error("Operation limit exceeded: limit {limit}, requested {requested}")]
    OperationLimitExceeded { limit: usize, requested: usize },

    #[error("Malformed path: path must contain at least 2 vertices (got {length})")]
    MalformedPath { length: usize },

    #[error("Empty path rejected: path must contain at least 2 vertices")]
    EmptyPath,

    #[error("Duplicate vertex declared: '{id}'")]
    DuplicateVertex { id: String },

    #[error("Duplicate edge declared: ({src}, {tgt})")]
    DuplicateEdge { src: String, tgt: String },

    #[error("Duplicate face declared: '{id}'")]
    DuplicateFace { id: String },

    #[error("Face '{id}' not found in cell complex")]
    FaceNotFound { id: String },

    #[error("Face boundary cycle mismatch: face '{face}' does not form a closed cycle: {detail}")]
    BoundaryCycleMismatch { face: String, detail: String },

    #[error("Division by zero in exact rational field arithmetic")]
    ZeroDivision,

    #[error("Non-Hermitian connection Laplacian at ({u}, {v}): {detail}")]
    NonHermitianLaplacian {
        u: String,
        v: String,
        detail: String,
    },

    #[error("Curvature commutator violation: {detail}")]
    CurvatureCommutatorViolation { detail: String },

    #[error("Negative bound: {quantity} = {value} must be non-negative")]
    NegativeBound { quantity: String, value: String },

    /// A matrix with no inverse, outside any edge: `ExactMatrix::inverse`
    /// reports this, and `DiscreteConnection::set_connection` turns it into
    /// `SingularConnection` with the edge attached.
    #[error("Singular matrix: {detail}")]
    SingularMatrix { detail: String },

    /// An edge index beyond the complex: the edge-indexed connection and walk
    /// API of `gauge_fixing` names edges by index, not by vertex pair.
    #[error("Edge index {index} is out of range: the complex has {edge_count} edges")]
    EdgeIndexOutOfRange { index: usize, edge_count: usize },

    #[error("Vertex index {index} is out of range: the complex has {vertex_count} vertices")]
    VertexIndexOutOfRange { index: usize, vertex_count: usize },

    #[error("Expected one value per edge ({expected} edges) but got {actual} values")]
    EdgeValueCount { expected: usize, actual: usize },

    #[error("Expected one gauge value per vertex ({expected} vertices) but got {actual} values")]
    VertexValueCount { expected: usize, actual: usize },

    /// A `(source, target)`-keyed connection stores one matrix per vertex pair
    /// and treats the opposite direction as its inverse, so two edges joining
    /// the same vertices in opposite directions cannot carry independent values.
    #[error(
        "Edges {first} and {second} join the same vertices in opposite directions; a \
         (source, target)-keyed connection cannot give them independent values"
    )]
    AntiparallelEdges { first: usize, second: usize },

    #[error("Walk is broken at step {step}: {detail}")]
    BrokenWalk { step: usize, detail: String },

    #[error("Step {step} has direction {direction}; a step direction is +1 or -1")]
    InvalidStepDirection { step: usize, direction: i8 },

    #[error("Invalid group order {order}: a finite cyclic group has order at least 1")]
    InvalidGroupOrder { order: u64 },

    #[error("Exact integer elimination failed: {detail}")]
    IntegerEliminationFailed { detail: String },
}

impl HolonomyError {
    /// Returns the precedence rank of this error (lower integer = higher priority).
    pub fn precedence_rank(&self) -> usize {
        match self {
            HolonomyError::ResourceCountOverflow => 0,
            HolonomyError::AllocationFailure { .. } => 1,
            HolonomyError::SingularConnection { .. } => 2,
            HolonomyError::OpenLoop { .. } => 3,
            HolonomyError::VertexNotFound { .. } => 4,
            HolonomyError::EdgeNotFound { .. } => 5,
            HolonomyError::DimensionMismatch { .. } => 6,
            HolonomyError::PathLengthExceeded { .. } => 7,
            HolonomyError::LoopCountExceeded { .. } => 8,
            HolonomyError::OperationLimitExceeded { .. } => 9,
            HolonomyError::MalformedPath { .. } => 10,
            HolonomyError::EmptyPath => 11,
            HolonomyError::DuplicateVertex { .. } => 12,
            HolonomyError::DuplicateEdge { .. } => 13,
            HolonomyError::DuplicateFace { .. } => 14,
            HolonomyError::FaceNotFound { .. } => 15,
            HolonomyError::BoundaryCycleMismatch { .. } => 16,
            HolonomyError::ZeroDivision => 17,
            HolonomyError::NonHermitianLaplacian { .. } => 18,
            HolonomyError::CurvatureCommutatorViolation { .. } => 19,
            HolonomyError::NegativeBound { .. } => 20,
            HolonomyError::SingularMatrix { .. } => 21,
            HolonomyError::EdgeIndexOutOfRange { .. } => 22,
            HolonomyError::VertexIndexOutOfRange { .. } => 23,
            HolonomyError::EdgeValueCount { .. } => 24,
            HolonomyError::VertexValueCount { .. } => 25,
            HolonomyError::AntiparallelEdges { .. } => 26,
            HolonomyError::BrokenWalk { .. } => 27,
            HolonomyError::InvalidStepDirection { .. } => 28,
            HolonomyError::InvalidGroupOrder { .. } => 29,
            HolonomyError::IntegerEliminationFailed { .. } => 30,
        }
    }
}

/// Resource admission is owned by the kernel; holonomy preserves its domain error.
impl From<omega_kernel::resource_limits::ResourceError> for HolonomyError {
    fn from(error: omega_kernel::resource_limits::ResourceError) -> Self {
        use omega_kernel::resource_limits::ResourceError;
        match error {
            ResourceError::AllocationFailure { requested, detail } => {
                Self::AllocationFailure { requested, detail }
            }
            ResourceError::CountOverflow | ResourceError::DimensionOverflow => {
                Self::ResourceCountOverflow
            }
            ResourceError::HilbertDimensionExceeded { requested, limit }
            | ResourceError::OperatorCountExceeded { requested, limit }
            | ResourceError::BasisStateCountExceeded { requested, limit }
            | ResourceError::KrausRankExceeded { requested, limit } => {
                Self::OperationLimitExceeded { requested, limit }
            }
            ResourceError::NonPositiveDimension => Self::DimensionMismatch {
                expected: 1,
                actual: 0,
            },
        }
    }
}
