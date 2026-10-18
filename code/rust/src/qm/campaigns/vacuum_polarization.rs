//! Campaign module vacuum_polarization.
//!
//! The transverse tensor `Π^{μν} = q² g^{μν} - q^μ q^ν` contracts to zero
//! against `q`. The contraction is the matrix-vector product and the
//! algebraic cancellation `q² q^ν - q^ν q²`.

pub fn verify() -> Result<[i64; 2], &'static str> {
    let q = [2i64, 1];
    let q0_sq = q[0].checked_mul(q[0]).ok_or("q2")?;
    let q1_sq = q[1].checked_mul(q[1]).ok_or("q2")?;
    let q2 = q0_sq.checked_add(q1_sq).ok_or("q2")?;
    let cross = q[0].checked_mul(q[1]).ok_or("tensor")?.checked_neg().ok_or("tensor")?;
    let tensor = [
        [q2.checked_sub(q0_sq).ok_or("tensor")?, cross],
        [cross, q2.checked_sub(q1_sq).ok_or("tensor")?],
    ];
    let mut by_matrix = [0i64; 2];
    for nu in 0..2 {
        for mu in 0..2 {
            by_matrix[nu] = by_matrix[nu]
                .checked_add(q[mu].checked_mul(tensor[mu][nu]).ok_or("mul")?)
                .ok_or("mul")?;
        }
    }
    let alg0 = q2.checked_mul(q[0]).ok_or("alg")?;
    let alg1 = q2.checked_mul(q[1]).ok_or("alg")?;
    let by_algebra = [
        alg0.checked_sub(q[0].checked_mul(q2).ok_or("alg")?).ok_or("alg")?,
        alg1.checked_sub(q[1].checked_mul(q2).ok_or("alg")?).ok_or("alg")?,
    ];
    if by_matrix != by_algebra || by_matrix != [0, 0] {
        return Err("vacuum polarization is not transverse");
    }
    Ok(by_matrix)
}
