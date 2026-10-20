
pub fn verify() -> Result<i64, &'static str> {
    let n = 6usize;
    let adjacency = build_cycle_adjacency(n)?;
    let trace = trace_of_square(&adjacency)?;
    let by_degree = i64::try_from(n).map_err(|_| "n")?.checked_mul(2).ok_or("degree")?;
    if trace != by_degree {
        return Err("closed-walk count disagrees with n·degree");
    }
    Ok(trace)
}

fn build_cycle_adjacency(n: usize) -> Result<[[i64; 6]; 6], &'static str> {
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
    Ok(adjacency)
}

fn trace_of_square(adjacency: &[[i64; 6]; 6]) -> Result<i64, &'static str> {
    let mut trace = 0i64;
    for i in 0..6 {
        for k in 0..6 {
            let term = adjacency[i][k].checked_mul(adjacency[k][i]).ok_or("mul")?;
            trace = trace.checked_add(term).ok_or("trace")?;
        }
    }
    Ok(trace)
}
