//! Synonym-level path records for the HoTT spine.
//!
//! A [`Path`] is a finite shape record for a path/identity inhabitant
//! `p : Id_A(x, y)`. It does not mint authority and does not compute
//! path algebra; validation is shape-only (non-empty references).

use crate::identity::{IdentityError, IdentityType, TermId, TypeId};
use serde::{Deserialize, Serialize};

/// Synonym-level path record: `path_ref` witnesses `source = target` in `type_id`.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Path {
    pub type_id: TypeId,
    pub source: TermId,
    pub target: TermId,
    pub path_ref: String,
}

impl Path {
    /// Shape-only validation: type, endpoints, and path carrier must be non-empty.
    pub fn validate(&self) -> Result<(), IdentityError> {
        if self.type_id.0.is_empty()
            || self.source.0.is_empty()
            || self.target.0.is_empty()
            || self.path_ref.is_empty()
        {
            return Err(IdentityError::MissingTypeOrTerm);
        }
        Ok(())
    }

    /// Build a synonym-level path from an identity type.
    ///
    /// Uses the identity's difference object ref as the path carrier.
    /// Does not re-validate the identity's zero-certificate; callers that
    /// need a validated identity should call [`IdentityType::validate`] first.
    pub fn from_identity(identity: &IdentityType) -> Self {
        Self {
            type_id: identity.type_id.clone(),
            source: identity.left.clone(),
            target: identity.right.clone(),
            path_ref: identity.difference.difference_ref.clone(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::difference::{DifferenceTerm, ZeroDifferenceCertificate};

    fn sample_identity() -> IdentityType {
        IdentityType {
            type_id: TypeId("A".to_string()),
            left: TermId("x".to_string()),
            right: TermId("y".to_string()),
            difference: DifferenceTerm {
                source_ref: "x".to_string(),
                target_ref: "y".to_string(),
                difference_ref: "dxy".to_string(),
                computed_by_ref: "checker".to_string(),
            },
            zero_certificate: ZeroDifferenceCertificate {
                difference_ref: "dxy".to_string(),
                checker_ref: "zero-checker".to_string(),
                replay_ref: "replay".to_string(),
            },
        }
    }

    #[test]
    fn path_validate_rejects_empty_fields() {
        let path = Path {
            type_id: TypeId(String::new()),
            source: TermId("x".to_string()),
            target: TermId("y".to_string()),
            path_ref: "p".to_string(),
        };
        assert!(path.validate().is_err());

        let path = Path {
            type_id: TypeId("A".to_string()),
            source: TermId("x".to_string()),
            target: TermId("y".to_string()),
            path_ref: String::new(),
        };
        assert!(path.validate().is_err());
    }

    #[test]
    fn path_validate_accepts_complete_record() {
        let path = Path {
            type_id: TypeId("A".to_string()),
            source: TermId("x".to_string()),
            target: TermId("y".to_string()),
            path_ref: "p".to_string(),
        };
        assert!(path.validate().is_ok());
    }

    #[test]
    fn path_from_identity_copies_endpoints_and_difference_ref() {
        let identity = sample_identity();
        assert!(identity.validate().is_ok());
        let path = Path::from_identity(&identity);
        assert_eq!(path.type_id, identity.type_id);
        assert_eq!(path.source, identity.left);
        assert_eq!(path.target, identity.right);
        assert_eq!(path.path_ref, "dxy");
        assert!(path.validate().is_ok());
    }
}
