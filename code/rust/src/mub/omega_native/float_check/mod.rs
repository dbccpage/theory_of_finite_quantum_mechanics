//! float check modules for the omega-native MUB lane.
#![allow(clippy::module_inception)]
#[path = "../d10_gtfoc_cross_validation.rs"]
pub mod d10_gtfoc_cross_validation;
#[path = "../d10_wall_status.rs"]
pub mod d10_wall_status;
#[path = "../d6_gtfoc_wall_cross_validation.rs"]
pub mod d6_gtfoc_wall_cross_validation;
#[path = "../d6_sos_float_sdp.rs"]
pub mod d6_sos_float_sdp;
#[path = "../gtfoc_float_wall.rs"]
pub mod gtfoc_float_wall;

/// Zero-float policy auditor ensuring zero IEEE-754 floats in exact verification paths.
pub fn assert_zero_float_bytes(source_bytes: &[u8]) -> Result<(), String> {
    let forbidden = [b"f32", b"f64", b"binary64", b"f128"];
    for needle in &forbidden {
        if source_bytes.windows(needle.len()).any(|w| w == *needle) {
            return Err(format!("Forbidden float type detected in source"));
        }
    }
    Ok(())
}

#[cfg(test)]
mod float_tests {
    use super::*;

    #[test]
    fn test_zero_float_policy() {
        assert!(assert_zero_float_bytes(b"let x: Ratio<i64> = Ratio::one();").is_ok());
        assert!(assert_zero_float_bytes(b"let x: f64 = 1.0;").is_err());
    }
}
