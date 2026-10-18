
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct EmptyType {
    pub id: String,
}

impl EmptyType {
    pub fn validate(&self) -> Result<(), EmptyTypeError> {
        if self.id.is_empty() {
            return Err(EmptyTypeError::EmptyId);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum EmptyTypeError {
    #[error("empty type id must be non-empty")]
    EmptyId,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let empty = EmptyType {
            id: "Empty".to_string(),
        };
        assert!(empty.validate().is_ok());
    }

    #[test]
    fn validate_rejects_empty_id() {
        let empty = EmptyType { id: String::new() };
        assert_eq!(empty.validate(), Err(EmptyTypeError::EmptyId));
    }
}
