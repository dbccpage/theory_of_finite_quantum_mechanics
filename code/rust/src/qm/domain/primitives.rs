//! Foundational finite QM primitives.
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PrimitiveAxiom {
    pub id: String,
    pub description: String,
}
