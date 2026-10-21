//! Six operations and the admitted state: exact enumeration of traces over a small item universe.
//!
//! Exact integer replay of `code/python/src/qm/pfp_six_operations.py` for PFP batch 01, node
//! PG-SIX-OPERATIONS. State = (mentioned, supplied, designated, admitted, retained, outputs); Retain and
//! Operate act only on admitted items. Definitional model only. AuthorityEffect: None.
use std::collections::BTreeSet;

const KINDS: [&str; 6] = ["mention", "supply", "designate", "admit", "retain", "operate"];

/// (mentioned mask, supplied mask, designated 0|item+1, admitted mask, retained mask, outputs mask)
type St = (u8, u8, u8, u8, u8, u8);
type Op = (usize, u8);

fn step(s: St, op: Op) -> St {
    let (k, x) = op;
    let bit = 1u8 << x;
    let (m, u, d, a, r, o) = s;
    match k {
        0 => (m | bit, u, d, a, r, o),
        1 => (m, u | bit, d, a, r, o),
        2 => (m, u, x + 1, a, r, o),
        3 => (m, u, d, a | bit, r, o),
        4 => {
            if a & bit != 0 {
                (m, u, d, a, r | bit, o)
            } else {
                s
            }
        }
        _ => {
            if a & bit != 0 {
                (m, u, d, a, r, o | bit)
            } else {
                s
            }
        }
    }
}

fn step_conflated(s: St, op: Op, a_kind: usize, b_kind: usize) -> St {
    let mut s = s;
    if op.0 == a_kind {
        s = step(s, (b_kind, op.1));
    }
    step(s, op)
}

fn all_ops(items: u8) -> Vec<Op> {
    let mut ops = Vec::new();
    for k in 0..6 {
        for x in 0..items {
            ops.push((k, x));
        }
    }
    ops
}

fn fields_changed(a: St, b: St) -> String {
    let (x, y) = ([a.0, a.1, a.2, a.3, a.4, a.5], [b.0, b.1, b.2, b.3, b.4, b.5]);
    (0..6).map(|i| if x[i] != y[i] { '1' } else { '0' }).collect()
}

fn items_text(mask: u8, items: u8) -> String {
    let v: Vec<String> = (0..items).filter(|i| mask >> i & 1 == 1).map(|i| i.to_string()).collect();
    if v.is_empty() {
        "-".to_string()
    } else {
        v.join("+")
    }
}

fn state_text(s: St) -> String {
    let des = if s.2 == 0 { "-".to_string() } else { (s.2 - 1).to_string() };
    format!(
        "m:{}|S:{}|d:{}|a:{}|r:{}|O:{}",
        items_text(s.0, 2),
        items_text(s.1, 2),
        des,
        items_text(s.3, 2),
        items_text(s.4, 2),
        items_text(s.5, 2)
    )
}

fn trace_text(trace: &[Op]) -> String {
    trace.iter().map(|&(k, x)| format!("{}:{}", KINDS[k], x)).collect::<Vec<_>>().join(",")
}

struct TraceStats {
    total: u64,
    changed: u64,
    with_admit: u64,
    with_new: u64,
    mismatches: u64,
    finals: BTreeSet<St>,
}

#[allow(clippy::too_many_arguments)]
fn walk(s: St, init_adm: u8, has_admit: bool, has_new: bool, depth: usize, max_len: usize, ops: &[Op], stats: &mut TraceStats) {
    stats.total += 1;
    let moved = s.3 != init_adm;
    stats.changed += moved as u64;
    stats.with_admit += has_admit as u64;
    stats.with_new += has_new as u64;
    stats.mismatches += (moved != has_new) as u64;
    stats.finals.insert(s);
    if depth == max_len {
        return;
    }
    for &op in ops {
        let adm = op.0 == 3;
        let new = adm && (init_adm >> op.1 & 1) == 0;
        walk(step(s, op), init_adm, has_admit || adm, has_new || new, depth + 1, max_len, ops, stats);
    }
}

fn trace_line(items: u8, max_len: usize, mask: u8) -> Option<String> {
    if items == 0 || items > 3 || max_len > 5 || mask >= (1u8 << items) {
        return None;
    }
    let ops = all_ops(items);
    let init: St = (0, 0, 0, mask, 0, 0);
    let mut stats = TraceStats { total: 0, changed: 0, with_admit: 0, with_new: 0, mismatches: 0, finals: BTreeSet::new() };
    walk(init, mask, false, false, 0, max_len, &ops, &mut stats);
    Some(format!(
        "trace\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        items, max_len, mask, stats.total, stats.changed, stats.with_admit, stats.with_new, stats.mismatches, stats.finals.len()
    ))
}

fn kind_index(name: &str) -> Option<usize> {
    KINDS.iter().position(|k| *k == name)
}

fn footprint_line(kind: &str) -> Option<String> {
    let k = kind_index(kind)?;
    let probe: St = (0, 0, 0, 1, 0, 0);
    Some(format!(
        "footprint\t{}\t{}\t{}",
        kind,
        fields_changed(probe, step(probe, (k, 1))),
        fields_changed(probe, step(probe, (k, 0)))
    ))
}

fn pair_walk(s: St, depth: usize, a: usize, b: usize, ops: &[Op], hits_at: &mut [u64; 4]) {
    let h = (0..2u8).filter(|&x| step(s, (a, x)) != step(s, (b, x))).count() as u64;
    hits_at[depth] += h;
    if depth == 3 {
        return;
    }
    for &op in ops {
        pair_walk(step(s, op), depth + 1, a, b, ops, hits_at);
    }
}

fn pair_line(a_name: &str, b_name: &str) -> Option<String> {
    let (a, b) = (kind_index(a_name)?, kind_index(b_name)?);
    let ops = all_ops(2);
    let mut hits_at = [0u64; 4];
    pair_walk((0, 0, 0, 0, 0, 0), 0, a, b, &ops, &mut hits_at);
    let min_len: i64 = (0..4).find(|&l| hits_at[l] > 0).map(|l| l as i64).unwrap_or(-1);
    let contexts = hits_at[0] + hits_at[1] + hits_at[2];
    Some(format!("pair\t{}\t{}\t{}\t{}", a_name, b_name, min_len, contexts))
}

fn conflation_search(
    s6: St,
    sc: St,
    depth: usize,
    length: usize,
    a: usize,
    b: usize,
    ops: &[Op],
    trace: &mut Vec<Op>,
    count: &mut u64,
    first: &mut Option<(Vec<Op>, St, St)>,
) {
    if depth == length {
        if s6 != sc {
            *count += 1;
            if first.is_none() {
                *first = Some((trace.clone(), s6, sc));
            }
        }
        return;
    }
    for &op in ops {
        trace.push(op);
        conflation_search(step(s6, op), step_conflated(sc, op, a, b), depth + 1, length, a, b, ops, trace, count, first);
        trace.pop();
    }
}

fn conflation_line(name: &str) -> Option<String> {
    let (a_name, b_name) = match name {
        "mention_includes_admit" => ("mention", "admit"),
        "supply_includes_admit" => ("supply", "admit"),
        "designate_includes_admit" => ("designate", "admit"),
        "retain_includes_admit" => ("retain", "admit"),
        "operate_includes_admit" => ("operate", "admit"),
        "designate_includes_retain" => ("designate", "retain"),
        "mention_includes_supply" => ("mention", "supply"),
        _ => return None,
    };
    let (a, b) = (kind_index(a_name)?, kind_index(b_name)?);
    let ops = all_ops(2);
    for length in 1..5 {
        let mut count = 0;
        let mut first = None;
        conflation_search((0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0), 0, length, a, b, &ops, &mut Vec::new(), &mut count, &mut first);
        if let Some((trace, s6, sc)) = first {
            return Some(format!(
                "conflation\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                name,
                length,
                count,
                trace_text(&trace),
                fields_changed(s6, sc),
                (s6.3 != sc.3) as i32,
                state_text(s6),
                state_text(sc)
            ));
        }
    }
    None
}

fn reading_line(token: u8) -> Option<String> {
    if token > 1 {
        return None;
    }
    let z: St = (0, 0, 0, 0, 0, 0);
    let (supply, admit) = (1usize, 3usize);
    let six_l = step(z, (supply, token)).3;
    let six_f = step(step(z, (supply, token)), (admit, token)).3;
    let cl = step_conflated(z, (supply, token), supply, admit);
    let conf_l = cl.3;
    let conf_f = step(cl, (admit, token)).3;
    Some(format!(
        "reading\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        token,
        items_text(six_l, 2),
        items_text(six_f, 2),
        items_text(conf_l, 2),
        items_text(conf_f, 2),
        (six_l != six_f) as i32,
        (conf_l != conf_f) as i32
    ))
}

/// Replay one tab-separated public-input line (trace / footprint / pair / conflation / reading).
pub fn replay(input: &str) -> Option<String> {
    let p: Vec<&str> = input.split('\t').collect();
    match *p.first()? {
        "trace" if p.len() == 4 => trace_line(p[1].parse().ok()?, p[2].parse().ok()?, p[3].parse().ok()?),
        "footprint" if p.len() == 2 => footprint_line(p[1]),
        "pair" if p.len() == 3 => pair_line(p[1], p[2]),
        "conflation" if p.len() == 2 => conflation_line(p[1]),
        "reading" if p.len() == 2 => reading_line(p[1].parse().ok()?),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_six_operations_trace_counts_match_closed_forms() {
        assert_eq!(replay("trace\t2\t4\t0").unwrap(), "trace\t2\t4\t0\t22621\t11510\t11510\t11510\t0\t273");
        let one = replay("trace\t2\t4\t1").unwrap();
        assert!(one.starts_with("trace\t2\t4\t1\t22621\t6516\t11510\t6516\t0\t"));
        assert!(replay("trace\t2\t4\t3").unwrap().starts_with("trace\t2\t4\t3\t22621\t0\t11510\t0\t0\t"));
    }

    #[test]
    fn pfp_six_operations_only_admit_writes_admitted() {
        assert_eq!(replay("footprint\tadmit").unwrap(), "footprint\tadmit\t000100\t000000");
        assert_eq!(replay("footprint\tretain").unwrap(), "footprint\tretain\t000000\t000010");
        for k in ["mention", "supply", "designate", "retain", "operate"] {
            let line = replay(&format!("footprint\t{}", k)).unwrap();
            let cols: Vec<&str> = line.split('\t').collect();
            assert_eq!(&cols[2][3..4], "0");
            assert_eq!(&cols[3][3..4], "0");
        }
    }

    #[test]
    fn pfp_six_operations_readings_collapse_only_when_supply_admits() {
        assert_eq!(replay("reading\t0").unwrap(), "reading\t0\t-\t0\t0\t0\t1\t0");
        let c = replay("conflation\tsupply_includes_admit").unwrap();
        assert!(c.starts_with("conflation\tsupply_includes_admit\t1\t2\tsupply:0\t000100\t1\t"));
    }

    #[test]
    fn pfp_six_operations_pairs_and_designation_conflation() {
        assert_eq!(replay("pair\tretain\toperate").unwrap(), "pair\tretain\toperate\t1\t48");
        let c = replay("conflation\tdesignate_includes_retain").unwrap();
        assert!(c.contains("\t2\t2\tadmit:0,designate:0\t000010\t0\t"));
    }

    #[test]
    fn pfp_six_operations_rejects_malformed_lines() {
        assert!(replay("footprint\tnonsense").is_none());
        assert!(replay("trace\t0\t4\t0").is_none());
        assert!(replay("conflation\tx").is_none());
    }
}
