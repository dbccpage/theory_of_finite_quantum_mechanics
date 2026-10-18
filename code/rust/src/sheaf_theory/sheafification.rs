//! Grothendieck plus-construction and sheafification functor F^# = (F^+)^+ (SH-09, SH-10, SH-11, SH-12).
//!
//! AuthorityEffect: None.

use crate::open_set::{OpenSet, PosetTopology};
use crate::presheaf::Presheaf;
use crate::sheaf::compute_equalizer_kernel;
use std::collections::BTreeMap;
use std::fmt::Debug;

/// Grothendieck's plus-construction F^+(U) = H^0_cech(U, F) (SH-09).
///
/// Sections over U are matching families over the canonical cover of minimal neighborhoods {U_x}_{x in U}.
pub fn plus_construction<T: Clone + PartialEq + Debug + Send + Sync + 'static>(
    presheaf: &Presheaf<T>,
) -> Presheaf<Vec<T>> {
    let mut plus_sections = BTreeMap::new();
    let opens: Vec<OpenSet> = presheaf.sections_map.keys().cloned().collect();

    for u in &opens {
        let pts: Vec<String> = u.elements.iter().cloned().collect();
        let pt_opens: Vec<OpenSet> = pts
            .iter()
            .map(|p| presheaf.topology.minimal_open_neighborhood(p))
            .collect();
        let eq = compute_equalizer_kernel(presheaf, &pt_opens);
        plus_sections.insert(u.clone(), eq);
    }

    Presheaf::new(
        format!("{}^+", presheaf.name),
        presheaf.topology.clone(),
        plus_sections,
        |u, v, s| {
            let pts_u: Vec<String> = u.elements.iter().cloned().collect();
            let pts_v: Vec<String> = v.elements.iter().cloned().collect();
            let idx_map: Vec<usize> = pts_v
                .iter()
                .filter_map(|p| pts_u.iter().position(|pu| pu == p))
                .collect();
            idx_map
                .iter()
                .map(|&i| s.get(i).cloned().unwrap())
                .collect()
        },
    )
}

/// Grothendieck Sheafification Functor F^# = (F^+)^+ (SH-10).
///
/// Transforms any presheaf into an authentic sheaf while canonically preserving stalks.
pub fn sheafify<T: Clone + PartialEq + Debug + Send + Sync + 'static>(
    presheaf: &Presheaf<T>,
) -> Presheaf<Vec<Vec<T>>> {
    let f_plus = plus_construction(presheaf);
    let mut f_sharp = plus_construction(&f_plus);
    f_sharp.name = format!("{}^#", presheaf.name);
    f_sharp
}

/// Constant presheaf assigns the same single value to EVERY non-empty open set (SH-11).
/// Fails S2 gluing on disconnected open sets U = U_1 uplus U_2.
pub fn make_constant_presheaf(topology: &PosetTopology, val: &str) -> Presheaf<String> {
    let mut sections = BTreeMap::new();
    // Add minimal open neighborhoods
    for p in &topology.base_elements {
        let u_p = topology.minimal_open_neighborhood(p);
        sections.insert(u_p, vec![val.to_string()]);
    }
    // Add total space
    let total = OpenSet {
        elements: topology.base_elements.clone(),
    };
    sections.insert(total, vec![val.to_string()]);

    Presheaf::new(
        "ConstantPresheaf",
        topology.clone(),
        sections,
        |_u, _v, s| s.clone(),
    )
}

/// Skyscraper sheaf i_{x*} A supported at point x (SH-12):
/// F(U) = {stalk_value} if point in U else {zero_value}.
pub fn make_skyscraper_sheaf(
    topology: &PosetTopology,
    point: &str,
    stalk_value: &str,
    zero_value: &str,
) -> Presheaf<String> {
    let mut sections = BTreeMap::new();
    let mut all_opens = Vec::new();
    for p in &topology.base_elements {
        all_opens.push(topology.minimal_open_neighborhood(p));
    }
    all_opens.push(OpenSet {
        elements: topology.base_elements.clone(),
    });

    for u in all_opens {
        if u.contains(point) {
            sections.insert(u, vec![stalk_value.to_string()]);
        } else {
            sections.insert(u, vec![zero_value.to_string()]);
        }
    }

    let pt = point.to_string();
    let zero = zero_value.to_string();
    Presheaf::new(
        format!("Skyscraper_{point}"),
        topology.clone(),
        sections,
        move |_u, v, s| {
            if v.contains(&pt) {
                s.clone()
            } else {
                zero.clone()
            }
        },
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_skyscraper_sheaf_stalk() {
        let top = PosetTopology::discrete(vec!["p1", "p2"]);
        let sky = make_skyscraper_sheaf(&top, "p1", "42", "0");

        let u1 = top.minimal_open_neighborhood("p1");
        let u2 = top.minimal_open_neighborhood("p2");

        assert_eq!(sky.sections(&u1), &["42".to_string()]);
        assert_eq!(sky.sections(&u2), &["0".to_string()]);
    }
}
