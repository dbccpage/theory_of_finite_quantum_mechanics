//! Scoped exact finite boundary controls, never a physical certification oracle.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::{Signed, ToPrimitive, Zero};
use std::collections::BTreeSet;
type M = Vec<Vec<Q>>;
fn n(v: i64) -> Q {
    Q::from_integer(v.into())
}
fn q(s: &str) -> Q {
    let (a, b) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(a.parse::<BigInt>().unwrap(), b.parse::<BigInt>().unwrap())
}
fn sq(a: &Q) -> Q {
    a * a
}
fn integer(v: &Q, lo: i64, hi: i64) -> i64 {
    assert!(v.is_integer());
    let k = v.to_integer().to_i64().unwrap();
    assert!(lo <= k && k <= hi);
    k
}
fn bits(v: &[Q]) -> Vec<i64> {
    v.iter().map(|z| integer(z, 0, 1)).collect()
}
fn mm(a: &M, b: &M) -> M {
    (0..a.len())
        .map(|i| {
            (0..b[0].len())
                .map(|j| (0..b.len()).map(|k| &a[i][k] * &b[k][j]).sum())
                .collect()
        })
        .collect()
}
fn tr(a: &M) -> M {
    (0..a[0].len())
        .map(|j| (0..a.len()).map(|i| a[i][j].clone()).collect())
        .collect()
}
fn flat(a: &M) -> Vec<Q> {
    a.iter().flatten().cloned().collect()
}
fn trace(a: &M) -> Q {
    (0..a.len()).map(|i| a[i][i].clone()).sum()
}
fn ma(a: &M, b: &M, k: i64) -> M {
    a.iter()
        .zip(b)
        .map(|(r, s)| r.iter().zip(s).map(|(x, y)| x + n(k) * y).collect())
        .collect()
}
fn scale(a: &M, k: &Q) -> M {
    a.iter()
        .map(|r| r.iter().map(|z| z * k).collect())
        .collect()
}
fn eye(k: usize) -> M {
    (0..k)
        .map(|i| (0..k).map(|j| n((i == j) as i64)).collect())
        .collect()
}
fn rot(t: &Q) -> M {
    let d = n(1) + sq(t);
    let r = (n(1) - sq(t)) / &d;
    let s = n(2) * t / d;
    vec![vec![r.clone(), -&s], vec![s, r]]
}
fn conj(u: &M, a: &M) -> M {
    mm(&mm(u, a), &tr(u))
}
fn parity(v: usize) -> usize {
    let b: Vec<usize> = (0..9).map(|i| v >> i & 1).collect();
    let cs = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
    ];
    cs.iter()
        .enumerate()
        .map(|(j, c)| ((b[c[0]] + b[c[1]] + b[c[2]]) % 2) << j)
        .sum()
}
fn solutions(mask: usize) -> Vec<usize> {
    (0..512).filter(|v| (parity(*v) ^ 32) & mask == 0).collect()
}
fn quat(c: i64) -> [i64; 4] {
    let mut v = [0; 4];
    v[(c % 4) as usize] = if c >= 4 { -1 } else { 1 };
    v
}
fn qm(a: [i64; 4], b: [i64; 4]) -> [i64; 4] {
    let [w, x, y, z] = a;
    let [v, p, q, r] = b;
    [
        w * v - x * p - y * q - z * r,
        w * p + x * v + y * r - z * q,
        w * q - x * r + y * v + z * p,
        w * r + x * q - y * p + z * v,
    ]
}
fn qi(a: [i64; 4]) -> [i64; 4] {
    [a[0], -a[1], -a[2], -a[3]]
}
fn qc(a: [i64; 4]) -> i64 {
    (0..8).find(|c| quat(*c) == a).unwrap()
}
fn proxy(k: i64) -> Vec<Q> {
    let mut a = vec![vec![n(0), n(1)], vec![n(1), n(0)]];
    let mut b = vec![vec![n(1), n(0)], vec![n(0), n(-1)]];
    let h = n(1) / n(2);
    let mut rho = vec![vec![h.clone(), n(0)], vec![n(0), h.clone()]];
    let mut t = vec![vec![n(0), n(-1)], vec![n(1), n(0)]];
    let (local, joint) = if k == 0 { (8, 9) } else { (15, 15) };
    let p = if k == 1 { 4 } else { 2 };
    let i3 = 3_i64.pow(p) - 3 * 2_i64.pow(p) + 3;
    if k == 2 {
        a = vec![vec![n(1), n(0)], vec![n(0), n(-1)]];
        b = vec![vec![n(2), n(0)], vec![n(0), n(3)]];
    }
    if k == 3 {
        rho[0][1] = n(3) / n(4);
        rho[1][0] = n(3) / n(4);
    }
    if k == 4 {
        t = vec![vec![n(1), n(0)], vec![n(0), n(0)]];
    }
    let comm = ma(&mm(&a, &b), &mm(&b, &a), -1);
    let orth = mm(&tr(&t), &t);
    let det = &t[0][0] * &t[1][1] - &t[0][1] * &t[1][0];
    let probes = vec![
        rho[0][0].clone(),
        rho[1][1].clone(),
        &rho[0][0] - &rho[0][1] - &rho[1][0] + &rho[1][1],
    ];
    let flags = vec![
        n((local == joint) as i64),
        n((i3 == 0) as i64),
        n(flat(&comm).iter().any(|z| !z.is_zero()) as i64),
        n((trace(&rho) == n(1) && probes.iter().all(|z| z >= &n(0))) as i64),
        n((orth == eye(2) && det == n(1)) as i64),
    ];
    [
        vec![n(local), n(joint), n(i3)],
        flat(&a),
        flat(&b),
        flat(&rho),
        flat(&t),
        flat(&comm),
        probes,
        flat(&orth),
        vec![det],
        flags,
    ]
    .concat()
}
fn eval_registry(x: &[Q]) -> Vec<Q> {
    assert_eq!(x.len(), 9);
    let caps: Vec<i64> = x[..7].iter().map(|z| integer(z, 0, 15)).collect();
    let a = &x[7];
    let b = &x[8];
    assert!(a >= &n(0) && b >= &n(0));
    let flags: Vec<Q> = caps.iter().map(|c| n((*c == 15) as i64)).collect();
    let mut v = flags.clone();
    v.extend([
        flags.into_iter().sum(),
        a.clone(),
        a.min(b).clone(),
        a - a.min(b),
    ]);
    v
}

fn eval_uniqueness(x: &[Q]) -> Vec<Q> {
    let k = integer(&x[0], 1, 4);
    let table: Vec<Q> = (0..3)
        .flat_map(|_| vec![n(0), n(1) / n(2), n(1) / n(2), n(0)])
        .collect();
    let normal: Vec<Q> = table.chunks(4).map(|r| r.iter().cloned().sum()).collect();
    let mut marginal = vec![];
    for row in table.chunks(4) {
        marginal.push(&row[0] + &row[1]);
        marginal.push(&row[2] + &row[3]);
    }
    let count = (0..8)
        .filter(|j| {
            let a = j & 1;
            let b = j >> 1 & 1;
            let c = j >> 2 & 1;
            a != b && b != c && c != a
        })
        .count();
    let extra: Vec<Q> = (0..k)
        .flat_map(|_| table.iter().map(|z| z / n(k)))
        .collect();
    [
        table,
        normal,
        marginal,
        vec![n(count as i64), n(k), n(2 * k)],
        extra,
    ]
    .concat()
}

fn eval_cochain(x: &[Q]) -> Vec<Q> {
    let [a, b, d, e, f, g, t, u] = x else {
        panic!("arity")
    };
    let rho = vec![vec![a.clone(), b.clone()], vec![b.clone(), d.clone()]];
    let eff = vec![vec![e.clone(), f.clone()], vec![f.clone(), g.clone()]];
    let uu = rot(t);
    let vv = rot(u);
    let r1 = conj(&uu, &rho);
    let e1 = conj(&uu, &eff);
    let r2 = conj(&vv, &r1);
    let e2 = conj(&vv, &e1);
    let r3 = conj(&mm(&vv, &uu), &rho);
    let z0 = trace(&mm(&rho, &eff));
    let z1 = trace(&mm(&r1, &e1));
    let z2 = trace(&mm(&r2, &e2));
    [
        flat(&r1),
        flat(&e1),
        flat(&r2),
        flat(&r3),
        vec![
            z0.clone(),
            z1.clone(),
            z2.clone(),
            &z1 - &z0,
            &z2 - &z1,
            &z0 - &z2,
            (&z1 - &z0) + (&z2 - &z1) + (&z0 - &z2),
        ],
    ]
    .concat()
}

fn eval_survival(x: &[Q]) -> Vec<Q> {
    assert_eq!(x.len(), 3);
    let b = bits(x);
    let mut v = x.to_vec();
    v.extend([
        n(b.iter().all(|z| *z == 1) as i64),
        n(b[0] * b[1]),
        n(b[0] * b[1] * (1 - b[2])),
    ]);
    v
}

fn eval_relative(x: &[Q]) -> Vec<Q> {
    let [a, b, c, d, u, v, w] = x else {
        panic!("arity")
    };
    assert_eq!(sq(a) + sq(b), n(1));
    assert_eq!(sq(c) + sq(d), n(1));
    let psi = vec![a.clone(), n(0), b * c, b * d];
    let rho: M = psi
        .iter()
        .map(|s| psi.iter().map(|t| s * t).collect())
        .collect();
    let red: M = (0..2)
        .map(|i| {
            (0..2)
                .map(|j| &rho[2 * i][2 * j] + &rho[2 * i + 1][2 * j + 1])
                .collect()
        })
        .collect();
    let eff = vec![vec![u.clone(), v.clone()], vec![v.clone(), w.clone()]];
    let dephase = vec![vec![red[0][0].clone(), n(0)], vec![n(0), red[1][1].clone()]];
    let full = trace(&mm(&red, &eff));
    let diag = trace(&mm(&dephase, &eff));
    let off = n(2) * (a * b * c).abs();
    [
        psi,
        flat(&rho),
        flat(&red),
        vec![
            off.clone(),
            full.clone(),
            diag.clone(),
            full - diag,
            v.abs() * off,
        ],
    ]
    .concat()
}

fn eval_threshold(x: &[Q]) -> Vec<Q> {
    assert_eq!(x.len(), 9);
    let la = integer(&x[0], 0, 10000);
    let mu = integer(&x[1], 0, 10000);
    let mut state = integer(&x[2], 0, 10000);
    let k = integer(&x[3], 0, 32);
    let b = bits(&x[4..]);
    let mut v = vec![n(state)];
    for _ in 0..k {
        state = (state + la - mu).max(0);
        v.push(n(state));
    }
    v.extend([
        n((b.iter().all(|z| *z == 1) && mu >= la) as i64),
        n((la - mu).max(0)),
    ]);
    v
}

fn eval_syndrome(x: &[Q]) -> Vec<Q> {
    let size = integer(&x[0], 1, 7) as usize;
    assert!(size % 2 == 1);
    let t = (size - 1) / 2;
    let mut v = vec![n(size as i64), n(t as i64), n((2 * t) as i64)];
    let mut small = 0;
    let mut zero = 0;
    for e in 0_usize..1 << size {
        let b: Vec<usize> = (0..size).map(|j| e >> j & 1).collect();
        let wt: usize = b.iter().sum();
        let sy: usize = (0..size - 1).map(|j| (b[j] ^ b[j + 1]) << j).sum();
        let logical = (wt > size / 2) as i64;
        small += i64::from(wt <= t && logical == 0);
        zero += i64::from(sy == 0);
        v.extend([n(wt as i64), n(sy as i64), n(logical)]);
    }
    v.extend([n(small), n(zero)]);
    v
}

fn eval_packet(x: &[Q]) -> Vec<Q> {
    assert_eq!(x.len(), 7);
    let b = bits(&x[..4]);
    let workload = integer(&x[4], 0, 1000000);
    let target = integer(&x[5], 1, 1000000);
    let claim = integer(&x[6], 0, 1);
    let missing = 4 - b.iter().sum::<i64>();
    let at = (workload >= target) as i64;
    let eligible = (missing == 0 && at == 1) as i64;
    let code = if claim == 1 && eligible == 0 {
        3
    } else if missing > 0 {
        0
    } else if at == 0 {
        1
    } else {
        2
    };
    let mut v = x[..4].to_vec();
    v.extend([n(missing), n(at), n(eligible), n(code)]);
    v
}

fn eval_q8(x: &[Q]) -> Vec<Q> {
    assert_eq!(x.len(), 5);
    let gs: Vec<[i64; 4]> = x.iter().map(|z| quat(integer(z, 0, 7))).collect();
    let edges = [
        qm(qi(gs[0]), gs[1]),
        qm(qi(gs[1]), gs[2]),
        qm(qi(gs[2]), gs[0]),
    ];
    let lp = qm(qm(edges[0], edges[1]), edges[2]);
    let c = qm(qm(qm(gs[3], gs[4]), qi(gs[3])), qi(gs[4]));
    let mut v: Vec<Q> = edges.iter().map(|z| n(qc(*z))).collect();
    v.extend([n(qc(lp)), n(qc(c))]);
    v.extend(lp.map(n));
    v.extend(c.map(n));
    v.extend([n(lp[0]), n(c[0])]);
    v
}

fn eval_parity(x: &[Q]) -> Vec<Q> {
    let mask = integer(&x[0], 0, 63) as usize;
    let sol: Vec<Vec<usize>> = (0..64).map(solutions).collect();
    let first = sol[mask].first().copied();
    let mut v: Vec<Q> = sol.iter().map(|a| n(a.len() as i64)).collect();
    v.extend([
        n(sol[mask].len() as i64),
        n(first.map(|v| v as i64).unwrap_or(-1)),
        n(first.map(|v| parity(v) as i64).unwrap_or(-1)),
    ]);
    v.extend((0..6).map(|j| n(sol[63 ^ (1 << j)][0] as i64)));
    v
}

fn eval_born(x: &[Q]) -> Vec<Q> {
    let [a, b, t] = x else {
        panic!("arity")
    };
    assert!(sq(a) + sq(b) > n(0));
    let mut out = vec![];
    for p in [1, 2, 4] {
        let aa = a.abs().pow(p);
        let bb = b.abs().pow(p);
        let nn = &aa + &bb;
        out.extend([aa / &nn, bb / nn]);
    }
    let v = flat(&mm(&rot(t), &vec![vec![a.clone()], vec![b.clone()]]));
    out.extend(v.clone());
    out.extend([
        sq(a) + sq(b),
        v.iter().map(sq).sum(),
        a.pow(4) + b.pow(4),
        v.iter().map(|z| z.pow(4)).sum(),
    ]);
    out
}

fn eval_synthesis(x: &[Q]) -> Vec<Q> {
    let k = integer(&x[0], 0, 3);
    let images: Vec<i64> = (0..4).map(|j| 2 * j % 4).collect();
    let mut v: Vec<Q> = images.iter().map(|j| n(*j)).collect();
    v.extend((0..4).map(|j| n(images.contains(&j) as i64)));
    v.extend([n(2 * k % 4), n(2 * ((k + 2) % 4) % 4)]);
    for a in 0_i64..4 {
        for b in 0_i64..4 {
            v.push(n(
                (2 * ((a + b) % 4) - (2 * a % 4 + 2 * b % 4)).rem_euclid(4)
            ));
        }
    }
    v
}

fn eval_cascade(x: &[Q]) -> Vec<Q> {
    let [a, b] = x else {
        panic!("arity")
    };
    let aa = vec![vec![n(0), n(1)], vec![n(1), n(0)]];
    let bb = vec![vec![n(1), n(0)], vec![n(0), n(-1)]];
    [
        vec![
            sq(a) + sq(b),
            a.pow(4) + b.pow(4),
            sq(&(a + b)) - sq(a) - sq(b),
            n(2) * a * b,
        ],
        flat(&ma(&mm(&aa, &bb), &mm(&bb, &aa), -1)),
        vec![sq(a) + sq(b), sq(&(sq(a) + sq(b))) - (a.pow(4) + b.pow(4))],
    ]
    .concat()
}

fn eval_majorana(x: &[Q]) -> Vec<Q> {
    let [a, b] = x else {
        panic!("arity")
    };
    let g = vec![vec![a.clone(), n(0)], vec![n(0), -a]];
    let h = vec![vec![n(0), b.clone()], vec![b.clone(), n(0)]];
    let p = mm(&g, &h);
    let bb = ma(&eye(2), &p, 1);
    let den = n(1) + sq(&(a * b));
    let mats = vec![
        g.clone(),
        h.clone(),
        mm(&g, &g),
        mm(&h, &h),
        ma(&mm(&g, &h), &mm(&h, &g), 1),
        p.clone(),
        mm(&p, &p),
        mm(&bb, &bb),
        mm(&bb, &tr(&bb)),
        scale(&conj(&bb, &g), &(n(1) / &den)),
        scale(&conj(&bb, &h), &(n(1) / den)),
    ];
    mats.iter().flat_map(flat).collect()
}

fn eval_busch(x: &[Q]) -> Vec<Q> {
    let [a, b, c, d] = x else {
        panic!("arity")
    };
    let one = n(1) / n(6);
    let mut effects = vec![];
    for s in [1, -1] {
        effects.push(vec![one.clone(), n(s) / n(6), n(0), one.clone()]);
    }
    for s in [1, -1] {
        effects.push(vec![one.clone(), n(0), n(-s) / n(6), one.clone()]);
    }
    for s in [1, -1] {
        effects.push(vec![n(1 + s) / n(6), n(0), n(0), n(1 - s) / n(6)]);
    }
    let probs: Vec<Q> = effects
        .iter()
        .map(|e| a * &e[0] + d * &e[3] + n(2) * (b * &e[1] + c * &e[2]))
        .collect();
    let sums: Vec<Q> = (0..4)
        .map(|j| effects.iter().map(|e| e[j].clone()).sum())
        .collect();
    let total: Q = probs.iter().cloned().sum();
    let recon = vec![
        (&total + n(3) * (&probs[4] - &probs[5])) / n(2),
        n(3) * (&probs[0] - &probs[1]) / n(2),
        n(3) * (&probs[3] - &probs[2]) / n(2),
        (&total - n(3) * (&probs[4] - &probs[5])) / n(2),
    ];
    [
        effects.into_iter().flatten().collect::<Vec<Q>>(),
        sums,
        probs,
        recon,
        vec![
            a * d - sq(b) - sq(c),
            a + n(2) * d - n(2) * b - n(2) * c,
            total,
        ],
    ]
    .concat()
}

fn eval_choi(x: &[Q]) -> Vec<Q> {
    let p = &x[0];
    let mut j = scale(&eye(4), &((n(1) - p) / n(2)));
    let omega = [n(1), n(0), n(0), n(1)];
    let pure: M = omega
        .iter()
        .map(|a| omega.iter().map(|b| p * a * b).collect())
        .collect();
    j = ma(&j, &pure, 1);
    let vs = vec![
        vec![n(1), n(0), n(0), n(1)],
        vec![n(1), n(0), n(0), n(-1)],
        vec![n(0), n(1), n(1), n(0)],
        vec![n(0), n(1), n(-1), n(0)],
    ];
    let ev = vec![
        (n(1) + n(3) * p) / n(2),
        (n(1) - p) / n(2),
        (n(1) - p) / n(2),
        (n(1) - p) / n(2),
    ];
    let pt: M = (0..2)
        .map(|i| {
            (0..2)
                .map(|k| &j[2 * i][2 * k] + &j[2 * i + 1][2 * k + 1])
                .collect()
        })
        .collect();
    let images: Vec<Q> = vs
        .iter()
        .flat_map(|v| flat(&mm(&j, &v.iter().map(|z| vec![z.clone()]).collect())))
        .collect();
    let rank = ev.iter().filter(|z| !z.is_zero()).count();
    let minimum = ev.iter().min().unwrap().clone();
    [
        flat(&j),
        flat(&pt),
        ev,
        images,
        vec![n(rank as i64), minimum, trace(&j)],
    ]
    .concat()
}

fn eval_maps(x: &[Q]) -> Vec<Q> {
    let z = &x[0];
    let e = sq(z) - n(27) / n(8) * z;
    let opt = n(27) / n(16);
    let t = sq(&opt);
    let v = -n(4) * &opt + n(5) / n(8) * &opt;
    let eo = &t + &v;
    vec![
        z.clone(),
        e.clone(),
        opt.clone(),
        t.clone(),
        v.clone(),
        eo.clone(),
        n(2) * t + v,
        e - eo,
        sq(&(z - opt)),
        -n(4) + n(5) / n(4),
    ]
}

fn eval_tensor(x: &[Q]) -> Vec<Q> {
    let [a, b, c, d] = x else {
        panic!("arity")
    };
    vec![
        a * c,
        a * d,
        b * c,
        b * d,
        a * c,
        -(a * d),
        b * c,
        -(b * d),
        (c + d) * a,
        (c + d) * b,
        (c - d) * a,
        (c - d) * b,
        a.clone(),
        b.clone(),
        a.clone(),
        b.clone(),
        a.clone(),
        b.clone(),
        -a,
        -b,
    ]
}

fn eval_torsion(x: &[Q]) -> Vec<Q> {
    assert_eq!(x.len(), 10);
    let nn = integer(&x[0], 1, 5);
    let e: Vec<i64> = x[1..6].iter().map(|z| integer(z, 0, nn - 1)).collect();
    let g: Vec<i64> = x[6..].iter().map(|z| integer(z, 0, nn - 1)).collect();
    let edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)];
    let shift: Vec<i64> = edges
        .iter()
        .enumerate()
        .map(|(k, (i, j))| (e[k] + g[*j] - g[*i]).rem_euclid(nn))
        .collect();
    let canon = |a: &[i64]| {
        (
            (a[3] + a[0] + a[1] + a[2]).rem_euclid(nn),
            (a[4] - a[0] - a[1]).rem_euclid(nn),
        )
    };
    let mut forms = BTreeSet::new();
    for label in 0..nn.pow(5) {
        let mut m = label;
        let mut a = vec![];
        for _ in 0..5 {
            a.push(m % nn);
            m /= nn;
        }
        forms.insert(canon(&a));
    }
    let c = canon(&e);
    let d = canon(&shift);
    let mut out: Vec<Q> = shift.into_iter().map(n).collect();
    out.extend([
        n(c.0),
        n(c.1),
        n(d.0),
        n(d.1),
        n(forms.len() as i64),
        n(nn * nn),
        n((e[0] + e[1] - e[4]).rem_euclid(nn)),
        n((-c.1).rem_euclid(nn)),
        n((0..nn).any(|k| 2 * k % nn != 0) as i64),
    ]);
    for (a, b) in forms {
        out.extend([n(a), n(b)]);
    }
    out
}

fn eval_algebraic(kind: &str, x: &[Q]) -> Option<Vec<Q>> {
    match kind {
        "registry" => Some(eval_registry(x)),
        "uniqueness" => Some(eval_uniqueness(x)),
        "cochain" => Some(eval_cochain(x)),
        "survival" => Some(eval_survival(x)),
        "relative" => Some(eval_relative(x)),
        "threshold" => Some(eval_threshold(x)),
        "syndrome" => Some(eval_syndrome(x)),
        _ => None,
    }
}

fn eval_structural(kind: &str, x: &[Q]) -> Option<Vec<Q>> {
    match kind {
        "packet" => Some(eval_packet(x)),
        "q8" => Some(eval_q8(x)),
        "parity" => Some(eval_parity(x)),
        "born" => Some(eval_born(x)),
        "synthesis" => Some(eval_synthesis(x)),
        "cascade" => Some(eval_cascade(x)),
        "majorana" => Some(eval_majorana(x)),
        _ => None,
    }
}

fn eval_geometric(kind: &str, x: &[Q]) -> Option<Vec<Q>> {
    match kind {
        "busch" => Some(eval_busch(x)),
        "choi" => Some(eval_choi(x)),
        "proxy" => Some(proxy(integer(&x[0], 0, 4))),
        "maps" => Some(eval_maps(x)),
        "tensor" => Some(eval_tensor(x)),
        "torsion" => Some(eval_torsion(x)),
        _ => None,
    }
}

pub fn evaluate(kind: &str, values: &[String]) -> Vec<String> {
    let x: Vec<Q> = values.iter().map(|s| q(s)).collect();
    let out: Vec<Q> = eval_algebraic(kind, &x)
        .or_else(|| eval_structural(kind, &x))
        .or_else(|| eval_geometric(kind, &x))
        .unwrap_or_else(|| panic!("unknown boundary operation"));
    out.into_iter()
        .map(|v| {
            if v.denom() == &1.into() {
                v.numer().to_string()
            } else {
                format!("{}/{}", v.numer(), v.denom())
            }
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    fn run(k: &str, s: &[&str]) -> Vec<Q> {
        evaluate(k, &s.iter().map(|x| x.to_string()).collect::<Vec<_>>())
            .iter()
            .map(|x| q(x))
            .collect()
    }
    #[test]
    fn boundaries_registry() {
        let v = run(
            "registry",
            &["12", "9", "11", "11", "7", "10", "15", "7", "5"],
        );
        assert_eq!(v[7], n(1));
        assert_eq!(v[10], n(2));
    }
    #[test]
    fn boundaries_uniqueness() {
        let v = run("uniqueness", &["1"]);
        assert_eq!(v[21], n(0));
        assert_eq!(v[12..15], [n(1), n(1), n(1)]);
    }
    #[test]
    fn boundaries_cochain() {
        let v = run("cochain", &["1/2", "1/4", "1/2", "1", "2", "3", "1/2", "2"]);
        assert_eq!(v[16], v[17]);
        assert_eq!(v[17], v[18]);
        assert_eq!(v[22], n(0));
    }
    #[test]
    fn boundaries_survival() {
        let v = run("survival", &["0", "0", "0"]);
        assert_eq!(v[3], n(0));
    }
    #[test]
    fn boundaries_relative() {
        let v = run("relative", &["3/5", "4/5", "0", "1", "1", "1", "2"]);
        assert_eq!(v[21], n(0));
        assert_eq!(&v[20] + &v[23], n(1));
        assert_eq!(v[27], n(0));
    }
    #[test]
    fn boundaries_threshold() {
        let v = run("threshold", &["5", "6", "3", "4", "1", "1", "1", "1", "1"]);
        assert_eq!(v[..5], [n(3), n(2), n(1), n(0), n(0)]);
        assert_eq!(v[5], n(1));
    }
    #[test]
    fn boundaries_syndrome() {
        let v = run("syndrome", &["1"]);
        assert!(v[2] < v[0]);
        assert_eq!(*v.last().unwrap(), n(2));
    }
    #[test]
    fn boundaries_packet() {
        let v = run("packet", &["1", "1", "1", "1", "100", "100", "0"]);
        assert_eq!(v[4], n(0));
        assert_eq!(v[6], n(1));
        assert_eq!(v[7], n(2));
    }
    #[test]
    fn boundaries_q8() {
        let v = run("q8", &["0", "1", "2", "1", "2"]);
        assert_eq!(v[3], n(0));
        assert_eq!(v[4], n(4));
        assert_eq!(*v.last().unwrap(), n(-1));
    }
    #[test]
    fn boundaries_parity() {
        let v = run("parity", &["63"]);
        assert_eq!(v[63], n(0));
        assert_eq!(v[64], n(0));
        assert_eq!(v[65], n(-1));
    }
    #[test]
    fn boundaries_born() {
        let v = run("born", &["3/5", "4/5", "0"]);
        assert_eq!(v[8], v[9]);
        assert_ne!(v[2], v[4]);
    }
    #[test]
    fn boundaries_synthesis() {
        let v = run("synthesis", &["0"]);
        assert_eq!(v[0], v[2]);
        assert_eq!(v[5], n(0));
        assert!(v[10..].iter().all(|q| q.is_zero()));
    }
    #[test]
    fn boundaries_cascade() {
        let v = run("cascade", &["3", "4"]);
        assert_eq!(v[2], v[3]);
        assert_eq!(v[9], n(288));
    }
    #[test]
    fn boundaries_majorana() {
        let v = run("majorana", &["1", "1"]);
        assert_eq!(v[24], n(-1));
        assert_eq!(v[27], n(-1));
        assert_eq!(v[16..20], vec![n(0); 4]);
    }
    #[test]
    fn boundaries_busch() {
        let v = run("busch", &["1/2", "3/10", "2/5", "1/2"]);
        assert_eq!(v[24..28], [n(1), n(0), n(0), n(1)]);
        assert_eq!(v[35], n(3) / n(10));
        assert_eq!(v[40], n(1));
    }
    #[test]
    fn boundaries_choi() {
        let v = run("choi", &["1"]);
        assert_eq!(v[40], n(1));
        assert_eq!(v[42], n(2));
    }
    #[test]
    fn boundaries_proxy() {
        let v = run("proxy", &["0"]);
        assert_eq!(v[31], n(0));
        assert_eq!(v[31..].iter().cloned().sum::<Q>(), n(4));
    }
    #[test]
    fn boundaries_maps() {
        let v = run("maps", &["2"]);
        assert_eq!(v[6], n(0));
        assert_eq!(v[7], v[8]);
        assert!(v[7] >= n(0));
    }
    #[test]
    fn boundaries_tensor() {
        let v = run("tensor", &["1", "0", "1", "0"]);
        assert_eq!(v[12], v[14]);
        assert_ne!(v[16], v[18]);
    }
    #[test]
    fn boundaries_torsion() {
        let v = run(
            "torsion",
            &["1", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        );
        assert_eq!(v[9], v[10]);
        assert_eq!(v[5..7], v[7..9]);
        assert_eq!(v[11], v[12]);
    }
    #[test]
    fn boundaries_q8_all_group_products() {
        for a in 0..8 {
            for b in 0..8 {
                for c in 0..8 {
                    assert_eq!(
                        qm(qm(quat(a), quat(b)), quat(c)),
                        qm(quat(a), qm(quat(b), quat(c)))
                    );
                }
            }
            assert_eq!(qm(quat(a), qi(quat(a))), quat(0));
        }
    }
    #[test]
    fn boundaries_parity_all_subsets() {
        for m in 0_usize..64 {
            assert_eq!(
                solutions(m).len(),
                if m == 63 {
                    0
                } else {
                    1 << (9 - m.count_ones())
                }
            );
        }
    }
    #[test]
    fn boundaries_proxy_all_rows() {
        for k in 0..5 {
            let v = proxy(k);
            for j in 0..5 {
                assert_eq!(v[31 + j], n((k != j as i64) as i64));
            }
        }
    }
    #[test]
    #[should_panic]
    fn boundaries_refuse_even_repetition() {
        run("syndrome", &["2"]);
    }
}
