//! Coends — Spec Section 14.
//!
//! A coend ∫^c F(c,c) is the universal quotient of diagonal contributions
//! by dinaturality. It is the categorical analog of integration.
//!
//! For a bifunctor F : C^op × C → Set, the coend is computed by:
//! 1. Collecting all F(c,c) contributions (one per object c).
//! 2. Quotienting by dinaturality: for each f: c → c',
//!    the left-action F(f, id)(x) is identified with the right-action F(id, f)(x).
//!
//! Coends appear in: profunctor composition, Kan extensions, tensor products.

use std::collections::BTreeMap;

// ---------------------------------------------------------------------------
// DinaturalityWitness — records one identification
// ---------------------------------------------------------------------------

/// A witness that two elements were identified via dinaturality.
///
/// For f: c → c', dinaturality identifies:
///   F(id_c, f)(x)  for x ∈ F(c, c)
/// with
///   F(f, id_c')(y) for y ∈ F(c', c')
/// when both land in F(c, c').
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DinaturalityWitness {
    /// The morphism f: source → target that induced this identification.
    pub morphism: String,
    pub source_object: String,
    pub target_object: String,
    /// Index of the element in the forward contribution.
    pub forward_index: usize,
    /// Index of the element in the backward contribution.
    pub backward_index: usize,
}

// ---------------------------------------------------------------------------
// DeclaredFiniteCoend
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct TaggedDiagonal<T> {
    pub object: String,
    pub index: usize,
    pub value: T,
}

/// A finite coend over a bifunctor F: C^op × C → Set, represented
/// by explicit elements and dinaturality identifications.
///
/// The elements are equivalence class representatives after
/// quotienting by all dinaturality relations.
#[derive(Debug, Clone)]
pub struct DeclaredFiniteCoend<T: Clone + PartialEq> {
    /// The contributing objects (diagonal entries of the bifunctor).
    pub objects: Vec<String>,
    /// Raw diagonal contributions: object → list of elements in F(c,c).
    pub contributions: BTreeMap<String, Vec<T>>,
    /// Quotient classes after identification.
    pub classes: Vec<Vec<TaggedDiagonal<T>>>,
    /// Maps a tagged diagonal element (object, index) to its equivalence class index.
    pub class_of: BTreeMap<(String, usize), usize>,
    /// Dinaturality identifications applied during computation.
    pub identifications: Vec<DinaturalityWitness>,
}

/// Input for computing a finite coend.
pub struct CoendInput<T: Clone + PartialEq> {
    /// Objects of the indexing category.
    pub objects: Vec<String>,
    /// Morphisms: (name, source, target).
    pub morphisms: Vec<(String, String, String)>,
    /// Diagonal contributions: object → elements of F(c,c).
    pub diagonal: BTreeMap<String, Vec<T>>,
    /// Forward action: F(id_c, f): F(c,c) -> F(c,c')
    /// Key: morphism name. Value: element index in F(c,c) → element index in F(c,c').
    pub forward_action: BTreeMap<String, Vec<(usize, usize)>>,
    /// Backward action: F(f, id_c'): F(c',c') -> F(c,c')
    /// Key: morphism name. Value: element index in F(c',c') → element index in F(c,c').
    pub backward_action: BTreeMap<String, Vec<(usize, usize)>>,
}

impl<T: Clone + PartialEq + Eq + std::hash::Hash> DeclaredFiniteCoend<T> {
    /// Compute the coend from an explicit input specification.
    ///
    /// This implements the coequalizer construction:
    ///   ∐_{f:c→c'} F(c',c) ⇉ ∐_c F(c,c) → ∫^c F(c,c)
    pub fn compute(input: &CoendInput<T>) -> Self {
        let objects = input.objects.clone();
        let contributions = input.diagonal.clone();

        // Assign global indices to all diagonal elements.
        let mut all_elements: Vec<TaggedDiagonal<T>> = Vec::new();
        for obj in &objects {
            if let Some(elems) = input.diagonal.get(obj) {
                for (i, elem) in elems.iter().enumerate() {
                    all_elements.push(TaggedDiagonal {
                        object: obj.clone(),
                        index: i,
                        value: elem.clone(),
                    });
                }
            }
        }

        // Build union-find for identifications.
        let n = all_elements.len();
        let mut parent: Vec<usize> = (0..n).collect();

        fn find(parent: &mut Vec<usize>, i: usize) -> usize {
            if parent[i] != i {
                parent[i] = find(parent, parent[i]);
            }
            parent[i]
        }

        fn union(parent: &mut Vec<usize>, a: usize, b: usize) {
            let ra = find(parent, a);
            let rb = find(parent, b);
            if ra != rb {
                parent[rb] = ra;
            }
        }

        // Helper: find global index for (object, local_index).
        let global_index = |obj: &str, local: usize| -> Option<usize> {
            all_elements
                .iter()
                .position(|td| td.object == obj && td.index == local)
        };

        let mut identifications = Vec::new();

        // Apply dinaturality identifications for each morphism.
        for (mor_name, src, tgt) in &input.morphisms {
            if let (Some(forward_pairs), Some(backward_pairs)) = (
                input.forward_action.get(mor_name),
                input.backward_action.get(mor_name),
            ) {
                // For each pair of (element in F(src,src), element in F(tgt,tgt))
                // that land in the same slot of F(src, tgt), unify them.
                for &(src_local, forward_target) in forward_pairs {
                    for &(tgt_local, backward_target) in backward_pairs {
                        if forward_target == backward_target {
                            if let (Some(gi_src), Some(gi_tgt)) =
                                (global_index(src, src_local), global_index(tgt, tgt_local))
                            {
                                union(&mut parent, gi_src, gi_tgt);
                                identifications.push(DinaturalityWitness {
                                    morphism: mor_name.clone(),
                                    source_object: src.clone(),
                                    target_object: tgt.clone(),
                                    forward_index: src_local,
                                    backward_index: tgt_local,
                                });
                            }
                        }
                    }
                }
            }
        }

        // Extract equivalence classes.
        let mut classes_map: BTreeMap<usize, Vec<TaggedDiagonal<T>>> = BTreeMap::new();
        let mut class_of: BTreeMap<(String, usize), usize> = BTreeMap::new();

        for (i, element) in all_elements.iter().enumerate() {
            let root = find(&mut parent, i);
            classes_map.entry(root).or_default().push(element.clone());
            class_of.insert((element.object.clone(), element.index), root);
        }

        let classes = classes_map.into_values().collect();

        DeclaredFiniteCoend {
            objects,
            contributions,
            classes,
            class_of,
            identifications,
        }
    }
}

// ---------------------------------------------------------------------------
// Validation: dinaturality check
// ---------------------------------------------------------------------------

pub fn validate_coend_input<T: Clone + PartialEq>(input: &CoendInput<T>) -> Vec<String> {
    let mut violations = Vec::new();

    // 1. Every object has a diagonal contribution
    for obj in &input.objects {
        if !input.diagonal.contains_key(obj) {
            violations.push(format!("Missing diagonal contribution for object {}", obj));
        }
    }

    // 2. Every morphism has both actions
    for (mor_name, _, _) in &input.morphisms {
        if !input.forward_action.contains_key(mor_name) {
            violations.push(format!("Missing forward action for morphism {}", mor_name));
        }
        if !input.backward_action.contains_key(mor_name) {
            violations.push(format!("Missing backward action for morphism {}", mor_name));
        }
    }

    violations
}

/// Verify that all dinaturality conditions are satisfied in the coend.
///
/// For each morphism f: c → c', verify that elements identified by
/// forward-action and backward-action are in the same equivalence class.
pub fn check_dinaturality<T: Clone + PartialEq>(
    coend: &DeclaredFiniteCoend<T>,
    input: &CoendInput<T>,
) -> Vec<String> {
    let mut violations = Vec::new();
    for (mor_name, src, tgt) in &input.morphisms {
        if let (Some(forward_pairs), Some(backward_pairs)) = (
            input.forward_action.get(mor_name),
            input.backward_action.get(mor_name),
        ) {
            for &(src_local, forward_target) in forward_pairs {
                for &(tgt_local, backward_target) in backward_pairs {
                    if forward_target == backward_target {
                        let lhs_class = coend.class_of.get(&(src.clone(), src_local));
                        let rhs_class = coend.class_of.get(&(tgt.clone(), tgt_local));

                        match (lhs_class, rhs_class) {
                            (Some(l), Some(r)) if l == r => {} // valid
                            (Some(l), Some(r)) => {
                                violations.push(format!(
                                    "Dinaturality violated: {} and {} via morphism {} mapped to different classes ({} vs {})",
                                    src_local, tgt_local, mor_name, l, r
                                ));
                            }
                            _ => {
                                violations.push(format!(
                                    "Dinaturality: missing class mapping for elements involved in morphism {}",
                                    mor_name
                                ));
                            }
                        }
                    }
                }
            }
        }
    }
    violations
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn trivial_coend_single_object() {
        // One object, no non-identity morphisms. Coend = F(c,c) itself.
        let input = CoendInput {
            objects: vec!["A".into()],
            morphisms: vec![],
            diagonal: {
                let mut m = BTreeMap::new();
                m.insert("A".into(), vec![1, 2, 3]);
                m
            },
            forward_action: BTreeMap::new(),
            backward_action: BTreeMap::new(),
        };

        let coend = DeclaredFiniteCoend::compute(&input);
        assert_eq!(coend.classes.len(), 3);
        assert!(coend.identifications.is_empty());
    }

    #[test]
    fn coend_with_identification() {
        // Two objects A, B with morphism f: A → B.
        // F(A,A) = {0}, F(B,B) = {1}.
        // Forward action of f sends 0 to slot 0 in F(A,B).
        // Backward action of f sends 1 to slot 0 in F(A,B).
        // So 0 ~ 1 in the coend.
        let input = CoendInput {
            objects: vec!["A".into(), "B".into()],
            morphisms: vec![("f".into(), "A".into(), "B".into())],
            diagonal: {
                let mut m = BTreeMap::new();
                m.insert("A".into(), vec![0]);
                m.insert("B".into(), vec![1]);
                m
            },
            forward_action: {
                let mut m = BTreeMap::new();
                m.insert("f".into(), vec![(0, 0)]); // element 0 of F(A,A) → slot 0
                m
            },
            backward_action: {
                let mut m = BTreeMap::new();
                m.insert("f".into(), vec![(0, 0)]); // element 0 of F(B,B) → slot 0
                m
            },
        };

        let coend = DeclaredFiniteCoend::compute(&input);
        // 0 and 1 are identified, so only 1 class.
        assert_eq!(coend.classes.len(), 1);
        assert_eq!(coend.identifications.len(), 1);
    }
}
