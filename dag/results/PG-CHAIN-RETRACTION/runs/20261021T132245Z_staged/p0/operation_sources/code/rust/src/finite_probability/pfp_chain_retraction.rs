//! Chain retractions over Q: homology of a subcomplex inclusion and the existence of a retraction.
//!
//! Exact replay of `code/python/src/qm/pfp_chain_retraction.py` (wire line only) for PFP batch 01, node
//! PG-CHAIN-RETRACTION. A case is a finite free chain complex D over Q (basis sizes, integer boundary matrices
//! d_k : D_k -> D_{k-1}) and a set of basis vectors per degree spanning a candidate subcomplex C. Reports closedness,
//! dimensions, Betti numbers, rank H_k(i) (via dim ker H_k(i) = rank d_{k+1}^D - rank E_k - rank d_{k+1}^C) and the rank
//! and augmented rank of the linear system "r restricted to C is the identity, d r = r d". Exact rationals only;
//! nothing about Z, torsion or infinite complexes. AuthorityEffect: None.
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;
use std::collections::BTreeMap;

type Q = BigRational;

fn q(x: i64) -> Q {
    Q::from_integer(BigInt::from(x))
}

fn rank(rows: &[Vec<Q>], ncols: usize) -> usize {
    let mut m: Vec<Vec<Q>> = rows.to_vec();
    let mut r = 0;
    for c in 0..ncols {
        let piv = match (r..m.len()).find(|&i| !m[i][c].is_zero()) {
            Some(p) => p,
            None => continue,
        };
        m.swap(r, piv);
        for i in (r + 1)..m.len() {
            if !m[i][c].is_zero() {
                let f = &m[i][c] / &m[r][c];
                for j in 0..m[i].len() {
                    let t = &f * &m[r][j];
                    let v = &m[i][j] - t;
                    m[i][j] = v;
                }
            }
        }
        r += 1;
    }
    r
}

fn irank(mat: &[Vec<i64>], ncols: usize) -> usize {
    let rows: Vec<Vec<Q>> = mat.iter().map(|r| r.iter().map(|x| q(*x)).collect()).collect();
    rank(&rows, ncols)
}

struct Cx {
    dims: Vec<usize>,
    mats: Vec<Vec<Vec<i64>>>, // mats[k-1] = d_k, rows indexed by D_{k-1}, columns by D_k
}

impl Cx {
    fn n(&self) -> usize {
        self.dims.len() - 1
    }
    fn rk(&self, k: usize) -> usize {
        if k >= 1 && k <= self.n() {
            irank(&self.mats[k - 1], self.dims[k])
        } else {
            0
        }
    }
    fn betti(&self) -> Vec<i64> {
        (0..=self.n())
            .map(|k| self.dims[k] as i64 - self.rk(k) as i64 - self.rk(k + 1) as i64)
            .collect()
    }
}

fn parse(dims_s: &str, mats_s: &str, sub_s: &str) -> Option<(Cx, Vec<Vec<usize>>)> {
    let dims: Vec<usize> = dims_s.split(',').map(|x| x.parse().ok()).collect::<Option<_>>()?;
    let n = dims.len() - 1;
    let mut mats = Vec::new();
    if n > 0 {
        let parts: Vec<&str> = mats_s.split(';').collect();
        if parts.len() != n {
            return None;
        }
        for (i, part) in parts.iter().enumerate() {
            let k = i + 1;
            let rows: Vec<Vec<i64>> = part
                .split('/')
                .map(|row| row.split(',').map(|x| x.parse().ok()).collect::<Option<Vec<i64>>>())
                .collect::<Option<_>>()?;
            if rows.len() != dims[k - 1] || rows.iter().any(|r| r.len() != dims[k]) {
                return None;
            }
            mats.push(rows);
        }
    }
    for k in 2..=n {
        for i in 0..dims[k - 2] {
            for j in 0..dims[k] {
                let s: i64 = (0..dims[k - 1]).map(|t| mats[k - 2][i][t] * mats[k - 1][t][j]).sum();
                if s != 0 {
                    return None;
                }
            }
        }
    }
    let mut subs = Vec::new();
    for (k, part) in sub_s.split(';').enumerate() {
        let s: Vec<usize> = if part == "-" {
            Vec::new()
        } else {
            part.split('.').map(|x| x.parse().ok()).collect::<Option<_>>()?
        };
        if k > n || s.windows(2).any(|w| w[0] >= w[1]) || s.iter().any(|i| *i >= dims[k]) {
            return None;
        }
        subs.push(s);
    }
    if subs.len() != n + 1 {
        return None;
    }
    Some((Cx { dims, mats }, subs))
}

fn lst<T: ToString>(v: &[T]) -> String {
    if v.is_empty() {
        "-".to_string()
    } else {
        v.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",")
    }
}

/// Wire line for one case, identical to the Python `wire_lines` format.
pub fn line(name: &str, dims_s: &str, mats_s: &str, sub_s: &str) -> Option<String> {
    let (d, subs) = parse(dims_s, mats_s, sub_s)?;
    let n = d.n();
    let dims_d: Vec<usize> = d.dims.clone();
    let closed = (1..=n).all(|k| {
        subs[k].iter().all(|j| (0..d.dims[k - 1]).filter(|i| !subs[k - 1].contains(i)).all(|i| d.mats[k - 1][i][*j] == 0))
    });
    if !closed {
        return Some(format!("chain\t{}\t0\t{}\t-\t-\t-\t-\t-1\t0\t0\t-1\t-1", name, lst(&dims_d)));
    }
    let dims_c: Vec<usize> = subs.iter().map(|s| s.len()).collect();
    let mats_c: Vec<Vec<Vec<i64>>> = (1..=n)
        .map(|k| subs[k - 1].iter().map(|a| subs[k].iter().map(|c| d.mats[k - 1][*a][*c]).collect()).collect())
        .collect();
    let cc = Cx { dims: dims_c.clone(), mats: mats_c };
    let (b_c, b_d) = (cc.betti(), d.betti());
    let mut kernel = Vec::new();
    for k in 0..=n {
        if k == n {
            kernel.push(0i64);
            continue;
        }
        let rows_out: Vec<Vec<i64>> = d.mats[k].iter().enumerate().filter(|(i, _)| !subs[k].contains(i)).map(|(_, r)| r.clone()).collect();
        let e = if rows_out.is_empty() { 0 } else { irank(&rows_out, d.dims[k + 1]) };
        kernel.push(d.rk(k + 1) as i64 - e as i64 - cc.rk(k + 1) as i64);
    }
    let rank_hi: Vec<i64> = b_c.iter().zip(kernel.iter()).map(|(b, z)| b - z).collect();
    let killed: i64 = kernel.iter().sum();
    // linear system for the retraction r : D -> C
    let mut index: BTreeMap<(usize, usize, usize), usize> = BTreeMap::new();
    for k in 0..=n {
        for c in 0..subs[k].len() {
            for b in 0..d.dims[k] {
                if !subs[k].contains(&b) {
                    let id = index.len();
                    index.insert((k, c, b), id);
                }
            }
        }
    }
    let nv = index.len();
    let form = |k: usize, c: usize, b: usize| -> (Vec<Q>, Q) {
        let mut coef = vec![q(0); nv];
        if subs[k].contains(&b) {
            return (coef, q(if subs[k][c] == b { 1 } else { 0 }));
        }
        coef[index[&(k, c, b)]] = q(1);
        (coef, q(0))
    };
    let mut rows: Vec<Vec<Q>> = Vec::new();
    for k in 1..=n {
        let dd = &d.mats[k - 1];
        for a in 0..subs[k - 1].len() {
            for b in 0..d.dims[k] {
                let mut coef = vec![q(0); nv];
                let mut cst = q(0);
                for c in 0..subs[k].len() {
                    let w = q(dd[subs[k - 1][a]][subs[k][c]]);
                    let (cf, cs) = form(k, c, b);
                    for i in 0..nv {
                        coef[i] = &coef[i] + &w * &cf[i];
                    }
                    cst = &cst + &w * &cs;
                }
                for e in 0..d.dims[k - 1] {
                    let w = q(dd[e][b]);
                    let (cf, cs) = form(k - 1, a, e);
                    for i in 0..nv {
                        coef[i] = &coef[i] - &w * &cf[i];
                    }
                    cst = &cst - &w * &cs;
                }
                let mut row = coef;
                row.push(-cst);
                rows.push(row);
            }
        }
    }
    let plain_rows: Vec<Vec<Q>> = rows.iter().map(|r| r[..nv].to_vec()).collect();
    let plain = if nv == 0 { 0 } else { rank(&plain_rows, nv) };
    let aug = rank(&rows, nv + 1);
    Some(format!(
        "chain\t{}\t1\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        name,
        lst(&dims_d),
        lst(&dims_c),
        lst(&b_c),
        lst(&b_d),
        lst(&rank_hi),
        killed,
        (killed == 0) as u8,
        (plain == aug) as u8,
        plain,
        aug
    ))
}

/// Replay one tab-separated public-input line `cx\tname\tdims\tmatrices\tsubcomplex`.
pub fn replay(input: &str) -> Option<String> {
    let p: Vec<&str> = input.split('\t').collect();
    if p.len() != 5 || p[0] != "cx" {
        return None;
    }
    line(p[1], p[2], p[3], p[4])
}

#[cfg(test)]
mod tests {
    use super::*;

    const EDGE: &str = "-1/1";

    #[test]
    fn pfp_chain_retraction_two_isolated_points_have_no_retraction() {
        assert_eq!(
            line("p", "2,1", EDGE, "0.1;-").unwrap(),
            "chain\tp\t1\t2,1\t2,0\t2,0\t1,0\t1,0\t1\t0\t0\t0\t1"
        );
    }

    #[test]
    fn pfp_chain_retraction_point_in_edge_retracts() {
        assert_eq!(
            line("q", "2,1", EDGE, "0;-").unwrap(),
            "chain\tq\t1\t2,1\t1,0\t1,0\t1,0\t1,0\t0\t1\t1\t1\t1"
        );
    }

    #[test]
    fn pfp_chain_retraction_triangle_with_face_kills_the_cycle() {
        let l = line("t", "3,3,1", "-1,0,-1/1,-1,0/0,1,1;1/1/-1", "0.1.2;0.1.2;-").unwrap();
        assert_eq!(l, "chain\tt\t1\t3,3,1\t3,3,0\t1,1,0\t1,0,0\t1,0,0\t1\t0\t0\t0\t1");
    }

    #[test]
    fn pfp_chain_retraction_non_subcomplex_is_refused() {
        let l = line("n", "3,3,1", "-1,0,-1/1,-1,0/0,1,1;1/1/-1", "0;0;-").unwrap();
        assert_eq!(l, "chain\tn\t0\t3,3,1\t-\t-\t-\t-\t-1\t0\t0\t-1\t-1");
        assert!(replay("cx\tn\t2,1\t1,1/1\t0;-").is_none());
        assert!(replay("cx\tn\t2,1").is_none());
    }

    const TET: &str = "4,6,4,1";
    const TET_D: &str = "-1,-1,-1,0,0,0/1,0,0,-1,-1,0/0,1,0,1,0,-1/0,0,1,0,1,1;1,1,0,0/-1,0,1,0/0,-1,-1,0/1,0,0,1/0,1,0,-1/0,0,1,1;-1/1/-1/1";

    #[test]
    fn pfp_chain_retraction_tetrahedron_surface_class_is_killed_by_the_solid() {
        // hollow tetrahedron (H2 = Z) inside the solid: the degree-2 class dies, no retraction
        assert_eq!(
            line("h", TET, TET_D, "0.1.2.3;0.1.2.3.4.5;0.1.2.3;-").unwrap(),
            "chain	h	1	4,6,4,1	4,6,4,0	1,0,1,0	1,0,0,0	1,0,0,0	1	0	0	0	1"
        );
    }

    #[test]
    fn pfp_chain_retraction_contractible_subcomplex_retracts() {
        // filled face inside the solid tetrahedron: contractible, the homology map is injective and a retraction exists
        assert_eq!(
            line("f", TET, TET_D, "0.1.2;0.1.3;0;-").unwrap(),
            "chain	f	1	4,6,4,1	3,3,1,0	1,0,0,0	1,0,0,0	1,0,0,0	0	1	1	10	10"
        );
    }
}
