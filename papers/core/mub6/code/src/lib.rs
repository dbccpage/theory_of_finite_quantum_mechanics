//! Single Source of Truth bridge for MUB(6) code.
//!
//! Re-exports the sovereign `omega_mub` crate so that `omega_engine_atlas/coda_atlas/F004_papers/010_mub6/code`
//! has direct, zero-drift access to the canonical Rust implementations in `crates_rs`.
//!
//! AuthorityEffect: None.

pub use omega_mub::*;
