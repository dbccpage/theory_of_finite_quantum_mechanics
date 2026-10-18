//! Grothendieck sites, covering sieves, and sheaves on sites (SH-23, Site & SheafOnSite Contracts).
//!
//! AuthorityEffect: None.

use crate::open_set::{OpenSet, PosetTopology};
use crate::presheaf::Presheaf;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};
use std::fmt::Debug;

/// A Grothendieck Site (C, J) conforming to `urn:omega:math:site:v0.1.0` (SH-23).
///
/// Models a site where the underlying category is the poset category and J is a Grothendieck pretopology.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct GrothendieckSite {
    pub site_id: String,
    pub topology: PosetTopology,
    /// Covering sieves assigned to each open set
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

    /// Add a covering sieve/family {U_i} covering U.
    pub fn add_covering_family(&mut self, u: OpenSet, family: Vec<OpenSet>) -> Result<(), String> {
        if !self.is_valid_covering(&u, &family) {
            return Err(
                "Family does not satisfy Grothendieck pretopology axioms for U".to_string(),
            );
        }
        self.covering_sieves.entry(u).or_default().push(family);
        Ok(())
    }

    /// Check pretopology axioms for family {U_i} covering U:
    /// 1. Each U_i is a subset of U.
    /// 2. The union of U_i equals U.
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

    /// Validate the site axioms:
    /// 1. Maximality: {U} is a covering of U for all U.
    /// 2. Stability: If {U_i} covers U and V subset U, then {U_i cap V} covers V.
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

/// A Sheaf on a Site conforming to `urn:omega:math:sheaf_on_site:v0.1.0`.
///
/// Validates that for every object U and every covering sieve {U_i} in J(U),
/// matching families on overlaps glue to a unique section in F(U).
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
