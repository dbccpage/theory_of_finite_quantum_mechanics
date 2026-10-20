use linear_algebra::backend::basic_matrix::{BasicMatrix, OperationLimits};
use linear_algebra::exact_field::matrix;

use crate::braid_group::DEFAULT_BRAID_LIMITS;
use crate::error::FusionError;
use crate::scalar::FusionScalar;

fn charge(what: &'static str, requested: u128, limit: usize) -> Result<(), FusionError> {
    if requested > limit as u128 {
        return Err(FusionError::Budget {
            what,
            requested,
            limit: limit as u128,
        });
    }
    Ok(())
}

fn preflight(
    n: usize,
    products: usize,
    storage: usize,
    limits: OperationLimits,
) -> Result<(), FusionError> {
    let dimension = n.checked_pow(3).ok_or(FusionError::Overflow {
        context: "sizing a three-fold Yang-Baxter carrier",
    })?;
    let entries = dimension
        .checked_mul(dimension)
        .ok_or(FusionError::Overflow {
            context: "sizing Yang-Baxter embeddings",
        })? as u128;
    charge(
        "Yang-Baxter embedding storage",
        storage as u128 * entries,
        limits.max_elements,
    )?;
    let work = 2 * products as u128 * dimension as u128 * entries + (storage as u128 + 1) * entries;
    charge("Yang-Baxter scalar work", work, limits.max_scalar_ops)
}

pub fn base_dimension<K: FusionScalar>(r: &BasicMatrix<K>) -> Result<usize, FusionError> {
    if r.rows() != r.cols() {
        return Err(FusionError::NotSquare {
            operation: "Yang-Baxter",
            rows: r.rows(),
            cols: r.cols(),
        });
    }
    let size = r.rows() as u128;
    let (mut low, mut high) = (0u128, size + 1);
    while low < high {
        let mid = low + (high - low) / 2;
        if mid * mid < size {
            low = mid + 1;
        } else {
            high = mid;
        }
    }
    if low == 0 || low * low != size {
        return Err(FusionError::NotSquare {
            operation: "Yang-Baxter (dimension must be a square n^2)",
            rows: r.rows(),
            cols: r.cols(),
        });
    }
    usize::try_from(low).map_err(|_| FusionError::Overflow {
        context: "the Yang-Baxter base dimension",
    })
}

pub fn swap_matrix<K: FusionScalar>(n: usize) -> Result<BasicMatrix<K>, FusionError> {
    swap_matrix_with_limits(n, DEFAULT_BRAID_LIMITS)
}

pub fn swap_matrix_with_limits<K: FusionScalar>(
    n: usize,
    limits: OperationLimits,
) -> Result<BasicMatrix<K>, FusionError> {
    let dimension = n.checked_mul(n).ok_or(FusionError::Overflow {
        context: "sizing the flip matrix",
    })?;
    matrix::from_fn_with_limits(dimension, dimension, limits, |row, column| {
        let (i, j) = (row / n.max(1), row % n.max(1));
        let (k, l) = (column / n.max(1), column % n.max(1));
        if i == l && j == k {
            K::one()
        } else {
            K::zero()
        }
    })
    .map_err(FusionError::from)
}

fn check_family_shape<K: FusionScalar>(r: &BasicMatrix<K>, n: usize) -> Result<(), FusionError> {
    if base_dimension(r)? != n {
        return Err(FusionError::Shape {
            operation: "one Yang-Baxter spectral carrier",
            left: (n * n, n * n),
            right: r.shape(),
        });
    }
    Ok(())
}

fn embeddings<K: FusionScalar>(
    r: &BasicMatrix<K>,
    n: usize,
    limits: OperationLimits,
) -> Result<[BasicMatrix<K>; 3], FusionError> {
    check_family_shape(r, n)?;
    let identity = matrix::identity_with_limits::<K>(n, limits)?;
    let r12 = matrix::kronecker_with_limits(r, &identity, limits)?;
    let r23 = matrix::kronecker_with_limits(&identity, r, limits)?;
    let p23 = matrix::kronecker_with_limits(
        &identity,
        &swap_matrix_with_limits::<K>(n, limits)?,
        limits,
    )?;
    let r13 = matrix::multiply_with_limits(
        &matrix::multiply_with_limits(&p23, &r12, limits)?,
        &p23,
        limits,
    )?;
    Ok([r12, r13, r23])
}

pub fn braid_form_defect<K: FusionScalar>(
    r: &BasicMatrix<K>,
) -> Result<BasicMatrix<K>, FusionError> {
    braid_form_defect_with_limits(r, DEFAULT_BRAID_LIMITS)
}

pub fn braid_form_defect_with_limits<K: FusionScalar>(
    r: &BasicMatrix<K>,
    limits: OperationLimits,
) -> Result<BasicMatrix<K>, FusionError> {
    let n = base_dimension(r)?;
    preflight(n, 6, 8, limits)?;
    let [r12, _, r23] = embeddings(r, n, limits)?;
    let left = matrix::multiply_with_limits(
        &matrix::multiply_with_limits(&r12, &r23, limits)?,
        &r12,
        limits,
    )?;
    let right = matrix::multiply_with_limits(
        &matrix::multiply_with_limits(&r23, &r12, limits)?,
        &r23,
        limits,
    )?;
    matrix::sub(&left, &right).map_err(FusionError::from)
}

pub fn spectral_form_defect<K: FusionScalar>(
    family: impl Fn(&K) -> Result<BasicMatrix<K>, FusionError>,
    a: &K,
    b: &K,
    c: &K,
) -> Result<BasicMatrix<K>, FusionError> {
    spectral_form_defect_with_limits(family, a, b, c, DEFAULT_BRAID_LIMITS)
}

pub fn spectral_form_defect_with_limits<K: FusionScalar>(
    family: impl Fn(&K) -> Result<BasicMatrix<K>, FusionError>,
    a: &K,
    b: &K,
    c: &K,
    limits: OperationLimits,
) -> Result<BasicMatrix<K>, FusionError> {
    let ra = family(a)?;
    let n = base_dimension(&ra)?;
    preflight(n, 10, 12, limits)?;
    let rb = family(b)?;
    let rc = family(c)?;
    check_family_shape(&rb, n)?;
    check_family_shape(&rc, n)?;
    let [r12, _, _] = embeddings(&ra, n, limits)?;
    let [_, r13, _] = embeddings(&rb, n, limits)?;
    let [_, _, r23] = embeddings(&rc, n, limits)?;
    let left = matrix::multiply_with_limits(
        &matrix::multiply_with_limits(&r12, &r13, limits)?,
        &r23,
        limits,
    )?;
    let right = matrix::multiply_with_limits(
        &matrix::multiply_with_limits(&r23, &r13, limits)?,
        &r12,
        limits,
    )?;
    matrix::sub(&left, &right).map_err(FusionError::from)
}

pub fn spectral_braid_form_defect<K: FusionScalar>(
    family: impl Fn(&K) -> Result<BasicMatrix<K>, FusionError>,
    x: &K,
    y: &K,
    z: &K,
) -> Result<BasicMatrix<K>, FusionError> {
    spectral_braid_form_defect_with_limits(family, x, y, z, DEFAULT_BRAID_LIMITS)
}

pub fn spectral_braid_form_defect_with_limits<K: FusionScalar>(
    family: impl Fn(&K) -> Result<BasicMatrix<K>, FusionError>,
    x: &K,
    y: &K,
    z: &K,
    limits: OperationLimits,
) -> Result<BasicMatrix<K>, FusionError> {
    let rx = family(x)?;
    let n = base_dimension(&rx)?;
    preflight(n, 4, 10, limits)?;
    let ry = family(y)?;
    let rz = family(z)?;
    check_family_shape(&ry, n)?;
    check_family_shape(&rz, n)?;
    let identity = matrix::identity_with_limits::<K>(n, limits)?;
    let at_12 = |m: &BasicMatrix<K>| {
        matrix::kronecker_with_limits(m, &identity, limits).map_err(FusionError::from)
    };
    let at_23 = |m: &BasicMatrix<K>| {
        matrix::kronecker_with_limits(&identity, m, limits).map_err(FusionError::from)
    };
    let left = matrix::multiply_with_limits(
        &matrix::multiply_with_limits(&at_12(&rx)?, &at_23(&ry)?, limits)?,
        &at_12(&rz)?,
        limits,
    )?;
    let right = matrix::multiply_with_limits(
        &matrix::multiply_with_limits(&at_23(&rz)?, &at_12(&ry)?, limits)?,
        &at_23(&rx)?,
        limits,
    )?;
    matrix::sub(&left, &right).map_err(FusionError::from)
}

pub fn yang_rational<K: FusionScalar>(n: usize, u: &K) -> Result<BasicMatrix<K>, FusionError> {
    let dimension = n.checked_mul(n).ok_or(FusionError::Overflow {
        context: "sizing Yang's R-matrix",
    })?;
    matrix::add(
        &matrix::scale(
            &matrix::identity_with_limits::<K>(dimension, DEFAULT_BRAID_LIMITS)?,
            u,
        )?,
        &swap_matrix::<K>(n)?,
    )
    .map_err(FusionError::from)
}

pub fn hecke<K: FusionScalar>(q: &K) -> Result<BasicMatrix<K>, FusionError> {
    let q_inverse = omega_number_theory::scalar::inverse(q).map_err(FusionError::from)?;
    let zero = K::zero();
    let one = K::one();
    matrix::from_rows(vec![
        vec![q.clone(), zero.clone(), zero.clone(), zero.clone()],
        vec![zero.clone(), zero.clone(), one.clone(), zero.clone()],
        vec![zero.clone(), one, q.sub(&q_inverse), zero.clone()],
        vec![zero.clone(), zero.clone(), zero, q.clone()],
    ])
    .map_err(FusionError::from)
}

pub fn hecke_quadratic_defect<K: FusionScalar>(
    r: &BasicMatrix<K>,
    q: &K,
) -> Result<BasicMatrix<K>, FusionError> {
    if r.rows() != r.cols() || r.rows() == 0 {
        return Err(FusionError::NotSquare {
            operation: "Hecke relation",
            rows: r.rows(),
            cols: r.cols(),
        });
    }
    let n = r.rows() as u128;
    charge(
        "Hecke relation storage",
        4 * n * n,
        DEFAULT_BRAID_LIMITS.max_elements,
    )?;
    charge(
        "Hecke relation scalar work",
        2 * n * n * n + 4 * n * n,
        DEFAULT_BRAID_LIMITS.max_scalar_ops,
    )?;
    let q_inverse = omega_number_theory::scalar::inverse(q).map_err(FusionError::from)?;
    let identity = matrix::identity_with_limits::<K>(r.rows(), DEFAULT_BRAID_LIMITS)?;
    let left = matrix::sub(r, &matrix::scale(&identity, q)?)?;
    let right = matrix::add(r, &matrix::scale(&identity, &q_inverse)?)?;
    matrix::multiply_with_limits(&left, &right, DEFAULT_BRAID_LIMITS).map_err(FusionError::from)
}

pub fn six_vertex<K: FusionScalar>(q: &K, z: &K) -> Result<BasicMatrix<K>, FusionError> {
    let qz = q.mul(z);
    let a = qz.sub(&omega_number_theory::scalar::inverse(&qz).map_err(FusionError::from)?);
    let b = z.sub(&omega_number_theory::scalar::inverse(z).map_err(FusionError::from)?);
    let c = q.sub(&omega_number_theory::scalar::inverse(q).map_err(FusionError::from)?);
    let zero = K::zero();
    matrix::from_rows(vec![
        vec![a.clone(), zero.clone(), zero.clone(), zero.clone()],
        vec![zero.clone(), b.clone(), c.clone(), zero.clone()],
        vec![zero.clone(), c, b, zero.clone()],
        vec![zero.clone(), zero.clone(), zero, a],
    ])
    .map_err(FusionError::from)
}

#[cfg(test)]
mod tests {
    use super::*;
    use linear_algebra::exact_field::elimination;
    use omega_number_theory::rational::{rq, Rational};

    fn q(n: i64, d: i64) -> Rational {
        rq(n, d)
    }

    #[test]
    fn oversized_yang_baxter_embeddings_refuse_before_dense_products() {
        let r = matrix::identity::<Rational>(256).unwrap();
        assert_eq!(base_dimension(&r).unwrap(), 16);
        assert!(matches!(
            braid_form_defect(&r),
            Err(FusionError::Budget { .. })
        ));
        assert!(matches!(
            swap_matrix::<Rational>(usize::MAX),
            Err(FusionError::Overflow { .. })
        ));
        assert!(matches!(
            yang_rational::<Rational>(usize::MAX, &q(1, 1)),
            Err(FusionError::Overflow { .. })
        ));
        let rectangular = BasicMatrix::<Rational>::from_row_major(usize::MAX, 0, vec![]).unwrap();
        assert!(matches!(
            base_dimension(&rectangular),
            Err(FusionError::NotSquare { .. })
        ));
        let r = matrix::identity::<Rational>(4).unwrap();
        let tight = OperationLimits {
            max_elements: 1 << 20,
            max_scalar_ops: 1,
        };
        assert!(matches!(
            braid_form_defect_with_limits(&r, tight),
            Err(FusionError::Budget {
                what: "Yang-Baxter scalar work",
                ..
            })
        ));
    }

    #[test]
    fn spectral_families_use_one_checked_carrier_and_one_value_per_argument() {
        assert!(matches!(
            spectral_form_defect(
                |u| yang_rational(if u == &q(0, 1) { 2 } else { 3 }, u),
                &q(0, 1),
                &q(1, 1),
                &q(2, 1)
            ),
            Err(FusionError::Shape { .. })
        ));
        let seen = std::cell::RefCell::new(Vec::new());
        let defect = spectral_braid_form_defect(
            |u| {
                seen.borrow_mut().push(u.clone());
                matrix::identity::<Rational>(4).map_err(FusionError::from)
            },
            &q(1, 1),
            &q(2, 1),
            &q(3, 1),
        )
        .unwrap();
        assert!(matrix::is_zero_matrix(&defect));
        assert_eq!(*seen.borrow(), vec![q(1, 1), q(2, 1), q(3, 1)]);
    }

    fn pauli_x() -> BasicMatrix<Rational> {
        matrix::from_rows(vec![vec![q(0, 1), q(1, 1)], vec![q(1, 1), q(0, 1)]])
            .map_err(FusionError::from)
            .unwrap()
    }

    fn pauli_z() -> BasicMatrix<Rational> {
        matrix::from_rows(vec![vec![q(1, 1), q(0, 1)], vec![q(0, 1), q(-1, 1)]])
            .map_err(FusionError::from)
            .unwrap()
    }

    #[test]
    fn the_flip_squares_to_the_identity_and_swaps_basis_vectors() {
        let p = swap_matrix::<Rational>(3).unwrap();
        assert!(matrix::is_identity_matrix(
            &matrix::multiply(&p, &p).map_err(FusionError::from).unwrap()
        )
        .map_err(FusionError::from)
        .unwrap());
        assert_eq!(p.get(7, 5).unwrap(), q(1, 1));
        assert_eq!(p.get(5, 5).unwrap(), q(0, 1));
        assert_eq!(base_dimension(&p).unwrap(), 3);
        assert!(base_dimension(
            &matrix::zeros::<Rational>(5, 5)
                .map_err(FusionError::from)
                .unwrap()
        )
        .is_err());
        assert!(base_dimension(
            &matrix::zeros::<Rational>(4, 6)
                .map_err(FusionError::from)
                .unwrap()
        )
        .is_err());
    }

    #[test]
    fn yang_rational_satisfies_the_spectral_and_braid_forms() {
        let (u, v) = (q(3, 2), q(2, 5));
        let family = |x: &Rational| yang_rational::<Rational>(2, x);
        let defect = spectral_form_defect(family, &(&u - &v), &u, &v).unwrap();
        assert!(
            matrix::is_zero_matrix(&defect),
            "R12(u-v) R13(u) R23(v) = R23(v) R13(u) R12(u-v)"
        );
        let braid_family = |x: &Rational| -> Result<BasicMatrix<Rational>, FusionError> {
            matrix::multiply(
                &swap_matrix::<Rational>(2)?,
                &yang_rational::<Rational>(2, x)?,
            )
            .map_err(FusionError::from)
        };
        let defect = spectral_braid_form_defect(braid_family, &(&u - &v), &u, &v).unwrap();
        assert!(matrix::is_zero_matrix(&defect));
        let product = matrix::multiply(
            &yang_rational::<Rational>(2, &u).unwrap(),
            &yang_rational::<Rational>(2, &(-&u)).unwrap(),
        )
        .map_err(FusionError::from)
        .unwrap();
        let scaled = matrix::scale(
            &matrix::identity::<Rational>(4)
                .map_err(FusionError::from)
                .unwrap(),
            &(Rational::from_integer(1.into()) - &u * &u),
        )
        .map_err(FusionError::from)
        .unwrap();
        assert_eq!(product, scaled);
        assert_eq!(
            yang_rational::<Rational>(2, &q(0, 1)).unwrap(),
            swap_matrix::<Rational>(2).unwrap()
        );
    }

    #[test]
    fn mismatched_spectral_arguments_violate_the_equation() {
        let (u, v) = (q(3, 2), q(2, 5));
        let family = |x: &Rational| yang_rational::<Rational>(2, x);
        let defect = spectral_form_defect(family, &(&u + &v), &u, &v).unwrap();
        assert!(!matrix::is_zero_matrix(&defect));
    }

    #[test]
    fn hecke_matrices_satisfy_the_braid_relation_and_the_quadratic_relation() {
        let two = q(2, 1);
        let r = hecke(&two).unwrap();
        assert_eq!(
            r,
            matrix::from_rows(vec![
                vec![q(2, 1), q(0, 1), q(0, 1), q(0, 1)],
                vec![q(0, 1), q(0, 1), q(1, 1), q(0, 1)],
                vec![q(0, 1), q(1, 1), q(3, 2), q(0, 1)],
                vec![q(0, 1), q(0, 1), q(0, 1), q(2, 1)],
            ])
            .map_err(FusionError::from)
            .unwrap()
        );
        assert!(matrix::is_zero_matrix(&braid_form_defect(&r).unwrap()));
        assert!(matrix::is_zero_matrix(
            &hecke_quadratic_defect(&r, &two).unwrap()
        ));
        let difference = matrix::sub(
            &r,
            &elimination::inverse(&r)
                .map_err(FusionError::from)
                .map_err(FusionError::from)
                .unwrap(),
        )
        .map_err(FusionError::from)
        .unwrap();
        let expected = matrix::scale(
            &matrix::identity::<Rational>(4)
                .map_err(FusionError::from)
                .unwrap(),
            &q(3, 2),
        )
        .map_err(FusionError::from)
        .unwrap();
        assert_eq!(difference, expected);
        assert!(hecke(&q(0, 1)).is_err(), "q = 0 has no inverse");
    }

    #[test]
    fn perturbed_hecke_matrices_violate_the_braid_relation() {
        let two = q(2, 1);
        let mut entries = matrix::to_rows(&hecke(&two).unwrap())
            .map_err(FusionError::from)
            .unwrap();
        entries[2][2] = q(5, 2);
        let bad = matrix::from_rows(entries)
            .map_err(FusionError::from)
            .unwrap();
        assert!(!matrix::is_zero_matrix(&braid_form_defect(&bad).unwrap()));
        assert!(!matrix::is_zero_matrix(
            &hecke_quadratic_defect(&bad, &two).unwrap()
        ));
    }

    #[test]
    fn the_six_vertex_matrix_satisfies_the_multiplicative_yang_baxter_equation() {
        let (z1, z2) = (q(3, 1), q(5, 7));
        let param = q(2, 1);
        let family = |z: &Rational| six_vertex(&param, z);
        let ratio = &z1 / &z2;
        let defect = spectral_form_defect(family, &ratio, &z1, &z2).unwrap();
        assert!(matrix::is_zero_matrix(&defect));
        let perturbed = |z: &Rational| -> Result<BasicMatrix<Rational>, FusionError> {
            let mut entries =
                matrix::to_rows(&six_vertex(&param, z)?).map_err(FusionError::from)?;
            entries[1][1] = &entries[1][1] + q(1, 1);
            matrix::from_rows(entries).map_err(FusionError::from)
        };
        assert!(!matrix::is_zero_matrix(
            &spectral_form_defect(perturbed, &ratio, &z1, &z2).unwrap()
        ));
        assert!(six_vertex(&q(0, 1), &z1).is_err());
    }

    #[test]
    fn unmatched_pauli_mixtures_are_genuine_negative_controls_but_commuting_ones_are_not() {
        let (u, v) = (q(3, 2), q(2, 5));
        let zz = matrix::kronecker(&pauli_z(), &pauli_z())
            .map_err(FusionError::from)
            .unwrap();
        let xx = matrix::kronecker(&pauli_x(), &pauli_x())
            .map_err(FusionError::from)
            .unwrap();
        let identity = matrix::identity::<Rational>(4)
            .map_err(FusionError::from)
            .unwrap();
        let commuting = |x: &Rational| {
            matrix::add(
                &matrix::scale(&identity, x).map_err(FusionError::from)?,
                &zz,
            )
            .map_err(FusionError::from)
        };
        assert!(matrix::is_zero_matrix(
            &spectral_form_defect(commuting, &(&u - &v), &u, &v).unwrap()
        ));
        let mixed = |x: &Rational| -> Result<BasicMatrix<Rational>, FusionError> {
            matrix::add(
                &matrix::add(
                    &matrix::scale(&identity, x).map_err(FusionError::from)?,
                    &matrix::scale(&xx, &q(2, 1)).map_err(FusionError::from)?,
                )
                .map_err(FusionError::from)?,
                &zz,
            )
            .map_err(FusionError::from)
        };
        assert!(!matrix::is_zero_matrix(
            &spectral_form_defect(mixed, &(&u - &v), &u, &v).unwrap()
        ));
        let scaled_flip = |x: &Rational| -> Result<BasicMatrix<Rational>, FusionError> {
            matrix::add(
                &matrix::scale(&identity, x).map_err(FusionError::from)?,
                &matrix::scale(&swap_matrix::<Rational>(2)?, &q(7, 3))
                    .map_err(FusionError::from)?,
            )
            .map_err(FusionError::from)
        };
        assert!(matrix::is_zero_matrix(
            &spectral_form_defect(scaled_flip, &(&u - &v), &u, &v).unwrap()
        ));
    }
}
