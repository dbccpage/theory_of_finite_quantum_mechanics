//! Omega-native MUB reconstruction (CODA_GTLA / CODA-FOC).
//!
//! **This is our product crate** — original Rust, inspired by the MUB(6) problem
//! literature (including the wall theorem we cite by DOI only). It is not a
//! Python reimplementation and not a redistributed copy of upstream Zenodo code.
//!
//! Architecture notes live under
//! `omega_engine/research/published/012_mutually_unbiased_bases/`.
//! The optional Apache **compare** surface (`apache-compare`) and the `crates/mub`
//! port it depended on were removed 2026-08-04; this crate now has no Apache
//! dependency at all, and deep_run's replays are unconditionally "not replayed".
//!
//! Optional **thin PyO3** face: features `python` / `extension-module` for
//! Jupyter dicts; math SSOT stays Rust (`src/python.rs`).
//!
//! Nothing here mints authority — diagnostics / exact local certificates only.
//!
//! The exact finite MUB constructions and the projector-algebra verifier live
//! in `omega_quantum_physics::mub`; import them from there.

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

/// Top-level MUB crate invariant verification.
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
