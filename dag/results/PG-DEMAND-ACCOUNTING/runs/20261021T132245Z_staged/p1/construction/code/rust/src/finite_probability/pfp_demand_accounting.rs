//! Finite demand accounting `s_next = s - d + b`: exhaustive classification of (W, D, B) over small universes.
//!
//! Exact integer replay of `code/python/src/qm/pfp_demand_accounting.py` for PFP batch 01, node
//! PG-DEMAND-ACCOUNTING. Sets are bitmasks over `u` elements; the next register is `(W \ D) | B`.
//! Scope: finite sets only; no statement about which demands an engine carries. AuthorityEffect: None.

fn popcount(x: u64) -> i64 {
    x.count_ones() as i64
}

/// Tally per hypothesis class [hold, subset-only violated, overlap-only violated, both]:
/// (triples, integer identity holds, truncated identity holds).
pub fn classes(u: u32) -> [[u64; 3]; 4] {
    let full: u64 = (1u64 << u) - 1;
    let mut tally = [[0u64; 3]; 4];
    for w in 0..=full {
        for d in 0..=full {
            for b in 0..=full {
                let surv = w & !d & full;
                let nxt = surv | b;
                let (s, dd, bb) = (popcount(w), popcount(d), popcount(b));
                let sub_bad = (d & !w & full) != 0;
                let ov_bad = (surv & b) != 0;
                let k = (sub_bad as usize) + 2 * (ov_bad as usize);
                tally[k][0] += 1;
                if popcount(nxt) == s - dd + bb {
                    tally[k][1] += 1;
                }
                if popcount(nxt) == (s - dd).max(0) + bb {
                    tally[k][2] += 1;
                }
            }
        }
    }
    tally
}

/// Number of (d, b) with 0 <= d <= s, b >= 0 and s - d + b == t.
pub fn decomposition_count(s: i64, t: i64) -> i64 {
    (0..=s).filter(|d| t - s + d >= 0).count() as i64
}

pub fn demand_line(u: u32) -> String {
    let cls = classes(u);
    let mut parts = vec!["demand".to_string(), u.to_string(), 8u64.pow(u).to_string()];
    for c in cls.iter() {
        parts.push(format!("{}:{}:{}", c[0], c[1], c[2]));
    }
    parts.join("\t")
}

pub fn sequence_line(seq: &[i64]) -> String {
    let steps: Vec<(i64, i64)> = seq.windows(2).map(|p| (p[0], p[1])).collect();
    let counts: Vec<i64> = steps.iter().map(|&(s, t)| decomposition_count(s, t)).collect();
    let under = counts.iter().any(|&c| c >= 2);
    let join = |v: &[i64]| v.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",");
    format!(
        "sequence\t{}\t{}\t{}",
        join(seq),
        join(&counts),
        under as i32
    )
}

fn lists(a: u8, maxlen: usize) -> Vec<Vec<u8>> {
    let mut all: Vec<Vec<u8>> = vec![vec![]];
    let mut layer: Vec<Vec<u8>> = vec![vec![]];
    for _ in 0..maxlen {
        let mut next = Vec::new();
        for w in &layer {
            for x in 0..a {
                let mut v = w.clone();
                v.push(x);
                next.push(v);
            }
        }
        all.extend(next.iter().cloned());
        layer = next;
    }
    all
}

fn is_nodup(v: &[u8]) -> bool {
    (0..v.len()).all(|i| !v[..i].contains(&v[i]))
}

/// List-register census: every active list, discharge predicate (subset of the alphabet) and births list.
pub fn listreg_line(a: u8, maxlen: usize) -> String {
    let ls = lists(a, maxlen);
    let (mut total, mut identity, mut nodup_in, mut disjoint, mut nd_dis, mut nd_ov) = (0u64, 0u64, 0u64, 0u64, 0u64, 0u64);
    for active in &ls {
        for mask in 0..(1u32 << a) {
            let surv: Vec<u8> = active.iter().copied().filter(|x| (mask >> x) & 1 == 0).collect();
            for births in &ls {
                total += 1;
                let mut reg = surv.clone();
                reg.extend(births.iter().copied());
                if reg.len() == active.len() - (active.len() - surv.len()) + births.len() {
                    identity += 1;
                }
                if is_nodup(active) && is_nodup(births) {
                    nodup_in += 1;
                    let ok = is_nodup(&reg);
                    if !surv.iter().any(|x| births.contains(x)) {
                        disjoint += 1;
                        if ok {
                            nd_dis += 1;
                        }
                    } else if ok {
                        nd_ov += 1;
                    }
                }
            }
        }
    }
    format!("listreg\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}", a, maxlen, total, identity, nodup_in, disjoint, nd_dis, nd_ov)
}

/// Replay one tab-separated public-input line (`demand\tu` or `sequence\ta,b,c`).
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    match parts.next()? {
        "demand" => {
            let u: u32 = parts.next()?.parse().ok()?;
            if u > 6 {
                return None;
            }
            Some(demand_line(u))
        }
        "sequence" => {
            let seq: Option<Vec<i64>> = parts.next()?.split(',').map(|x| x.parse().ok()).collect();
            let seq = seq?;
            if seq.is_empty() || seq.iter().any(|&x| x < 0 || x > 64) {
                return None;
            }
            Some(sequence_line(&seq))
        }
        "listreg" => {
            let a: u8 = parts.next()?.parse().ok()?;
            let maxlen: usize = parts.next()?.parse().ok()?;
            if a > 4 || maxlen > 4 {
                return None;
            }
            Some(listreg_line(a, maxlen))
        }
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_demand_accounting_class_sizes_follow_closed_forms() {
        for u in 0..=5u32 {
            let c = classes(u);
            let p = |b: u64| b.pow(u);
            assert_eq!(c[0][0], p(5));
            assert_eq!(c[1][0], p(7) - p(5));
            assert_eq!(c[2][0], p(6) - p(5));
            assert_eq!(c[3][0], p(8) + p(5) - p(7) - p(6));
        }
    }

    #[test]
    fn pfp_demand_accounting_identity_holds_exactly_under_both_hypotheses() {
        for u in 0..=5u32 {
            let c = classes(u);
            assert_eq!(c[0][1], c[0][0]);
            assert_eq!(c[0][2], c[0][0]);
            assert_eq!(c[1][1], 0);
            assert_eq!(c[2][1], 0);
        }
    }

    #[test]
    fn pfp_demand_accounting_accidental_agreement_and_truncation() {
        assert_eq!(classes(2)[3], [4, 4, 4]);
        assert_eq!(classes(3)[1], [218, 0, 152]);
    }

    #[test]
    fn pfp_demand_accounting_declared_sequence_is_underdetermined() {
        let l = sequence_line(&[0, 1, 1, 1, 0, 1, 1]);
        assert_eq!(l, "sequence\t0,1,1,1,0,1,1\t1,2,2,1,1,2\t1");
        assert!(sequence_line(&[0, 5, 0, 2]).ends_with("\t0"));
    }

    #[test]
    fn pfp_demand_accounting_listreg_census_and_replay_matches_wire() {
        assert_eq!(listreg_line(2, 2), "listreg\t2\t2\t196\t196\t100\t68\t68\t0");
        let l = listreg_line(3, 3);
        let cols: Vec<&str> = l.split('\t').collect();
        assert_eq!(cols[4], cols[3]);
        assert_eq!(cols[8], "0");
        assert_eq!(cols[7], cols[6]);
        assert_eq!(replay("demand\t0").unwrap(), "demand\t0\t1\t1:1:1\t0:0:0\t0:0:0\t0:0:0");
        assert!(replay("demand\t9").is_none());
        assert!(replay("other\t1").is_none());
    }
}
