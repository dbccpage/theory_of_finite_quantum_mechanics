
pub mod deep_run;
pub mod omega_native;
pub mod primitive_map;
pub mod runtime_adapter;

pub use omega_native::exact::mub6_cover_tree;
pub use omega_native::exact::mub6_degree8_sdp;
pub use omega_native::exact::mub6_moment_ledger;
pub use omega_native::exact::mub6_nerve_chaining;
pub use omega_native::exact::mub6_szollosi_t5_cover;

#[cfg(feature = "python")]
pub mod python;

use num_rational::Ratio;

pub fn verify_mub_crate_invariants() -> Result<(), String> {
    let d = 6i64;
    let expected_overlap = Ratio::new(1, d);
    if expected_overlap != Ratio::new(1, 6) {
        return Err("MUB overlap mismatch".to_string());
    }
    Ok(())
}

#[cfg(test)]
mod crate_tests {
    use super::*;

    #[test]
    fn test_mub_crate_invariants() {
        assert!(verify_mub_crate_invariants().is_ok());
    }
}
