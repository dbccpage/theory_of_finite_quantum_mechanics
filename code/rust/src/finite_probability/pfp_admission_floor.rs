//! Admission floor: exhaustive tables of relations, cuts, laws and identifications on small carriers.
//!
//! Exact replay of the Python producer `code/python/src/qm/pfp_admission_floor.py`
//! for PFP batch 01, node PG-ADMISSION-FLOOR. Relations on
//! Fin n are bitmasks (bit i*n+j is R(i, j)). Integers only; the law is supplied data and is not derived
//! from distinctness. AuthorityEffect: None.

fn bit(mask: u64, n: usize, i: usize, j: usize) -> bool {
    (mask >> (i * n + j)) & 1 == 1
}

fn irreflexive(mask: u64, n: usize) -> bool {
    (0..n).all(|i| !bit(mask, n, i, i))
}

fn classify(n: usize) -> Vec<u64> {
    let (mut rel, mut law, mut cuts, mut triples, mut inst_no_law, mut law_no_inst) = (0u64, 0u64, 0u64, 0u64, 0u64, 0u64);
    let (mut re, mut rd, mut ue, mut ud, mut ire) = (0u64, 0u64, 0u64, 0u64, 0u64);
    for mask in 0..(1u64 << (n * n)) {
        rel += 1;
        let lawful = irreflexive(mask, n);
        let nonempty = mask != 0;
        law += lawful as u64;
        cuts += (lawful && nonempty) as u64;
        inst_no_law += (nonempty && !lawful) as u64;
        law_no_inst += (lawful && !nonempty) as u64;
        for a in 0..n {
            for b in 0..n {
                let related = bit(mask, n, a, b);
                match (related, a == b) {
                    (true, true) => re += 1,
                    (true, false) => rd += 1,
                    (false, true) => ue += 1,
                    (false, false) => ud += 1,
                }
                if lawful && related {
                    triples += 1;
                    if a == b {
                        ire += 1;
                    }
                }
            }
        }
    }
    vec![rel, law, cuts, triples, inst_no_law, law_no_inst, re, rd, ue, ud, ire]
}

/// All maps q : Fin n -> Fin n, as vectors.
fn maps(n: usize) -> Vec<Vec<usize>> {
    let mut out: Vec<Vec<usize>> = vec![Vec::new()];
    for _ in 0..n {
        let mut next = Vec::new();
        for prefix in &out {
            for v in 0..n {
                let mut t = prefix.clone();
                t.push(v);
                next.push(t);
            }
        }
        out = next;
    }
    out
}

fn identify(n: usize) -> Vec<u64> {
    let lawful: Vec<u64> = (0..(1u64 << (n * n))).filter(|m| irreflexive(*m, n)).collect();
    let (mut rq, mut with_target, mut identifying, mut overlap) = (0u64, 0u64, 0u64, 0u64);
    let (mut cut_q, mut cut_with_target, mut cut_ident, mut cut_ident_with_target) = (0u64, 0u64, 0u64, 0u64);
    for q in maps(n) {
        for r in &lawful {
            let mut related = Vec::new();
            for a in 0..n {
                for b in 0..n {
                    if bit(*r, n, a, b) {
                        related.push((a, b));
                    }
                }
            }
            let has_target = lawful.iter().any(|t| related.iter().all(|(a, b)| bit(*t, n, q[*a], q[*b])));
            let ident = related.iter().any(|(a, b)| q[*a] == q[*b]);
            rq += 1;
            with_target += has_target as u64;
            identifying += ident as u64;
            overlap += (has_target && ident) as u64;
            for (a, b) in &related {
                cut_q += 1;
                cut_with_target += has_target as u64;
                cut_ident += (q[*a] == q[*b]) as u64;
                cut_ident_with_target += (has_target && q[*a] == q[*b]) as u64;
            }
        }
    }
    vec![rq, with_target, identifying, overlap, cut_q, cut_with_target, cut_ident, cut_ident_with_target]
}

/// Wire line for one case, identical to the Python `wire_lines` format.
pub fn line(kind: &str, n: usize) -> Option<String> {
    let fields = match kind {
        "classify" if n <= 5 => classify(n),
        "identify" if (1..=3).contains(&n) => identify(n),
        _ => return None,
    };
    let mut parts = vec![kind.to_string(), n.to_string()];
    parts.extend(fields.iter().map(|f| f.to_string()));
    Some(parts.join("\t"))
}

/// Replay one tab-separated public-input line `classify\tn` or `identify\tn`.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    let kind = parts.next()?;
    let n: usize = parts.next()?.parse().ok()?;
    if parts.next().is_some() {
        return None;
    }
    line(kind, n)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn f(kind: &str, n: usize) -> Vec<u64> {
        line(kind, n).unwrap().split('\t').skip(2).map(|x| x.parse().unwrap()).collect()
    }

    #[test]
    fn pfp_admission_floor_no_cut_on_a_subsingleton() {
        for n in 0..2 {
            let c = f("classify", n);
            assert_eq!((c[2], c[3]), (0, 0), "cut on {} points", n);
        }
        assert_eq!(f("classify", 2)[2], 3);
    }

    #[test]
    fn pfp_admission_floor_endpoints_apart_and_independence() {
        for n in 0..5 {
            assert_eq!(f("classify", n)[10], 0, "apartness at n={}", n);
        }
        let one = f("classify", 1);
        assert_eq!((one[4], one[5], one[6], one[7]), (1, 1, 1, 0)); // instance w/o law, law w/o instance, loop, no distinct pair
        let two = f("classify", 2);
        assert!(two[9] > 0 && two[7] > 0);
    }

    #[test]
    fn pfp_admission_floor_identification_breaks_law_and_converse() {
        for n in 1..=3 {
            let i = f("identify", n);
            assert_eq!(i[3], 0);
            assert_eq!(i[7], 0);
            assert_eq!(i[1] + i[2], i[0]);
        }
    }

    #[test]
    fn pfp_admission_floor_replay_matches_hand_counts() {
        assert_eq!(replay("classify\t2").unwrap(), "classify\t2\t16\t4\t3\t4\t12\t1\t16\t16\t16\t16\t0");
        assert_eq!(replay("identify\t2").unwrap(), "identify\t2\t16\t10\t6\t0\t16\t8\t8\t0");
        assert!(replay("identify\t0").is_none());
        assert!(replay("classify\t2\textra").is_none());
    }
}
