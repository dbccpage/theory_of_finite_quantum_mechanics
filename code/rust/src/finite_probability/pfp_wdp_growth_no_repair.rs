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

fn side(
    nv: usize,
    edges: &[(usize, usize)],
    w: &[i64],
    d1: &[Vec<i64>],
    h: &[i64],
) -> (bool, BigRational, BigRational, &'static str) {
    let ok = cochain_defect(nv, edges, d1).is_none();
    let phi = phi1(nv, edges, w, h);
    let gam = gamma2(d1, h);
    let cls = if ok { diag_class(&phi, &gam) } else { "NoRule" };
    (ok, phi, gam, cls)
}

fn verdict(kind: &str, ok_b: bool, phi_a: &BigRational, phi_b: &BigRational, gam_a: &BigRational, gam_b: &BigRational) -> &'static str {
    match kind {
        "restrict" => {
            if phi_b <= phi_a {
                "sub_phi_le"
            } else {
                "sub_phi_gt"
            }
        }
        "attach" => {
            if !ok_b {
                "attach_not_a_window"
            } else if phi_b != phi_a {
                "attach_phi_changed"
            } else if gam_b > gam_a {
                "phi_equal_gamma_up"
            } else {
                "phi_equal_gamma_same"
            }
        }
        _ => {
            if phi_b < phi_a {
                "phi_lower"
            } else if phi_b == phi_a {
                "phi_same"
            } else {
                "phi_higher"
            }
        }
    }
}

/// Wire line for one pair, identical to the Python `wire_lines` format.
pub fn line(p: &Pair) -> Option<String> {
    let a = &p.a;
    let (ok_a, phi_a, gam_a, cls_a) = side(a.nv, &a.edges, &a.w, &a.d1, &a.h);
    let (nvb, eb, wb, db, hb) = derive_b(p)?;
    let (ok_b, phi_b, gam_b, cls_b) = side(nvb, &eb, &wb, &db, &hb);
    Some(format!(
        "pair\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        a.id,
        p.kind,
        a.edges.len(),
        eb.len(),
        a.d1.len(),
        db.len(),
        ok_a as i32,
        ok_b as i32,
        fs(&phi_a),
        fs(&phi_b),
        fs(&gam_a),
        fs(&gam_b),
        cls_a,
        cls_b,
        verdict(&p.kind, ok_b, &phi_a, &phi_b, &gam_a, &gam_b)
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
    if a.nv == 0 || a.edges.iter().any(|&(s, t)| s >= a.nv || t >= a.nv) || a.d1.iter().any(|r| r.len() != a.edges.len()) {
        return None;
    }
    let (_, eb, wb, db, hb) = derive_b(&p)?;
    if eb.is_empty() || wb.len() != eb.len() || hb.len() != eb.len() || db.iter().any(|r| r.len() != eb.len()) {
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
        assert_eq!(l, "pair\tt\tattach\t3\t3\t0\t1\t1\t1\t1\t1\t0\t1\tClosedResidual\tActiveClosureFailure\tphi_equal_gamma_up");
    }

    #[test]
    fn pfp_wdp_growth_no_repair_rescaled_weights_obstruction() {
        let tsv = "pair\tp\t2\t0>1,0>1,0>1\t2,2,2\t1,-1,0\t1,-1,0\trestrict\t0,1|3,3";
        let l = replay(tsv).unwrap();
        assert!(l.ends_with("\t4\t6\t2\t2\tActiveClosureFailure\tActiveClosureFailure\tsub_phi_gt"), "{}", l);
        let ok = replay("pair\tp\t2\t0>1,0>1,0>1\t2,2,2\t1,-1,0\t1,-1,0\trestrict\t0,1|-").unwrap();
        assert!(ok.ends_with("\tsub_phi_le"));
    }

    #[test]
    fn pfp_wdp_growth_no_repair_restriction_monotone_on_all_k4_edge_subsets() {
        let edges = "0>1,0>2,0>3,1>2,1>3,2>3";
        let d1 = "1,-1,0,1,0,0;1,0,-1,0,1,0;0,1,-1,0,0,1;0,0,0,1,-1,1";
        let hs = ["1,0,2,1,0,1", "2,-1,0,1,1,-1", "0,0,1,-1,0,0"];
        for h in hs {
            let mut phis_big = None;
            for mask in 1u32..64 {
                let keep: Vec<String> = (0..6).filter(|i| mask & (1 << i) != 0).map(|i| i.to_string()).collect();
                let tsv = format!("pair\tk\t4\t{}\t1,1,1,1,1,1\t{}\t{}\trestrict\t{}|-", edges, d1, h, keep.join(","));
                let l = replay(&tsv).unwrap();
                let cols: Vec<&str> = l.split('\t').collect();
                assert_eq!(cols[15], "sub_phi_le", "{} {}", h, mask);
                phis_big = Some(cols[9].to_string());
            }
            assert!(phis_big.is_some());
        }
    }

    #[test]
    fn pfp_wdp_growth_no_repair_invalid_row_and_malformed_input() {
        let l = replay(&format!("pair\tt\t{}\t-\t1,0,0\tattach\t1,0,0", TRI)).unwrap();
        assert!(l.ends_with("\tNoRule\tattach_not_a_window"));
        assert!(replay("pair\tbad").is_none());
        assert!(replay(&format!("pair\tt\t{}\t-\t1,0,0\trestrict\t7|-", TRI)).is_none());
        assert!(replay("window\tx").is_none());
    }
}
