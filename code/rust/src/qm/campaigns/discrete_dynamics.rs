//! Campaign module discrete_dynamics.
//!
//! The affine map `x ↦ 2x + 1` on `Z/7Z` is a bijection. The closed-form
//! inverse `4(x - 1)` undoes it, and the orbit census is three cycles.

pub fn verify() -> Result<usize, &'static str> {
    let modulus = 7i64;
    let mut image = [false; 7];
    for index in 0..modulus {
        let forward = (2 * index + 1).rem_euclid(modulus);
        let slot = usize::try_from(forward).map_err(|_| "index")?;
        if image[slot] {
            return Err("dynamics collided");
        }
        image[slot] = true;
        let back = (4 * (forward - 1)).rem_euclid(modulus);
        if back != index {
            return Err("inverse dynamics failed");
        }
    }
    if image.iter().any(|hit| !*hit) {
        return Err("dynamics missed a residue");
    }
    let mut visited = [false; 7];
    let mut cycles = 0usize;
    for start in 0..modulus {
        let slot = usize::try_from(start).map_err(|_| "index")?;
        if visited[slot] {
            continue;
        }
        cycles += 1;
        let mut cursor = start;
        for _ in 0..7 {
            let slot = usize::try_from(cursor).map_err(|_| "index")?;
            if visited[slot] {
                break;
            }
            visited[slot] = true;
            cursor = (2 * cursor + 1).rem_euclid(modulus);
        }
    }
    if visited.iter().any(|hit| !*hit) || cycles != 3 {
        return Err("orbit census does not cover Z/7Z in three cycles");
    }
    Ok(cycles)
}
