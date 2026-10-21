//! Exact finite witnesses, with no continuum or authority status oracle.
use num_bigint::BigInt;
use num_integer::Integer;
use num_rational::BigRational as Q;
use num_traits::{Signed, ToPrimitive, Zero};
type E = (Q, Q);
type M = Vec<Vec<E>>;
fn n(x: i64) -> Q {
    Q::from_integer(x.into())
}
fn q(s: &str) -> Q {
    let (a, b) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(a.parse::<BigInt>().unwrap(), b.parse::<BigInt>().unwrap())
}
fn add(a: &E, b: &E) -> E {
    (&a.0 + &b.0, &a.1 + &b.1)
}
fn mul(a: &E, b: &E, d: i64) -> E {
    (&a.0 * &b.0 + n(d) * &a.1 * &b.1, &a.0 * &b.1 + &a.1 * &b.0)
}
fn mm(a: &M, b: &M) -> M {
    (0..a.len())
        .map(|i| {
            (0..b[0].len())
                .map(|j| {
                    (0..b.len()).fold((n(0), n(0)), |s, k| add(&s, &mul(&a[i][k], &b[k][j], -1)))
                })
                .collect()
        })
        .collect()
}
fn adj(a: &M) -> M {
    (0..a[0].len())
        .map(|j| {
            (0..a.len())
                .map(|i| (a[i][j].0.clone(), -&a[i][j].1))
                .collect()
        })
        .collect()
}
fn qm(a: Vec<Vec<Q>>) -> M {
    a.into_iter()
        .map(|r| r.into_iter().map(|x| (x, n(0))).collect())
        .collect()
}
fn eye(s: usize) -> M {
    qm((0..s)
        .map(|i| (0..s).map(|j| n(if i == j { 1 } else { 0 })).collect())
        .collect())
}
fn ma(a: &M, b: &M, sgn: i64) -> M {
    a.iter()
        .zip(b)
        .map(|(r, t)| {
            r.iter()
                .zip(t)
                .map(|(x, y)| add(x, &(&y.0 * n(sgn), &y.1 * n(sgn))))
                .collect()
        })
        .collect()
}
fn rflat(a: &M) -> Vec<Q> {
    a.iter().flatten().map(|z| z.0.clone()).collect()
}
fn flat(a: &M) -> Vec<Q> {
    a.iter()
        .flatten()
        .flat_map(|z| [z.0.clone(), z.1.clone()])
        .collect()
}
fn tr(a: &M) -> E {
    (0..a.len()).fold((n(0), n(0)), |s, i| add(&s, &a[i][i]))
}
fn norm(v: &[E]) -> Q {
    v.iter().map(|z| &z.0 * &z.0 + &z.1 * &z.1).sum()
}
fn power(a: &M, k: usize) -> M {
    let mut r = eye(a.len());
    for _ in 0..k {
        r = mm(&r, a);
    }
    r
}
fn integer(v: &Q, lo: i64, hi: i64) -> i64 {
    assert!(v.is_integer());
    let k = v.to_integer().to_i64().unwrap();
    assert!((lo..=hi).contains(&k));
    k
}
fn cayley(t: &Q) -> M {
    let den = n(1) + t * t;
    let r = (n(1) - t * t) / &den;
    let s = n(2) * t / den;
    qm(vec![vec![r.clone(), s.clone()], vec![-s, r]])
}
fn real2(v: &[Q]) -> M {
    qm(vec![v[..2].to_vec(), v[2..4].to_vec()])
}
fn vec2(v: &[Q]) -> M {
    qm(vec![vec![v[0].clone()], vec![v[1].clone()]])
}
fn path_sum_between(a: &M, k: usize, i: usize, j: usize) -> Q {
    if k == 0 {
        return if i == j { q("1") } else { q("0") };
    }
    let mut total = Q::zero();
    for mask in 0..(1usize << (k - 1)) {
        let mut prev = j;
        let mut w = q("1");
        for at in 0..k {
            let next = if at + 1 == k { i } else { (mask >> at) & 1 };
            w *= &a[next][prev].0;
            prev = next;
        }
        total += w;
    }
    total
}

fn eval_path(x: &[Q]) -> Vec<Q> {
    let a = real2(x);
    let m = integer(&x[4], 0, 3) as usize;
    let n = integer(&x[5], 0, 3) as usize;
    let k = m + n;
    let mut paths = vec![];
    for i in 0..2 {
        for j in 0..2 {
            paths.push(path_sum_between(&a, k, i, j));
        }
    }
    let mut o = rflat(&power(&a, k));
    o.extend(paths);
    o.extend(rflat(&mm(&power(&a, m), &power(&a, n))));
    o
}

fn eval_transfer(x: &[Q]) -> Vec<Q> {
    let a = real2(x);
    let b = real2(&x[4..]);
    let v = vec2(&x[8..]);
    let f = qm(vec![x[10..12].to_vec()]);
    [
        mm(&a, &b),
        mm(&mm(&a, &b), &v),
        mm(&a, &mm(&b, &v)),
        mm(&f, &a),
        mm(&f, &mm(&a, &v)),
        mm(&mm(&f, &a), &v),
    ]
    .iter()
    .flat_map(rflat)
    .collect()
}

fn eval_overcount(x: &[Q]) -> Vec<Q> {
    let (a, b, d) = (&x[0], &x[1], &x[2]);
    let t = qm(vec![
        vec![n(0), n(0), n(0)],
        vec![a.clone(), n(0), n(0)],
        vec![d.clone(), b.clone(), n(0)],
    ]);
    let z = ma(&ma(&eye(3), &t, 1), &mm(&t, &t), 1);
    let zz = mm(&z, &z);
    let mut o = rflat(&z);
    o.extend(rflat(&zz));
    o.extend([a * b, d.clone(), z[2][0].0.clone(), zz[2][0].0.clone()]);
    o
}

fn eval_refinement(x: &[Q]) -> Vec<Q> {
    let (n, m, k, u) = (&x[0], &x[1], &x[2], &x[3]);
    vec![
        u + m - k + n - m,
        u + n - k,
        k + n - k,
        k - n,
        (k - n).abs(),
    ]
}

fn eval_histories(x: &[Q]) -> Vec<Q> {
    let p = &x[0] * &x[2];
    let q = &x[1] * &x[3];
    vec![
        p.clone(),
        q.clone(),
        &p + &q,
        (&p + &q).pow(2),
        p.pow(2) + q.pow(2),
        n(2) * p * q,
    ]
}

fn eval_held(x: &[Q]) -> Vec<Q> {
    let (a, b) = (&x[0], &x[1]);
    vec![
        a * a,
        b * b,
        a * a,
        b * b,
        (a + b).pow(2),
        (a - b).pow(2),
        n(4) * a * b,
    ]
}

fn eval_schrodinger(x: &[Q]) -> Vec<Q> {
    let (h0, h1, u, v, a, b, c, d, dt, hbar) = (
        &x[0], &x[1], &x[2], &x[3], &x[4], &x[5], &x[6], &x[7], &x[8], &x[9],
    );
    assert!(hbar > &n(0));
    let h = vec![
        vec![(h0.clone(), n(0)), (u.clone(), v.clone())],
        vec![(u.clone(), -v), (h1.clone(), n(0))],
    ];
    let psi = vec![(a.clone(), b.clone()), (c.clone(), d.clone())];
    let hp: Vec<E> = mm(&h, &psi.iter().map(|z| vec![z.clone()]).collect())
        .into_iter()
        .map(|r| r[0].clone())
        .collect();
    let der: Vec<E> = hp.iter().map(|z| (&z.1 / hbar, -&z.0 / hbar)).collect();
    let rate = n(2)
        * psi
            .iter()
            .zip(&der)
            .map(|(a, b)| &a.0 * &b.0 + &a.1 * &b.1)
            .sum::<Q>();
    let e: Vec<E> = psi
        .iter()
        .zip(&der)
        .map(|(a, b)| add(a, &(&b.0 * dt, &b.1 * dt)))
        .collect();
    let mut o: Vec<Q> = hp
        .iter()
        .chain(&der)
        .flat_map(|z| [z.0.clone(), z.1.clone()])
        .collect();
    o.extend([rate, norm(&psi)]);
    o.extend(e.iter().flat_map(|z| [z.0.clone(), z.1.clone()]));
    o.extend([norm(&e), norm(&e) - norm(&psi), dt * dt * norm(&der)]);
    o
}

fn eval_cayley(x: &[Q]) -> Vec<Q> {
    let t = &x[0];
    let u = cayley(t);
    let e = qm(vec![vec![n(1), t.clone()], vec![-t, n(1)]]);
    let a = qm(vec![vec![n(0), n(1)], vec![n(1), n(0)]]);
    let z = qm(vec![vec![n(1), n(0)], vec![n(0), n(-1)]]);
    let mut o: Vec<Q> = [
        u.clone(),
        mm(&adj(&u), &u),
        e.clone(),
        mm(&adj(&e), &e),
        ma(&mm(&a, &z), &mm(&z, &a), 1),
        mm(&a, &a),
        mm(&z, &z),
    ]
    .iter()
    .flat_map(rflat)
    .collect();
    o.push(n(1) + t * t);
    o
}

fn eval_lambda(x: &[Q]) -> Vec<Q> {
    let r = &x[0];
    let z = (n(0), n(0));
    let one = (r.clone(), n(0));
    let l1 = vec![
        vec![z.clone(), one.clone(), z.clone()],
        vec![one.clone(), z.clone(), z.clone()],
        vec![z.clone(); 3],
    ];
    let l2 = vec![
        vec![z.clone(), (n(0), -r), z.clone()],
        vec![(n(0), r.clone()), z.clone(), z.clone()],
        vec![z.clone(); 3],
    ];
    let l3 = vec![
        vec![one.clone(), z.clone(), z.clone()],
        vec![z.clone(), (-r, n(0)), z.clone()],
        vec![z.clone(); 3],
    ];
    let ls = vec![l1, l2, l3];
    let comms: Vec<M> = (0..3)
        .map(|i| {
            ma(
                &mm(&ls[i], &ls[(i + 1) % 3]),
                &mm(&ls[(i + 1) % 3], &ls[i]),
                -1,
            )
        })
        .collect();
    let rhs: Vec<M> = (0..3)
        .map(|i| {
            ls[(i + 2) % 3]
                .iter()
                .map(|row| row.iter().map(|q| mul(&(n(0), n(2) * r), q, -1)).collect())
                .collect()
        })
        .collect();
    let mut mats = ls.clone();
    mats.extend(comms);
    mats.extend(rhs);
    for k in 0..2 {
        let p = qm((0..3)
            .map(|i| {
                (0..3)
                    .map(|j| n(if i == j && j == k { 1 } else { 0 }))
                    .collect()
            })
            .collect());
        mats.push(mm(&p, &p));
    }
    let mut o: Vec<Q> = mats.iter().flat_map(flat).collect();
    o.extend(ls.iter().flat_map(|a| {
        let t = tr(a);
        [t.0, t.1]
    }));
    o
}

fn eval_heisenberg(x: &[Q]) -> Vec<Q> {
    let u = cayley(&x[0]);
    let a = qm(vec![
        vec![x[1].clone(), x[2].clone()],
        vec![x[2].clone(), x[3].clone()],
    ]);
    let psi = vec2(&x[4..]);
    let ah = mm(&adj(&u), &mm(&a, &u));
    let ps = mm(&u, &psi);
    let f = mm(&adj(&ps), &mm(&a, &ps))[0][0].0.clone();
    let g = mm(&adj(&psi), &mm(&ah, &psi))[0][0].0.clone();
    let mut o: Vec<Q> = [ah, ps, mm(&adj(&u), &u)].iter().flat_map(rflat).collect();
    o.extend([f, g]);
    o
}

fn eval_decoherence(x: &[Q]) -> Vec<Q> {
    let (a, b) = (&x[0], &x[1]);
    vec![
        a * a,
        a * b,
        a * b,
        b * b,
        a * a,
        b * b,
        n(0),
        a * a + b * b,
        (a + b).pow(2),
        a + b,
        a * a + b * b,
    ]
}

fn eval_global(x: &[Q]) -> Vec<Q> {
    let (a, b, c) = (&x[0], &x[1], &x[2]);
    vec![a + c, a + n(2) * b + c, n(2) * b, a - n(2) * b + c]
}

fn eval_ccr(x: &[Q]) -> Vec<Q> {
    let s = integer(&x[0], 1, 3) as usize;
    let a = qm((0..s)
        .map(|i| x[1 + i * s..1 + (i + 1) * s].to_vec())
        .collect());
    let at = 1 + s * s;
    let b = qm((0..s)
        .map(|i| x[at + i * s..at + (i + 1) * s].to_vec())
        .collect());
    let com = ma(&mm(&a, &b), &mm(&b, &a), -1);
    let mut o = rflat(&com);
    o.extend([tr(&com).0, n(s as i64) * x.last().unwrap(), n(s as i64)]);
    o
}

fn eval_dichotomy(x: &[Q]) -> Vec<Q> {
    let k = integer(&x[0], 1, 8);
    let (mut a, mut b) = (BigInt::from(1), BigInt::from(0));
    let mut ip = (n(1), n(0));
    for _ in 0..k {
        (a, b) = (3 * &a - 4 * &b, 4 * &a + 3 * &b);
        ip = mul(&ip, &(n(0), n(1)), -1);
    }
    let den = BigInt::from(5).pow(k as u32);
    vec![
        Q::from_integer(a.clone()),
        Q::from_integer(b.clone()),
        Q::from_integer(den.clone()),
        Q::new(a.clone(), den.clone()),
        Q::new(b.clone(), den.clone()),
        Q::from_integer(a.mod_floor(&5.into())),
        Q::from_integer(b.mod_floor(&5.into())),
        ip.0.clone(),
        ip.1.clone(),
        Q::new(&a * &a + &b * &b, &den * &den),
        n(if ip == (n(1), n(0)) { 1 } else { 0 }),
    ]
}

fn eval_everett(x: &[Q]) -> Vec<Q> {
    assert!(
        !x.is_empty()
            && x.iter().all(|q| q >= &n(0))
            && x.iter().cloned().sum::<Q>() == n(1)
    );
    let mut den = BigInt::from(1);
    for q in x {
        den = den.lcm(q.denom());
    }
    let counts: Vec<Q> = x.iter().map(|q| q * Q::from_integer(den.clone())).collect();
    let wp = (q("1/2"), q("1/10"));
    let wm = (q("1/2"), q("-1/10"));
    let poly = |w: &E| {
        let sq = mul(w, w, 5);
        (n(5) * sq.0 - n(5) * &w.0 + n(1), n(5) * sq.1 - n(5) * &w.1)
    };
    let mut o = vec![Q::from_integer(den)];
    o.extend(counts.clone());
    o.push(counts.into_iter().sum());
    let p = poly(&wp);
    let m = poly(&wm);
    let sum = add(&wp, &wm);
    o.extend([p.0, p.1, m.0, m.1, sum.0, sum.1, wp.0, wp.1]);
    o
}

fn eval_embedding(x: &[Q]) -> Vec<Q> {
    let p = (x[0].clone(), x[1].clone());
    let qv = (x[2].clone(), x[3].clone());
    let conductor = integer(&x[4], 3, 120);
    let gram = vec![mul(&p, &p, 5), mul(&p, &qv, 5), mul(&qv, &qv, 5)];
    let conjugate: Vec<E> = gram.iter().map(|z| (z.0.clone(), -&z.1)).collect();
    let ab = mul(&gram[0], &gram[2], 5);
    let bc = mul(&gram[1], &gram[1], 5);
    let mut pairs = gram;
    pairs.extend(conjugate);
    pairs.extend([
        (ab.0 - bc.0, ab.1 - bc.1),
        (n(-2), n(1)),
        (n(3), n(-1)),
        (n(-2), n(-1)),
        (n(3), n(1)),
    ]);
    let phi = (1..=conductor).filter(|i| i.gcd(&conductor) == 1).count() as i64;
    let mut o: Vec<Q> = pairs.into_iter().flat_map(|z| [z.0, z.1]).collect();
    o.extend([
        n(phi),
        n(phi) / n(2),
        n(2),
        n(3),
        n(4),
        n(5),
        n(9),
        q("9/4").pow(2) - n(5),
    ]);
    o
}

fn eval_stone_gap(x: &[Q]) -> Vec<Q> {
    let t = integer(&x[0], 0, 16);
    let k = integer(&x[1], -16, 16);
    vec![
        n((t * k).rem_euclid(4)),
        n((t * (k + 4)).rem_euclid(4)),
        n((t * k).rem_euclid(8)),
        n((t * (k + 4)).rem_euclid(8)),
        n((4 * t).rem_euclid(4)),
    ]
}

fn eval_cptp(x: &[Q]) -> Vec<Q> {
    let t = &x[0];
    assert!(t >= &n(0));
    let rho: Vec<Vec<Q>> = (0..4)
        .map(|i| {
            (0..4)
                .map(|j| {
                    if (i == 0 || i == 3) && (j == 0 || j == 3) {
                        t / n(2)
                    } else {
                        n(0)
                    }
                })
                .collect()
        })
        .collect();
    let pt: Vec<Vec<Q>> = (0..4)
        .map(|i| {
            (0..4)
                .map(|j| rho[2 * (i / 2) + j % 2][2 * (j / 2) + i % 2].clone())
                .collect()
        })
        .collect();
    let v = [0, 1, -1, 0];
    let quad: Q = (0..4)
        .flat_map(|i| {
            (0..4).map({
                let pt = &pt;
                move |j| n(v[i]) * &pt[i][j] * n(v[j])
            })
        })
        .sum();
    let mut o: Vec<Q> = rho.iter().chain(&pt).flatten().cloned().collect();
    o.extend([
        quad,
        n(2),
        (0..4).map(|i| rho[i][i].clone()).sum(),
        (0..4).map(|i| pt[i][i].clone()).sum(),
        n(1),
        n(0),
        n(0),
        n(1),
    ]);
    o
}

fn eval_condition(x: &[Q]) -> Vec<Q> {
    let s = integer(&x[0], 1, 4) as usize;
    assert!(x.len() == 1 + 2 * s);
    let w = &x[1..1 + s];
    let mask = &x[1 + s..];
    assert!(w.iter().all(|q| q >= &n(0)) && mask.iter().all(|q| q == &n(0) || q == &n(1)));
    let mass: Q = w.iter().zip(mask).map(|(q, s)| q * s).sum();
    assert!(mass > n(0));
    let p: Vec<Q> = w.iter().zip(mask).map(|(q, s)| q * s / &mass).collect();
    let mass2: Q = p.iter().zip(mask).map(|(q, s)| q * s).sum();
    let again: Vec<Q> = p.iter().zip(mask).map(|(q, s)| q * s / &mass2).collect();
    let mut o = vec![mass];
    o.extend(p.clone());
    o.extend(again);
    o.push(p.into_iter().sum());
    o
}

fn eval_trajectories(kind: &str, x: &[Q]) -> Option<Vec<Q>> {
    match kind {
        "path" => Some(eval_path(x)),
        "transfer" => Some(eval_transfer(x)),
        "overcount" => Some(eval_overcount(x)),
        "refinement" => Some(eval_refinement(x)),
        "histories" => Some(eval_histories(x)),
        "held" => Some(eval_held(x)),
        "schrodinger" => Some(eval_schrodinger(x)),
        _ => None,
    }
}

fn eval_algebraic_dynamics(kind: &str, x: &[Q]) -> Option<Vec<Q>> {
    match kind {
        "cayley" => Some(eval_cayley(x)),
        "lambda" => Some(eval_lambda(x)),
        "heisenberg" => Some(eval_heisenberg(x)),
        "decoherence" => Some(eval_decoherence(x)),
        "global" => Some(eval_global(x)),
        "ccr" => Some(eval_ccr(x)),
        "dichotomy" => Some(eval_dichotomy(x)),
        _ => None,
    }
}

fn eval_open_dynamics(kind: &str, x: &[Q]) -> Option<Vec<Q>> {
    match kind {
        "everett" => Some(eval_everett(x)),
        "embedding" => Some(eval_embedding(x)),
        "stone_gap" => Some(eval_stone_gap(x)),
        "cptp" => Some(eval_cptp(x)),
        "condition" => Some(eval_condition(x)),
        _ => None,
    }
}

pub fn evaluate(kind: &str, vs: &[String]) -> Vec<String> {
    if kind == "stone" {
        return crate::structure_exact::evaluate("time", vs);
    }
    let x: Vec<Q> = vs.iter().map(|s| q(s)).collect();
    let out: Vec<Q> = eval_trajectories(kind, &x)
        .or_else(|| eval_algebraic_dynamics(kind, &x))
        .or_else(|| eval_open_dynamics(kind, &x))
        .unwrap_or_else(|| panic!("unknown scoped operation"));
    out.iter().map(ToString::to_string).collect()
}
#[cfg(test)]
mod tests {
    use super::*;
    fn run(k: &str, v: &[&str]) -> Vec<String> {
        evaluate(k, &v.iter().map(|s| s.to_string()).collect::<Vec<_>>())
    }
    #[test]
    fn dynamics_path() {
        let o = run("path", &["1", "1", "1", "0", "1", "2"]);
        assert_eq!(&o[..4], &o[4..8]);
        assert_eq!(&o[..4], &o[8..12]);
    }
    #[test]
    fn dynamics_transfer() {
        let o = run(
            "transfer",
            &["1", "2", "3", "4", "0", "1", "1", "0", "2", "3", "1", "-1"],
        );
        assert_eq!(&o[4..6], &o[6..8]);
        assert_eq!(o[10], o[11]);
    }
    #[test]
    fn dynamics_overcount() {
        let o = run("overcount", &["1", "1", "0"]);
        assert_eq!(&o[20..], ["1", "3"]);
    }
    #[test]
    fn dynamics_refinement() {
        let o = run("refinement", &["1", "2", "4", "7"]);
        assert_eq!(o[0], o[1]);
        assert_eq!(o[2], "1");
    }
    #[test]
    fn dynamics_histories() {
        assert_eq!(
            &run("histories", &["1", "1", "1", "-1"])[2..],
            ["0", "0", "2", "-2"]
        );
    }
    #[test]
    fn dynamics_held() {
        assert_eq!(&run("held", &["1", "1"])[4..6], ["4", "0"]);
    }
    #[test]
    fn dynamics_schrodinger() {
        let o = run(
            "schrodinger",
            &["1", "2", "3", "4", "1", "0", "0", "1", "1/10", "1"],
        );
        assert_eq!(o[8], "0");
        assert_eq!(o[15], o[16]);
    }
    #[test]
    fn dynamics_cayley() {
        assert_eq!(&run("cayley", &["1/2"])[4..8], ["1", "0", "0", "1"]);
    }
    #[test]
    fn dynamics_lambda() {
        let o = run("lambda", &["1"]);
        assert_eq!(&o[54..108], &o[108..162]);
        assert!(o[198..].iter().all(|q| q == "0"));
    }
    #[test]
    fn dynamics_heisenberg() {
        let o = run("heisenberg", &["1/2", "1", "2", "3", "1", "2"]);
        assert_eq!(o[10], o[11]);
    }
    #[test]
    fn dynamics_decoherence() {
        let o = run("decoherence", &["1/2", "1/2"]);
        assert_eq!(o[7], "1/2");
        assert_eq!(o[8], "1");
    }
    #[test]
    fn dynamics_global() {
        assert_eq!(run("global", &["1", "1", "1"]), ["2", "4", "2", "0"]);
    }
    #[test]
    fn dynamics_ccr() {
        let o = run("ccr", &["2", "1", "2", "3", "4", "0", "1", "1", "0", "1"]);
        assert_eq!(&o[4..], ["0", "2", "2"]);
    }
    #[test]
    fn dynamics_dichotomy() {
        let o = run("dichotomy", &["4"]);
        assert_eq!(&o[5..7], ["3", "4"]);
        assert_eq!(o[10], "1");
    }
    #[test]
    fn dynamics_stone() {
        let o = run("stone", &["0", "1"]);
        assert_eq!(&o[6..14], &o[14..22]);
    }
    #[test]
    fn dynamics_everett() {
        let o = run("everett", &["1/2", "1/3", "1/6"]);
        assert_eq!(&o[..5], ["6", "3", "2", "1", "6"]);
    }
    #[test]
    fn dynamics_embedding() {
        let o = run("embedding", &["1", "1", "2", "0", "120"]);
        assert_eq!(&o[22..24], ["32", "16"]);
        assert_eq!(o[29], "1/16");
    }
    #[test]
    fn dynamics_stone_gap() {
        assert_eq!(run("stone_gap", &["1", "1"]), ["1", "1", "1", "5", "0"]);
    }
    #[test]
    fn dynamics_cptp() {
        let o = run("cptp", &["1"]);
        assert_eq!(o[32], "-1");
    }
    #[test]
    fn dynamics_condition() {
        let o = run("condition", &["3", "2", "3", "5", "1", "0", "1"]);
        assert_eq!(&o[1..4], &o[4..7]);
    }
}
