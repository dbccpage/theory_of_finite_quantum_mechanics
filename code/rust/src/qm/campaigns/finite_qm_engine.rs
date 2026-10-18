//! Campaign module finite_qm_engine.
//!
//! One step of a finite engine applies the rotation `[[0,-1],[1,0]]`.
//! The determinant is 1 by the Leibniz formula and by the action on the
//! standard basis, and the rotation preserves the squared Euclidean norm.

pub fn verify() -> Result<i64, &'static str> {
    let rotation = [[0i64, -1], [1, 0]];
    let minor = rotation[0][1]
        .checked_mul(rotation[1][0])
        .ok_or("det")?;
    let leibniz = rotation[0][0]
        .checked_mul(rotation[1][1])
        .and_then(|v| v.checked_sub(minor))
        .ok_or("det")?;
    let column_area = rotation[1][0]
        .checked_mul(rotation[0][1].checked_neg().ok_or("neg")?)
        .ok_or("det")?;
    // Columns are the images of the basis. det is the signed area of those images.
    if leibniz != 1 || column_area != 1 {
        return Err("engine step is not a rotation of determinant 1");
    }
    let state = [3i64, 4];
    let image = [
        rotation[0][0]
            .checked_mul(state[0])
            .and_then(|v| {
                rotation[0][1]
                    .checked_mul(state[1])
                    .and_then(|term| v.checked_add(term))
            })
            .ok_or("step")?,
        rotation[1][0]
            .checked_mul(state[0])
            .and_then(|v| {
                rotation[1][1]
                    .checked_mul(state[1])
                    .and_then(|term| v.checked_add(term))
            })
            .ok_or("step")?,
    ];
    let before = norm_sq(&state)?;
    let after = norm_sq(&image)?;
    if before != after {
        return Err("engine step changed the norm");
    }
    Ok(after)
}

fn norm_sq(vector: &[i64; 2]) -> Result<i64, &'static str> {
    let left = vector[0].checked_mul(vector[0]).ok_or("norm")?;
    let right = vector[1].checked_mul(vector[1]).ok_or("norm")?;
    left.checked_add(right).ok_or("norm")
}
