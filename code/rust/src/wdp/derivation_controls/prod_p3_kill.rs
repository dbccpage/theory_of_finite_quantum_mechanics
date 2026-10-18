//! Companion Rust witness for PROD-P3-KILL (Evaluate P3 kill conditions on pilot workloads).

pub fn evaluate_p3_kill(saving_num: i64, transfer_sound: bool) -> (bool, bool, bool) {
    let kill_no_benefit = saving_num <= 0;
    let kill_unsound = !transfer_sound;
    let any_kill = kill_no_benefit || kill_unsound;
    (kill_no_benefit, kill_unsound, any_kill)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pilot_p3_kill_conditions_do_not_hold() {
        assert_eq!(evaluate_p3_kill(1, true), (false, false, false));
        assert_eq!(evaluate_p3_kill(0, true), (true, false, true));
        assert_eq!(evaluate_p3_kill(1, false), (false, true, true));
    }
}
