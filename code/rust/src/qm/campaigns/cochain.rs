//! Campaign module cochain.
//!
//! Oriented boundary of a triangle. `∂₁ ∂₂` is the zero column by matrix
//! multiplication and by the telescoping vertex sum.

pub fn verify() -> Result<[i64; 3], &'static str> {
    // Columns are edges 01, 12, 20. Rows are vertices 0, 1, 2.
    let boundary_1 = [[-1i64, 0, 1], [1, -1, 0], [0, 1, -1]];
    let boundary_2 = [1i64, 1, 1];
    let mut by_matrix = [0i64; 3];
    for row in 0..3 {
        for col in 0..3 {
            by_matrix[row] = by_matrix[row]
                .checked_add(boundary_1[row][col].checked_mul(boundary_2[col]).ok_or("mul")?)
                .ok_or("mul")?;
        }
    }
    let by_telescope = [
        -boundary_2[0] + boundary_2[2],
        boundary_2[0] - boundary_2[1],
        boundary_2[1] - boundary_2[2],
    ];
    if by_matrix != by_telescope || by_matrix.iter().any(|entry| *entry != 0) {
        return Err("∂₁∂₂ is not zero");
    }
    Ok(by_matrix)
}
