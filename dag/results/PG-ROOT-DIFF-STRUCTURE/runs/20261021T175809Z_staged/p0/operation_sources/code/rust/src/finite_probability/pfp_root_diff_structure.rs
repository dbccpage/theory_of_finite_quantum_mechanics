//! The root coproduct Real_0 = PrimitiveDifference + Structure: exhaustive counts on small finite channels.
//!
//! Exact integer replay of `code/python/src/qm/pfp_root_diff_structure.py` for PFP batch 01, node
//! PG-ROOT-DIFF-STRUCTURE (an ADMITTED PRIMITIVE). Channels are {0..a-1} and {0..b-1}; the tables verify
//! the coproduct property and the neutrality of the construction about the two posits. They derive neither
//! channel nor any reduction. AuthorityEffect: None.
use std::collections::{BTreeMap, BTreeSet};

/// All functions from a domain of size `n` to {0..c-1}, as vectors of values (c^n of them).
fn functions(n: usize, c: usize) -> Vec<Vec<usize>> {
    let mut out: Vec<Vec<usize>> = vec![Vec::new()];
    for _ in 0..n {
        let mut next = Vec::new();
        for f in &out {
            for v in 0..c {
                let mut g = f.clone();
                g.push(v);
                next.push(g);
            }
        }
        out = next;
    }
    out
}

fn maps_line(a: usize, b: usize, c: usize) -> Option<String> {
    if a > 4 || b > 4 || c > 4 || a + b > 6 {
        return None;
    }
    // coproduct positions: 0..a are the difference channel, a..a+b the structure channel
    let mut total = 0u64;
    let mut pairs: BTreeMap<(Vec<usize>, Vec<usize>), u64> = BTreeMap::new();
    for h in functions(a + b, c) {
        total += 1;
        let key = (h[..a].to_vec(), h[a..].to_vec());
        *pairs.entry(key).or_insert(0) += 1;
    }
    let left = functions(a, c).len() as u64;
    let right = functions(b, c).len() as u64;
    let unique = pairs.values().filter(|&&v| v == 1).count();
    let inl: Vec<usize> = (0..a).collect();
    let inr: Vec<usize> = (a..a + b).collect();
    let inl_injective = inl.iter().collect::<BTreeSet<_>>().len() == a;
    let inr_injective = inr.iter().collect::<BTreeSet<_>>().len() == b;
    let disjoint = inl.iter().all(|i| !inr.contains(i));
    let covering = (0..a + b).all(|p| inl.contains(&p) || inr.contains(&p));
    Some(format!(
        "maps\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        a,
        b,
        c,
        total,
        left,
        right,
        (total == left * right) as i32,
        unique,
        inl_injective as i32,
        inr_injective as i32,
        disjoint as i32,
        covering as i32
    ))
}

fn reduction_line(a: usize, b: usize) -> Option<String> {
    if a > 4 || b > 4 || a + b > 7 {
        return None;
    }
    let retr_a = functions(a + b, a).into_iter().filter(|h| (0..a).all(|i| h[i] == i)).count();
    let retr_b = functions(a + b, b).into_iter().filter(|h| (0..b).all(|j| h[a + j] == j)).count();
    Some(format!(
        "reduction\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        a,
        b,
        functions(b, a).len(),
        functions(a, b).len(),
        retr_a,
        retr_b,
        (retr_a > 0) as i32,
        (retr_b > 0) as i32
    ))
}

fn posit_line(a: usize, b: usize) -> Option<String> {
    if a > 1 || b > 1 {
        return None;
    }
    let size = a + b;
    Some(format!(
        "posit\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        a,
        b,
        (a > 0) as i32,
        (b > 0) as i32,
        size,
        (size > 0) as i32,
        ((size > 0) == (a > 0 || b > 0)) as i32
    ))
}

/// Replay one tab-separated public-input line (maps / reduction / posit).
pub fn replay(input: &str) -> Option<String> {
    let p: Vec<&str> = input.split('\t').collect();
    match *p.first()? {
        "maps" if p.len() == 4 => maps_line(p[1].parse().ok()?, p[2].parse().ok()?, p[3].parse().ok()?),
        "reduction" if p.len() == 3 => reduction_line(p[1].parse().ok()?, p[2].parse().ok()?),
        "posit" if p.len() == 3 => posit_line(p[1].parse().ok()?, p[2].parse().ok()?),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_root_diff_structure_maps_out_count_is_the_product() {
        assert_eq!(replay("maps\t2\t2\t2").unwrap(), "maps\t2\t2\t2\t16\t4\t4\t1\t16\t1\t1\t1\t1");
        assert_eq!(replay("maps\t0\t1\t0").unwrap(), "maps\t0\t1\t0\t0\t1\t0\t1\t0\t1\t1\t1\t1");
        assert_eq!(replay("maps\t3\t2\t2").unwrap(), "maps\t3\t2\t2\t32\t8\t4\t1\t32\t1\t1\t1\t1");
    }

    #[test]
    fn pfp_root_diff_structure_no_reduction_into_an_empty_channel() {
        assert_eq!(replay("reduction\t0\t2").unwrap(), "reduction\t0\t2\t0\t1\t0\t1\t0\t1");
        assert_eq!(replay("reduction\t3\t0").unwrap(), "reduction\t3\t0\t1\t0\t1\t0\t1\t0");
        assert_eq!(replay("reduction\t0\t0").unwrap(), "reduction\t0\t0\t1\t1\t1\t1\t1\t1");
    }

    #[test]
    fn pfp_root_diff_structure_reductions_are_a_choice_when_they_exist() {
        assert_eq!(replay("reduction\t2\t2").unwrap(), "reduction\t2\t2\t4\t4\t4\t4\t1\t1");
        assert_eq!(replay("reduction\t2\t3").unwrap(), "reduction\t2\t3\t8\t9\t8\t9\t1\t1");
    }

    #[test]
    fn pfp_root_diff_structure_posits_are_independent() {
        assert_eq!(replay("posit\t0\t0").unwrap(), "posit\t0\t0\t0\t0\t0\t0\t1");
        assert_eq!(replay("posit\t0\t1").unwrap(), "posit\t0\t1\t0\t1\t1\t1\t1");
        assert_eq!(replay("posit\t1\t0").unwrap(), "posit\t1\t0\t1\t0\t1\t1\t1");
        assert_eq!(replay("posit\t1\t1").unwrap(), "posit\t1\t1\t1\t1\t2\t1\t1");
        assert!(replay("posit\t2\t0").is_none());
    }

    #[test]
    fn pfp_root_diff_structure_rejects_malformed_lines() {
        assert!(replay("maps\t1\t1").is_none());
        assert!(replay("other\t1").is_none());
    }
}
