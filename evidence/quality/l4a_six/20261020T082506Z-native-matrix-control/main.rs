use linear_algebra::backend::basic_matrix::BasicMatrix;
fn main(){
    let left=BasicMatrix::from_row_major(1,1,vec![i64::MAX]).unwrap();
    let right=BasicMatrix::from_row_major(1,1,vec![2i64]).unwrap();
    let observed=std::panic::catch_unwind(||left.mul(&right)).is_err();
    assert!(observed,"native matrix overflow did not reproduce");
    println!("DEFECT_CONFIRMED:provider_native_matrix_multiply_overflow");
}
