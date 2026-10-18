//! Companion Rust witness for PROD-P4-KILL (Evaluate P4 kill conditions on pilot instrument menus).

pub fn evaluate_p4_kill(solver_finished: bool, planned_cost_num: u64, planned_cost_den: u64, buyer_cost_num: u64, buyer_cost_den: u64) -> (bool, bool, bool) {
    let kill_exceeds_solver = !solver_finished;
    let kill_never_differs = planned_cost_num * buyer_cost_den >= buyer_cost_num * planned_cost_den;
    let any_kill = kill_exceeds_solver || kill_never_differs;
    (kill_exceeds_solver, kill_never_differs, any_kill)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pilot_p4_kill_conditions_do_not_hold() {
        assert_eq!(evaluate_p4_kill(true, 7, 2, 5, 1), (false, false, false));
        assert_eq!(evaluate_p4_kill(false, 7, 2, 5, 1), (true, false, true));
        assert_eq!(evaluate_p4_kill(true, 5, 1, 5, 1), (false, true, true));
    }
}
