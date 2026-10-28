#[cfg(test)]
mod category_review {
    use super::*;
    use crate::fusion_ring::FusionTable;
    use engine_number_theory::rational::{rq, Rational};

    fn tuple<const N: usize>(mut code: usize, rank: usize) -> [usize; N] {
        let mut out = [0; N];
        for i in (0..N).rev() {
            out[i] = code % rank;
            code /= rank;
        }
        out
    }
    fn expected_cost(ring: &FusionRing) -> (u128, u128, u128, u128) {
        let r = ring.rank();
        let n = r as u128;
        let width = (0..r * r)
            .map(|i| (0..r).filter(|&c| ring.n(i / r, i % r, c) > 0).count())
            .max()
            .unwrap() as u128;
        let traversal = 4 * n.pow(5) + n.pow(4) * (2 * width.pow(6) + 2 * width.pow(3));
        let (mut entries, mut inverse, mut equations) = (0, 0, 0);
        for i in 0..r.pow(4) {
            let [a, b, c, d] = tuple(i, r);
            let paths = (0..r)
                .filter(|&e| ring.n(a, b, e) > 0 && ring.n(e, c, d) > 0)
                .count() as u128;
            if paths > 0 {
                entries += 2 * (paths * paths + 2 * paths + 4);
                inverse += 4 * paths.pow(3) + 2 * paths * paths + paths;
            }
        }
        for i in 0..r.pow(5) {
            let [a, b, c, d, e] = tuple(i, r);
            let mut paths = 0u128;
            for f in 0..r {
                for g in 0..r {
                    if ring.n(a, b, f) > 0 && ring.n(f, c, g) > 0 && ring.n(g, d, e) > 0 {
                        paths += 1;
                    }
                }
            }
            equations += paths * paths;
        }
        (
            traversal,
            entries,
            equations,
            traversal
                + inverse
                + equations * (1 + 3 * width)
                + 2 * n.pow(4) * width.pow(2) * (1 + 4 * width),
        )
    }
    fn budget(error: FusionError, what: &str, requested: u128, limit: usize) {
        assert!(
            matches!(error,FusionError::Budget {what:w,requested:q,limit:l} if w==what&&q==requested&&l==limit as u128),
            "{error:?}"
        );
    }
    #[test]
    fn resource_counts_match_dense_paths_and_exact_admission_boundaries() {
        for ring in [
            FusionRing::pointed(&[], None).unwrap(),
            FusionRing::z_n(3).unwrap(),
            FusionRing::ising().unwrap(),
            FusionRing::rep_s3().unwrap(),
        ] {
            let (traversal, entries, equations, total) = expected_cost(&ring);
            let cells = entries.max(equations) as usize;
            assert!(admit_category_resources(
                &ring,
                OperationLimits {
                    max_elements: cells,
                    max_scalar_ops: total as usize
                }
            )
            .is_ok());
            budget(
                admit_category_resources(
                    &ring,
                    OperationLimits {
                        max_elements: 0,
                        max_scalar_ops: traversal as usize - 1,
                    },
                )
                .unwrap_err(),
                "fusion category label traversal",
                traversal,
                traversal as usize - 1,
            );
            budget(
                admit_category_resources(
                    &ring,
                    OperationLimits {
                        max_elements: entries as usize - 1,
                        max_scalar_ops: total as usize,
                    },
                )
                .unwrap_err(),
                "fusion category symbol storage",
                entries,
                entries as usize - 1,
            );
            budget(
                admit_category_resources(
                    &ring,
                    OperationLimits {
                        max_elements: cells,
                        max_scalar_ops: total as usize - 1,
                    },
                )
                .unwrap_err(),
                "fusion category aggregate replay work",
                total,
                total as usize - 1,
            );
            let mut calls = 0;
            assert!(FSymbols::<Rational>::from_fn_with_limits(
                &ring,
                OperationLimits {
                    max_elements: cells,
                    max_scalar_ops: total as usize - 1
                },
                |_, _, _| {
                    calls += 1;
                    rq(1, 1)
                }
            )
            .is_err());
            assert_eq!(calls, 0);
        }
        let ring = FusionRing::z_n(16).unwrap();
        budget(
            admit_category_resources(
                &ring,
                OperationLimits {
                    max_elements: 14 * 16usize.pow(3),
                    max_scalar_ops: usize::MAX,
                },
            )
            .unwrap_err(),
            "pentagon defect records",
            16u128.pow(4),
            14 * 16usize.pow(3),
        );
        assert!(charge_category("edge", 4, 4).is_ok());
        budget(charge_category("edge", 5, 4).unwrap_err(), "edge", 5, 4);
    }
    #[test]
    fn callback_support_order_and_first_failure_are_exact() {
        let ring = FusionRing::su2_level(3).unwrap();
        let r = ring.rank();
        let mut observed = Vec::new();
        let symbols = FSymbols::try_from_fn(&ring, |labels, e, f| {
            observed.push((labels, e, f));
            Ok(rq((1 + e + 2 * f) as i64, 1))
        })
        .unwrap();
        let mut expected = Vec::new();
        let mut blocks = 0;
        for code in 0..r.pow(4) {
            let labels @ [a, b, c, d] = tuple(code, r);
            let es = (0..r)
                .filter(|&e| ring.n(a, b, e) > 0 && ring.n(e, c, d) > 0)
                .collect::<Vec<_>>();
            let fs = (0..r)
                .filter(|&f| ring.n(b, c, f) > 0 && ring.n(a, f, d) > 0)
                .collect::<Vec<_>>();
            if !es.is_empty() {
                blocks += 1;
            }
            for &e in &es {
                for &f in &fs {
                    expected.push((labels, e, f));
                    assert_eq!(
                        symbols.entry(labels, e, f),
                        Some(&rq((1 + e + 2 * f) as i64, 1))
                    );
                }
            }
        }
        assert_eq!(observed, expected);
        assert_eq!(symbols.blocks().count(), blocks);
        let mut calls = 0;
        let sentinel = FusionError::Overflow {
            context: "caller coefficient",
        };
        let failed = FSymbols::<Rational>::try_from_fn(&ring, |_, _, _| {
            calls += 1;
            if calls == 7 {
                Err(sentinel.clone())
            } else {
                Ok(rq(1, 1))
            }
        });
        assert_eq!(failed.unwrap_err(), sentinel);
        assert_eq!(calls, 7);
        let table = FusionTable::new(2, vec![1, 0, 0, 1, 0, 1, 1, 2]).unwrap();
        let multiplicity = FusionRing::try_new(table).unwrap();
        let mut calls = 0;
        assert!(matches!(
            FSymbols::<Rational>::from_fn(&multiplicity, |_, _, _| {
                calls += 1;
                rq(1, 1)
            }),
            Err(FusionError::Category(CategoryDefect::NotMultiplicityFree {
                labels: [1, 1, 1],
                multiplicity: 2
            }))
        ));
        assert_eq!(calls, 0);
        assert!(matches!(
            FSymbols::<Rational>::trivial(&FusionRing::rep_s3().unwrap()),
            Err(FusionError::NotInSubfield { .. })
        ));
    }
    #[test]
    fn malformed_internal_blocks_are_typed_and_singular_states_remain_raw() {
        let ring = FusionRing::z_n(2).unwrap();
        let good = FSymbols::<Rational>::trivial(&ring).unwrap();
        let mut wrong_rank = good.clone();
        wrong_rank.rank = 3;
        assert!(matches!(
            FusionCategory::new(ring.clone(), wrong_rank),
            Err(FusionError::ListLength {
                what: "F-symbol labels",
                expected: 2,
                got: 3
            })
        ));
        let mut missing = good.clone();
        missing.blocks.remove(&[0, 0, 0, 0]);
        assert!(matches!(
            FusionCategory::new(ring.clone(), missing),
            Err(FusionError::Category(CategoryDefect::BlockMissing {
                labels: [0, 0, 0, 0]
            }))
        ));
        let mut extra = good.clone();
        extra
            .blocks
            .insert([0, 0, 0, 1], good.block([0, 0, 0, 0]).unwrap().clone());
        assert!(matches!(
            FusionCategory::new(ring.clone(), extra),
            Err(FusionError::Category(CategoryDefect::BlockUnexpected {
                labels: [0, 0, 0, 1]
            }))
        ));
        let mut labels = good.clone();
        labels.blocks.get_mut(&[0, 0, 0, 0]).unwrap().cols[0] = 1;
        assert!(matches!(
            FusionCategory::new(ring.clone(), labels),
            Err(FusionError::Category(CategoryDefect::BlockLabels {
                labels: [0, 0, 0, 0]
            }))
        ));
        let mut shape = good.clone();
        shape.blocks.get_mut(&[0, 0, 0, 0]).unwrap().matrix =
            BasicMatrix::try_from_fn(2, 2, |_, _| rq(1, 1)).unwrap();
        assert!(matches!(
            FusionCategory::new(ring.clone(), shape),
            Err(FusionError::Category(CategoryDefect::BlockShape {
                labels: [0, 0, 0, 0],
                rows: 2,
                cols: 2,
                expected: 1
            }))
        ));
        let singular = good.with_entry([1, 1, 1, 1], 0, 0, rq(0, 1)).unwrap();
        let raw = FusionCategory::new(ring.clone(), singular.clone()).unwrap();
        assert_eq!(raw.singular_blocks(), &[[1, 1, 1, 1]]);
        assert!(matches!(
            raw.validate(),
            Err(FusionError::Category(CategoryDefect::BlockSingular {
                labels: [1, 1, 1, 1]
            }))
        ));
        assert!(FusionCategory::validated(ring, singular).is_err());
    }
    fn dense_defects(
        ring: &FusionRing,
        values: &BTreeMap<[usize; 6], Rational>,
    ) -> Vec<PentagonDefect<Rational>> {
        let r = ring.rank();
        let mut out = Vec::new();
        let v = |[a, b, c, d]: [usize; 4], e: usize, f: usize| {
            values.get(&[a, b, c, d, e, f]).cloned().unwrap_or(rq(0, 1))
        };
        for code in 0..r.pow(9) {
            let labels @ [a, b, c, d, e, f, g, k, l] = tuple(code, r);
            if [
                ring.n(a, b, f),
                ring.n(f, c, g),
                ring.n(g, d, e),
                ring.n(c, d, l),
                ring.n(b, l, k),
                ring.n(a, k, e),
            ]
            .contains(&0)
            {
                continue;
            }
            let lhs = v([f, c, d, e], g, l) * v([a, b, l, e], f, k);
            let rhs = (0..r)
                .map(|h| v([a, b, c, g], f, h) * v([a, h, d, e], g, k) * v([b, c, d, k], h, l))
                .fold(rq(0, 1), |a, b| a + b);
            if lhs != rhs {
                out.push(PentagonDefect { labels, lhs, rhs });
            }
        }
        out
    }
    #[test]
    fn sparse_pentagons_match_all_nine_label_equations_and_order() {
        for ring in [
            FusionRing::z_n(2).unwrap(),
            FusionRing::z_n(3).unwrap(),
            FusionRing::ising().unwrap(),
        ] {
            let mut values = BTreeMap::new();
            let f = FSymbols::from_fn(&ring, |labels @ [a, b, c, d], e, f| {
                let x = rq(
                    (1 + a + 2 * b + 3 * c + 4 * d + 5 * e + 7 * f + if e == f { 20 } else { 0 })
                        as i64,
                    3,
                );
                values.insert(
                    [labels[0], labels[1], labels[2], labels[3], e, f],
                    x.clone(),
                );
                x
            })
            .unwrap();
            let expected = dense_defects(&ring, &values);
            assert!(!expected.is_empty());
            let category = FusionCategory::new(ring, f).unwrap();
            assert_eq!(category.pentagon_defects(), expected);
            assert_eq!(category.first_pentagon_defect(), expected.first().cloned());
        }
        let ring = FusionRing::z_n(2).unwrap();
        for value in [1, -1] {
            let f = FSymbols::from_fn(&ring, |labels, _, _| {
                rq(if labels == [1, 1, 1, 1] { value } else { 1 }, 1)
            })
            .unwrap();
            assert!(FusionCategory::validated(ring.clone(), f).is_ok());
        }
    }
    #[test]
    fn inverses_and_changed_entries_keep_channel_orientation() {
        let ring = FusionRing::su2_level(3).unwrap();
        let f = FSymbols::from_fn(&ring, |_, e, f| {
            rq((if e == f { 20 } else { 0 } + 1 + 2 * e + 3 * f) as i64, 1)
        })
        .unwrap();
        let category = FusionCategory::new(ring, f.clone()).unwrap();
        let mut nonsymmetric = false;
        for (&labels, block) in f.blocks() {
            let inv = category.f_inverse_block(labels).unwrap();
            assert_eq!(inv.rows(), block.cols());
            assert_eq!(inv.cols(), block.rows());
            let n = block.rows().len();
            assert!(n <= 2);
            for i in 0..n {
                for j in 0..n {
                    let expected = if n == 1 {
                        rq(1, 1) / block.matrix.get_ref(0, 0).unwrap().clone()
                    } else {
                        let a = block.matrix.get_ref(0, 0).unwrap().clone();
                        let b = block.matrix.get_ref(0, 1).unwrap().clone();
                        let c = block.matrix.get_ref(1, 0).unwrap().clone();
                        let d = block.matrix.get_ref(1, 1).unwrap().clone();
                        let det = a.clone() * d.clone() - b.clone() * c.clone();
                        let numerator = match (i, j) {
                            (0, 0) => d,
                            (0, 1) => -b,
                            (1, 0) => -c,
                            _ => a,
                        };
                        numerator / det
                    };
                    assert_eq!(
                        category.f_inverse_entry(labels, block.cols()[i], block.rows()[j]),
                        expected
                    );
                    if i != j
                        && inv.entry(block.cols()[i], block.rows()[j])
                            != inv.entry(block.cols()[j], block.rows()[i])
                    {
                        nonsymmetric = true;
                    }
                }
            }
            assert_eq!(block.entry(99, 99), None);
            assert_eq!(category.f_entry(labels, 99, 99), rq(0, 1));
            assert_eq!(category.f_inverse_entry(labels, 99, 99), rq(0, 1));
            let e = block.rows()[0];
            let v = block.cols()[0];
            let changed = f.with_entry(labels, e, v, rq(123, 1)).unwrap();
            assert_eq!(changed.entry(labels, e, v), Some(&rq(123, 1)));
            assert_eq!(f.entry(labels, e, v), block.entry(e, v));
        }
        assert!(nonsymmetric);
    }
    fn z2(value: i64) -> FusionCategory<Rational> {
        let ring = FusionRing::z_n(2).unwrap();
        let f = FSymbols::from_fn(&ring, |l, _, _| {
            rq(if l == [1, 1, 1, 1] { value } else { 1 }, 1)
        })
        .unwrap();
        FusionCategory::new(ring, f).unwrap()
    }
    #[test]
    fn gauge_formula_inverse_and_unit_repair_are_independent() {
        let category = z2(-1);
        assert!(matches!(
            Gauge::<Rational>::from_fn(category.ring(), |_| rq(0, 1)),
            Err(FusionError::Category(CategoryDefect::GaugeZero {
                labels: [0, 0, 0]
            }))
        ));
        assert!(matches!(
            z2(2).validate(),
            Err(FusionError::Category(CategoryDefect::Pentagon { .. }))
        ));
        let g = Gauge::from_fn(category.ring(), |[a, b, c]| {
            rq((2 + 3 * a + 5 * b + 7 * c) as i64, 3)
        })
        .unwrap();
        let changed = category.gauge_transform(&g).unwrap();
        for (&l @ [a, b, c, d], block) in category.f_symbols().blocks() {
            for &e in block.rows() {
                for &f in block.cols() {
                    let expected = g.get([a, b, e]).unwrap().clone()
                        * g.get([e, c, d]).unwrap().clone()
                        / (g.get([b, c, f]).unwrap().clone() * g.get([a, f, d]).unwrap().clone())
                        * block.entry(e, f).unwrap().clone();
                    assert_eq!(changed.f_entry(l, e, f), expected);
                }
            }
        }
        assert_eq!(
            changed.gauge_transform(&g.inverse().unwrap()).unwrap(),
            category
        );
        assert!(changed.pentagon_defects().is_empty());
        assert!(!changed.unit_defects().is_empty());
        assert!(matches!(
            changed.validate(),
            Err(FusionError::Category(CategoryDefect::UnitLaw { .. }))
        ));
        assert_eq!(changed.normalize_units().unwrap(), category);
        assert!(category.is_unitary().unwrap());
        assert!(!changed.is_unitary().unwrap());
        assert!(matches!(
            g.with([9, 9, 9], rq(0, 1)),
            Err(FusionError::Category(CategoryDefect::GaugeZero {
                labels: [9, 9, 9]
            }))
        ));
        assert!(matches!(
            g.with([9, 9, 9], rq(1, 1)),
            Err(FusionError::Category(CategoryDefect::GaugeMissing {
                labels: [9, 9, 9]
            }))
        ));
        let mut missing = Gauge::trivial(category.ring());
        missing.u.remove(&[0, 0, 0]);
        assert!(matches!(
            category.gauge_transform(&missing),
            Err(FusionError::Category(CategoryDefect::GaugeMissing {
                labels: [0, 0, 0]
            }))
        ));
    }
    #[test]
    fn dimensions_preserve_failure_order_and_do_not_imply_positivity() {
        let category = z2(-1);
        let ones = [rq(1, 1), rq(1, 1)];
        let fail = |d| FusionError::Category(CategoryDefect::Dimensions(d));
        assert_eq!(
            category.verify_dimensions(&[]),
            Err(fail(DimensionDefect::Count {
                expected: 2,
                got: 0
            }))
        );
        assert_eq!(
            category.verify_dimensions(&[rq(2, 1), rq(0, 1)]),
            Err(fail(DimensionDefect::UnitNotOne))
        );
        assert_eq!(
            category.verify_dimensions(&[rq(1, 1), rq(0, 1)]),
            Err(fail(DimensionDefect::Zero { label: 1 }))
        );
        assert_eq!(
            category.verify_dimensions(&[rq(1, 1), rq(2, 1)]),
            Err(fail(DimensionDefect::NotCharacter { a: 1, b: 1 }))
        );
        assert_eq!(
            z2(2).verify_dimensions(&ones),
            Err(fail(DimensionDefect::DisagreesWithF { label: 1 }))
        );
        assert_eq!(category.verify_dimensions(&[rq(1, 1), rq(-1, 1)]), Ok(()));
        assert_eq!(category.frobenius_schur_indicator(1, &ones), Ok(Some(-1)));
        assert_eq!(
            z2(2).frobenius_schur_indicator(1, &ones),
            Err(fail(DimensionDefect::FrobeniusSchurNotSign { label: 1 }))
        );
        let ring = FusionRing::z_n(3).unwrap();
        let category =
            FusionCategory::new(ring.clone(), FSymbols::trivial(&ring).unwrap()).unwrap();
        assert_eq!(
            category.verify_dimensions(&[rq(1, 1), rq(2, 1), rq(3, 1)]),
            Err(fail(DimensionDefect::NotSpherical { label: 1 }))
        );
        assert_eq!(category.frobenius_schur_indicator(1, &[]), Ok(None));
    }
}
