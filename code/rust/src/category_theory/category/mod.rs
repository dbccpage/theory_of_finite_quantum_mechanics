//! Category hierarchy shells for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

pub mod arrow_category;
#[allow(clippy::module_inception)]
pub mod category;
pub mod coslice_category;
pub mod discrete_category;
pub mod discrete_fibration;
pub mod fibered_category;
pub mod opfibration;
pub mod opposite;
pub mod product_category;
pub mod slice_category;
pub mod small_category;
pub mod sum_category;
pub mod terminal_category;

pub use arrow_category::ArrowCategoryShell;
pub use category::{FiniteCategoryShell, MorphismTriple};
pub use coslice_category::CosliceCategoryShell;
pub use discrete_category::DiscreteCategoryShell;
pub use discrete_fibration::DiscreteFibrationShell;
pub use fibered_category::FiberedCategoryShell;
pub use opfibration::OpfibrationShell;
pub use opposite::OppositeCategoryShell;
pub use product_category::ProductCategoryShell;
pub use slice_category::SliceCategoryShell;
pub use small_category::SmallCategoryShell;
pub use sum_category::SumCategoryShell;
pub use terminal_category::TerminalCategoryShell;
