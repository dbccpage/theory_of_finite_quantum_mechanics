
pub fn evaluate_kernel_kill(arena_declared: bool, initial_value: u64, usable_budget: u64, receipt_replayed: bool) -> (bool, bool, bool) {
    let kill_no_finite_arena = !(arena_declared && initial_value <= usable_budget);
    let kill_receipts_unreplayed = !receipt_replayed;
    let any_kill = kill_no_finite_arena || kill_receipts_unreplayed;
    (kill_no_finite_arena, kill_receipts_unreplayed, any_kill)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pilot_kernel_kill_conditions_do_not_hold() {
        assert_eq!(evaluate_kernel_kill(true, 3, 3, true), (false, false, false));
        assert_eq!(evaluate_kernel_kill(false, 3, 3, true), (true, false, true));
        assert_eq!(evaluate_kernel_kill(true, 3, 3, false), (false, true, true));
    }
}
