//! History-report criterion: exhaustive replay over all (report, question) function pairs.
//!
//! Exact integer replay of `code/python/src/qm/pfp_history_report.py` for PFP batch 01, node
//! PG-HISTORY-REPORT-CRITERION. Histories {0..h-1}, reports {0..v-1}, answers {0..s-1}; every report and every
//! question is enumerated and the factorization through the report image is searched directly.
//! Finite instances only; the general statement is the Lean module HistoryReport. AuthorityEffect: None.
use std::collections::{BTreeMap, HashMap};

/// All tuples of the given length over `0..base`; exactly one empty tuple when `len == 0`, none when `base == 0 < len`.
fn tuples(base: usize, len: usize) -> Vec<Vec<usize>> {
    let mut out: Vec<Vec<usize>> = vec![Vec::new()];
    for _ in 0..len {
        let mut next = Vec::with_capacity(out.len() * base);
        for t in &out {
            for x in 0..base {
                let mut u = t.clone();
                u.push(x);
                next.push(u);
            }
        }
        out = next;
    }
    out
}

/// One certificate row for the triple (h, v, s).
pub struct Row {
    pub pairs: u64,
    pub fiber_constant: u64,
    pub factoring: u64,
    pub mismatch: u64,
    pub hist: BTreeMap<usize, u64>,
    pub max_mult: u64,
    pub ext_total: u64,
    pub nonunique: u64,
    pub surj: u64,
    pub surj_nonunique: u64,
}

pub fn record(h: usize, v: usize, s: usize) -> Row {
    let all_f = tuples(s, v);
    let answers = tuples(s, h);
    let mut row = Row { pairs: 0, fiber_constant: 0, factoring: 0, mismatch: 0, hist: BTreeMap::new(), max_mult: 0, ext_total: 0, nonunique: 0, surj: 0, surj_nonunique: 0 };
    for rep in tuples(v, h) {
        let mut image: Vec<usize> = rep.clone();
        image.sort();
        image.dedup();
        let k = image.len();
        *row.hist.entry(k).or_insert(0) += 1;
        let is_surj = k == v;
        if is_surj {
            row.surj += 1;
        }
        let index: HashMap<usize, usize> = image.iter().enumerate().map(|(i, &x)| (x, i)).collect();
        let mut factor_count: HashMap<Vec<usize>, u64> = HashMap::new();
        for g in tuples(s, k) {
            let key: Vec<usize> = (0..h).map(|i| g[index[&rep[i]]]).collect();
            *factor_count.entry(key).or_insert(0) += 1;
        }
        let mut ext_count: HashMap<Vec<usize>, u64> = HashMap::new();
        for f in &all_f {
            let key: Vec<usize> = (0..h).map(|i| f[rep[i]]).collect();
            *ext_count.entry(key).or_insert(0) += 1;
        }
        for ans in &answers {
            row.pairs += 1;
            let mut fc = true;
            for i in 0..h {
                for j in 0..h {
                    if rep[i] == rep[j] && ans[i] != ans[j] {
                        fc = false;
                    }
                }
            }
            let ng = *factor_count.get(ans).unwrap_or(&0);
            let fact = ng > 0;
            row.fiber_constant += fc as u64;
            row.factoring += fact as u64;
            row.mismatch += (fc != fact) as u64;
            if ng > row.max_mult {
                row.max_mult = ng;
            }
            let ne = *ext_count.get(ans).unwrap_or(&0);
            row.ext_total += ne;
            if fact && ne >= 2 {
                row.nonunique += 1;
                if is_surj {
                    row.surj_nonunique += 1;
                }
            }
        }
    }
    row
}

/// Wire line identical to the Python `wire_lines` format.
pub fn line(h: usize, v: usize, s: usize) -> String {
    let r = record(h, v, s);
    let hist: Vec<String> = r.hist.iter().map(|(k, c)| format!("{}:{}", k, c)).collect();
    format!(
        "report\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        h,
        v,
        s,
        r.pairs,
        r.fiber_constant,
        r.factoring,
        r.mismatch,
        if hist.is_empty() { "-".to_string() } else { hist.join(";") },
        r.max_mult,
        r.ext_total,
        r.nonunique,
        r.surj,
        r.surj_nonunique
    )
}

/// Replay one tab-separated public-input line `report\th\tv\ts`.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "report" {
        return None;
    }
    let h: usize = parts.next()?.parse().ok()?;
    let v: usize = parts.next()?.parse().ok()?;
    let s: usize = parts.next()?.parse().ok()?;
    if parts.next().is_some() || h > 6 || v > 6 || s > 6 {
        return None;
    }
    Some(line(h, v, s))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn binom(n: u64, k: u64) -> u64 {
        if k > n {
            return 0;
        }
        (0..k).fold(1u64, |acc, i| acc * (n - i) / (i + 1))
    }

    fn surjections(h: u32, k: u64) -> i64 {
        (0..=k as i64).map(|j| (if j % 2 == 0 { 1 } else { -1 }) * binom(k, j as u64) as i64 * (k as i64 - j).pow(h)).sum()
    }

    #[test]
    fn pfp_history_report_criterion_pairwise_on_a_range() {
        for h in 0..4 {
            for v in 0..4 {
                for s in 0..3 {
                    let r = record(h, v, s);
                    assert_eq!(r.mismatch, 0, "({}, {}, {})", h, v, s);
                    assert_eq!(r.fiber_constant, r.factoring);
                    assert!(r.max_mult <= 1);
                    assert_eq!(r.surj_nonunique, 0);
                }
            }
        }
    }

    #[test]
    fn pfp_history_report_factoring_count_matches_surjection_formula() {
        for h in 0..5usize {
            for v in 0..4usize {
                for s in 0..3usize {
                    let want: i64 = (0..=std::cmp::min(h, v) as u64)
                        .map(|k| binom(v as u64, k) as i64 * surjections(h as u32, k) * (s as i64).pow(k as u32))
                        .sum();
                    assert_eq!(record(h, v, s).factoring as i64, want, "({}, {}, {})", h, v, s);
                    assert_eq!(record(h, v, s).ext_total as usize, v.pow(h as u32) * s.pow(v as u32));
                }
            }
        }
    }

    #[test]
    fn pfp_history_report_off_image_extension_not_unique() {
        let r = record(1, 2, 2);
        assert_eq!((r.factoring, r.nonunique), (4, 4));
        assert_eq!(record(2, 1, 2).nonunique, 0);
        assert_eq!(record(0, 0, 0).factoring, 1);
        assert_eq!(record(1, 0, 2).pairs, 0);
    }

    #[test]
    fn pfp_history_report_wire_line() {
        assert_eq!(replay("report\t3\t3\t2").unwrap(), "report\t3\t3\t2\t216\t126\t126\t0\t1:3;2:18;3:6\t1\t216\t78\t6\t0");
        assert_eq!(replay("report\t1\t0\t2").unwrap(), "report\t1\t0\t2\t0\t0\t0\t0\t-\t0\t0\t0\t0\t0");
        assert!(replay("fiber\t1\t1\t1").is_none());
    }
}
