
use crate::open_set::{OpenSet, PosetTopology};
use std::collections::BTreeMap;
use std::fmt::Debug;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PresheafError {
    MissingOpenSet(OpenSet),
    NotSubset { subset: OpenSet, superset: OpenSet },
    IdentityRestrictionFailed(OpenSet),
    CompositionLawFailed { u: OpenSet, v: OpenSet, w: OpenSet },
    NaturalityFailed { u: OpenSet, v: OpenSet },
}

#[derive(Clone)]
pub struct Presheaf<T> {
    pub name: String,
    pub topology: PosetTopology,
    pub sections_map: BTreeMap<OpenSet, Vec<T>>,
    pub restriction_fn: std::sync::Arc<dyn Fn(&OpenSet, &OpenSet, &T) -> T + Send + Sync>,
}

impl<T: Debug> Debug for Presheaf<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Presheaf")
            .field("name", &self.name)
            .field("topology", &self.topology)
            .field("sections_map", &self.sections_map)
            .finish()
    }
}

impl<T: Clone + PartialEq + Debug> Presheaf<T> {
    pub fn new(
        name: impl Into<String>,
        topology: PosetTopology,
        sections_map: BTreeMap<OpenSet, Vec<T>>,
        restriction_fn: impl Fn(&OpenSet, &OpenSet, &T) -> T + Send + Sync + 'static,
    ) -> Self {
        Self {
            name: name.into(),
            topology,
            sections_map,
            restriction_fn: std::sync::Arc::new(restriction_fn),
        }
    }

    pub fn sections(&self, u: &OpenSet) -> &[T] {
        self.sections_map.get(u).map(Vec::as_slice).unwrap_or(&[])
    }

    pub fn restrict(&self, u: &OpenSet, v: &OpenSet, s: &T) -> Result<T, PresheafError> {
        if !v.is_subset(u) {
            return Err(PresheafError::NotSubset {
                subset: v.clone(),
                superset: u.clone(),
            });
        }
        Ok((self.restriction_fn)(u, v, s))
    }

    fn validate_identity_restrictions(&self, opens: &[OpenSet]) -> Result<(), PresheafError> {
        for u in opens {
            for s in self.sections(u) {
                let res = self.restrict(u, u, s)?;
                if &res != s {
                    return Err(PresheafError::IdentityRestrictionFailed(u.clone()));
                }
            }
        }
        Ok(())
    }

    fn validate_triple_composition(
        &self,
        u: &OpenSet,
        v: &OpenSet,
        w: &OpenSet,
    ) -> Result<(), PresheafError> {
        for s in self.sections(u) {
            let res_uv = self.restrict(u, v, s)?;
            let res_vw = self.restrict(v, w, &res_uv)?;
            let res_uw = self.restrict(u, w, s)?;
            if res_vw != res_uw {
                return Err(PresheafError::CompositionLawFailed {
                    u: u.clone(),
                    v: v.clone(),
                    w: w.clone(),
                });
            }
        }
        Ok(())
    }

    fn validate_pair_compositions(
        &self,
        opens: &[OpenSet],
        u: &OpenSet,
        v: &OpenSet,
    ) -> Result<(), PresheafError> {
        for w in opens {
            if w.is_subset(v) {
                self.validate_triple_composition(u, v, w)?;
            }
        }
        Ok(())
    }

    pub fn validate_functoriality(&self) -> Result<(), PresheafError> {
        let opens: Vec<OpenSet> = self.sections_map.keys().cloned().collect();
        self.validate_identity_restrictions(&opens)?;
        for u in &opens {
            for v in &opens {
                if v.is_subset(u) {
                    self.validate_pair_compositions(&opens, u, v)?;
                }
            }
        }
        Ok(())
    }
}

#[derive(Clone)]
pub struct PresheafMorphism<T, V> {
    pub source: Presheaf<T>,
    pub target: Presheaf<V>,
    pub component_fn: std::sync::Arc<dyn Fn(&OpenSet, &T) -> V + Send + Sync>,
}

impl<T: Clone + PartialEq + Debug, V: Clone + PartialEq + Debug> PresheafMorphism<T, V> {
    pub fn new(
        source: Presheaf<T>,
        target: Presheaf<V>,
        component_fn: impl Fn(&OpenSet, &T) -> V + Send + Sync + 'static,
    ) -> Self {
        Self {
            source,
            target,
            component_fn: std::sync::Arc::new(component_fn),
        }
    }

    pub fn apply(&self, u: &OpenSet, s: &T) -> V {
        (self.component_fn)(u, s)
    }

    pub fn check_naturality(&self) -> Result<bool, PresheafError> {
        let opens: Vec<OpenSet> = self.source.sections_map.keys().cloned().collect();
        for u in &opens {
            for v in &opens {
                if v.is_subset(u) && !self.naturality_holds_on_pair(u, v)? {
                    return Ok(false);
                }
            }
        }
        Ok(true)
    }

    fn naturality_holds_on_pair(&self, u: &OpenSet, v: &OpenSet) -> Result<bool, PresheafError> {
        for s in self.source.sections(u) {
            let left = self.target.restrict(u, v, &self.apply(u, s))?;
            let right = self.apply(v, &self.source.restrict(u, v, s)?);
            if left != right {
                return Ok(false);
            }
        }
        Ok(true)
    }
}

pub fn presheaf_kernel<T: Clone + PartialEq + Debug, V: Clone + PartialEq + Debug>(
    morph: &PresheafMorphism<T, V>,
    zero_val: &V,
) -> Presheaf<T> {
    let mut ker_sections = BTreeMap::new();
    for (u, secs) in &morph.source.sections_map {
        let filtered: Vec<T> = secs
            .iter()
            .filter(|s| &morph.apply(u, s) == zero_val)
            .cloned()
            .collect();
        ker_sections.insert(u.clone(), filtered);
    }

    let src_restr = morph.source.restriction_fn.clone();
    Presheaf {
        name: format!("ker({})", morph.source.name),
        topology: morph.source.topology.clone(),
        sections_map: ker_sections,
        restriction_fn: src_restr,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_presheaf_functoriality_validation() {
        let top = PosetTopology::discrete(vec!["0", "1"]);
        let u0 = OpenSet::new(vec!["0"]);
        let u1 = OpenSet::new(vec!["1"]);
        let u01 = OpenSet::new(vec!["0", "1"]);

        let mut secs = BTreeMap::new();
        secs.insert(u0.clone(), vec![10]);
        secs.insert(u1.clone(), vec![20]);
        secs.insert(u01.clone(), vec![30]);

        let p = Presheaf::new("test_p", top, secs, |_u, _v, s| *s);
        assert!(p.validate_functoriality().is_ok());
    }

    #[test]
    fn test_presheaf_functoriality_and_naturality_refusals() {
        let top = PosetTopology::discrete(vec!["0", "1"]);
        let u0 = OpenSet::new(vec!["0"]);
        let u01 = OpenSet::new(vec!["0", "1"]);

        let mut bad_id_secs = BTreeMap::new();
        bad_id_secs.insert(u0.clone(), vec![10]);
        let bad_id = Presheaf::new("bad_id", top.clone(), bad_id_secs, |_u, _v, s| s + 1);
        assert!(matches!(
            bad_id.validate_functoriality(),
            Err(PresheafError::IdentityRestrictionFailed(_))
        ));

        let mut secs = BTreeMap::new();
        secs.insert(u0.clone(), vec![10, 11]);
        secs.insert(u01.clone(), vec![10]);
        let source = Presheaf::new("src", top.clone(), secs.clone(), |_u, _v, s| *s);
        let target = Presheaf::new("tgt", top, secs, |_u, _v, s| *s);
        let non_natural = PresheafMorphism::new(source, target, |u, s| {
            if u.elements.len() == 2 {
                *s
            } else {
                s + 1
            }
        });
        assert_eq!(non_natural.check_naturality().unwrap(), false);
    }
}
