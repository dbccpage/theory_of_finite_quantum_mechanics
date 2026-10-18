//! Companion Rust witness crate for `WDP-APPX-REPORT-DOMAIN`:
//! Aligns calibrated model admission and bounded raw report semantics.
//! AuthorityEffect: None.

pub const COST_DOMAIN: &str = "ideal_calibrated_interval_product";
pub const MAX_RAW_BITS: u32 = 256;

/// Checks whether a point interval `[y_pow2, y_pow2]` with `offset = 0` and
/// `gain = 2^(-gain_neg_pow2)` has a raw reading `r = y / gain = 2^(y_pow2 + gain_neg_pow2)`
/// within the 256-bit parser cap (`<= 2^256`).
pub fn point_cell_raw_bits(y_pow2: u32, gain_neg_pow2: u32) -> u32 {
    y_pow2.saturating_add(gain_neg_pow2)
}

pub fn is_executable_under_256bit_cap(y_pow2: u32, gain_neg_pow2: u32) -> bool {
    point_cell_raw_bits(y_pow2, gain_neg_pow2) <= MAX_RAW_BITS
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct R1AlignmentSummary {
    pub cost_domain: &'static str,
    pub ideal_fixed_cost: u32,
    pub ideal_adaptive_cost: u32,
    pub high_cell_raw_exponent: u32,
    pub executable_raw_domain_admissible: bool,
    pub raw_2_510_status: &'static str,
    pub authority_effect: &'static str,
}

pub fn evaluate_r1_witness() -> R1AlignmentSummary {
    let exp = point_cell_raw_bits(255, 255);
    let admissible = is_executable_under_256bit_cap(255, 255);
    R1AlignmentSummary {
        cost_domain: COST_DOMAIN,
        ideal_fixed_cost: 1,
        ideal_adaptive_cost: 1,
        high_cell_raw_exponent: exp,
        executable_raw_domain_admissible: admissible,
        raw_2_510_status: if admissible { "SUPPORTED_MATCH" } else { "INVALID_REPORT" },
        authority_effect: "None",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_r1_witness_alignment() {
        let s = evaluate_r1_witness();
        assert_eq!(s.cost_domain, "ideal_calibrated_interval_product");
        assert_eq!(s.ideal_fixed_cost, 1);
        assert_eq!(s.ideal_adaptive_cost, 1);
        assert_eq!(s.high_cell_raw_exponent, 510);
        assert!(!s.executable_raw_domain_admissible);
        assert_eq!(s.raw_2_510_status, "INVALID_REPORT");
        assert_eq!(s.authority_effect, "None");
    }

    #[test]
    fn test_cap_boundary_255_vs_257() {
        // y = 2^128, gain = 2^-127 => raw = 2^255 (within 2^256 cap)
        assert!(is_executable_under_256bit_cap(128, 127));
        // y = 2^128, gain = 2^-128 => raw = 2^256 (exact boundary of 2^256 cap)
        assert!(is_executable_under_256bit_cap(128, 128));
        // y = 2^129, gain = 2^-128 => raw = 2^257 (exceeds 2^256 cap)
        assert!(!is_executable_under_256bit_cap(129, 128));
    }
}
