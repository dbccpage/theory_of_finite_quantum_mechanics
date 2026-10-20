//! Independent exact arithmetic and public-storage boundary challenges.
//! AuthorityEffect: None.
use num_rational::BigRational;
use omega_kernel::resource_limits::OperationLimits;
use tfqm_holonomy::{
    compute_loop_holonomy, curvature_commutator, plaquette_curvature, DiscreteConnection,
    ExactMatrix, HolonomyError,
};

fn rational(value: i64) -> BigRational {
    BigRational::from_integer(value.into())
}

fn matrix(values: [i64; 4]) -> ExactMatrix<BigRational> {
    ExactMatrix::try_new(2, 2, values.into_iter().map(rational).collect()).unwrap()
}

fn triangle() -> DiscreteConnection<BigRational> {
    let mut connection = DiscreteConnection::new(1, OperationLimits::holonomy());
    for (source, target) in [("u", "v"), ("v", "w"), ("w", "u")] {
        connection
            .set_connection(source, target, ExactMatrix::try_identity(1).unwrap())
            .unwrap();
    }
    connection
}

fn boundary() -> Vec<String> {
    ["u", "v", "w", "u"].into_iter().map(String::from).collect()
}

#[test]
fn public_rectangular_transports_are_refused_at_path_boundary() {
    for (rows, cols) in [(2, 1), (1, 2), (0, 1), (1, 0)] {
        let mut connection = triangle();
        let transport = ExactMatrix::try_new(rows, cols, vec![rational(1); rows * cols]).unwrap();
        connection
            .forward
            .insert(("w".into(), "u".into()), transport);
        assert!(matches!(
            compute_loop_holonomy(&connection, &boundary()),
            Err(HolonomyError::DimensionMismatch { expected: 1, .. })
        ));
        assert!(matches!(
            plaquette_curvature(&connection, &boundary()),
            Err(HolonomyError::DimensionMismatch { expected: 1, .. })
        ));
    }
}

#[test]
fn valid_triangle_and_zero_transport_have_literal_curvature() {
    let mut connection = triangle();
    assert_eq!(
        plaquette_curvature(&connection, &boundary())
            .unwrap()
            .as_slice(),
        &[rational(0)]
    );
    connection.forward.insert(
        ("w".into(), "u".into()),
        ExactMatrix::try_zero(1, 1).unwrap(),
    );
    assert_eq!(
        plaquette_curvature(&connection, &boundary())
            .unwrap()
            .as_slice(),
        &[rational(-1)]
    );
}

fn entries(mut ordinal: usize) -> [i64; 4] {
    let mut output = [0; 4];
    for value in &mut output {
        *value = (ordinal % 3) as i64 - 1;
        ordinal /= 3;
    }
    output
}

#[test]
fn all_ternary_two_by_two_commutators_match_integer_formula() {
    for i in 0..81 {
        for j in 0..81 {
            let a = entries(i);
            let b = entries(j);
            let expected = [
                a[1] * b[2] - b[1] * a[2],
                a[0] * b[1] + a[1] * b[3] - b[0] * a[1] - b[1] * a[3],
                a[2] * b[0] + a[3] * b[2] - b[2] * a[0] - b[3] * a[2],
                a[2] * b[1] - b[2] * a[1],
            ];
            let actual =
                curvature_commutator(&matrix(a), &matrix(b), &OperationLimits::holonomy()).unwrap();
            assert_eq!(actual.as_slice(), expected.map(rational));
        }
    }
}

#[test]
fn commutator_enforces_inclusive_separate_resource_limits() {
    let identity = matrix([1, 0, 0, 1]);
    let mut limits = OperationLimits::holonomy();
    limits.max_cells = 3;
    assert_eq!(
        curvature_commutator(&identity, &identity, &limits),
        Err(HolonomyError::MatrixCellLimitExceeded {
            requested: 4,
            limit: 3
        })
    );
    limits.max_cells = 4;
    limits.max_operations = 35;
    assert_eq!(
        curvature_commutator(&identity, &identity, &limits),
        Err(HolonomyError::OperationLimitExceeded {
            requested: 36,
            limit: 35
        })
    );
    limits.max_operations = 36;
    assert_eq!(
        curvature_commutator(&identity, &identity, &limits)
            .unwrap()
            .as_slice(),
        &[rational(0), rational(0), rational(0), rational(0)]
    );
    limits.max_dimension = 1;
    assert_eq!(
        curvature_commutator(&identity, &identity, &limits),
        Err(HolonomyError::DimensionMismatch {
            expected: 1,
            actual: 2
        })
    );
    let empty = ExactMatrix::<BigRational>::try_zero(0, 0).unwrap();
    limits.max_cells = 0;
    limits.max_operations = 0;
    limits.max_dimension = 0;
    assert_eq!(
        curvature_commutator(&empty, &empty, &limits)
            .unwrap()
            .shape(),
        (0, 0)
    );
}

#[test]
fn shape_and_path_resource_refusals_are_typed() {
    let rectangle = ExactMatrix::<BigRational>::try_zero(1, 2).unwrap();
    assert!(matches!(
        curvature_commutator(&rectangle, &rectangle, &OperationLimits::holonomy()),
        Err(HolonomyError::DimensionMismatch { .. })
    ));
    let mut connection = triangle();
    connection.limits.max_cells = 0;
    assert_eq!(
        compute_loop_holonomy(&connection, &boundary()),
        Err(HolonomyError::MatrixCellLimitExceeded {
            requested: 1,
            limit: 0
        })
    );
    connection.limits.max_cells = 1;
    connection.limits.max_operations = 1;
    assert_eq!(
        compute_loop_holonomy(&connection, &boundary()),
        Err(HolonomyError::OperationLimitExceeded {
            requested: 2,
            limit: 1
        })
    );
}
