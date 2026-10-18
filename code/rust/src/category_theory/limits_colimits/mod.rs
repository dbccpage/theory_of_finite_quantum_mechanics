//! Limits / colimits shells for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Hierarchical catalog under `limits_colimits/`. Legacy flat modules
//! `limits.rs`, `colimits.rs`, and `coend.rs` remain at crate root.

pub mod coend;
pub mod coequalizer;
pub mod cokernel_pair;
pub mod colimit;
pub mod cone;
pub mod coproduct;
pub mod density_comonad;
pub mod end;
pub mod equalizer;
pub mod initial_object;
pub mod kan_extension;
pub mod kernel_pair;
pub mod limit;
pub mod pointwise_kan_extension;
pub mod product;
pub mod pullback;
pub mod pushout;
pub mod terminal_object;

pub use coend::Coend;
pub use coequalizer::Coequalizer;
pub use cokernel_pair::CokernelPair;
pub use colimit::Colimit;
pub use cone::{Cocone, Cone, ConeLeg};
pub use coproduct::Coproduct;
pub use density_comonad::DensityComonad;
pub use end::End;
pub use equalizer::Equalizer;
pub use initial_object::InitialObject;
pub use kan_extension::{KanExtension, KanExtensionKind};
pub use kernel_pair::KernelPair;
pub use limit::Limit;
pub use pointwise_kan_extension::PointwiseKanExtension;
pub use product::Product;
pub use pullback::Pullback;
pub use pushout::Pushout;
pub use terminal_object::TerminalObject;
