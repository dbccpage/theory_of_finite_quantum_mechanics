// Executable finite evidence; AuthorityEffect: None.
use thiserror::Error;

#[derive(Debug, Error)]
pub enum WdpError {
    #[error("Invalid exact input: {detail}")]
    InvalidInput { detail: String },
    #[error("Refusal: {reason}")]
    Refusal { reason: String },
    #[error("Dimension mismatch: expected {expected}, got {actual}")]
    DimensionMismatch { expected: usize, actual: usize },
    #[error("Float rejected by firewall: exact rational required")]
    FloatRejected,
}
