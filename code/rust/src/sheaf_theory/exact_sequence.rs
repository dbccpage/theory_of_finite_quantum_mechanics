
use crate::open_set::OpenSet;
use crate::presheaf::Presheaf;
use num_rational::Ratio;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};
use std::fmt::Debug;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ConnectingHomomorphismResult {
    pub h0_target_val: Ratio<i64>,
    pub connecting_coboundary_h1: Ratio<i64>,
    pub is_exact_at_boundary: bool,
}

pub fn connecting_homomorphism_delta_star(
    section_h: Ratio<i64>,
    lift_to_g: Ratio<i64>,
    overlap_difference: Ratio<i64>,
) -> ConnectingHomomorphismResult {
    ConnectingHomomorphismResult {
        h0_target_val: section_h,
        connecting_coboundary_h1: overlap_difference,
        is_exact_at_boundary: if lift_to_g == section_h {
            overlap_difference.is_zero()
        } else {
            true
        },
    }
}

pub fn is_flasque_sheaf<T: Clone + PartialEq + Debug>(
    presheaf: &Presheaf<T>,
    all_open_pairs: &[(OpenSet, OpenSet)],
) -> bool {
    for (u, v) in all_open_pairs {
        if !v.is_subset(u) {
            continue;
        }
        let u_secs = presheaf.sections(u);
        let v_secs = presheaf.sections(v);
        let mut restricted_v = BTreeSet::new();
        for s in u_secs {
            if let Ok(res) = presheaf.restrict(u, v, s) {
                restricted_v.insert(format!("{res:?}"));
            }
        }
        for vs in v_secs {
            if !restricted_v.contains(&format!("{vs:?}")) {
                return false;
            }
        }
    }
    true
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PartitionOfUnity {
    pub cover: Vec<OpenSet>,
    pub weights: BTreeMap<(usize, String), Ratio<i64>>,
}

impl PartitionOfUnity {
    pub fn new(
        cover: Vec<OpenSet>,
        weights: impl IntoIterator<Item = ((usize, impl Into<String>), Ratio<i64>)>,
    ) -> Self {
        let mut map = BTreeMap::new();
        for ((idx, pt), w) in weights {
            map.insert((idx, pt.into()), w);
        }
        Self {
            cover,
            weights: map,
        }
    }

    pub fn verify_sum_to_one(&self, points: &BTreeSet<String>) -> bool {
        let one = Ratio::from_integer(1);
        let zero = Ratio::from_integer(0);
        for p in points {
            let mut sum = zero;
            for i in 0..self.cover.len() {
                let w = self.weights.get(&(i, p.clone())).copied().unwrap_or(zero);
                sum += w;
            }
            if sum != one {
                return false;
            }
        }
        true
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LocalToGlobalSpectralSequencePage {
    pub e2_table: BTreeMap<(usize, usize), usize>,
}

impl LocalToGlobalSpectralSequencePage {
    pub fn new(e2_table: impl IntoIterator<Item = ((usize, usize), usize)>) -> Self {
        Self {
            e2_table: e2_table.into_iter().collect(),
        }
    }

    pub fn total_cohomology_bound(&self, degree: usize) -> usize {
        self.e2_table
            .iter()
            .filter(|&(&(p, q), _)| p + q == degree)
            .map(|(_, &dim)| dim)
            .sum()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_partition_of_unity() {
        let u0 = OpenSet::new(vec!["p1", "p2"]);
        let u1 = OpenSet::new(vec!["p2", "p3"]);
        let cover = vec![u0, u1];

        let half = Ratio::new(1, 2);
        let one = Ratio::from_integer(1);
        let zero = Ratio::from_integer(0);

        let pou = PartitionOfUnity::new(
            cover,
            vec![
                ((0, "p1"), one),
                ((1, "p1"), zero),
                ((0, "p2"), half),
                ((1, "p2"), half),
                ((0, "p3"), zero),
                ((1, "p3"), one),
            ],
        );

        let mut pts = BTreeSet::new();
        pts.insert("p1".to_string());
        pts.insert("p2".to_string());
        pts.insert("p3".to_string());
        assert!(pou.verify_sum_to_one(&pts));
    }
}
