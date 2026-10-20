
pub fn verify() -> Result<[i64; 2], &'static str> {
    let q = [2i64, 1];
    let (q2, tensor) = build_transverse_tensor(&q)?;
    let by_matrix = contract_q_tensor(&q, &tensor)?;
    let by_algebra = algebraic_transverse_check(&q, q2)?;
    if by_matrix != by_algebra || by_matrix != [0, 0] {
        return Err("vacuum polarization is not transverse");
    }
    Ok(by_matrix)
}

fn build_transverse_tensor(q: &[i64; 2]) -> Result<(i64, [[i64; 2]; 2]), &'static str> {
    let q0_sq = q[0].checked_mul(q[0]).ok_or("q2")?;
    let q1_sq = q[1].checked_mul(q[1]).ok_or("q2")?;
    let q2 = q0_sq.checked_add(q1_sq).ok_or("q2")?;
    let cross = q[0]
        .checked_mul(q[1])
        .ok_or("tensor")?
        .checked_neg()
        .ok_or("tensor")?;
    let tensor = [
        [q2.checked_sub(q0_sq).ok_or("tensor")?, cross],
        [cross, q2.checked_sub(q1_sq).ok_or("tensor")?],
    ];
    Ok((q2, tensor))
}

fn contract_q_tensor(q: &[i64; 2], tensor: &[[i64; 2]; 2]) -> Result<[i64; 2], &'static str> {
    let mut by_matrix = [0i64; 2];
    for nu in 0..2 {
        for mu in 0..2 {
            let term = q[mu].checked_mul(tensor[mu][nu]).ok_or("mul")?;
            by_matrix[nu] = by_matrix[nu].checked_add(term).ok_or("mul")?;
        }
    }
    Ok(by_matrix)
}

fn algebraic_transverse_check(q: &[i64; 2], q2: i64) -> Result<[i64; 2], &'static str> {
    let alg0 = q2.checked_mul(q[0]).ok_or("alg")?;
    let alg1 = q2.checked_mul(q[1]).ok_or("alg")?;
    Ok([
        alg0.checked_sub(q[0].checked_mul(q2).ok_or("alg")?)
            .ok_or("alg")?,
        alg1.checked_sub(q[1].checked_mul(q2).ok_or("alg")?)
            .ok_or("alg")?,
    ])
}
