
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SumType {
    pub left_type_ref: String,
    pub right_type_ref: String,
}

impl SumType {
    pub fn validate(&self) -> Result<(), SumTypeError> {
        if self.left_type_ref.is_empty() {
            return Err(SumTypeError::EmptyLeftTypeRef);
        }
        if self.right_type_ref.is_empty() {
            return Err(SumTypeError::EmptyRightTypeRef);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum SumTypeError {
    #[error("sum type left_type_ref must be non-empty")]
    EmptyLeftTypeRef,
    #[error("sum type right_type_ref must be non-empty")]
    EmptyRightTypeRef,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let sum = SumType {
            left_type_ref: "A".to_string(),
            right_type_ref: "B".to_string(),
        };
        assert!(sum.validate().is_ok());
    }

    #[test]
    fn validate_rejects_empty_left() {
        let sum = SumType {
            left_type_ref: String::new(),
            right_type_ref: "B".to_string(),
        };
        assert_eq!(sum.validate(), Err(SumTypeError::EmptyLeftTypeRef));
    }

    #[test]
    fn validate_rejects_empty_right() {
        let sum = SumType {
            left_type_ref: "A".to_string(),
            right_type_ref: String::new(),
        };
        assert_eq!(sum.validate(), Err(SumTypeError::EmptyRightTypeRef));
    }
}
