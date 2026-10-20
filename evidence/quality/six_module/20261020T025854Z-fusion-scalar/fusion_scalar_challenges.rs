#[cfg(test)]
mod scalar_review {
    use super::*;
    use omega_number_theory::rational::rq;
    use omega_number_theory::scalar::RationalEmbedding;

    #[test]
    fn full_signed_exponents_use_the_mathematical_period() {
        // Independent generator from the provider, with i128 reference arithmetic.
        for n in [1u32, 2, 3, 4, 6, 12] {
            for k in [
                i64::MIN,
                i64::MIN + 1,
                -13,
                -1,
                0,
                1,
                13,
                i64::MAX - 1,
                i64::MAX,
            ] {
                let power = ((k as i128) * (12 / n) as i128).rem_euclid(12) as i32;
                assert_eq!(
                    Cyc12::root_of_unity(n, k),
                    Some(Cyc12::zeta12(power)),
                    "n={n}, k={k}"
                );
                assert_eq!(root_of_unity::<Cyc12>(n, k).unwrap(), Cyc12::zeta12(power));
            }
        }
        for n in [0, 5, 7, 13, u32::MAX] {
            assert!(Cyc12::root_of_unity(n, 1).is_none());
            assert!(matches!(
                root_of_unity::<Cyc12>(n, 1),
                Err(FusionError::FieldTooSmall { .. })
            ));
        }
    }

    fn adapter<K: FusionScalar>(w: u32) {
        assert_eq!(K::root_of_unity_order(), w);
        let z = K::primitive_root_of_unity();
        let mut powers = vec![K::one()];
        for _ in 1..w {
            powers.push(powers.last().unwrap().mul(&z));
        }
        assert_eq!(powers.last().unwrap().mul(&z), K::one());
        for j in 1..w {
            assert_ne!(powers[j as usize], K::one());
        }
        for q in [rq(-7, 3), rq(0, 1), rq(11, 5)] {
            let x = K::from_rational(&q);
            assert_eq!(x.to_rational(), Some(q.clone()));
            assert_eq!(sign_of(&x).unwrap(), q.cmp(&rq(0, 1)));
        }
        for n in 1..=w {
            if w % n != 0 {
                assert!(K::root_of_unity(n, 1).is_none());
                continue;
            }
            for k in [-1, 0, 1, i64::MIN, i64::MAX] {
                let index = ((k as i128) * (w / n) as i128).rem_euclid(w as i128) as usize;
                assert_eq!(K::root_of_unity(n, k), Some(powers[index].clone()));
            }
        }
        if w > 2 {
            assert!(z.to_rational().is_none());
            assert!(sign_of(&z).is_err());
        }
    }

    #[test]
    fn all_fixed_and_generic_adapters_have_the_advertised_exact_order() {
        adapter::<Rational>(2);
        adapter::<GaussianRat>(4);
        adapter::<EisensteinRat>(6);
        adapter::<Cyc5>(10);
        adapter::<Cyc8>(8);
        adapter::<Cyc12>(12);
        adapter::<Cyc24>(24);
        adapter::<Cyc28>(28);
        adapter::<Cyc44>(44);
        adapter::<Cyc52>(52);
        adapter::<Cyc120>(120);
        adapter::<Cyclotomic<1>>(2);
        adapter::<Cyclotomic<3>>(6);
        adapter::<Cyclotomic<4>>(4);
        adapter::<Cyclotomic<5>>(10);
        adapter::<Cyclotomic<8>>(8);
    }

    #[test]
    fn identification_returns_reduced_angles_and_refuses_non_roots() {
        // Independent gcd search via divisibility, over the actual fixed basis.
        for k in 0..12u32 {
            let g = (1..=12)
                .filter(|d| k % d == 0 && 12 % d == 0)
                .max()
                .unwrap();
            assert_eq!(
                root_of_unity_data(&Cyc12::zeta12(k as i32)),
                Some((12 / g, k / g))
            );
        }
        assert_eq!(root_of_unity_data(&Cyc12::zero()), None);
        assert_eq!(root_of_unity_data(&Cyc12::from_rational(&rq(2, 1))), None);
    }

    #[test]
    fn constants_signs_and_subfield_boundaries() {
        assert_eq!(Cyclotomic::<0>::root_of_unity_order(), 0);
        assert_eq!(Cyclotomic::<{ usize::MAX }>::root_of_unity_order(), 0);
        assert_eq!(constant_term(&[]), None);
        assert_eq!(constant_term(&[rq(2,3)]),Some(rq(2,3)));
        assert_eq!(constant_term(&[rq(2,3),rq(1,100),rq(0,1)]),None);
        assert_eq!(constant_term(&[rq(2, 3), rq(0, 1)]), Some(rq(2, 3)));
        assert_eq!(constant_term(&[rq(2, 3), rq(1, 100)]), None);
        assert_eq!(sign_of(&sqrt_two::<Cyc8>().unwrap()), Ok(Ordering::Greater));
        let s = sqrt_two::<Cyc8>().unwrap();
        assert_eq!(s.mul(&s), Cyc8::from_rational(&rq(2, 1)));
        let g = golden_ratio::<Cyc5>().unwrap();
        assert_eq!(g.mul(&g), g.add(&Cyc5::one()));
        assert_eq!(sign_of(&g), Ok(Ordering::Greater));
        assert!(sqrt_two::<Rational>().is_err());
        assert!(golden_ratio::<Cyc8>().is_err());
        assert_eq!(
            GaussianRat {
                re: rq(4, 1),
                im: rq(1, 1)
            }
            .to_rational(),
            None
        );
        assert_eq!(
            EisensteinRat {
                a: rq(4, 1),
                b: rq(1, 1)
            }
            .to_rational(),
            None
        );
    }
}
