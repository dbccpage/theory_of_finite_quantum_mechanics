//! Error types for homological algebra operations.

use crate::linear_algebra::basic_matrix::MatrixError;
use crate::linear_algebra::smith_form::SmithError;
use thiserror::Error;

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum HomologicalError {
    #[error("dimension mismatch: expected {expected}, got {got}")]
    DimensionMismatch { expected: usize, got: usize },

    #[error("boundary law violated: d_(k) * d_(k+1) != 0 at degree {degree}")]
    BoundaryLawViolation { degree: i32 },

    #[error("coboundary law violated: d^(k+1) * d^(k) != 0 at degree {degree}")]
    CoboundaryLawViolation { degree: i32 },

    #[error("invalid degree: {0}")]
    InvalidDegree(i32),

    #[error("matrix error: {0}")]
    MatrixError(#[from] MatrixError),

    #[error("non-exact division encountered")]
    NonExactDivision,

    #[error("basis mismatch: {description}")]
    BasisMismatch { description: String },

    #[error("element is not a cycle: boundary is non-zero")]
    NotCycle,

    #[error("element is not a cocycle: coboundary is non-zero")]
    NotCocycle,

    #[error("element is not a boundary")]
    NotBoundary,

    #[error("element is not a coboundary")]
    NotCoboundary,

    #[error("homology dimension underflow: ker_dim={ker_dim}, im_dim={im_dim}")]
    HomologyDimensionUnderflow { ker_dim: usize, im_dim: usize },

    #[error("empty basis")]
    EmptyBasis,

    #[error("invalid manifest: {reason}")]
    InvalidManifest { reason: String },

    #[error("hash mismatch: expected {expected}, got {got}")]
    HashMismatch { expected: String, got: String },

    #[error("missing witness")]
    MissingWitness,
    /// A Smith-normal-form rank exceeds the dimension it is subtracted from, which
    /// would make a Betti number negative. Reported rather than clamped to zero:
    /// clamping would emit a plausible Betti number for an inconsistent carrier.
    #[error(
        "Betti rank inconsistency at degree {degree}: rank sum {rank_sum} exceeds dimension {dimension}"
    )]
    BettiRankInconsistency {
        dimension: usize,
        rank_sum: usize,
        degree: usize,
    },

    /// A boundary map has a non-integer entry in the carrier's coordinate lattice,
    /// so it has no Smith normal form over ℤ and no integral rank or torsion can be
    /// reported for it.
    ///
    /// Typed rather than folded into [`Self::UnsupportedOperation`]: a caller must be
    /// able to distinguish "this carrier is rational, not integral" — a fact about
    /// the input that a different lattice could change — from "the SNF algorithm
    /// failed", which is a fact about this implementation.
    #[error(
        "boundary map {map} is not integral in the carrier's coordinate lattice: \
         non-integer entry at row {row}, column {col}"
    )]
    NonIntegralBoundaryMap {
        map: &'static str,
        row: usize,
        col: usize,
    },

    /// Smith normal form of a boundary map failed. The underlying [`SmithError`] is
    /// preserved as the source rather than stringified, so a caller can match on
    /// `Overflow` / `DivisibilityViolation` / `VerificationFailed` separately.
    #[error("Smith normal form of boundary map {map} failed")]
    SmithNormalFormFailed {
        map: &'static str,
        #[source]
        source: SmithError,
    },

    #[error("unsupported operation: {0}")]
    UnsupportedOperation(String),

    #[error("non-positive weight at index {index}")]
    NonPositiveWeight { index: usize },

    #[error("weight dimension mismatch: expected {expected}, got {got}")]
    WeightDimensionMismatch { expected: usize, got: usize },

    #[error("empty verification source")]
    EmptyVerificationSource,

    #[error("edge source out of range: edge {edge}, source {src}")]
    EdgeSourceOutOfRange { edge: usize, src: usize },

    #[error("edge target out of range: edge {edge}, target {tgt}")]
    EdgeTargetOutOfRange { edge: usize, tgt: usize },

    #[error("self-loop not allowed: node {node}")]
    SelfLoopNotAllowed { node: usize },

    #[error("triangle vertex out of range: triangle {triangle}, vertex {vertex}")]
    TriangleVertexOutOfRange { triangle: usize, vertex: usize },

    #[error("triangle missing required edge: triangle {triangle}, edge ({src}, {tgt})")]
    TriangleMissingEdge {
        triangle: usize,
        src: usize,
        tgt: usize,
    },

    #[error("serialization error: {0}")]
    SerializationError(String),
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_error_display() {
        let err = HomologicalError::DimensionMismatch {
            expected: 3,
            got: 5,
        };
        assert_eq!(format!("{}", err), "dimension mismatch: expected 3, got 5");
    }

    #[test]
    fn test_boundary_law_violation_display() {
        let err = HomologicalError::BoundaryLawViolation { degree: 2 };
        assert_eq!(
            format!("{}", err),
            "boundary law violated: d_(k) * d_(k+1) != 0 at degree 2"
        );
    }

    #[test]
    fn test_matrix_error_conversion() {
        let matrix_err = MatrixError::DimensionMismatch {
            left: (2, 3),
            right: (4, 5),
        };
        let hom_err: HomologicalError = matrix_err.into();
        assert!(matches!(hom_err, HomologicalError::MatrixError(_)));
    }
}
