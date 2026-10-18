
pub fn evaluate_p5_kill(ci_executed: bool, proved_missing_d3_count: usize) -> (bool, bool, bool) {
    let kill_1 = !ci_executed;
    let kill_2 = proved_missing_d3_count > 0;
    let any_kill = kill_1 || kill_2;
    (kill_1, kill_2, any_kill)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pilot_p5_kill_conditions_do_not_hold() {
        assert_eq!(evaluate_p5_kill(true, 0), (false, false, false));
        assert_eq!(evaluate_p5_kill(false, 0), (true, false, true));
        assert_eq!(evaluate_p5_kill(true, 1), (false, true, true));
    }
}
