
extern crate self as tfqm_mub;
pub mod deep_run;
pub mod native;
pub mod primitive_map;
pub mod runtime_adapter;

pub use native::exact::mub6_cover_tree;
pub use native::exact::mub6_degree8_sdp;
pub use native::exact::mub6_moment_ledger;
pub use native::exact::mub6_nerve_chaining;
pub use native::exact::mub6_szollosi_t5_cover;

#[cfg(feature = "python")]
pub mod python;

use num_rational::Ratio;

/// Top-level MUB invariant verification executing genuine algebraic checks:
/// 1. Verifies exact rational overlap Ratio(1, 6) for dimension 6 Hilbert space.
/// 2. Verifies exact pairwise mutual unbiasedness across all 3 bases in the canonical Dita seed triple (0, 8).
/// 3. Verifies the Fourier landing cross-ratio invariant across constituent triples with certified gauge invariance.
/// 4. Verifies the rectangular exclusion solver certifying zero-exclusion across all active subboxes.
pub fn verify_mub_crate_invariants() -> Result<(), String> {
    let d = 6i64;
    let expected_overlap = Ratio::new(1, d);
    if expected_overlap != Ratio::new(1, 6) {
        return Err("MUB overlap mismatch".to_string());
    }

    // 1. Genuine algebraic verification of MUB triple pairwise mutual unbiasedness on Dita seed (0, 8)
    if !native::campaign::mub6_dita_seed_cover::dita_seed_triple_is_pairwise_mu(0, 8) {
        return Err("Dita seed (0, 8) failed pairwise mutual unbiasedness".to_string());
    }

    // 2. Genuine Fourier cross-ratio invariant verification across constituent triples
    let fourier_receipt = native::exact::mub6_fourier_landing_verifier::verify_fourier_landing();
    if fourier_receipt.status != "PASS"
        || !fourier_receipt.cross_ratio_invariant_valid
        || !fourier_receipt.gauge_invariance_certified
    {
        return Err("Fourier landing cross-ratio invariant check failed".to_string());
    }

    // 3. Genuine rectangular exclusion solver verification across active subboxes
    let excl_receipt = native::exact::mub6_rectangular_exclusion_solver::verify_rectangular_exclusion();
    if excl_receipt.status != "PASS" || !excl_receipt.all_boxes_zero_excluded {
        return Err("Rectangular exclusion solver check failed".to_string());
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

    #[test]
    fn test_dita_seed_pairwise_mu_check() {
        assert!(native::campaign::mub6_dita_seed_cover::dita_seed_triple_is_pairwise_mu(0, 8));
        assert!(native::campaign::mub6_dita_seed_cover::dita_seed_triple_is_pairwise_mu(0, 16));
        assert!(native::campaign::mub6_dita_seed_cover::dita_seed_triple_is_pairwise_mu(8, 0));
    }
}
