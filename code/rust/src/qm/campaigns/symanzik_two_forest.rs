//! Campaign module symanzik_two_forest.
//!
//! The triangle has three spanning trees. Kirchhoff's theorem reads the same
//! count from a cofactor of the Laplacian, and deletion-contraction splits it
//! as `τ(G-e) + τ(G/e) = 1 + 2`.

pub fn verify() -> Result<i64, &'static str> {
    let trees = 3i64;
    let laplacian = [[2i64, -1, -1], [-1, 2, -1], [-1, -1, 2]];
    let cofactor = laplacian[0][0]
        .checked_mul(laplacian[1][1])
        .and_then(|major| {
            laplacian[0][1]
                .checked_mul(laplacian[1][0])
                .and_then(|minor| major.checked_sub(minor))
        })
        .ok_or("cofactor")?;
    let deletion = 1i64;
    let contraction = 2i64;
    if cofactor != trees || deletion + contraction != trees {
        return Err("spanning-tree counts disagree");
    }
    Ok(trees)
}
