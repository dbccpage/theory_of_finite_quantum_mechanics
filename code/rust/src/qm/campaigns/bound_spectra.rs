
pub fn verify() -> Result<i64, &'static str> {
    let laplacian = [[1i64, -1, 0], [-1, 2, -1], [0, -1, 1]];
    verify_laplacian_rows(&laplacian)?;
    let vector = [1i64, -1, 0];
    let image = mat_vec_mul(&laplacian, &vector)?;
    let by_matrix = dot_product(&vector, &image)?;
    let by_edges = rayleigh_by_edges(&vector)?;
    if by_matrix != by_edges {
        return Err("Rayleigh readings disagree");
    }
    verify_gershgorin_bound(by_matrix, &vector)?;
    Ok(by_matrix)
}

fn verify_laplacian_rows(laplacian: &[[i64; 3]; 3]) -> Result<(), &'static str> {
    let mut row_sum = [0i64; 3];
    for i in 0..3 {
        for j in 0..3 {
            row_sum[i] = row_sum[i].checked_add(laplacian[i][j]).ok_or("row")?;
        }
        if row_sum[i] != 0 {
            return Err("Laplacian rows do not sum to 0");
        }
    }
    Ok(())
}

fn mat_vec_mul(laplacian: &[[i64; 3]; 3], vector: &[i64; 3]) -> Result<[i64; 3], &'static str> {
    let mut image = [0i64; 3];
    for i in 0..3 {
        for j in 0..3 {
            image[i] = image[i]
                .checked_add(laplacian[i][j].checked_mul(vector[j]).ok_or("mul")?)
                .ok_or("mul")?;
        }
    }
    Ok(image)
}

fn dot_product(left: &[i64; 3], right: &[i64; 3]) -> Result<i64, &'static str> {
    let mut sum = 0i64;
    for i in 0..3 {
        sum = sum
            .checked_add(left[i].checked_mul(right[i]).ok_or("dot")?)
            .ok_or("dot")?;
    }
    Ok(sum)
}

fn rayleigh_by_edges(vector: &[i64; 3]) -> Result<i64, &'static str> {
    let edge_01 = vector[0].checked_sub(vector[1]).ok_or("edge")?;
    let edge_12 = vector[1].checked_sub(vector[2]).ok_or("edge")?;
    let jump_01 = edge_01.checked_mul(edge_01).ok_or("edge")?;
    let jump_12 = edge_12.checked_mul(edge_12).ok_or("edge")?;
    jump_01.checked_add(jump_12).ok_or("edge")
}

fn verify_gershgorin_bound(by_matrix: i64, vector: &[i64; 3]) -> Result<(), &'static str> {
    let norm_sq = dot_product(vector, vector).map_err(|_| "norm")?;
    let cap = norm_sq.checked_mul(4).ok_or("cap")?;
    if by_matrix < 0 || by_matrix > cap {
        return Err("Rayleigh value left the Gershgorin bound");
    }
    Ok(())
}
