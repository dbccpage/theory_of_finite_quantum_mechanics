
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TypeUniverse {
    pub level: u32,
    pub name: String,
}

impl TypeUniverse {
    pub fn validate(&self) -> Result<(), TypeUniverseError> {
        if self.name.is_empty() {
            return Err(TypeUniverseError::EmptyName);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum TypeUniverseError {
    #[error("type universe name must be non-empty")]
    EmptyName,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok_nonempty_name() {
        let u = TypeUniverse {
            level: 0,
            name: "U0".to_string(),
        };
        assert!(u.validate().is_ok());
    }

    #[test]
    fn validate_rejects_empty_name() {
        let u = TypeUniverse {
            level: 1,
            name: String::new(),
        };
        assert_eq!(u.validate(), Err(TypeUniverseError::EmptyName));
    }

    #[test]
    fn level_zero_is_allowed() {
        let u = TypeUniverse {
            level: 0,
            name: "U".to_string(),
        };
        assert!(u.validate().is_ok());
        assert_eq!(u.level, 0);
    }
}
