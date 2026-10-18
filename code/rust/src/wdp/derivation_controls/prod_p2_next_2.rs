//! Companion Rust witness for PROD-P2-NEXT-2 (Fixture per G.5 step failing exclusively that step).

pub const G5_STEPS: [&str; 12] = [
    "G.5.1", "G.5.2", "G.5.3", "G.5.4", "G.5.5", "G.5.6",
    "G.5.7", "G.5.8", "G.5.9", "G.5.10", "G.5.11", "G.5.12",
];

pub fn evaluate_single_step_fixture(step_flags: &[bool; 12]) -> Vec<&'static str> {
    G5_STEPS
        .iter()
        .zip(step_flags.iter())
        .filter_map(|(step, &passed)| if !passed { Some(*step) } else { None })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn each_g5_fixture_fails_exclusively_its_target_step() {
        for idx in 0..12 {
            let mut flags = [true; 12];
            flags[idx] = false;
            let failures = evaluate_single_step_fixture(&flags);
            assert_eq!(failures, vec![G5_STEPS[idx]]);
        }
    }
}
