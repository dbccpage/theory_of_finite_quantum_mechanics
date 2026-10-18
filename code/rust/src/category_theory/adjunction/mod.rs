//! Adjunction hierarchy shells for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Hierarchical catalog under `adjunction/`. Legacy finite/auditable records
//! remain at crate root as `legacy_adjunction` (alias `adjunction_legacy`).

pub mod adjoint_functor_theorem;
#[allow(clippy::module_inception)]
pub mod adjunction;
pub mod coreflective_subcategory;
pub mod counit;
pub mod galois_connection;
pub mod hom_set_adjunction;
pub mod reflective_subcategory;
pub mod unit;

pub use adjoint_functor_theorem::AdjointFunctorTheoremShell;
pub use adjunction::AdjunctionShell;
pub use coreflective_subcategory::CoreflectiveSubcategoryShell;
pub use counit::CounitShell;
pub use galois_connection::{GaloisConnectionShell, MonotonePair};
pub use hom_set_adjunction::HomSetAdjunctionShell;
pub use reflective_subcategory::ReflectiveSubcategoryShell;
pub use unit::UnitShell;

// Compatibility: finite/auditable adjunction records still live at crate root.
pub use crate::legacy_adjunction::{DeclaredFiniteAdjunction, DerivedMonad};
