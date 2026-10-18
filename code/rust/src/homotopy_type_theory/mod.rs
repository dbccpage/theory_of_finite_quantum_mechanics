//! HoTT-facing spine for the Omega tower.
//!
//! This crate encodes the type-theoretic reading of the tower:
//! difference is primitive, sameness is certified zero-difference, authority is
//! an inhabited dependent type, and terminalization is an eliminator into
//! authority/refusal outcomes. It is a finite record layer, not a proof
//! assistant kernel.
//!
//! `primitive_difference` (the finite PD quotient/descent kernel) and the type
//! formers (Π, Σ, sum, unit, empty, path, universe, univalence witness) are
//! shape records validated here. The former `omega_engine_native_hott` crate
//! was a partial copy of this one and was merged into it on 2026-09-25.

pub mod contractible_type;
pub mod difference;
pub mod empty_type;
pub mod higher_inductive_type;
pub mod hott_contract_alignment;
pub mod identity;
pub mod path;
pub mod path_transport;
pub mod pi_type;
pub mod presentation_difference;
pub mod primitive_difference;
pub mod sigma_type;
pub mod sum_type;
pub mod tower;
pub mod truncation;
pub mod type_formation;
pub mod type_universe;
pub mod unit_type;
pub mod univalence_witness;

pub use presentation_difference::{
    active_obstruction, evaluate_extension, ActiveObstructionV1, DemandV1,
    ExtensionEffect, ExtensionEvaluationV1, PresentationV1, QuestionV1,
};

pub use higher_inductive_type::{HigherInductiveType, PathConstructor, PointConstructor};
pub use hott_contract_alignment::HottContractBinding;
pub use tower::{HottLayerView, HottTower, OmegaLayer};
pub mod a_infinity;
pub mod quasi_category;
pub mod substitution;
