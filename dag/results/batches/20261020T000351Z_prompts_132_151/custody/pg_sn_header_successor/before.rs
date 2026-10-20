//! MSS lift/forget towers as finite functor bridge declarations.

use super::bridges::BridgeEvidence;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MssnFunctorBridge {
    pub lift_functor: String,
    pub forget_functor: String,
    pub evidence: BridgeEvidence,
}

impl MssnFunctorBridge {
    pub fn new(lift_functor: &str, forget_functor: &str) -> Self {
        Self {
            lift_functor: lift_functor.into(),
            forget_functor: forget_functor.into(),
            evidence: BridgeEvidence {
                source_discipline: "MSSN".into(),
                target_discipline: "category".into(),
                map_name: format!("{} adjoint {}", lift_functor, forget_functor),
                laws_preserved: vec!["lift/forget boundary".into()],
            },
        }
    }
}
