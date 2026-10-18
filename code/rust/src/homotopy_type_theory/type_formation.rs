
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum FormationKind {
    Base,
    Pi,
    Sigma,
    Sum,
    Identity,
    Unit,
    Empty,
    Hit,
    Other,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TypeRecord {
    pub id: String,
    pub universe_level: u32,
    pub formation: FormationKind,
}

impl TypeRecord {
    pub fn validate(&self) -> Result<(), TypeFormationError> {
        if self.id.is_empty() {
            return Err(TypeFormationError::EmptyId);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum TypeFormationError {
    #[error("type record id must be non-empty")]
    EmptyId,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok_pi_formation() {
        let t = TypeRecord {
            id: "Pi_A_B".to_string(),
            universe_level: 0,
            formation: FormationKind::Pi,
        };
        assert!(t.validate().is_ok());
    }

    #[test]
    fn validate_rejects_empty_id() {
        let t = TypeRecord {
            id: String::new(),
            universe_level: 0,
            formation: FormationKind::Base,
        };
        assert_eq!(t.validate(), Err(TypeFormationError::EmptyId));
    }

    #[test]
    fn all_formation_kinds_construct() {
        let kinds = [
            FormationKind::Base,
            FormationKind::Pi,
            FormationKind::Sigma,
            FormationKind::Sum,
            FormationKind::Identity,
            FormationKind::Unit,
            FormationKind::Empty,
            FormationKind::Hit,
            FormationKind::Other,
        ];
        for (i, formation) in kinds.into_iter().enumerate() {
            let t = TypeRecord {
                id: format!("t{i}"),
                universe_level: i as u32,
                formation,
            };
            assert!(t.validate().is_ok());
        }
    }
}
