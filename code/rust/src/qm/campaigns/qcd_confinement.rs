//! Campaign module qcd_confinement.
//!
//! Four plaquettes of the 2 by 2 torus. Every edge meets exactly two faces,
//! so the sum of the face boundaries is zero in two ways: by counting
//! incidences, and by adding the boundary vectors over `F2`.

pub fn verify() -> Result<usize, &'static str> {
    let faces: [[usize; 4]; 4] = [
        [0, 2, 4, 5],
        [1, 3, 4, 5],
        [0, 2, 6, 7],
        [1, 3, 6, 7],
    ];
    let mut incidence = [0usize; 8];
    let mut boundary = [0u8; 8];
    for face in faces {
        for edge in face {
            incidence[edge] += 1;
            boundary[edge] ^= 1;
        }
    }
    if incidence.iter().any(|count| *count != 2) {
        return Err("an edge is not shared by two plaquettes");
    }
    if boundary.iter().any(|bit| *bit != 0) {
        return Err("total plaquette boundary is not zero");
    }
    Ok(incidence.iter().sum())
}
