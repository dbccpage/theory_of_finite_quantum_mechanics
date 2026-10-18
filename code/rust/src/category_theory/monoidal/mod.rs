//! Monoidal hierarchy shells for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Distinct from crate-root trait modules `monoidal_category` and `braided_monoidal`.

pub mod braided_monoidal;
pub mod cartesian_closed;
pub mod closed_monoidal;
pub mod cohomology_in_monoidal;
pub mod compact_closed;
pub mod monoidal_category;
pub mod monoidal_functor;
pub mod rigid_category;
pub mod symmetric_monoidal;
pub mod symmetric_monoidal_functor;
pub mod traced_monoidal;

pub use braided_monoidal::BraidedMonoidal;
pub use cartesian_closed::CartesianClosed;
pub use closed_monoidal::ClosedMonoidal;
pub use cohomology_in_monoidal::CohomologyInMonoidal;
pub use compact_closed::CompactClosed;
pub use monoidal_category::MonoidalCategory;
pub use monoidal_functor::MonoidalFunctor;
pub use rigid_category::RigidCategory;
pub use symmetric_monoidal::SymmetricMonoidal;
pub use symmetric_monoidal_functor::SymmetricMonoidalFunctor;
pub use traced_monoidal::TracedMonoidal;
