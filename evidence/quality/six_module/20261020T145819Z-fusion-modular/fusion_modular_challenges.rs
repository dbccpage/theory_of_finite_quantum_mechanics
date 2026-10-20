#[cfg(test)]
mod modular_review {
    use super::*;
    use crate::catalog;
    use linear_algebra::scalars::{Ring, Semiring};
    use omega_number_theory::cyclotomic::{Cyc12, Cyc8};
    use omega_number_theory::cyclotomic_field::Cyclotomic;
    use omega_number_theory::rational::rq;
    use omega_number_theory::scalar::RationalEmbedding;

    type K = Cyc8;
    fn q(n: i64, d: i64) -> K {
        K::from_rational(&rq(n, d))
    }
    fn semion() -> ModularData<K> {
        ModularData::verified(&catalog::semion::<K>().unwrap()).unwrap()
    }
    fn raw(square: K, dimension: K) -> ModularData<K> {
        ModularData {
            ring: FusionRing::pointed(&[], None).unwrap(),
            dimensions: vec![dimension],
            twists: vec![K::one()],
            s_tilde: BasicMatrix::from_row_major(1, 1, vec![K::one()]).unwrap(),
            d_squared: square,
            p_plus: K::one(),
        }
    }

    #[test]
    fn complex_nonselfdual_data_matches_fourier_and_indicator_oracles() {
        let ribbon = catalog::cyclic_pointed::<Cyc12>(3, 1).unwrap();
        let data = ModularData::verified(&ribbon).unwrap();
        assert_eq!(data.rank(), 3);
        assert_eq!(data.dimensions(), ribbon.dimensions());
        assert_eq!(data.twists(), ribbon.twists());
        assert_eq!(data.ring(), ribbon.ring());
        assert_eq!(
            data.d_squared(),
            data.topological_entanglement_entropy_dimension_squared()
        );
        let weights = data.indicator_weights().unwrap();
        for a in 0..3 {
            for b in 0..3 {
                let mut expected = Cyc12::zero();
                for c in 0..3 {
                    if (b + c) % 3 == a {
                        let ratio =
                            omega_number_theory::scalar::divide(&data.twists[b], &data.twists[c])
                                .unwrap();
                        expected = expected.add(
                            &data.dimensions[b]
                                .mul(&data.dimensions[c])
                                .mul(&ratio.mul(&ratio)),
                        );
                    }
                }
                assert_eq!(data.indicator_row(a, b, &weights).unwrap(), expected);
            }
        }
        let c = data.charge_conjugation().unwrap();
        let t = data.t_matrix().unwrap();
        for a in 0..3 {
            for b in 0..3 {
                assert_eq!(
                    data.s_tilde().get(a, b).unwrap(),
                    Cyc12::zeta12((4 * a * b) as i32)
                );
                assert_eq!(
                    c.get(a, b).unwrap(),
                    Cyc12::from_rational(&rq(i64::from((a + b) % 3 == 0), 1))
                );
                assert_eq!(
                    t.get(a, b).unwrap(),
                    if a == b {
                        Cyc12::zeta12((4 * a * a) as i32)
                    } else {
                        Cyc12::zero()
                    }
                );
            }
        }
        for a in 0..3 {
            assert_eq!(
                data.frobenius_schur_indicator(a).unwrap(),
                if a == 0 { 1 } else { 0 }
            );
        }
        for genus in 0..=5 {
            assert_eq!(
                data.ground_state_degeneracy(genus).unwrap(),
                BigInt::from(3).pow(genus)
            );
        }
        assert_eq!(data.central_charge_mod_4().unwrap(), rq(2, 1));
        let sqrt3 = Cyc12::zeta12(1).add(&Cyc12::zeta12(-1));
        assert_eq!(data.central_charge_mod_8(&sqrt3).unwrap(), rq(2, 1));
        let unverified =
            ModularData::from_ribbon(&catalog::cyclic_pointed::<Rational>(3, 3).unwrap()).unwrap();
        assert!(matches!(
            unverified.verify(),
            Err(FusionError::Modular(ModularDefect::Degenerate {
                rank: 1,
                size: 3
            }))
        ));
    }

    #[test]
    fn every_verification_stage_has_its_ordered_first_defect() {
        let base = semion();
        let mut data = base.clone();
        data.d_squared = K::zero();
        data.s_tilde.set(0, 1, q(2, 1)).unwrap();
        assert_eq!(
            data.verify(),
            Err(FusionError::Modular(ModularDefect::ZeroGlobalDimension))
        );
        let mut data = base.clone();
        data.s_tilde.set(0, 1, q(2, 1)).unwrap();
        assert_eq!(
            data.verify(),
            Err(FusionError::Modular(ModularDefect::NotSymmetric {
                a: 0,
                b: 1
            }))
        );
        let mut data = base.clone();
        data.s_tilde = BasicMatrix::from_row_major(2, 2, vec![K::one(); 4]).unwrap();
        assert_eq!(
            data.verify(),
            Err(FusionError::Modular(ModularDefect::Degenerate {
                rank: 1,
                size: 2
            }))
        );
        let mut data = base.clone();
        data.s_tilde = matrix::identity(2).unwrap();
        assert_eq!(
            data.verify(),
            Err(FusionError::Modular(ModularDefect::SSquared { a: 0, b: 0 }))
        );
        let s = K::zeta8(1).add(&K::zeta8(-1));
        let a = s.mul(&q(5, 4));
        let b = s.mul(&q(3, 4)).mul(&K::zeta8(2));
        assert_eq!(a.mul(&a).add(&b.mul(&b)), q(2, 1));
        let mut data = base.clone();
        data.s_tilde =
            BasicMatrix::from_row_major(2, 2, vec![a.clone(), b.clone(), b, a.neg()]).unwrap();
        assert_eq!(
            data.verify(),
            Err(FusionError::Modular(ModularDefect::Unitarity {
                a: 0,
                b: 0
            }))
        );
        let mut data = base.clone();
        data.p_plus = K::zero();
        assert_eq!(
            data.verify(),
            Err(FusionError::Modular(ModularDefect::Relation { a: 0, b: 0 }))
        );
        let mut data = base.clone();
        data.ring = FusionRing::fibonacci().unwrap();
        assert_eq!(
            data.verify(),
            Err(FusionError::Modular(ModularDefect::Verlinde {
                a: 1,
                b: 1,
                c: 1
            }))
        );
        let mut changed = base.s_tilde.clone();
        changed.set(0, 1, q(7, 1)).unwrap();
        changed.set(1, 0, q(8, 1)).unwrap();
        assert_eq!(
            ModularData::<K>::first_difference(&base.s_tilde, &changed).unwrap(),
            Some((0, 1))
        );
        assert!(matches!(
            ModularData::<K>::first_difference(&base.s_tilde, &matrix::identity(1).unwrap()),
            Err(FusionError::Shape { .. })
        ));
        let st = base.st_matrix().unwrap();
        for a in 0..2 {
            for b in 0..2 {
                assert_eq!(
                    st.get(a, b).unwrap(),
                    base.s_tilde.get(a, b).unwrap().mul(&base.twists[b])
                );
            }
        }
    }

    #[test]
    fn named_charges_indicators_and_genus_sums_have_exact_expected_values() {
        let data = semion();
        let s = K::zeta8(1).add(&K::zeta8(-1));
        assert_eq!(data.central_charge_mod_4().unwrap(), rq(1, 1));
        assert_eq!(data.central_charge_mod_8(&s).unwrap(), rq(1, 1));
        assert_eq!(data.frobenius_schur_indicator(0), Ok(1));
        assert_eq!(data.frobenius_schur_indicator(1), Ok(-1));
        for g in 0..=5 {
            assert_eq!(
                data.ground_state_degeneracy(g).unwrap(),
                BigInt::from(2).pow(g)
            );
        }
        let ising = ModularData::verified(&catalog::ising::<Cyclotomic<16>>().unwrap()).unwrap();
        assert_eq!(ising.central_charge_mod_4().unwrap(), rq(1, 2));
        assert_eq!(
            ising
                .central_charge_mod_8(&Cyclotomic::<16>::one().add(&Cyclotomic::<16>::one()))
                .unwrap(),
            rq(1, 2)
        );
        for a in 0..3 {
            assert_eq!(ising.frobenius_schur_indicator(a), Ok(1));
        }
        for (g, expected) in [(0, 1), (1, 3), (2, 10), (3, 36)] {
            assert_eq!(
                ising.ground_state_degeneracy(g).unwrap(),
                BigInt::from(expected)
            );
        }
        let fib = ModularData::verified(&catalog::fibonacci::<Cyclotomic<20>>().unwrap()).unwrap();
        assert_eq!(fib.central_charge_mod_4().unwrap(), rq(14, 5));
        let d = Cyclotomic::<20>::zeta(1).add(&Cyclotomic::<20>::zeta(-1));
        assert_eq!(fib.central_charge_mod_8(&d).unwrap(), rq(14, 5));
        assert_eq!(fib.frobenius_schur_indicator(0), Ok(1));
        assert_eq!(fib.frobenius_schur_indicator(1), Ok(1));
        for (g, expected) in [(0, 1), (1, 2), (2, 5), (3, 15), (4, 50)] {
            assert_eq!(
                fib.ground_state_degeneracy(g).unwrap(),
                BigInt::from(expected)
            );
        }
        for (ribbon, charge) in [
            (catalog::toric_code::<Rational>().unwrap(), 0),
            (catalog::three_fermion::<Rational>().unwrap(), 4),
        ] {
            let model = ModularData::verified(&ribbon).unwrap();
            assert_eq!(model.central_charge_mod_4().unwrap(), rq(0, 1));
            assert_eq!(
                model.central_charge_mod_8(&rq(2, 1)).unwrap(),
                rq(charge, 1)
            );
            for a in 0..4 {
                assert_eq!(model.frobenius_schur_indicator(a), Ok(1));
            }
        }
    }

    #[test]
    fn conversion_output_and_failure_boundaries_are_typed() {
        let data = semion();
        let s = K::zeta8(1).add(&K::zeta8(-1));
        assert_eq!(
            data.central_charge_mod_8(&K::one()),
            Err(FusionError::Modular(ModularDefect::WrongGlobalDimension))
        );
        assert_eq!(
            data.central_charge_mod_8(&s.neg()),
            Err(FusionError::Modular(ModularDefect::NonPositiveDimension))
        );
        let mut complex = data.clone();
        complex.d_squared = q(-1, 1);
        assert!(matches!(
            complex.central_charge_mod_8(&K::zeta8(2)),
            Err(FusionError::SignUndecided { .. })
        ));
        let mut outside = data.clone();
        outside.p_plus = q(2, 1);
        assert!(matches!(
            outside.central_charge_mod_4(),
            Err(FusionError::NotInSubfield { .. })
        ));
        assert_eq!(
            data.frobenius_schur_indicator(2),
            Err(FusionError::Label { label: 2, rank: 2 })
        );
        assert_eq!(
            ModularData::<K>::add_multiple(q(3, 1), &q(5, 1), 2).unwrap(),
            q(13, 1)
        );
        assert!(matches!(
            ModularData::<K>::add_multiple(K::zero(), &K::one(), u64::MAX),
            Err(FusionError::Overflow { .. })
        ));
        for (v, expected) in [(K::one(), 1), (K::one().neg(), -1), (K::zero(), 0)] {
            assert_eq!(ModularData::<K>::indicator_result(0, &v), Ok(expected));
        }
        assert_eq!(
            ModularData::<K>::indicator_result(7, &q(2, 1)),
            Err(FusionError::Modular(ModularDefect::FrobeniusSchur {
                label: 7
            }))
        );
        let limit = omega_number_theory::scalar::MAX_SCALAR_EXPONENT as u32;
        assert_eq!(ModularData::<K>::genus_exponent(0).unwrap(), -1);
        assert_eq!(
            ModularData::<K>::genus_exponent(limit + 1).unwrap(),
            i64::from(limit)
        );
        assert!(matches!(
            ModularData::<K>::genus_exponent(limit + 2),
            Err(FusionError::Budget { .. })
        ));
        assert!(matches!(
            raw(K::zero(), K::zero()).ground_state_degeneracy(u32::MAX),
            Err(FusionError::Budget { .. })
        ));
        for dimension in [K::zero()] {
            assert!(matches!(
                raw(K::one(), dimension).ground_state_degeneracy(2),
                Err(FusionError::Scalar(_))
            ));
        }
        for square in [q(-1, 1), q(1, 2), s] {
            assert!(matches!(
                raw(square, K::one()).ground_state_degeneracy(2),
                Err(FusionError::NotInSubfield { .. })
            ));
        }
        let mut same = data;
        same.dimensions = vec![K::one(), K::one().neg()];
        let groups = same.dimension_ratios().unwrap();
        assert_eq!(groups.len(), 1);
        assert_eq!(groups[0], (q(2, 1), 2));
    }
}
