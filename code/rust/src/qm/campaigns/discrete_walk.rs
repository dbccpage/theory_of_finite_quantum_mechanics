
pub fn verify() -> Result<i64, &'static str> {
    let n = 6usize;
    let mut adjacency = [[0i64; 6]; 6];
    for vertex in 0..n {
        adjacency[vertex][(vertex + 1) % n] = 1;
        adjacency[vertex][(vertex + n - 1) % n] = 1;
    }
    for row in &adjacency {
        let sum: i64 = row.iter().sum();
        if sum != 2 {
            return Err("row sum is not the degree");
        }
    }
    let mut trace = 0i64;
    for i in 0..n {
        let mut diagonal = 0i64;
        for k in 0..n {
            diagonal = diagonal
                .checked_add(adjacency[i][k].checked_mul(adjacency[k][i]).ok_or("mul")?)
                .ok_or("mul")?;
        }
        trace = trace.checked_add(diagonal).ok_or("trace")?;
    }
    let by_degree = i64::try_from(n).map_err(|_| "n")?.checked_mul(2).ok_or("degree")?;
    if trace != by_degree {
        return Err("closed-walk count disagrees with n·degree");
    }
    Ok(trace)
}
