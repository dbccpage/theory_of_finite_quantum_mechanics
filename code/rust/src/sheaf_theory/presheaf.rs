//! Presheaf functor F: Open(X)^op -> C and natural transformations (SH-02, SH-04, SH-05, Presheaf Contract).
//!
//! AuthorityEffect: None.

use crate::open_set::{OpenSet, PosetTopology};
use std::collections::BTreeMap;
use std::fmt::Debug;

/// Presheaf validation errors conforming to `presheaf.contract.yaml`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PresheafError {
    MissingOpenSet(OpenSet),
    NotSubset { subset: OpenSet, superset: OpenSet },
    IdentityRestrictionFailed(OpenSet),
    CompositionLawFailed { u: OpenSet, v: OpenSet, w: OpenSet },
    NaturalityFailed { u: OpenSet, v: OpenSet },
}

/// A finite presheaf F: Open(X)^op -> Set (or Vect).
///
/// Stores for each OpenSet U a finite list of sections F(U), and for each inclusion
/// V subset U a restriction function rho_{V, U}: F(U) -> F(V).
#[derive(Clone)]
pub struct Presheaf<T> {
    pub name: String,
    pub topology: PosetTopology,
    pub sections_map: BTreeMap<OpenSet, Vec<T>>,
    /// Custom restriction function: (U, V, section_u) -> section_v
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

    /// Apply restriction rho_{V,U}(s). Verifies V is subset of U.
    pub fn restrict(&self, u: &OpenSet, v: &OpenSet, s: &T) -> Result<T, PresheafError> {
        if !v.is_subset(u) {
            return Err(PresheafError::NotSubset {
                subset: v.clone(),
                superset: u.clone(),
            });
        }
        Ok((self.restriction_fn)(u, v, s))
    }

    /// Validate presheaf functoriality laws according to `presheaf.contract.yaml`:
    /// 1. For each open U, rho_{U,U} = id_{F(U)}
    /// 2. For each chain W subset V subset U, rho_{W,U} = rho_{W,V} o rho_{V,U}
    pub fn validate_functoriality(&self) -> Result<(), PresheafError> {
        let opens: Vec<OpenSet> = self.sections_map.keys().cloned().collect();

        // 1. Identity law
        for u in &opens {
            for s in self.sections(u) {
                let res = self.restrict(u, u, s)?;
                if &res != s {
                    return Err(PresheafError::IdentityRestrictionFailed(u.clone()));
                }
            }
        }

        // 2. Composition law
        for u in &opens {
            for v in &opens {
                if !v.is_subset(u) {
                    continue;
                }
                for w in &opens {
                    if !w.is_subset(v) {
                        continue;
                    }
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
                }
            }
        }

        Ok(())
    }
}

/// A natural transformation alpha: F -> G between presheaves (SH-04).
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

    /// Verify naturality condition: rho^G_{V,U}(alpha_U(s)) == alpha_V(rho^F_{V,U}(s)).
    pub fn check_naturality(&self) -> Result<bool, PresheafError> {
        let opens: Vec<OpenSet> = self.source.sections_map.keys().cloned().collect();
        for u in &opens {
            for v in &opens {
                if !v.is_subset(u) {
                    continue;
                }
                for s in self.source.sections(u) {
                    let left = self.target.restrict(u, v, &self.apply(u, s))?;
                    let right = self.apply(v, &self.source.restrict(u, v, s)?);
                    if left != right {
                        return Ok(false);
                    }
                }
            }
        }
        Ok(true)
    }
}

/// Construct presheaf kernel: ker(alpha)(U) = {s in F(U) | alpha_U(s) == zero_val} (SH-05).
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
}
