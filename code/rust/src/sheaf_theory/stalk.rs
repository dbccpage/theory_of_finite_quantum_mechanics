//! Stalk at a point/simplex and germs of sections (SH-03).
//!
//! AuthorityEffect: None.

use crate::open_set::OpenSet;
use crate::presheaf::Presheaf;
use serde::{Deserialize, Serialize};
use std::fmt::Debug;

/// A germ of a section at point x: equivalence class [(U, s)]_x.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Germ<T> {
    pub point: String,
    pub neighborhood: OpenSet,
    pub section: T,
}

/// In a finite Alexandrov poset, the stalk F_x is canonically isomorphic
/// to the sections over the minimal open neighborhood U_x = star(x).
pub fn compute_stalk<T: Clone + PartialEq + Debug>(
    presheaf: &Presheaf<T>,
    x: &str,
) -> Vec<Germ<T>> {
    let u_x = presheaf.topology.minimal_open_neighborhood(x);
    let secs = presheaf.sections(&u_x);
    secs.iter()
        .map(|s| Germ {
            point: x.to_string(),
            neighborhood: u_x.clone(),
            section: s.clone(),
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::open_set::PosetTopology;
    use std::collections::BTreeMap;

    #[test]
    fn test_compute_stalk() {
        let top = PosetTopology::new(vec!["0", "1", "01"], vec![("0", "01"), ("1", "01")]);
        let u_0 = top.minimal_open_neighborhood("0");
        let mut secs = BTreeMap::new();
        secs.insert(u_0.clone(), vec![42]);

        let p = Presheaf::new("test", top, secs, |_u, _v, s| *s);
        let stalk = compute_stalk(&p, "0");
        assert_eq!(stalk.len(), 1);
        assert_eq!(stalk[0].section, 42);
        assert_eq!(stalk[0].point, "0");
    }
}
