mod tests {
    use super::*;

    fn qr(n: i64, d: i64) -> Q {
        super::qr(n, d).expect("nonzero fixture denominator")
    }

    #[test]
    fn rational_constructor_refuses_zero_and_normalizes_signed_boundaries() {
        assert_eq!(
            super::qr(1, 0),
            Err(RationalConstructionError::ZeroDenominator)
        );
        assert_eq!(
            super::qr(i64::MIN, -1).unwrap(),
            Q::from_integer(-BigInt::from(i64::MIN))
        );
        assert_eq!(super::qr(2, -4).unwrap(), Q::new((-1).into(), 2.into()));
        assert_eq!(super::qr(0, i64::MIN).unwrap(), q(0));
    }

    #[test]
    fn production_gaussian_rational_arithmetic_and_identities() {
        let i = GaussianRational::from_integers(0, 1);
        let minus_one = GaussianRational::from_integers(-1, 0);
        let one = GaussianRational::from_integers(1, 0);
        let zero = GaussianRational::from_integers(0, 0);

        // i^2 = -1
        assert_eq!(i.mul(&i), minus_one);

        // (1 + i)^(-1) = (1 - i) / 2
        let one_plus_i = GaussianRational::from_integers(1, 1);
        let inv = one_plus_i.try_inv().expect("invertible");
        assert_eq!(inv.real, qr(1, 2));
        assert_eq!(inv.imag, qr(-1, 2));
        assert_eq!(one_plus_i.mul(&inv), one);

        // z * conj(z) = norm_sq(z)
        let z = GaussianRational::new(qr(3, 4), qr(-5, 6)).unwrap();
        let z_conj = z.conjugate();
        let prod = z.mul(&z_conj);
        assert_eq!(prod.imag, qr(0, 1));
        assert_eq!(prod.real, z.norm_sq());

        // zero inversion is None
        assert_eq!(zero.try_inv(), None);

        // conjugation identities
        let z1 = GaussianRational::new(qr(1, 2), qr(3, 4)).unwrap();
        let z2 = GaussianRational::new(qr(-2, 5), qr(7, 3)).unwrap();
        assert_eq!(z1.conjugate().conjugate(), z1);
        assert_eq!(z1.add(&z2).conjugate(), z1.conjugate().add(&z2.conjugate()));
        assert_eq!(z1.mul(&z2).conjugate(), z1.conjugate().mul(&z2.conjugate()));

        // 2x2 rational matrix isomorphism
        // M(a + bi) = [[a, -b], [b, a]]
        let m_mul = |a1: &Q, b1: &Q, a2: &Q, b2: &Q| -> (Q, Q) {
            let r = a1 * a2 - b1 * b2;
            let im = a1 * b2 + b1 * a2;
            (r, im)
        };
        let (mr, mim) = m_mul(&z1.real, &z1.imag, &z2.real, &z2.imag);
        let z_prod = z1.mul(&z2);
        assert_eq!(z_prod.real, mr);
        assert_eq!(z_prod.imag, mim);
    }

    #[test]
    fn production_gaussian_rational_serde() {
        let z = GaussianRational::new(qr(7, 11), qr(-13, 17)).unwrap();
        let serialized = serde_json::to_string(&z).expect("serialize");
        let deserialized: GaussianRational =
            serde_json::from_str(&serialized).expect("deserialize");
        assert_eq!(z, deserialized);
    }

    #[test]
    fn hash_rational_unreduced_fractions_match() {
        let mut h1 = blake3::Hasher::new();
        hash_rational(&mut h1, &qr(1, 2)).unwrap();
        let mut h2 = blake3::Hasher::new();
        hash_rational(&mut h2, &qr(2, 4)).unwrap();
        assert_eq!(h1.finalize().as_bytes(), h2.finalize().as_bytes());
    }

    #[test]
    fn raw_components_are_refused_before_any_field_operation() {
        let cases = [
            (
                Q::new_raw(1.into(), 0.into()),
                RationalConstructionError::ZeroDenominator,
            ),
            (
                Q::new_raw(1.into(), (-1).into()),
                RationalConstructionError::NegativeDenominator,
            ),
            (
                Q::new_raw(2.into(), 2.into()),
                RationalConstructionError::NonReduced,
            ),
            (
                Q::new_raw(0.into(), 2.into()),
                RationalConstructionError::NonReduced,
            ),
        ];
        for (bad, error) in cases {
            assert_eq!(validate_rational(&bad), Err(error));
            assert_eq!(GaussianRational::new(bad.clone(), q(0)), Err(error));
            assert_eq!(GaussianRational::new(q(0), bad), Err(error));
        }
    }

    #[test]
    fn gaussian_wire_admits_canonical_components_and_refuses_shape_extensions() {
        let good = GaussianRational::from_integers(3, -4);
        let wire = serde_json::to_value(&good).unwrap();
        assert_eq!(
            serde_json::from_value::<GaussianRational>(wire.clone()).unwrap(),
            good
        );
        let mut unknown = wire.clone();
        unknown["extra"] = true.into();
        assert!(serde_json::from_value::<GaussianRational>(unknown).is_err());
        for field in ["real", "imag"] {
            let mut missing = wire.clone();
            missing.as_object_mut().unwrap().remove(field);
            assert!(serde_json::from_value::<GaussianRational>(missing).is_err());
            let mut undefined = wire.clone();
            undefined[field] = serde_json::to_value(Q::new_raw(1.into(), 0.into())).unwrap();
            assert!(serde_json::from_value::<GaussianRational>(undefined).is_err());
        }
    }

    #[test]
    fn gaussian_grid_matches_independent_integer_pair_operations() {
        for mut code in 0..2401 {
            let [a, b, c, d]: [i64; 4] = std::array::from_fn(|_| {
                let n = code % 7 - 3;
                code /= 7;
                n
            });
            let z = GaussianRational::from_integers(a, b);
            let w = GaussianRational::from_integers(c, d);
            assert_eq!(z.norm_sq(), q(a * a + b * b));
            assert_eq!(z.add(&w), GaussianRational::from_integers(a + c, b + d));
            assert_eq!(z.sub(&w), GaussianRational::from_integers(a - c, b - d));
            assert_eq!(
                z.mul(&w),
                GaussianRational::from_integers(a * c - b * d, a * d + b * c)
            );
            check_inverse(&z, a, b);
            check_quotient(&z, &w, [a, b, c, d]);
        }
        let huge = GaussianRational::from_integers(i64::MAX, i64::MIN);
        let product = huge.mul(&GaussianRational::from_integers(2, 0));
        assert_eq!(product.real().to_integer(), BigInt::from(i64::MAX) * 2);
        assert_eq!(product.imag().to_integer(), BigInt::from(i64::MIN) * 2);
    }

    fn check_inverse(z: &GaussianRational, a: i64, b: i64) {
        if a == 0 && b == 0 {
            assert_eq!(z.try_inv(), None);
        } else {
            let inverse = z.try_inv().unwrap();
            assert_eq!(inverse.real(), &qr(a, a * a + b * b));
            assert_eq!(inverse.imag(), &qr(-b, a * a + b * b));
        }
    }

    fn check_quotient(z: &GaussianRational, w: &GaussianRational, [a, b, c, d]: [i64; 4]) {
        if c == 0 && d == 0 {
            assert_eq!(z.try_div(w), None);
        } else {
            let quotient = z.try_div(w).unwrap();
            assert_eq!(quotient.real(), &qr(a * c + b * d, c * c + d * d));
            assert_eq!(quotient.imag(), &qr(b * c - a * d, c * c + d * d));
        }
    }

    #[test]
    fn integer_hash_matches_literal_twos_complement_frames() {
        let cases: [(i64, &[u8]); 6] = [
            (-129, &[0x7f, 0xff]),
            (-128, &[0x80]),
            (-1, &[0xff]),
            (0, &[0]),
            (127, &[0x7f]),
            (128, &[0x80, 0]),
        ];
        for (n, bytes) in cases {
            let mut expected = blake3::Hasher::new();
            expected.update(&(bytes.len() as u64).to_le_bytes());
            expected.update(bytes);
            let mut actual = blake3::Hasher::new();
            hash_bigint(&mut actual, &BigInt::from(n));
            assert_eq!(actual.finalize(), expected.finalize());
        }
    }

    #[test]
    fn rational_hash_refusal_is_failure_atomic_and_finite_raw_values_normalize() {
        let mut hasher = blake3::Hasher::new();
        hasher.update(b"prefix");
        let before = hasher.finalize();
        assert_eq!(
            hash_rational(&mut hasher, &Q::new_raw(1.into(), 0.into())),
            Err(RationalConstructionError::ZeroDenominator)
        );
        assert_eq!(hasher.finalize(), before);
        let mut normalized = blake3::Hasher::new();
        hash_rational(&mut normalized, &qr(-1, 2)).unwrap();
        let mut expected = blake3::Hasher::new();
        expected.update(&1u64.to_le_bytes());
        expected.update(&[0xff]);
        expected.update(&1u64.to_le_bytes());
        expected.update(&[2]);
        assert_eq!(normalized.finalize(), expected.finalize());
        for raw in [
            Q::new_raw(2.into(), (-4).into()),
            Q::new_raw((-2).into(), 4.into()),
        ] {
            let mut hasher = blake3::Hasher::new();
            hash_rational(&mut hasher, &raw).unwrap();
            assert_eq!(hasher.finalize(), normalized.finalize());
        }
    }
}