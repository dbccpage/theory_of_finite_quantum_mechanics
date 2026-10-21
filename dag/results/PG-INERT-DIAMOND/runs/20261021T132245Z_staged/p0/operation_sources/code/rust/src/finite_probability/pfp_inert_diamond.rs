//! The inert inscription <>: exhaustive event traces of a finite admission model.
//!
//! Exact integer replay of `code/python/src/qm/pfp_inert_diamond.py` for PFP batch 01, node PG-INERT-DIAMOND
//! (a definition node: the result is consistency and independence of the definition). Tokens 0 = "<>",
//! 1 = a Difference datum, 2 = a Structure datum. Events: supply (mention), admit datum, admit form.
//! Supply never changes the state in the model; the rival rule makes supply admit. Finite instances only;
//! the general statements are the Lean module InertDiamond. AuthorityEffect: None.
use std::collections::HashSet;

type State = (Vec<u8>, Vec<u8>);
type Ev = (char, u8);

const EVENTS: [Ev; 8] = [('s', 0), ('s', 1), ('s', 2), ('a', 0), ('a', 1), ('a', 2), ('f', 0), ('f', 1)];
const SUPPLY0: Ev = ('s', 0);
const ADMIT0: Ev = ('a', 0);

fn init() -> State {
    (Vec::new(), Vec::new())
}

fn admit(state: &State, t: u8) -> State {
    if state.0.contains(&t) {
        state.clone()
    } else {
        let mut data = state.0.clone();
        data.push(t);
        (data, state.1.clone())
    }
}

/// The model: supply is the identity; admit designates; form 0 is refused.
pub fn step(state: &State, ev: Ev) -> Option<State> {
    match ev.0 {
        's' => Some(state.clone()),
        'a' => Some(admit(state, ev.1)),
        _ => {
            if ev.1 < 1 {
                None
            } else {
                let mut forms = state.1.clone();
                forms.push(ev.1);
                Some((state.0.clone(), forms))
            }
        }
    }
}

/// Rival rule: supply of a token admits it.
pub fn rival_step(state: &State, ev: Ev) -> Option<State> {
    if ev.0 == 's' {
        Some(admit(state, ev.1))
    } else {
        step(state, ev)
    }
}

fn run(trace: &[Ev], start: &State, rival: bool) -> Option<State> {
    let mut state = start.clone();
    for &ev in trace {
        state = if rival { rival_step(&state, ev)? } else { step(&state, ev)? };
    }
    Some(state)
}

fn has_coproduct(state: &State) -> bool {
    // class of token 1 is Difference, of token 2 is Structure, of token 0 none
    state.0.contains(&1) && state.0.contains(&2)
}

pub const FIELDS: usize = 22;

/// Counts in the order of the Python `FIELDS`.
pub fn record(max_len: usize) -> [u64; FIELDS] {
    let mut c = [0u64; FIELDS];
    let mut finals: HashSet<State> = HashSet::new();
    for n in 0..=max_len {
        let total = 8usize.pow(n as u32);
        for code in 0..total {
            let mut trace: Vec<Ev> = Vec::with_capacity(n);
            let mut rest = code;
            for _ in 0..n {
                trace.push(EVENTS[rest % 8]);
                rest /= 8;
            }
            c[0] += 1;
            let final_state = run(&trace, &init(), false);
            let kept: Vec<Ev> = trace.iter().copied().filter(|e| e.0 != 's').collect();
            let filtered = run(&kept, &init(), false);
            c[3] += (final_state != filtered) as u64;
            let inscribed = trace.contains(&SUPPLY0);
            let supply_only = trace.iter().all(|e| e.0 == 's');
            if supply_only {
                c[4] += 1;
                c[5] += (final_state != Some(init())) as u64;
                if n >= 1 {
                    c[18] += (run(&trace, &init(), true) != Some(init())) as u64;
                }
            }
            let rooted = n >= 1 && trace[0] == SUPPLY0 && final_state.is_some();
            c[2] += rooted as u64;
            let rooted_out = if n >= 1 && trace[0] == SUPPLY0 { run(&trace[1..], &init(), false) } else { None };
            if n >= 1 && trace[0] == SUPPLY0 {
                let mut kept_first: Vec<Ev> = vec![trace[0]];
                kept_first.extend(trace[1..].iter().copied().filter(|e| e.0 != 's'));
                let rooted_kept = run(&kept_first[1..], &init(), false);
                c[19] += (rooted_out != rooted_kept) as u64;
                let tail = &trace[1..];
                let omitted = if !tail.is_empty() && tail[0] == SUPPLY0 { run(&tail[1..], &init(), false) } else { None };
                if rooted_out.is_some() && omitted.is_none() {
                    c[20] += 1;
                }
            }
            c[21] += (rooted_out.is_none() && final_state.is_some()) as u64;
            let root_only = trace.iter().all(|e| *e == SUPPLY0 || *e == ADMIT0);
            if root_only {
                c[14] += 1;
            }
            let start = step(&init(), SUPPLY0).unwrap();
            c[16] += (final_state != run(&trace, &start, false)) as u64;
            let rival_start = rival_step(&init(), SUPPLY0).unwrap();
            c[17] += (run(&trace, &init(), true) != run(&trace, &rival_start, true)) as u64;
            let state = match final_state {
                None => {
                    c[1] += 1;
                    continue;
                }
                Some(s) => s,
            };
            c[6] += (state != init()) as u64;
            let cop = has_coproduct(&state);
            c[8] += cop as u64;
            if root_only && cop {
                c[15] += 1;
            }
            if inscribed {
                if cop {
                    c[10] += 1;
                } else {
                    c[9] += 1;
                }
            } else if cop {
                c[11] += 1;
            }
            if rooted {
                if cop {
                    c[12] += 1;
                } else {
                    c[13] += 1;
                }
            }
            finals.insert(state);
        }
    }
    c[7] = finals.len() as u64;
    c
}

/// Wire line identical to the Python `wire_lines` format.
pub fn line(max_len: usize) -> String {
    let c = record(max_len);
    let mut fields = vec!["inert".to_string(), max_len.to_string()];
    fields.extend(c.iter().map(|x| x.to_string()));
    fields.join("\t")
}

/// Replay one tab-separated public-input line `inert\tL`.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "inert" {
        return None;
    }
    let max_len: usize = parts.next()?.parse().ok()?;
    if parts.next().is_some() || max_len > 6 {
        return None;
    }
    Some(line(max_len))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_inert_diamond_closed_form_trace_counts() {
        for l in 0..5usize {
            let c = record(l);
            assert_eq!(c[0] as usize, (8usize.pow(l as u32 + 1) - 1) / 7);
            assert_eq!(c[4] as usize, (3usize.pow(l as u32 + 1) - 1) / 2);
            assert_eq!(c[14] as usize, 2usize.pow(l as u32 + 1) - 1);
        }
    }

    #[test]
    fn pfp_inert_diamond_supply_is_invisible_and_rival_is_not() {
        let c = record(4);
        assert_eq!(c[3], 0);
        assert_eq!(c[5], 0);
        assert_eq!(c[16], 0);
        assert_eq!(c[15], 0);
        assert!(c[17] > 0 && c[18] > 0);
        assert_eq!(c[19], 0);
        assert!(c[20] > 0 && c[21] > 0);
    }

    #[test]
    fn pfp_inert_diamond_inscription_and_coproduct_independent() {
        let both = run(&[SUPPLY0, ('a', 1), ('a', 2)], &init(), false).unwrap();
        let only = run(&[SUPPLY0], &init(), false).unwrap();
        let without = run(&[('a', 1), ('a', 2)], &init(), false).unwrap();
        assert!(has_coproduct(&both) && !has_coproduct(&only) && has_coproduct(&without));
        assert_eq!(run(&[('f', 0)], &init(), false), None);
        assert_eq!(run(&[('a', 1), ('a', 1)], &init(), false).unwrap().0, vec![1u8]);
    }

    #[test]
    fn pfp_inert_diamond_wire_line() {
        assert_eq!(replay("inert\t1").unwrap(), "inert\t1\t9\t1\t1\t0\t4\t0\t4\t5\t0\t1\t0\t0\t0\t1\t3\t0\t0\t6\t3\t0\t1\t7");
        assert!(replay("report\t1").is_none());
    }
}
