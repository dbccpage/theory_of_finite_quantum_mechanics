//! Entrypoint: score_block.
//!
//! Score one block by two readings of the same 2 by 2 determinant: the
//! Leibniz formula over the integers, and Gaussian elimination over the
//! rationals. The block passes only when both scores agree.

use num_bigint::BigInt;
use num_rational::BigRational;

pub fn run_score_block() -> Result<(), String> {
    let matrix = [[3i64, 5], [2, 7]];
    let leibniz = matrix[0][0]
        .checked_mul(matrix[1][1])
        .and_then(|major| {
            matrix[0][1]
                .checked_mul(matrix[1][0])
                .and_then(|minor| major.checked_sub(minor))
        })
        .ok_or("score overflow")?;
    let eliminated = gauss_det(&matrix)?;
    if eliminated != BigRational::from_integer(BigInt::from(leibniz)) {
        return Err(format!(
            "block scores disagree: leibniz {leibniz}, elimination {eliminated}"
        ));
    }
    Ok(())
}

fn gauss_det(matrix: &[[i64; 2]; 2]) -> Result<BigRational, String> {
    let a = BigRational::from_integer(BigInt::from(matrix[0][0]));
    let b = BigRational::from_integer(BigInt::from(matrix[0][1]));
    let c = BigRational::from_integer(BigInt::from(matrix[1][0]));
    let d = BigRational::from_integer(BigInt::from(matrix[1][1]));
    if a == BigRational::from_integer(BigInt::from(0)) {
        return Err("score pivot vanished".into());
    }
    // Schur complement d - c * a^{-1} * b, then det = a * schur.
    let schur = &d - &(&c * &b / &a);
    Ok(&a * &schur)
}
