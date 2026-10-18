
pub fn evaluate_p1_kill(state_count: usize, distinct_decisions: usize, loss_cert_verified: bool) -> (bool, bool, bool, bool) {
    let kill_size = state_count > 64;
    let kill_decisions = distinct_decisions < 3;
    let kill_loss = !loss_cert_verified;
    let any_kill = kill_size || kill_decisions || kill_loss;
    (kill_size, kill_decisions, kill_loss, any_kill)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pilot_p1_kill_conditions_do_not_hold() {
        assert_eq!(evaluate_p1_kill(4, 3, true), (false, false, false, false));
        assert_eq!(evaluate_p1_kill(100, 3, true), (true, false, false, true));
        assert_eq!(evaluate_p1_kill(4, 1, true), (false, true, false, true));
        assert_eq!(evaluate_p1_kill(4, 3, false), (false, false, true, true));
    }
}
