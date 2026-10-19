//! Raw finite named witness multisets and nonnegative rational-weight collections.
//! Discrete-middle composition concatenates supplied witness Cartesian products;
//! it does not admit category actions or a general coend. Companion/conjoint
//! helpers observe supplied object maps/arrow boundaries only. Boundary reports
//! do not certify action/functor/category laws. AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::Zero;
use std::collections::BTreeMap;

// ═══════════════════════════════════════════════════════════════════════════
// Finite relational profunctor
// ═══════════════════════════════════════════════════════════════════════════

/// Raw named relation multisets with unchecked action metadata.
///
/// For each pair (A, B) where A ∈ Ob(C) and B ∈ Ob(D),
/// P(A, B) is a finite multiset (list) of elements (witnesses/relations).
/// Multiplicity matters for obstruction/mass calculations.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredFiniteRelationalProfunctor {
    pub name: String,
    pub source_category: String, // C
    pub target_category: String, // D
    /// (source_object, target_object) → list/multiset of relation witnesses.
    pub relations: BTreeMap<(String, String), Vec<String>>,

    /// Action of source morphisms contravariantly.
    /// f : A' -> A sends P(A, B) -> P(A', B)
    pub left_action: BTreeMap<(String, String, String), Vec<(usize, usize)>>,

    /// Action of target morphisms covariantly.
    /// g : B -> B' sends P(A, B) -> P(A, B')
    pub right_action: BTreeMap<(String, String, String), Vec<(usize, usize)>>,
}

impl DeclaredFiniteRelationalProfunctor {
    pub fn new(name: &str, source: &str, target: &str) -> Self {
        Self {
            name: name.into(),
            source_category: source.into(),
            target_category: target.into(),
            relations: BTreeMap::new(),
            left_action: BTreeMap::new(),
            right_action: BTreeMap::new(),
        }
    }

    /// Add a witness to P(A, B).
    pub fn add_witness(&mut self, source_ob: &str, target_ob: &str, witness: &str) {
        self.relations
            .entry((source_ob.into(), target_ob.into()))
            .or_default()
            .push(witness.into());
    }

    /// Get P(A, B) as a slice.
    pub fn hom_set(&self, source_ob: &str, target_ob: &str) -> &[String] {
        self.relations
            .get(&(source_ob.into(), target_ob.into()))
            .map(|v| v.as_slice())
            .unwrap_or(&[])
    }

    /// Check if P(A, B) is nonempty.
    pub fn is_related(&self, source_ob: &str, target_ob: &str) -> bool {
        !self.hom_set(source_ob, target_ob).is_empty()
    }

    /// Total number of witness elements across all (A, B) pairs.
    pub fn total_witnesses(&self) -> usize {
        self.relations.values().map(|v| v.len()).sum()
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// Weighted profunctor (P(A,B) → R≥0)
// ═══════════════════════════════════════════════════════════════════════════

/// Raw named witness multisets with admitted defined nonnegative rational weights.
///
/// Names are metadata;no category actions or profunctor laws are admitted.
#[derive(Debug, Clone, PartialEq)]
pub struct DeclaredFiniteWeightedProfunctor {
    pub name: String,
    pub source_category: String,
    pub target_category: String,
    /// (source_object, target_object) → list of (witness, weight).
    weighted_relations: BTreeMap<(String, String), Vec<(String, BigRational)>>,
}

impl DeclaredFiniteWeightedProfunctor {
    pub fn new(name: &str, source: &str, target: &str) -> Self {
        Self {
            name: name.into(),
            source_category: source.into(),
            target_category: target.into(),
            weighted_relations: BTreeMap::new(),
        }
    }

    pub fn add_weighted_witness(
        &mut self,
        source_ob: &str,
        target_ob: &str,
        witness: &str,
        weight: BigRational,
    ) -> Result<(), String> {
        if weight.denom() <= &0.into() || weight < BigRational::zero() {
            return Err(format!(
                "Weight must be finite and non-negative, got {}",
                weight
            ));
        }

        self.weighted_relations
            .entry((source_ob.into(), target_ob.into()))
            .or_default()
            .push((witness.into(), weight));

        Ok(())
    }

    /// Total weight of P(A, B).
    pub fn weighted_relations(&self) -> &BTreeMap<(String, String), Vec<(String, BigRational)>> {
        &self.weighted_relations
    }

    pub fn total_weight(&self, source_ob: &str, target_ob: &str) -> BigRational {
        self.weighted_relations
            .get(&(source_ob.into(), target_ob.into()))
            .map(|v| v.iter().map(|(_, w)| w).sum())
            .unwrap_or_else(BigRational::zero)
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// Profunctor composition via coend
// ═══════════════════════════════════════════════════════════════════════════

struct RelationView<'a> {
    rows: BTreeMap<(&'a str, &'a str), &'a [String]>,
}

impl<'a> RelationView<'a> {
    fn new(relations: &'a BTreeMap<(String, String), Vec<String>>) -> Self {
        Self { rows: relations.iter().map(|((a, b), values)| ((a.as_str(), b.as_str()), values.as_slice())).collect() }
    }

    fn hom(&self, source: &str, target: &str) -> &'a [String] {
        self.rows.get(&(source, target)).copied().unwrap_or(&[])
    }
}

fn composed_witnesses(p: &RelationView<'_>, q: &RelationView<'_>, a: &str, c: &str, middle: &[&str]) -> Vec<String> {
    let mut witnesses = Vec::new();
    for &b in middle {
        let left = p.hom(a, b);
        let right = q.hom(b, c);
        for pw in left {
            for qw in right {
                witnesses.push(format!("({},{})@{}", pw, qw, b));
            }
        }
    }
    witnesses
}

/// Compose two finite relational profunctors assuming a discrete middle category.
///
/// Given P : C^op × D → Set and Q : D^op × E → Set,
/// when the intermediate category D is discrete, the coend composition
/// (Q ∘ P)(A, C) = ∫^B P(A, B) × Q(B, C) reduces to the coproduct
/// ∐_B P(A, B) × Q(B, C) over the intermediate objects B.
///
/// Output positions enumerate these products in supplied middle-list order,
/// preserving repetitions. Textual witness descriptors need not be injective;
/// equal text remains separate list occurrences. Actions are ignored and result
/// action maps are empty. No general coend quotient or action law is admitted.
pub fn compose_relational_profunctors_discrete_middle(
    name: &str,
    p: &DeclaredFiniteRelationalProfunctor,
    q: &DeclaredFiniteRelationalProfunctor,
    intermediate_objects: &[&str],
) -> Result<DeclaredFiniteRelationalProfunctor, String> {
    if p.target_category != q.source_category {
        return Err(format!(
            "Cannot compose profunctors: P targets {} but Q sources {}",
            p.target_category, q.source_category
        ));
    }

    let mut result =
        DeclaredFiniteRelationalProfunctor::new(name, &p.source_category, &q.target_category);

    let p_view = RelationView::new(&p.relations);
    let q_view = RelationView::new(&q.relations);
    let sources: std::collections::BTreeSet<&str> = p.relations.keys().map(|(a, _)| a.as_str()).collect();
    let targets: std::collections::BTreeSet<&str> = q.relations.keys().map(|(_, c)| c.as_str()).collect();
    for a in sources {
        for &c in &targets {
            let witnesses = composed_witnesses(&p_view, &q_view, a, c, intermediate_objects);
            if !witnesses.is_empty() {
                result.relations.insert((a.to_owned(), c.to_owned()), witnesses);
            }
        }
    }

    Ok(result)
}

// ═══════════════════════════════════════════════════════════════════════════
// Companion and conjoint from a functor
// ═══════════════════════════════════════════════════════════════════════════

use super::cat_functor::DeclaredFiniteFunctor;
use super::finite_category::DeclaredFiniteCategory;
use super::validation::{
    ValidationLocation, ValidationReport, ValidationSeverity, ValidationUnit, ValidationViolation,
};

type BorrowedRelations<'a> = BTreeMap<(&'a str, &'a str), Vec<String>>;

fn own_relations(rows: BorrowedRelations<'_>) -> BTreeMap<(String, String), Vec<String>> {
    rows.into_iter().map(|((a, b), values)| ((a.to_owned(), b.to_owned()), values)).collect()
}

/// Build raw Hom-boundary witness multisets from a supplied object map.
///
/// F_* : C^op × D → Set defined by F_*(A, B) = Hom_D(F(A), B).
/// Note: Adjunctions L ⊣ R can be expressed as isomorphisms between
/// the companion L_* and the conjoint R^*.
pub fn declared_companion_profunctor(
    name: &str,
    functor: &DeclaredFiniteFunctor,
    target_category: &DeclaredFiniteCategory,
) -> DeclaredFiniteRelationalProfunctor {
    let mut prof = DeclaredFiniteRelationalProfunctor::new(
        name,
        &functor.source_category,
        &functor.target_category,
    );

    let mut rows = BorrowedRelations::new();
    for (a, fa) in &functor.object_map {
        for morphism in target_category.morphisms.values() {
            if morphism.source == *fa {
                rows.entry((a.as_str(), morphism.target.as_str())).or_default().push(morphism.name.clone());
            }
        }
    }

    prof.relations = own_relations(rows);
    prof
}

/// Build raw reversed Hom-boundary multisets from a supplied object map.
///
/// F^* : D^op × C → Set defined by F^*(B, A) = Hom_D(B, F(A)).
pub fn declared_conjoint_profunctor(
    name: &str,
    functor: &DeclaredFiniteFunctor,
    target_category: &DeclaredFiniteCategory,
) -> DeclaredFiniteRelationalProfunctor {
    let mut prof = DeclaredFiniteRelationalProfunctor::new(
        name,
        &functor.target_category,
        &functor.source_category,
    );

    let mut rows = BorrowedRelations::new();
    for (a, fa) in &functor.object_map {
        for morphism in target_category.morphisms.values() {
            if morphism.target == *fa {
                rows.entry((morphism.source.as_str(), a.as_str())).or_default().push(morphism.name.clone());
            }
        }
    }

    prof.relations = own_relations(rows);
    prof
}

// ═══════════════════════════════════════════════════════════════════════════
// Validation
// ═══════════════════════════════════════════════════════════════════════════

/// Check declared category-name/object-key membership only;action laws untouched.
pub fn validate_relational_profunctor(
    prof: &DeclaredFiniteRelationalProfunctor,
    source: &DeclaredFiniteCategory,
    target: &DeclaredFiniteCategory,
) -> ValidationReport {
    let mut report = ValidationReport::new(&prof.name);
    let mut violations = Vec::new();

    let unit = ValidationUnit::Other("ProfunctorBoundary".into());

    if prof.source_category != source.name {
        violations.push(ValidationViolation::new(
            unit.clone(),
            ValidationLocation::Global,
            format!(
                "Source category mismatch: expected {}, got {}",
                source.name, prof.source_category
            ),
            ValidationSeverity::Error,
        ));
    }

    if prof.target_category != target.name {
        violations.push(ValidationViolation::new(
            unit.clone(),
            ValidationLocation::Global,
            format!(
                "Target category mismatch: expected {}, got {}",
                target.name, prof.target_category
            ),
            ValidationSeverity::Error,
        ));
    }

    for (a, b) in prof.relations.keys() {
        if !source.objects.contains(a) {
            violations.push(ValidationViolation::new(
                unit.clone(),
                ValidationLocation::Object(a.clone()),
                format!("Source object {} not in source category {}", a, source.name),
                ValidationSeverity::Error,
            ));
        }
        if !target.objects.contains(b) {
            violations.push(ValidationViolation::new(
                unit.clone(),
                ValidationLocation::Object(b.clone()),
                format!("Target object {} not in target category {}", b, target.name),
                ValidationSeverity::Error,
            ));
        }
    }

    report.add_typed("boundary_checks", violations);
    report
}

// ═══════════════════════════════════════════════════════════════════════════
// Tests
// ═══════════════════════════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn relational_profunctor_tracks_witnesses() {
        let mut p = DeclaredFiniteRelationalProfunctor::new("P", "C", "D");
        p.add_witness("A", "X", "w1");
        p.add_witness("A", "X", "w2");
        p.add_witness("A", "Y", "w3");

        assert_eq!(p.hom_set("A", "X").len(), 2);
        assert_eq!(p.hom_set("A", "Y").len(), 1);
        assert!(p.is_related("A", "X"));
        assert!(!p.is_related("B", "X"));
        assert_eq!(p.total_witnesses(), 3);
    }

    #[test]
    fn weighted_profunctor_sums_weights() {
        let mut p = DeclaredFiniteWeightedProfunctor::new("W", "C", "D");
        p.add_weighted_witness("A", "X", "w1", BigRational::new(3.into(), 2.into()))
            .unwrap();
        p.add_weighted_witness("A", "X", "w2", BigRational::new(5.into(), 2.into()))
            .unwrap();

        let total = p.total_weight("A", "X");
        assert_eq!(total, BigRational::from_integer(4.into()));
        assert_eq!(p.total_weight("A", "Y"), BigRational::zero());

        assert!(p
            .add_weighted_witness("A", "X", "w3", BigRational::from_integer((-1).into()))
            .is_err());
    }

    #[test]
    fn profunctor_composition_collects_pairs() {
        let mut p = DeclaredFiniteRelationalProfunctor::new("P", "C", "D");
        p.add_witness("A", "B1", "p1");
        p.add_witness("A", "B2", "p2");

        let mut q = DeclaredFiniteRelationalProfunctor::new("Q", "D", "E");
        q.add_witness("B1", "X", "q1");
        q.add_witness("B2", "X", "q2");

        let composed =
            compose_relational_profunctors_discrete_middle("QP", &p, &q, &["B1", "B2"]).unwrap();

        // (Q∘P)(A, X) = P(A, B1)×Q(B1, X) ∪ P(A, B2)×Q(B2, X) = {(p1,q1), (p2,q2)}
        assert_eq!(composed.hom_set("A", "X").len(), 2);
    }
}
