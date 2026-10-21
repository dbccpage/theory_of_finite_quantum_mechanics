//! Symmetry price of selecting a point on an n-point set: invariant points and the minimal-input frontier.
//!
//! Exact integer replay of `code/python/src/qm/pfp_wdp_protected_questions.py` for PFP batch 01, node
//! PG-WDP-PROTECTED-QUESTIONS. Subsets of {0..n-1} are bit masks. Model: a declared set S is fixed pointwise;
//! x is invariant when every permutation fixing S pointwise fixes x; the frontier is the family of inclusion-minimal
//! selecting sets. Rust is the independent third implementation: it enumerates the permutations that fix S
//! pointwise (recursive generation) instead of using the closed form, and defines minimality by the definition
//! over proper submasks. Symmetry-price bookkeeping only. AuthorityEffect: None.

fn permutations(n: usize) -> Vec<Vec<usize>> {
    fn go(prefix: &mut Vec<usize>, used: &mut Vec<bool>, n: usize, out: &mut Vec<Vec<usize>>) {
        if prefix.len() == n {
            out.push(prefix.clone());
            return;
        }
        for i in 0..n {
            if !used[i] {
                used[i] = true;
                prefix.push(i);
                go(prefix, used, n, out);
                prefix.pop();
                used[i] = false;
            }
        }
    }
    let mut out = Vec::new();
    go(&mut Vec::new(), &mut vec![false; n], n, &mut out);
    out
}

/// Points fixed by every permutation of 0..n that fixes the points of `mask`, as a bit mask.
pub fn invariant_mask(n: usize, mask: u32, perms: &[Vec<usize>]) -> u32 {
    let mut inv = 0u32;
    'point: for x in 0..n {
        for p in perms {
            let fixes_s = (0..n).all(|i| mask >> i & 1 == 0 || p[i] == i);
            if fixes_s && p[x] != x {
                continue 'point;
            }
        }
        inv |= 1 << x;
    }
    inv
}

/// One public-input line `sel\tn` to the wire line.
pub fn line(n: usize) -> String {
    let perms = permutations(n);
    let size = 1usize << n;
    let inv: Vec<u32> = (0..size).map(|mask| invariant_mask(n, mask as u32, &perms)).collect();
    let selecting: Vec<bool> = inv.iter().map(|&v| v != 0).collect();
    let minimal: Vec<bool> = (0..size)
        .map(|mask| {
            selecting[mask]
                && !(0..size).any(|sub| sub != mask && sub & mask == sub && selecting[sub])
        })
        .collect();
    let sel_count = selecting.iter().filter(|&&s| s).count();
    let frontier: Vec<String> = (0..size).filter(|&i| minimal[i]).map(|i| i.to_string()).collect();
    let min_price: i64 = (0..size)
        .filter(|&i| selecting[i])
        .map(|i| (i as u32).count_ones() as i64)
        .min()
        .unwrap_or(-1);
    let table: Vec<String> = (0..size)
        .map(|i| format!("{}:{}:{}:{}", i, inv[i], selecting[i] as i32, minimal[i] as i32))
        .collect();
    format!(
        "sel\t{}\t{}\t{}\t{}\t{}\t{}",
        n,
        sel_count,
        frontier.len(),
        min_price,
        if frontier.is_empty() { "-".to_string() } else { frontier.join(";") },
        table.join(";")
    )
}

/// Replay one tab-separated public-input line `sel\tn` (n at most 8).
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "sel" {
        return None;
    }
    let n: usize = parts.next()?.parse().ok()?;
    if parts.next().is_some() || n > 8 {
        return None;
    }
    Some(line(n))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_wdp_protected_questions_no_invariant_point_for_empty_declaration() {
        for n in 2..=6 {
            let perms = permutations(n);
            assert_eq!(invariant_mask(n, 0, &perms), 0, "n={}", n);
        }
    }

    #[test]
    fn pfp_wdp_protected_questions_frontier_is_singletons_from_two_points() {
        for n in 2..=6usize {
            let l = line(n);
            let cols: Vec<&str> = l.split('\t').collect();
            let want: Vec<String> = (0..n).map(|i| (1u32 << i).to_string()).collect();
            assert_eq!(cols[5], want.join(";"), "n={}", n);
            assert_eq!(cols[3], n.to_string());
            assert_eq!(cols[4], "1");
        }
    }

    #[test]
    fn pfp_wdp_protected_questions_boundary_carriers() {
        assert_eq!(line(0), "sel\t0\t0\t0\t-1\t-\t0:0:0:0");
        assert_eq!(line(1), "sel\t1\t2\t1\t0\t0\t0:1:1:1;1:1:1:0");
    }

    #[test]
    fn pfp_wdp_protected_questions_two_point_complement_singleton_is_invariant() {
        let perms = permutations(2);
        assert_eq!(invariant_mask(2, 1, &perms), 3);
        let perms3 = permutations(3);
        assert_eq!(invariant_mask(3, 1, &perms3), 1);
    }

    #[test]
    fn pfp_wdp_protected_questions_replay_rejects_malformed_lines() {
        assert!(replay("sel\t2").unwrap().starts_with("sel\t2\t3\t2\t1\t1;2\t"));
        assert!(replay("sel").is_none());
        assert!(replay("fiber\t2").is_none());
        assert!(replay("sel\t2\t3").is_none());
        assert!(replay("sel\t9").is_none());
    }
}
