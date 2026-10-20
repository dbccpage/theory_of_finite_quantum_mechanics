//! Independent exact arithmetic and adversarial admission controls.
//! AuthorityEffect: None. Finite challenges do not prove arbitrary Rust execution.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use omega_kernel::resource_limits::OperationLimits;
use tfqm_holonomy::matrix::ScalarRef;
use tfqm_holonomy::{
    CellComplex, Connection, ConnectionLaplacian, ExactMatrix, ExactScalar, GaussianRational,
    HolonomyError, Vertex,
};

fn q(n: i64) -> BigRational {
    BigRational::from_integer(n.into())
}
fn matrix(values: [i64; 4]) -> ExactMatrix<BigRational> {
    ExactMatrix::try_new(2, 2, values.into_iter().map(q).collect()).unwrap()
}

#[test]
fn exact_two_by_two_grid_matches_integer_determinants_ranks_and_adjugates() {
    for a in -1..=1 {
        for b in -1..=1 {
            for c in -1..=1 {
                for d in -1..=1 {
                    let m = matrix([a, b, c, d]);
                    let determinant = a * d - b * c;
                    let expected_rank = if determinant != 0 {
                        2
                    } else {
                        usize::from([a, b, c, d].iter().any(|&v| v != 0))
                    };
                    assert_eq!(m.trace(), Ok(q(a + d)));
                    assert_eq!(m.determinant(), Ok(q(determinant)));
                    assert_eq!(m.rank(), Ok(expected_rank));
                    if determinant == 0 {
                        assert!(matches!(
                            m.inverse(),
                            Err(HolonomyError::SingularMatrix { .. })
                        ));
                    } else {
                        let adjugate = [d, -b, -c, a]
                            .into_iter()
                            .map(|v| BigRational::new(v.into(), determinant.into()))
                            .collect();
                        let inverse = ExactMatrix::try_new(2, 2, adjugate).unwrap();
                        assert_eq!(m.inverse().unwrap(), inverse);
                        assert_eq!(
                            m.matmul(&inverse).unwrap(),
                            ExactMatrix::try_identity(2).unwrap()
                        );
                    }
                }
            }
        }
    }
}

#[test]
fn product_matches_direct_integer_dot_products_on_the_full_small_grid() {
    for code_left in 0..81 {
        for code_right in 0..81 {
            let decode = |mut code: i64| -> [i64; 4] {
                std::array::from_fn(|_| {
                    let x = code % 3 - 1;
                    code /= 3;
                    x
                })
            };
            let left = decode(code_left);
            let right = decode(code_right);
            let product = matrix(left).matmul(&matrix(right)).unwrap();
            let expected: Vec<_> = (0..2)
                .flat_map(|r| {
                    (0..2).map(move |c| q(left[r * 2] * right[c] + left[r * 2 + 1] * right[2 + c]))
                })
                .collect();
            assert_eq!(product.as_slice(), expected);
        }
    }
}

#[test]
fn raw_rationals_are_refused_and_setters_preserve_the_original_on_failure() {
    let mut m = ExactMatrix::try_identity(1).unwrap();
    let before = m.clone();
    for bad in [
        BigRational::new_raw(1.into(), 0.into()),
        BigRational::new_raw(2.into(), 2.into()),
        BigRational::new_raw(1.into(), (-1).into()),
    ] {
        assert!(matches!(
            ExactMatrix::try_new(1, 1, vec![bad.clone()]),
            Err(HolonomyError::InvalidScalar { .. })
        ));
        assert!(matches!(
            m.set(0, 0, bad.clone()),
            Err(HolonomyError::InvalidScalar { .. })
        ));
        assert!(matches!(
            bad.exact_inv(),
            Err(HolonomyError::InvalidScalar { .. })
        ));
        assert_eq!(m, before);
    }
    assert!(matches!(
        m.get(1, 0),
        Err(HolonomyError::MatrixIndexOutOfBounds { .. })
    ));
    assert!(matches!(
        m.get(0, usize::MAX),
        Err(HolonomyError::MatrixIndexOutOfBounds { .. })
    ));
    assert!(matches!(
        m.set(1, 0, q(0)),
        Err(HolonomyError::MatrixIndexOutOfBounds { .. })
    ));
    assert_eq!(m, before);
}

#[test]
fn wire_decoding_rechecks_shape_and_rejects_unknown_fields() {
    let m = matrix([1, 2, 3, 4]);
    let wire = serde_json::to_value(&m).unwrap();
    assert_eq!(
        serde_json::from_value::<ExactMatrix<BigRational>>(wire.clone()).unwrap(),
        m
    );
    for field in ["rows", "cols"] {
        let mut forged = wire.clone();
        forged[field] = 3.into();
        assert!(serde_json::from_value::<ExactMatrix<BigRational>>(forged).is_err());
    }
    let mut forged = wire.clone();
    forged["data"] = serde_json::json!([]);
    assert!(serde_json::from_value::<ExactMatrix<BigRational>>(forged).is_err());
    let mut forged = wire;
    forged["unexpected"] = true.into();
    assert!(serde_json::from_value::<ExactMatrix<BigRational>>(forged).is_err());
}

#[test]
fn exact_products_exceed_machine_integer_storage_without_wrapping() {
    let left = ExactMatrix::try_new(1, 1, vec![q(i64::MAX)]).unwrap();
    let right = ExactMatrix::try_new(1, 1, vec![q(2)]).unwrap();
    let product = left.matmul(&right).unwrap();
    assert_eq!(
        product.get(0, 0).unwrap().to_integer(),
        BigInt::from(i64::MAX) * 2
    );
}

#[test]
fn cell_and_work_budgets_are_inclusive_and_precede_arithmetic() {
    let m = matrix([1, 0, 0, 1]);
    let mut limits = OperationLimits::holonomy();
    limits.max_cells = 4;
    limits.max_operations = 16;
    assert_eq!(m.matmul_with_limits(&m, &limits).unwrap(), m);
    limits.max_operations = 15;
    assert_eq!(
        m.matmul_with_limits(&m, &limits),
        Err(HolonomyError::OperationLimitExceeded {
            requested: 16,
            limit: 15
        })
    );
    limits.max_cells = 3;
    assert_eq!(
        m.matmul_with_limits(&m, &limits),
        Err(HolonomyError::MatrixCellLimitExceeded {
            requested: 4,
            limit: 3
        })
    );
    assert!(matches!(
        ExactMatrix::<BigRational>::try_zero(usize::MAX, 2),
        Err(HolonomyError::ResourceCountOverflow)
    ));
    assert!(matches!(
        ExactMatrix::<BigRational>::try_new(101, 100, vec![]),
        Err(HolonomyError::MatrixCellLimitExceeded { .. })
    ));
}

#[test]
fn zero_area_metadata_terminates_without_enumerating_huge_dimensions() {
    let m = ExactMatrix::<BigRational>::try_zero(0, usize::MAX).unwrap();
    assert_eq!(m.rank(), Ok(0));
    let t = m.transpose().unwrap();
    assert_eq!(t.shape(), (usize::MAX, 0));
    assert_eq!(m.conjugate_transpose().unwrap(), t);
    let empty = ExactMatrix::<BigRational>::try_zero(0, 0).unwrap();
    assert_eq!(t.matmul(&empty).unwrap().shape(), (usize::MAX, 0));
    assert_eq!(empty.determinant(), Ok(q(1)));
    assert_eq!(empty.inverse().unwrap(), empty);
}

#[test]
fn gaussian_rationals_have_checked_construction_division_and_real_norms() {
    for real in -3..=3 {
        for imag in -3..=3 {
            let z = GaussianRational::new(q(real), q(imag)).unwrap();
            assert_eq!(z.norm_sq(), q(real * real + imag * imag));
            let zero = GaussianRational::<BigRational>::zero();
            assert_eq!(z.try_div(&zero), Err(HolonomyError::ZeroDivision));
            assert_eq!(z.clone() / zero, Err(HolonomyError::ZeroDivision));
            if !z.is_zero() {
                assert_eq!(z.clone() * z.exact_inv().unwrap(), GaussianRational::one());
            }
            let wire = serde_json::to_value(&z).unwrap();
            assert_eq!(
                serde_json::from_value::<GaussianRational<BigRational>>(wire).unwrap(),
                z
            );
        }
    }
    assert!(matches!(
        GaussianRational::new(BigRational::new_raw(1.into(), 0.into()), q(0)),
        Err(HolonomyError::InvalidScalar { .. })
    ));
}

#[test]
fn malformed_vertex_and_laplacian_metadata_return_typed_errors() {
    let mut complex = CellComplex::new(OperationLimits::holonomy());
    complex.vertices.push(Vertex {
        id: "v".into(),
        index: 0,
    });
    let connection = Connection::new(1, OperationLimits::holonomy());
    assert!(ConnectionLaplacian::compute(&complex, &connection, None).is_err());
    complex.vertex_map.insert("v".into(), usize::MAX);
    assert!(matches!(
        ConnectionLaplacian::compute(&complex, &connection, None),
        Err(HolonomyError::VertexRegistryMismatch { .. })
    ));
    let malformed = ConnectionLaplacian {
        matrix: matrix([1, 0, 0, 1]),
        num_vertices: 1,
        fiber_dim: 1,
        total_dim: 2,
    };
    assert!(malformed.evaluate_quadratic_form(&[q(1), q(1)]).is_err());
    assert!(malformed.kernel_dimension().is_err());
    assert!(malformed.perturbation_certificate(q(0), q(1)).is_err());
}

#[test]
fn admitted_scalar_borrows_reject_raw_values_and_preserve_exact_operations() {
    let invalid = BigRational::new_raw(1.into(), 0.into());
    assert!(matches!(
        ScalarRef::try_new(&invalid),
        Err(HolonomyError::InvalidScalar { .. })
    ));
    let (a, b) = (q(3), q(-2));
    let (a, b) = (
        ScalarRef::try_new(&a).unwrap(),
        ScalarRef::try_new(&b).unwrap(),
    );
    assert_eq!(a.add(b), q(1));
    assert_eq!(a.sub(b), q(5));
    assert_eq!(a.mul(b), q(-6));
    assert!(!a.conjugate_eq(b));
    assert!(a.conjugate_eq(a));
    assert_eq!(q(0).exact_inv(), Err(HolonomyError::ZeroDivision));
}

fn cmul(a: (i64, i64), b: (i64, i64)) -> (i64, i64) {
    (a.0 * b.0 - a.1 * b.1, a.0 * b.1 + a.1 * b.0)
}
fn gaussian(a: (i64, i64)) -> GaussianRational {
    GaussianRational::new(q(a.0), q(a.1)).unwrap()
}

#[test]
fn complex_two_by_two_grid_matches_integer_pair_determinants_and_adjugates() {
    for mut code in 0..6561 {
        let values: [(i64, i64); 4] = std::array::from_fn(|_| {
            let pair = (code % 3 - 1, (code / 3) % 3 - 1);
            code /= 9;
            pair
        });
        let [a, b, c, d] = values;
        let (ad, bc) = (cmul(a, d), cmul(b, c));
        let det = (ad.0 - bc.0, ad.1 - bc.1);
        let matrix =
            ExactMatrix::try_new(2, 2, values.into_iter().map(gaussian).collect()).unwrap();
        assert_eq!(matrix.determinant().unwrap(), gaussian(det));
        let rank = if det != (0, 0) {
            2
        } else {
            usize::from(values.iter().any(|&x| x != (0, 0)))
        };
        assert_eq!(matrix.rank().unwrap(), rank);
        if det == (0, 0) {
            assert!(matches!(
                matrix.inverse(),
                Err(HolonomyError::SingularMatrix { .. })
            ));
            continue;
        }
        let denominator = det.0 * det.0 + det.1 * det.1;
        let expected: Vec<_> = [d, (-b.0, -b.1), (-c.0, -c.1), a]
            .into_iter()
            .map(|v| {
                let numerator = cmul(v, (det.0, -det.1));
                GaussianRational::new(
                    BigRational::new(numerator.0.into(), denominator.into()),
                    BigRational::new(numerator.1.into(), denominator.into()),
                )
                .unwrap()
            })
            .collect();
        assert_eq!(matrix.inverse().unwrap().as_slice(), expected);
        assert_eq!(
            matrix.is_hermitian(),
            a.1 == 0 && d.1 == 0 && b.0 == c.0 && b.1 == -c.1
        );
        assert_eq!(matrix.is_symmetric(), b == c);
        assert_eq!(
            matrix
                .conjugate_transpose()
                .unwrap()
                .conjugate_transpose()
                .unwrap(),
            matrix
        );
    }
}

#[test]
fn rectangular_rank_matches_all_integer_minors() {
    for mut code in 0..729 {
        let entries: [i64; 6] = std::array::from_fn(|_| {
            let value = code % 3 - 1;
            code /= 3;
            value
        });
        let has_minor = (0..3).any(|i| {
            ((i + 1)..3).any(|j| entries[i] * entries[3 + j] != entries[j] * entries[3 + i])
        });
        let expected = if has_minor {
            2
        } else {
            usize::from(entries.iter().any(|&n| n != 0))
        };
        let matrix = ExactMatrix::try_new(2, 3, entries.into_iter().map(q).collect()).unwrap();
        assert_eq!(matrix.rank().unwrap(), expected);
        assert_eq!(matrix.transpose().unwrap().rank().unwrap(), expected);
        assert_eq!(matrix.transpose().unwrap().transpose().unwrap(), matrix);
    }
}

#[test]
fn input_and_elimination_workspace_budgets_are_admitted_before_work() {
    let left = ExactMatrix::try_new(1, 4, vec![q(1); 4]).unwrap();
    let right = ExactMatrix::try_new(4, 1, vec![q(1); 4]).unwrap();
    let mut limits = OperationLimits::holonomy();
    limits.max_cells = 3;
    assert!(matches!(
        left.matmul_with_limits(&right, &limits),
        Err(HolonomyError::MatrixCellLimitExceeded {
            requested: 4,
            limit: 3
        })
    ));
    let transpose = left.transpose().unwrap();
    assert!(matches!(
        transpose.matmul_with_limits(&left, &limits),
        Err(HolonomyError::MatrixCellLimitExceeded {
            requested: 4,
            limit: 3
        })
    ));
    let matrix = matrix([1, 0, 0, 1]);
    limits.max_cells = 4;
    limits.max_operations = 26;
    assert_eq!(matrix.determinant_with_limits(&limits), Ok(q(1)));
    assert_eq!(matrix.rank_with_limits(&limits), Ok(2));
    assert!(matches!(
        matrix.inverse_with_limits(&limits),
        Err(HolonomyError::MatrixCellLimitExceeded {
            requested: 8,
            limit: 4
        })
    ));
    limits.max_operations = 25;
    assert!(matches!(
        matrix.rank_with_limits(&limits),
        Err(HolonomyError::OperationLimitExceeded {
            requested: 26,
            limit: 25
        })
    ));
    limits.max_cells = 8;
    limits.max_operations = 50;
    assert_eq!(matrix.inverse_with_limits(&limits).unwrap(), matrix);
    limits.max_operations = 49;
    assert!(matches!(
        matrix.inverse_with_limits(&limits),
        Err(HolonomyError::OperationLimitExceeded {
            requested: 50,
            limit: 49
        })
    ));
    let huge = ExactMatrix::<BigRational>::try_zero(usize::MAX, 0).unwrap();
    let wide = ExactMatrix::<BigRational>::try_zero(0, usize::MAX).unwrap();
    assert_eq!(
        huge.matmul(&wide),
        Err(HolonomyError::ResourceCountOverflow)
    );
}

#[test]
fn conjugation_requires_admitted_coefficients_and_preserves_exact_coordinates() {
    for raw in [BigRational::new_raw(1.into(), 0.into()),
                BigRational::new_raw(1.into(), (-1).into()),
                BigRational::new_raw(2.into(), 2.into())] {
        assert!(ScalarRef::try_new(&raw).is_err());
    }
    let real = BigRational::new((-2).into(), 3.into());
    assert_eq!(ScalarRef::try_new(&real).unwrap().conjugate(), real);
    let complex = GaussianRational::new(q(2), q(3)).unwrap();
    let conjugate = ScalarRef::try_new(&complex).unwrap().conjugate();
    assert_eq!(conjugate.real(), &q(2));
    assert_eq!(conjugate.imag(), &q(-3));
    assert_eq!(ScalarRef::try_new(&conjugate).unwrap().conjugate(), complex);
}
