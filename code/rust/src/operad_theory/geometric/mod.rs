//! Geometric Tier for Operad Theory.
//!
//! AuthorityEffect: None.

pub mod little_disks;
pub mod en_algebra;

pub use little_disks::{LittleDisksConfiguration, RectilinearDisk};
pub use en_algebra::{build_associative_homology_operad, build_commutative_homology_operad, build_gerstenhaber_homology_operad};

use num_rational::Ratio;

/// Checks whether two 1D open interval operad elements (a1, b1) and (a2, b2) overlap.
pub fn intervals_overlap(a1: Ratio<i64>, b1: Ratio<i64>, a2: Ratio<i64>, b2: Ratio<i64>) -> bool {
    a1 < b2 && a2 < b1
}

#[cfg(test)]
mod geom_tests {
    use super::*;

    #[test]
    fn test_intervals() {
        assert!(intervals_overlap(Ratio::new(0, 1), Ratio::new(2, 1), Ratio::new(1, 1), Ratio::new(3, 1)));
        assert!(!intervals_overlap(Ratio::new(0, 1), Ratio::new(1, 1), Ratio::new(2, 1), Ratio::new(3, 1)));
    }
}
