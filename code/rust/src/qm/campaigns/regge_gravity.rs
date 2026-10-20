
pub fn verify() -> Result<i64, &'static str> {
    let vertices = 4i64;
    let edges = 6i64;
    let faces = 4i64;
    let euler = vertices - edges + faces;
    let deficit = sum_vertex_deficits(&[3i64, 3, 3, 3])?;
    let by_euler = 6i64.checked_mul(euler).ok_or("euler")?;
    let by_hands = gauss_bonnet_handshaking(vertices, edges)?;
    if euler != 2 || deficit != by_euler || deficit != by_hands {
        return Err("discrete Gauss-Bonnet failed");
    }
    Ok(deficit)
}

fn sum_vertex_deficits(degrees: &[i64; 4]) -> Result<i64, &'static str> {
    let mut deficit = 0i64;
    for &degree in degrees {
        let local = 6i64.checked_sub(degree).ok_or("deficit")?;
        deficit = deficit.checked_add(local).ok_or("deficit")?;
    }
    Ok(deficit)
}

fn gauss_bonnet_handshaking(vertices: i64, edges: i64) -> Result<i64, &'static str> {
    let six_vertices = 6i64.checked_mul(vertices).ok_or("hands")?;
    let two_edges = 2i64.checked_mul(edges).ok_or("hands")?;
    six_vertices.checked_sub(two_edges).ok_or("hands")
}
