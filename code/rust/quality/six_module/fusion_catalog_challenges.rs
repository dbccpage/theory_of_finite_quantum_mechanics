#[cfg(test)]
mod catalog_review {
    use super::*;
    use linear_algebra::scalars::{Ring, Semiring};
    use engine_number_theory::cyclotomic::{Cyc12, Cyc5, GaussianRat};
    use engine_number_theory::cyclotomic_field::Cyclotomic;
    use engine_number_theory::rational::{rq, Rational};

    fn divisor(a: usize, b: usize) -> usize {
        (1..=a.min(b))
            .filter(|d| a % d == 0 && b % d == 0)
            .max()
            .unwrap()
    }
    fn digits(mut label: usize, moduli: &[usize]) -> Vec<usize> {
        moduli
            .iter()
            .map(|m| {
                let x = label % m;
                label /= m;
                x
            })
            .collect()
    }
    fn raw_phase(
        x: &[usize],
        y: &[usize],
        moduli: &[usize],
        b: &[Vec<i64>],
        order: usize,
    ) -> usize {
        let mut total = 0i128;
        for i in 0..moduli.len() {
            for j in 0..moduli.len() {
                total += i128::from(b[i][j])
                    * x[i] as i128
                    * y[j] as i128
                    * (order / divisor(moduli[i], moduli[j])) as i128;
            }
        }
        total.rem_euclid(order as i128) as usize
    }

    #[test]
    fn reduced_phase_plans_match_raw_signed_fractions_and_minimal_orders() {
        for moduli in [
            vec![],
            vec![2],
            vec![3],
            vec![4],
            vec![5],
            vec![2, 2],
            vec![2, 3],
            vec![2, 4],
            vec![2, 2, 2],
            vec![32],
        ] {
            let size: usize = moduli.iter().product();
            let r = moduli.len();
            let raw_order = (1..=32)
                .find(|n| moduli.iter().all(|m| n % m == 0))
                .unwrap();
            for seed in [i64::MIN, -32, -1, 0, 1, 6, i64::MAX] {
                let b: Vec<Vec<i64>> = (0..r)
                    .map(|i| {
                        (0..r)
                            .map(|j| if (i + j) % 2 == 0 { seed } else { seed / 2 })
                            .collect()
                    })
                    .collect();
                let plan = PhasePlan::new(&moduli, &b);
                let mut phases = vec![];
                for x in 0..size {
                    for y in 0..size {
                        let dx = digits(x, &moduli);
                        let dy = digits(y, &moduli);
                        let expected = raw_phase(&dx, &dy, &moduli, &b, raw_order);
                        let actual = plan.exponent(&dx, &dy);
                        assert!(actual < plan.order);
                        assert_eq!(actual * (raw_order / plan.order) % raw_order, expected);
                        phases.push(expected);
                    }
                }
                let minimal = (1..=raw_order)
                    .find(|n| phases.iter().all(|p| p * n % raw_order == 0))
                    .unwrap();
                assert_eq!(plan.order, minimal);
            }
        }
    }

    #[test]
    fn supported_phase_fields_and_actual_symbol_values_are_exact() {
        let trivial = cyclic_pointed::<Rational>(3, 3).unwrap();
        assert_eq!(trivial.ring().rank(), 3);
        assert!(trivial
            .braided()
            .r_symbols()
            .entries()
            .all(|(_, x)| *x == rq(1, 1)));
        assert!(cyclic_pointed::<Rational>(3, 1).is_err());
        for k in [i64::MIN, i64::MAX] {
            let model = cyclic_pointed::<Rational>(2, k).unwrap();
            assert_eq!(
                model.twist(1).unwrap(),
                &rq(if k % 2 == 0 { 1 } else { -1 }, 1)
            );
        }
        let moduli = [2, 3];
        let b = vec![vec![i64::MIN, i64::MAX], vec![i64::MAX, i64::MIN]];
        let model = pointed_braided::<Cyc12>(&moduli, &b, None).unwrap();
        for (&[x, y, z], value) in model.braided().r_symbols().entries() {
            let dx = digits(x, &moduli);
            let dy = digits(y, &moduli);
            let expected = raw_phase(&dx, &dy, &moduli, &b, 6);
            assert_eq!(*value, Cyc12::zeta12((2 * expected) as i32));
            assert_eq!(z, (dx[0] + dy[0]) % 2 + 2 * ((dx[1] + dy[1]) % 3));
        }
        assert_eq!(
            pointed_braided::<Rational>(&[], &[], None)
                .unwrap()
                .ring()
                .rank(),
            1
        );
        assert_eq!(
            phase_roots::<Cyc12>(3).unwrap(),
            vec![Cyc12::one(), Cyc12::zeta12(4), Cyc12::zeta12(8)]
        );
    }

    #[test]
    fn named_recipes_have_the_declared_gauge_dimensions_and_twists() {
        let ising = ising::<Cyclotomic<16>>().unwrap();
        let z = Cyclotomic::<16>::zeta(1);
        let s = Cyclotomic::<16>::zeta(2).add(&Cyclotomic::<16>::zeta(-2));
        assert_eq!(
            ising.dimensions(),
            &[Cyclotomic::<16>::one(), s.clone(), Cyclotomic::<16>::one()]
        );
        assert_eq!(
            ising.twists(),
            &[Cyclotomic::<16>::one(), z, Cyclotomic::<16>::one().neg()]
        );
        let f = ising.category().f_symbols().block([1, 1, 1, 1]).unwrap();
        let two = Cyclotomic::<16>::one().add(&Cyclotomic::<16>::one());
        let inverse = s.mul(&engine_number_theory::scalar::inverse(&two).unwrap());
        assert_eq!(
            f.matrix().as_slice(),
            &[
                inverse.clone(),
                inverse.clone(),
                inverse.clone(),
                inverse.neg()
            ]
        );
        let fib = fibonacci::<Cyc5>().unwrap();
        let phi = Cyc5::zeta5(3).neg().add(&Cyc5::zeta5(-3).neg());
        assert_eq!(fib.dimensions(), &[Cyc5::one(), phi.clone()]);
        let inverse = phi.sub(&Cyc5::one());
        assert_eq!(
            fib.category()
                .f_symbols()
                .block([1, 1, 1, 1])
                .unwrap()
                .matrix()
                .as_slice(),
            &[inverse.clone(), Cyc5::one(), inverse.clone(), inverse.neg()]
        );
        assert_eq!(
            semion::<GaussianRat>().unwrap().twists(),
            &[GaussianRat::one(), GaussianRat::i()]
        );
        assert_eq!(
            toric_code::<Rational>().unwrap().twists(),
            &[rq(1, 1), rq(1, 1), rq(1, 1), rq(-1, 1)]
        );
        assert_eq!(
            three_fermion::<Rational>().unwrap().twists(),
            &[rq(1, 1), rq(-1, 1), rq(-1, 1), rq(-1, 1)]
        );
        assert_eq!(
            quantum_double_cyclic::<Rational>(2).unwrap().twists(),
            toric_code::<Rational>().unwrap().twists()
        );
    }

    #[test]
    fn domain_and_shape_errors_keep_the_actual_witness() {
        assert!(matches!(
            pointed_braided::<Rational>(&[2, 2], &[vec![0, 0]], None),
            Err(FusionError::ListLength {
                what: "rows of bicharacter exponents",
                expected: 2,
                got: 1
            })
        ));
        assert!(matches!(
            pointed_braided::<Rational>(&[2, 2], &[vec![0], vec![0, 0]], None),
            Err(FusionError::ListLength {
                what: "columns of bicharacter exponents",
                expected: 2,
                got: 1
            })
        ));
        assert!(matches!(
            pointed_braided::<Rational>(&[3], &[vec![1]], Some(vec![])),
            Err(FusionError::ListLength { .. })
        ));
        for n in [0, 1, 33, usize::MAX] {
            assert!(cyclic_pointed::<Rational>(n, 1).is_err());
        }
        for n in [0, 1, 6, usize::MAX] {
            assert!(quantum_double_cyclic::<Rational>(n).is_err());
        }
        assert!(ising::<Rational>().is_err());
        assert!(fibonacci::<Rational>().is_err());
        assert!(semion::<Rational>().is_err());
        assert_eq!(gcd(0, 3), 3);
        assert_eq!(reduced_coefficient(i64::MIN, 2, 2), (0, 1));
        assert_eq!(reduced_coefficient(2, 4, 4), (1, 2));
        assert_eq!(reduced_coefficient(-1, 4, 4), (3, 4));
    }
}
