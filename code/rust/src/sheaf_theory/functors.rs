//! Direct image (pushforward f_*) and inverse image (pullback f^*) functors (SH-13, SH-14).
//!
//! AuthorityEffect: None.

use crate::open_set::{OpenSet, PosetTopology};
use crate::presheaf::Presheaf;
use std::collections::{BTreeMap, BTreeSet};
use std::fmt::Debug;

/// Pushforward sheaf (f_* F)(V) = F(f^{-1}(V)) (SH-13).
pub fn pushforward_sheaf<T: Clone + PartialEq + Debug + Send + Sync + 'static>(
    f: impl Fn(&str) -> String + Send + Sync + 'static,
    presheaf: &Presheaf<T>,
    target_topology: PosetTopology,
) -> Presheaf<T> {
    let mut sections = BTreeMap::new();
    let opens: Vec<OpenSet> = target_topology
        .base_elements
        .iter()
        .map(|p| target_topology.minimal_open_neighborhood(p))
        .collect();

    for v_set in &opens {
        let preimage_elems: BTreeSet<String> = presheaf
            .topology
            .base_elements
            .iter()
            .filter(|x| v_set.contains(&f(x)))
            .cloned()
            .collect();
        let u_preimage = OpenSet {
            elements: preimage_elems,
        };
        sections.insert(v_set.clone(), presheaf.sections(&u_preimage).to_vec());
    }

    let orig_restr = presheaf.restriction_fn.clone();
    Presheaf::new(
        format!("f_*({})", presheaf.name),
        target_topology,
        sections,
        move |u, v, s| (orig_restr)(u, v, s),
    )
}

/// Pullback presheaf (f^* G)(U) (SH-14): assigns colimit of G(V) for V superset f(U).
pub fn pullback_presheaf<T: Clone + PartialEq + Debug + Send + Sync + 'static>(
    f: impl Fn(&str) -> String + Send + Sync + 'static,
    source_topology: PosetTopology,
    target_sheaf: &Presheaf<T>,
) -> Presheaf<T> {
    let mut sections = BTreeMap::new();
    let opens: Vec<OpenSet> = source_topology
        .base_elements
        .iter()
        .map(|p| source_topology.minimal_open_neighborhood(p))
        .collect();

    for u_set in &opens {
        let mut target_elems = BTreeSet::new();
        for p in &u_set.elements {
            target_elems.insert(f(p));
        }
        let v_set = OpenSet {
            elements: target_elems,
        };
        sections.insert(u_set.clone(), target_sheaf.sections(&v_set).to_vec());
    }

    let tgt_restr = target_sheaf.restriction_fn.clone();
    Presheaf::new(
        format!("f^*({})", target_sheaf.name),
        source_topology,
        sections,
        move |u, v, s| (tgt_restr)(u, v, s),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pushforward_sheaf() {
        let top_x = PosetTopology::discrete(vec!["x1", "x2"]);
        let top_y = PosetTopology::discrete(vec!["y1"]);

        let u_x = OpenSet::new(vec!["x1", "x2"]);
        let mut secs = BTreeMap::new();
        secs.insert(u_x.clone(), vec![99]);

        let p = Presheaf::new("F", top_x, secs, |_u, _v, s| *s);
        let pf = pushforward_sheaf(|_x| "y1".to_string(), &p, top_y);

        let v_y = OpenSet::new(vec!["y1"]);
        assert_eq!(pf.sections(&v_y), &[99]);
    }
}
