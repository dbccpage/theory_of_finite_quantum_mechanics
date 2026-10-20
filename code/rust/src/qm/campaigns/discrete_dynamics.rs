
pub fn verify() -> Result<usize, &'static str> {
    let modulus = 7i64;
    verify_bijection(modulus)?;
    let cycles = count_orbit_cycles(modulus)?;
    Ok(cycles)
}

fn verify_bijection(modulus: i64) -> Result<(), &'static str> {
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
    Ok(())
}

fn trace_orbit(start: i64, modulus: i64, visited: &mut [bool; 7]) -> Result<(), &'static str> {
    let mut cursor = start;
    for _ in 0..7 {
        let slot = usize::try_from(cursor).map_err(|_| "index")?;
        if visited[slot] {
            break;
        }
        visited[slot] = true;
        cursor = (2 * cursor + 1).rem_euclid(modulus);
    }
    Ok(())
}

fn count_orbit_cycles(modulus: i64) -> Result<usize, &'static str> {
    let mut visited = [false; 7];
    let mut cycles = 0usize;
    for start in 0..modulus {
        let slot = usize::try_from(start).map_err(|_| "index")?;
        if !visited[slot] {
            cycles += 1;
            trace_orbit(start, modulus, &mut visited)?;
        }
    }
    if visited.iter().any(|hit| !*hit) || cycles != 3 {
        return Err("orbit census does not cover Z/7Z in three cycles");
    }
    Ok(cycles)
}
