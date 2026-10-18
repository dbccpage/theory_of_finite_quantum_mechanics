
pub fn verify() -> Result<i64, &'static str> {
    let vertices = 4i64;
    let edges = 6i64;
    let faces = 4i64;
    let euler = vertices - edges + faces;
    let degrees = [3i64, 3, 3, 3];
    let mut deficit = 0i64;
    for degree in degrees {
        deficit = deficit.checked_add(6i64.checked_sub(degree).ok_or("deficit")?).ok_or("deficit")?;
    }
    let by_euler = 6i64.checked_mul(euler).ok_or("euler")?;
    let six_vertices = 6i64.checked_mul(vertices).ok_or("hands")?;
    let two_edges = 2i64.checked_mul(edges).ok_or("hands")?;
    let by_hands = six_vertices.checked_sub(two_edges).ok_or("hands")?;
    if euler != 2 || deficit != by_euler || deficit != by_hands {
        return Err("discrete Gauss-Bonnet failed");
    }
    Ok(deficit)
}
