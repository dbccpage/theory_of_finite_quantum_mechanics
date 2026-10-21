//! Exact bounded replay. No continuum structure or general observer classification is admitted.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::{Signed, ToPrimitive, Zero};
fn n(v: i64) -> Q {
    Q::from_integer(v.into())
}
fn parse(s: &str) -> Q {
    let (a, b) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(a.parse::<BigInt>().unwrap(), b.parse::<BigInt>().unwrap())
}
fn perm(v: &mut [i64], i: usize, out: &mut Vec<Vec<i64>>) {
    if i == v.len() {
        out.push(v.to_vec());
        return;
    }
    for j in i..v.len() {
        v.swap(i, j);
        perm(v, i + 1, out);
        v.swap(i, j)
    }
}
type G = (Q, Q);
fn mm(a: &[G], b: &[G]) -> Vec<G> {
    (0..2)
        .flat_map(|i| {
            (0..2).map(move |j| {
                let mut z = (n(0), n(0));
                for k in 0..2 {
                    let u = &a[2 * i + k];
                    let v = &b[2 * k + j];
                    z.0 += &u.0 * &v.0 - &u.1 * &v.1;
                    z.1 += &u.0 * &v.1 + &u.1 * &v.0
                }
                z
            })
        })
        .collect()
}

fn eval_chain(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let (a, b, c, f) = (&x[0], &x[1], &x[2], &x[3]);
            let d = vec![b - a, c - b, a - c];
            e!(f.clone(), n(0), -f);
            o.extend(d.clone());
            e!(d.iter().cloned().sum::<Q>() + f * &d[2], bit(f.is_zero()));
    None
}

fn eval_kkt(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let (v, w, h, z) = (&x[..3], &x[3..6], &x[6..9], &x[9..12]);
            let d = vec![&h[1] - &h[0], &h[2] - &h[1], &h[0] - &h[2]];
            let r = (0..3).map(|i| &v[i] - &d[i]).collect::<Vec<_>>();
            let div = vec![&z[2] - &z[0], &z[0] - &z[1], &z[1] - &z[2]];
            let cap = (0..3).map(|i| &w[i] - z[i].abs()).collect::<Vec<_>>();
            let slack = (0..3)
                .map(|i| &w[i] * r[i].abs() - &z[i] * &r[i])
                .collect::<Vec<_>>();
            let cost = (0..3).map(|i| &w[i] * r[i].abs()).sum::<Q>();
            let dual = (0..3).map(|i| &z[i] * &v[i]).sum::<Q>();
            let ok = w.iter().all(|v| v > &n(0))
                && cap.iter().all(|v| v >= &n(0))
                && div.iter().all(|v| v.is_zero())
                && cost == dual;
            o.extend(r);
            o.extend(div);
            o.extend(cap);
            o.extend(slack);
            e!(cost.clone(), dual.clone(), cost - dual, bit(ok));
    None
}

fn eval_edge_gauge_observer(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let (a, b, p, q) = (&x[0], &x[1], &x[2], &x[3]);
            assert!(*p >= n(0) && *q >= n(0));
            let norm = p * a.abs() + q * b.abs();
            let sw = p * b.abs() + q * a.abs();
            if kind == "edge" {
                e!(
                    p * a.abs(),
                    q * b.abs(),
                    norm.clone(),
                    sw.clone(),
                    sw - &norm,
                    a.abs() + b.abs(),
                    a.abs().max(b.abs()),
                    a.abs() + b.abs() - a.abs().max(b.abs())
                );
            } else if kind == "gauge" {
                for swap in 0..2 {
                    let val = if swap == 0 { &norm } else { &sw };
                    for _ in 0..4 {
                        o.push(val.clone());
                    }
                }
                e!(
                    a * a + b * b,
                    b * b + a * a,
                    n(3) * p + n(4) * q,
                    n(5) * p,
                    n(3) * p + n(4) * q - n(5) * p
                );
            } else {
                e!(
                    norm.clone(),
                    norm.clone(),
                    a.abs() + b.abs() - a.abs().max(b.abs()),
                    n(2) * (a * a + b * b),
                    sw - norm,
                    q * b.abs(),
                    p * a.abs()
                );
            }
    None
}

fn eval_quotient_window(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let v = &x[..3];
            let w = &x[3..6];
            assert!(w.iter().all(|v| v > &n(0)));
            if kind == "window" && !x[9].is_zero() {
                return Some(vec!["0".into()]);
            };
            let total = v.iter().cloned().sum::<Q>();
            let min = w.iter().min().unwrap();
            let k = w.iter().position(|v| v == min).unwrap();
            let r = (0..3)
                .map(|i| if i == k { total.clone() } else { n(0) })
                .collect::<Vec<_>>();
            let h = vec![n(0), &v[0] - &r[0], &v[0] + &v[1] - &r[0] - &r[1]];
            let shift = vec![
                &v[0] + &x[7] - &x[6],
                &v[1] + &x[8] - &x[7],
                &v[2] + &x[6] - &x[8],
            ];
            let cost = (0..3).map(|i| &w[i] * r[i].abs()).sum::<Q>();
            e!(n(1), n(k as i64));
            o.extend(r.clone());
            o.extend(h);
            o.push(cost.clone());
            o.extend(shift.clone());
            o.push(min * shift.iter().cloned().sum::<Q>().abs());
            if kind == "window" {
                let gamma = r.iter().cloned().sum::<Q>().abs();
                e!(
                    gamma.clone(),
                    bit(!cost.is_zero()),
                    if cost.is_zero() { n(0) } else { gamma / cost }
                );
            }
    None
}

fn eval_replica(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let (a, b, k) = (&x[0], &x[1], &x[2]);
            let count = k.to_integer().to_i64().unwrap();
            assert!(k.is_integer() && (0..=8).contains(&count));
            let l = a.abs() + b.abs();
            let s = a * a + b * b;
            e!(k * &l, k * &s, k * l, k * &s, k * k * &s, k * k * s);
    None
}

fn eval_mass(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    if x.iter().any(|v| v < &n(0)) {
                return Some(vec!["-1".into()]);
            }
            let m = x.iter().cloned().sum::<Q>();
            if m.is_zero() {
                return Some(vec!["0".into()]);
            };
            e!(n(1), m.clone());
            o.extend(x.iter().map(|v| v / &m));
            e!((&x[0] + &x[1]) / &m, (&x[2] + &x[3]) / &m, n(1));
    None
}

fn eval_circle(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let k = x[0].to_integer().to_i64().unwrap();
            assert!(x[0].is_integer() && [2, 3, 4].contains(&k));
            for i in 0..k {
                o.push(bit(2 * i % k == 0));
            }
            for i in 0..k {
                for j in 0..k {
                    o.push(n((i + j) % k));
                }
            }
            e!(bit((0..k).all(|i| 2 * i % k == 0)), n(4), n(0));
    None
}

fn eval_gauss_complex(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let (a, b) = (&x[0], &x[1]);
            let z = a * a + b * b;
            if kind == "gauss" {
                assert!(a.is_integer() && b.is_integer());
                e!(
                    z.clone(),
                    bit(z == n(1)),
                    bit(!z.is_zero()),
                    if z.is_zero() { n(0) } else { a / &z },
                    if z.is_zero() { n(0) } else { -b / &z }
                );
                for k in -3..=3 {
                    o.push(n(k * k - 2));
                }
            } else {
                let (c, d) = (&x[2], &x[3]);
                let t = c * c + d * d;
                let u = a * c - b * d;
                let v = a * d + b * c;
                e!(
                    z.clone(),
                    t.clone(),
                    u.clone(),
                    v.clone(),
                    &u * &u + &v * &v,
                    &z * t,
                    bit(!z.is_zero()),
                    if z.is_zero() { n(0) } else { a / &z },
                    if z.is_zero() { n(0) } else { -b / &z }
                );
            }
    None
}

fn eval_time(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let s = &x[0];
            assert!(*s == n(-1) || *s == n(1));
            let maps = [[0, 0], [0, 1], [1, 0], [1, 1]];
            let mut count = 0;
            for f in maps {
                let t = [f[f[0]], f[f[1]]];
                e!(n(t[0] as i64), n(t[1] as i64));
                if t == [1, 0] {
                    count += 1;
                }
            }
            o.push(n(count));
            let h = Q::new(1.into(), 2.into());
            let u = vec![
                (h.clone(), s * &h),
                (h.clone(), -s * &h),
                (h.clone(), -s * &h),
                (h.clone(), s * &h),
            ];
            let adj = (0..2)
                .flat_map(|i| {
                    (0..2).map({
                        let u = &u;
                        move |j| (u[2 * j + i].0.clone(), -u[2 * j + i].1.clone())
                    })
                })
                .collect::<Vec<_>>();
            let square = mm(&u, &u);
            let unit = mm(&adj, &u);
            for z in u.into_iter().chain(square).chain(unit) {
                e!(z.0, z.1);
            }
    None
}

fn eval_hilbert(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let k = x[0].to_integer().to_u32().unwrap();
            assert!(x[0].is_integer() && k <= 8);
            let u = (1..=k)
                .map(|i| Q::new(1.into(), BigInt::from(2).pow(i)))
                .collect::<Vec<_>>();
            o.extend(u.clone());
            e!(
                u.iter().map(|v| v * v).sum::<Q>(),
                Q::new(1.into(), BigInt::from(3) * BigInt::from(4).pow(k)),
                Q::new(1.into(), BigInt::from(4).pow(k + 1)),
                Q::new(1.into(), 3.into()),
                n(1)
            );
    None
}

fn eval_dilation(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let (a, b, d) = (&x[0], &x[1], &x[2]);
            assert!(a + d == n(1) && *a >= n(0) && *d >= n(0) && a * d >= b * b);
            let mut ps = vec![];
            perm(&mut [0, 1, 2, 3], 0, &mut ps);
            ps.sort();
            ps.retain(|p| p[0] / 2 == 0 && p[2] / 2 == 0);
            o.push(n(ps.len() as i64));
            for p in ps {
                for v in &p {
                    o.push(n(*v));
                }
                for i in 0..4 {
                    o.push(n(p.iter().position(|v| *v == i).unwrap() as i64));
                }
            }
            for i in 0..4 {
                for j in 0..4 {
                    o.push(bit(i == j && (i == 0 || i == 2)));
                }
            }
            e!(n(1), n(0), n(0), n(1), a + d, n(0), n(0), n(0));
    None
}

fn eval_gleason(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let (a, b) = (&x[0], &x[1]);
            let u = (a + b) * (a + b);
            let v = (a - b) * (a - b);
            let z = a * a + b * b;
            e!(
                a * a,
                b * b,
                z.clone(),
                z.clone(),
                u.clone(),
                v.clone(),
                z.clone(),
                z.clone(),
                &u + &v,
                n(2) * &z,
                &u * &u + &v * &v,
                n(2) * &z * &z,
                n(8) * a * a * b * b
            );
    None
}

fn eval_tensor(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let (a, b, c, d) = (&x[0], &x[1], &x[2], &x[3]);
            let t = vec![a * c, a * d, b * c, b * d];
            let v = vec![a * (c + d), n(0), b * (c + d), n(0)];
            o.extend(t.clone());
            o.extend(v.clone());
            o.extend(t.iter().zip(v.iter()).map(|(u, w)| u - w));
            e!(
                (a * a + b * b) * (c * c + d * d),
                t.iter().map(|v| v * v).sum::<Q>()
            );
    None
}

fn eval_lift(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let (a, b, c, d) = (&x[0], &x[1], &x[2], &x[3]);
            let aa = a * a + b * b;
            let bb = c * c + d * d;
            if aa.is_zero() || bb.is_zero() {
                return Some(vec!["0".into()]);
            };
            let rho = vec![a * a / &aa, a * b / &aa, a * b / &aa, b * b / &aa];
            let sig = vec![c * c / &bb, c * d / &bb, c * d / &bb, d * d / &bb];
            let dot = a * c + b * d;
            let ov = &dot * &dot / (&aa * &bb);
            let r = vec![a * a.abs(), b * b.abs()];
            let z = vec![c * c.abs(), d * d.abs()];
            let sat = (0..2).map(|i| &r[i] * &z[i]).sum::<Q>()
                == (0..2).map(|i| r[i].abs() * z[i].abs()).sum::<Q>();
            let faith = (0..2).all(|i| r[i].is_zero() || !z[i].is_zero());
            e!(n(1), aa, bb);
            o.extend(rho);
            o.extend(sig);
            e!(ov.clone(), n(1) - &ov, bit(sat), bit(faith), bit(ov > n(0)));
    None
}

fn eval_average(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let (a, b) = (&x[0], &x[1]);
            let ph = [(1, 0), (0, 1), (-1, 0), (0, -1)];
            let mut vals = vec![];
            let mut cor = vec![];
            for (u, s) in ph {
                for (v, t) in ph {
                    let re = a * n(u) + b * n(v);
                    let im = a * n(s) + b * n(t);
                    vals.push(&re * &re + &im * &im);
                }
                let re = (a + b) * n(u);
                let im = (a + b) * n(s);
                cor.push(&re * &re + &im * &im);
            }
            o.extend(vals.clone());
            o.extend(cor.clone());
            e!(
                vals.iter().cloned().sum::<Q>() / n(16),
                cor.iter().cloned().sum::<Q>() / n(4),
                a * a + b * b,
                n(2) * a * b
            );
    None
}

fn eval_gram(kind: &str, x: &[Q], o: &mut Vec<Q>) -> Option<Vec<String>> {
    let bit = |v: bool| n(v as i64);
    macro_rules! e { ($($v:expr),* $(,)?) => { $(o.push($v);)* }; }
    let (a, b, c, d) = (&x[0], &x[1], &x[2], &x[3]);
            e!(
                a * c + b * d,
                a * c + n(2) * b * d,
                n(2) * a * c + n(3) * b * d,
                a * a + b * b,
                a * a + n(2) * b * b,
                n(2) * a * a + n(3) * b * b,
                b * d,
                b * b
            );
    None
}

type EvalFn = fn(&str, &[Q], &mut Vec<Q>) -> Option<Vec<String>>;

const HANDLERS: &[(&str, EvalFn)] = &[
    ("chain", eval_chain),
    ("kkt", eval_kkt),
    ("edge", eval_edge_gauge_observer),
    ("gauge", eval_edge_gauge_observer),
    ("observer", eval_edge_gauge_observer),
    ("quotient", eval_quotient_window),
    ("window", eval_quotient_window),
    ("replica", eval_replica),
    ("mass", eval_mass),
    ("circle", eval_circle),
    ("gauss", eval_gauss_complex),
    ("complex", eval_gauss_complex),
    ("time", eval_time),
    ("hilbert", eval_hilbert),
    ("dilation", eval_dilation),
    ("gleason", eval_gleason),
    ("tensor", eval_tensor),
    ("lift", eval_lift),
    ("average", eval_average),
    ("gram", eval_gram)
];

pub fn evaluate(kind: &str, values: &[String]) -> Vec<String> {
    let x = values.iter().map(|v| parse(v)).collect::<Vec<_>>();
    let mut o: Vec<Q> = vec![];
    for &(k, handler) in HANDLERS {
        if k == kind {
            if let Some(early) = handler(kind, &x, &mut o) {
                return early;
            }
            return o.iter().map(ToString::to_string).collect();
        }
    }
    o.iter().map(ToString::to_string).collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn l1_import_chain() {
        let input = vec![
            "2".to_string(),
            "-3".to_string(),
            "5".to_string(),
            "1".to_string(),
        ];
        let y = evaluate("chain", &input);
        assert_eq!(&y[0..8], &["1", "0", "-1", "-5", "8", "-3", "-3", "0"]);
    }
    #[test]
    fn l1_import_kkt() {
        let input = vec![
            "2".to_string(),
            "0".to_string(),
            "0".to_string(),
            "1".to_string(),
            "2".to_string(),
            "3".to_string(),
            "0".to_string(),
            "0".to_string(),
            "0".to_string(),
            "1".to_string(),
            "1".to_string(),
            "1".to_string(),
        ];
        let y = evaluate("kkt", &input);
        assert_eq!(&y[12..16], &["2", "2", "0", "1"]);
    }
    #[test]
    fn l1_import_edge() {
        let input = vec![
            "1".to_string(),
            "2".to_string(),
            "1".to_string(),
            "3".to_string(),
        ];
        let y = evaluate("edge", &input);
        assert_eq!(&y[2..8], &["7", "5", "-2", "3", "2", "1"]);
    }
    #[test]
    fn l1_import_gauge() {
        let input = vec![
            "3".to_string(),
            "4".to_string(),
            "1".to_string(),
            "1".to_string(),
        ];
        let y = evaluate("gauge", &input);
        assert_eq!(&y[8..13], &["25", "25", "7", "5", "2"]);
    }
    #[test]
    fn l1_import_observer() {
        let input = vec![
            "1".to_string(),
            "1".to_string(),
            "1".to_string(),
            "1".to_string(),
        ];
        let y = evaluate("observer", &input);
        assert_eq!(&y[2..7], &["1", "4", "0", "1", "1"]);
    }
    #[test]
    fn l1_import_quotient() {
        let input = vec![
            "3".to_string(),
            "-1".to_string(),
            "2".to_string(),
            "2".to_string(),
            "1".to_string(),
            "3".to_string(),
            "2".to_string(),
            "-3".to_string(),
            "1".to_string(),
        ];
        let y = evaluate("quotient", &input);
        assert_eq!(&y[0..9], &["1", "1", "0", "4", "0", "0", "3", "-2", "4"]);
    }
    #[test]
    fn l1_import_replica() {
        let input = vec!["3".to_string(), "4".to_string(), "2".to_string()];
        let y = evaluate("replica", &input);
        assert_eq!(&y[0..6], &["14", "50", "14", "50", "100", "100"]);
    }
    #[test]
    fn l1_import_window() {
        let input = vec![
            "0".to_string(),
            "0".to_string(),
            "0".to_string(),
            "1".to_string(),
            "1".to_string(),
            "1".to_string(),
            "0".to_string(),
            "0".to_string(),
            "0".to_string(),
            "0".to_string(),
        ];
        let y = evaluate("window", &input);
        assert_eq!(&y[13..16], &["0", "0", "0"]);
    }
    #[test]
    fn l1_import_mass() {
        let input = vec![
            "1".to_string(),
            "2".to_string(),
            "3".to_string(),
            "4".to_string(),
        ];
        let y = evaluate("mass", &input);
        assert_eq!(
            &y[2..9],
            &["1/10", "1/5", "3/10", "2/5", "3/10", "7/10", "1"]
        );
    }
    #[test]
    fn l1_import_circle() {
        let input = vec!["3".to_string()];
        let y = evaluate("circle", &input);
        assert_eq!(
            &y[0..15],
            &["1", "0", "0", "0", "1", "2", "1", "2", "0", "2", "0", "1", "0", "4", "0"]
        );
    }
    #[test]
    fn l1_import_gauss() {
        let input = vec!["1".to_string(), "1".to_string()];
        let y = evaluate("gauss", &input);
        assert_eq!(
            &y[0..12],
            &["2", "0", "1", "1/2", "-1/2", "7", "2", "-1", "-2", "-1", "2", "7"]
        );
    }
    #[test]
    fn l1_import_time() {
        let input = vec!["1".to_string()];
        let y = evaluate("time", &input);
        assert_eq!(
            &y[17..33],
            &["0", "0", "1", "0", "1", "0", "0", "0", "1", "0", "0", "0", "0", "0", "1", "0"]
        );
    }
    #[test]
    fn l1_import_hilbert() {
        let input = vec!["1".to_string()];
        let y = evaluate("hilbert", &input);
        assert_eq!(&y[1..6], &["1/4", "1/12", "1/16", "1/3", "1"]);
    }
    #[test]
    fn l1_import_dilation() {
        let input = vec!["1/2".to_string(), "0".to_string(), "1/2".to_string()];
        let y = evaluate("dilation", &input);
        assert_eq!(&y[49..57], &["1", "0", "0", "1", "1", "0", "0", "0"]);
    }
    #[test]
    fn l1_import_gleason() {
        let input = vec!["2".to_string(), "1".to_string()];
        let y = evaluate("gleason", &input);
        assert_eq!(
            &y[0..13],
            &["4", "1", "5", "5", "9", "1", "5", "5", "10", "10", "82", "50", "32"]
        );
    }
    #[test]
    fn l1_import_tensor() {
        let input = vec![
            "1".to_string(),
            "0".to_string(),
            "0".to_string(),
            "1".to_string(),
        ];
        let y = evaluate("tensor", &input);
        assert_eq!(
            &y[0..14],
            &["0", "1", "0", "0", "1", "0", "0", "0", "-1", "1", "0", "0", "1", "1"]
        );
    }
    #[test]
    fn l1_import_lift() {
        let input = vec![
            "1".to_string(),
            "0".to_string(),
            "0".to_string(),
            "1".to_string(),
        ];
        let y = evaluate("lift", &input);
        assert_eq!(&y[11..16], &["0", "1", "1", "0", "0"]);
    }
    #[test]
    fn l1_import_complex() {
        let input = vec![
            "1".to_string(),
            "1".to_string(),
            "2".to_string(),
            "1".to_string(),
        ];
        let y = evaluate("complex", &input);
        assert_eq!(
            &y[0..9],
            &["2", "5", "1", "3", "10", "10", "1", "1/2", "-1/2"]
        );
    }
    #[test]
    fn l1_import_average() {
        let input = vec!["3".to_string(), "4".to_string()];
        let y = evaluate("average", &input);
        assert_eq!(&y[20..24], &["25", "49", "25", "24"]);
    }
    #[test]
    fn l1_import_gram() {
        let input = vec![
            "0".to_string(),
            "1".to_string(),
            "0".to_string(),
            "1".to_string(),
        ];
        let y = evaluate("gram", &input);
        assert_eq!(&y[0..8], &["1", "2", "3", "1", "2", "3", "1", "1"]);
    }
}
