//! Campaign module bound_spectra.
//!
//! The path Laplacian on three vertices has a kernel (the constant vector)
//! and a quadratic form equal to the sum of squared edge jumps. Both readings
//! of `x^T L x` agree, and the value sits inside the Gershgorin interval.

pub fn verify() -> Result<i64, &'static str> {
    let laplacian = [[1i64, -1, 0], [-1, 2, -1], [0, -1, 1]];
    let mut row_sum = [0i64; 3];
    for i in 0..3 {
        for j in 0..3 {
            row_sum[i] = row_sum[i].checked_add(laplacian[i][j]).ok_or("row")?;
        }
        if row_sum[i] != 0 {
            return Err("Laplacian rows do not sum to 0");
        }
    }
    let vector = [1i64, -1, 0];
    let mut image = [0i64; 3];
    for i in 0..3 {
        for j in 0..3 {
            image[i] = image[i]
                .checked_add(laplacian[i][j].checked_mul(vector[j]).ok_or("mul")?)
                .ok_or("mul")?;
        }
    }
    let mut by_matrix = 0i64;
    for i in 0..3 {
        by_matrix = by_matrix
            .checked_add(vector[i].checked_mul(image[i]).ok_or("dot")?)
            .ok_or("dot")?;
    }
    let edge_01 = vector[0].checked_sub(vector[1]).ok_or("edge")?;
    let edge_12 = vector[1].checked_sub(vector[2]).ok_or("edge")?;
    let jump_01 = edge_01.checked_mul(edge_01).ok_or("edge")?;
    let jump_12 = edge_12.checked_mul(edge_12).ok_or("edge")?;
    let by_edges = jump_01.checked_add(jump_12).ok_or("edge")?;
    if by_matrix != by_edges {
        return Err("Rayleigh readings disagree");
    }
    let norm_sq = vector
        .iter()
        .try_fold(0i64, |acc, v| v.checked_mul(*v).and_then(|square| acc.checked_add(square)))
        .ok_or("norm")?;
    // Gershgorin puts every eigenvalue in [0, 4], so x^T L x ≤ 4 ||x||².
    let cap = norm_sq.checked_mul(4).ok_or("cap")?;
    if by_matrix < 0 || by_matrix > cap {
        return Err("Rayleigh value left the Gershgorin bound");
    }
    Ok(by_matrix)
}
