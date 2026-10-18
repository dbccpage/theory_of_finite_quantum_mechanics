
pub fn verify() -> Result<i64, &'static str> {
    let swap = [
        [1i64, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ];
    let square = mat_mul(&swap, &swap)?;
    if square != identity() {
        return Err("swap does not square to I");
    }
    for basis in 0..4 {
        let mut vector = [0i64; 4];
        vector[basis] = 1;
        let once = apply(&swap, &vector)?;
        let twice = apply(&swap, &once)?;
        if twice != vector {
            return Err("swap failed to invert on a basis vector");
        }
    }
    let singlet = [0i64, 1, -1, 0];
    let triplet = [0i64, 1, 1, 0];
    if apply(&swap, &singlet)? != scale(&singlet, -1)? {
        return Err("singlet is not antisymmetric");
    }
    if apply(&swap, &triplet)? != triplet {
        return Err("triplet is not symmetric");
    }
    Ok(-1)
}

fn identity() -> [[i64; 4]; 4] {
    let mut out = [[0i64; 4]; 4];
    for i in 0..4 {
        out[i][i] = 1;
    }
    out
}

fn apply(matrix: &[[i64; 4]; 4], vector: &[i64; 4]) -> Result<[i64; 4], &'static str> {
    let mut out = [0i64; 4];
    for i in 0..4 {
        for j in 0..4 {
            out[i] = out[i]
                .checked_add(matrix[i][j].checked_mul(vector[j]).ok_or("mul")?)
                .ok_or("mul")?;
        }
    }
    Ok(out)
}

fn scale(vector: &[i64; 4], factor: i64) -> Result<[i64; 4], &'static str> {
    let mut out = [0i64; 4];
    for i in 0..4 {
        out[i] = vector[i].checked_mul(factor).ok_or("scale")?;
    }
    Ok(out)
}

fn mat_mul(left: &[[i64; 4]; 4], right: &[[i64; 4]; 4]) -> Result<[[i64; 4]; 4], &'static str> {
    let mut out = [[0i64; 4]; 4];
    for i in 0..4 {
        for j in 0..4 {
            for k in 0..4 {
                out[i][j] = out[i][j]
                    .checked_add(left[i][k].checked_mul(right[k][j]).ok_or("mul")?)
                    .ok_or("mul")?;
            }
        }
    }
    Ok(out)
}
