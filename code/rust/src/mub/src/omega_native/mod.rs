//! Clean-room Omega-native MUB lane.
//!
//! Exact certificates, campaign corpora, and float cross-checks are separate
//! modules. The finite exact carriers live in `omega_quantum_physics::mub`.
//! `carrier` stays re-exported here because the ownership ledger names this
//! path as the domain-carrier surface.

pub mod campaign;
pub mod census;
pub mod exact;
pub mod float_check;

pub use omega_quantum_physics::mub::carrier;
