//! Primitive-difference axioms A1-A10 and the admission kernel: exhaustive finite models on carriers of 1, 2, 3 points.
//!
//! Exact integer replay of `code/python/src/qm/pfp_primdiff_axioms.py` for PFP batch 01, node PG-PRIMDIFF-AXIOMS.
//! The predicates are a TRANSCRIPTION (the pinned Rust source names ten axioms and realises only A1, A3, A5 and the
//! triad rule); independence on tiny carriers is not a derivation of the list. AuthorityEffect: None.
use std::collections::{BTreeMap, BTreeSet};

const NAMES: [&str; 10] = [
    "A01NonIdentification",
    "A02UnentailedAdmission",
    "A03EvaluationRelation",
    "A04DirectedEvaluationCarrier",
    "A05NilpotentCoboundary",
    "A06QuotientDefectPurity",
    "A07DescendedClosureMap",
    "A08TriadTrichotomy",
    "A09ObserverSelectedMetric",
    "A10AntiReificationFirewall",
];
const STATUS: [&str; 10] = [
    "state_predicate",
    "not_a_state_predicate",
    "theorem_true_in_every_structure",
    "state_predicate",
    "state_predicate",
    "checked_on_named_complexes",
    "equivalent_to_A5",
    "checked_on_named_complexes",
    "checked_on_named_complexes",
    "state_predicate",
];

type Edges = Vec<(usize, usize)>;

fn relation(n: usize, mask: u32) -> Edges {
    let mut out = Vec::new();
    for u in 0..n {
        for v in 0..n {
            if mask >> (u * n + v) & 1 == 1 {
                out.push((u, v));
            }
        }
    }
    out
}

fn faces_of(n: usize, f: bool) -> Vec<(usize, usize, usize)> {
    if f && n == 3 {
        vec![(0, 1, 2)]
    } else {
        Vec::new()
    }
}

fn closure(n: usize, edges: &Edges) -> Vec<Vec<bool>> {
    let mut r = vec![vec![false; n]; n];
    for i in 0..n {
        r[i][i] = true;
    }
    for &(u, v) in edges {
        r[u][v] = true;
    }
    for k in 0..n {
        for i in 0..n {
            for j in 0..n {
                if r[i][k] && r[k][j] {
                    r[i][j] = true;
                }
            }
        }
    }
    r
}

fn a3_holds(n: usize, edges: &Edges) -> bool {
    let r = closure(n, edges);
    let refl = (0..n).all(|i| r[i][i]);
    let trans = (0..n).all(|i| (0..n).all(|j| (0..n).all(|k| !(r[i][j] && r[j][k]) || r[i][k])));
    refl && trans && edges.iter().all(|&(u, v)| r[u][v])
}

/// d1 o d0 as an integer matrix product.
fn a5_holds(n: usize, edges: &Edges, faces: &[(usize, usize, usize)]) -> bool {
    if faces.is_empty() || edges.is_empty() {
        return true;
    }
    let d0: Vec<Vec<i64>> = edges
        .iter()
        .map(|&(u, v)| {
            let mut row = vec![0i64; n];
            row[v] += 1;
            row[u] -= 1;
            row
        })
        .collect();
    for &(a, b, c) in faces {
        let mut row = vec![0i64; edges.len()];
        if let Some(i) = edges.iter().position(|&e| e == (b, c)) {
            row[i] += 1;
        }
        if let Some(i) = edges.iter().position(|&e| e == (a, c)) {
            row[i] -= 1;
        }
        if let Some(i) = edges.iter().position(|&e| e == (a, b)) {
            row[i] += 1;
        }
        for j in 0..n {
            let s: i64 = (0..edges.len()).map(|k| row[k] * d0[k][j]).sum();
            if s != 0 {
                return false;
            }
        }
    }
    true
}

/// d1 vanishes on the unit potentials.
fn a7_holds(n: usize, edges: &Edges, faces: &[(usize, usize, usize)]) -> bool {
    for v in 0..n {
        let phi: Vec<i64> = (0..n).map(|x| (x == v) as i64).collect();
        let psi = |e: (usize, usize)| -> i64 {
            if edges.contains(&e) {
                phi[e.1] - phi[e.0]
            } else {
                0
            }
        };
        for &(a, b, c) in faces {
            if psi((b, c)) - psi((a, c)) + psi((a, b)) != 0 {
                return false;
            }
        }
    }
    true
}

fn well_formed(edges: &Edges, faces: &[(usize, usize, usize)]) -> bool {
    faces.iter().all(|&(a, b, c)| edges.contains(&(a, b)) && edges.contains(&(b, c)) && edges.contains(&(a, c)))
}

fn a1_holds(d: &Edges) -> bool {
    d.iter().all(|&(u, v)| u != v)
}

fn a4_holds(e: &Edges) -> bool {
    e.iter().all(|&(u, v)| u != v) && e.iter().all(|&(u, v)| !e.contains(&(v, u)))
}

/// Bits of a joint signature: 0 A1, 1 A3, 2 A4, 3 A5, 4 A7, 5 A10, 6 W.
fn joint(n: usize) -> BTreeMap<u8, u64> {
    let mut d_hist: BTreeMap<bool, u64> = BTreeMap::new();
    for mask in 0u32..(1u32 << (n * n)) {
        *d_hist.entry(a1_holds(&relation(n, mask))).or_insert(0) += 1;
    }
    let mut ef_hist: BTreeMap<u8, u64> = BTreeMap::new();
    for mask in 0u32..(1u32 << (n * n)) {
        let edges = relation(n, mask);
        let fs: Vec<bool> = if n == 3 { vec![false, true] } else { vec![false] };
        for f in fs {
            let faces = faces_of(n, f);
            let sig = (a3_holds(n, &edges) as u8)
                | (a4_holds(&edges) as u8) << 1
                | (a5_holds(n, &edges, &faces) as u8) << 2
                | (a7_holds(n, &edges, &faces) as u8) << 3
                | (well_formed(&edges, &faces) as u8) << 4;
            *ef_hist.entry(sig).or_insert(0) += 1;
        }
    }
    let mut out: BTreeMap<u8, u64> = BTreeMap::new();
    for (&a1, &cd) in &d_hist {
        for (&ef, &ce) in &ef_hist {
            for a10 in [true, false] {
                let key = (a1 as u8)
                    | (ef & 1) << 1
                    | ((ef >> 1) & 1) << 2
                    | ((ef >> 2) & 1) << 3
                    | ((ef >> 3) & 1) << 4
                    | (a10 as u8) << 5
                    | ((ef >> 4) & 1) << 6;
                *out.entry(key).or_insert(0) += cd * ce;
            }
        }
    }
    out
}

fn axiom_line(k: usize) -> Option<String> {
    if !(1..=10).contains(&k) {
        return None;
    }
    let mut counts = [-1i64; 3];
    if matches!(k, 1 | 3 | 4 | 5 | 7 | 10) {
        let position = match k {
            1 => 0,
            3 => 1,
            4 => 2,
            5 => 3,
            7 => 4,
            _ => 5,
        };
        for n in 1..=3 {
            counts[n - 1] = joint(n).iter().filter(|(key, _)| (**key >> position) & 1 == 1).map(|(_, c)| *c as i64).sum();
        }
    }
    Some(format!("axiom\t{}\t{}\t{}\t{}\t{}\t{}", k, NAMES[k - 1], STATUS[k - 1], counts[0], counts[1], counts[2]))
}

fn models_line(n: usize) -> Option<String> {
    if !(1..=3).contains(&n) {
        return None;
    }
    let hist = joint(n);
    let total: u64 = hist.values().sum();
    let mut violate = [0u64; 6];
    let mut jointly = 0u64;
    let mut all_hold = 0u64;
    let (mut w_models, mut a5_not_w) = (0u64, 0u64);
    let mut patterns: BTreeSet<u8> = BTreeSet::new();
    let mut equal = true;
    for (&key, &c) in &hist {
        let bits = key & 0x3f;
        patterns.insert(bits);
        if bits == 0x3f {
            all_hold += c;
        }
        let missing: Vec<usize> = (0..6).filter(|i| (bits >> i) & 1 == 0).collect();
        if missing.len() == 1 {
            violate[missing[0]] += c;
        }
        if missing == [3, 4] {
            jointly += c;
        }
        if (key >> 6) & 1 == 1 {
            w_models += c;
        }
        if (key >> 3) & 1 == 1 && (key >> 6) & 1 == 0 {
            a5_not_w += c;
        }
        if (key >> 3) & 1 != (key >> 4) & 1 {
            equal = false;
        }
    }
    Some(format!(
        "models\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        n, total, all_hold, violate[0], violate[1], violate[2], violate[3], violate[4], violate[5], jointly, equal as i32, w_models, a5_not_w,
        patterns.len()
    ))
}

fn unentailed_line(n: usize) -> Option<String> {
    if !(2..=3).contains(&n) {
        return None;
    }
    let mut d_irreflexive = 0u64;
    let mut with_pair: BTreeSet<u64> = BTreeSet::new();
    let mut ef_models = 0u64;
    for mask in 0u32..(1u32 << (n * n)) {
        let edges = relation(n, mask);
        let fs: Vec<bool> = if n == 3 { vec![false, true] } else { vec![false] };
        for f in fs {
            let faces = faces_of(n, f);
            if a3_holds(n, &edges) && a4_holds(&edges) && a5_holds(n, &edges, &faces) && a7_holds(n, &edges, &faces) {
                ef_models += 1;
            }
        }
        if a1_holds(&edges) {
            d_irreflexive += 1;
        }
    }
    let mut diag_in_model = 0u64;
    for u in 0..n {
        for v in 0..n {
            if u == v {
                continue;
            }
            let count = (0u32..(1u32 << (n * n))).filter(|&m| a1_holds(&relation(n, m)) && relation(n, m).contains(&(u, v))).count() as u64;
            with_pair.insert(count * ef_models);
        }
    }
    for mask in 0u32..(1u32 << (n * n)) {
        let d = relation(n, mask);
        if a1_holds(&d) && d.iter().any(|&(u, v)| u == v) {
            diag_in_model += 1;
        }
    }
    if with_pair.len() != 1 {
        return None;
    }
    let with_each = *with_pair.iter().next().unwrap();
    let models = d_irreflexive * ef_models;
    Some(format!(
        "unentailed\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        n,
        models,
        n * (n - 1),
        with_each,
        models - with_each,
        diag_in_model,
        ef_models
    ))
}

#[derive(PartialEq, Eq, Clone, Copy)]
enum Outcome {
    Ok,
    A1,
    Carrier,
}

fn kernel_admit(carrier: usize, store: &mut Vec<(usize, usize, u8)>, a: usize, b: usize, token: u8) -> Outcome {
    if a == b {
        return Outcome::A1;
    }
    if a >= carrier || b >= carrier {
        return Outcome::Carrier;
    }
    store.push((a, b, token));
    Outcome::Ok
}

fn kernel_line(n: usize) -> Option<String> {
    if !(1..=6).contains(&n) {
        return None;
    }
    let (mut ok, mut a1, mut carrier) = (0u64, 0u64, 0u64);
    let mut token_irrelevant = true;
    for a in 0..=n {
        for b in 0..=n {
            let mut outcomes = Vec::new();
            for token in 0..2u8 {
                let o = kernel_admit(n, &mut Vec::new(), a, b, token);
                outcomes.push(o as u8);
                match o {
                    Outcome::Ok => ok += 1,
                    Outcome::A1 => a1 += 1,
                    Outcome::Carrier => carrier += 1,
                }
            }
            token_irrelevant = token_irrelevant && outcomes[0] == outcomes[1];
        }
    }
    let mut store = Vec::new();
    let first = kernel_admit(n, &mut store, 0, 1, 0);
    let second = kernel_admit(n, &mut store, 0, 1, 0);
    let reverse = kernel_admit(n, &mut store, 1, 0, 1);
    let duplicates = second == Outcome::Ok && store.iter().filter(|&&x| x == (0, 1, 0)).count() == 2;
    Some(format!(
        "kernel\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        n,
        2 * (n + 1) * (n + 1),
        ok,
        a1,
        carrier,
        token_irrelevant as i32,
        (first == Outcome::Ok) as i32,
        duplicates as i32,
        (reverse == Outcome::Ok) as i32,
        (kernel_admit(n, &mut Vec::new(), n, n, 0) == Outcome::A1) as i32
    ))
}

fn closure_line(n: usize) -> Option<String> {
    if !(1..=3).contains(&n) {
        return None;
    }
    let mut seen: BTreeSet<Vec<bool>> = BTreeSet::new();
    let (mut all_preorders, mut contains, mut reach_equal) = (true, true, true);
    let total = 1u32 << (n * n);
    for mask in 0..total {
        let edges = relation(n, mask);
        let r = closure(n, &edges);
        all_preorders = all_preorders && a3_holds(n, &edges);
        contains = contains && edges.iter().all(|&(u, v)| r[u][v]);
        seen.insert(r.iter().flatten().cloned().collect());
        for s in 0..n {
            let mut visited = vec![false; n];
            visited[s] = true;
            let mut stack = vec![s];
            while let Some(x) = stack.pop() {
                for &(u, v) in &edges {
                    if u == x && !visited[v] {
                        visited[v] = true;
                        stack.push(v);
                    }
                }
            }
            reach_equal = reach_equal && (0..n).all(|t| r[s][t] == visited[t]);
        }
    }
    Some(format!(
        "closure\t{}\t{}\t{}\t{}\t{}\t{}",
        n,
        total,
        seen.len(),
        all_preorders as i32,
        contains as i32,
        reach_equal as i32
    ))
}

// ------------------------------------------------------------------ triads
fn parse_tuples(text: &str, arity: usize) -> Option<Vec<Vec<usize>>> {
    if text == "-" {
        return Some(Vec::new());
    }
    let mut out = Vec::new();
    for part in text.split(',') {
        let v: Option<Vec<usize>> = part.split('-').map(|x| x.parse().ok()).collect();
        let v = v?;
        if v.len() != arity {
            return None;
        }
        out.push(v);
    }
    Some(out)
}

fn subsets(items: &[usize], size: usize) -> Vec<Vec<usize>> {
    if size == 0 {
        return vec![Vec::new()];
    }
    let mut out = Vec::new();
    for (i, &x) in items.iter().enumerate() {
        for mut rest in subsets(&items[i + 1..], size - 1) {
            let mut t = vec![x];
            t.append(&mut rest);
            out.push(t);
        }
    }
    out
}

fn root(uf: &[usize], mut x: usize) -> usize {
    while uf[x] != x {
        x = uf[x];
    }
    x
}

fn phi1(n: usize, edges: &Edges, h: &[i64]) -> i64 {
    let real: Vec<usize> = (0..edges.len()).filter(|&i| edges[i].0 != edges[i].1).collect();
    let mut parent: Vec<usize> = (0..n).collect();
    let mut comps = n;
    for &i in &real {
        let (ru, rv) = (root(&parent, edges[i].0), root(&parent, edges[i].1));
        if ru != rv {
            parent[ru] = rv;
            comps -= 1;
        }
    }
    let size = n - comps;
    let mut best: Option<i64> = None;
    for tree in subsets(&real, size) {
        let mut uf: Vec<usize> = (0..n).collect();
        let mut acyclic = true;
        for &i in &tree {
            let (ru, rv) = (root(&uf, edges[i].0), root(&uf, edges[i].1));
            if ru == rv {
                acyclic = false;
                break;
            }
            uf[ru] = rv;
        }
        if !acyclic {
            continue;
        }
        let mut phi: Vec<Option<i64>> = vec![None; n];
        for start in 0..n {
            if phi[start].is_some() {
                continue;
            }
            phi[start] = Some(0);
            let mut stack = vec![start];
            while let Some(x) = stack.pop() {
                for &i in &tree {
                    let (u, v) = edges[i];
                    if u == x && phi[v].is_none() {
                        phi[v] = Some(phi[u].unwrap() + h[i]);
                        stack.push(v);
                    } else if v == x && phi[u].is_none() {
                        phi[u] = Some(phi[v].unwrap() - h[i]);
                        stack.push(u);
                    }
                }
            }
        }
        let cost: i64 = (0..edges.len()).map(|i| (h[i] - (phi[edges[i].1].unwrap() - phi[edges[i].0].unwrap())).abs()).sum();
        best = Some(match best {
            Some(b) if b <= cost => b,
            _ => cost,
        });
    }
    best.unwrap_or(0)
}

fn coboundary(edges: &Edges, faces: &[(usize, usize, usize)], h: &[i64]) -> Vec<i64> {
    faces
        .iter()
        .map(|&(a, b, c)| {
            let get = |e: (usize, usize)| edges.iter().position(|&x| x == e).map(|i| h[i]).unwrap_or(0);
            get((b, c)) - get((a, c)) + get((a, b))
        })
        .collect()
}

fn permutations(n: usize) -> Vec<Vec<usize>> {
    if n == 0 {
        return vec![Vec::new()];
    }
    let mut out = Vec::new();
    for p in permutations(n - 1) {
        for pos in 0..=p.len() {
            let mut q = p.clone();
            q.insert(pos, n - 1);
            out.push(q);
        }
    }
    out
}

fn triad_line(name: &str, n: usize, edges_text: &str, faces_text: &str) -> Option<String> {
    if n == 0 || n > 3 {
        return None;
    }
    let edge_list = parse_tuples(edges_text, 2)?;
    let face_list = parse_tuples(faces_text, 3)?;
    let edges: Edges = edge_list.iter().map(|v| (v[0], v[1])).collect();
    let faces: Vec<(usize, usize, usize)> = face_list.iter().map(|v| (v[0], v[1], v[2])).collect();
    if edges.iter().any(|&(u, v)| u >= n || v >= n) || faces.iter().any(|&(a, b, c)| a >= n || b >= n || c >= n) || edges.len() > 6 {
        return None;
    }
    let m = edges.len();
    let cochains = 3usize.pow(m as u32);
    let (mut ce, mut cc, mut cr, mut cx) = (0u64, 0u64, 0u64, 0u64);
    let (mut phi_sum, mut phi_max) = (0i64, 0i64);
    let (mut gauge, mut relabel) = (true, true);
    let perms = permutations(n);
    for hi in 0..cochains {
        let h: Vec<i64> = (0..m).map(|k| (hi / 3usize.pow(k as u32) % 3) as i64 - 1).collect();
        let p = phi1(n, &edges, &h);
        phi_sum += p;
        phi_max = phi_max.max(p);
        let closed = coboundary(&edges, &faces, &h).iter().all(|&x| x == 0);
        let exact = p == 0;
        match (exact, closed) {
            (true, true) => ce += 1,
            (true, false) => cx += 1,
            (false, true) => cc += 1,
            (false, false) => cr += 1,
        }
        for pi in 0..3usize.pow(n as u32) {
            let psi: Vec<i64> = (0..n).map(|k| (pi / 3usize.pow(k as u32) % 3) as i64 - 1).collect();
            let shifted: Vec<i64> = (0..m).map(|i| h[i] + psi[edges[i].1] - psi[edges[i].0]).collect();
            if phi1(n, &edges, &shifted) != p {
                gauge = false;
            }
        }
        for perm in &perms {
            let moved: Edges = edges.iter().map(|&(u, v)| (perm[u], perm[v])).collect();
            if phi1(n, &moved, &h) != p {
                relabel = false;
            }
        }
    }
    let nilpotent = a5_holds(n, &edges, &faces);
    let wf = well_formed(&edges, &faces);
    let fmt_edges = |xs: &Vec<Vec<usize>>| -> String {
        if xs.is_empty() {
            "-".to_string()
        } else {
            xs.iter().map(|t| t.iter().map(|x| x.to_string()).collect::<Vec<_>>().join("-")).collect::<Vec<_>>().join(",")
        }
    };
    Some(format!(
        "triad\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        name,
        n,
        fmt_edges(&edge_list),
        fmt_edges(&face_list),
        cochains,
        ce,
        cc,
        cr,
        cx,
        cx,
        phi_sum,
        phi_max,
        gauge as i32,
        relabel as i32,
        nilpotent as i32,
        wf as i32
    ))
}

/// Replay one tab-separated public-input line (axiom / models / unentailed / kernel / closure / triad).
pub fn replay(input: &str) -> Option<String> {
    let p: Vec<&str> = input.split('\t').collect();
    match *p.first()? {
        "axiom" if p.len() == 2 => axiom_line(p[1].parse().ok()?),
        "models" if p.len() == 2 => models_line(p[1].parse().ok()?),
        "unentailed" if p.len() == 2 => unentailed_line(p[1].parse().ok()?),
        "kernel" if p.len() == 2 => kernel_line(p[1].parse().ok()?),
        "closure" if p.len() == 2 => closure_line(p[1].parse().ok()?),
        "triad" if p.len() == 5 => triad_line(p[1], p[2].parse().ok()?, p[3], p[4]),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn cols(line: &str) -> Vec<String> {
        line.split('\t').map(|s| s.to_string()).collect()
    }

    #[test]
    fn pfp_primdiff_axioms_model_counts_and_independence() {
        let m3 = cols(&replay("models\t3").unwrap());
        assert_eq!(&m3[2..4], ["1048576", "2304"]);
        assert_eq!(&m3[4..10], ["16128", "0", "38656", "0", "0", "2304"]);
        assert_eq!(m3[10], "1152");
        assert_eq!(cols(&replay("models\t2").unwrap())[10], "0");
        assert_eq!(cols(&replay("models\t1").unwrap())[3], "1");
    }

    #[test]
    fn pfp_primdiff_axioms_axiom_table_statuses_and_counts() {
        assert_eq!(replay("axiom\t1").unwrap(), "axiom\t1\tA01NonIdentification\tstate_predicate\t4\t128\t131072");
        assert_eq!(replay("axiom\t2").unwrap(), "axiom\t2\tA02UnentailedAdmission\tnot_a_state_predicate\t-1\t-1\t-1");
        assert_eq!(cols(&replay("axiom\t5").unwrap())[4..], cols(&replay("axiom\t7").unwrap())[4..]);
        assert_eq!(cols(&replay("axiom\t5").unwrap())[4..], ["8", "512", "655360"]);
    }

    #[test]
    fn pfp_primdiff_axioms_kernel_checks_a1_then_carrier_and_not_the_token() {
        assert_eq!(replay("kernel\t2").unwrap(), "kernel\t2\t18\t4\t6\t8\t1\t1\t1\t1\t1");
        assert_eq!(replay("kernel\t3").unwrap(), "kernel\t3\t32\t12\t8\t12\t1\t1\t1\t1\t1");
        let mut store = Vec::new();
        assert!(kernel_admit(2, &mut store, 0, 1, 0) == Outcome::Ok);
        assert!(kernel_admit(2, &mut store, 5, 5, 0) == Outcome::A1);
        assert!(kernel_admit(2, &mut store, 0, 5, 0) == Outcome::Carrier);
    }

    #[test]
    fn pfp_primdiff_axioms_closure_counts_are_preorder_counts() {
        assert_eq!(replay("closure\t1").unwrap(), "closure\t1\t2\t1\t1\t1\t1");
        assert_eq!(replay("closure\t2").unwrap(), "closure\t2\t16\t4\t1\t1\t1");
        assert_eq!(replay("closure\t3").unwrap(), "closure\t3\t512\t29\t1\t1\t1");
    }

    #[test]
    fn pfp_primdiff_axioms_triad_cells_and_refusals() {
        assert_eq!(
            replay("triad\tbroken_face\t3\t0-1,1-2\t0-1-2").unwrap(),
            "triad\tbroken_face\t3\t0-1,1-2\t0-1-2\t9\t3\t0\t0\t6\t6\t0\t0\t1\t1\t0\t0"
        );
        let filled = cols(&replay("triad\tfilled_triangle\t3\t0-1,1-2,0-2\t0-1-2").unwrap());
        assert_eq!(&filled[6..11], ["7", "0", "20", "0", "0"]);
        assert_eq!(phi1(3, &vec![(0, 1), (1, 2), (0, 2)], &[1, 1, 0]), 2);
        assert!(replay("triad\tx\t4\t-\t-").is_none());
    }
}
