//! Collapsed observation barrier: exhaustive counts of profiles, tasks, factorisations and added tags.
//!
//! Exact replay of `code/python/src/qm/pfp_collapse_barrier.py` for PFP batch 01, node PG-COLLAPSE-BARRIER.
//! Carrier X = Fin n, profile p : X -> Fin my, task s : X -> Fin mz. Integers only; no selection or physical
//! claim. AuthorityEffect: None.
use std::collections::BTreeMap;

/// All tuples of length `len` over `0..base` (one empty tuple when `len == 0`, none when `base == 0 < len`).
fn tuples(len: usize, base: usize) -> Vec<Vec<usize>> {
    let mut out: Vec<Vec<usize>> = vec![Vec::new()];
    for _ in 0..len {
        let mut next = Vec::with_capacity(out.len() * base);
        for prefix in &out {
            for v in 0..base {
                let mut t = prefix.clone();
                t.push(v);
                next.push(t);
            }
        }
        out = next;
    }
    out
}

fn fibre_constant(codes: &[usize], s: &[usize]) -> bool {
    let mut seen: BTreeMap<usize, usize> = BTreeMap::new();
    for (a, b) in codes.iter().zip(s.iter()) {
        if *seen.entry(*a).or_insert(*b) != *b {
            return false;
        }
    }
    true
}

/// Number of g : codomain -> Z with g(codes[x]) = s[x], by enumerating every g.
fn count_g(codes: &[usize], gs: &[Vec<usize>], s: &[usize]) -> u64 {
    gs.iter()
        .filter(|g| codes.iter().zip(s.iter()).all(|(c, v)| g[*c] == *v))
        .count() as u64
}

fn min_tag(p: &[usize], s: &[usize], my: usize, mz: usize, n: usize, tags: &[Vec<Vec<usize>>]) -> u64 {
    for k in 0..=n.max(1) {
        for t in &tags[k] {
            let codes: Vec<usize> = p.iter().zip(t.iter()).map(|(a, b)| a * k + b).collect();
            let mut distinct = codes.clone();
            distinct.sort();
            distinct.dedup();
            if fibre_constant(&codes, s) && (mz >= 1 || distinct.len() == my * k) {
                return k as u64;
            }
        }
    }
    u64::MAX
}

/// Wire line for one case, identical to the Python `wire_lines` format.
pub fn line(n: usize, my: usize, mz: usize) -> String {
    let ps = tuples(n, my);
    let ss = tuples(n, mz);
    let gs = tuples(my, mz);
    let tags: Vec<Vec<Vec<usize>>> = (0..=n.max(1)).map(|k| tuples(n, k)).collect();
    let (mut total, mut fc, mut fac, mut viol, mut facs) = (0u64, 0u64, 0u64, 0u64, 0u64);
    let mut hist: BTreeMap<u64, u64> = BTreeMap::new();
    for p in &ps {
        for s in &ss {
            total += 1;
            let constant = fibre_constant(p, s);
            fc += constant as u64;
            let cg = count_g(p, &gs, s);
            facs += cg;
            fac += (cg > 0) as u64;
            viol += (cg > 0 && !constant) as u64;
            *hist.entry(min_tag(p, s, my, mz, n, &tags)).or_insert(0) += 1;
        }
    }
    let h: Vec<String> = hist.iter().map(|(k, c)| format!("{}:{}", k, c)).collect();
    format!(
        "tag\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        n,
        my,
        mz,
        total,
        fc,
        total - fc,
        fac,
        facs,
        viol,
        if h.is_empty() { "-".to_string() } else { h.join(";") }
    )
}

/// Replay one tab-separated public-input line `tag\tn\tmy\tmz`. Refuses cases with more than 10^6 pairs.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "tag" {
        return None;
    }
    let n: usize = parts.next()?.parse().ok()?;
    let my: usize = parts.next()?.parse().ok()?;
    let mz: usize = parts.next()?.parse().ok()?;
    if parts.next().is_some() || n > 8 || my > 8 || mz > 8 {
        return None;
    }
    let pairs = (my as u128).pow(n as u32) * (mz as u128).pow(n as u32);
    if pairs > 1_000_000 {
        return None;
    }
    Some(line(n, my, mz))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn cols(l: &str) -> Vec<String> {
        l.split('\t').map(|x| x.to_string()).collect()
    }

    #[test]
    fn pfp_collapse_barrier_has_no_exceptions_on_every_listed_case() {
        for (n, my, mz) in [(0, 0, 1), (0, 1, 0), (1, 1, 2), (2, 0, 2), (2, 1, 2), (2, 2, 2), (3, 1, 2), (3, 2, 3)] {
            let c = cols(&line(n, my, mz));
            assert_eq!(c[9], "0", "violations at ({}, {}, {})", n, my, mz);
            let total: u64 = c[4].parse().unwrap();
            let fc: u64 = c[5].parse().unwrap();
            let cs: u64 = c[6].parse().unwrap();
            assert_eq!(fc + cs, total);
        }
    }

    #[test]
    fn pfp_collapse_barrier_empty_task_codomain_boundary() {
        // empty X, one profile value, empty Z: the fibre condition holds vacuously but no g exists
        let c = cols(&line(0, 1, 0));
        assert_eq!((c[5].as_str(), c[7].as_str(), c[8].as_str()), ("1", "0", "0"));
        assert_eq!(c[10], "0:1");
        // empty carrier: the empty tag alphabet works, for every codomain
        assert_eq!(cols(&line(0, 0, 1))[10], "0:1");
        assert_eq!(cols(&line(0, 2, 2))[10], "0:1");
    }

    #[test]
    fn pfp_collapse_barrier_collapsed_two_point_needs_two_tag_values() {
        let c = cols(&line(2, 1, 2));
        assert_eq!(c[10], "1:2;2:2");
        assert_eq!(c[6], "2");
    }

    #[test]
    fn pfp_collapse_barrier_replay_matches_hand_counts() {
        assert_eq!(
            replay("tag\t3\t2\t3").unwrap(),
            "tag\t3\t2\t3\t216\t60\t156\t60\t72\t0\t1:60;2:144;3:12"
        );
        assert_eq!(replay("tag\t2\t0\t2").unwrap(), "tag\t2\t0\t2\t0\t0\t0\t0\t0\t0\t-");
        assert!(replay("tag\t3\t2").is_none());
        assert!(replay("other\t1\t1\t1").is_none());
    }

    #[test]
    fn pfp_collapse_barrier_factorizations_are_my_pow_n_times_mz_pow_my() {
        for n in 0..4usize {
            for my in 0..3usize {
                for mz in 0..3usize {
                    let c = cols(&line(n, my, mz));
                    let want = (my as u64).pow(n as u32) * (mz as u64).pow(my as u32);
                    assert_eq!(c[8].parse::<u64>().unwrap(), want, "({}, {}, {})", n, my, mz);
                }
            }
        }
    }
}
