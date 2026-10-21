use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Error, Serialize, Deserialize)]
pub enum HolonomyError {
    #[error("matrix index ({row}, {col}) is outside shape {rows}x{cols}")]
    MatrixIndexOutOfBounds {
        row: usize,
        col: usize,
        rows: usize,
        cols: usize,
    },
    #[error("invalid exact scalar: {detail}")]
    InvalidScalar { detail: String },
    #[error("matrix requires {requested} cells, above the declared limit {limit}")]
    MatrixCellLimitExceeded { requested: usize, limit: usize },
    #[error(
        "vertex '{id}' has registry/index binding ({mapped}, {declared}), expected {expected}"
    )]
    VertexRegistryMismatch {
        id: String,
        expected: usize,
        declared: usize,
        mapped: usize,
    },
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

    #[error("Singular matrix: {detail}")]
    SingularMatrix { detail: String },

    #[error("Edge index {index} is out of range: the complex has {edge_count} edges")]
    EdgeIndexOutOfRange { index: usize, edge_count: usize },

    #[error("Vertex index {index} is out of range: the complex has {vertex_count} vertices")]
    VertexIndexOutOfRange { index: usize, vertex_count: usize },

    #[error("Expected one value per edge ({expected} edges) but got {actual} values")]
    EdgeValueCount { expected: usize, actual: usize },

    #[error("Expected one gauge value per vertex ({expected} vertices) but got {actual} values")]
    VertexValueCount { expected: usize, actual: usize },

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
    fn precedence_group_0_to_6(&self) -> Option<usize> {
        match self {
            HolonomyError::ResourceCountOverflow => Some(0),
            HolonomyError::AllocationFailure { .. } => Some(1),
            HolonomyError::SingularConnection { .. } => Some(2),
            HolonomyError::OpenLoop { .. } => Some(3),
            HolonomyError::VertexNotFound { .. } => Some(4),
            HolonomyError::EdgeNotFound { .. } => Some(5),
            HolonomyError::DimensionMismatch { .. } => Some(6),
            _ => None,
        }
    }

    fn precedence_group_7_to_13(&self) -> Option<usize> {
        match self {
            HolonomyError::PathLengthExceeded { .. } => Some(7),
            HolonomyError::LoopCountExceeded { .. } => Some(8),
            HolonomyError::OperationLimitExceeded { .. } => Some(9),
            HolonomyError::MalformedPath { .. } => Some(10),
            HolonomyError::EmptyPath => Some(11),
            HolonomyError::DuplicateVertex { .. } => Some(12),
            HolonomyError::DuplicateEdge { .. } => Some(13),
            _ => None,
        }
    }

    fn precedence_group_14_to_20(&self) -> Option<usize> {
        match self {
            HolonomyError::DuplicateFace { .. } => Some(14),
            HolonomyError::FaceNotFound { .. } => Some(15),
            HolonomyError::BoundaryCycleMismatch { .. } => Some(16),
            HolonomyError::ZeroDivision => Some(17),
            HolonomyError::NonHermitianLaplacian { .. } => Some(18),
            HolonomyError::CurvatureCommutatorViolation { .. } => Some(19),
            HolonomyError::NegativeBound { .. } => Some(20),
            _ => None,
        }
    }

    fn precedence_group_21_to_27(&self) -> Option<usize> {
        match self {
            HolonomyError::SingularMatrix { .. } => Some(21),
            HolonomyError::EdgeIndexOutOfRange { .. } => Some(22),
            HolonomyError::VertexIndexOutOfRange { .. } => Some(23),
            HolonomyError::EdgeValueCount { .. } => Some(24),
            HolonomyError::VertexValueCount { .. } => Some(25),
            HolonomyError::AntiparallelEdges { .. } => Some(26),
            HolonomyError::BrokenWalk { .. } => Some(27),
            _ => None,
        }
    }

    fn precedence_group_28_to_34(&self) -> Option<usize> {
        match self {
            HolonomyError::InvalidStepDirection { .. } => Some(28),
            HolonomyError::InvalidGroupOrder { .. } => Some(29),
            HolonomyError::IntegerEliminationFailed { .. } => Some(30),
            HolonomyError::MatrixIndexOutOfBounds { .. } => Some(31),
            HolonomyError::InvalidScalar { .. } => Some(32),
            HolonomyError::VertexRegistryMismatch { .. } => Some(33),
            HolonomyError::MatrixCellLimitExceeded { .. } => Some(34),
            _ => None,
        }
    }

    pub fn precedence_rank(&self) -> usize {
        self.precedence_group_0_to_6()
            .or_else(|| self.precedence_group_7_to_13())
            .or_else(|| self.precedence_group_14_to_20())
            .or_else(|| self.precedence_group_21_to_27())
            .or_else(|| self.precedence_group_28_to_34())
            .unwrap_or(usize::MAX)
    }
}

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
