
use crate::open_set::OpenSet;
use crate::presheaf::Presheaf;
use serde::{Deserialize, Serialize};
use std::fmt::Debug;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SheafConditionResult<T> {
    pub is_sheaf: bool,
    pub is_separated: bool,
    pub unmatched_family: Option<Vec<(OpenSet, T)>>,
    pub witness_global_section: Option<T>,
}

pub fn check_separated<T: Clone + PartialEq + Debug>(
    presheaf: &Presheaf<T>,
    u: &OpenSet,
    cover: &[OpenSet],
) -> (bool, Option<(T, T)>) {
    let secs = presheaf.sections(u);
    for i in 0..secs.len() {
        for j in (i + 1)..secs.len() {
            let s1 = &secs[i];
            let s2 = &secs[j];
            let mut agree_on_all = true;
            for u_i in cover {
                let r1 = presheaf.restrict(u, u_i, s1);
                let r2 = presheaf.restrict(u, u_i, s2);
                match (r1, r2) {
                    (Ok(v1), Ok(v2)) if v1 == v2 => {}
                    _ => {
                        agree_on_all = false;
                        break;
                    }
                }
            }
            if agree_on_all && s1 != s2 {
                return (false, Some((s1.clone(), s2.clone())));
            }
        }
    }
    (true, None)
}

pub fn compute_equalizer_kernel<T: Clone + PartialEq + Debug>(
    presheaf: &Presheaf<T>,
    cover: &[OpenSet],
) -> Vec<Vec<T>> {
    let cover_secs: Vec<&[T]> = cover.iter().map(|u_i| presheaf.sections(u_i)).collect();
    if cover_secs.iter().any(|s| s.is_empty()) {
        return Vec::new();
    }

    let mut families: Vec<Vec<T>> = vec![vec![]];
    for &secs in &cover_secs {
        let mut next_families = Vec::new();
        for fam in &families {
            for s in secs {
                let mut new_fam = fam.clone();
                new_fam.push(s.clone());
                next_families.push(new_fam);
            }
        }
        families = next_families;
    }

    let mut matching = Vec::new();
    for fam in families {
        let mut compat = true;
        for i in 0..cover.len() {
            for j in (i + 1)..cover.len() {
                let u_ij = cover[i].intersection(&cover[j]);
                if u_ij.is_empty() {
                    continue;
                }
                let r_i = presheaf.restrict(&cover[i], &u_ij, &fam[i]);
                let r_j = presheaf.restrict(&cover[j], &u_ij, &fam[j]);
                match (r_i, r_j) {
                    (Ok(vi), Ok(vj)) if vi == vj => {}
                    _ => {
                        compat = false;
                        break;
                    }
                }
            }
            if !compat {
                break;
            }
        }
        if compat {
            matching.push(fam);
        }
    }

    matching
}

pub fn check_sheaf_condition<T: Clone + PartialEq + Debug>(
    presheaf: &Presheaf<T>,
    u: &OpenSet,
    cover: &[OpenSet],
) -> SheafConditionResult<T> {
    let (sep_ok, _) = check_separated(presheaf, u, cover);
    if !sep_ok {
        return SheafConditionResult {
            is_sheaf: false,
            is_separated: false,
            unmatched_family: None,
            witness_global_section: None,
        };
    }

    let matching_families = compute_equalizer_kernel(presheaf, cover);
    let u_secs = presheaf.sections(u);

    for fam in &matching_families {
        let mut gluing_found = false;
        for s in u_secs {
            let mut glues = true;
            for (i, u_i) in cover.iter().enumerate() {
                match presheaf.restrict(u, u_i, s) {
                    Ok(res) if res == fam[i] => {}
                    _ => {
                        glues = false;
                        break;
                    }
                }
            }
            if glues {
                gluing_found = true;
                break;
            }
        }

        if !gluing_found {
            let unmatched: Vec<(OpenSet, T)> =
                cover.iter().cloned().zip(fam.iter().cloned()).collect();
            return SheafConditionResult {
                is_sheaf: false,
                is_separated: true,
                unmatched_family: Some(unmatched),
                witness_global_section: None,
            };
        }
    }

    SheafConditionResult {
        is_sheaf: true,
        is_separated: true,
        unmatched_family: None,
        witness_global_section: u_secs.first().cloned(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::open_set::PosetTopology;
    use std::collections::BTreeMap;

    #[test]
    fn test_sheaf_condition_on_disjoint_open_sets() {
        let top = PosetTopology::discrete(vec!["0", "1"]);
        let u0 = OpenSet::new(vec!["0"]);
        let u1 = OpenSet::new(vec!["1"]);
        let u01 = OpenSet::new(vec!["0", "1"]);

        let mut secs = BTreeMap::new();
        secs.insert(u0.clone(), vec!["val0".to_string()]);
        secs.insert(u1.clone(), vec!["val1".to_string()]);
        secs.insert(u01.clone(), vec!["val0_val1".to_string()]);

        let p = Presheaf::new("sheaf_demo", top, secs, |u, v, s| {
            if u.elements.len() == 2 && v.contains("0") && !v.contains("1") {
                "val0".to_string()
            } else if u.elements.len() == 2 && v.contains("1") && !v.contains("0") {
                "val1".to_string()
            } else {
                s.clone()
            }
        });

        let cover = vec![u0, u1];
        let res = check_sheaf_condition(&p, &u01, &cover);
        assert!(res.is_sheaf);
        assert!(res.is_separated);
    }
}
