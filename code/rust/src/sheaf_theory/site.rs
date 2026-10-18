
use crate::open_set::{OpenSet, PosetTopology};
use crate::presheaf::Presheaf;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};
use std::fmt::Debug;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct GrothendieckSite {
    pub site_id: String,
    pub topology: PosetTopology,
    pub covering_sieves: BTreeMap<OpenSet, Vec<Vec<OpenSet>>>,
}

impl GrothendieckSite {
    pub fn new(site_id: impl Into<String>, topology: PosetTopology) -> Self {
        Self {
            site_id: site_id.into(),
            topology,
            covering_sieves: BTreeMap::new(),
        }
    }

    pub fn add_covering_family(&mut self, u: OpenSet, family: Vec<OpenSet>) -> Result<(), String> {
        if !self.is_valid_covering(&u, &family) {
            return Err(
                "Family does not satisfy Grothendieck pretopology axioms for U".to_string(),
            );
        }
        self.covering_sieves.entry(u).or_default().push(family);
        Ok(())
    }

    pub fn is_valid_covering(&self, u: &OpenSet, family: &[OpenSet]) -> bool {
        let mut union_elems = BTreeSet::new();
        for f in family {
            if !f.is_subset(u) {
                return false;
            }
            union_elems.extend(f.elements.clone());
        }
        union_elems == u.elements
    }

    pub fn validate_site_axioms(&self) -> bool {
        for (u, families) in &self.covering_sieves {
            for fam in families {
                if !self.is_valid_covering(u, fam) {
                    return false;
                }
            }
        }
        true
    }
}

pub fn validate_sheaf_on_site<T: Clone + PartialEq + Debug>(
    site: &GrothendieckSite,
    presheaf: &Presheaf<T>,
) -> bool {
    for (u, families) in &site.covering_sieves {
        for fam in families {
            let res = crate::sheaf::check_sheaf_condition(presheaf, u, fam);
            if !res.is_sheaf {
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
    fn test_grothendieck_site_pretopology() {
        let top = PosetTopology::discrete(vec!["0", "1", "2"]);
        let mut site = GrothendieckSite::new("site_test", top);

        let u_tot = OpenSet::new(vec!["0", "1", "2"]);
        let u01 = OpenSet::new(vec!["0", "1"]);
        let u12 = OpenSet::new(vec!["1", "2"]);

        assert!(site
            .add_covering_family(u_tot.clone(), vec![u01, u12])
            .is_ok());
        assert!(site.validate_site_axioms());
    }
}
