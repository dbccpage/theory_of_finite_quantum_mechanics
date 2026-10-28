#[cfg(test)]
mod error_review {
    use super::*;
    use std::error::Error;

    #[test]
    fn defect_conversions_keep_the_original_payload() {
        let r = RingDefect::Associativity {
            labels: (1, 3, 5),
            outcome: 7,
            left: u128::MAX,
            right: 2,
        };
        let c = CategoryDefect::BlockShape {
            labels: [1, 2, 3, 4],
            rows: 5,
            cols: 6,
            expected: 7,
        };
        let b = BraidedDefect::Hexagon {
            mirror: true,
            labels: [1, 2, 3, 4, 5, 6],
        };
        let m = ModularDefect::Verlinde { a: 1, b: 2, c: 3 };
        assert_eq!(FusionError::from(r.clone()), FusionError::Ring(r.clone()));
        assert_eq!(
            FusionError::from(c.clone()),
            FusionError::Category(c.clone())
        );
        assert_eq!(
            FusionError::from(b.clone()),
            FusionError::Braided(b.clone())
        );
        assert_eq!(
            FusionError::from(m.clone()),
            FusionError::Modular(m.clone())
        );
        for (value, expected) in [
            (FusionError::from(r), "fusion ring:"),
            (FusionError::from(c), "fusion category:"),
            (FusionError::from(b), "braided fusion category:"),
            (FusionError::from(m), "modular data:"),
        ] {
            assert!(value.to_string().starts_with(expected));
            // The nested domain defects are data wrappers, not #[source] chains.
            assert!(value.source().is_none());
            assert_eq!(value.clone(), value);
        }
    }

    #[test]
    fn every_local_diagnostic_retains_its_named_fields() {
        let cases = [
            (
                FusionError::RankOutOfRange { rank: 33, max: 32 },
                "rank 33 is outside 1..=32",
            ),
            (
                FusionError::TableShape {
                    rank: 2,
                    expected: 8,
                    got: 7,
                },
                "a fusion table of rank 2 needs 8 entries, got 7",
            ),
            (
                FusionError::ListLength {
                    what: "names",
                    expected: 2,
                    got: 1,
                },
                "expected 2 names, got 1",
            ),
            (
                FusionError::Label { label: 4, rank: 3 },
                "label 4 is outside 0..3",
            ),
            (
                FusionError::Overflow { context: "testing" },
                "arithmetic overflow while testing",
            ),
            (
                FusionError::Budget {
                    what: "word",
                    requested: u128::MAX,
                    limit: 3,
                },
                "word of size 340282366920938463463374607431768211455 exceeds the budget 3",
            ),
            (
                FusionError::Shape {
                    operation: "join",
                    left: (2, 3),
                    right: (4, 5),
                },
                "join: incompatible shapes (2, 3) and (4, 5)",
            ),
            (
                FusionError::NotSquare {
                    operation: "inverse",
                    rows: 2,
                    cols: 3,
                },
                "inverse needs a square matrix, got 2x3",
            ),
            (
                FusionError::Singular { context: "solve" },
                "solve: the matrix is singular",
            ),
            (
                FusionError::NoInverse { context: "zero" },
                "zero: no multiplicative inverse",
            ),
            (
                FusionError::FieldTooSmall { needed: "zeta" },
                "the coefficient field does not contain zeta",
            ),
            (
                FusionError::NotInSubfield {
                    what: "value",
                    expected: "rational",
                },
                "value is not rational in this field",
            ),
            (FusionError::Polynomial("fraction"), "polynomial: fraction"),
            (
                FusionError::SignUndecided { context: "root" },
                "the sign of root could not be decided exactly",
            ),
            (
                FusionError::Inconsistent { context: "state" },
                "internal inconsistency: state",
            ),
        ];
        for (error, message) in cases {
            assert_eq!(error.to_string(), message);
            assert!(error.source().is_none());
            assert_eq!(error.clone(), error);
            assert!(!format!("{error:?}").is_empty());
        }
    }

    #[test]
    fn generated_provider_conversions_preserve_variant_and_text() {
        let scalar = engine_number_theory::scalar::ScalarError::ZeroInverse;
        let algebraic = engine_number_theory::algebraic_real::AlgebraicRealError::Invalid("probe");
        let matrix = MatrixError::AllocationLimitExceeded {
            requested: 17,
            limit: 9,
        };
        let exact = linear_algebra::exact_field::ExactFieldError::NotSquare {
            operation: "probe",
            rows: 2,
            cols: 3,
        };
        assert_eq!(
            FusionError::from(scalar.clone()),
            FusionError::Scalar(scalar.clone())
        );
        assert_eq!(
            FusionError::from(algebraic.clone()),
            FusionError::AlgebraicReal(algebraic.clone())
        );
        assert_eq!(
            FusionError::from(matrix.clone()),
            FusionError::Matrix(matrix.clone())
        );
        assert_eq!(
            FusionError::from(exact.clone()),
            FusionError::ExactField(exact.clone())
        );
        for (actual, message) in [
            (FusionError::from(scalar.clone()), scalar.to_string()),
            (FusionError::from(algebraic.clone()), algebraic.to_string()),
            (FusionError::from(exact.clone()), exact.to_string()),
        ] {
            assert_eq!(actual.to_string(), message);
        }
        let wrapped = FusionError::from(matrix.clone());
        assert_eq!(wrapped.to_string(), format!("matrix storage: {matrix}"));
        assert_eq!(wrapped.source().unwrap().to_string(), matrix.to_string());
    }
}
