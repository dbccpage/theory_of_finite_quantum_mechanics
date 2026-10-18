//! Monad shells for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Hierarchical best-effort records (endofunctor monoids, duals, algebras).
//! Computational finite monads live in `crate::legacy_monad`.

pub mod algebra_for_monad;
pub mod coalgebra_for_comonad;
pub mod comonad;
pub mod distributive_law;
pub mod eilenberg_moore;
pub mod kleisli_category;
#[allow(clippy::module_inception)]
pub mod monad;
pub mod monad_transformer;

pub use algebra_for_monad::AlgebraForMonad;
pub use coalgebra_for_comonad::CoalgebraForComonad;
pub use comonad::Comonad;
pub use distributive_law::DistributiveLaw;
pub use eilenberg_moore::EilenbergMoore;
pub use kleisli_category::KleisliCategory;
pub use monad::Monad;
pub use monad_transformer::MonadTransformer;
