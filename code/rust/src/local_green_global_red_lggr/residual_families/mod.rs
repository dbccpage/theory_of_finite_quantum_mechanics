
pub mod record;
pub mod recurrence;
pub mod registry;
pub mod signature;
pub mod wire;

pub use record::{Gamma2ClassId, Q1ClassId, ResidualClassRecord};
pub use recurrence::registry_hit_recurrence;
pub use registry::{FamilyConsultation, FamilyRegistry, RegistryWrite};
pub use signature::{
    shape_signature, shape_signature_from_exact_complex, ShapeSignature, ShapeSignatureError,
};
pub use wire::{
    derive_gamma2_class_id, derive_q1_class_id, reconcile_verified, record_from_verified,
    FamilyCollision, FamilyResolution,
};
