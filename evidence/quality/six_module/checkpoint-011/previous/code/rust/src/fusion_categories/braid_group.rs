use std::collections::{HashSet, VecDeque};
use std::hash::Hash;

use linear_algebra::backend::basic_matrix::{BasicMatrix, OperationLimits};

use crate::error::FusionError;
use crate::scalar::FusionScalar;
use linear_algebra::exact_field::{elimination, matrix};

pub const DEFAULT_BRAID_LIMITS: OperationLimits = OperationLimits {
    max_elements: 1 << 20,
    max_scalar_ops: 1 << 26,
};

fn charge(what: &'static str, requested: u128, limit: usize) -> Result<(), FusionError> {
    if requested > limit as u128 {
        return Err(FusionError::Budget {
            what,
            requested,
            limit: limit as u128,
        });
    }
    Ok(())
}

fn product(factors: &[u128]) -> Result<u128, FusionError> {
    factors.iter().try_fold(1u128, |p, &factor| {
        p.checked_mul(factor).ok_or(FusionError::Overflow {
            context: "braid computation resource estimate",
        })
    })
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BraidRelationDefect {
    Braid { i: usize },
    Far { i: usize, j: usize },
    Singular { i: usize },
}

pub fn braid_relation_defects<K: FusionScalar>(
    generators: &[BasicMatrix<K>],
) -> Result<Vec<BraidRelationDefect>, FusionError> {
    braid_relation_defects_with_limits(generators, DEFAULT_BRAID_LIMITS)
}

pub fn braid_relation_defects_with_limits<K: FusionScalar>(
    generators: &[BasicMatrix<K>],
    limits: OperationLimits,
) -> Result<Vec<BraidRelationDefect>, FusionError> {
    let n = generators.first().map_or(0, BasicMatrix::rows);
    let g = generators.len() as u128;
    let dimension = n as u128;
    charge(
        "braid generator storage",
        product(&[g, dimension, dimension])?,
        limits.max_elements,
    )?;
    let products = product(&[g, g.saturating_sub(1)])?
        .checked_add(4 * g.saturating_sub(1))
        .ok_or(FusionError::Overflow {
            context: "braid relation count",
        })?;
    let work = product(&[2, products, dimension, dimension, dimension])?
        .checked_add(product(&[3, g, dimension, dimension, dimension])?)
        .and_then(|work| work.checked_add(g * dimension * (dimension + 1)))
        .ok_or(FusionError::Overflow {
            context: "braid relation scalar work",
        })?;
    charge("braid relation scalar work", work, limits.max_scalar_ops)?;
    if generators.iter().any(|m| m.shape() != (n, n)) {
        return Err(FusionError::Shape {
            operation: "braid relations (one square generator shape)",
            left: (n, n),
            right: generators
                .iter()
                .find(|m| m.shape() != (n, n))
                .map_or((0, 0), BasicMatrix::shape),
        });
    }
    let mut defects = Vec::new();
    for (i, generator) in generators.iter().enumerate() {
        if n == 0 || elimination::rank_with_limits(generator, limits)? < n {
            defects.push(BraidRelationDefect::Singular { i });
        }
    }
    for i in 0..generators.len() {
        if let (Some(a), Some(b)) = (generators.get(i), generators.get(i + 1)) {
            let left = matrix::multiply_with_limits(
                &matrix::multiply_with_limits(a, b, limits)?,
                a,
                limits,
            )
            .map_err(FusionError::from)?;
            let right = matrix::multiply_with_limits(
                &matrix::multiply_with_limits(b, a, limits)?,
                b,
                limits,
            )
            .map_err(FusionError::from)?;
            if left != right {
                defects.push(BraidRelationDefect::Braid { i });
            }
        }
        for j in i + 2..generators.len() {
            if let (Some(a), Some(b)) = (generators.get(i), generators.get(j)) {
                if matrix::multiply_with_limits(a, b, limits)?
                    != matrix::multiply_with_limits(b, a, limits)?
                {
                    defects.push(BraidRelationDefect::Far { i, j });
                }
            }
        }
    }
    Ok(defects)
}

pub fn projective_normal_form<K: FusionScalar>(
    m: &BasicMatrix<K>,
) -> Result<Option<(BasicMatrix<K>, K)>, FusionError> {
    let Some(first) = m.as_slice().iter().find(|entry| !entry.is_zero()) else {
        return Ok(None);
    };
    let lambda = first.clone();
    let scale = omega_number_theory::scalar::inverse(&lambda).map_err(FusionError::from)?;
    Ok(Some((
        matrix::scale(m, &scale).map_err(FusionError::from)?,
        lambda,
    )))
}

pub fn equal_up_to_scalar<K: FusionScalar>(
    a: &BasicMatrix<K>,
    b: &BasicMatrix<K>,
) -> Result<Option<K>, FusionError> {
    if a.shape() != b.shape() {
        return Ok(None);
    }
    match (projective_normal_form(a)?, projective_normal_form(b)?) {
        (Some((na, la)), Some((nb, lb))) => {
            if na == nb {
                Ok(Some(
                    omega_number_theory::scalar::divide(&lb, &la).map_err(FusionError::from)?,
                ))
            } else {
                Ok(None)
            }
        }
        _ => Ok(None),
    }
}

#[derive(Debug, Clone)]
pub struct FiniteMatrixGroup<K> {
    elements: Vec<BasicMatrix<K>>,
    index: HashSet<Vec<K>>,
    projective: bool,
    dimension: usize,
}

impl<K: FusionScalar + Hash + Eq> FiniteMatrixGroup<K> {
    pub fn order(&self) -> usize {
        self.elements.len()
    }

    pub fn elements(&self) -> &[BasicMatrix<K>] {
        &self.elements
    }

    pub fn is_projective(&self) -> bool {
        self.projective
    }

    pub fn contains(&self, m: &BasicMatrix<K>) -> Result<bool, FusionError> {
        if m.shape() != (self.dimension, self.dimension) {
            return Ok(false);
        }
        let key = if self.projective {
            match projective_normal_form(m)? {
                Some((normal, _)) => normal,
                None => return Ok(false),
            }
        } else {
            m.clone()
        };
        Ok(self.index.contains(key.as_slice()))
    }
}

#[derive(Debug, Clone)]
pub enum ClosureOutcome<K> {
    Finite(FiniteMatrixGroup<K>),
    ExceedsBound { bound: usize },
}

impl<K> ClosureOutcome<K> {
    pub fn order(&self) -> Option<usize> {
        match self {
            Self::Finite(group) => Some(group.elements.len()),
            Self::ExceedsBound { .. } => None,
        }
    }
}

pub fn group_closure<K: FusionScalar + Hash + Eq>(
    generators: &[BasicMatrix<K>],
    bound: usize,
    projective: bool,
) -> Result<ClosureOutcome<K>, FusionError> {
    group_closure_with_limits(generators, bound, projective, DEFAULT_BRAID_LIMITS)
}

pub fn group_closure_with_limits<K: FusionScalar + Hash + Eq>(
    generators: &[BasicMatrix<K>],
    bound: usize,
    projective: bool,
    limits: OperationLimits,
) -> Result<ClosureOutcome<K>, FusionError> {
    let Some(first) = generators.first() else {
        return Err(FusionError::ListLength {
            what: "generators",
            expected: 1,
            got: 0,
        });
    };
    let n = first.rows();
    if n == 0 || generators.iter().any(|g| g.shape() != (n, n)) {
        return Err(FusionError::NotSquare {
            operation: "group closure (generators must share one square shape)",
            rows: first.rows(),
            cols: first.cols(),
        });
    }
    let d = n as u128;
    let entries = d * d;
    charge(
        "group generator storage",
        product(&[generators.len() as u128, entries])?,
        limits.max_elements,
    )?;
    let mut work = product(&[generators.len() as u128, d, 2 * entries + d + 1])?;
    charge("group admission scalar work", work, limits.max_scalar_ops)?;
    for generator in generators {
        if elimination::rank_with_limits(generator, limits)? != n {
            return Err(FusionError::Singular {
                context: "group closure generator",
            });
        }
    }
    if bound == 0 {
        return Ok(ClosureOutcome::ExceedsBound { bound });
    }
    charge("group closure storage", 3 * entries, limits.max_elements)?;
    let normalise = |m: BasicMatrix<K>| -> Result<BasicMatrix<K>, FusionError> {
        if projective {
            projective_normal_form(&m)?
                .map(|(normal, _)| normal)
                .ok_or(FusionError::Inconsistent {
                    context: "a product of invertible group generators is zero",
                })
        } else {
            Ok(m)
        }
    };
    let identity = normalise(matrix::identity_with_limits::<K>(n, limits)?)?;
    let mut elements = vec![identity.clone()];
    let mut index: HashSet<Vec<K>> = HashSet::new();
    index.insert(identity.as_slice().to_vec());
    let mut queue = VecDeque::from([identity]);
    while let Some(g) = queue.pop_front() {
        for s in generators {
            work = work
                .checked_add(2 * d * entries + if projective { entries + 1 } else { 0 })
                .ok_or(FusionError::Overflow {
                    context: "group closure scalar work",
                })?;
            charge("group closure scalar work", work, limits.max_scalar_ops)?;
            let h = normalise(matrix::multiply_with_limits(&g, s, limits)?)?;
            if !index.contains(h.as_slice()) {
                if elements.len() >= bound {
                    return Ok(ClosureOutcome::ExceedsBound { bound });
                }
                charge(
                    "group closure storage",
                    3 * (elements.len() as u128 + 1) * entries,
                    limits.max_elements,
                )?;
                index.insert(h.as_slice().to_vec());
                elements.push(h.clone());
                queue.push_back(h);
            }
        }
    }
    Ok(ClosureOutcome::Finite(FiniteMatrixGroup {
        elements,
        index,
        projective,
        dimension: n,
    }))
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_number_theory::cyclotomic::GaussianRat;
    use omega_number_theory::rational::{rq, Rational};

    fn q(n: i64) -> Rational {
        rq(n, 1)
    }

    fn mat(rows: Vec<Vec<Rational>>) -> BasicMatrix<Rational> {
        matrix::from_rows(rows).map_err(FusionError::from).unwrap()
    }

    #[test]
    fn the_symmetric_group_permutation_matrices_satisfy_the_braid_relations() {
        let s1 = mat(vec![
            vec![q(0), q(1), q(0)],
            vec![q(1), q(0), q(0)],
            vec![q(0), q(0), q(1)],
        ]);
        let s2 = mat(vec![
            vec![q(1), q(0), q(0)],
            vec![q(0), q(0), q(1)],
            vec![q(0), q(1), q(0)],
        ]);
        assert_eq!(
            braid_relation_defects(&[s1.clone(), s2.clone()]).unwrap(),
            vec![]
        );
        let scaled = matrix::scale(
            &matrix::identity::<Rational>(3)
                .map_err(FusionError::from)
                .unwrap(),
            &q(2),
        )
        .map_err(FusionError::from)
        .unwrap();
        let defects = braid_relation_defects(&[s1, scaled]).unwrap();
        assert_eq!(defects, vec![BraidRelationDefect::Braid { i: 0 }]);
    }

    #[test]
    fn far_commutation_and_invertibility_are_checked() {
        let id = matrix::identity::<Rational>(2)
            .map_err(FusionError::from)
            .unwrap();
        let x = mat(vec![vec![q(0), q(1)], vec![q(1), q(0)]]);
        let z = mat(vec![vec![q(1), q(0)], vec![q(0), q(-1)]]);
        let defects = braid_relation_defects(&[x.clone(), id.clone(), z.clone()]).unwrap();
        assert!(defects.contains(&BraidRelationDefect::Far { i: 0, j: 2 }));
        let singular = mat(vec![vec![q(1), q(0)], vec![q(0), q(0)]]);
        let defects = braid_relation_defects(&[singular]).unwrap();
        assert_eq!(defects, vec![BraidRelationDefect::Singular { i: 0 }]);
    }

    #[test]
    fn projective_normal_forms_identify_exactly_the_proportional_matrices() {
        let a = mat(vec![vec![q(0), q(2)], vec![q(4), q(6)]]);
        let b = mat(vec![vec![q(0), q(-3)], vec![q(-6), q(-9)]]);
        let c = mat(vec![vec![q(0), q(3)], vec![q(6), q(10)]]);
        assert_eq!(equal_up_to_scalar(&a, &b).unwrap(), Some(rq(-3, 2)));
        assert_eq!(equal_up_to_scalar(&a, &c).unwrap(), None);
        let zero = matrix::zeros::<Rational>(2, 2)
            .map_err(FusionError::from)
            .unwrap();
        assert_eq!(equal_up_to_scalar(&a, &zero).unwrap(), None);
        assert_eq!(equal_up_to_scalar(&zero, &zero).unwrap(), None);
        let (normal, lambda) = projective_normal_form(&a).unwrap().unwrap();
        assert_eq!(lambda, q(2));
        assert_eq!(normal.get(0, 1).unwrap(), q(1));
        assert_eq!(projective_normal_form(&zero).unwrap(), None);
    }

    #[test]
    fn closure_counts_the_klein_four_and_dihedral_groups_exactly() {
        let x = mat(vec![vec![q(0), q(1)], vec![q(1), q(0)]]);
        let z = mat(vec![vec![q(1), q(0)], vec![q(0), q(-1)]]);
        let outcome = group_closure(&[x.clone(), z.clone()], 100, false).unwrap();
        assert_eq!(outcome.order(), Some(8));
        let projective = group_closure(&[x.clone(), z.clone()], 100, true).unwrap();
        assert_eq!(projective.order(), Some(4));
        let ClosureOutcome::Finite(group) = projective else {
            panic!("finite");
        };
        assert!(group.is_projective());
        let xz = matrix::multiply(&x, &z).map_err(FusionError::from).unwrap();
        assert!(group
            .contains(
                &matrix::scale(&xz, &q(5))
                    .map_err(FusionError::from)
                    .unwrap()
            )
            .unwrap());
        let rotation = mat(vec![vec![q(1), q(1)], vec![q(-1), q(1)]]);
        assert!(!group.contains(&rotation).unwrap());
        assert!(matches!(
            group_closure(&[x, z], 3, false).unwrap(),
            ClosureOutcome::ExceedsBound { bound: 3 }
        ));
    }

    #[test]
    fn closure_of_an_infinite_group_exceeds_every_bound() {
        let d = mat(vec![vec![q(2), q(0)], vec![q(0), q(1)]]);
        let outcome = group_closure(&[d], 50, false).unwrap();
        assert!(matches!(
            outcome,
            ClosureOutcome::ExceedsBound { bound: 50 }
        ));
    }

    #[test]
    fn closure_over_the_gaussian_rationals_finds_the_phase_group() {
        let s_gate =
            matrix::diagonal(&[GaussianRat::from_ints(1, 0), GaussianRat::from_ints(0, 1)])
                .map_err(FusionError::from)
                .unwrap();
        let outcome = group_closure(&[s_gate.clone()], 100, false).unwrap();
        assert_eq!(outcome.order(), Some(4), "S has order 4");
        assert_eq!(
            group_closure(&[s_gate], 100, true).unwrap().order(),
            Some(4)
        );
        assert!(matches!(
            group_closure::<GaussianRat>(&[], 10, false),
            Err(FusionError::ListLength { .. })
        ));
    }

    #[test]
    fn closure_refuses_singular_and_empty_generators_and_binds_membership_shape() {
        let zero = matrix::zeros::<Rational>(1, 1).unwrap();
        for projective in [false, true] {
            assert!(matches!(
                group_closure(&[zero.clone()], 10, projective),
                Err(FusionError::Singular { .. })
            ));
            let empty = matrix::identity::<Rational>(0).unwrap();
            assert!(matches!(
                group_closure(&[empty], 10, projective),
                Err(FusionError::NotSquare { .. })
            ));
            let identity = matrix::identity::<Rational>(2).unwrap();
            let ClosureOutcome::Finite(group) =
                group_closure(&[identity.clone()], 10, projective).unwrap()
            else {
                panic!("the identity generates a finite group");
            };
            let wrong_shape =
                BasicMatrix::from_row_major(1, 4, identity.as_slice().to_vec()).unwrap();
            assert!(!group.contains(&wrong_shape).unwrap());
            assert!(group.contains(&identity).unwrap());
            assert!(matches!(
                group_closure(&[identity], 0, projective).unwrap(),
                ClosureOutcome::ExceedsBound { bound: 0 }
            ));
        }
    }

    #[test]
    fn closure_and_relation_replay_enforce_aggregate_resource_limits() {
        let x = mat(vec![vec![q(0), q(1)], vec![q(1), q(0)]]);
        let limits = OperationLimits {
            max_elements: 12,
            max_scalar_ops: 1 << 20,
        };
        assert!(matches!(
            group_closure_with_limits(&[x.clone()], 10, false, limits),
            Err(FusionError::Budget {
                what: "group closure storage",
                ..
            })
        ));
        let limits = OperationLimits {
            max_elements: 1 << 20,
            max_scalar_ops: 1,
        };
        assert!(matches!(
            braid_relation_defects_with_limits(&[x], limits),
            Err(FusionError::Budget { .. })
        ));
        let identity = matrix::identity::<Rational>(1).unwrap();
        assert_eq!(
            group_closure(&[identity], usize::MAX, false)
                .unwrap()
                .order(),
            Some(1)
        );
    }
}
