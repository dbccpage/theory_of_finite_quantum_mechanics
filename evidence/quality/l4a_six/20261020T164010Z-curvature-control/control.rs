//! Expected-defect controls for the pinned installed holonomy boundary.
//! These observations are not ordinary passing correctness tests.
//! AuthorityEffect: None.
use num_rational::BigRational;
use omega_kernel::resource_limits::OperationLimits;
use tfqm_holonomy::{
    compute_loop_holonomy, curvature_commutator, plaquette_curvature, DiscreteConnection,
    ExactMatrix,
};

fn identity_connection() -> DiscreteConnection<BigRational> {
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
fn valid_triangle_has_zero_plaquette_curvature() {
    let connection = identity_connection();
    let result = plaquette_curvature(&connection, &boundary()).unwrap();
    assert_eq!(result.shape(), (1, 1));
    assert_eq!(result.as_slice(), &[BigRational::from_integer(0.into())]);
    println!("POSITIVE_CONTROL valid admitted one-dimensional triangle");
}

#[test]
fn public_transport_storage_reaches_a_rectangular_plaquette_index_panic() {
    let mut connection = identity_connection();
    let rectangular = ExactMatrix::try_new(
        2,
        1,
        vec![
            BigRational::from_integer(1.into()),
            BigRational::from_integer(2.into()),
        ],
    )
    .unwrap();
    connection
        .forward
        .insert(("w".into(), "u".into()), rectangular);
    let path = boundary();
    // Establish that the actual lower boundary accepts the forged transport.
    assert_eq!(
        compute_loop_holonomy(&connection, &path).unwrap().shape(),
        (2, 1)
    );
    let observed = std::panic::catch_unwind(|| plaquette_curvature(&connection, &path));
    let failure = observed.expect_err("the pinned public-input panic did not reproduce");
    let message = failure
        .downcast_ref::<String>()
        .map(String::as_str)
        .or_else(|| failure.downcast_ref::<&str>().copied())
        .unwrap_or("non-string panic");
    assert_eq!(
        message,
        "index out of bounds: the len is 1 but the index is 1"
    );
    println!("DEFECT_CONFIRMED curvature plaquette indexes 1x1 identity with a 2x1 loop result");
}

#[test]
fn explicit_zero_commutator_budget_is_ignored() {
    let matrix = ExactMatrix::<BigRational>::try_identity(1).unwrap();
    let mut limits = OperationLimits::holonomy();
    limits.max_cells = 0;
    limits.max_operations = 0;
    let result = curvature_commutator(&matrix, &matrix, &limits).unwrap();
    assert_eq!(result.shape(), (1, 1));
    assert_eq!(result.as_slice(), &[BigRational::from_integer(0.into())]);
    println!("MECHANISM_ABSENT commutator computes despite explicit zero cell and work limits");
}
