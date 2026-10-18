//! Lexicographic permutations of a 4-tuple.
//!
//! Shared by the 5-cube facet charts and the Freudenthal path enumeration.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

pub(super) fn lex_permutations_4(items: [usize; 4]) -> Vec<[usize; 4]> {
    let mut state = PermuteState {
        chosen: [0; 4],
        used: [false; 4],
        out: Vec::with_capacity(24),
    };
    permute_lex(&items, 0, &mut state);
    state.out
}

struct PermuteState {
    chosen: [usize; 4],
    used: [bool; 4],
    out: Vec<[usize; 4]>,
}

fn permute_lex(items: &[usize; 4], depth: usize, state: &mut PermuteState) {
    if depth == 4 {
        state.out.push(state.chosen);
        return;
    }
    for index in 0..4 {
        if state.used[index] {
            continue;
        }
        state.used[index] = true;
        state.chosen[depth] = items[index];
        permute_lex(items, depth + 1, state);
        state.used[index] = false;
    }
}
