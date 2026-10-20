use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct EmptyType {
    pub id: String,
}

impl EmptyType {
    pub fn validate(&self) -> Result<(), EmptyTypeError> {
        if self.id.is_empty() {
            return Err(EmptyTypeError::EmptyId);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum EmptyTypeError {
    #[error("empty type id must be non-empty")]
    EmptyId,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let empty = EmptyType {
            id: "Empty".to_string(),
        };
        assert!(empty.validate().is_ok());
    }

    #[test]
    fn validate_rejects_empty_id() {
        let empty = EmptyType { id: String::new() };
        assert_eq!(empty.validate(), Err(EmptyTypeError::EmptyId));
    }
}

// Finite categorical interpretation: a initial object is a model of the
// categorical empty object. This does not prove arbitrary HoTT references uninhabited.
// AuthorityEffect: None.
use crate::quasi_category::{CategoryError, FiniteCategory};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct InitialEmptyLimits {
    pub max_objects: usize,
    pub max_arrows: usize,
    pub max_reference_bytes: usize,
    /// Per-call bound on iterated or directly read arrow records, plus the composition-table lookup in
    /// coherence queries. Does not bound the caller's category allocation.
    pub max_arrow_visits: usize,
}
impl Default for InitialEmptyLimits {
    fn default() -> Self {
        Self {
            max_objects: 4096,
            max_arrows: 4096,
            max_reference_bytes: 65536,
            max_arrow_visits: 1_000_000,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum InitialEmptyError {
    #[error(transparent)]
    Presentation(#[from] EmptyTypeError),
    #[error(transparent)]
    Category(#[from] CategoryError),
    #[error("initial-unit resource arithmetic overflows usize")]
    CountOverflow,
    #[error("{resource} needs {requested} units, above limit {limit}")]
    Limit {
        resource: &'static str,
        requested: usize,
        limit: usize,
    },
    #[error("object {object} has no arrow from proposed initial object {initial}")]
    MissingFactor { object: usize, initial: usize },
    #[error("object {object} has distinct factors {first} and {second} from the proposed initial")]
    NonUniqueFactor {
        object: usize,
        first: usize,
        second: usize,
    },
}

fn initial_empty_limit(
    resource: &'static str,
    requested: usize,
    limit: usize,
) -> Result<(), InitialEmptyError> {
    if requested > limit {
        return Err(InitialEmptyError::Limit {
            resource,
            requested,
            limit,
        });
    }
    Ok(())
}

fn initial_empty_factor(
    category: &FiniteCategory,
    target: usize,
    initial: usize,
) -> Result<usize, InitialEmptyError> {
    let mut factors = category.hom(initial, target)?;
    let first = factors
        .next()
        .map(|(index, _)| index)
        .ok_or(InitialEmptyError::MissingFactor {
            object: target,
            initial,
        })?;
    if let Some((second, _)) = factors.next() {
        return Err(InitialEmptyError::NonUniqueFactor {
            object: target,
            first,
            second,
        });
    }
    Ok(first)
}

/// An immutable certificate of the initial-object universal property in an
/// already admitted finite category. The presentation's names remain opaque;
/// the caller explicitly supplies their interpretation as the chosen object.
///
/// Admission scans every Hom(initial, x), checking existence and uniqueness.
/// The borrowed category has private immutable tables and already satisfies
/// unit, composition and associativity laws. Thus the unique factors form a
/// natural transformation from the constant initial functor to the identity.
/// Queries return replayable arrow identifiers; no model operation allocates.
///
/// ```compile_fail
/// use tfqm_homotopy_type_theory::unit_type::{InitialEmpty, InitialEmptyLimits, EmptyType};
/// use tfqm_homotopy_type_theory::quasi_category::FiniteCategory;
/// fn forge<'a>(declaration: &'a EmptyType, category: &'a FiniteCategory) -> InitialEmpty<'a> {
///     InitialEmpty { declaration, category, initial: 0, limits: InitialEmptyLimits::default() }
/// }
/// ```
#[derive(Debug)]
pub struct InitialEmpty<'a> {
    declaration: &'a EmptyType,
    category: &'a FiniteCategory,
    initial: usize,
    limits: InitialEmptyLimits,
}

fn admit_initial_empty(
    declaration: &EmptyType,
    category: &FiniteCategory,
    initial: usize,
    limits: InitialEmptyLimits,
) -> Result<(), InitialEmptyError> {
    let bytes = declaration.id.len();
    initial_empty_limit("reference bytes", bytes, limits.max_reference_bytes)?;
    category.identity(initial)?;
    initial_empty_limit("objects", category.object_count(), limits.max_objects)?;
    initial_empty_limit("arrows", category.arrows().len(), limits.max_arrows)?;
    let visits = category
        .object_count()
        .checked_mul(category.arrows().len())
        .ok_or(InitialEmptyError::CountOverflow)?;
    initial_empty_limit("arrow visits", visits, limits.max_arrow_visits)?;
    Ok(())
}

impl EmptyType {
    /// Check the finite initial-object interpretation without copying either
    /// the presentation or category, under inclusive per-call resource limits.
    pub fn initial_model<'a>(
        &'a self,
        category: &'a FiniteCategory,
        initial: usize,
        limits: InitialEmptyLimits,
    ) -> Result<InitialEmpty<'a>, InitialEmptyError> {
        self.validate()?;
        admit_initial_empty(self, category, initial, limits)?;
        for source in 0..category.object_count() {
            initial_empty_factor(category, source, initial)?;
        }
        Ok(InitialEmpty {
            declaration: self,
            category,
            initial,
            limits,
        })
    }
}

impl<'a> InitialEmpty<'a> {
    pub fn declaration(&self) -> &'a EmptyType {
        self.declaration
    }
    pub fn category(&self) -> &'a FiniteCategory {
        self.category
    }
    pub fn initial(&self) -> usize {
        self.initial
    }

    /// The unique arrow from the chosen initial object to target. Invalid
    /// target identifiers are refused by the admitted category's public API.
    pub fn factor(&self, target: usize) -> Result<usize, InitialEmptyError> {
        initial_empty_limit(
            "arrow visits",
            self.category.arrows().len(),
            self.limits.max_arrow_visits,
        )?;
        initial_empty_factor(self.category, target, self.initial)
    }

    /// Check initial_to_source ; f = initial_to_target for a supplied arrow f. The admission proof
    /// guarantees equality; this query exposes its concrete replay boundary.
    pub fn coherence(&self, arrow: usize) -> Result<bool, InitialEmptyError> {
        let visits = self
            .category
            .arrows()
            .len()
            .checked_mul(2)
            .and_then(|value| value.checked_add(4))
            .ok_or(InitialEmptyError::CountOverflow)?;
        initial_empty_limit("arrow visits", visits, self.limits.max_arrow_visits)?;
        let f = self.category.arrow(arrow)?;
        let source_factor = self.factor(f.source)?;
        Ok(self.category.compose(source_factor, arrow)? == self.factor(f.target)?)
    }
}

#[cfg(test)]
mod initial_empty_challenges {
    use super::*;
    use crate::quasi_category::{Arrow, CategoryLimits};

    fn declaration() -> EmptyType {
        EmptyType { id: "0".into() }
    }

    fn poset(objects: usize, relation: &[bool]) -> FiniteCategory {
        let arrows: Vec<_> = (0..objects)
            .flat_map(|source| {
                (0..objects).filter_map(move |target| {
                    relation[source * objects + target].then_some(Arrow { source, target })
                })
            })
            .collect();
        let identities = (0..objects)
            .map(|object| {
                arrows
                    .iter()
                    .position(|a| a.source == object && a.target == object)
                    .unwrap()
            })
            .collect();
        let arrow_slice = &arrows;
        let composition = arrows
            .iter()
            .flat_map(|first| {
                arrow_slice.iter().map(move |second| {
                    if first.target == second.source {
                        arrow_slice
                            .iter()
                            .position(|a| a.source == first.source && a.target == second.target)
                    } else {
                        None
                    }
                })
            })
            .collect();
        FiniteCategory::try_new(
            objects,
            arrows,
            identities,
            composition,
            CategoryLimits::default(),
        )
        .unwrap()
    }

    #[test]
    fn every_small_partial_order_matches_the_literal_least_element_oracle() {
        let declaration = declaration();
        for objects in 1..=3 {
            for code in 0..(1usize << (objects * objects)) {
                let relation: Vec<_> = (0..objects * objects)
                    .map(|bit| code & (1 << bit) != 0)
                    .collect();
                let reflexive = (0..objects).all(|a| relation[a * objects + a]);
                let antisymmetric = (0..objects).all(|a| {
                    (0..objects).all(|b| {
                        a == b || !(relation[a * objects + b] && relation[b * objects + a])
                    })
                });
                let transitive = (0..objects).all(|a| {
                    (0..objects).all(|b| {
                        (0..objects).all(|c| {
                            !(relation[a * objects + b] && relation[b * objects + c])
                                || relation[a * objects + c]
                        })
                    })
                });
                if !(reflexive && antisymmetric && transitive) {
                    continue;
                }
                let category = poset(objects, &relation);
                for initial in 0..objects {
                    let expected = (0..objects).all(|source| relation[initial * objects + source]);
                    match declaration.initial_model(
                        &category,
                        initial,
                        InitialEmptyLimits::default(),
                    ) {
                        Ok(model) => {
                            assert!(expected);
                            assert_eq!(model.declaration(), &declaration);
                            assert_eq!(model.initial(), initial);
                            assert!(std::ptr::eq(model.category(), &category));
                            for source in 0..objects {
                                let factor = category.arrow(model.factor(source).unwrap()).unwrap();
                                assert_eq!((factor.source, factor.target), (initial, source));
                            }
                            for arrow in 0..category.arrows().len() {
                                assert_eq!(model.coherence(arrow), Ok(true));
                            }
                        }
                        Err(InitialEmptyError::MissingFactor { .. }) => assert!(!expected),
                        Err(error) => panic!("unexpected refusal: {error}"),
                    }
                }
            }
        }
    }

    #[test]
    fn nontrivial_endomorphisms_and_empty_categories_refuse_false_unit_models() {
        let declaration = declaration();
        let group = FiniteCategory::try_new(
            1,
            vec![
                Arrow {
                    source: 0,
                    target: 0
                };
                2
            ],
            vec![0],
            vec![Some(0), Some(1), Some(1), Some(0)],
            CategoryLimits::default(),
        )
        .unwrap();
        assert!(matches!(
            declaration.initial_model(&group, 0, InitialEmptyLimits::default()),
            Err(InitialEmptyError::NonUniqueFactor {
                object: 0,
                first: 0,
                second: 1
            })
        ));
        let empty =
            FiniteCategory::try_new(0, vec![], vec![], vec![], CategoryLimits::default()).unwrap();
        assert!(matches!(
            declaration.initial_model(&empty, 0, InitialEmptyLimits::default()),
            Err(InitialEmptyError::Category(
                CategoryError::ObjectOutOfBounds { object: 0 }
            ))
        ));
    }

    #[test]
    fn independent_limits_query_domains_and_utf8_names_are_checked() {
        let declaration = declaration();
        let category = poset(2, &[true, true, false, true]);
        let exact = InitialEmptyLimits {
            max_objects: 2,
            max_arrows: 3,
            max_reference_bytes: 1,
            max_arrow_visits: 6,
        };
        let model = declaration.initial_model(&category, 0, exact).unwrap();
        assert!(matches!(
            model.coherence(1),
            Err(InitialEmptyError::Limit {
                resource: "arrow visits",
                requested: 10,
                limit: 6
            })
        ));
        // Two Hom scans visit three records each. The supplied arrow read,
        // two endpoint arrow reads inside compose, and its table lookup
        // add four more units: exactly ten.
        let short = declaration
            .initial_model(
                &category,
                0,
                InitialEmptyLimits {
                    max_arrow_visits: 9,
                    ..exact
                },
            )
            .unwrap();
        assert!(matches!(
            short.coherence(1),
            Err(InitialEmptyError::Limit {
                requested: 10,
                limit: 9,
                ..
            })
        ));
        let inclusive = declaration
            .initial_model(
                &category,
                0,
                InitialEmptyLimits {
                    max_arrow_visits: 10,
                    ..exact
                },
            )
            .unwrap();
        assert_eq!(inclusive.coherence(1), Ok(true));
        for limits in [
            InitialEmptyLimits {
                max_objects: 1,
                ..exact
            },
            InitialEmptyLimits {
                max_arrows: 2,
                ..exact
            },
            InitialEmptyLimits {
                max_reference_bytes: 0,
                ..exact
            },
            InitialEmptyLimits {
                max_arrow_visits: 5,
                ..exact
            },
        ] {
            assert!(matches!(
                declaration.initial_model(&category, 0, limits),
                Err(InitialEmptyError::Limit { .. })
            ));
        }
        let admitted = declaration
            .initial_model(&category, 0, InitialEmptyLimits::default())
            .unwrap();
        assert!(matches!(
            admitted.factor(2),
            Err(InitialEmptyError::Category(
                CategoryError::ObjectOutOfBounds { object: 2 }
            ))
        ));
        assert!(matches!(
            admitted.coherence(3),
            Err(InitialEmptyError::Category(
                CategoryError::ArrowOutOfBounds { arrow: 3 }
            ))
        ));
        let unicode = EmptyType { id: "é".into() };
        assert!(unicode
            .initial_model(
                &category,
                0,
                InitialEmptyLimits {
                    max_reference_bytes: 2,
                    ..exact
                }
            )
            .is_ok());
        assert!(matches!(
            unicode.initial_model(&category, 0, exact),
            Err(InitialEmptyError::Limit {
                resource: "reference bytes",
                requested: 2,
                limit: 1
            })
        ));
        let invalid = EmptyType { id: String::new() };
        assert!(matches!(
            invalid.initial_model(&category, 0, exact),
            Err(InitialEmptyError::Presentation(EmptyTypeError::EmptyId))
        ));
    }
}
