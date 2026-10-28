#[cfg(test)]
mod tensor_review {
    use super::*;
    use engine_number_theory::rational::{rq, Rational};

    fn values(n: usize, seed: i64) -> BasicMatrix<Rational> {
        BasicMatrix::from_row_major(
            n * n,
            n * n,
            (0..n * n * n * n)
                .map(|i| rq((i as i64 * 7 + seed * 3) % 11 - 5, 3))
                .collect(),
        )
        .unwrap()
    }
    fn embed(r: &BasicMatrix<Rational>, n: usize, pair: usize) -> Vec<Rational> {
        let d = n * n * n;
        let mut out = vec![rq(0, 1); d * d];
        // Forward basis action, independently depositing each two-particle coefficient.
        for a in 0..n {
            for b in 0..n {
                for c in 0..n {
                    for x in 0..n {
                        for y in 0..n {
                            let col = (a * n + b) * n + c;
                            let (row, u, v) = match pair {
                                0 => ((x * n + y) * n + c, a * n + b, x * n + y),
                                1 => ((x * n + b) * n + y, a * n + c, x * n + y),
                                _ => ((a * n + x) * n + y, b * n + c, x * n + y),
                            };
                            out[row * d + col] = r.as_slice()[v * n * n + u].clone();
                        }
                    }
                }
            }
        }
        out
    }
    fn mul(a: &[Rational], b: &[Rational], d: usize) -> Vec<Rational> {
        (0..d * d)
            .map(|p| {
                (0..d).fold(rq(0, 1), |sum, k| {
                    sum + &a[p / d * d + k] * &b[k * d + p % d]
                })
            })
            .collect()
    }
    fn diff(left: [&[Rational]; 3], right: [&[Rational]; 3], d: usize) -> Vec<Rational> {
        let a = mul(&mul(left[0], left[1], d), left[2], d);
        let b = mul(&mul(right[0], right[1], d), right[2], d);
        a.into_iter().zip(b).map(|(x, y)| x - y).collect()
    }

    #[test]
    fn actual_embeddings_and_all_three_defect_orientations_match_coefficient_sums() {
        for n in 1..=3 {
            let ra = values(n, 1);
            let rb = values(n, 2);
            let rc = values(n, 4);
            let d = n * n * n;
            let a = embed(&ra, n, 0);
            let b = embed(&ra, n, 1);
            let c = embed(&ra, n, 2);
            for (pair, expected) in [
                (TensorPair::First, &a),
                (TensorPair::Outer, &b),
                (TensorPair::Last, &c),
            ] {
                assert_eq!(
                    tensor_embedding(&ra, n, pair, DEFAULT_BRAID_LIMITS)
                        .unwrap()
                        .as_slice(),
                    expected
                );
            }
            assert_eq!(
                braid_form_defect(&ra).unwrap().as_slice(),
                diff([&a, &c, &a], [&c, &a, &c], d)
            );
            let family = |x: &Rational| {
                Ok(if x == &rq(1, 1) {
                    ra.clone()
                } else if x == &rq(2, 1) {
                    rb.clone()
                } else {
                    rc.clone()
                })
            };
            let b13 = embed(&rb, n, 1);
            let c23 = embed(&rc, n, 2);
            assert_eq!(
                spectral_form_defect(family, &rq(1, 1), &rq(2, 1), &rq(3, 1))
                    .unwrap()
                    .as_slice(),
                diff([&a, &b13, &c23], [&c23, &b13, &a], d)
            );
            let b23 = embed(&rb, n, 2);
            let c12 = embed(&rc, n, 0);
            let b12 = embed(&rb, n, 0);
            assert_eq!(
                spectral_braid_form_defect(family, &rq(1, 1), &rq(2, 1), &rq(3, 1))
                    .unwrap()
                    .as_slice(),
                diff([&a, &b23, &c12], [&c23, &b12, &c], d)
            );
        }
    }

    #[test]
    fn flip_yang_hecke_and_six_vertex_have_independent_entry_formulas() {
        for n in 0..=4 {
            let flip = swap_matrix::<Rational>(n).unwrap();
            let r = yang_rational(n, &rq(3, 2)).unwrap();
            assert_eq!(flip.shape(), (n * n, n * n));
            assert_eq!(r.shape(), flip.shape());
            for i in 0..n {
                for j in 0..n {
                    for k in 0..n {
                        for l in 0..n {
                            let p = rq(i64::from(i == l && j == k), 1);
                            let value = &p + if i == k && j == l { rq(3, 2) } else { rq(0, 1) };
                            assert_eq!(flip.get(i * n + j, k * n + l).unwrap(), p);
                            assert_eq!(r.get(i * n + j, k * n + l).unwrap(), value);
                        }
                    }
                }
            }
        }
        for q in [rq(-2, 1), rq(1, 1), rq(2, 1), rq(3, 2)] {
            let h = hecke(&q).unwrap();
            let delta = &q - rq(1, 1) / &q;
            let expected = vec![
                q.clone(),
                rq(0, 1),
                rq(0, 1),
                rq(0, 1),
                rq(0, 1),
                rq(0, 1),
                rq(1, 1),
                rq(0, 1),
                rq(0, 1),
                rq(1, 1),
                delta.clone(),
                rq(0, 1),
                rq(0, 1),
                rq(0, 1),
                rq(0, 1),
                q.clone(),
            ];
            assert_eq!(h.as_slice(), expected);
            assert!(hecke_quadratic_defect(&h, &q)
                .unwrap()
                .as_slice()
                .iter()
                .all(|v| *v == rq(0, 1)));
            for z in [rq(-3, 1), rq(1, 1), rq(5, 2)] {
                let v = six_vertex(&q, &z).unwrap();
                let az = &q * &z - rq(1, 1) / (&q * &z);
                let b = &z - rq(1, 1) / &z;
                let expected = vec![
                    az.clone(),
                    rq(0, 1),
                    rq(0, 1),
                    rq(0, 1),
                    rq(0, 1),
                    b.clone(),
                    delta.clone(),
                    rq(0, 1),
                    rq(0, 1),
                    delta.clone(),
                    b,
                    rq(0, 1),
                    rq(0, 1),
                    rq(0, 1),
                    rq(0, 1),
                    az,
                ];
                assert_eq!(v.as_slice(), expected);
            }
        }
        let h = hecke(&rq(2, 1)).unwrap();
        assert!(hecke_quadratic_defect(&h, &rq(3, 1))
            .unwrap()
            .as_slice()
            .iter()
            .any(|v| *v != rq(0, 1)));
        for result in [
            hecke(&rq(0, 1)),
            six_vertex(&rq(0, 1), &rq(1, 1)),
            six_vertex(&rq(1, 1), &rq(0, 1)),
        ] {
            assert!(matches!(result, Err(FusionError::Scalar(_))));
        }
    }

    #[test]
    fn storage_work_cutoffs_and_callback_error_order_are_exact() {
        let two = BasicMatrix::from_row_major(
            4,
            4,
            (0..16).map(|p| rq(i64::from(p / 4 == p % 4), 1)).collect(),
        )
        .unwrap();
        let two_exact = OperationLimits {
            max_elements: 320,
            max_scalar_ops: 4480,
        };
        assert!(braid_form_defect_with_limits(&two, two_exact).is_ok());
        assert!(matches!(
            braid_form_defect_with_limits(
                &two,
                OperationLimits {
                    max_elements: 319,
                    ..two_exact
                }
            ),
            Err(FusionError::Budget {
                what: "Yang-Baxter embedding storage",
                requested: 320,
                ..
            })
        ));
        assert!(matches!(
            braid_form_defect_with_limits(
                &two,
                OperationLimits {
                    max_scalar_ops: 4479,
                    ..two_exact
                }
            ),
            Err(FusionError::Budget {
                what: "Yang-Baxter scalar work",
                requested: 4480,
                ..
            })
        ));
        let limits = OperationLimits {
            max_elements: 5,
            max_scalar_ops: 14,
        };
        let id = BasicMatrix::from_row_major(1, 1, vec![rq(1, 1)]).unwrap();
        assert!(braid_form_defect_with_limits(&id, limits).is_ok());
        assert!(matches!(
            braid_form_defect_with_limits(
                &id,
                OperationLimits {
                    max_elements: 4,
                    ..limits
                }
            ),
            Err(FusionError::Budget {
                what: "Yang-Baxter embedding storage",
                requested: 5,
                ..
            })
        ));
        assert!(matches!(
            braid_form_defect_with_limits(
                &id,
                OperationLimits {
                    max_scalar_ops: 13,
                    ..limits
                }
            ),
            Err(FusionError::Budget {
                what: "Yang-Baxter scalar work",
                requested: 14,
                ..
            })
        ));
        let calls = std::cell::RefCell::new(vec![]);
        let family = |x: &Rational| {
            calls.borrow_mut().push(x.clone());
            Ok(id.clone())
        };
        let exact = OperationLimits {
            max_elements: 9,
            max_scalar_ops: 18,
        };
        assert!(
            spectral_form_defect_with_limits(family, &rq(1, 1), &rq(2, 1), &rq(3, 1), exact)
                .is_ok()
        );
        assert_eq!(*calls.borrow(), vec![rq(1, 1), rq(2, 1), rq(3, 1)]);
        calls.borrow_mut().clear();
        assert!(spectral_form_defect_with_limits(
            family,
            &rq(1, 1),
            &rq(2, 1),
            &rq(3, 1),
            OperationLimits {
                max_elements: 8,
                ..exact
            }
        )
        .is_err());
        assert_eq!(*calls.borrow(), vec![rq(1, 1)]);
        let fail = |x: &Rational| {
            if x == &rq(2, 1) {
                Err(FusionError::Polynomial("callback"))
            } else {
                Ok(id.clone())
            }
        };
        assert_eq!(
            spectral_form_defect(fail, &rq(1, 1), &rq(2, 1), &rq(3, 1)),
            Err(FusionError::Polynomial("callback"))
        );
        let wrong = |x: &Rational| {
            Ok(if x == &rq(1, 1) {
                id.clone()
            } else {
                values(2, 1)
            })
        };
        assert!(matches!(
            spectral_braid_form_defect(wrong, &rq(1, 1), &rq(2, 1), &rq(3, 1)),
            Err(FusionError::Shape { .. })
        ));
        let rectangle = BasicMatrix::<Rational>::from_row_major(usize::MAX, 0, vec![]).unwrap();
        assert!(matches!(
            base_dimension(&rectangle),
            Err(FusionError::NotSquare { .. })
        ));
        for n in [0, 2, 3, 5, 6, 7, 8, 10] {
            let m = BasicMatrix::from_row_major(n, n, vec![rq(0, 1); n * n]).unwrap();
            assert!(base_dimension(&m).is_err());
        }
        for n in 1..=8 {
            let m =
                BasicMatrix::from_row_major(n * n, n * n, vec![rq(0, 1); n * n * n * n]).unwrap();
            assert_eq!(base_dimension(&m).unwrap(), n);
        }
        assert!(matches!(
            swap_matrix::<Rational>(usize::MAX),
            Err(FusionError::Overflow { .. })
        ));
        assert!(matches!(
            yang_rational::<Rational>(usize::MAX, &rq(1, 1)),
            Err(FusionError::Overflow { .. })
        ));
        assert!(preflight(
            usize::MAX,
            4,
            5,
            OperationLimits {
                max_elements: usize::MAX,
                max_scalar_ops: usize::MAX
            }
        )
        .is_err());
        assert!(hecke_quadratic_defect(
            &BasicMatrix::<Rational>::from_row_major(0, 0, vec![]).unwrap(),
            &rq(1, 1)
        )
        .is_err());
    }
}
