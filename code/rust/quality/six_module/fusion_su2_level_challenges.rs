#[cfg(test)]
mod su2_review {
    use super::*;
    use linear_algebra::scalars::{Ring, Semiring};
    use omega_number_theory::cyclotomic_field::Cyclotomic;
    use omega_number_theory::rational::{rq, Rational};

    fn fuses(k: usize, a: usize, b: usize, c: usize) -> bool {
        c <= k && a.abs_diff(b) <= c && c <= a + b && a + b + c <= 2 * k && (a + b + c) % 2 == 0
    }
    fn raw_q<const N: usize>(n: usize) -> Cyclotomic<N> {
        let numerator =
            Cyclotomic::<N>::zeta(4 * n as i64).sub(&Cyclotomic::<N>::zeta(-4 * n as i64));
        let denominator = Cyclotomic::<N>::zeta(4).sub(&Cyclotomic::<N>::zeta(-4));
        omega_number_theory::scalar::divide(&numerator, &denominator).unwrap()
    }
    fn raw_factorials<const N: usize>(k: usize) -> Vec<Cyclotomic<N>> {
        let mut values = vec![Cyclotomic::<N>::one()];
        for n in 1..=k + 1 {
            let next = values[n - 1].mul(&raw_q::<N>(n));
            values.push(next);
        }
        values
    }
    fn raw_delta<const N: usize>(
        a: usize,
        b: usize,
        c: usize,
        facts: &[Cyclotomic<N>],
    ) -> Cyclotomic<N> {
        let s = (a + b + c) / 2;
        let top = facts[(b + c - a) / 2]
            .mul(&facts[(a + c - b) / 2])
            .mul(&facts[(a + b - c) / 2]);
        omega_number_theory::scalar::divide(&top, &facts[s + 1]).unwrap()
    }
    fn tables<const N: usize>(k: usize) {
        assert_eq!(N, 8 * (k + 2));
        let (dimensions, facts) = coefficient_data::<Cyclotomic<N>>(k).unwrap();
        assert_eq!(dimensions.len(), k + 1);
        for n in 0..=2 * (k + 2) {
            assert_eq!(
                quantum_integer::<Cyclotomic<N>>(k, n).unwrap(),
                raw_q::<N>(n)
            );
        }
        for a in 0..=k {
            assert_eq!(dimensions[a], raw_q::<N>(a + 1));
        }
        assert_eq!(facts, raw_factorials::<N>(k));
        assert_eq!(raw_q::<N>(0), Cyclotomic::<N>::zero());
        assert_eq!(raw_q::<N>(1), Cyclotomic::<N>::one());
        assert_eq!(raw_q::<N>(k + 2), Cyclotomic::<N>::zero());
        let phases = phase_table(&Cyclotomic::<N>::zeta(1), N);
        assert_eq!(phases.len(), N);
        for (n, phase) in phases.iter().enumerate() {
            assert_eq!(*phase, Cyclotomic::<N>::zeta(n as i64));
        }
        for a in 0..=k {
            for b in 0..=k {
                for c in 0..=k {
                    if !fuses(k, a, b, c) {
                        continue;
                    }
                    let mut expected = Cyclotomic::<N>::zeta(
                        (c * (c + 2)) as i64 - (a * (a + 2)) as i64 - (b * (b + 2)) as i64,
                    );
                    if (a + b + c) / 2 % 2 != c % 2 {
                        expected = expected.neg();
                    }
                    assert_eq!(braiding_value([a, b, c], &phases), expected);
                    assert_eq!(
                        triangle_squared(a, b, c, &facts).unwrap(),
                        raw_delta(a, b, c, &facts)
                    );
                }
            }
        }
    }
    #[test]
    fn raw_root_oracles_cover_every_level_and_all_admissible_triangles() {
        tables::<24>(1);
        tables::<32>(2);
        tables::<40>(3);
        tables::<48>(4);
        tables::<56>(5);
        tables::<64>(6);
    }

    fn raw_racah<const N: usize>(
        k: usize,
        [a, b, c, d]: [usize; 4],
        e: usize,
        f: usize,
        facts: &[Cyclotomic<N>],
    ) -> Cyclotomic<N> {
        let top = [
            (a + b + e) / 2,
            (e + c + d) / 2,
            (b + c + f) / 2,
            (a + f + d) / 2,
        ];
        let bottom = [
            (a + b + c + d) / 2,
            (a + c + e + f) / 2,
            (b + d + e + f) / 2,
        ];
        let mut sum = Cyclotomic::<N>::zero();
        // Enumerate the whole level carrier, independently of production folds.
        for z in 0..=k {
            if top.iter().any(|&s| z < s) || bottom.iter().any(|&s| z > s) {
                continue;
            }
            let mut denominator = Cyclotomic::<N>::one();
            for s in top {
                denominator = denominator.mul(&facts[z - s]);
            }
            for s in bottom {
                denominator = denominator.mul(&facts[s - z]);
            }
            let term = omega_number_theory::scalar::divide(&facts[z + 1], &denominator).unwrap();
            sum = if z % 2 == 0 {
                sum.add(&term)
            } else {
                sum.sub(&term)
            };
        }
        let value = raw_q::<N>(e + 1)
            .mul(&raw_delta(a, b, e, facts))
            .mul(&raw_delta(e, c, d, facts))
            .mul(&sum);
        if ((a + b + c + d) / 2) % 2 == 0 {
            value
        } else {
            value.neg()
        }
    }
    fn block<const N: usize>(k: usize, labels: [usize; 4]) {
        let [a, b, c, d] = labels;
        let facts = raw_factorials::<N>(k);
        let dimensions = (1..=k + 1).map(raw_q::<N>).collect::<Vec<_>>();
        let left = (0..=k)
            .filter(|&e| fuses(k, a, b, e) && fuses(k, e, c, d))
            .collect::<Vec<_>>();
        let right = (0..=k)
            .filter(|&f| fuses(k, b, c, f) && fuses(k, a, f, d))
            .collect::<Vec<_>>();
        let ring = FusionRing::su2_level(k).unwrap();
        let (lm, rm) = tree_metrics(&ring, labels, &dimensions, &facts).unwrap();
        for (index, &e) in left.iter().enumerate() {
            let squared = raw_q::<N>(e + 1)
                .mul(&raw_q::<N>(d + 1))
                .mul(&raw_delta(a, b, e, &facts))
                .mul(&raw_delta(e, c, d, &facts));
            for col in 0..left.len() {
                let expected = if col == index {
                    omega_number_theory::scalar::inverse(&squared).unwrap()
                } else {
                    Cyclotomic::<N>::zero()
                };
                assert_eq!(lm.get(index, col).unwrap(), expected);
            }
            for &f in &right {
                assert_eq!(
                    associator(k, labels, e, f, &dimensions, &facts).unwrap(),
                    raw_racah(k, labels, e, f, &facts)
                );
            }
        }
        for (index, &f) in right.iter().enumerate() {
            let squared = raw_q::<N>(f + 1)
                .mul(&raw_q::<N>(d + 1))
                .mul(&raw_delta(b, c, f, &facts))
                .mul(&raw_delta(a, f, d, &facts));
            assert_eq!(
                rm.get(index, index).unwrap(),
                omega_number_theory::scalar::inverse(&squared).unwrap()
            );
        }
    }
    #[test]
    fn racah_and_tree_metrics_match_raw_formulas_and_known_gauges() {
        for a in 0..=3 {
            for b in 0..=3 {
                for c in 0..=3 {
                    for d in 0..=3 {
                        block::<40>(3, [a, b, c, d]);
                    }
                }
            }
        }
        for labels in [[2, 3, 3, 2], [3, 3, 3, 3], [1, 4, 4, 1]] {
            block::<64>(6, labels);
        }
        let (d, facts) = coefficient_data::<Cyclotomic<32>>(2).unwrap();
        let t = omega_number_theory::scalar::inverse(&raw_q::<32>(2)).unwrap();
        for (e, f, expected) in [
            (0, 0, t.neg()),
            (0, 2, t.clone()),
            (2, 0, t.clone()),
            (2, 2, t),
        ] {
            assert_eq!(
                associator(2, [1, 1, 1, 1], e, f, &d, &facts).unwrap(),
                expected
            );
        }
        let zero = racah_sum::<Rational>(1, &[2; 4], &[0; 3], &[]).unwrap();
        assert_eq!(zero, rq(0, 1));
    }
    #[test]
    fn actual_recipes_and_public_metrics_retain_the_declared_laws() {
        let semion = su2_level::<Cyclotomic<24>>(1).unwrap();
        assert_eq!(
            semion.twists(),
            &[Cyclotomic::<24>::one(), Cyclotomic::<24>::zeta(6)]
        );
        assert_eq!(
            *semion
                .category()
                .f_symbols()
                .entry([1, 1, 1, 1], 0, 0)
                .unwrap(),
            Cyclotomic::<24>::one().neg()
        );
        let fib = su2_level::<Cyclotomic<40>>(3).unwrap();
        let x = omega_number_theory::scalar::inverse(&raw_q::<40>(3)).unwrap();
        let f = fib
            .category()
            .f_symbols()
            .block([2, 2, 2, 2])
            .unwrap()
            .matrix();
        assert_eq!(
            f.as_slice(),
            &[x.clone(), Cyclotomic::<40>::one().neg(), x.neg(), x.neg()]
        );
        let (left, right) = associator_metrics::<Cyclotomic<40>>(3, [2, 2, 2, 2]).unwrap();
        require_weighted_unitarity(f, &left, &right).unwrap();
        let (boundary, _) = associator_metrics::<Cyclotomic<40>>(3, [3, 0, 0, 3]).unwrap();
        assert_eq!(boundary.shape(), (1, 1));
        let (empty_left, empty_right) =
            associator_metrics::<Cyclotomic<40>>(3, [0, 0, 0, 1]).unwrap();
        assert_eq!(empty_left.shape(), (0, 0));
        assert_eq!(empty_right.shape(), (0, 0));
    }
    #[test]
    fn level_index_label_field_and_weighted_failures_keep_their_boundaries() {
        for level in [0, 7, usize::MAX] {
            assert!(matches!(
                checked_level(level),
                Err(FusionError::Budget {
                    what: "SU(2) level (positive)",
                    ..
                })
            ));
            assert!(matches!(
                su2_level::<Rational>(level),
                Err(FusionError::Budget { .. })
            ));
        }
        checked_level(6).unwrap();
        assert!(matches!(
            quantum_integer::<Rational>(3, 11),
            Err(FusionError::Budget {
                what: "q-integer index",
                requested: 11,
                limit: 10
            })
        ));
        assert!(matches!(
            quantum_integer::<Rational>(0, usize::MAX),
            Err(FusionError::Budget {
                what: "SU(2) level (positive)",
                ..
            })
        ));
        assert!(matches!(
            associator_metrics::<Rational>(3, [0, 4, usize::MAX, 0]),
            Err(FusionError::Label { label: 4, rank: 4 })
        ));
        assert!(matches!(
            su2_level::<Rational>(1),
            Err(FusionError::FieldTooSmall { .. })
        ));
        assert!(matches!(
            quantum_integer::<Rational>(1, 1),
            Err(FusionError::FieldTooSmall { .. })
        ));
        let one = BasicMatrix::from_row_major(1, 1, vec![rq(1, 1)]).unwrap();
        let two = BasicMatrix::from_row_major(1, 1, vec![rq(2, 1)]).unwrap();
        assert_eq!(
            require_weighted_unitarity(&one, &two, &one),
            Err(FusionError::Inconsistent {
                context: "q-Racah weighted unitarity"
            })
        );
        assert!(triangle_squared(1, 1, 0, &[rq(1, 1), rq(1, 1), rq(0, 1)]).is_err());
    }
}
