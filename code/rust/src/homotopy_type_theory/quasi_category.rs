//! Nerves of admitted finite categories. AuthorityEffect: None.
//!
//! Unit and associativity checks admit a category before nerve construction.
//! The nerve of a category has unique inner-horn fillers; this module does not
//! accept an arbitrary simplicial set or claim to decide its infinite Kan laws.
#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Arrow {
    pub source: usize,
    pub target: usize,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CategoryLimits {
    pub max_table_cells: usize,
    pub max_check_operations: usize,
    pub max_simplex_edges: usize,
}
impl Default for CategoryLimits {
    fn default() -> Self {
        Self {
            max_table_cells: 4096,
            max_check_operations: 1_000_000,
            max_simplex_edges: 4096,
        }
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CategoryError {
    CountOverflow,
    Limit {
        resource: &'static str,
        requested: usize,
        limit: usize,
    },
    Shape {
        resource: &'static str,
        expected: usize,
        actual: usize,
    },
    ObjectOutOfBounds {
        object: usize,
    },
    ArrowOutOfBounds {
        arrow: usize,
    },
    InvalidIdentity {
        object: usize,
    },
    InvalidComposition {
        first: usize,
        second: usize,
    },
    UnitLaw {
        arrow: usize,
    },
    Associativity {
        first: usize,
        second: usize,
        third: usize,
    },
    NotComposable {
        first: usize,
        second: usize,
    },
    PathEndpoint {
        expected: usize,
        actual: usize,
    },
    FaceOutOfBounds {
        face: usize,
        dimension: usize,
    },
    DegeneracyOutOfBounds {
        vertex: usize,
        dimension: usize,
    },
    VertexOutOfBounds {
        vertex: usize,
        dimension: usize,
    },
    AllocationFailed {
        edges: usize,
    },
}
impl std::fmt::Display for CategoryError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}
impl std::error::Error for CategoryError {}
type Result<T> = std::result::Result<T, CategoryError>;
fn add(a: usize, b: usize) -> Result<usize> {
    a.checked_add(b).ok_or(CategoryError::CountOverflow)
}
fn mul(a: usize, b: usize) -> Result<usize> {
    a.checked_mul(b).ok_or(CategoryError::CountOverflow)
}
fn admit(resource: &'static str, requested: usize, limit: usize) -> Result<()> {
    if requested > limit {
        return Err(CategoryError::Limit {
            resource,
            requested,
            limit,
        });
    }
    Ok(())
}
fn shape(resource: &'static str, expected: usize, actual: usize) -> Result<()> {
    if expected != actual {
        return Err(CategoryError::Shape {
            resource,
            expected,
            actual,
        });
    }
    Ok(())
}

/// Immutable evidence of all finite category laws for this complete table.
/// table[f*m+g] means g after f; it is Some exactly for composable pairs.
/// ```compile_fail
/// use tfqm_homotopy_type_theory::quasi_category::{FiniteCategory,CategoryLimits};
/// let _ = FiniteCategory { objects: 1, arrows: vec![], identities: vec![],
///     composition: vec![], limits: CategoryLimits::default() };
/// ```
/// ```
/// use tfqm_homotopy_type_theory::quasi_category::{Arrow, FiniteCategory, CategoryLimits, QuasiCategory};
/// let category = FiniteCategory::try_new(1, vec![Arrow { source: 0, target: 0 }],
///     vec![0], vec![Some(0)], CategoryLimits::default())?;
/// let nerve = QuasiCategory::from_category(category);
/// assert_eq!(nerve.simplex(0, &[0, 0])?.face(1)?.edges(), &[0]);
/// # Ok::<(), tfqm_homotopy_type_theory::quasi_category::CategoryError>(())
/// ```
#[derive(Debug, PartialEq, Eq)]
pub struct FiniteCategory {
    objects: usize,
    arrows: Vec<Arrow>,
    identities: Vec<usize>,
    composition: Vec<Option<usize>>,
    limits: CategoryLimits,
}
impl FiniteCategory {
    pub fn try_new(
        objects: usize,
        arrows: Vec<Arrow>,
        identities: Vec<usize>,
        composition: Vec<Option<usize>>,
        limits: CategoryLimits,
    ) -> Result<Self> {
        admit_category_input(
            objects,
            arrows.len(),
            identities.len(),
            composition.len(),
            limits,
        )?;
        let category = Self {
            objects,
            arrows,
            identities,
            composition,
            limits,
        };
        category.check_endpoints()?;
        category.check_identities()?;
        category.check_compositions()?;
        category.check_units()?;
        category.check_associativity()?;
        Ok(category)
    }
    pub fn object_count(&self) -> usize {
        self.objects
    }
    pub fn arrows(&self) -> &[Arrow] {
        &self.arrows
    }
    pub fn arrow(&self, index: usize) -> Result<&Arrow> {
        self.arrows
            .get(index)
            .ok_or(CategoryError::ArrowOutOfBounds { arrow: index })
    }
    pub fn identity(&self, object: usize) -> Result<usize> {
        self.identities
            .get(object)
            .copied()
            .ok_or(CategoryError::ObjectOutOfBounds { object })
    }
    pub fn compose(&self, first: usize, second: usize) -> Result<usize> {
        let f = self.arrow(first)?;
        let g = self.arrow(second)?;
        if f.target != g.source {
            return Err(CategoryError::NotComposable { first, second });
        }
        // Private table has m*m entries; first,second<m proves this index fits.
        self.composition[first * self.arrows.len() + second]
            .ok_or(CategoryError::InvalidComposition { first, second })
    }
    pub fn hom(
        &self,
        source: usize,
        target: usize,
    ) -> Result<impl Iterator<Item = (usize, &Arrow)>> {
        self.identity(source)?;
        self.identity(target)?;
        Ok(self
            .arrows
            .iter()
            .enumerate()
            .filter(move |(_, a)| a.source == source && a.target == target))
    }
    fn check_endpoints(&self) -> Result<()> {
        for arrow in &self.arrows {
            self.check_object(arrow.source)?;
            self.check_object(arrow.target)?;
        }
        Ok(())
    }
    fn check_object(&self, object: usize) -> Result<()> {
        if object >= self.objects {
            return Err(CategoryError::ObjectOutOfBounds { object });
        }
        Ok(())
    }
    fn check_identities(&self) -> Result<()> {
        for (object, &identity) in self.identities.iter().enumerate() {
            let arrow = self.arrow(identity)?;
            if arrow.source != object || arrow.target != object {
                return Err(CategoryError::InvalidIdentity { object });
            }
        }
        Ok(())
    }
    fn check_compositions(&self) -> Result<()> {
        for first in 0..self.arrows.len() {
            for second in 0..self.arrows.len() {
                self.check_composition(first, second)?;
            }
        }
        Ok(())
    }
    fn check_composition(&self, first: usize, second: usize) -> Result<()> {
        let f = &self.arrows[first];
        let g = &self.arrows[second];
        let composite = self.composition[first * self.arrows.len() + second];
        if f.target != g.source {
            if composite.is_some() {
                return Err(CategoryError::InvalidComposition { first, second });
            }
            return Ok(());
        }
        let id = composite.ok_or(CategoryError::InvalidComposition { first, second })?;
        let result = self.arrow(id)?;
        if result.source != f.source || result.target != g.target {
            return Err(CategoryError::InvalidComposition { first, second });
        }
        Ok(())
    }
    fn check_units(&self) -> Result<()> {
        for (id, arrow) in self.arrows.iter().enumerate() {
            let left = self.compose(self.identities[arrow.source], id)?;
            let right = self.compose(id, self.identities[arrow.target])?;
            if left != id || right != id {
                return Err(CategoryError::UnitLaw { arrow: id });
            }
        }
        Ok(())
    }
    fn check_associativity(&self) -> Result<()> {
        for first in 0..self.arrows.len() {
            for second in 0..self.arrows.len() {
                if self.arrows[first].target == self.arrows[second].source {
                    self.check_associative_pair(first, second)?;
                }
            }
        }
        Ok(())
    }
    fn check_associative_pair(&self, first: usize, second: usize) -> Result<()> {
        for third in 0..self.arrows.len() {
            if self.arrows[second].target == self.arrows[third].source {
                let left = self.compose(self.compose(first, second)?, third)?;
                let right = self.compose(first, self.compose(second, third)?)?;
                if left != right {
                    return Err(CategoryError::Associativity {
                        first,
                        second,
                        third,
                    });
                }
            }
        }
        Ok(())
    }
}
fn admit_category_input(
    objects: usize,
    arrows: usize,
    identities: usize,
    cells: usize,
    limits: CategoryLimits,
) -> Result<()> {
    let expected = mul(arrows, arrows)?;
    admit("table cells", expected, limits.max_table_cells)?;
    shape("identities", objects, identities)?;
    shape("composition", expected, cells)?;
    let checks = category_work(objects, arrows, expected)?;
    admit("category checks", checks, limits.max_check_operations)
}
fn category_work(objects: usize, arrows: usize, cells: usize) -> Result<usize> {
    // Conservative loop/lookup units: endpoints, identities, cells, unit replay,
    // composable-pair scans and at most four composition lookups per triple.
    add(
        add(mul(objects, 2)?, mul(arrows, 8)?)?,
        add(mul(cells, 4)?, mul(mul(cells, arrows)?, 5)?)?,
    )
}

/// A category nerve has no unverified mutable "Kan verified" flag.
/// Its inner-horn uniqueness follows from the checked category laws: inner
/// faces compose adjacent arrows, and associativity makes repeated faces agree.
#[derive(Debug, PartialEq, Eq)]
pub struct QuasiCategory {
    category: FiniteCategory,
}
impl QuasiCategory {
    pub fn from_category(category: FiniteCategory) -> Self {
        Self { category }
    }
    pub fn category(&self) -> &FiniteCategory {
        &self.category
    }
    pub fn simplex(&self, start: usize, edges: &[usize]) -> Result<NerveSimplex<'_>> {
        admit(
            "simplex edges",
            edges.len(),
            self.category.limits.max_simplex_edges,
        )?;
        self.category.check_object(start)?;
        check_path(&self.category, start, edges)?;
        Ok(NerveSimplex {
            category: &self.category,
            start,
            edges: copy_edges(edges)?,
        })
    }
}
fn check_path(category: &FiniteCategory, start: usize, edges: &[usize]) -> Result<()> {
    let mut current = start;
    for &edge in edges {
        let arrow = category.arrow(edge)?;
        if arrow.source != current {
            return Err(CategoryError::PathEndpoint {
                expected: current,
                actual: arrow.source,
            });
        }
        current = arrow.target;
    }
    Ok(())
}
fn edge_buffer(count: usize) -> Result<Vec<usize>> {
    let mut edges = Vec::new();
    edges
        .try_reserve_exact(count)
        .map_err(|_| CategoryError::AllocationFailed { edges: count })?;
    Ok(edges)
}
fn copy_edges(source: &[usize]) -> Result<Vec<usize>> {
    let mut edges = edge_buffer(source.len())?;
    edges.extend_from_slice(source);
    Ok(edges)
}

/// A finite simplex bound by lifetime to its immutable admitted category.
/// No path or category reference can be replaced through this public view.
/// ```compile_fail
/// use tfqm_homotopy_type_theory::quasi_category::{FiniteCategory, CategoryLimits, NerveSimplex};
/// let category = FiniteCategory::try_new(0, vec![], vec![], vec![], CategoryLimits::default()).unwrap();
/// let _ = NerveSimplex { category: &category, start: 0, edges: vec![] };
/// ```
#[derive(Debug)]
pub struct NerveSimplex<'a> {
    category: &'a FiniteCategory,
    start: usize,
    edges: Vec<usize>,
}
impl<'a> NerveSimplex<'a> {
    pub fn dimension(&self) -> usize {
        self.edges.len()
    }
    pub fn start(&self) -> usize {
        self.start
    }
    pub fn edges(&self) -> &[usize] {
        &self.edges
    }
    pub fn category(&self) -> &'a FiniteCategory {
        self.category
    }
    pub fn vertex(&self, index: usize) -> Result<usize> {
        if index == 0 {
            return Ok(self.start);
        }
        let edge = self
            .edges
            .get(index - 1)
            .ok_or(CategoryError::VertexOutOfBounds {
                vertex: index,
                dimension: self.dimension(),
            })?;
        Ok(self.category.arrow(*edge)?.target)
    }
    pub fn face(&self, index: usize) -> Result<Self> {
        if self.edges.is_empty() || index > self.dimension() {
            return Err(CategoryError::FaceOutOfBounds {
                face: index,
                dimension: self.dimension(),
            });
        }
        let mut output = edge_buffer(self.edges.len() - 1)?;
        let start = self.face_edges(index, &mut output)?;
        Ok(Self {
            category: self.category,
            start,
            edges: output,
        })
    }
    fn face_edges(&self, index: usize, output: &mut Vec<usize>) -> Result<usize> {
        if index == 0 {
            output.extend_from_slice(&self.edges[1..]);
            return self.vertex(1);
        }
        if index == self.dimension() {
            output.extend_from_slice(&self.edges[..index - 1]);
            return Ok(self.start);
        }
        output.extend_from_slice(&self.edges[..index - 1]);
        output.push(
            self.category
                .compose(self.edges[index - 1], self.edges[index])?,
        );
        output.extend_from_slice(&self.edges[index + 1..]);
        Ok(self.start)
    }
    pub fn degeneracy(&self, index: usize) -> Result<Self> {
        if index > self.dimension() {
            return Err(CategoryError::DegeneracyOutOfBounds {
                vertex: index,
                dimension: self.dimension(),
            });
        }
        let object = self.vertex(index)?;
        let count = add(self.edges.len(), 1)?;
        admit(
            "simplex edges",
            count,
            self.category.limits.max_simplex_edges,
        )?;
        let mut edges = edge_buffer(count)?;
        edges.extend_from_slice(&self.edges[..index]);
        edges.push(self.category.identity(object)?);
        edges.extend_from_slice(&self.edges[index..]);
        Ok(Self {
            category: self.category,
            start: self.start,
            edges,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn cyclic(order: usize) -> FiniteCategory {
        let arrows = vec![
            Arrow {
                source: 0,
                target: 0
            };
            order
        ];
        let composition = (0..order)
            .flat_map(|a| (0..order).map(move |b| Some((a + b) % order)))
            .collect();
        FiniteCategory::try_new(1, arrows, vec![0], composition, CategoryLimits::default()).unwrap()
    }
    #[test]
    fn category_laws_reject_incorrect_tables_and_endpoints() {
        let arrows = vec![
            Arrow {
                source: 0,
                target: 0
            };
            3
        ];
        // A unital, nonassociative magma: 1*1=2,1*2=1,2*1=0,2*2=2.
        let table = vec![0, 1, 2, 1, 2, 1, 2, 0, 2]
            .into_iter()
            .map(Some)
            .collect();
        assert!(matches!(
            FiniteCategory::try_new(1, arrows.clone(), vec![0], table, CategoryLimits::default()),
            Err(CategoryError::Associativity { .. })
        ));
        let table = vec![Some(0); 9];
        assert!(matches!(
            FiniteCategory::try_new(1, arrows, vec![0], table, CategoryLimits::default()),
            Err(CategoryError::UnitLaw { .. })
        ));
        assert!(FiniteCategory::try_new(
            1,
            vec![Arrow {
                source: 0,
                target: 1
            }],
            vec![0],
            vec![Some(0)],
            CategoryLimits::default()
        )
        .is_err());
        assert!(
            FiniteCategory::try_new(1, vec![], vec![0], vec![], CategoryLimits::default()).is_err()
        );
        assert!(
            FiniteCategory::try_new(0, vec![], vec![], vec![], CategoryLimits::default()).is_ok()
        );
    }
    #[test]
    fn all_unital_three_element_tables_match_the_independent_integer_law() {
        let mut admitted = 0;
        for mut code in 0..81 {
            let mut table = [0, 1, 2, 1, 0, 0, 2, 0, 0];
            for index in [4, 5, 7, 8] {
                table[index] = code % 3;
                code /= 3;
            }
            let expected = (0..3).all(|a| {
                (0..3).all(|b| {
                    (0..3)
                        .all(|c| table[table[a * 3 + b] * 3 + c] == table[a * 3 + table[b * 3 + c]])
                })
            });
            let result = FiniteCategory::try_new(
                1,
                vec![
                    Arrow {
                        source: 0,
                        target: 0
                    };
                    3
                ],
                vec![0],
                table.into_iter().map(Some).collect(),
                CategoryLimits::default(),
            );
            assert_eq!(result.is_ok(), expected, "table {table:?}");
            admitted += usize::from(result.is_ok());
        }
        assert_eq!(admitted, 11);
    }
    #[test]
    fn exact_inclusive_admission_and_extreme_counts() {
        let limits = CategoryLimits {
            max_table_cells: 1,
            max_check_operations: 19,
            max_simplex_edges: 1,
        };
        assert_eq!(category_work(1, 1, 1), Ok(19));
        assert!(FiniteCategory::try_new(
            1,
            vec![Arrow {
                source: 0,
                target: 0
            }],
            vec![0],
            vec![Some(0)],
            limits
        )
        .is_ok());
        assert!(admit_category_input(
            1,
            1,
            1,
            1,
            CategoryLimits {
                max_check_operations: 18,
                ..limits
            }
        )
        .is_err());
        assert_eq!(
            admit_category_input(0, usize::MAX, 0, 0, limits),
            Err(CategoryError::CountOverflow)
        );
        assert_eq!(
            admit_category_input(usize::MAX, 0, usize::MAX, 0, limits),
            Err(CategoryError::CountOverflow)
        );
        assert!(admit_category_input(1, 2, 1, 4, limits).is_err());
    }
    #[test]
    fn each_admission_role_has_a_specific_typed_refusal() {
        let d = CategoryLimits::default();
        let out_of_domain = vec![
            Arrow {
                source: 0,
                target: 0,
            },
            Arrow {
                source: 0,
                target: usize::MAX,
            },
        ];
        assert_eq!(
            FiniteCategory::try_new(
                1,
                out_of_domain,
                vec![0],
                vec![Some(0), Some(1), None, None],
                d
            )
            .err(),
            Some(CategoryError::ObjectOutOfBounds { object: usize::MAX })
        );
        assert_eq!(
            FiniteCategory::try_new(
                1,
                vec![Arrow {
                    source: usize::MAX,
                    target: 0
                }],
                vec![0],
                vec![Some(0)],
                d
            )
            .err(),
            Some(CategoryError::ObjectOutOfBounds { object: usize::MAX })
        );
        let a = vec![
            Arrow {
                source: 0,
                target: 0,
            },
            Arrow {
                source: 1,
                target: 1,
            },
        ];
        assert_eq!(
            FiniteCategory::try_new(
                2,
                a.clone(),
                vec![1, 0],
                vec![Some(0), None, None, Some(1)],
                d
            )
            .err(),
            Some(CategoryError::InvalidIdentity { object: 0 })
        );
        assert_eq!(
            FiniteCategory::try_new(
                2,
                a.clone(),
                vec![0, 1],
                vec![Some(0), Some(0), None, Some(1)],
                d
            )
            .err(),
            Some(CategoryError::InvalidComposition {
                first: 0,
                second: 1
            })
        );
        assert_eq!(
            FiniteCategory::try_new(2, a.clone(), vec![0, 1], vec![None, None, None, Some(1)], d)
                .err(),
            Some(CategoryError::InvalidComposition {
                first: 0,
                second: 0
            })
        );
        assert_eq!(
            FiniteCategory::try_new(
                2,
                a.clone(),
                vec![0, 1],
                vec![Some(1), None, None, Some(1)],
                d
            )
            .err(),
            Some(CategoryError::InvalidComposition {
                first: 0,
                second: 0
            })
        );
        assert_eq!(
            FiniteCategory::try_new(
                2,
                a,
                vec![0, 1],
                vec![Some(usize::MAX), None, None, Some(1)],
                d
            )
            .err(),
            Some(CategoryError::ArrowOutOfBounds { arrow: usize::MAX })
        );
        let c = cyclic(1);
        assert!(c.identity(usize::MAX).is_err());
        assert!(c.compose(usize::MAX, 0).is_err());
        assert!(c.hom(0, usize::MAX).is_err());
        let c = FiniteCategory::try_new(
            1,
            vec![Arrow {
                source: 0,
                target: 0,
            }],
            vec![0],
            vec![Some(0)],
            CategoryLimits {
                max_simplex_edges: 0,
                ..d
            },
        )
        .unwrap();
        let q = QuasiCategory::from_category(c);
        let point = q.simplex(0, &[]).unwrap();
        assert!(point.face(0).is_err());
        assert!(point.degeneracy(0).is_err());
        assert!(q.simplex(0, &[0]).is_err());
    }
    #[test]
    fn literal_arrow_category_paths_and_composition_failures() {
        let a = vec![
            Arrow {
                source: 0,
                target: 0,
            },
            Arrow {
                source: 1,
                target: 1,
            },
            Arrow {
                source: 0,
                target: 1,
            },
        ];
        let table = vec![
            Some(0),
            None,
            Some(2),
            None,
            Some(1),
            None,
            None,
            Some(2),
            None,
        ];
        let c =
            FiniteCategory::try_new(2, a, vec![0, 1], table, CategoryLimits::default()).unwrap();
        assert_eq!(c.compose(0, 2), Ok(2));
        assert_eq!(c.compose(2, 1), Ok(2));
        assert_eq!(
            c.compose(2, 2),
            Err(CategoryError::NotComposable {
                first: 2,
                second: 2
            })
        );
        assert_eq!(
            c.hom(0, 1).unwrap().map(|(i, _)| i).collect::<Vec<_>>(),
            vec![2]
        );
        let q = QuasiCategory::from_category(c);
        assert!(q.simplex(1, &[2]).is_err());
        assert!(q.simplex(0, &[usize::MAX]).is_err());
        assert!(q.simplex(2, &[]).is_err());
        let edge = q.simplex(0, &[2]).unwrap();
        assert_eq!(edge.degeneracy(0).unwrap().edges(), &[0, 2]);
        assert_eq!(edge.degeneracy(1).unwrap().edges(), &[2, 1]);
        assert_eq!(edge.face(0).unwrap().start(), 1);
        assert_eq!(edge.face(1).unwrap().start(), 0);
        assert!(edge.face(2).is_err());
        assert_eq!(
            edge.degeneracy(2).err(),
            Some(CategoryError::DegeneracyOutOfBounds {
                vertex: 2,
                dimension: 1
            })
        );
        assert_eq!(
            edge.vertex(2).err(),
            Some(CategoryError::VertexOutOfBounds {
                vertex: 2,
                dimension: 1
            })
        );
    }
    #[test]
    fn cross_object_inner_faces_compose_in_the_declared_order() {
        let arrows = vec![
            Arrow {
                source: 0,
                target: 0,
            },
            Arrow {
                source: 1,
                target: 1,
            },
            Arrow {
                source: 2,
                target: 2,
            },
            Arrow {
                source: 0,
                target: 1,
            },
            Arrow {
                source: 1,
                target: 2,
            },
            Arrow {
                source: 0,
                target: 2,
            },
        ];
        let mut table = vec![None; 36];
        for (f, a) in arrows.iter().enumerate() {
            for (g, b) in arrows.iter().enumerate() {
                if a.target == b.source {
                    table[6 * f + g] = arrows
                        .iter()
                        .position(|c| c.source == a.source && c.target == b.target);
                }
            }
        }
        let c = FiniteCategory::try_new(3, arrows, vec![0, 1, 2], table, CategoryLimits::default())
            .unwrap();
        let q = QuasiCategory::from_category(c);
        let triangle = q.simplex(0, &[3, 4]).unwrap();
        assert_eq!(triangle.face(0).unwrap().edges(), &[4]);
        assert_eq!(triangle.face(0).unwrap().start(), 1);
        assert_eq!(triangle.face(1).unwrap().edges(), &[5]);
        assert_eq!(triangle.face(2).unwrap().edges(), &[3]);
        assert_eq!(triangle.degeneracy(1).unwrap().edges(), &[3, 1, 4]);
        assert!(q.simplex(0, &[4, 3]).is_err());
    }
    fn same(a: &NerveSimplex<'_>, b: &NerveSimplex<'_>) {
        assert_eq!((a.start(), a.edges()), (b.start(), b.edges()));
    }
    #[test]
    fn simplicial_identities_match_cyclic_group_oracles() {
        for order in 1..=4 {
            let q = QuasiCategory::from_category(cyclic(order));
            for code in 0..order.pow(4) {
                let mut n = code;
                let edges: Vec<_> = (0..4)
                    .map(|_| {
                        let a = n % order;
                        n /= order;
                        a
                    })
                    .collect();
                let simplex = q.simplex(0, &edges).unwrap();
                for i in 1..4 {
                    let face = simplex.face(i).unwrap();
                    let mut expected = edges.clone();
                    expected[i - 1] = (edges[i - 1] + edges[i]) % order;
                    expected.remove(i);
                    assert_eq!(face.edges(), expected);
                }
                for i in 0..4 {
                    for j in i + 1..=4 {
                        same(
                            &simplex.face(j).unwrap().face(i).unwrap(),
                            &simplex.face(i).unwrap().face(j - 1).unwrap(),
                        );
                    }
                }
                for j in 0..=4 {
                    let repeated = simplex.degeneracy(j).unwrap();
                    same(&repeated.face(j).unwrap(), &simplex);
                    same(&repeated.face(j + 1).unwrap(), &simplex);
                    for i in 0..=4 {
                        same(
                            &simplex.degeneracy(i).unwrap().degeneracy(j + 1).unwrap(),
                            &simplex.degeneracy(j).unwrap().degeneracy(i).unwrap(),
                        );
                        if i == j {
                            break;
                        }
                    }
                }
            }
        }
    }
}
