//! Congruence Quotient & Observation Refinement Calculus (REV-SMRM-P1-QUOTIENT) exact verifier.

/// Checks whether a partition `obs` over states `0..n` respects deterministic transition table `next_state`
/// and state output `goal`.
pub fn is_congruence(obs: &[usize], next_state: &[usize], goal: &[u8]) -> bool {
    let n = obs.len();
    for i in 0..n {
        for j in (i + 1)..n {
            if obs[i] == obs[j] {
                if goal[i] != goal[j] {
                    return false;
                }
                if obs[next_state[i]] != obs[next_state[j]] {
                    return false;
                }
            }
        }
    }
    true
}

/// Refines `obs` until it is a congruence with respect to `next_state` and `goal`.
pub fn refine_observation(obs: &[usize], next_state: &[usize], goal: &[u8]) -> Vec<usize> {
    let n = obs.len();
    let mut current: Vec<usize> = obs.to_vec();
    loop {
        let mut signatures: Vec<(usize, u8, usize)> = Vec::with_capacity(n);
        for i in 0..n {
            signatures.push((current[i], goal[i], current[next_state[i]]));
        }
        let mut unique_sigs = signatures.clone();
        unique_sigs.sort_unstable();
        unique_sigs.dedup();
        let next_obs: Vec<usize> = signatures
            .iter()
            .map(|sig| unique_sigs.binary_search(sig).unwrap())
            .collect();
        if next_obs == current {
            return current;
        }
        current = next_obs;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quotient_congruence_and_refinement() {
        // States: 0 -> 1 -> 2 (goal=1), 2 -> 2
        let next_state = [1usize, 2, 2];
        let goal = [0u8, 0, 1];
        // Coarse observation merges 0 and 1 into class 0, 2 into class 1
        let coarse_obs = [0usize, 0, 1];
        assert!(!is_congruence(&coarse_obs, &next_state, &goal));

        let refined = refine_observation(&coarse_obs, &next_state, &goal);
        assert!(is_congruence(&refined, &next_state, &goal));
        assert_ne!(refined[0], refined[1]);
    }
}
