
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ContractibleType {
    pub type_ref: String,
    pub center_ref: String,
    pub contraction_ref: String,
}

impl ContractibleType {
    pub fn validate(&self) -> Result<(), ContractibleError> {
        if self.type_ref.is_empty() || self.center_ref.is_empty() || self.contraction_ref.is_empty()
        {
            return Err(ContractibleError::MissingReference);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum ContractibleError {
    #[error("contractible type is missing type, center, or contraction reference")]
    MissingReference,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn contractible_type_validate_ok() {
        let c = ContractibleType {
            type_ref: "Unit".to_string(),
            center_ref: "tt".to_string(),
            contraction_ref: "contr_unit".to_string(),
        };
        assert!(c.validate().is_ok());
    }

    #[test]
    fn contractible_type_rejects_empty() {
        let c = ContractibleType {
            type_ref: "Unit".to_string(),
            center_ref: String::new(),
            contraction_ref: "contr".to_string(),
        };
        assert_eq!(c.validate(), Err(ContractibleError::MissingReference));
    }
}
