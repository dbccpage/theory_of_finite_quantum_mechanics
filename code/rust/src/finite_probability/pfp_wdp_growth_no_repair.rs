//! Growth does not repair a quotient residual: restriction, attachment and edits on small graph windows.
//!
//! Exact BigRational replay of `code/python/src/qm/pfp_wdp_growth_no_repair.py` for PFP batch 01, node
//! PG-WDP-GROWTH-NO-REPAIR. Scope: weighted-L1 graph windows with positive integer weights; the operations are
//! restrict (edge subset, optional new weights), attach (2-cell rows), edit_h, edit_w. No other norms, no equal-weight
//! subdivision, no complex coefficients. AuthorityEffect: None.
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

/// A window plus one operation.
pub struct Pair {
    pub a: Window,
    pub kind: String,
    pub arg: String,
}

/// Parse `id nv edges w d1 h kind arg` (the fields after the `pair` token).
pub fn parse_pair<'a>(parts: impl Iterator<Item = &'a str>) -> Option<Pair> {
    let fields: Vec<&str> = parts.collect();
    if fields.len() != 8 {
        return None;
    }
    let a = parse_window(fields[..6].iter().copied())?;
    Some(Pair { a, kind: fields[6].to_string(), arg: fields[7].to_string() })
}

/// The second window of a pair: (nv, edges, w, d1, h).
pub fn derive_b(p: &Pair) -> Option<(usize, Vec<(usize, usize)>, Vec<i64>, Vec<Vec<i64>>, Vec<i64>)> {
    let a = &p.a;
    match p.kind.as_str() {
        "restrict" => {
            let (keep_s, neww) = p.arg.split_once('|')?;
            let keep: Vec<usize> = keep_s.split(',').map(|x| x.parse().ok()).collect::<Option<Vec<_>>>()?;
            if keep.iter().any(|&i| i >= a.edges.len()) {
                return None;
            }
            let rows: Vec<Vec<i64>> = a
                .d1
                .iter()
                .filter(|row| (0..a.edges.len()).all(|e| keep.contains(&e) || row[e] == 0))
                .map(|row| keep.iter().map(|&i| row[i]).collect())
                .collect();
            let wb = if neww == "-" { keep.iter().map(|&i| a.w[i]).collect() } else { ints(neww)? };
            Some((a.nv, keep.iter().map(|&i| a.edges[i]).collect(), wb, rows, keep.iter().map(|&i| a.h[i]).collect()))
        }
        "attach" => {
            let mut d1 = a.d1.clone();
            for r in p.arg.split(';') {
                d1.push(ints(r)?);
            }
            Some((a.nv, a.edges.clone(), a.w.clone(), d1, a.h.clone()))
        }
        "edit_h" => Some((a.nv, a.edges.clone(), a.w.clone(), a.d1.clone(), ints(&p.arg)?)),
        "edit_w" => Some((a.nv, a.edges.clone(), ints(&p.arg)?, a.d1.clone(), a.h.clone())),
        _ => None,
    }
}

struct Side {
    ok: bool,
    phi: BigRational,
    gam: Option<BigRational>,
    cls: &'static str,
    wit: String,
}

fn side(nv: usize, edges: &[(usize, usize)], w: &[i64], d1: &[Vec<i64>], h: &[i64]) -> Side {
    let ok = cochain_defect(nv, edges, d1).is_none();
    let (phi, wit) = witness(nv, edges, w, h);
    let gam = gamma2(d1, h);
    let cls = if ok { diag_class(&phi, &gam) } else { "NotAWindow" };
    Side { ok, phi, gam: if ok { Some(gam) } else { None }, cls, wit }
}

fn verdict(kind: &str, b: &Side, a: &Side) -> &'static str {
    match kind {
        "restrict" => {
            if b.phi <= a.phi {
                "sub_phi_le"
            } else {
                "sub_phi_gt"
            }
        }
        "attach" => {
            if !b.ok {
                "attach_not_a_window"
            } else if b.phi != a.phi {
                "attach_phi_changed"
            } else if b.gam > a.gam {
                "phi_equal_gamma_up"
            } else {
                "phi_equal_gamma_same"
            }
        }
        _ => {
            if b.phi < a.phi {
                "phi_lower"
            } else if b.phi == a.phi {
                "phi_same"
            } else {
                "phi_higher"
            }
        }
    }
}

fn opt_fs(x: &Option<BigRational>) -> String {
    x.as_ref().map_or("-".to_string(), fs)
}

/// Wire line for one pair, identical to the Python `wire_lines` format.
pub fn line(p: &Pair) -> Option<String> {
    let a = &p.a;
    let sa = side(a.nv, &a.edges, &a.w, &a.d1, &a.h);
    let (nvb, eb, wb, db, hb) = derive_b(p)?;
    let sb = side(nvb, &eb, &wb, &db, &hb);
    Some(format!(
        "pair\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        a.id,
        p.kind,
        a.edges.len(),
        eb.len(),
        a.d1.len(),
        db.len(),
        sa.ok as i32,
        sb.ok as i32,
        fs(&sa.phi),
        fs(&sb.phi),
        opt_fs(&sa.gam),
        opt_fs(&sb.gam),
        sa.cls,
        sb.cls,
        verdict(&p.kind, &sb, &sa),
        sa.wit,
        sb.wit
    ))
}

/// Replay one tab-separated public-input line `pair\tid\tnv\tedges\tw\td1\th\tkind\targ`.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "pair" {
        return None;
    }
    let p = parse_pair(parts)?;
    let a = &p.a;
    if a.nv == 0 || a.edges.iter().any(|&(s, t)| s >= a.nv || t >= a.nv) || a.d1.iter().any(|r| r.len() != a.edges.len()) || a.w.iter().any(|&x| x <= 0) {
        return None;
    }
    let (_, eb, wb, db, hb) = derive_b(&p)?;
    if eb.is_empty() || wb.len() != eb.len() || hb.len() != eb.len() || db.iter().any(|r| r.len() != eb.len()) || wb.iter().any(|&x| x <= 0) {
        return None;
    }
    line(&p)
}

#[cfg(test)]
mod tests {
    use super::*;

    const TRI: &str = "3\t0>1,1>2,0>2\t1,1,1";

    #[test]
    fn pfp_wdp_growth_no_repair_attachment_keeps_phi1_and_raises_gamma2() {
        let l = replay(&format!("pair\tt\t{}\t-\t1,0,0\tattach\t1,1,-1", TRI)).unwrap();
        assert_eq!(
            l,
            "pair\tt\tattach\t3\t3\t0\t1\t1\t1\t1\t1\t0\t1\tClosedResidual\tActiveClosureFailure\tphi_equal_gamma_up\tx=-1,0,0|y=1,1,-1\tx=-1,0,0|y=1,1,-1"
        );
    }

    #[test]
    fn pfp_wdp_growth_no_repair_rescaled_weights_obstruction() {
        let tsv = "pair\tp\t2\t0>1,0>1,0>1\t2,2,2\t1,-1,0\t1,-1,0\trestrict\t0,1|3,3";
        let l = replay(tsv).unwrap();
        assert!(l.contains("\t4\t6\t2\t2\tActiveClosureFailure\tActiveClosureFailure\tsub_phi_gt\t"), "{}", l);
        let ok = replay("pair\tp\t2\t0>1,0>1,0>1\t2,2,2\t1,-1,0\t1,-1,0\trestrict\t0,1|-").unwrap();
        assert!(ok.contains("\tsub_phi_le\t"));
    }

    #[test]
    fn pfp_wdp_growth_no_repair_restriction_monotone_on_all_k4_edge_subsets() {
        let edges = "0>1,0>2,0>3,1>2,1>3,2>3";
        let d1 = "1,-1,0,1,0,0;1,0,-1,0,1,0;0,1,-1,0,0,1;0,0,0,1,-1,1";
        let hs = ["1,0,2,1,0,1", "2,-1,0,1,1,-1", "0,0,1,-1,0,0"];
        for h in hs {
            for mask in 1u32..64 {
                let keep: Vec<String> = (0..6).filter(|i| mask & (1 << i) != 0).map(|i| i.to_string()).collect();
                let tsv = format!("pair\tk\t4\t{}\t1,1,1,1,1,1\t{}\t{}\trestrict\t{}|-", edges, d1, h, keep.join(","));
                let l = replay(&tsv).unwrap();
                let cols: Vec<&str> = l.split('\t').collect();
                assert_eq!(cols[15], "sub_phi_le", "{} {}", h, mask);
            }
        }
    }

    #[test]
    fn pfp_wdp_growth_no_repair_invalid_row_and_malformed_input() {
        let l = replay(&format!("pair\tt\t{}\t-\t1,0,0\tattach\t1,0,0", TRI)).unwrap();
        let cols: Vec<&str> = l.split('\t').collect();
        assert_eq!((cols[12], cols[14], cols[15]), ("-", "NotAWindow", "attach_not_a_window"));
        assert!(replay("pair\tbad").is_none());
        assert!(replay(&format!("pair\tt\t{}\t-\t1,0,0\trestrict\t7|-", TRI)).is_none());
        assert!(replay("window\tx").is_none());
    }
}
