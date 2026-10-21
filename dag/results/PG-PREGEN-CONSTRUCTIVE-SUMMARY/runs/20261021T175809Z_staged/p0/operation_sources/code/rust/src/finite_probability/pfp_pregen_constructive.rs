//! Pre-Genesis summary over listed histories: first-match reconstruction versus fiber constancy.
//!
//! Exact integer replay of `code/python/src/qm/pfp_pregen_constructive.py` for PFP batch 01, node
//! PG-PREGEN-CONSTRUCTIVE-SUMMARY. Every listing of length <= ell (repeats allowed), every report and every
//! answer is enumerated; finite instances only, the general choice-free statement is the Lean module
//! PregenConstructive. AuthorityEffect: None.
use std::collections::HashSet;

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

/// First-match reconstruction: the answer of the first listed history whose report is `x`.
pub fn recon(listing: &[usize], report: &[usize], answer: &[usize], x: usize) -> Option<usize> {
    for &h in listing {
        if report[h] == x {
            return Some(answer[h]);
        }
    }
    None
}

#[derive(Default, Debug, PartialEq, Eq)]
pub struct Row {
    pub lists: u64,
    pub triples: u64,
    pub listed_fc: u64,
    pub recon_correct: u64,
    pub mismatch: u64,
    pub complete_triples: u64,
    pub complete_mismatch: u64,
    pub partial_false_positive: u64,
    pub unlisted_refused: u64,
    pub unlisted_correct: u64,
    pub unlisted_wrong: u64,
}

pub fn record(p: usize, ell: usize, v: usize, s: usize) -> Row {
    let mut lists: Vec<Vec<usize>> = vec![Vec::new()];
    for k in 1..=ell {
        lists.extend(tuples(p, k));
    }
    let reports = tuples(v, p);
    let answers = tuples(s, p);
    let mut r = Row { lists: lists.len() as u64, ..Row::default() };
    for listing in &lists {
        let listed: HashSet<usize> = listing.iter().copied().collect();
        let complete = listed.len() == p;
        for report in &reports {
            for answer in &answers {
                r.triples += 1;
                let mut fc = true;
                for &a in listing {
                    for &b in listing {
                        if report[a] == report[b] && answer[a] != answer[b] {
                            fc = false;
                        }
                    }
                }
                let rc = listing.iter().all(|&a| recon(listing, report, answer, report[a]) == Some(answer[a]));
                let mut global_fc = true;
                for a in 0..p {
                    for b in 0..p {
                        if report[a] == report[b] && answer[a] != answer[b] {
                            global_fc = false;
                        }
                    }
                }
                r.listed_fc += fc as u64;
                r.recon_correct += rc as u64;
                r.mismatch += (fc != rc) as u64;
                if complete {
                    r.complete_triples += 1;
                    r.complete_mismatch += (fc != global_fc) as u64;
                } else if fc && !global_fc {
                    r.partial_false_positive += 1;
                }
                if fc {
                    for h in 0..p {
                        if listed.contains(&h) {
                            continue;
                        }
                        match recon(listing, report, answer, report[h]) {
                            None => r.unlisted_refused += 1,
                            Some(a) if a == answer[h] => r.unlisted_correct += 1,
                            Some(_) => r.unlisted_wrong += 1,
                        }
                    }
                }
            }
        }
    }
    r
}

/// Wire line identical to the Python `wire_lines` format.
pub fn line(p: usize, ell: usize, v: usize, s: usize) -> String {
    let r = record(p, ell, v, s);
    format!(
        "listed\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        p, ell, v, s, r.lists, r.triples, r.listed_fc, r.recon_correct, r.mismatch, r.complete_triples, r.complete_mismatch,
        r.partial_false_positive, r.unlisted_refused, r.unlisted_correct, r.unlisted_wrong
    )
}

/// Replay one tab-separated public-input line `listed\tp\tell\tv\ts`.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "listed" {
        return None;
    }
    let p: usize = parts.next()?.parse().ok()?;
    let ell: usize = parts.next()?.parse().ok()?;
    let v: usize = parts.next()?.parse().ok()?;
    let s: usize = parts.next()?.parse().ok()?;
    if parts.next().is_some() || p > 5 || ell > 5 || v > 4 || s > 4 {
        return None;
    }
    Some(line(p, ell, v, s))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_pregen_constructive_listed_criterion_on_a_range() {
        for p in 0..4 {
            for ell in 0..4 {
                for v in 0..3 {
                    for s in 0..3 {
                        let r = record(p, ell, v, s);
                        assert_eq!(r.mismatch, 0, "({}, {}, {}, {})", p, ell, v, s);
                        assert_eq!(r.listed_fc, r.recon_correct);
                        assert_eq!(r.complete_mismatch, 0);
                    }
                }
            }
        }
    }

    #[test]
    fn pfp_pregen_constructive_listing_and_triple_totals() {
        for &(p, ell, v, s) in &[(2usize, 3usize, 2usize, 2usize), (3, 2, 2, 3), (3, 4, 1, 2)] {
            let r = record(p, ell, v, s);
            assert_eq!(r.lists as usize, (0..=ell).map(|k| p.pow(k as u32)).sum::<usize>());
            assert_eq!(r.triples as usize, r.lists as usize * v.pow(p as u32) * s.pow(p as u32));
        }
    }

    #[test]
    fn pfp_pregen_constructive_failure_off_the_listing() {
        let (report, answer) = ([0usize, 1, 0], [0usize, 1, 2]);
        assert_eq!(recon(&[0], &report, &answer, report[2]), Some(0));
        assert_ne!(recon(&[0], &report, &answer, report[2]), Some(answer[2]));
        assert_eq!(recon(&[0], &report, &answer, report[1]), None);
    }

    #[test]
    fn pfp_pregen_constructive_wire_line() {
        assert_eq!(replay("listed\t1\t2\t2\t2").unwrap(), "listed\t1\t2\t2\t2\t3\t12\t12\t12\t0\t8\t0\t0\t4\t0\t0");
        assert!(replay("report\t1\t2\t2\t2").is_none());
    }
}
