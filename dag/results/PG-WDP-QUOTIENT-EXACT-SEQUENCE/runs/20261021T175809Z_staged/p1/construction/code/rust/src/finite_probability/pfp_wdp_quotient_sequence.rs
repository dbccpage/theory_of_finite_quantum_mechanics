//! The exact sequence 0 -> H1 -> Q1 -> im d1 -> 0, its splitting freedom and the bound Gamma2 <= ||d1|| Phi1.
//!
//! Exact BigRational replay of `code/python/src/qm/pfp_wdp_quotient_sequence.py` for PFP batch 01, node
//! PG-WDP-QUOTIENT-EXACT-SEQUENCE. Scope: graph windows with non-negative integer weights (weight 0 is a
//! hypothesis-violating seminorm control), integer d1 rows, integer cochain. ||d1|| is the J-to-L1 operator norm
//! (largest column sum over weight). No other norms, no complex coefficients, no derivation of the window.
//! AuthorityEffect: None.
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};

fn q(n: i64) -> BigRational {
    BigRational::from_integer(BigInt::from(n))
}

fn fs(x: &BigRational) -> String {
    if x.denom().is_one() {
        x.numer().to_string()
    } else {
        format!("{}/{}", x.numer(), x.denom())
    }
}

/// A parsed graph window.
pub struct Window {
    pub id: String,
    pub nv: usize,
    pub edges: Vec<(usize, usize)>,
    pub w: Vec<i64>,
    pub d1: Vec<Vec<i64>>,
    pub h: Vec<i64>,
}

fn ints(s: &str) -> Option<Vec<i64>> {
    if s == "-" {
        return Some(vec![]);
    }
    s.split(',').map(|x| x.parse().ok()).collect()
}

/// Parse `id nv edges w d1 h` (the fields after the `window` token).
pub fn parse_window<'a>(mut parts: impl Iterator<Item = &'a str>) -> Option<Window> {
    let id = parts.next()?.to_string();
    let nv: usize = parts.next()?.parse().ok()?;
    let mut edges = Vec::new();
    for e in parts.next()?.split(',') {
        let (s, t) = e.split_once('>')?;
        edges.push((s.parse().ok()?, t.parse().ok()?));
    }
    let w = ints(parts.next()?)?;
    let d1f = parts.next()?;
    let d1 = if d1f == "-" {
        vec![]
    } else {
        d1f.split(';').map(ints).collect::<Option<Vec<_>>>()?
    };
    let h = ints(parts.next()?)?;
    if parts.next().is_some() || edges.len() != w.len() || edges.len() != h.len() {
        return None;
    }
    Some(Window { id, nv, edges, w, d1, h })
}

/// Edge-by-vertex coboundary matrix (loop rows are zero).
pub fn d0_rows(nv: usize, edges: &[(usize, usize)]) -> Vec<Vec<i64>> {
    edges
        .iter()
        .map(|&(s, t)| {
            let mut row = vec![0i64; nv];
            if s != t {
                row[s] = -1;
                row[t] = 1;
            }
            row
        })
        .collect()
}

fn to_q(rows: &[Vec<i64>]) -> Vec<Vec<BigRational>> {
    rows.iter().map(|r| r.iter().map(|&x| q(x)).collect()).collect()
}

pub fn rank(rows: &[Vec<i64>]) -> usize {
    let mut mat = to_q(rows);
    let ncol = if mat.is_empty() { 0 } else { mat[0].len() };
    let mut rk = 0;
    for c in 0..ncol {
        let piv = match (rk..mat.len()).find(|&i| !mat[i][c].is_zero()) {
            Some(p) => p,
            None => continue,
        };
        mat.swap(rk, piv);
        for i in 0..mat.len() {
            if i != rk && !mat[i][c].is_zero() {
                let f = mat[i][c].clone() / mat[rk][c].clone();
                let base = mat[rk].clone();
                for j in 0..ncol {
                    mat[i][j] = mat[i][j].clone() - f.clone() * base[j].clone();
                }
            }
        }
        rk += 1;
    }
    rk
}

/// Solve rows * x = rhs for linearly independent rows (free variables 0); None when dependent.
fn solve_rows(rows: &[Vec<i64>], rhs: &[i64]) -> Option<Vec<BigRational>> {
    let r = rows.len();
    let n = rows[0].len();
    let mut mat: Vec<Vec<BigRational>> = (0..r)
        .map(|i| {
            let mut row: Vec<BigRational> = rows[i].iter().map(|&x| q(x)).collect();
            row.push(q(rhs[i]));
            row
        })
        .collect();
    let mut pivs = Vec::new();
    let mut rk = 0;
    for c in 0..n {
        let piv = match (rk..r).find(|&i| !mat[i][c].is_zero()) {
            Some(p) => p,
            None => continue,
        };
        mat.swap(rk, piv);
        let pv = mat[rk][c].clone();
        for j in 0..=n {
            mat[rk][j] = mat[rk][j].clone() / pv.clone();
        }
        for i in 0..r {
            if i != rk && !mat[i][c].is_zero() {
                let f = mat[i][c].clone();
                let base = mat[rk].clone();
                for j in 0..=n {
                    mat[i][j] = mat[i][j].clone() - f.clone() * base[j].clone();
                }
            }
        }
        pivs.push(c);
        rk += 1;
        if rk == r {
            break;
        }
    }
    if rk < r {
        return None;
    }
    let mut x = vec![BigRational::zero(); n];
    for (i, &c) in pivs.iter().enumerate() {
        x[c] = mat[i][n].clone();
    }
    Some(x)
}

fn combos(m: usize, r: usize) -> Vec<Vec<usize>> {
    fn go(start: usize, m: usize, r: usize, cur: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
        if cur.len() == r {
            out.push(cur.clone());
            return;
        }
        for i in start..m {
            cur.push(i);
            go(i + 1, m, r, cur, out);
            cur.pop();
        }
    }
    let mut out = Vec::new();
    go(0, m, r, &mut Vec::new(), &mut out);
    out
}

fn cost(d0: &[Vec<i64>], w: &[i64], h: &[i64], x: &[BigRational]) -> BigRational {
    let mut total = BigRational::zero();
    for i in 0..d0.len() {
        let mut dx = BigRational::zero();
        for j in 0..x.len() {
            dx += q(d0[i][j]) * x[j].clone();
        }
        total += q(w[i]) * (q(h[i]) - dx).abs();
    }
    total
}

/// Primal: attained minimum of sum_e w_e |h_e - (d0 x)_e| and the first minimising vertex potential x.
pub fn phi1_x(nv: usize, edges: &[(usize, usize)], w: &[i64], h: &[i64]) -> (BigRational, Vec<BigRational>) {
    let d0 = d0_rows(nv, edges);
    let m = d0.len();
    let r = rank(&d0);
    if r == 0 {
        let total = (0..m).fold(BigRational::zero(), |a, i| a + q(w[i]) * q(h[i]).abs());
        return (total, vec![BigRational::zero(); nv]);
    }
    let mut best: Option<(BigRational, Vec<BigRational>)> = None;
    for sub in combos(m, r) {
        let rows: Vec<Vec<i64>> = sub.iter().map(|&i| d0[i].clone()).collect();
        let rhs: Vec<i64> = sub.iter().map(|&i| h[i]).collect();
        let x = match solve_rows(&rows, &rhs) {
            Some(x) => x,
            None => continue,
        };
        let c = cost(&d0, w, h, &x);
        if best.as_ref().map_or(true, |b| c < b.0) {
            best = Some((c, x));
        }
    }
    best.expect("a vertex exists when rank > 0")
}

pub fn phi1(nv: usize, edges: &[(usize, usize)], w: &[i64], h: &[i64]) -> BigRational {
    phi1_x(nv, edges, w, h).0
}

/// Solve sum_j y_j cols[j] = rhs; None unless the solution exists and is unique.
fn unique_solution(cols: &[Vec<i64>], rhs: &[BigRational]) -> Option<Vec<BigRational>> {
    let r = cols.len();
    let n = rhs.len();
    let mut rows: Vec<Vec<BigRational>> = (0..n)
        .map(|i| {
            let mut row: Vec<BigRational> = (0..r).map(|j| q(cols[j][i])).collect();
            row.push(rhs[i].clone());
            row
        })
        .collect();
    let mut used: Vec<usize> = Vec::new();
    for j in 0..r {
        let p = (0..n).find(|i| !used.contains(i) && !rows[*i][j].is_zero())?;
        used.push(p);
        let pivot = rows[p][j].clone();
        for c in 0..=r {
            rows[p][c] = rows[p][c].clone() / pivot.clone();
        }
        for i in 0..n {
            if i != p && !rows[i][j].is_zero() {
                let f = rows[i][j].clone();
                let base = rows[p].clone();
                for c in 0..=r {
                    rows[i][c] = rows[i][c].clone() - f.clone() * base[c].clone();
                }
            }
        }
    }
    if (0..n).any(|i| !used.contains(&i) && !rows[i][r].is_zero()) {
        return None;
    }
    Some((0..r).map(|j| rows[used[j]][r].clone()).collect())
}

/// Dual: maximum of y.h over d0^T y = 0, |y_e| <= w_e and the first maximising vertex y (same order as the Python producer).
pub fn dual_y(nv: usize, edges: &[(usize, usize)], w: &[i64], h: &[i64]) -> (BigRational, Vec<BigRational>) {
    let d0 = d0_rows(nv, edges);
    let m = edges.len();
    let r = rank(&d0);
    let mut best: Option<(BigRational, Vec<BigRational>)> = None;
    for pinned in combos(m, m - r) {
        let free: Vec<usize> = (0..m).filter(|e| !pinned.contains(e)).collect();
        let k = pinned.len();
        for t in 0u32..(1u32 << k) {
            let mut y = vec![BigRational::zero(); m];
            for (pos, &e) in pinned.iter().enumerate() {
                let sign = if (t >> (k - 1 - pos)) & 1 == 0 { 1 } else { -1 };
                y[e] = q(sign * w[e]);
            }
            if !free.is_empty() {
                let rhs: Vec<BigRational> = (0..nv)
                    .map(|v| {
                        let mut s = BigRational::zero();
                        for &e in &pinned {
                            s += y[e].clone() * q(d0[e][v]);
                        }
                        -s
                    })
                    .collect();
                let cols: Vec<Vec<i64>> = free.iter().map(|&e| (0..nv).map(|v| d0[e][v]).collect()).collect();
                let sol = match unique_solution(&cols, &rhs) {
                    Some(s) => s,
                    None => continue,
                };
                for (&e, val) in free.iter().zip(sol) {
                    y[e] = val;
                }
                if free.iter().any(|&e| y[e].abs() > q(w[e])) {
                    continue;
                }
            } else {
                let mut bad = false;
                for v in 0..nv {
                    let mut s = BigRational::zero();
                    for &e in &pinned {
                        s += y[e].clone() * q(d0[e][v]);
                    }
                    if !s.is_zero() {
                        bad = true;
                    }
                }
                if bad {
                    continue;
                }
            }
            let mut val = BigRational::zero();
            for e in 0..m {
                val += y[e].clone() * q(h[e]);
            }
            if best.as_ref().map_or(true, |b| val > b.0) {
                best = Some((val, y));
            }
        }
    }
    best.expect("the dual polytope contains 0")
}

/// (Phi1, witness string `x=..|y=..`): a primal potential and a dual vector with equal values.
pub fn witness(nv: usize, edges: &[(usize, usize)], w: &[i64], h: &[i64]) -> (BigRational, String) {
    let (phi, x) = phi1_x(nv, edges, w, h);
    let (val, y) = dual_y(nv, edges, w, h);
    assert_eq!(phi, val, "primal and dual values differ");
    let xs: Vec<String> = x.iter().map(fs).collect();
    let ys: Vec<String> = y.iter().map(fs).collect();
    (phi, format!("x={}|y={}", xs.join(","), ys.join(",")))
}

pub fn gamma2(d1: &[Vec<i64>], h: &[i64]) -> BigRational {
    d1.iter().fold(BigRational::zero(), |a, row| {
        let s: i64 = row.iter().zip(h).map(|(x, y)| x * y).sum();
        a + q(s).abs()
    })
}

/// First vertex v with d1 d0 e_v != 0 and the vector over the 2-cells.
pub fn cochain_defect(nv: usize, edges: &[(usize, usize)], d1: &[Vec<i64>]) -> Option<(usize, Vec<i64>)> {
    let d0 = d0_rows(nv, edges);
    for v in 0..nv {
        let vec: Vec<i64> = d1.iter().map(|row| (0..edges.len()).map(|e| row[e] * d0[e][v]).sum()).collect();
        if vec.iter().any(|&x| x != 0) {
            return Some((v, vec));
        }
    }
    None
}

pub fn diag_class(phi: &BigRational, gam: &BigRational) -> &'static str {
    if phi.is_zero() {
        "ExactClass"
    } else if gam.is_zero() {
        "ClosedResidual"
    } else {
        "ActiveClosureFailure"
    }
}

/// Is h in the column space of d0? (rank of the augmented matrix equals rank d0)
fn class_zero(nv: usize, edges: &[(usize, usize)], h: &[i64]) -> bool {
    let d0 = d0_rows(nv, edges);
    let aug: Vec<Vec<i64>> = d0
        .iter()
        .enumerate()
        .map(|(i, row)| {
            let mut r = row.clone();
            r.push(h[i]);
            r
        })
        .collect();
    rank(&aug) == rank(&d0)
}

/// Least c with ||d1 v||_1 <= c ||v||_J: largest column-sum/weight ratio; None when a null-weight edge has a nonzero column.
fn opnorm(d1: &[Vec<i64>], w: &[i64]) -> Option<BigRational> {
    let mut best = BigRational::zero();
    for (e, &we) in w.iter().enumerate() {
        let col: i64 = d1.iter().map(|row| row[e].abs()).sum();
        if we == 0 {
            if col > 0 {
                return None;
            }
        } else {
            let ratio = BigRational::new(BigInt::from(col), BigInt::from(we));
            if ratio > best {
                best = ratio;
            }
        }
    }
    Some(best)
}

fn cell(b: bool) -> String {
    (b as i32).to_string()
}

fn opt_cell(b: Option<bool>) -> String {
    b.map_or("-".to_string(), cell)
}

/// Wire line for one window, identical to the Python `wire_lines` format.
pub fn line(c: &Window) -> String {
    let m = c.edges.len();
    let r0 = rank(&d0_rows(c.nv, &c.edges));
    let r1 = if c.d1.is_empty() { 0 } else { rank(&c.d1) };
    let ok = cochain_defect(c.nv, &c.edges, &c.d1).is_none();
    let (phi, wit) = witness(c.nv, &c.edges, &c.w, &c.h);
    let gam = gamma2(&c.d1, &c.h);
    let zero = class_zero(c.nv, &c.edges, &c.h);
    let dim_h1 = if ok { Some(m - r1 - r0) } else { None };
    let section = dim_h1.map(|d| d * r1);
    let op = opnorm(&c.d1, &c.w);
    let classes = [phi.is_zero(), phi > BigRational::zero() && gam.is_zero(), phi > BigRational::zero() && !gam.is_zero()];
    let hit = classes.iter().filter(|&&x| x).count();
    let diag = if ok { diag_class(&phi, &gam) } else { "NotAWindow" };
    let bound = if ok { op.as_ref().map(|o| gam <= o.clone() * phi.clone()) } else { None };
    let cols: Vec<String> = vec![
        "seq".to_string(),
        c.id.clone(),
        cell(ok),
        m.to_string(),
        r0.to_string(),
        r1.to_string(),
        (m - r0).to_string(),
        dim_h1.map_or("-".to_string(), |d| d.to_string()),
        r1.to_string(),
        opt_cell(if ok { Some(m - r0 == dim_h1.unwrap() + r1) } else { None }),
        section.map_or("-".to_string(), |s| s.to_string()),
        opt_cell(section.map(|s| s == 0)),
        cell(zero),
        cell(c.w.iter().all(|&x| x > 0)),
        fs(&phi),
        if ok { fs(&gam) } else { "-".to_string() },
        diag.to_string(),
        if ok { hit.to_string() } else { "-".to_string() },
        op.as_ref().map_or("-".to_string(), fs),
        opt_cell(bound),
        cell(phi.is_zero() == zero),
        wit,
    ];
    cols.join("\t")
}

/// Replay one tab-separated public-input line `window\tid\tnv\tedges\tw\td1\th`.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "window" {
        return None;
    }
    let c = parse_window(parts)?;
    if c.nv == 0 || c.edges.is_empty() || c.edges.iter().any(|&(s, t)| s >= c.nv || t >= c.nv) || c.d1.iter().any(|r| r.len() != c.edges.len()) || c.w.iter().any(|&x| x < 0) {
        return None;
    }
    Some(line(&c))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_wdp_quotient_sequence_filled_triangle_row() {
        let l = replay("window\tt\t3\t0>1,1>2,0>2\t1,1,1\t1,1,-1\t1,1,0").unwrap();
        assert_eq!(l, "seq\tt\t1\t3\t2\t1\t1\t0\t1\t1\t0\t1\t0\t1\t2\t2\tActiveClosureFailure\t1\t1\t1\t1\tx=-2,-1,0|y=1,1,-1");
    }

    #[test]
    fn pfp_wdp_quotient_sequence_splitting_freedom_and_bound() {
        // two disjoint triangles, one filled: dim H1 = dim im d1 = 1, one-parameter family of sections
        let l = replay("window\tm\t6\t0>1,1>2,0>2,3>4,4>5,3>5\t1,1,1,1,1,1\t1,1,-1,0,0,0\t1,1,0,1,0,0").unwrap();
        let cols: Vec<&str> = l.split('\t').collect();
        assert_eq!((cols[7], cols[8], cols[10], cols[11]), ("1", "1", "1", "0"));
        // the column (1,1,1) has largest entry 1 but J-to-L1 norm 3: the bound is tight, not violated
        let loop3 = replay("window\tl\t1\t0>0\t1\t1;1;1\t1").unwrap();
        let cols: Vec<&str> = loop3.split('\t').collect();
        assert_eq!((cols[14], cols[15], cols[18], cols[19]), ("1", "3", "3", "1"));
    }

    #[test]
    fn pfp_wdp_quotient_sequence_refusal_seminorm_and_malformed() {
        let refused = replay("window\tv\t2\t0>1\t1\t1\t2").unwrap();
        assert_eq!(refused, "seq\tv\t0\t1\t1\t1\t0\t-\t1\t-\t-\t-\t1\t1\t0\t-\tNotAWindow\t-\t1\t-\t1\tx=-2,0|y=0");
        let semi = replay("window\ts\t3\t0>1,1>2,0>2\t0,1,1\t-\t1,0,0").unwrap();
        assert!(semi.contains("\tExactClass\t"));
        let cols: Vec<&str> = semi.split('\t').collect();
        assert_eq!((cols[12], cols[13], cols[20]), ("0", "0", "0"));
        assert!(replay("window\tbad\t2\t0>1\t-1\t-\t1").is_none());
        assert!(replay("seq\tx").is_none());
    }

    #[test]
    fn pfp_wdp_quotient_sequence_weighted_norm_is_column_over_weight() {
        let heavy = replay("window\th\t3\t0>1,1>2,0>2\t3,3,3\t1,1,-1\t1,1,0").unwrap();
        let cols: Vec<&str> = heavy.split('\t').collect();
        assert_eq!((cols[14], cols[15], cols[18]), ("6", "2", "1/3"));
        assert_eq!(opnorm(&[vec![1, 1, -1]], &[3, 3, 3]), Some(BigRational::new(BigInt::from(1), BigInt::from(3))));
        assert_eq!(opnorm(&[vec![1, 1, -1]], &[0, 1, 1]), None);
    }
}
