//! Bridges — Spec Section 8.
//!
//! The StructurePreservingMap base trait enables cross-discipline
//! functor-like maps without requiring full categorical infrastructure.

// ---------------------------------------------------------------------------
// Trait: StructurePreservingMap
// ---------------------------------------------------------------------------

/// Base trait for all structure-preserving maps across disciplines.
///
/// Specialized by: CatFunctor, GroupHomomorphism, ContinuousMap,
/// LinearMap, MeasurableMap, etc.
///
/// CatFunctor implements StructurePreservingMap automatically.
/// Other disciplines can implement the base without being forced
/// into full category infrastructure.
pub trait StructurePreservingMap {
    type Domain;
    type Codomain;

    fn map(&self, x: &Self::Domain) -> Self::Codomain;
}

/// Evidence emitted when a bridge performs a structural transformation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BridgeEvidence {
    pub source_discipline: String,
    pub target_discipline: String,
    pub map_name: String,
    pub laws_preserved: Vec<String>,
}

impl BridgeEvidence {
    pub fn new(source: &str, target: &str, name: &str) -> Self {
        Self {
            source_discipline: source.into(),
            target_discipline: target.into(),
            map_name: name.into(),
            laws_preserved: Vec::new(),
        }
    }

    pub fn preserve_law(&mut self, law: &str) {
        self.laws_preserved.push(law.into());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    struct DoubleMap;

    impl StructurePreservingMap for DoubleMap {
        type Domain = i32;
        type Codomain = i32;

        fn map(&self, x: &i32) -> i32 {
            x * 2
        }
    }

    #[test]
    fn structure_preserving_map_basic() {
        let m = DoubleMap;
        assert_eq!(m.map(&5), 10);
        assert_eq!(m.map(&0), 0);
    }

    #[test]
    fn bridge_evidence_construction() {
        let mut ev = BridgeEvidence::new("topology", "analysis", "MetricTopologyFunctor");
        ev.preserve_law("composition");
        ev.preserve_law("identity");
        assert_eq!(ev.laws_preserved.len(), 2);
        assert_eq!(ev.source_discipline, "topology");
    }
}
