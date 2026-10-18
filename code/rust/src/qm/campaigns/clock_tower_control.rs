//! Campaign module clock_tower_control.
//!
//! A 4-cycle clock returns to the identity at step 4, which is also the length
//! of its only cycle. The controlled clock acts as that cycle when the control
//! bit is 1 and as the identity when the control bit is 0.

pub fn verify() -> Result<usize, &'static str> {
    let clock = [1usize, 2, 3, 0];
    let by_iteration = order_of(&clock)?;
    let by_cycle = cycle_length(&clock)?;
    if by_iteration != by_cycle || by_iteration != 4 {
        return Err("clock order readings disagree");
    }
    for tick in 0..4 {
        let held = controlled(0, tick);
        if held != (0, tick) {
            return Err("control 0 did not hold the clock");
        }
        let advanced = controlled(1, tick);
        if advanced != (1, clock[tick]) {
            return Err("control 1 did not advance the clock");
        }
    }
    let mut tick = 0usize;
    for _ in 0..4 {
        tick = controlled(1, tick).1;
    }
    if tick != 0 {
        return Err("controlled clock did not close");
    }
    Ok(by_iteration)
}

fn order_of(perm: &[usize]) -> Result<usize, &'static str> {
    let n = perm.len();
    let mut state: Vec<usize> = (0..n).collect();
    for step in 1..=n {
        let mut next = vec![0usize; n];
        for (index, value) in state.iter().enumerate() {
            next[index] = *perm.get(*value).ok_or("perm")?;
        }
        state = next;
        if state.iter().enumerate().all(|(index, value)| *value == index) {
            return Ok(step);
        }
    }
    Err("permutation order exceeds its degree")
}

fn cycle_length(perm: &[usize]) -> Result<usize, &'static str> {
    let mut seen = vec![false; perm.len()];
    let mut length = 0usize;
    let mut cursor = 0usize;
    while !seen[cursor] {
        seen[cursor] = true;
        length += 1;
        cursor = *perm.get(cursor).ok_or("perm")?;
        if length > perm.len() {
            return Err("cycle did not close");
        }
    }
    if seen.iter().any(|hit| !*hit) || cursor != 0 {
        return Err("clock is not a single cycle");
    }
    Ok(length)
}

fn controlled(control: usize, tick: usize) -> (usize, usize) {
    if control == 0 {
        (0, tick)
    } else {
        (1, (tick + 1) % 4)
    }
}
