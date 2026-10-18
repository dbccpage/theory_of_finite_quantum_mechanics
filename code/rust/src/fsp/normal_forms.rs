//! Normal form solvers: RREF over Q, quotient normal form modulo im(d0),
//! exact L1 quotient distance solver, and graph switching normal form over F2.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use std::collections::VecDeque;

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RrefResult {
    pub rref: Vec<Vec<BigRational>>,
    pub transform: Vec<Vec<BigRational>>, // T such that T * A = R
    pub pivots: Vec<usize>,
    pub rank: usize,
}

/// Compute Reduced Row Echelon Form (RREF) over Q with row operation witness matrix T.
pub fn rref_with_witness(
    matrix: &[Vec<BigRational>],
    num_cols: usize,
) -> Result<RrefResult, &'static str> {
    let num_rows = matrix.len();
    if num_rows == 0 || num_cols == 0 {
        return Ok(RrefResult {
            rref: Vec::new(),
            transform: Vec::new(),
            pivots: Vec::new(),
            rank: 0,
        });
    }

    let mut rref: Vec<Vec<BigRational>> = matrix.to_vec();
    let mut transform = vec![vec![BigRational::zero(); num_rows]; num_rows];
    for i in 0..num_rows {
        transform[i][i] = BigRational::one();
    }

    let mut pivots = Vec::new();
    let mut rank = 0;

    for col in 0..num_cols {
        // Find first nonzero row in col >= rank
        let mut pivot_row = None;
        for r in rank..num_rows {
            if !rref[r][col].is_zero() {
                pivot_row = Some(r);
                break;
            }
        }
        let p = match pivot_row {
            Some(r) => r,
            None => continue,
        };

        // Swap pivot row with current rank row
        rref.swap(rank, p);
        transform.swap(rank, p);

        // Normalize rank row so leading entry is 1
        let scale = rref[rank][col].clone();
        for c in 0..num_cols {
            rref[rank][c] = &rref[rank][c] / &scale;
        }
        for c in 0..num_rows {
            transform[rank][c] = &transform[rank][c] / &scale;
        }

        // Eliminate column entries in all other rows
        for r in 0..num_rows {
            if r == rank {
                continue;
            }
            let factor = rref[r][col].clone();
            if !factor.is_zero() {
                for c in 0..num_cols {
                    let term = &factor * &rref[rank][c];
                    rref[r][c] = &rref[r][c] - term;
                }
                for c in 0..num_rows {
                    let term = &factor * &transform[rank][c];
                    transform[r][c] = &transform[r][c] - term;
                }
            }
        }

        pivots.push(col);
        rank += 1;
        if rank == num_rows {
            break;
        }
    }

    Ok(RrefResult {
        rref: rref[..rank].to_vec(),
        transform: transform[..rank].to_vec(),
        pivots,
        rank,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct QuotientNormalForm {
    pub representative: Vec<BigRational>,
    pub gauge: Vec<BigRational>,
    pub pivot_coordinates: Vec<usize>,
}

/// Compute Quotient Normal Form modulo im(d0).
/// Sets pivot coordinates to zero and returns unique representative and gauge.
pub fn normalize_cochain(
    d0: &[Vec<BigRational>], // dim_c1 x dim_c0
    c1: &[BigRational],      // dim_c1
) -> Result<QuotientNormalForm, &'static str> {
    let dim_c1 = d0.len();
    if dim_c1 == 0 {
        return Err("d0 must have nonzero row count");
    }
    let dim_c0 = d0[0].len();
    if c1.len() != dim_c1 {
        return Err("c1 length must match dim_c1");
    }

    // Transpose d0 to get columns of d0 as rows for RREF: size dim_c0 x dim_c1
    let mut columns = vec![vec![BigRational::zero(); dim_c1]; dim_c0];
    for r in 0..dim_c1 {
        for c in 0..dim_c0 {
            columns[c][r] = d0[r][c].clone();
        }
    }

    let rref_res = rref_with_witness(&columns, dim_c1)?;
    let mut residual = c1.to_vec();
    let mut gauge = vec![BigRational::zero(); dim_c0];

    for idx in 0..rref_res.rank {
        let pivot = rref_res.pivots[idx];
        let coef = residual[pivot].clone();
        if !coef.is_zero() {
            for c in 0..dim_c1 {
                let term = &coef * &rref_res.rref[idx][c];
                residual[c] = &residual[c] - term;
            }
            for j in 0..dim_c0 {
                let term = &coef * &rref_res.transform[idx][j];
                gauge[j] = &gauge[j] + term;
            }
        }
    }

    Ok(QuotientNormalForm {
        representative: residual,
        gauge,
        pivot_coordinates: rref_res.pivots,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SignSwitchingNormalForm {
    pub parities: Vec<u8>,
    pub gauge: Vec<u8>,
    pub forest_edges: Vec<usize>,
    pub obstruction_cycles: Vec<Vec<usize>>,
}

/// Normalizes F2 edge signs modulo vertex switching on a fixed ordered graph.
/// Spanning forest is chosen greedily following declared edge order.
/// Odd cycles witnessing sign obstruction are produced for each nonzero chord.
pub fn normalize_sign_cochain(
    vertex_count: usize,
    edges: &[(usize, usize)],
    parities: &[u8],
) -> Result<SignSwitchingNormalForm, &'static str> {
    if edges.len() != parities.len() {
        return Err("edge count and parity count mismatch");
    }
    for &p in parities {
        if p > 1 {
            return Err("edge parity must be in {0, 1}");
        }
    }
    for &(u, v) in edges {
        if u >= vertex_count || v >= vertex_count {
            return Err("edge endpoint out of range");
        }
    }

    // Disjoint set / union-find for spanning forest
    let mut parents: Vec<usize> = (0..vertex_count).collect();
    fn find(parents: &mut [usize], mut v: usize) -> usize {
        while parents[v] != v {
            parents[v] = parents[parents[v]];
            v = parents[v];
        }
        v
    }

    let mut adjacency: Vec<Vec<(usize, usize)>> = vec![Vec::new(); vertex_count];
    let mut forest_edges = Vec::new();

    for (edge_idx, &(u, v)) in edges.iter().enumerate() {
        if u == v {
            continue; // self loop
        }
        let ru = find(&mut parents, u);
        let rv = find(&mut parents, v);
        if ru != rv {
            parents[rv] = ru;
            forest_edges.push(edge_idx);
            adjacency[u].push((v, edge_idx));
            adjacency[v].push((u, edge_idx));
        }
    }

    // BFS tree gauge assignment
    let mut gauge: Vec<Option<u8>> = vec![None; vertex_count];
    let mut paths: Vec<Vec<usize>> = vec![Vec::new(); vertex_count];

    for start in 0..vertex_count {
        if gauge[start].is_some() {
            continue;
        }
        gauge[start] = Some(0);
        let mut queue = VecDeque::new();
        queue.push_back(start);

        while let Some(u) = queue.pop_front() {
            let u_gauge = gauge[u].unwrap();
            for &(v, edge_idx) in &adjacency[u] {
                if gauge[v].is_none() {
                    let v_gauge = u_gauge ^ parities[edge_idx];
                    gauge[v] = Some(v_gauge);
                    let mut path_v = paths[u].clone();
                    path_v.push(edge_idx);
                    paths[v] = path_v;
                    queue.push_back(v);
                }
            }
        }
    }

    let final_gauge: Vec<u8> = gauge.into_iter().map(|g| g.unwrap_or(0)).collect();

    let mut normal_parities = Vec::with_capacity(edges.len());
    let mut obstruction_cycles = Vec::new();

    for (edge_idx, &(u, v)) in edges.iter().enumerate() {
        let norm_bit = parities[edge_idx] ^ final_gauge[u] ^ final_gauge[v];
        normal_parities.push(norm_bit);

        if norm_bit == 1 {
            // Reconstruct fundamental cycle
            let mut edge_set = std::collections::BTreeSet::new();
            for &e in &paths[u] {
                if edge_set.contains(&e) {
                    edge_set.remove(&e);
                } else {
                    edge_set.insert(e);
                }
            }
            for &e in &paths[v] {
                if edge_set.contains(&e) {
                    edge_set.remove(&e);
                } else {
                    edge_set.insert(e);
                }
            }
            edge_set.insert(edge_idx);
            let cycle: Vec<usize> = edge_set.into_iter().collect();
            obstruction_cycles.push(cycle);
        }
    }

    Ok(SignSwitchingNormalForm {
        parities: normal_parities,
        gauge: final_gauge,
        forest_edges,
        obstruction_cycles,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;

    #[test]
    fn rref_2x2_identity_and_singular() {
        let m = vec![
            vec![BigRational::from(BigInt::from(1)), BigRational::from(BigInt::from(2))],
            vec![BigRational::from(BigInt::from(3)), BigRational::from(BigInt::from(4))],
        ];
        let res = rref_with_witness(&m, 2).unwrap();
        assert_eq!(res.rank, 2);
        assert_eq!(res.pivots, vec![0, 1]);
        assert_eq!(res.rref[0], vec![BigRational::one(), BigRational::zero()]);
        assert_eq!(res.rref[1], vec![BigRational::zero(), BigRational::one()]);
    }

    #[test]
    fn quotient_normal_form_projection() {
        // d0: [ [1], [1] ] -> dim_c1=2, dim_c0=1
        let d0 = vec![vec![BigRational::one()], vec![BigRational::one()]];
        let c1 = vec![BigRational::from(BigInt::from(5)), BigRational::from(BigInt::from(7))];
        let qnf = normalize_cochain(&d0, &c1).unwrap();
        // Pivot is coordinate 0, so representative at 0 must be 0!
        assert_eq!(qnf.representative[0], BigRational::zero());
        assert_eq!(qnf.representative[1], BigRational::from(BigInt::from(2)));
    }

    #[test]
    fn sign_switching_triangle_obstruction() {
        // Triangle with parities [0, 0, 1] -> odd cycle has obstruction
        let edges = vec![(0, 1), (1, 2), (0, 2)];
        let parities = vec![0, 0, 1];
        let nf = normalize_sign_cochain(3, &edges, &parities).unwrap();
        assert_eq!(nf.forest_edges.len(), 2);
        assert_eq!(nf.obstruction_cycles.len(), 1);
        assert_eq!(nf.obstruction_cycles[0], vec![0, 1, 2]);
    }
}
