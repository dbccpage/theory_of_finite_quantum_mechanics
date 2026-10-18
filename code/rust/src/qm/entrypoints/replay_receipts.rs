//! Entrypoint: replay_receipts.
//!
//! A receipt is an initial integer state and a list of additions. Replaying
//! forward must meet the recorded final state, and walking the same additions
//! backward from that final state must recover the initial state.

pub fn run_replay_receipts() -> Result<(), String> {
    let initial = 5i64;
    let steps = [3i64, -8, 4, 1];
    let recorded_final = 5i64;
    let replayed = replay_forward(initial, &steps)?;
    if replayed != recorded_final {
        return Err(format!(
            "forward replay {replayed} does not match the receipt {recorded_final}"
        ));
    }
    let unwound = replay_backward(replayed, &steps)?;
    if unwound != initial {
        return Err(format!(
            "backward replay {unwound} does not recover the initial state {initial}"
        ));
    }
    Ok(())
}

fn replay_forward(mut state: i64, steps: &[i64]) -> Result<i64, String> {
    for step in steps {
        state = state.checked_add(*step).ok_or("replay overflow")?;
    }
    Ok(state)
}

fn replay_backward(mut state: i64, steps: &[i64]) -> Result<i64, String> {
    for step in steps.iter().rev() {
        state = state.checked_sub(*step).ok_or("replay overflow")?;
    }
    Ok(state)
}
