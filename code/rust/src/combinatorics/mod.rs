//! Exact finite combinatorics with budgets checked before enumeration.
//! Depends on nothing in the workspace.
//!
//! AuthorityEffect: None.

/// Mandatory authority effect declaration.
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";

pub mod cartesian_words;
pub mod enumeration;
pub mod finite_geometry;
pub mod mub_configurations;
pub mod weyl_systems;

pub mod color_constraints;

pub mod partitions;
