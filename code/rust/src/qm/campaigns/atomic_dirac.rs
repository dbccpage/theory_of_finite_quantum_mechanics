
pub fn verify() -> Result<i64, &'static str> {
    let gamma0 = [[1i64, 0], [0, -1]];
    let gamma1 = [[0i64, 1], [1, 0]];
    let identity = [[1i64, 0], [0, 1]];
    let zero = [[0i64, 0], [0, 0]];
    if mat_mul(&gamma0, &gamma0)? != identity || mat_mul(&gamma1, &gamma1)? != identity {
        return Err("gamma matrices are not involutions");
    }
    if mat_add(mat_mul(&gamma0, &gamma1)?, mat_mul(&gamma1, &gamma0)?)? != zero {
        return Err("gamma matrices do not anticommute");
    }
    let mass = 2i64;
    let momentum = 3i64;
    let hamiltonian = [
        [mass, momentum],
        [momentum, mass.checked_neg().ok_or("mass")?],
    ];
    let squared = mat_mul(&hamiltonian, &hamiltonian)?;
    let mass_sq = mass.checked_mul(mass).ok_or("scalar")?;
    let momentum_sq = momentum.checked_mul(momentum).ok_or("scalar")?;
    let scalar = mass_sq.checked_add(momentum_sq).ok_or("scalar")?;
    if squared != [[scalar, 0], [0, scalar]] {
        return Err("Dirac square disagrees with m²+p²");
    }
    Ok(scalar)
}

fn mat_mul(left: &[[i64; 2]; 2], right: &[[i64; 2]; 2]) -> Result<[[i64; 2]; 2], &'static str> {
    let mut out = [[0i64; 2]; 2];
    for i in 0..2 {
        for j in 0..2 {
            let mut slot = 0i64;
            for k in 0..2 {
                slot = slot
                    .checked_add(left[i][k].checked_mul(right[k][j]).ok_or("mul")?)
                    .ok_or("mul")?;
            }
            out[i][j] = slot;
        }
    }
    Ok(out)
}

fn mat_add(left: [[i64; 2]; 2], right: [[i64; 2]; 2]) -> Result<[[i64; 2]; 2], &'static str> {
    let mut out = [[0i64; 2]; 2];
    for i in 0..2 {
        for j in 0..2 {
            out[i][j] = left[i][j].checked_add(right[i][j]).ok_or("add")?;
        }
    }
    Ok(out)
}
