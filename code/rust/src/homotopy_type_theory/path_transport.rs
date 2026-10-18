//! Path-oriented transport and J-style identity elimination records.
//!
//! [`PathTransport`] is a synonym name for [`Transport`](crate::identity::Transport):
//! transport along a path into a dependent family. [`IdentityEliminator`] is the
//! finite shape of the path-induction (J) eliminator. Neither record mints
//! authority; validation is shape-only.

use crate::identity::{IdentityError, Transport};
use serde::{Deserialize, Serialize};

/// Transport along a path into a dependent family (synonym of [`Transport`]).
pub type PathTransport = Transport;

/// J-style identity eliminator record (path induction).
///
/// Motive `C`, base case `c` for `refl`, path `p`, and result term.
/// Shape-only: does not compute or verify the elimination.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct IdentityEliminator {
    pub motive_ref: String,
    pub base_case_ref: String,
    pub path_ref: String,
    pub result_ref: String,
}

impl IdentityEliminator {
    /// Shape-only validation: all J-eliminator references must be non-empty.
    pub fn validate(&self) -> Result<(), IdentityError> {
        if self.motive_ref.is_empty()
            || self.base_case_ref.is_empty()
            || self.path_ref.is_empty()
            || self.result_ref.is_empty()
        {
            return Err(IdentityError::MissingTransportReference);
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::identity::TermId;

    #[test]
    fn path_transport_is_transport_validate() {
        let transport: PathTransport = Transport {
            path_ref: "p".to_string(),
            family_ref: "B".to_string(),
            input_term: TermId("x".to_string()),
            output_term: TermId("y".to_string()),
            transport_certificate_ref: "tr-cert".to_string(),
        };
        assert!(transport.validate().is_ok());
    }

    #[test]
    fn identity_eliminator_requires_all_refs() {
        let elim = IdentityEliminator {
            motive_ref: "C".to_string(),
            base_case_ref: "c_refl".to_string(),
            path_ref: "p".to_string(),
            result_ref: "J(C,c,p)".to_string(),
        };
        assert!(elim.validate().is_ok());

        let bad = IdentityEliminator {
            motive_ref: String::new(),
            base_case_ref: "c".to_string(),
            path_ref: "p".to_string(),
            result_ref: "r".to_string(),
        };
        assert!(bad.validate().is_err());
    }
}
