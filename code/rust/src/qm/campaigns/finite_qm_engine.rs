
pub fn verify() -> Result<i64, &'static str> {
    let rotation = [[0i64, -1], [1, 0]];
    verify_rotation_det(&rotation)?;
    let state = [3i64, 4];
    let image = apply_2x2(&rotation, &state)?;
    let before = norm_sq(&state)?;
    let after = norm_sq(&image)?;
    if before != after {
        return Err("engine step changed the norm");
    }
    Ok(after)
}

fn verify_rotation_det(rotation: &[[i64; 2]; 2]) -> Result<(), &'static str> {
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
    if leibniz != 1 || column_area != 1 {
        return Err("engine step is not a rotation of determinant 1");
    }
    Ok(())
}

fn row_dot(row: &[i64; 2], state: &[i64; 2]) -> Result<i64, &'static str> {
    let left = row[0].checked_mul(state[0]).ok_or("step")?;
    let right = row[1].checked_mul(state[1]).ok_or("step")?;
    left.checked_add(right).ok_or("step")
}

fn apply_2x2(rotation: &[[i64; 2]; 2], state: &[i64; 2]) -> Result<[i64; 2], &'static str> {
    Ok([row_dot(&rotation[0], state)?, row_dot(&rotation[1], state)?])
}

fn norm_sq(vector: &[i64; 2]) -> Result<i64, &'static str> {
    let left = vector[0].checked_mul(vector[0]).ok_or("norm")?;
    let right = vector[1].checked_mul(vector[1]).ok_or("norm")?;
    left.checked_add(right).ok_or("norm")
}
