//! The degree-1 window (C0, C1, C2, d0, d1) with a weighted-L1 norm J: invariants and diagnostic classes.
//!
//! Exact BigRational replay of `code/python/src/qm/pfp_wdp_degree1_window.py` for PFP batch 01, node
//! PG-WDP-DEGREE1-WINDOW. Scope: graph windows with positive integer weights, integer d1 rows and an integer
//! 1-cochain; Phi1 by vertex enumeration of the repair arrangement. No complex coefficients, no other norms,
//! no derivation of the window. AuthorityEffect: None.
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

/// Quotient defect: attained minimum of sum_e w_e |h_e - (d0 x)_e| over potentials x.
pub fn phi1(nv: usize, edges: &[(usize, usize)], w: &[i64], h: &[i64]) -> BigRational {
    let d0 = d0_rows(nv, edges);
    let m = d0.len();
    let r = rank(&d0);
    if r == 0 {
        return (0..m).fold(BigRational::zero(), |a, i| a + q(w[i]) * q(h[i]).abs());
    }
    let mut best: Option<BigRational> = None;
    for sub in combos(m, r) {
        let rows: Vec<Vec<i64>> = sub.iter().map(|&i| d0[i].clone()).collect();
        let rhs: Vec<i64> = sub.iter().map(|&i| h[i]).collect();
        let x = match solve_rows(&rows, &rhs) {
            Some(x) => x,
            None => continue,
        };
        let mut cost = BigRational::zero();
        for i in 0..m {
            let mut dx = BigRational::zero();
            for j in 0..nv {
                dx += q(d0[i][j]) * x[j].clone();
            }
            cost += q(w[i]) * (q(h[i]) - dx).abs();
        }
        if best.as_ref().map_or(true, |b| cost < *b) {
            best = Some(cost);
        }
    }
    best.expect("a vertex exists when rank > 0")
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

/// Wire line for one window, identical to the Python `wire_lines` format.
pub fn line(c: &Window) -> String {
    let d0 = d0_rows(c.nv, &c.edges);
    let m = c.edges.len();
    let r0 = rank(&d0);
    let r1 = if c.d1.is_empty() { 0 } else { rank(&c.d1) };
    let witness = cochain_defect(c.nv, &c.edges, &c.d1);
    let ok = witness.is_none();
    let phi = phi1(c.nv, &c.edges, &c.w, &c.h);
    let gam = gamma2(&c.d1, &c.h);
    let dim_h1 = if ok { (m - r1 - r0).to_string() } else { "-".to_string() };
    let r_cl = if ok && phi > BigRational::zero() { fs(&(gam.clone() / phi.clone())) } else { "-".to_string() };
    let diag = if ok { diag_class(&phi, &gam) } else { "NoRule" };
    let wit = match &witness {
        None => "-".to_string(),
        Some((v, vec)) => format!("{}:{}", v, vec.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",")),
    };
    format!(
        "window\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        c.id,
        c.nv,
        m,
        c.d1.len(),
        r0,
        r1,
        ok as i32,
        m - r0,
        dim_h1,
        fs(&phi),
        fs(&gam),
        r_cl,
        diag,
        wit
    )
}

/// Replay one tab-separated public-input line `window\tid\tnv\tedges\tw\td1\th`.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "window" {
        return None;
    }
    let c = parse_window(parts)?;
    if c.nv == 0 || c.edges.iter().any(|&(s, t)| s >= c.nv || t >= c.nv) || c.d1.iter().any(|r| r.len() != c.edges.len()) {
        return None;
    }
    Some(line(&c))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn win(s: &str) -> Window {
        parse_window(s.split('\t')).unwrap()
    }

    #[test]
    fn pfp_wdp_degree1_window_filled_triangle_signature() {
        let l = replay("window\tt\t3\t0>1,1>2,0>2\t1,1,1\t1,1,-1\t1,1,0").unwrap();
        assert_eq!(l, "window\tt\t3\t3\t1\t2\t1\t1\t1\t0\t2\t2\t1\tActiveClosureFailure\t-");
    }

    #[test]
    fn pfp_wdp_degree1_window_three_classes_and_refusal() {
        let exact = replay("window\ta\t3\t0>1,1>2,0>2\t1,1,1\t1,1,-1\t1,2,3").unwrap();
        assert!(exact.contains("\tExactClass\t"));
        let closed = replay("window\tb\t3\t0>1,1>2,0>2\t1,1,1\t-\t1,0,0").unwrap();
        assert!(closed.contains("\tClosedResidual\t"));
        let refused = replay("window\tc\t2\t0>1\t1\t1\t2").unwrap();
        assert!(refused.ends_with("\tNoRule\t0:-1"));
    }

    #[test]
    fn pfp_wdp_degree1_window_phi1_matches_lattice_search() {
        let c = win("k\t4\t0>1,0>2,0>3,1>2,1>3,2>3\t1,1,1,1,1,1\t1,-1,0,1,0,0;1,0,-1,0,1,0;0,1,-1,0,0,1\t1,0,2,1,0,1");
        let d0 = d0_rows(c.nv, &c.edges);
        let mut best: Option<i64> = None;
        for a in -4i64..=4 {
            for b in -4i64..=4 {
                for d in -4i64..=4 {
                    let x = [0, a, b, d];
                    let cost: i64 = (0..6)
                        .map(|i| (c.h[i] - (0..4).map(|j| d0[i][j] * x[j]).sum::<i64>()).abs() * c.w[i])
                        .sum();
                    best = Some(best.map_or(cost, |v: i64| v.min(cost)));
                }
            }
        }
        assert_eq!(best.unwrap(), 3);
        assert_eq!(phi1(c.nv, &c.edges, &c.w, &c.h), q(3));
    }

    #[test]
    fn pfp_wdp_degree1_window_loop_and_rejects_malformed() {
        let l = replay("window\tl\t1\t0>0\t1\t1\t3").unwrap();
        assert!(l.contains("\t3\t3\t1\tActiveClosureFailure\t"));
        assert!(replay("window\tbad\t2\t0>5\t1\t-\t1").is_none());
        assert!(replay("other\tx").is_none());
    }
}
