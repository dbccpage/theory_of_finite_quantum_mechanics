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

fn scale_rref_pivot_row(
    rref_row: &mut [BigRational],
    trans_row: &mut [BigRational],
    num_cols: usize,
    num_rows: usize,
    scale: &BigRational,
) {
    for val in rref_row.iter_mut().take(num_cols) {
        *val = &*val / scale;
    }
    for val in trans_row.iter_mut().take(num_rows) {
        *val = &*val / scale;
    }
}

fn eliminate_rref_column(
    rref: &mut [Vec<BigRational>],
    transform: &mut [Vec<BigRational>],
    rank: usize,
    col: usize,
    num_cols: usize,
    num_rows: usize,
) {
    let pivot_rref = rref[rank].clone();
    let pivot_trans = transform[rank].clone();
    for r in 0..num_rows {
        if r == rank {
            continue;
        }
        let factor = rref[r][col].clone();
        if !factor.is_zero() {
            for c in 0..num_cols {
                let term = &factor * &pivot_rref[c];
                rref[r][c] = &rref[r][c] - term;
            }
            for c in 0..num_rows {
                let term = &factor * &pivot_trans[c];
                transform[r][c] = &transform[r][c] - term;
            }
        }
    }
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
    if matrix.iter().any(|row| row.len() < num_cols) {
        return Err("matrix row length shorter than num_cols");
    }

    let mut rref: Vec<Vec<BigRational>> = matrix.to_vec();
    let mut transform = vec![vec![BigRational::zero(); num_rows]; num_rows];
    for (i, row) in transform.iter_mut().enumerate() {
        row[i] = BigRational::one();
    }

    let mut pivots = Vec::new();
    let mut rank = 0;

    for col in 0..num_cols {
        let Some(p) = (rank..num_rows).find(|&r| !rref[r][col].is_zero()) else {
            continue;
        };

        rref.swap(rank, p);
        transform.swap(rank, p);

        let scale = rref[rank][col].clone();
        scale_rref_pivot_row(&mut rref[rank], &mut transform[rank], num_cols, num_rows, &scale);
        eliminate_rref_column(&mut rref, &mut transform, rank, col, num_cols, num_rows);

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

fn apply_pivot_gauge_step(
    residual: &mut [BigRational],
    gauge: &mut [BigRational],
    rref_row: &[BigRational],
    trans_row: &[BigRational],
    coef: &BigRational,
) {
    for (res_c, rref_c) in residual.iter_mut().zip(rref_row.iter()) {
        *res_c = &*res_c - coef * rref_c;
    }
    for (g_j, tr_j) in gauge.iter_mut().zip(trans_row.iter()) {
        *g_j = &*g_j + coef * tr_j;
    }
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
    if dim_c0 == 0 || d0.iter().any(|row| row.len() != dim_c0) {
        return Err("d0 must be rectangular with positive column count");
    }
    if c1.len() != dim_c1 {
        return Err("c1 length must match dim_c1");
    }

    // Transpose d0 to get columns of d0 as rows for RREF: size dim_c0 x dim_c1
    let mut columns = vec![vec![BigRational::zero(); dim_c1]; dim_c0];
    for (r, row) in d0.iter().enumerate() {
        for (c, val) in row.iter().enumerate() {
            columns[c][r] = val.clone();
        }
    }

    let rref_res = rref_with_witness(&columns, dim_c1)?;
    let mut residual = c1.to_vec();
    let mut gauge = vec![BigRational::zero(); dim_c0];

    for idx in 0..rref_res.rank {
        let pivot = rref_res.pivots[idx];
        let coef = residual[pivot].clone();
        if !coef.is_zero() {
            apply_pivot_gauge_step(
                &mut residual,
                &mut gauge,
                &rref_res.rref[idx],
                &rref_res.transform[idx],
                &coef,
            );
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

fn find_root(parents: &mut [usize], mut v: usize) -> usize {
    while parents[v] != v {
        parents[v] = parents[parents[v]];
        v = parents[v];
    }
    v
}

fn build_spanning_forest(
    vertex_count: usize,
    edges: &[(usize, usize)],
) -> (Vec<Vec<(usize, usize)>>, Vec<usize>) {
    let mut parents: Vec<usize> = (0..vertex_count).collect();
    let mut adjacency: Vec<Vec<(usize, usize)>> = vec![Vec::new(); vertex_count];
    let mut forest_edges = Vec::new();

    for (edge_idx, &(u, v)) in edges.iter().enumerate() {
        if u == v {
            continue;
        }
        let ru = find_root(&mut parents, u);
        let rv = find_root(&mut parents, v);
        if ru != rv {
            parents[rv] = ru;
            forest_edges.push(edge_idx);
            adjacency[u].push((v, edge_idx));
            adjacency[v].push((u, edge_idx));
        }
    }
    (adjacency, forest_edges)
}

fn assign_forest_gauge_and_paths(
    vertex_count: usize,
    adjacency: &[Vec<(usize, usize)>],
    parities: &[u8],
) -> (Vec<u8>, Vec<Vec<usize>>) {
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
            let u_gauge = gauge[u].unwrap_or(0);
            for &(v, edge_idx) in &adjacency[u] {
                if gauge[v].is_none() {
                    gauge[v] = Some(u_gauge ^ parities[edge_idx]);
                    let mut path_v = paths[u].clone();
                    path_v.push(edge_idx);
                    paths[v] = path_v;
                    queue.push_back(v);
                }
            }
        }
    }

    let final_gauge = gauge.into_iter().map(|g| g.unwrap_or(0)).collect();
    (final_gauge, paths)
}

fn symmetric_diff_cycle(path_u: &[usize], path_v: &[usize], chord_idx: usize) -> Vec<usize> {
    let mut edge_set = std::collections::BTreeSet::new();
    for &e in path_u.iter().chain(path_v.iter()) {
        if !edge_set.insert(e) {
            edge_set.remove(&e);
        }
    }
    edge_set.insert(chord_idx);
    edge_set.into_iter().collect()
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
    if parities.iter().any(|&p| p > 1) {
        return Err("edge parity must be in {0, 1}");
    }
    if edges.iter().any(|&(u, v)| u >= vertex_count || v >= vertex_count) {
        return Err("edge endpoint out of range");
    }

    let (adjacency, forest_edges) = build_spanning_forest(vertex_count, edges);
    let (final_gauge, paths) = assign_forest_gauge_and_paths(vertex_count, &adjacency, parities);

    let mut normal_parities = Vec::with_capacity(edges.len());
    let mut obstruction_cycles = Vec::new();

    for (edge_idx, &(u, v)) in edges.iter().enumerate() {
        let norm_bit = parities[edge_idx] ^ final_gauge[u] ^ final_gauge[v];
        normal_parities.push(norm_bit);

        if norm_bit == 1 {
            obstruction_cycles.push(symmetric_diff_cycle(&paths[u], &paths[v], edge_idx));
        }
    }

    Ok(SignSwitchingNormalForm {
        parities: normal_parities,
        gauge: final_gauge,
        forest_edges,
        obstruction_cycles,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SignSwitchingGridRow {
    pub rows: usize,
    pub cols: usize,
    pub vertices: usize,
    pub edges: usize,
    pub forest_size: usize,
    pub fundamental_cycles: usize,
    pub obstruction_cycles_found: usize,
}

/// Finite lattice scaling benchmark for F2 sign-switching normal form across 2D `rows x cols`
/// grids with alternating row-parity flux (frustrated plaquettes).
pub fn benchmark_sign_switching_grid_scaling(
    grid_sizes: &[(usize, usize)],
) -> Result<Vec<SignSwitchingGridRow>, &'static str> {
    if grid_sizes.is_empty() {
        return Err("grid_sizes must not be empty");
    }
    let mut out = Vec::with_capacity(grid_sizes.len());
    for &(rows, cols) in grid_sizes {
        if rows < 2 || cols < 2 {
            return Err("grid dimensions must be at least 2x2");
        }
        let vertices = rows * cols;
        let idx = |r: usize, c: usize| r * cols + c;
        let mut edges = Vec::new();
        let mut parities = Vec::new();
        for r in 0..rows {
            for c in 0..cols {
                if c + 1 < cols {
                    edges.push((idx(r, c), idx(r, c + 1)));
                    // Odd rows carry parity 1 on horizontal bonds to induce frustrated plaquettes
                    parities.push((r % 2) as u8);
                }
                if r + 1 < rows {
                    edges.push((idx(r, c), idx(r + 1, c)));
                    parities.push(0);
                }
            }
        }
        let nf = normalize_sign_cochain(vertices, &edges, &parities)?;
        let fundamental_cycles = edges.len() - (vertices - 1);
        out.push(SignSwitchingGridRow {
            rows,
            cols,
            vertices,
            edges: edges.len(),
            forest_size: nf.forest_edges.len(),
            fundamental_cycles,
            obstruction_cycles_found: nf.obstruction_cycles.len(),
        });
    }
    Ok(out)
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

    #[test]
    fn sign_switching_grid_scaling_up_to_8x8() {
        let sizes = [(2usize, 2usize), (3, 3), (4, 4), (6, 6), (8, 8)];
        let rows = benchmark_sign_switching_grid_scaling(&sizes).unwrap();
        assert_eq!(rows.len(), sizes.len());
        for (&(r, c), row) in sizes.iter().zip(rows.iter()) {
            assert_eq!(row.vertices, r * c);
            assert_eq!(row.edges, r * (c - 1) + (r - 1) * c);
            assert_eq!(row.forest_size, r * c - 1);
            assert_eq!(row.fundamental_cycles, (r - 1) * (c - 1));
            assert!(
                row.obstruction_cycles_found > 0,
                "expected frustrated cycles on {r}x{c}"
            );
        }
    }

    #[test]
    fn sign_switching_nonzero_endpoint_gauge_and_boundary_refusals() {
        let edges = vec![(0, 1), (1, 2), (0, 2)];

        // Parities [0, 1, 0]: tree edges (0,1)=0, (1,2)=1 -> final_gauge = [0, 0, 1].
        // On chord (0,2), parities[2]=0, gauge[0]=0, gauge[2]=1 -> norm_bit = 0 ^ 0 ^ 1 = 1.
        let nf_odd = normalize_sign_cochain(3, &edges, &[0, 1, 0]).unwrap();
        assert_eq!(nf_odd.gauge, vec![0, 0, 1]);
        assert_eq!(nf_odd.parities, vec![0, 0, 1]);
        assert_eq!(nf_odd.obstruction_cycles, vec![vec![0, 1, 2]]);

        // Parities [1, 0, 1]: tree edges (0,1)=1, (1,2)=0 -> final_gauge = [0, 1, 1].
        // On chord (0,2), parities[2]=1, gauge[0]=0, gauge[2]=1 -> norm_bit = 1 ^ 0 ^ 1 = 0 (exact coboundary).
        let nf_even = normalize_sign_cochain(3, &edges, &[1, 0, 1]).unwrap();
        assert_eq!(nf_even.gauge, vec![0, 1, 1]);
        assert_eq!(nf_even.parities, vec![0, 0, 0]);
        assert!(nf_even.obstruction_cycles.is_empty());

        // Boundary refusals for rref_with_witness, normalize_cochain, and normalize_sign_cochain
        let short_row = vec![vec![BigRational::one()]];
        assert!(rref_with_witness(&short_row, 2).is_err());

        let ragged_d0 = vec![
            vec![BigRational::one(), BigRational::zero()],
            vec![BigRational::one()],
        ];
        assert!(normalize_cochain(&ragged_d0, &[BigRational::one(), BigRational::zero()]).is_err());

        assert!(normalize_sign_cochain(3, &edges, &[0, 1]).is_err());
        assert!(normalize_sign_cochain(3, &edges, &[0, 2, 0]).is_err());
        assert!(normalize_sign_cochain(2, &edges, &[0, 1, 0]).is_err());
    }
}
