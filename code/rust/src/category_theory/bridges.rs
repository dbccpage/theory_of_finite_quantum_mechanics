//! Raw cross-discipline mapping interfaces and declarations. AuthorityEffect: None.
//! The trait requires only a map operation. BridgeEvidence stores caller-supplied
//! law labels; it performs no law checking and confers no mathematical evidence.

// ---------------------------------------------------------------------------
// Trait: StructurePreservingMap
// ---------------------------------------------------------------------------

/// A map signature; preservation obligations belong to each implementation.
pub trait StructurePreservingMap {
    type Domain;
    type Codomain;

    fn map(&self, x: &Self::Domain) -> Self::Codomain;
}

/// Unchecked declarations associated with a proposed bridge.
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
