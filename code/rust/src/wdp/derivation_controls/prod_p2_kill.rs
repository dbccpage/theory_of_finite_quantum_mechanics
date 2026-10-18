//! Companion Rust witness for PROD-P2-KILL (Evaluate P2 kill conditions: G.5 pass share, failure-list use).

pub fn evaluate_p2_kill(initial_passed: usize, batch_size: usize, repaired_passed: bool) -> (bool, bool, bool) {
    let kill_low_share = batch_size == 0 || (initial_passed * 2 < batch_size);
    let kill_failures_ignored = !repaired_passed;
    let any_kill = kill_low_share || kill_failures_ignored;
    (kill_low_share, kill_failures_ignored, any_kill)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pilot_p2_kill_conditions_do_not_hold() {
        assert_eq!(evaluate_p2_kill(3, 4, true), (false, false, false));
        assert_eq!(evaluate_p2_kill(1, 4, true), (true, false, true));
        assert_eq!(evaluate_p2_kill(3, 4, false), (false, true, true));
    }
}
