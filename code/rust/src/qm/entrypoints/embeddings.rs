
fn verify_product_embedding(z: &(i64, i64), w: &(i64, i64)) -> Result<(), String> {
    let prod = mul_gauss(z, w)?;
    let by_elements = embed(&prod)?;
    let ez = embed(z)?;
    let ew = embed(w)?;
    let by_matrices = mat_mul(&ez, &ew)?;
    if by_elements != by_matrices {
        return Err(format!(
            "embedding failed to preserve multiplication: {by_elements:?} vs {by_matrices:?}"
        ));
    }
    Ok(())
}

pub fn run_embeddings() -> Result<(), String> {
    let one = gauss(1, 0);
    let i = gauss(0, 1);
    let z = gauss(2, -3);
    let w = gauss(4, 1);
    let identity = [[1i64, 0], [0, 1]];
    if embed(&one)? != identity {
        return Err("ρ(1) is not the identity matrix".into());
    }
    verify_product_embedding(&z, &w)?;
    let ei = embed(&i)?;
    let i_sq = mat_mul(&ei, &ei)?;
    if i_sq != [[-1, 0], [0, -1]] {
        return Err(format!("ρ(i)^2 is not -I: {i_sq:?}"));
    }
    Ok(())
}

fn gauss(real: i64, imag: i64) -> (i64, i64) {
    (real, imag)
}

fn mul_gauss(left: &(i64, i64), right: &(i64, i64)) -> Result<(i64, i64), String> {
    let cross = left.1.checked_mul(right.1).ok_or("gaussian product overflow")?;
    let real = left
        .0
        .checked_mul(right.0)
        .and_then(|v| v.checked_sub(cross))
        .ok_or("gaussian product overflow")?;
    let imag = left
        .0
        .checked_mul(right.1)
        .and_then(|v| {
            left.1
                .checked_mul(right.0)
                .and_then(|cross| v.checked_add(cross))
        })
        .ok_or("gaussian product overflow")?;
    Ok((real, imag))
}

fn embed(value: &(i64, i64)) -> Result<[[i64; 2]; 2], String> {
    Ok([[value.0, value.1.checked_neg().ok_or("embed")?], [value.1, value.0]])
}

fn mat_mul(left: &[[i64; 2]; 2], right: &[[i64; 2]; 2]) -> Result<[[i64; 2]; 2], String> {
    let mut out = [[0i64; 2]; 2];
    for i in 0..2 {
        for j in 0..2 {
            let mut slot = 0i64;
            for k in 0..2 {
                slot = slot
                    .checked_add(
                        left[i][k]
                            .checked_mul(right[k][j])
                            .ok_or("matrix product overflow")?,
                    )
                    .ok_or("matrix product overflow")?;
            }
            out[i][j] = slot;
        }
    }
    Ok(out)
}
