use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct UnitType {
    pub id: String,
    pub unit_term_ref: String,
}

impl UnitType {
    pub fn validate(&self) -> Result<(), UnitTypeError> {
        if self.id.is_empty() {
            return Err(UnitTypeError::EmptyId);
        }
        if self.unit_term_ref.is_empty() {
            return Err(UnitTypeError::EmptyUnitTermRef);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum UnitTypeError {
    #[error("unit type id must be non-empty")]
    EmptyId,
    #[error("unit type unit_term_ref must be non-empty")]
    EmptyUnitTermRef,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let unit = UnitType {
            id: "Unit".to_string(),
            unit_term_ref: "star".to_string(),
        };
        assert!(unit.validate().is_ok());
    }

    #[test]
    fn validate_rejects_empty_id() {
        let unit = UnitType {
            id: String::new(),
            unit_term_ref: "star".to_string(),
        };
        assert_eq!(unit.validate(), Err(UnitTypeError::EmptyId));
    }

    #[test]
    fn validate_rejects_empty_unit_term() {
        let unit = UnitType {
            id: "Unit".to_string(),
            unit_term_ref: String::new(),
        };
        assert_eq!(unit.validate(), Err(UnitTypeError::EmptyUnitTermRef));
    }
}

// Finite categorical interpretation: a terminal object is a model of the
// categorical unit. This does not prove arbitrary HoTT references inhabited.
// AuthorityEffect: None.
use crate::quasi_category::{CategoryError, FiniteCategory};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TerminalUnitLimits {
    pub max_objects: usize,
    pub max_arrows: usize,
    pub max_reference_bytes: usize,
    /// Per-call bound on iterated or directly read arrow records, plus the composition-table lookup in
    /// coherence queries. Does not bound the caller's category allocation.
    pub max_arrow_visits: usize,
}
impl Default for TerminalUnitLimits {
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
pub enum TerminalUnitError {
    #[error(transparent)]
    Presentation(#[from] UnitTypeError),
    #[error(transparent)]
    Category(#[from] CategoryError),
    #[error("terminal-unit resource arithmetic overflows usize")]
    CountOverflow,
    #[error("{resource} needs {requested} units, above limit {limit}")]
    Limit {
        resource: &'static str,
        requested: usize,
        limit: usize,
    },
    #[error("object {object} has no arrow to proposed terminal object {terminal}")]
    MissingFactor { object: usize, terminal: usize },
    #[error("object {object} has distinct factors {first} and {second} to the proposed terminal")]
    NonUniqueFactor {
        object: usize,
        first: usize,
        second: usize,
    },
}

fn terminal_unit_limit(
    resource: &'static str,
    requested: usize,
    limit: usize,
) -> Result<(), TerminalUnitError> {
    if requested > limit {
        return Err(TerminalUnitError::Limit {
            resource,
            requested,
            limit,
        });
    }
    Ok(())
}

fn terminal_unit_factor(
    category: &FiniteCategory,
    source: usize,
    terminal: usize,
) -> Result<usize, TerminalUnitError> {
    let mut factors = category.hom(source, terminal)?;
    let first = factors
        .next()
        .map(|(index, _)| index)
        .ok_or(TerminalUnitError::MissingFactor {
            object: source,
            terminal,
        })?;
    if let Some((second, _)) = factors.next() {
        return Err(TerminalUnitError::NonUniqueFactor {
            object: source,
            first,
            second,
        });
    }
    Ok(first)
}

/// An immutable certificate of the terminal-object universal property in an
/// already admitted finite category. The presentation's names remain opaque;
/// the caller explicitly supplies their interpretation as the chosen object.
///
/// Admission scans every Hom(x, terminal), checking existence and uniqueness.
/// The borrowed category has private immutable tables and already satisfies
/// unit, composition and associativity laws. Thus the unique factors form a
/// natural transformation from the identity to the constant terminal functor.
/// Queries return replayable arrow identifiers; no model operation allocates.
///
/// ```compile_fail
/// use tfqm_homotopy_type_theory::unit_type::{TerminalUnit, TerminalUnitLimits, UnitType};
/// use tfqm_homotopy_type_theory::quasi_category::FiniteCategory;
/// fn forge<'a>(declaration: &'a UnitType, category: &'a FiniteCategory) -> TerminalUnit<'a> {
///     TerminalUnit { declaration, category, terminal: 0, limits: TerminalUnitLimits::default() }
/// }
/// ```
#[derive(Debug)]
pub struct TerminalUnit<'a> {
    declaration: &'a UnitType,
    category: &'a FiniteCategory,
    terminal: usize,
    limits: TerminalUnitLimits,
}

fn admit_terminal_unit(
    declaration: &UnitType,
    category: &FiniteCategory,
    terminal: usize,
    limits: TerminalUnitLimits,
) -> Result<(), TerminalUnitError> {
    let bytes = declaration
        .id
        .len()
        .checked_add(declaration.unit_term_ref.len())
        .ok_or(TerminalUnitError::CountOverflow)?;
    terminal_unit_limit("reference bytes", bytes, limits.max_reference_bytes)?;
    category.identity(terminal)?;
    terminal_unit_limit("objects", category.object_count(), limits.max_objects)?;
    terminal_unit_limit("arrows", category.arrows().len(), limits.max_arrows)?;
    let visits = category
        .object_count()
        .checked_mul(category.arrows().len())
        .ok_or(TerminalUnitError::CountOverflow)?;
    terminal_unit_limit("arrow visits", visits, limits.max_arrow_visits)?;
    Ok(())
}

impl UnitType {
    /// Check the finite terminal-object interpretation without copying either
    /// the presentation or category, under inclusive per-call resource limits.
    pub fn terminal_model<'a>(
        &'a self,
        category: &'a FiniteCategory,
        terminal: usize,
        limits: TerminalUnitLimits,
    ) -> Result<TerminalUnit<'a>, TerminalUnitError> {
        self.validate()?;
        admit_terminal_unit(self, category, terminal, limits)?;
        for source in 0..category.object_count() {
            terminal_unit_factor(category, source, terminal)?;
        }
        Ok(TerminalUnit {
            declaration: self,
            category,
            terminal,
            limits,
        })
    }
}

impl<'a> TerminalUnit<'a> {
    pub fn declaration(&self) -> &'a UnitType {
        self.declaration
    }
    pub fn category(&self) -> &'a FiniteCategory {
        self.category
    }
    pub fn terminal(&self) -> usize {
        self.terminal
    }

    /// The unique arrow from source to the chosen terminal object. Invalid
    /// source identifiers are refused by the admitted category's public API.
    pub fn factor(&self, source: usize) -> Result<usize, TerminalUnitError> {
        terminal_unit_limit(
            "arrow visits",
            self.category.arrows().len(),
            self.limits.max_arrow_visits,
        )?;
        terminal_unit_factor(self.category, source, self.terminal)
    }

    /// Check f ; !target = !source for a supplied arrow f. The admission proof
    /// guarantees equality; this query exposes its concrete replay boundary.
    pub fn coherence(&self, arrow: usize) -> Result<bool, TerminalUnitError> {
        let visits = self
            .category
            .arrows()
            .len()
            .checked_mul(2)
            .and_then(|value| value.checked_add(2))
            .ok_or(TerminalUnitError::CountOverflow)?;
        terminal_unit_limit("arrow visits", visits, self.limits.max_arrow_visits)?;
        let f = self.category.arrow(arrow)?;
        let target_factor = self.factor(f.target)?;
        Ok(self.category.compose(arrow, target_factor)? == self.factor(f.source)?)
    }
}

#[cfg(test)]
mod terminal_unit_challenges {
    use super::*;
    use crate::quasi_category::{Arrow, CategoryLimits};

    fn declaration() -> UnitType {
        UnitType {
            id: "1".into(),
            unit_term_ref: "*".into(),
        }
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
    fn every_small_partial_order_matches_the_literal_greatest_element_oracle() {
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
                for terminal in 0..objects {
                    let expected = (0..objects).all(|source| relation[source * objects + terminal]);
                    match declaration.terminal_model(
                        &category,
                        terminal,
                        TerminalUnitLimits::default(),
                    ) {
                        Ok(model) => {
                            assert!(expected);
                            assert_eq!(model.declaration(), &declaration);
                            assert_eq!(model.terminal(), terminal);
                            assert!(std::ptr::eq(model.category(), &category));
                            for source in 0..objects {
                                let factor = category.arrow(model.factor(source).unwrap()).unwrap();
                                assert_eq!((factor.source, factor.target), (source, terminal));
                            }
                            for arrow in 0..category.arrows().len() {
                                assert_eq!(model.coherence(arrow), Ok(true));
                            }
                        }
                        Err(TerminalUnitError::MissingFactor { .. }) => assert!(!expected),
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
            declaration.terminal_model(&group, 0, TerminalUnitLimits::default()),
            Err(TerminalUnitError::NonUniqueFactor {
                object: 0,
                first: 0,
                second: 1
            })
        ));
        let empty =
            FiniteCategory::try_new(0, vec![], vec![], vec![], CategoryLimits::default()).unwrap();
        assert!(matches!(
            declaration.terminal_model(&empty, 0, TerminalUnitLimits::default()),
            Err(TerminalUnitError::Category(
                CategoryError::ObjectOutOfBounds { object: 0 }
            ))
        ));
    }

    #[test]
    fn independent_limits_query_domains_and_utf8_names_are_checked() {
        let declaration = declaration();
        let category = poset(2, &[true, true, false, true]);
        let exact = TerminalUnitLimits {
            max_objects: 2,
            max_arrows: 3,
            max_reference_bytes: 2,
            max_arrow_visits: 6,
        };
        let model = declaration.terminal_model(&category, 1, exact).unwrap();
        assert!(matches!(
            model.coherence(1),
            Err(TerminalUnitError::Limit {
                resource: "arrow visits",
                requested: 8,
                limit: 6
            })
        ));
        // Two Hom scans visit three records each; the supplied arrow read
        // and composition-table lookup add two more units: exactly eight.
        let short = declaration
            .terminal_model(
                &category,
                1,
                TerminalUnitLimits {
                    max_arrow_visits: 7,
                    ..exact
                },
            )
            .unwrap();
        assert!(matches!(
            short.coherence(1),
            Err(TerminalUnitError::Limit {
                requested: 8,
                limit: 7,
                ..
            })
        ));
        let inclusive = declaration
            .terminal_model(
                &category,
                1,
                TerminalUnitLimits {
                    max_arrow_visits: 8,
                    ..exact
                },
            )
            .unwrap();
        assert_eq!(inclusive.coherence(1), Ok(true));
        for limits in [
            TerminalUnitLimits {
                max_objects: 1,
                ..exact
            },
            TerminalUnitLimits {
                max_arrows: 2,
                ..exact
            },
            TerminalUnitLimits {
                max_reference_bytes: 1,
                ..exact
            },
            TerminalUnitLimits {
                max_arrow_visits: 5,
                ..exact
            },
        ] {
            assert!(matches!(
                declaration.terminal_model(&category, 1, limits),
                Err(TerminalUnitError::Limit { .. })
            ));
        }
        let admitted = declaration
            .terminal_model(&category, 1, TerminalUnitLimits::default())
            .unwrap();
        assert!(matches!(
            admitted.factor(2),
            Err(TerminalUnitError::Category(
                CategoryError::ObjectOutOfBounds { object: 2 }
            ))
        ));
        assert!(matches!(
            admitted.coherence(3),
            Err(TerminalUnitError::Category(
                CategoryError::ArrowOutOfBounds { arrow: 3 }
            ))
        ));
        let unicode = UnitType {
            id: "é".into(),
            unit_term_ref: "*".into(),
        };
        assert!(unicode
            .terminal_model(
                &category,
                1,
                TerminalUnitLimits {
                    max_reference_bytes: 3,
                    ..exact
                }
            )
            .is_ok());
        assert!(matches!(
            unicode.terminal_model(&category, 1, exact),
            Err(TerminalUnitError::Limit {
                resource: "reference bytes",
                requested: 3,
                limit: 2
            })
        ));
        let invalid = UnitType {
            id: String::new(),
            unit_term_ref: "*".into(),
        };
        assert!(matches!(
            invalid.terminal_model(&category, 1, exact),
            Err(TerminalUnitError::Presentation(UnitTypeError::EmptyId))
        ));
    }
}
