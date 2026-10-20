
use num_rational::{BigRational, Rational64};
use tfqm_holonomy::{Connection, CellComplex, ConnectionLaplacian, ExactMatrix, Vertex};

fn reproduced(name: &str, operation: impl FnOnce() + std::panic::UnwindSafe) {
    assert!(std::panic::catch_unwind(operation).is_err(), "expected reachable panic was not reproduced");
    println!("DEFECT_CONFIRMED:{name}");
}

#[test]
fn matrix_public_index_panics_on_out_of_bounds() {
    let matrix = ExactMatrix::try_new(1, 1, vec![BigRational::from_integer(1.into())]).unwrap();
    reproduced("matrix_public_index_panics_on_out_of_bounds", || { matrix.get(1, 0); });
}

#[test]
fn matrix_public_fields_bypass_storage_admission() {
    let forged = ExactMatrix::<BigRational> { rows: 1, cols: 1, data: vec![] };
    let identity = ExactMatrix::<BigRational>::try_identity(1).unwrap();
    reproduced("matrix_public_fields_bypass_storage_admission", || { let _ = forged.matmul(&identity); });
}

#[test]
fn matrix_admits_overflowing_rational64_scalar_arithmetic() {
    let left = ExactMatrix::try_new(1, 1, vec![Rational64::from_integer(i64::MAX)]).unwrap();
    let right = ExactMatrix::try_new(1, 1, vec![Rational64::from_integer(2)]).unwrap();
    reproduced("matrix_admits_overflowing_rational64_scalar_arithmetic", || { let _ = left.matmul(&right); });
}

#[test]
fn connection_accepts_forged_matrix_until_inverse_panics() {
    let forged = ExactMatrix::<BigRational> { rows: 1, cols: 1, data: vec![] };
    let mut connection = Connection::new(1, Default::default());
    reproduced("connection_accepts_forged_matrix_until_inverse_panics", move || { let _ = connection.set_connection("u", "v", forged); });
}

#[test]
fn laplacian_accepts_forged_vertex_registry_until_lookup_panics() {
    let mut complex = CellComplex::new(Default::default());
    complex.vertices.push(Vertex { id: "v".into(), index: 0 });
    let connection = Connection::new(1, Default::default());
    reproduced("laplacian_accepts_forged_vertex_registry_until_lookup_panics", || { let _ = ConnectionLaplacian::compute(&complex, &connection, None); });
}

#[test]
fn gaussian_scalar_accepts_raw_invalid_rational_until_inverse_panics() {
    use tfqm_homology_linear_audit::linear_algebra::scalars::{GaussianRational, Field, Q, q};
    let candidate = GaussianRational::new(Q::new_raw(1.into(), 0.into()), q(0));
    reproduced("gaussian_scalar_accepts_raw_invalid_rational_until_inverse_panics", || { let _ = candidate.try_inv(); });
}
