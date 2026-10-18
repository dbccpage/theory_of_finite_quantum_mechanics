//! Campaign module simplicial_qm.
//!
//! Stokes' identity on a triangle: the pairing of a 1-cochain with the
//! boundary of the face equals the evaluation of its coboundary on the face.
//! When the cochain is itself a coboundary, both sides vanish.

pub fn verify() -> Result<i64, &'static str> {
    let vertices = [4i64, -2, 5];
    let edges = [
        vertices[1] - vertices[0],
        vertices[2] - vertices[1],
        vertices[0] - vertices[2],
    ];
    let face = [1i64, 1, 1];
    let mut pairing = 0i64;
    for index in 0..3 {
        pairing = pairing
            .checked_add(edges[index].checked_mul(face[index]).ok_or("pair")?)
            .ok_or("pair")?;
    }
    let coboundary = edges[0]
        .checked_add(edges[1])
        .and_then(|v| v.checked_add(edges[2]))
        .ok_or("coboundary")?;
    if pairing != coboundary || pairing != 0 {
        return Err("Stokes pairing is not zero on an exact cochain");
    }
    Ok(pairing)
}
