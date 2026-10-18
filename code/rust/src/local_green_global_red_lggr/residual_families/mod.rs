//! # `residual_families` — Hashed-shape registry of recognized residual classes.
//!
//! Diagnostic-only lookup surface. Mints **no** authority. Product-local
//! terminal stamping and checked-packet evidence certification both remain
//! non-authoritative; only the authenticated host promotion contract may create
//! an authorized local result. This module is not on that path.
//!
//! ODP packet:
//! `omega_engine/crates/omega_contracts/src/contract_canonical_definitions/core/09_packets/omega_residual_families_packet.md`
//!
//! ## Carrier (verbatim from packet §1)
//!
//! > The diagnostic carrier formed by the cochain shape signature of
//! > `omega_homology::cochain_primitive_difference::CochainPrimitiveDifference`
//! > instances emitted by `omega_homology::cochain_complex::CochainComplex::d0`
//! > and `::d1`. The 2-window inspects the local pair
//! > $(\sigma(Q^1), \sigma(\Gamma_2))$ where $\sigma$ is a `blake3`-derived
//! > shape-only signature over the primitive-difference structure (face indices,
//! > arity, coefficient-domain tag, quotient-class id from
//! > `omega_homology::quotient::QuotientSpace`), and where the right-hand window
//! > slot is the diagnostic mass pair
//! > $(\Phi_1, \Gamma_2)$ produced by
//! > `omega_functional::phi1::VerifiedExactPhi1` and
//! > `omega_functional::gamma2::ExactGamma2Result` under a fixed
//! > `omega_types::observer::Observer`. The carrier deliberately discards
//! > raw cochain payload bytes: the signature key is the only persisted shape
//! > fingerprint.
//!
//! ## $C^0$ (verbatim from packet §2)
//!
//! > No crate yet exists. The local assignments are
//! > (a) the existing in-tree types
//! > `CochainPrimitiveDifference`, `QuotientSpace`,
//! > `omega_functional::phi1::VerifiedExactPhi1`,
//! > `omega_functional::gamma2::ExactGamma2Result`,
//! > `omega_types::observer::Observer`,
//! > and (b) the empty crate skeleton `omega_engine/crates/omega_residual_families/`
//! > to be added as a workspace member with a `ShapeSignature` newtype, a
//! > `ResidualClassRecord { signature, q1_class_id, gamma2_class_id, hits: u64 }`
//! > struct, and a `FamilyRegistry` lookup table keyed by `ShapeSignature`.
//!
//! ## ZeroRel (verbatim from packet §5)
//!
//! > Two `CochainPrimitiveDifference` instances are identified iff their
//! > canonicalized shape signature
//! > $\sigma : \text{CochainPrimitiveDifference} \to \text{blake3 digest}$
//! > agrees. Equivalently: differences that vary only by
//! > `omega_homology::cochain::Cochain` coefficient values, internal field
//! > ordering, or `omega_types::observer::Observer`-local naming, but that
//! > share the same face-index pattern, arity, coefficient-domain tag, and
//! > `QuotientSpace`-id, are gauge-equivalent for registry purposes. ZeroRel is
//! > exactly the kernel of $\sigma$.
//!
//! ## Firewall
//!
//! The host crate (`omega_epk`) does NOT depend on `omega_sweep_kernel` or `omega_certifiers`.
//! No public function returns a `Certificate`; registry operations remain
//! evidence-only and have no authority effect.

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
