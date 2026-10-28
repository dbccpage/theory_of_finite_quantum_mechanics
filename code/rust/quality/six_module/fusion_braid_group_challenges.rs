#[cfg(test)]
mod braid_review {
    use super::*;
    use engine_number_theory::rational::{rq, Rational};

    fn mat(n: usize, entries: Vec<i64>) -> BasicMatrix<Rational> {
        BasicMatrix::from_row_major(n, n, entries.into_iter().map(|x| rq(x, 1)).collect()).unwrap()
    }
    fn identity(n: usize) -> Vec<i64> {
        (0..n * n).map(|i| i64::from(i / n == i % n)).collect()
    }
    fn permutations(n: usize) -> Vec<Vec<usize>> {
        fn fill(n: usize, p: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
            if p.len() == n {
                out.push(p.clone());
                return;
            }
            for x in 0..n {
                if !p.contains(&x) {
                    p.push(x);
                    fill(n, p, out);
                    p.pop();
                }
            }
        }
        let mut out = vec![];
        fill(n, &mut vec![], &mut out);
        out
    }

    #[test]
    fn independent_signed_permutation_sets_bind_exact_and_projective_closures() {
        for n in 1..=4 {
            let mut gens = vec![];
            let mut sign = identity(n);
            sign[0] = -1;
            gens.push(mat(n, sign));
            for i in 0..n - 1 {
                let mut swap = identity(n);
                swap[i * n + i] = 0;
                swap[(i + 1) * n + i + 1] = 0;
                swap[i * n + i + 1] = 1;
                swap[(i + 1) * n + i] = 1;
                gens.push(mat(n, swap));
            }
            let mut expected = HashSet::new();
            for p in permutations(n) {
                for mask in 0..1usize << n {
                    let mut a = vec![rq(0, 1); n * n];
                    for i in 0..n {
                        a[i * n + p[i]] = rq(if mask >> i & 1 == 0 { 1 } else { -1 }, 1);
                    }
                    expected.insert(a);
                }
            }
            for projective in [false, true] {
                let expected: HashSet<Vec<Rational>> = expected
                    .iter()
                    .map(|a| {
                        if !projective {
                            return a.clone();
                        }
                        let first = a.iter().find(|x| **x != rq(0, 1)).unwrap();
                        a.iter().map(|x| x / first).collect()
                    })
                    .collect();
                let bound = expected.len();
                let ClosureOutcome::Finite(g) = group_closure(&gens, bound, projective).unwrap()
                else {
                    panic!("exact bound");
                };
                assert_eq!(g.order(), bound);
                assert_eq!(g.is_projective(), projective);
                let actual: HashSet<_> =
                    g.elements().iter().map(|m| m.as_slice().to_vec()).collect();
                assert_eq!(actual, expected);
                for a in &expected {
                    assert!(g
                        .contains(&BasicMatrix::from_row_major(n, n, a.clone()).unwrap())
                        .unwrap());
                }
                assert!(
                    matches!(group_closure(&gens,bound-1,projective).unwrap(),ClosureOutcome::ExceedsBound{bound:b} if b==bound-1)
                );
                assert!(!g.contains(&mat(1, vec![0])).unwrap());
            }
        }
    }

    #[test]
    fn primitive_word_order_and_relation_witness_priority() {
        let x = mat(2, vec![0, 1, 1, 0]);
        let z = mat(2, vec![1, 0, 0, -1]);
        let id = mat(2, identity(2));
        let gens = [x.clone(), id, z.clone(), mat(2, vec![0; 4])];
        let s1 = mat(3, vec![0, 1, 0, 1, 0, 0, 0, 0, 1]);
        let s2 = mat(3, vec![1, 0, 0, 0, 0, 1, 0, 1, 0]);
        assert!(braid_relation_defects(&[s1, s2]).unwrap().is_empty());

        // Plain integer array multiplication; no provider matrix operations.
        fn mul(a: &[i64], b: &[i64]) -> Vec<i64> {
            (0..4)
                .map(|p| (0..2).map(|k| a[p / 2 * 2 + k] * b[k * 2 + p % 2]).sum())
                .collect()
        }
        let arrays = [vec![0, 1, 1, 0], identity(2), vec![1, 0, 0, -1], vec![0; 4]];
        let mut expected = vec![BraidRelationDefect::Singular { i: 3 }];
        for i in 0..4 {
            if i + 1 < 4
                && mul(&mul(&arrays[i], &arrays[i + 1]), &arrays[i])
                    != mul(&mul(&arrays[i + 1], &arrays[i]), &arrays[i + 1])
            {
                expected.push(BraidRelationDefect::Braid { i });
            }
            for j in i + 2..4 {
                if mul(&arrays[i], &arrays[j]) != mul(&arrays[j], &arrays[i]) {
                    expected.push(BraidRelationDefect::Far { i, j });
                }
            }
        }
        assert_eq!(braid_relation_defects(&gens).unwrap(), expected);
        let ClosureOutcome::Finite(group) = group_closure(&[x, z], 8, false).unwrap() else {
            panic!()
        };
        assert_eq!(group.elements()[0], mat(2, identity(2)));
        assert_eq!(group.elements()[1], gens[0]);
        assert_eq!(group.elements()[2], gens[2]);
        assert_eq!(group.elements()[3], mat(2, vec![0, -1, 1, 0]));
    }

    #[test]
    fn proportionality_has_an_oriented_factor_and_zero_is_not_a_class() {
        let a = mat(2, vec![0, 2, 4, -6]);
        let b = mat(2, vec![0, -3, -6, 9]);
        assert_eq!(equal_up_to_scalar(&a, &b).unwrap(), Some(rq(-3, 2)));
        let (normal, scale) = projective_normal_form(&a).unwrap().unwrap();
        assert_eq!(scale, rq(2, 1));
        assert_eq!(
            normalized(a.clone(), true).unwrap().as_slice(),
            &[rq(0, 1), rq(1, 1), rq(2, 1), rq(-3, 1)]
        );
        assert!(matches!(
            normalized(mat(1, vec![0]), true),
            Err(FusionError::Inconsistent { .. })
        ));
        assert_eq!(
            group_closure(
                &[mat(2, vec![0, 2, 2, 0]), mat(2, vec![3, 0, 0, -3])],
                4,
                true
            )
            .unwrap()
            .order(),
            Some(4)
        );

        assert_eq!(
            normal.as_slice(),
            &[rq(0, 1), rq(1, 1), rq(2, 1), rq(-3, 1)]
        );
        assert_eq!(
            equal_up_to_scalar(&a, &mat(2, vec![0, 3, 6, 10])).unwrap(),
            None
        );
        assert_eq!(equal_up_to_scalar(&a, &mat(1, vec![1])).unwrap(), None);
        assert_eq!(projective_normal_form(&mat(2, vec![0; 4])).unwrap(), None);
        assert_eq!(
            equal_up_to_scalar(&mat(1, vec![0]), &mat(1, vec![0])).unwrap(),
            None
        );
        let d = mat(2, vec![2, 0, 0, 1]);
        assert!(matches!(
            group_closure(&[d.clone()], 12, false).unwrap(),
            ClosureOutcome::ExceedsBound { bound: 12 }
        ));
        assert!(matches!(
            group_closure(&[d], 12, true).unwrap(),
            ClosureOutcome::ExceedsBound { bound: 12 }
        ));
    }

    #[test]
    fn exact_budget_thresholds_shapes_and_singular_priority() {
        let minus = mat(1, vec![-1]);
        let exact = OperationLimits {
            max_elements: 6,
            max_scalar_ops: 8,
        };
        assert_eq!(
            group_closure_with_limits(&[minus.clone()], 2, false, exact)
                .unwrap()
                .order(),
            Some(2)
        );
        assert!(matches!(
            group_closure_with_limits(
                &[minus],
                2,
                false,
                OperationLimits {
                    max_elements: 5,
                    ..exact
                }
            ),
            Err(FusionError::Budget {
                what: "group closure storage",
                ..
            })
        ));
        let all = OperationLimits {
            max_elements: usize::MAX,
            max_scalar_ops: usize::MAX,
        };
        assert_eq!(product(&[]).unwrap(), 1);
        assert_eq!(product(&[2, 3, 5]).unwrap(), 30);
        assert!(matches!(
            product(&[u128::MAX, 2]),
            Err(FusionError::Overflow { .. })
        ));
        assert!(charge("test", 7, 7).is_ok());
        assert!(charge("test", 8, 7).is_err());
        assert!(braid_relation_defects::<Rational>(&[]).unwrap().is_empty());
        assert_eq!(
            braid_relation_defects(&[mat(0, vec![])]).unwrap(),
            vec![BraidRelationDefect::Singular { i: 0 }]
        );
        assert!(matches!(
            group_closure::<Rational>(&[], 0, false),
            Err(FusionError::ListLength { .. })
        ));
        assert!(matches!(
            group_closure(&[mat(1, vec![0])], 0, false),
            Err(FusionError::Singular { .. })
        ));
        assert!(matches!(
            group_closure(&[mat(0, vec![])], 1, false),
            Err(FusionError::NotSquare { .. })
        ));
        let bad = BasicMatrix::from_row_major(1, 2, vec![rq(1, 1), rq(0, 1)]).unwrap();
        let zero = OperationLimits {
            max_elements: 0,
            max_scalar_ops: 0,
        };
        assert!(matches!(
            braid_relation_defects_with_limits(&[mat(1, vec![1]), bad.clone()], zero),
            Err(FusionError::Shape {
                left: (1, 1),
                right: (1, 2),
                ..
            })
        ));
        assert!(matches!(
            group_closure_with_limits(&[mat(1, vec![1]), bad], 1, false, zero),
            Err(FusionError::Shape { right: (1, 2), .. })
        ));
        let id = mat(1, vec![1]);
        // Admission 2*d^3+d^2+d=4; one multiplication adds 2, normalization adds 2.
        for (projective, work) in [(false, 6usize), (true, 8)] {
            let exact = OperationLimits {
                max_elements: 4,
                max_scalar_ops: work,
            };
            assert_eq!(
                group_closure_with_limits(&[id.clone()], 1, projective, exact)
                    .unwrap()
                    .order(),
                Some(1)
            );
            assert!(matches!(
                group_closure_with_limits(
                    &[id.clone()],
                    1,
                    projective,
                    OperationLimits {
                        max_scalar_ops: work - 1,
                        ..exact
                    }
                ),
                Err(FusionError::Budget { .. })
            ));
            assert!(matches!(
                group_closure_with_limits(
                    &[id.clone()],
                    1,
                    projective,
                    OperationLimits {
                        max_elements: 3,
                        ..exact
                    }
                ),
                Err(FusionError::Budget { .. })
            ));
        }
        assert!(matches!(
            group_closure_with_limits(&[id], 0, false, all).unwrap(),
            ClosureOutcome::ExceedsBound { bound: 0 }
        ));
    }
}
