
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct UnitType {
    pub id: String,
    pub unit_term_ref: String,
}

impl UnitType {
    pub fn validate(&self) -> Result<(), UnitTypeError> {
        if self.id.is_empty() {
            return Err(UnitTypeError::EmptyId);
        }
        if self.unit_term_ref.is_empty() {
            return Err(UnitTypeError::EmptyUnitTermRef);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum UnitTypeError {
    #[error("unit type id must be non-empty")]
    EmptyId,
    #[error("unit type unit_term_ref must be non-empty")]
    EmptyUnitTermRef,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let unit = UnitType {
            id: "Unit".to_string(),
            unit_term_ref: "star".to_string(),
        };
        assert!(unit.validate().is_ok());
    }

    #[test]
    fn validate_rejects_empty_id() {
        let unit = UnitType {
            id: String::new(),
            unit_term_ref: "star".to_string(),
        };
        assert_eq!(unit.validate(), Err(UnitTypeError::EmptyId));
    }

    #[test]
    fn validate_rejects_empty_unit_term() {
        let unit = UnitType {
            id: "Unit".to_string(),
            unit_term_ref: String::new(),
        };
        assert_eq!(unit.validate(), Err(UnitTypeError::EmptyUnitTermRef));
    }
}
