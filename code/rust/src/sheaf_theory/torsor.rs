//! Torsors and principal G-sheaves (SH-19).
//!
//! AuthorityEffect: None.

use crate::open_set::OpenSet;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// A Z_2-torsor (principal Z_2-bundle) on a simplicial complex (SH-19).
///
/// Classified by H^1(X, Z_2). Transition signs on pairwise overlaps are +1 or -1.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PrincipalBundleZ2 {
    pub cover: Vec<OpenSet>,
    /// Transition signs for sorted pairs (i, j) where i < j
    pub transition_signs: BTreeMap<(usize, usize), i8>,
}

impl PrincipalBundleZ2 {
    pub fn new(
        cover: Vec<OpenSet>,
        transition_signs: impl IntoIterator<Item = ((usize, usize), i8)>,
    ) -> Result<Self, String> {
        let mut map = BTreeMap::new();
        for ((i, j), sign) in transition_signs {
            if sign != 1 && sign != -1 {
                return Err(format!(
                    "Invalid Z_2 transition sign {sign}: must be +1 or -1"
                ));
            }
            let key = if i < j { (i, j) } else { (j, i) };
            map.insert(key, sign);
        }
        Ok(Self {
            cover,
            transition_signs: map,
        })
    }

    /// Compute holonomy along a cyclic sequence of cover indices: prod_{k} g_{i_k, i_{k+1}}.
    pub fn holonomy_around_loop(&self, loop_indices: &[usize]) -> i8 {
        if loop_indices.is_empty() {
            return 1;
        }
        let mut holo: i8 = 1;
        let n = loop_indices.len();
        for k in 0..n {
            let i = loop_indices[k];
            let j = loop_indices[(k + 1) % n];
            if i == j {
                continue;
            }
            let key = if i < j { (i, j) } else { (j, i) };
            let sign = self.transition_signs.get(&key).copied().unwrap_or(1);
            holo *= sign;
        }
        holo
    }

    /// Trivial bundle check: holonomy around canonical cycle is +1.
    pub fn is_trivial_bundle(&self) -> bool {
        let full_cycle: Vec<usize> = (0..self.cover.len()).collect();
        self.holonomy_around_loop(&full_cycle) == 1
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mobius_bundle_non_trivial_holonomy() {
        let u0 = OpenSet::new(vec!["0", "1"]);
        let u1 = OpenSet::new(vec!["1", "2"]);
        let u2 = OpenSet::new(vec!["2", "0"]);

        // Möbius transition: one flip (-1) along the wrap-around
        let bundle = PrincipalBundleZ2::new(
            vec![u0, u1, u2],
            vec![((0, 1), 1), ((1, 2), 1), ((0, 2), -1)],
        )
        .unwrap();

        assert_eq!(bundle.holonomy_around_loop(&[0, 1, 2]), -1);
        assert!(!bundle.is_trivial_bundle());
    }
}
