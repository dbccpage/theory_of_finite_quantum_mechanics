//! Geometric Tier for Operad Theory.
//!
//! AuthorityEffect: None.

pub mod little_disks;
pub mod en_algebra;

pub use little_disks::{LittleDisksConfiguration, RectilinearDisk};
pub use en_algebra::{build_associative_homology_operad, build_commutative_homology_operad, build_gerstenhaber_homology_operad};
