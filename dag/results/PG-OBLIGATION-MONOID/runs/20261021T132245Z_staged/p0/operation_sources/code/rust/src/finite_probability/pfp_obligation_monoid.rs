//! Obligation monoid: exact tables for counter vectors, event traces and the generate/discharge ledger.
//!
//! Exact replay of `code/python/src/qm/pfp_obligation_monoid.py` for PFP batch 01, node PG-OBLIGATION-MONOID.
//! Record kinds: laws, bounded, saturating, events, ledger. Counters are u64 with checked addition, as in the
//! `obligation.rs` source; the three-id ledger is a finite model, not a run of that crate. Genesis events and
//! S(n) maps are NOT shown to be monoid morphisms. AuthorityEffect: None.
use std::collections::BTreeSet;

type V = Vec<u64>;

fn tuples(k: usize, n: u64) -> Vec<V> {
    let mut out: Vec<V> = vec![Vec::new()];
    for _ in 0..k {
        let mut next = Vec::with_capacity(out.len() * n as usize);
        for p in &out {
            for c in 0..n {
                let mut t = p.clone();
                t.push(c);
                next.push(t);
            }
        }
        out = next;
    }
    out
}

fn vadd(x: &V, y: &V) -> V {
    x.iter().zip(y.iter()).map(|(a, b)| a + b).collect()
}

fn laws(k: usize, n: u64) -> String {
    let els = tuples(k, n);
    let zero: V = vec![0; k];
    let (mut assoc, mut comm, mut unit, mut cancel) = (0u64, 0u64, 0u64, 0u64);
    for x in &els {
        unit += (vadd(x, &zero) != *x) as u64 + (vadd(&zero, x) != *x) as u64;
        for y in &els {
            comm += (vadd(x, y) != vadd(y, x)) as u64;
            for z in &els {
                assoc += (vadd(&vadd(x, y), z) != vadd(x, &vadd(y, z))) as u64;
                cancel += (vadd(x, z) == vadd(y, z) && x != y) as u64;
            }
        }
    }
    let inv = els
        .iter()
        .filter(|x| **x != zero && els.iter().any(|y| vadd(x, y) == zero))
        .count();
    let e = els.len() as u64;
    format!("laws\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}", k, n, e, e * e * e, assoc, comm, unit, cancel, inv)
}

fn combine_bounded(x: &V, y: &V, bound: u64) -> Option<V> {
    let s = vadd(x, y);
    if s.iter().all(|c| *c <= bound) {
        Some(s)
    } else {
        None
    }
}

fn bounded(k: usize, m: u64) -> String {
    let els = tuples(k, m + 1);
    let e = els.len() as u64;
    let mut defined = 0u64;
    for x in &els {
        for y in &els {
            defined += combine_bounded(x, y, m).is_some() as u64;
        }
    }
    let (mut triples, mut def_triples, mut def_mis, mut val_mis) = (0u64, 0u64, 0u64, 0u64);
    for x in &els {
        for y in &els {
            let xy = combine_bounded(x, y, m);
            let yz_row: Vec<Option<V>> = els.iter().map(|z| combine_bounded(y, z, m)).collect();
            for (zi, z) in els.iter().enumerate() {
                triples += 1;
                let left = xy.as_ref().and_then(|s| combine_bounded(s, z, m));
                let right = yz_row[zi].as_ref().and_then(|t| combine_bounded(x, t, m));
                def_triples += left.is_some() as u64;
                def_mis += (left.is_none() != right.is_none()) as u64;
                if let (Some(a), Some(b)) = (&left, &right) {
                    val_mis += (a != b) as u64;
                }
            }
        }
    }
    format!(
        "bounded\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        k, m, e, e * e, defined, e * e - defined, triples, def_triples, def_mis, val_mis
    )
}

fn saturating(cap: u64) -> String {
    let op = |a: u64, b: u64| (a + b).min(cap);
    let (mut assoc, mut comm, mut unit, mut cancel) = (0u64, 0u64, 0u64, 0u64);
    for x in 0..=cap {
        unit += (op(x, 0) != x) as u64 + (op(0, x) != x) as u64;
        for y in 0..=cap {
            comm += (op(x, y) != op(y, x)) as u64;
            for z in 0..=cap {
                assoc += (op(op(x, y), z) != op(x, op(y, z))) as u64;
                cancel += (op(x, z) == op(y, z) && x != y) as u64;
            }
        }
    }
    let e = cap + 1;
    format!("saturating\t{}\t{}\t{}\t{}\t{}\t{}\t{}", cap, e, e * e * e, assoc, comm, unit, cancel)
}

fn letter(c: u8) -> Option<[u64; 3]> {
    match c {
        b'D' => Some([1, 0, 0]),
        b'A' => Some([0, 1, 0]),
        b'R' | b'I' => Some([0, 0, 1]),
        _ => None,
    }
}

fn trace(word: &[u8]) -> [u64; 3] {
    let mut v = [0u64; 3];
    for c in word {
        let l = letter(*c).unwrap();
        for i in 0..3 {
            v[i] += l[i];
        }
    }
    v
}

fn permutations(word: &[u8], out: &mut BTreeSet<Vec<u8>>) {
    fn go(cur: &mut Vec<u8>, rest: &mut Vec<u8>, out: &mut BTreeSet<Vec<u8>>) {
        if rest.is_empty() {
            out.insert(cur.clone());
            return;
        }
        for i in 0..rest.len() {
            let c = rest.remove(i);
            cur.push(c);
            go(cur, rest, out);
            cur.pop();
            rest.insert(i, c);
        }
    }
    go(&mut Vec::new(), &mut word.to_vec(), out);
}

fn events(arg: &str) -> Option<String> {
    let word: Vec<u8> = if arg == "-" { Vec::new() } else { arg.bytes().collect() };
    if word.iter().any(|c| letter(*c).is_none()) || word.len() > 8 {
        return None;
    }
    let t = trace(&word);
    let mut split_fail = 0u64;
    for cut in 0..=word.len() {
        let (u, v) = (trace(&word[..cut]), trace(&word[cut..]));
        if [u[0] + v[0], u[1] + v[1], u[2] + v[2]] != t {
            split_fail += 1;
        }
    }
    let mut perms = BTreeSet::new();
    permutations(&word, &mut perms);
    let perm_fail = perms.iter().filter(|p| trace(p) != t).count();
    let (mut declared, mut ordered) = (false, false);
    for c in &word {
        if *c == b'D' {
            declared = true;
        } else if *c == b'A' && declared {
            ordered = true;
        }
    }
    Some(format!(
        "events\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        arg,
        t[0],
        t[1],
        t[2],
        t[0] + t[1] + t[2],
        word.len(),
        (t[0] >= 1 && t[1] >= 1) as u8,
        ordered as u8,
        perms.len(),
        perm_fail,
        split_fail
    ))
}

fn triple(v: &[u64; 3]) -> String {
    format!("{},{},{}", v[0], v[1], v[2])
}

fn ledger(arg: &str) -> Option<String> {
    let mut ops: Vec<(char, usize, u64)> = Vec::new();
    if arg != "-" {
        for item in arg.split(',') {
            let mut p = item.split(':');
            let kind = p.next()?;
            let name = p.next()?;
            let count: u64 = p.next()?.parse().ok()?;
            if p.next().is_some() || !(kind == "g" || kind == "d") {
                return None;
            }
            let id = match name {
                "A" => 0,
                "B" => 1,
                "C" => 2,
                _ => return None,
            };
            ops.push((kind.chars().next()?, id, count));
        }
    }
    let (mut gen, mut dis) = ([0u64; 3], [0u64; 3]);
    let (mut status, mut fail) = ("ok", -1i64);
    for (idx, (kind, i, count)) in ops.iter().enumerate() {
        if *kind == 'g' {
            match gen[*i].checked_add(*count) {
                Some(v) => gen[*i] = v,
                None => {
                    status = "CountOverflow";
                    fail = idx as i64;
                    break;
                }
            }
        } else {
            if *count == 0 {
                continue;
            }
            if gen[*i] == 0 {
                status = "NeverGenerated";
                fail = idx as i64;
                break;
            }
            if *count > gen[*i] - dis[*i] {
                status = "OverDischarge";
                fail = idx as i64;
                break;
            }
            dis[*i] += *count;
        }
    }
    let out = [gen[0] - dis[0], gen[1] - dis[1], gen[2] - dis[2]];
    Some(format!(
        "ledger\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        arg,
        status,
        fail,
        triple(&gen),
        triple(&dis),
        triple(&out),
        (out == [0, 0, 0]) as u8
    ))
}

/// Replay one tab-separated public-input line: `laws\tk\tn`, `bounded\tk\tM`, `saturating\tcap`, `events\tword`, `ledger\tops`.
pub fn replay(input: &str) -> Option<String> {
    let parts: Vec<&str> = input.split('\t').collect();
    match (parts[0], parts.len()) {
        ("laws", 3) => {
            let (k, n): (usize, u64) = (parts[1].parse().ok()?, parts[2].parse().ok()?);
            if k > 4 || n > 6 || (n as f64).powi(3 * k as i32) > 3.0e6 {
                return None;
            }
            Some(laws(k, n))
        }
        ("bounded", 3) => {
            let (k, m): (usize, u64) = (parts[1].parse().ok()?, parts[2].parse().ok()?);
            if k > 4 || m > 8 || ((m + 1) as f64).powi(3 * k as i32) > 3.0e6 {
                return None;
            }
            Some(bounded(k, m))
        }
        ("saturating", 2) => {
            let cap: u64 = parts[1].parse().ok()?;
            if cap > 40 {
                return None;
            }
            Some(saturating(cap))
        }
        ("events", 2) => events(parts[1]),
        ("ledger", 2) => ledger(parts[1]),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_obligation_monoid_laws_hold_and_no_inverses() {
        assert_eq!(replay("laws\t2\t3").unwrap(), "laws\t2\t3\t9\t729\t0\t0\t0\t0\t0");
        assert_eq!(replay("laws\t1\t5").unwrap(), "laws\t1\t5\t5\t125\t0\t0\t0\t0\t0");
    }

    #[test]
    fn pfp_obligation_monoid_saturating_is_not_cancellative() {
        assert_eq!(replay("saturating\t3").unwrap(), "saturating\t3\t4\t64\t0\t0\t0\t20");
        assert_eq!(replay("saturating\t6").unwrap(), "saturating\t6\t7\t343\t0\t0\t0\t112");
    }

    #[test]
    fn pfp_obligation_monoid_bounded_combine_is_partially_associative() {
        assert_eq!(replay("bounded\t1\t6").unwrap(), "bounded\t1\t6\t7\t49\t28\t21\t343\t84\t0\t0");
        assert!(replay("bounded\t9\t9").is_none());
    }

    #[test]
    fn pfp_obligation_monoid_event_trace_forgets_order() {
        assert_eq!(replay("events\tAD").unwrap(), "events\tAD\t1\t1\t0\t2\t2\t1\t0\t2\t0\t0");
        assert_eq!(replay("events\tDARI").unwrap(), "events\tDARI\t1\t1\t2\t4\t4\t1\t1\t24\t0\t0");
        assert_eq!(replay("events\t-").unwrap(), "events\t-\t0\t0\t0\t0\t0\t0\t0\t1\t0\t0");
        assert!(replay("events\tXYZ").is_none());
    }

    #[test]
    fn pfp_obligation_monoid_ledger_refusals_and_overflow() {
        assert_eq!(replay("ledger\td:A:1").unwrap(), "ledger\td:A:1\tNeverGenerated\t0\t0,0,0\t0,0,0\t0,0,0\t1");
        assert_eq!(replay("ledger\td:A:0").unwrap(), "ledger\td:A:0\tok\t-1\t0,0,0\t0,0,0\t0,0,0\t1");
        assert_eq!(replay("ledger\tg:A:2,d:A:3").unwrap(), "ledger\tg:A:2,d:A:3\tOverDischarge\t1\t2,0,0\t0,0,0\t2,0,0\t0");
        assert_eq!(
            replay("ledger\tg:C:18446744073709551615,g:C:1").unwrap(),
            "ledger\tg:C:18446744073709551615,g:C:1\tCountOverflow\t1\t0,0,18446744073709551615\t0,0,0\t0,0,18446744073709551615\t0"
        );
        assert!(replay("ledger\tg:D:1").is_none());
    }
}
