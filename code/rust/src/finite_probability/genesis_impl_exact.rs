//! Exact scoped finite calculations; no physical admission or authority oracle.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::{Signed, ToPrimitive, Zero};
use std::collections::{BTreeMap, BTreeSet, VecDeque};
type G = (Q, Q);
type A = Vec<Vec<G>>;
fn n(k: i64) -> Q {
    Q::from_integer(k.into())
}
fn parse(s: &str) -> Q {
    let (a, b) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(a.parse::<BigInt>().unwrap(), b.parse::<BigInt>().unwrap())
}
fn int(v: &Q, lo: i64, hi: i64) -> i64 {
    assert!(v.is_integer());
    let k = v.to_integer().to_i64().unwrap();
    assert!(lo <= k && k <= hi);
    k
}
fn g(a: i64, b: i64) -> G {
    (n(a), n(b))
}
fn ga(z: &G, w: &G) -> G {
    (&z.0 + &w.0, &z.1 + &w.1)
}
fn gm(z: &G, w: &G, c: bool) -> G {
    (
        &z.0 * &w.0 - &z.1 * &w.1,
        &z.0 * &w.1 + &z.1 * &w.0 - if c { &z.1 * &w.1 } else { n(0) },
    )
}
fn gs(z: &G, c: bool) -> G {
    (&z.0 - if c { z.1.clone() } else { n(0) }, -&z.1)
}
fn gp(z: &G, k: i64, c: bool) -> G {
    let v = if k < 0 { gs(z, c) } else { z.clone() };
    (0..k.abs()).fold(g(1, 0), |a, _| gm(&a, &v, c))
}
fn pm(a: &A, b: &A, c: bool) -> A {
    (0..a.len())
        .map(|i| {
            (0..b[0].len())
                .map(|j| (0..b.len()).fold(g(0, 0), |z, k| ga(&z, &gm(&a[i][k], &b[k][j], c))))
                .collect()
        })
        .collect()
}
fn dag(a: &A, c: bool) -> A {
    (0..a[0].len())
        .map(|j| (0..a.len()).map(|i| gs(&a[i][j], c)).collect())
        .collect()
}
fn pf(a: &A) -> Vec<Q> {
    a.iter()
        .flatten()
        .flat_map(|z| [z.0.clone(), z.1.clone()])
        .collect()
}
fn mm(a: &[Vec<Q>], b: &[Vec<Q>]) -> Vec<Vec<Q>> {
    a.iter()
        .map(|r| {
            (0..b[0].len())
                .map(|j| r.iter().zip(b).map(|(x, s)| x * &s[j]).sum())
                .collect()
        })
        .collect()
}
fn fl(a: &[Vec<Q>]) -> Vec<Q> {
    a.iter().flatten().cloned().collect()
}
fn tr(a: &[Vec<Q>]) -> Vec<Vec<Q>> {
    (0..a[0].len())
        .map(|j| a.iter().map(|r| r[j].clone()).collect())
        .collect()
}
fn graph(m: i64, size: usize) -> BTreeSet<(usize, usize)> {
    (0..size)
        .flat_map(|i| (0..size).map(move |j| (i, j)))
        .filter(|(i, j)| m >> (size * i + j) & 1 == 1)
        .collect()
}
fn mask(e: &BTreeSet<(usize, usize)>, size: usize) -> i64 {
    e.iter().map(|(i, j)| 1_i64 << (size * i + j)).sum()
}
fn image(e: &BTreeSet<(usize, usize)>, f: &[usize]) -> BTreeSet<(usize, usize)> {
    e.iter().map(|(i, j)| (f[*i], f[*j])).collect()
}
fn legal(e: &BTreeSet<(usize, usize)>) -> bool {
    e.iter().all(|(i, j)| i != j)
}
fn integers(v: impl IntoIterator<Item = i64>) -> Vec<Q> {
    v.into_iter().map(n).collect()
}
fn permutations() -> [[usize; 3]; 6] {
    [
        [0, 1, 2],
        [0, 2, 1],
        [1, 0, 2],
        [1, 2, 0],
        [2, 0, 1],
        [2, 1, 0],
    ]
}
struct RegimeState {
    d: i64,
    flip: i64,
    forms: Vec<i64>,
    inst: BTreeSet<(i64, i64)>,
    rules: BTreeSet<i64>,
    req: BTreeSet<(i64, i64)>,
}

impl RegimeState {
    fn new() -> Self {
        Self {
            d: 0,
            flip: 0,
            forms: Vec::new(),
            inst: BTreeSet::new(),
            rules: BTreeSet::new(),
            req: BTreeSet::new(),
        }
    }

    fn step(&mut self, op: i64, a: i64, b: i64) -> bool {
        match op {
            0 => true,
            1 => {
                self.d += 1;
                true
            }
            2 => self.step_form(a),
            3 => self.step_inst(a, b),
            4 => self.step_rule(a),
            5 => self.step_req(a, b),
            6 => {
                self.flip = 1 - self.flip;
                true
            }
            _ => panic!("event code"),
        }
    }

    fn step_form(&mut self, a: i64) -> bool {
        if (1..=3).contains(&a) {
            self.forms.push(a);
            true
        } else {
            false
        }
    }

    fn step_inst(&mut self, a: i64, b: i64) -> bool {
        if (a as usize) >= self.forms.len() {
            return false;
        }
        let ar = self.forms[a as usize] as u32;
        let good = b < 4_i64.pow(ar) && (0..ar).all(|j| (b / 4_i64.pow(j)) % 4 < self.d);
        if good {
            self.inst.insert((a, b));
        }
        good
    }

    fn step_rule(&mut self, a: i64) -> bool {
        if (a as usize) < self.forms.len() {
            self.rules.insert(a);
            true
        } else {
            false
        }
    }

    fn step_req(&mut self, a: i64, b: i64) -> bool {
        if a < self.d && b < self.d && a != b {
            self.req.insert((a, b));
            true
        } else {
            false
        }
    }

    fn complexity(&self) -> i64 {
        self.d + self.forms.len() as i64 + self.inst.len() as i64 + self.rules.len() as i64 + self.req.len() as i64
    }
}

fn regime(h: &[(i64, i64, i64)], erase: bool) -> (Vec<i64>, Vec<i64>) {
    let mut state = RegimeState::new();
    let mut t = Vec::new();
    let mut failure = -1;
    for (i, &(op, a, b)) in h.iter().enumerate() {
        if erase && op == 0 {
            continue;
        }
        let ok = state.step(op, a, b);
        t.extend([state.complexity(), state.flip, ok as i64]);
        if !ok {
            failure = i as i64;
            break;
        }
    }
    let mut o = vec![
        failure,
        state.d,
        state.forms.len() as i64,
        state.inst.len() as i64,
        state.rules.len() as i64,
        state.req.len() as i64,
        state.flip,
    ];
    o.extend(state.forms);
    o.extend(state.inst.iter().flat_map(|(a, b)| [*a, *b]));
    o.extend(state.rules);
    o.extend(state.req.iter().flat_map(|(a, b)| [*a, *b]));
    (t, o)
}

fn toggle_directed_edge(mut f: BTreeSet<(usize, usize)>, i: usize, j: usize) -> i64 {
    if !f.remove(&(i, j)) {
        f.insert((i, j));
    }
    mask(&f, 3)
}

fn edge_toggles(e: &BTreeSet<(usize, usize)>, t: i64) -> Vec<(i64, i64)> {
    let mut next = Vec::new();
    for i in 0..3usize {
        for j in 0..3usize {
            if i != j && (t >> i & 1 == 1) && (t >> j & 1 == 1) {
                next.push((t, toggle_directed_edge(e.clone(), i, j)));
            }
        }
    }
    next
}

fn cost_graph(seed: i64, target_t: i64, target_e: i64) -> Vec<Q> {
    let mut initial = BTreeSet::from([(0, 1)]);
    if seed == 1 {
        initial.insert((1, 0));
    }
    let start = (3, mask(&initial, 3));
    let mut dist = BTreeMap::from([(start, 0)]);
    let mut todo = VecDeque::from([start]);
    while let Some((t, m)) = todo.pop_front() {
        let e = graph(m, 3);
        let mut next = edge_toggles(&e, t);
        if t == 3 {
            next.push((7, m));
        }
        for q in next {
            if !dist.contains_key(&q) {
                dist.insert(q, dist[&(t, m)] + 1);
                todo.push_back(q);
            }
        }
    }
    let target = graph(target_e, 3);
    assert!(
        legal(&target)
            && target
                .iter()
                .all(|(i, j)| target_t >> i & 1 == 1 && target_t >> j & 1 == 1)
    );
    let lost = initial.difference(&target).count() as i64;
    let size = target_t.count_ones() as i64 + target.len() as i64;
    let base = 2 + initial.len() as i64;
    let mut out = vec![
        dist.len() as i64,
        dist[&(target_t, target_e)],
        size,
        lost,
        base,
        size + 2 * lost - base,
    ];
    out.extend(dist.iter().flat_map(|((t, m), d)| [*t, *m, *d]));
    integers(out)
}

fn is_separated(forms: &[i64], d: i64, rule: bool, inst: &BTreeSet<Vec<i64>>) -> bool {
    let ar = forms[0] as usize;
    let limit = if ar == 1 { 1 } else { d };
    for hole in 0..ar {
        for tail in 0..limit {
            let member = |x| {
                let mut a = if ar == 1 { vec![] } else { vec![tail] };
                a.insert(hole, x);
                rule || inst.contains(&a)
            };
            if member(0) != member(1) {
                return true;
            }
        }
    }
    false
}

fn evaluate_separation_seq(seq: &[i64], args: &[Vec<i64>]) -> [i64; 4] {
    let mut forms = Vec::new();
    let mut inst = BTreeSet::new();
    let (mut d, mut arity, mut valid, mut rule) = (2, 0, true, false);
    for &item in seq {
        match item {
            0 => d += 1,
            1 | 2 => {
                forms.push(item);
                arity += item;
            }
            9 => rule = true,
            _ => {
                if forms.is_empty() {
                    valid = false;
                    break;
                }
                let a = args[item as usize - 3].clone();
                if a.len() != forms[0] as usize {
                    valid = false;
                    break;
                }
                inst.insert(a);
            }
        }
    }
    let sep = valid && !forms.is_empty() && is_separated(&forms, d, rule, &inst);
    [seq.len() as i64, valid as i64, sep as i64, arity]
}

fn build_separation_seqs() -> Vec<Vec<i64>> {
    let mut seqs = vec![vec![]];
    for i in 0..10 {
        seqs.push(vec![i]);
    }
    for i in 0..10 {
        for j in 0..10 {
            seqs.push(vec![i, j]);
        }
    }
    seqs
}

fn separation() -> Vec<Q> {
    let seqs = build_separation_seqs();
    let args = [
        vec![0],
        vec![1],
        vec![0, 0],
        vec![0, 1],
        vec![1, 0],
        vec![1, 1],
    ];
    let rows: Vec<[i64; 4]> = seqs
        .iter()
        .map(|seq| evaluate_separation_seq(seq, &args))
        .collect();
    let minimum = rows
        .iter()
        .filter(|r| r[1] == 1 && r[2] == 1)
        .map(|r| r[0])
        .min()
        .unwrap();
    let ties: Vec<_> = rows
        .iter()
        .enumerate()
        .filter(|(_, r)| r[1] == 1 && r[2] == 1 && r[0] == minimum)
        .map(|(i, _)| i as i64)
        .collect();
    let arity = ties.iter().map(|i| rows[*i as usize][3]).min().unwrap();
    let best: Vec<_> = ties
        .iter()
        .copied()
        .filter(|i| rows[*i as usize][3] == arity)
        .collect();
    let mut o = vec![rows.len() as i64];
    o.extend(rows.iter().flatten());
    o.extend([minimum, ties.len() as i64, arity, best.len() as i64]);
    o.extend(ties);
    o.extend(best);
    integers(o)
}

fn step_gauge_update(
    nv: usize,
    par: &[Option<(usize, usize)>],
    s: i64,
    gauge: &mut [Option<i64>],
) {
    for j in 0..nv {
        if let Some((i, k)) = par[j] {
            if gauge[j].is_none() && gauge[i].is_some() {
                gauge[j] = Some(gauge[i].unwrap() ^ (s >> k & 1));
            }
        }
    }
}

fn compute_gauge(
    nv: usize,
    roots: &[usize],
    par: &[Option<(usize, usize)>],
    s: i64,
) -> Vec<i64> {
    let mut gauge = vec![None; nv];
    for &r in roots {
        gauge[r] = Some(0_i64);
    }
    while gauge.iter().any(Option::is_none) {
        step_gauge_update(nv, par, s, &mut gauge);
    }
    gauge.into_iter().map(Option::unwrap).collect()
}

fn explore_bfs_tree(
    r: usize,
    adj: &[Vec<(usize, usize)>],
    seen: &mut [bool],
    par: &mut [Option<(usize, usize)>],
    tree: &mut Vec<usize>,
) {
    seen[r] = true;
    let mut todo = VecDeque::from([r]);
    while let Some(i) = todo.pop_front() {
        for &(j, k) in &adj[i] {
            if !seen[j] {
                seen[j] = true;
                par[j] = Some((i, k));
                tree.push(k);
                todo.push_back(j);
            }
        }
    }
}

fn normal(which: usize) -> Vec<Q> {
    let choices = [
        (3, vec![(0, 1), (1, 2), (2, 0)]),
        (3, vec![(0, 1), (1, 2)]),
        (4, vec![(0, 1), (1, 2), (2, 0)]),
        (4, vec![(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]),
    ];
    let (nv, e) = &choices[which];
    let nv = *nv;
    let mut adj = vec![vec![]; nv];
    for (k, &(i, j)) in e.iter().enumerate() {
        adj[i].push((j, k));
        adj[j].push((i, k));
    }
    let mut par = vec![None; nv];
    let mut seen = vec![false; nv];
    let mut roots = Vec::new();
    let mut tree = Vec::new();
    for r in 0..nv {
        if !seen[r] {
            roots.push(r);
            explore_bfs_tree(r, &adj, &mut seen, &mut par, &mut tree);
        }
    }
    let mut normals = Vec::new();
    let mut sizes = Vec::new();
    for s in 0..1_i64 << e.len() {
        let gauge = compute_gauge(nv, &roots, &par, s);
        let t = e
            .iter()
            .enumerate()
            .map(|(k, &(i, j))| ((s >> k & 1) ^ gauge[i] ^ gauge[j]) << k)
            .sum::<i64>();
        normals.push(t);
        let orbit: BTreeSet<_> = (0..1_i64 << nv)
            .map(|g| {
                s ^ e
                    .iter()
                    .enumerate()
                    .map(|(k, &(i, j))| ((g >> i & 1) ^ (g >> j & 1)) << k)
                    .sum::<i64>()
            })
            .collect();
        sizes.push(orbit.len() as i64);
    }
    let forms: BTreeSet<_> = normals.iter().copied().collect();
    let beta = e.len() + roots.len() - nv;
    let mut out = vec![
        nv as i64,
        e.len() as i64,
        roots.len() as i64,
        beta as i64,
        forms.len() as i64,
        1_i64 << beta,
    ];
    out.extend(tree.iter().map(|k| *k as i64));
    out.push(-1);
    out.extend(normals);
    out.extend(sizes);
    out.extend(forms);
    integers(out)
}
fn weyl_matrix(c: i64, d: i64, w: &G) -> A {
    (0..3)
        .map(|i| {
            (0..3)
                .map(|j| {
                    if i == (j + c) % 3 {
                        gp(w, d * j, true)
                    } else {
                        g(0, 0)
                    }
                })
                .collect()
        })
        .collect()
}

fn eval_weyl(x: &[Q]) -> Vec<Q> {
    assert_eq!(x.len(), 11);
    let a = int(&x[0], 0, 2);
    let b = int(&x[1], 0, 2);
    let a_mat: A = (0..3)
        .map(|i| (0..3).map(|j| (x[2 + 3 * i + j].clone(), n(0))).collect())
        .collect();
    let w = g(0, 1);
    let u = weyl_matrix(a, 0, &w);
    let v = weyl_matrix(0, b, &w);
    let comm = pm(
        &pm(&pm(&u, &v, true), &dag(&u, true), true),
        &dag(&v, true),
        true,
    );
    let basis: Vec<_> = (0..3)
        .flat_map(|i| (0..3).map(move |j| (i, j)))
        .map(|(i, j)| weyl_matrix(i, j, &w))
        .collect();
    let coef: Vec<G> = basis
        .iter()
        .map(|b| {
            let t = pm(&dag(b, true), &a_mat, true);
            let z = (0..3).fold(g(0, 0), |s, i| ga(&s, &t[i][i]));
            (z.0 / n(3), z.1 / n(3))
        })
        .collect();
    let recovered: A = (0..3)
        .map(|i| {
            (0..3)
                .map(|j| {
                    coef.iter()
                        .zip(&basis)
                        .fold(g(0, 0), |s, (c, b)| ga(&s, &gm(c, &b[i][j], true)))
                })
                .collect()
        })
        .collect();
    let gram: A = basis
        .iter()
        .map(|b| {
            basis
                .iter()
                .map(|c| {
                    let t = pm(&dag(b, true), c, true);
                    (0..3).fold(g(0, 0), |s, i| ga(&s, &t[i][i]))
                })
                .collect()
        })
        .collect();
    let phase = gp(&w, -a * b, true);
    let mut o = pf(&comm);
    o.extend([phase.0, phase.1]);
    o.extend(coef.into_iter().flat_map(|z| [z.0, z.1]));
    o.extend(pf(&recovered));
    o.extend(pf(&gram));
    o
}

fn eval_duality(x: &[Q]) -> Vec<Q> {
    assert_eq!(x.len(), 2);
    let mass = x[0].abs() + x[1].abs();
    let vals: Vec<Q> = (-1..=1)
        .flat_map(|u| (-1..=1).map(move |v| (u, v)))
        .map(|(u, v)| n(u) * &x[0] + n(v) * &x[1])
        .collect();
    let maximum = vals.iter().max().unwrap().clone();
    let mut o = vec![mass.clone()];
    o.extend(vals);
    o.extend([maximum.clone(), mass - maximum]);
    o
}

fn eval_separation(x: &[Q]) -> Vec<Q> {
    assert_eq!(x, vec![n(0)]);
    separation()
}

fn eval_distinct(x: &[Q]) -> Vec<Q> {
    let m = int(&x[0], 0, 15);
    let mut rows = Vec::new();
    let mut allowed = Vec::new();
    for k in 0..16 {
        let r = [
            legal(&graph(k, 2)) as i64,
            (k & 2 != 0) as i64,
            (k & 4 != 0) as i64,
        ];
        if r[0] == 1 && r[1] == 1 {
            allowed.push(k);
        }
        rows.extend(r);
    }
    let tail = rows[m as usize * 3..m as usize * 3 + 3].to_vec();
    rows.push(allowed.len() as i64);
    rows.extend(allowed);
    rows.extend(tail);
    integers(rows)
}

fn eval_regime_ops(x: &[Q]) -> Vec<Q> {
    assert!(x.len() % 3 == 0 && x.len() <= 30);
    let h: Vec<_> = x
        .chunks(3)
        .map(|z| {
            let o = int(&z[0], 0, 6);
            (o, int(&z[1], 0, 255), int(&z[2], 0, 255))
        })
        .collect();
    let (t, o) = regime(&h, false);
    let (te, oe) = regime(&h, true);
    let mut v = vec![t.len() as i64, o.len() as i64];
    v.extend(t);
    v.extend(o);
    v.extend([te.len() as i64, oe.len() as i64]);
    v.extend(te);
    v.extend(oe);
    integers(v)
}

fn eval_fewest(x: &[Q]) -> Vec<Q> {
    let seed = int(&x[0], 0, 1);
    let t = int(&x[1], 3, 7);
    assert!(t == 3 || t == 7);
    cost_graph(seed, t, int(&x[2], 0, 511))
}

fn eval_obstruction(x: &[Q]) -> Vec<Q> {
    let e = graph(int(&x[0], 0, 511), 3);
    assert!(legal(&e));
    let u = int(&x[1], 0, 2) as usize;
    let v = int(&x[2], 0, 2) as usize;
    assert_ne!(u, v);
    let f: Vec<_> = (0..3).map(|i| if i == v { u } else { i }).collect();
    let merged = image(&e, &f);
    let mut clean = e.clone();
    clean.remove(&(u, v));
    clean.remove(&(v, u));
    let left = image(&clean, &f);
    let mut right = merged.clone();
    right.remove(&(u, u));
    let mut o = vec![
        mask(&merged, 3),
        legal(&merged) as i64,
        (!e.contains(&(u, v)) && !e.contains(&(v, u))) as i64,
        mask(&left, 3),
        mask(&right, 3),
        (left == right) as i64,
    ];
    for i in 0..3 {
        for j in 0..3 {
            let mut q = e.clone();
            q.insert((i, j));
            o.push(legal(&q) as i64);
        }
    }
    integers(o)
}

fn eval_rename(x: &[Q]) -> Vec<Q> {
    let e = graph(int(&x[0], 0, 511), 3);
    let u = int(&x[1], 0, 2) as usize;
    let v = int(&x[2], 0, 2) as usize;
    assert_ne!(u, v);
    let mut out = Vec::new();
    for p in permutations() {
        let f: Vec<_> = (0..3).map(|i| if i == v { u } else { i }).collect();
        let g: Vec<_> = (0..3).map(|i| if i == p[v] { p[u] } else { i }).collect();
        out.extend(p.iter().map(|z| *z as i64));
        out.extend([
            mask(&image(&e, &p), 3),
            mask(&image(&image(&e, &f), &p), 3),
            mask(&image(&image(&e, &p), &g), 3),
            (legal(&e) == legal(&image(&e, &p))) as i64,
        ]);
    }
    integers(out)
}

fn eval_sameness(x: &[Q]) -> Vec<Q> {
    assert_eq!(x.len(), 8);
    let v: Vec<_> = x.iter().map(|z| int(z, 0, 5)).collect();
    let d: Vec<_> = (0..4).map(|i| v[i] - v[i + 4]).collect();
    let normal: Vec<_> = d
        .iter()
        .map(|z| (*z).max(0))
        .chain(d.iter().map(|z| (-z).max(0)))
        .collect();
    let tog: Vec<_> = (0..4).map(|i| v[i].min(v[i + 4])).collect();
    let mut all = BTreeSet::new();
    for k in 0..256 {
        all.insert(
            (0..4)
                .map(|i| (k >> i & 1) - (k >> (i + 4) & 1))
                .collect::<Vec<i64>>(),
        );
    }
    let canonical: BTreeSet<_> = all
        .iter()
        .map(|z| {
            let r: Vec<_> = z.iter().rev().copied().collect();
            z.clone().min(r)
        })
        .collect();
    let mut o = d.clone();
    o.extend(normal.iter());
    o.extend(tog.iter());
    o.extend([
        v.iter().sum(),
        normal.iter().sum(),
        2 * tog.iter().sum::<i64>(),
        all.len() as i64,
        canonical.len() as i64,
    ]);
    o.extend(d);
    integers(o)
}

fn eval_mss0(x: &[Q]) -> Vec<Q> {
    let s = int(&x[0], 0, 10);
    let node = int(&x[1], 0, 10);
    integers([(s > 0 || node == 0) as i64, 0, 0])
}

fn round_float53(v: i64) -> i64 {
    let bits = 64 - (v as u64).leading_zeros();
    let k = bits.saturating_sub(53);
    let step = 1_i64 << k;
    let (q, r) = (v / step, v % step);
    let tie = (2 * r > step) || (2 * r == step && q % 2 == 1);
    (q + tie as i64) * step
}

fn eval_float(x: &[Q]) -> Vec<Q> {
    let a = int(&x[0], 0, 1_i64 << 55);
    let b = int(&x[1], 0, 1_i64 << 55);
    let (a1, b1) = (round_float53(a), round_float53(b));
    integers([a - b, a1, b1, (a1 == b1) as i64, (a == b) as i64, 0])
}

fn eval_pairing(x: &[Q]) -> Vec<Q> {
    if x.len() != 5 {
        panic!("arity");
    }
    let a = &x[0];
    let b = &x[1];
    let d = &x[2];
    let u = &x[3];
    let v = &x[4];
    assert!(
        a + d == n(1)
            && a >= &n(0)
            && d >= &n(0)
            && a * d >= b * b
            && u * u + v * v == n(1)
    );
    let p = a * u * u + n(2) * b * u * v + d * v * v;
    let de = a * u * u + d * v * v;
    vec![
        u * u,
        u * v,
        u * v,
        v * v,
        p.clone(),
        de.clone(),
        &p - de,
        n(2) * &p * &p - p,
        n(0),
        n(1),
        n(0),
        n(1),
        -n(1) / n(8),
    ]
}

fn realify_c(a: Q, b: Q) -> Vec<Vec<Q>> {
    vec![vec![a.clone(), -&b], vec![b, a]]
}

fn kron_product(a: &[Vec<Q>], b: &[Vec<Q>]) -> Vec<Vec<Q>> {
    (0..4)
        .map(|i| {
            (0..4)
                .map(|j| &a[i / 2][j / 2] * &b[i % 2][j % 2])
                .collect()
        })
        .collect()
}

fn eval_realify(x: &[Q]) -> Vec<Q> {
    if x.len() != 4 {
        panic!("arity");
    }
    let a = &x[0];
    let b = &x[1];
    let c = &x[2];
    let d = &x[3];
    let aa = realify_c(a.clone(), b.clone());
    let bb = realify_c(c.clone(), d.clone());
    let pp = mm(&aa, &bb);
    let cc = realify_c(a * c - b * d, a * d + b * c);
    let m = vec![vec![n(1), n(0), n(0), n(-1)], vec![n(0), n(1), n(1), n(0)]];
    let j = realify_c(n(0), n(1));
    let eye = realify_c(n(1), n(0));
    let l = kron_product(&j, &eye);
    let h = kron_product(&eye, &j);
    let dif: Vec<Vec<Q>> = l
        .iter()
        .zip(h)
        .map(|(r, s)| r.iter().zip(s).map(|(a, b)| a - b).collect())
        .collect();
    let t = vec![vec![a * c], vec![a * d], vec![b * c], vec![b * d]];
    let mut o = fl(&aa);
    o.extend(fl(&bb));
    o.extend(fl(&pp));
    o.extend(fl(&cc));
    o.extend(fl(&m));
    o.extend(fl(&mm(&m, &dif)));
    o.extend(fl(&mm(&m, &tr(&m))));
    o.extend(fl(&mm(&m, &t)));
    o
}

fn eval_amplitude(x: &[Q]) -> Vec<Q> {
    assert_eq!(x.len(), 10);
    let e: Vec<_> = x[..6].iter().map(|z| int(z, -8, 8)).collect();
    let es = [
        e[0],
        e[1],
        e[2],
        e[0] + e[4] - e[3],
        e[1] + e[5] - e[4],
        e[2] + e[3] - e[5],
    ];
    let u = (n(3) / n(5), n(4) / n(5));
    let z = (&x[6] + &x[8], &x[7] + &x[9]);
    let t = gm(&gp(&u, e[3], false), &z, false);
    let norm = |z: &G| &z.0 * &z.0 + &z.1 * &z.1;
    let mut o: Vec<Q> = es
        .iter()
        .flat_map(|k| {
            let z = gp(&u, *k, false);
            [z.0, z.1]
        })
        .collect();
    for k in [es[..3].iter().sum(), es[3..].iter().sum()] {
        let z = gp(&u, k, false);
        o.extend([z.0, z.1]);
    }
    o.extend([norm(&z), norm(&t), norm(&z) * norm(&z), norm(&t) * norm(&t)]);
    for k in 1..=8 {
        let z = gp(&g(3, 4), k, false);
        o.extend([
            n(z.0.to_integer().to_i64().unwrap().rem_euclid(5)),
            n(z.1.to_integer().to_i64().unwrap().rem_euclid(5)),
        ]);
    }
    o
}

fn eval_normal(x: &[Q]) -> Vec<Q> {
    normal(int(&x[0], 0, 3) as usize)
}

fn eval_lggr(x: &[Q]) -> Vec<Q> {
    let size = int(&x[0], 1, 6);
    let m = int(&x[1], 0, (1 << size) - 1);
    let mass = int(&x[2], 0, 100);
    let counts: Vec<i64> = (0..1_i64 << size)
        .map(|s| {
            (0..size)
                .filter(|i| ((s >> i & 1) ^ (s >> ((i + 1) % size) & 1)) == (m >> i & 1))
                .count() as i64
        })
        .collect();
    let sections: Vec<_> = counts
        .iter()
        .enumerate()
        .filter(|(_, z)| **z == size)
        .map(|(i, _)| i as i64)
        .collect();
    let parity = m.count_ones() as i64 % 2;
    let mut o = integers([
        parity,
        sections.len() as i64,
        (mass == 0 || parity == 0) as i64,
    ]);
    o.extend(integers(counts));
    o.extend(integers(sections));
    let weights: Vec<Q> = (0..8)
        .map(|s| if s == 0 || s == 7 { n(0) } else { n(1) / n(6) })
        .collect();
    o.extend(weights.iter().cloned());
    for i in 0..3 {
        o.push(
            (0..8)
                .map(|s| &weights[s] * n(((s >> i & 1) ^ (s >> ((i + 1) % 3) & 1)) as i64))
                .sum(),
        );
    }
    o.push(n(2) / n(3));
    for s in 0..8 {
        let sat = (0..3)
            .map(|i| (s >> i & 1) ^ (s >> ((i + 1) % 3) & 1))
            .sum::<i64>();
        o.push(n(2 - sat) / n(3));
    }
    o
}

fn eval_thymus(x: &[Q]) -> Vec<Q> {
    let panel = int(&x[0], 0, 15);
    let p = int(&x[1], 0, 15);
    let e = int(&x[2], 0, 15);
    let mut o = Vec::new();
    for s in 0_i64..16 {
        o.extend([
            (s & p == 0) as i64,
            (s & e).count_ones() as i64,
            (s & p != 0 || s & e == 0) as i64,
        ]);
    }
    let bad: Vec<_> = (0..4)
        .filter(|i| e >> i & 1 == 1 && p >> i & 1 == 0)
        .collect();
    o.extend([
        bad.is_empty() as i64,
        bad.first().copied().unwrap_or(-1),
        (panel & p == 0) as i64,
        (panel & e).count_ones() as i64,
        ((15 ^ panel) & e).count_ones() as i64,
    ]);
    integers(o)
}

fn eval_discrete_genesis(kind: &str, x: &[Q]) -> Option<Vec<Q>> {
    match kind {
        "weyl" => Some(eval_weyl(x)),
        "duality" => Some(eval_duality(x)),
        "separation" => Some(eval_separation(x)),
        "distinct" => Some(eval_distinct(x)),
        "noreturn" | "events" | "erasure" | "supply" => Some(eval_regime_ops(x)),
        "fewest" => Some(eval_fewest(x)),
        _ => None,
    }
}

fn eval_combinatorial_genesis(kind: &str, x: &[Q]) -> Option<Vec<Q>> {
    match kind {
        "obstruction" => Some(eval_obstruction(x)),
        "rename" => Some(eval_rename(x)),
        "sameness" => Some(eval_sameness(x)),
        "mss0" => Some(eval_mss0(x)),
        "float" => Some(eval_float(x)),
        "pairing" => Some(eval_pairing(x)),
        _ => None,
    }
}

fn eval_algebraic_genesis(kind: &str, x: &[Q]) -> Option<Vec<Q>> {
    match kind {
        "realify" => Some(eval_realify(x)),
        "amplitude" => Some(eval_amplitude(x)),
        "normal" => Some(eval_normal(x)),
        "lggr" => Some(eval_lggr(x)),
        "thymus" => Some(eval_thymus(x)),
        _ => None,
    }
}

fn dispatch_genesis_eval(kind: &str, x: &[Q]) -> Vec<Q> {
    if let Some(res) = eval_discrete_genesis(kind, x) {
        return res;
    }
    if let Some(res) = eval_combinatorial_genesis(kind, x) {
        return res;
    }
    if let Some(res) = eval_algebraic_genesis(kind, x) {
        return res;
    }
    panic!("unknown scoped operation")
}

/// Panics outside the declared bounded input grammar; intended for exact local replay.
pub fn evaluate(kind: &str, values: &[String]) -> Vec<String> {
    let x: Vec<Q> = values.iter().map(|s| parse(s)).collect();
    let out = dispatch_genesis_eval(kind, &x);
    out.iter().map(ToString::to_string).collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    fn v(k: &str, x: &[&str]) -> Vec<Q> {
        evaluate(k, &x.iter().map(|s| s.to_string()).collect::<Vec<_>>())
            .iter()
            .map(|s| parse(s))
            .collect()
    }
    #[test]
    fn genesis_weyl() {
        let a = v(
            "weyl",
            &["1", "1", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        );
        assert_eq!(
            &a[38..56],
            &[
                n(1),
                n(0),
                n(2),
                n(0),
                n(3),
                n(0),
                n(4),
                n(0),
                n(5),
                n(0),
                n(6),
                n(0),
                n(7),
                n(0),
                n(8),
                n(0),
                n(9),
                n(0)
            ]
        );
    }
    #[test]
    fn genesis_duality() {
        assert_eq!(*v("duality", &["-3", "4"]).last().unwrap(), n(0));
    }
    #[test]
    fn genesis_separation() {
        let a = v("separation", &["0"]);
        assert_eq!(a[445], n(2));
        assert_eq!(a[446], n(6));
        assert_eq!(a[448], n(2));
    }
    #[test]
    fn genesis_distinct() {
        let a = v("distinct", &["2"]);
        assert_eq!(&a[48..51], &[n(2), n(2), n(6)]);
    }
    #[test]
    fn genesis_noreturn() {
        let a = v("noreturn", &["1", "0", "0", "6", "0", "0", "6", "0", "0"]);
        assert_eq!(a[2], n(1));
        assert_eq!(a[5], n(1));
        assert_eq!(a[8], n(1));
    }
    #[test]
    fn genesis_events() {
        let a = v("events", &["2", "0", "0"]);
        assert_eq!(a[4], n(0));
        assert_eq!(a[5], n(0));
    }
    #[test]
    fn genesis_erasure() {
        let a = v("erasure", &["0", "99", "0", "1", "0", "0"]);
        assert_eq!(a[8], n(-1));
    }
    #[test]
    fn genesis_supply() {
        let a = v("supply", &["0", "1", "0"]);
        assert_eq!(&a[5..12], &[n(-1), n(0), n(0), n(0), n(0), n(0), n(0)]);
    }
    #[test]
    fn genesis_fewest() {
        let a = v("fewest", &["0", "3", "0"]);
        assert_eq!(&a[..6], &[n(68), n(1), n(2), n(1), n(3), n(1)]);
    }
    #[test]
    fn genesis_obstruction() {
        let a = v("obstruction", &["2", "0", "1"]);
        assert_eq!(&a[..6], &[n(1), n(0), n(0), n(0), n(0), n(1)]);
    }
    #[test]
    fn genesis_rename() {
        let a = v("rename", &["2", "0", "1"]);
        for r in a.chunks(7) {
            assert_eq!(r[4], r[5]);
        }
    }
    #[test]
    fn genesis_sameness() {
        let a = v("sameness", &["1", "0", "0", "0", "1", "0", "0", "0"]);
        assert_eq!(&a[19..21], &[n(81), n(45)]);
    }
    #[test]
    fn genesis_mss0() {
        assert_eq!(v("mss0", &["0", "1"]), vec![n(0), n(0), n(0)]);
    }
    #[test]
    fn genesis_float() {
        let a = v("float", &["9007199254740993", "9007199254740992"]);
        assert_eq!(&a[3..], &[n(1), n(0), n(0)]);
    }
    #[test]
    fn genesis_pairing() {
        let a = v("pairing", &["1/2", "1/2", "1/2", "3/5", "4/5"]);
        assert!(a[4] > a[5]);
        assert_eq!(a[12], -n(1) / n(8));
    }
    #[test]
    fn genesis_realify() {
        let a = v("realify", &["1", "2", "3", "4"]);
        assert_eq!(&a[8..12], &a[12..16]);
        assert!(a[24..32].iter().all(Zero::is_zero));
    }
    #[test]
    fn genesis_amplitude() {
        let a = v(
            "amplitude",
            &["1", "2", "3", "-1", "0", "1", "1", "2", "3", "4"],
        );
        assert_eq!(&a[12..14], &a[14..16]);
        assert_eq!(a[16], a[17]);
    }
    #[test]
    fn genesis_normal() {
        for k in 0..4 {
            let a = v("normal", &[&k.to_string()]);
            assert_eq!(a[4], a[5]);
        }
    }
    #[test]
    fn genesis_lggr() {
        assert_eq!(&v("lggr", &["3", "7", "1"])[..3], &[n(1), n(0), n(0)]);
    }
    #[test]
    fn genesis_thymus() {
        let a = v("thymus", &["3", "0", "2"]);
        assert_eq!(&a[48..], &[n(0), n(1), n(1), n(1), n(0)]);
    }
    #[test]
    fn genesis_binary64_diagnostic() {
        for k in -8_i64..=8 {
            let a = (1_i64 << 53) + k;
            let o = v("float", &[&a.to_string(), "0"]);
            assert_eq!(o[1], n((a as f64) as i64));
        }
    }
}
