
use crate::open_set::OpenSet;
use num_rational::Ratio;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CechCochain {
    pub degree: usize,
    pub data: BTreeMap<Vec<usize>, Ratio<i64>>,
}

impl CechCochain {
    pub fn new(degree: usize, data: BTreeMap<Vec<usize>, Ratio<i64>>) -> Self {
        Self { degree, data }
    }

    pub fn get(&self, indices: &[usize]) -> Ratio<i64> {
        self.data
            .get(indices)
            .copied()
            .unwrap_or_else(|| Ratio::from_integer(0))
    }

    pub fn is_zero(&self) -> bool {
        self.data.values().all(|v| v.is_zero())
    }
}

pub fn cech_coboundary_rational(cochain: &CechCochain, cover: &[OpenSet]) -> CechCochain {
    let p = cochain.degree;
    let p_next = p + 1;
    let n = cover.len();
    let mut next_data = BTreeMap::new();

    fn combinations(n: usize, k: usize) -> Vec<Vec<usize>> {
        if k == 0 {
            return vec![vec![]];
        }
        if n < k {
            return vec![];
        }
        let mut res = Vec::new();
        for i in 0..n {
            for mut tail in combinations(i, k - 1) {
                tail.push(i);
                res.push(tail);
            }
        }
        res
    }

    let all_combos = combinations(n, p_next + 1);
    for mut indices in all_combos {
        indices.sort();

        let mut inter = cover[indices[0]].clone();
        for &idx in &indices[1..] {
            inter = inter.intersection(&cover[idx]);
        }
        if inter.is_empty() {
            continue;
        }

        let mut val = Ratio::from_integer(0);
        for k in 0..=p_next {
            let mut face_indices = indices.clone();
            face_indices.remove(k);
            let face_val = cochain.get(&face_indices);
            if k % 2 == 1 {
                val -= face_val;
            } else {
                val += face_val;
            }
        }

        next_data.insert(indices, val);
    }

    CechCochain::new(p_next, next_data)
}

pub fn compute_cech_h0(cover: &[OpenSet], constant_val: Ratio<i64>) -> Option<CechCochain> {
    let mut data = BTreeMap::new();
    for i in 0..cover.len() {
        data.insert(vec![i], constant_val);
    }
    let c0 = CechCochain::new(0, data);
    let d_c0 = cech_coboundary_rational(&c0, cover);
    if d_c0.is_zero() {
        Some(c0)
    } else {
        None
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CechH1Result {
    pub dim_h1: usize,
    pub is_trivial: bool,
    pub representative_obstruction: Option<CechCochain>,
}

pub fn compute_cech_h1_obstruction(
    cover: &[OpenSet],
    transition_1_cocycle: BTreeMap<Vec<usize>, Ratio<i64>>,
) -> Result<CechH1Result, String> {
    use omega_homology::scalar::inject_rational64;
    use omega_homology::simplicial::{Simplex, SimplicialComplex};
    use omega_homology::trichotomy_witness::{is_coboundary, is_cocycle};

    let n = cover.len();
    let mut simplices = Vec::new();
    for i in 0..n {
        if cover[i].is_empty() {
            continue;
        }
        simplices.push(Simplex::new(vec![i]).map_err(|e| e.to_string())?);
        for j in i + 1..n {
            let pair = cover[i].intersection(&cover[j]);
            if pair.is_empty() {
                continue;
            }
            simplices.push(Simplex::new(vec![i, j]).map_err(|e| e.to_string())?);
            for (k, item) in cover.iter().enumerate().skip(j + 1) {
                if !pair.intersection(item).is_empty() {
                    simplices.push(Simplex::new(vec![i, j, k]).map_err(|e| e.to_string())?);
                }
            }
        }
    }
    let nerve = SimplicialComplex::from_simplices(simplices).map_err(|e| e.to_string())?;
    for key in transition_1_cocycle.keys() {
        if key.len() != 2 || !nerve.simplices(1).iter().any(|edge| edge.vertices() == key) {
            return Err("cochain key is not an oriented nonempty nerve edge".into());
        }
    }
    let c1 = CechCochain::new(1, transition_1_cocycle);
    let values: Vec<_> = nerve
        .simplices(1)
        .iter()
        .map(|edge| inject_rational64(c1.get(edge.vertices())))
        .collect();
    let d0 = nerve.coboundary_matrix(0).map_err(|e| e.to_string())?;
    let d1 = nerve.coboundary_matrix(1).map_err(|e| e.to_string())?;
    if !is_cocycle(&d1, &values).map_err(|e| e.to_string())? {
        return Err("Provided 1-cochain is not a 1-cocycle".into());
    }
    let is_trivial = is_coboundary(&d0, &values).map_err(|e| e.to_string())?;
    let betti = nerve.rational_betti_numbers().map_err(|e| e.to_string())?;
    Ok(CechH1Result {
        dim_h1: betti.get(1).copied().unwrap_or(0),
        is_trivial,
        representative_obstruction: if is_trivial { None } else { Some(c1) },
    })
}

pub fn check_h1_vanishing_on_intersections(
    cover: &[OpenSet],
    h1_vanishing_oracle: impl Fn(&OpenSet) -> bool,
) -> bool {
    let mut intersections = std::collections::BTreeSet::new();
    for item in cover {
        let mut added = vec![item.clone()];
        added.extend(
            intersections
                .iter()
                .map(|old: &OpenSet| old.intersection(item)),
        );
        for intersection in added {
            if !intersection.is_empty()
                && intersections.insert(intersection.clone())
                && !h1_vanishing_oracle(&intersection)
            {
                return false;
            }
        }
    }
    true
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cech_coboundary_nilpotency() {
        let u0 = OpenSet::new(vec!["0", "1"]);
        let u1 = OpenSet::new(vec!["1", "2"]);
        let u2 = OpenSet::new(vec!["2", "0"]);
        let cover = vec![u0, u1, u2];

        let mut data0 = BTreeMap::new();
        data0.insert(vec![0], Ratio::from_integer(1));
        data0.insert(vec![1], Ratio::from_integer(2));
        data0.insert(vec![2], Ratio::from_integer(5));
        let c0 = CechCochain::new(0, data0);

        let c1 = cech_coboundary_rational(&c0, &cover);
        let c2 = cech_coboundary_rational(&c1, &cover);
        assert!(c2.is_zero());
    }

    #[test]
    fn test_cech_h1_obstruction_detection() {
        let u0 = OpenSet::new(vec!["0", "1"]);
        let u1 = OpenSet::new(vec!["1", "2"]);
        let u2 = OpenSet::new(vec!["2", "0"]);
        let cover = vec![u0, u1, u2];

        let mut data1 = BTreeMap::new();
        data1.insert(vec![0, 1], Ratio::from_integer(1));
        data1.insert(vec![1, 2], Ratio::from_integer(1));
        data1.insert(vec![0, 2], Ratio::from_integer(0));

        let res = compute_cech_h1_obstruction(&cover, data1).unwrap();
        assert!(!res.is_trivial);
        assert_eq!(res.dim_h1, 1);
    }
}
