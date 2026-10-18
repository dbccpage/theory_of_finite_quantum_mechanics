//! Primitive difference domain types.
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PrimitiveDifference {
    pub label: String,
    pub delta: i64,
}
