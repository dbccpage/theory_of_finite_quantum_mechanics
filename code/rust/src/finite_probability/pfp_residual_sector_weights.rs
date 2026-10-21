//! L1 residual minimizers on the n-cycle and the (non-)determination of sector weights.
//!
//! Exact integer replay of `code/python/src/qm/pfp_residual_sector_weights.py` for PFP batch 01, node
//! L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED. Record kinds: `residual` (equal edge masses: class = holonomy `S`, `Phi1 = |S|`,
//! minimizers = sign-definite cochains with sum `S`), `weighted` (declared integer masses: minimizers live on the
//! minimal-mass edges) and `twocycle` (two disjoint cycles). Gamma2 is modelled as the holonomy. Sector weights are block
//! sums of `|r_i|`. No Hilbert-lift or physical claim. AuthorityEffect: None.

use std::collections::BTreeSet;

fn gcd(a: u128, b: u128) -> u128 {
    if b == 0 {
        a
    } else {
        gcd(b, a % b)
    }
}

/// Binomial coefficient C(top, k) in exact u128 arithmetic.
fn comb(top: u128, k: u128) -> u128 {
    let mut result: u128 = 1;
    for i in 1..=k {
        result = result * (top - k + i) / i;
    }
    result
}

/// All tuples of `parts` nonnegative integers summing to `total`, in ascending lexicographic order.
fn weak_compositions(total: i64, parts: usize) -> Vec<Vec<i64>> {
    if parts == 1 {
        return vec![vec![total]];
    }
    let mut out = Vec::new();
    for first in 0..=total {
        for rest in weak_compositions(total - first, parts - 1) {
            let mut v = vec![first];
            v.extend(rest);
            out.push(v);
        }
    }
    out
}

fn ints(xs: &[i64]) -> String {
    xs.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",")
}

fn parse_list(s: &str) -> Option<Vec<i64>> {
    s.split(',').map(|t| t.parse::<i64>().ok()).collect()
}

fn vec_text(vecs: &[Vec<i64>]) -> String {
    vecs.iter().map(|v| ints(v)).collect::<Vec<_>>().join(";")
}

fn valid_sizes(n: usize, sizes: &[i64]) -> bool {
    !sizes.is_empty() && sizes.iter().all(|&s| s >= 1) && sizes.iter().sum::<i64>() == n as i64
}

/// Wire line for one unweighted (n, c, sector sizes) case.
pub fn line(n: usize, c: &[i64], sizes: &[i64]) -> Option<String> {
    if n == 0 || c.len() != n || !valid_sizes(n, sizes) {
        return None;
    }
    let s: i64 = c.iter().sum();
    let m = s.abs();
    let (lex_min, lex_max): (Vec<i64>, Vec<i64>) = if s >= 0 {
        let mut a = vec![0; n - 1];
        a.push(m);
        let mut b = vec![m];
        b.extend(vec![0; n - 1]);
        (a, b)
    } else {
        let mut a = vec![-m];
        a.extend(vec![0; n - 1]);
        let mut b = vec![0; n - 1];
        b.push(-m);
        (a, b)
    };
    let vecs = weak_compositions(m, sizes.len());
    let count = comb(m as u128 + n as u128 - 1, n as u128 - 1);
    let g = gcd(m as u128, n as u128);
    let (num, den) = (m as u128 / g, n as u128 / g);
    let (q, r) = (m / n as i64, m % n as i64);
    let sumsq_min = r * (q + 1) * (q + 1) + (n as i64 - r) * q * q;
    Some(format!(
        "residual\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}/{}\t{}\t{}\t{}\t{}",
        n,
        ints(c),
        ints(sizes),
        s,
        m,
        count,
        ints(&lex_min),
        ints(&lex_max),
        vec_text(&vecs),
        (vecs.len() == 1) as i32,
        (count == 1) as i32,
        num,
        den,
        (den == 1) as i32,
        sumsq_min,
        m * m,
        if m == 0 { "zero_mass_refused" } else { "ok" }
    ))
}

/// Wire line for one weighted (n, c, sector sizes, masses) case.
pub fn line_weighted(n: usize, c: &[i64], sizes: &[i64], masses: &[i64]) -> Option<String> {
    if n == 0 || c.len() != n || masses.len() != n || masses.iter().any(|&x| x < 1) || !valid_sizes(n, sizes) {
        return None;
    }
    let s: i64 = c.iter().sum();
    let m = s.abs();
    let mmin = *masses.iter().min().unwrap();
    let e: Vec<usize> = (0..n).filter(|&i| masses[i] == mmin).collect();
    let k = e.len();
    let sign = if s >= 0 { 1 } else { -1 };
    let (lo, hi) = if s >= 0 { (e[k - 1], e[0]) } else { (e[0], e[k - 1]) };
    let lex_min: Vec<i64> = (0..n).map(|i| if i == lo { sign * m } else { 0 }).collect();
    let lex_max: Vec<i64> = (0..n).map(|i| if i == hi { sign * m } else { 0 }).collect();
    let mut cuts = Vec::new();
    let mut acc = 0usize;
    for &sz in sizes {
        cuts.push((acc, acc + sz as usize));
        acc += sz as usize;
    }
    let mut set: BTreeSet<Vec<i64>> = BTreeSet::new();
    for comp in weak_compositions(m, k) {
        let mut w = vec![0i64; n];
        for (pos, val) in e.iter().zip(comp.iter()) {
            w[*pos] = *val;
        }
        set.insert(cuts.iter().map(|&(a, b)| w[a..b].iter().sum()).collect());
    }
    let vecs: Vec<Vec<i64>> = set.into_iter().collect();
    let count = comb(m as u128 + k as u128 - 1, k as u128 - 1);
    Some(format!(
        "weighted\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        n,
        ints(c),
        ints(sizes),
        ints(masses),
        s,
        m * mmin,
        count,
        ints(&lex_min),
        ints(&lex_max),
        vec_text(&vecs),
        (vecs.len() == 1) as i32,
        (count == 1) as i32,
        if m == 0 { "zero_mass_refused" } else { "ok" }
    ))
}

/// Wire line for two disjoint cycles.
pub fn line_twocycle(n1: usize, c1: &[i64], n2: usize, c2: &[i64]) -> Option<String> {
    if n1 == 0 || n2 == 0 || c1.len() != n1 || c2.len() != n2 {
        return None;
    }
    let (s1, s2): (i64, i64) = (c1.iter().sum(), c2.iter().sum());
    let phi1 = s1.abs() + s2.abs();
    let count = comb(s1.unsigned_abs() as u128 + n1 as u128 - 1, n1 as u128 - 1) * comb(s2.unsigned_abs() as u128 + n2 as u128 - 1, n2 as u128 - 1);
    Some(format!(
        "twocycle\t{}\t{}\t{}\t{}\t{},{}\t{}\t{}\t{}\t{}",
        n1,
        ints(c1),
        n2,
        ints(c2),
        s1,
        s2,
        phi1,
        count,
        s1 + s2,
        ((s1 + s2).abs() == phi1) as i32
    ))
}

/// Replay one tab-separated public-input line.
pub fn replay(input: &str) -> Option<String> {
    let p: Vec<&str> = input.split('\t').collect();
    match *p.first()? {
        "residual" if p.len() == 4 => line(p[1].parse().ok()?, &parse_list(p[2])?, &parse_list(p[3])?),
        "weighted" if p.len() == 5 => line_weighted(p[1].parse().ok()?, &parse_list(p[2])?, &parse_list(p[3])?, &parse_list(p[4])?),
        "twocycle" if p.len() == 5 => line_twocycle(p[1].parse().ok()?, &parse_list(p[2])?, p[3].parse().ok()?, &parse_list(p[4])?),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_residual_sector_weights_c4_orbit_sum_case_matches_python_wire() {
        assert_eq!(
            replay("residual\t4\t1,0,1,0\t2,2").unwrap(),
            "residual\t4\t1,0,1,0\t2,2\t2\t2\t10\t0,0,0,2\t2,0,0,0\t0,2;1,1;2,0\t0\t0\t1/2\t0\t2\t4\tok"
        );
    }

    #[test]
    fn pfp_residual_sector_weights_zero_mass_single_edge_and_single_sector_boundaries() {
        let z = replay("residual\t4\t1,-1,0,0\t2,2").unwrap();
        assert!(z.ends_with("\t0\t0\t1\t0,0,0,0\t0,0,0,0\t0,0\t1\t1\t0/1\t1\t0\t0\tzero_mass_refused"));
        let one = replay("residual\t1\t5\t1").unwrap();
        assert_eq!(one.split('\t').nth(6), Some("1"));
        assert_eq!(one.split('\t').nth(11), Some("1"));
        let single = replay("residual\t4\t1,1,0,0\t4").unwrap();
        assert_eq!(single.split('\t').nth(10), Some("1"));
        assert_eq!(single.split('\t').nth(11), Some("0"));
    }

    #[test]
    fn pfp_residual_sector_weights_minimizer_count_is_the_composition_count() {
        for n in 1..7usize {
            for s in -9i64..10 {
                let mut c = vec![0; n];
                c[0] = s;
                let l = line(n, &c, &[n as i64]).unwrap();
                let cols: Vec<&str> = l.split('\t').collect();
                let m = s.abs() as u128;
                assert_eq!(cols[6].parse::<u128>().unwrap(), comb(m + n as u128 - 1, n as u128 - 1));
                assert_eq!(cols[9], format!("{}", m));
            }
        }
        assert_eq!(comb(7, 3), 35);
    }

    #[test]
    fn pfp_residual_sector_weights_negative_class_and_symmetric_fraction() {
        let l = replay("residual\t4\t-2,0,-1,0\t2,2").unwrap();
        let cols: Vec<&str> = l.split('\t').collect();
        assert_eq!((cols[4], cols[5], cols[7], cols[8]), ("-3", "3", "-3,0,0,0", "0,0,0,-3"));
        assert_eq!(cols[12], "3/4");
        let l6 = replay("residual\t6\t1,0,0,0,0,0\t3,3").unwrap();
        assert_eq!(l6.split('\t').nth(12), Some("1/6"));
        assert_eq!(l6.split('\t').nth(13), Some("0"));
    }

    #[test]
    fn pfp_residual_sector_weights_weighted_minimizer_lives_on_minimal_mass_edges() {
        assert_eq!(
            replay("weighted\t4\t1,0,1,0\t2,2\t1,2,3,4").unwrap(),
            "weighted\t4\t1,0,1,0\t2,2\t1,2,3,4\t2\t2\t1\t2,0,0,0\t2,0,0,0\t2,0\t1\t1\tok"
        );
        assert_eq!(
            replay("weighted\t4\t3,0,0,0\t2,2\t2,2,1,1").unwrap(),
            "weighted\t4\t3,0,0,0\t2,2\t2,2,1,1\t3\t3\t4\t0,0,0,3\t0,0,3,0\t0,3\t1\t0\tok"
        );
        let eq = replay("weighted\t4\t1,0,1,0\t2,2\t1,1,1,1").unwrap();
        assert_eq!(eq.split('\t').nth(7), Some("10"));
        assert_eq!(eq.split('\t').nth(10), Some("0,2;1,1;2,0"));
        let neg = replay("weighted\t3\t2,-3,0\t1,2\t5,2,2").unwrap();
        assert_eq!(neg.split('\t').nth(6), Some("2"));
        assert_eq!(neg.split('\t').nth(7), Some("2"));
    }

    #[test]
    fn pfp_residual_sector_weights_two_disjoint_cycles_need_both_holonomies() {
        assert_eq!(
            replay("twocycle\t3\t2,0,0\t3\t-1,0,0").unwrap(),
            "twocycle\t3\t2,0,0\t3\t-1,0,0\t2,-1\t3\t18\t1\t0"
        );
        assert_eq!(replay("twocycle\t3\t1,0,0\t3\t1,0,0").unwrap().split('\t').nth(9), Some("1"));
    }

    #[test]
    fn pfp_residual_sector_weights_malformed_inputs_are_refused() {
        assert!(replay("residual\t4\t1,0,1\t2,2").is_none());
        assert!(replay("residual\t4\t1,0,1,0\t2,3").is_none());
        assert!(replay("weighted\t4\t1,0,1,0\t2,2\t1,0,3,4").is_none());
        assert!(replay("other\t4\t1,0,1,0\t2,2").is_none());
    }
}
