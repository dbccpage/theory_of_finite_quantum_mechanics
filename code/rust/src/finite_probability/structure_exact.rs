//! Exact finite witnesses. Domains and source-declared labels are inputs.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::{One, Signed, ToPrimitive, Zero};
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
fn mm(a: &M, b: &M, d: i64) -> M {
    (0..a.len())
        .map(|i| {
            (0..b[0].len())
                .map(|j| {
                    (0..b.len()).fold((n(0), n(0)), |s, k| add(&s, &mul(&a[i][k], &b[k][j], d)))
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
fn flat(a: &M) -> Vec<Q> {
    a.iter()
        .flatten()
        .flat_map(|z| [z.0.clone(), z.1.clone()])
        .collect()
}
fn qm(a: Vec<Vec<Q>>) -> M {
    a.into_iter()
        .map(|r| r.into_iter().map(|x| (x, n(0))).collect())
        .collect()
}
fn ma(a: &M, b: &M, s: i64) -> M {
    a.iter()
        .zip(b)
        .map(|(r, t)| {
            r.iter()
                .zip(t)
                .map(|(x, y)| add(x, &(&y.0 * n(s), &y.1 * n(s))))
                .collect()
        })
        .collect()
}
fn scale(a: &M, s: i64) -> M {
    a.iter()
        .map(|r| r.iter().map(|z| (&z.0 * n(s), &z.1 * n(s))).collect())
        .collect()
}
fn kron(a: &[Vec<Q>], b: &[Vec<Q>]) -> Vec<Vec<Q>> {
    (0..a.len() * b.len())
        .map(|i| {
            (0..a[0].len() * b[0].len())
                .map(|j| &a[i / b.len()][j / b[0].len()] * &b[i % b.len()][j % b[0].len()])
                .collect()
        })
        .collect()
}
fn i3<F: Fn(Q) -> Q>(f: F, a: Q, b: Q, c: Q) -> Q {
    f(&a + &b + &c) - f(&a + &b) - f(&a + &c) - f(&b + &c) + f(a) + f(b) + f(c) - f(n(0))
}
fn norm12(c: Vec<Q>) -> (Q, Q) {
    let z = vec![&c[0] + &c[2], c[1].clone(), -&c[2], -&c[1] - &c[3]];
    let mut p = vec![n(0); 7];
    for i in 0..4 {
        for j in 0..4 {
            p[i + j] += &c[i] * &z[j];
        }
    }
    for k in (4..=6).rev() {
        let t = p[k].clone();
        p[k - 2] += &t;
        p[k - 4] -= &t;
    }
    (p[0].clone(), -p[3].clone())
}
fn eval_power(x: &[Q]) -> Vec<Q> {
    assert!(x[0].is_integer());
    let p = x[0].to_integer().to_i32().unwrap();
    assert!((1..=16).contains(&p));
    let norm = n(1) + q("3/5").pow(p) + q("4/5").pow(p);
    vec![
        norm.clone(),
        q("1/2"),
        n(1) / &norm,
        q("1/2") - n(1) / norm,
        i3(|a| a.abs().pow(p), n(1), n(1), n(1)),
        i3(|a| a.abs().pow(p), n(1), n(1), n(-1)),
    ]
}

fn eval_selection(x: &[Q]) -> Vec<Q> {
    let (a, b) = (&x[0], &x[1]);
    let norm = a * a + b * b;
    assert!(!norm.is_zero());
    let quart = a.pow(4) + b.pow(4);
    vec![
        norm.clone(),
        quart.clone(),
        a * a / &norm,
        b * b / &norm,
        a.pow(4) / &quart,
        b.pow(4) / &quart,
        a * a / norm - a.pow(4) / quart,
    ]
}

fn eval_quotient(x: &[Q]) -> Vec<Q> {
    assert!(!x.is_empty() && x.iter().all(Q::is_integer));
    let mut labels = x.to_vec();
    labels.sort();
    labels.dedup();
    let mut out = vec![n(labels.len() as i64)];
    out.extend(
        x.iter()
            .map(|v| n(labels.iter().position(|a| a == v).unwrap() as i64)),
    );
    out.extend(
        x.iter()
            .flat_map(|a| x.iter().map(move |b| n(if a == b { 1 } else { 0 }))),
    );
    out
}

#[allow(non_snake_case)]
fn eval_sorkin(x: &[Q]) -> Vec<Q> {
    let (a, b, c, alpha, beta, A, B) = (&x[0], &x[1], &x[2], &x[3], &x[4], &x[5], &x[6]);
    let np = norm12(vec![n(2), n(2), n(0), n(-1)]);
    let nm = norm12(vec![n(2), n(-2), n(0), n(1)]);
    vec![
        i3(
            |t| alpha * &t * &t + beta * t.pow(4),
            a.clone(),
            b.clone(),
            c.clone(),
        ),
        n(12) * beta * a * b * c * (a + b + c),
        np.0.clone(),
        np.1.clone(),
        nm.0.clone(),
        nm.1.clone(),
        A * np.0 + B * np.1,
        A * nm.0 + B * nm.1,
    ]
}

fn eval_pinching(x: &[Q]) -> Vec<Q> {
    let (a, b, c) = (&x[0], &x[1], &x[2]);
    assert!(c > &n(0));
    let norm = n(4) * (a * a + b * b);
    let pin = n(4) * a * a;
    vec![
        norm.clone(),
        pin.clone(),
        n(4) * b * b,
        c * c * norm,
        c * c * pin,
    ]
}

fn eval_k23(x: &[Q]) -> Vec<Q> {
    let t = &x[0];
    assert!(t >= &n(0));
    let d: Vec<Vec<Q>> = (0..3)
        .map(|k| (0..3).map(|j| n(if k == j { 2 } else { -1 })).collect())
        .collect();
    let edges: Vec<(usize, usize)> = (0..2)
        .flat_map(|a| (0..3).map(move |k| (a, 2 + k)))
        .collect();
    let defects: Vec<Vec<Q>> = (0..2)
        .flat_map(|a| {
            (0..3).map({
                let d = &d;
                move |k| {
                    d[k].iter()
                        .map(|v| if a == 0 { v * t } else { n(0) })
                        .collect()
                }
            })
        })
        .collect();
    let ms = |den: i64| -> Vec<Vec<Q>> {
        (0..2)
            .flat_map(|a| {
                (0..3).map({
                    let d = &d;
                    move |k| {
                        d[k].iter()
                            .map(|v| v / n(den) * n(if a == 0 { 1 } else { -1 }))
                            .collect()
                    }
                })
            })
            .collect()
    };
    let mtz = ms(3);
    let mall = ms(4);
    let mut potential = vec![vec![n(0); 3]; 5];
    potential[0] = vec![t.clone(); 3];
    let residual: Vec<Vec<Q>> = defects
        .iter()
        .zip(&edges)
        .map(|(z, (u, v))| {
            (0..3)
                .map(|j| &z[j] - (&potential[*v][j] - &potential[*u][j]))
                .collect()
        })
        .collect();
    let div = |m: &Vec<Vec<Q>>| -> Vec<Vec<Q>> {
        (0..5)
            .map(|vtx| {
                (0..3)
                    .map(|j| {
                        m.iter()
                            .zip(&edges)
                            .map(|(r, (u, v))| {
                                if *u == vtx {
                                    r[j].clone()
                                } else if *v == vtx {
                                    -&r[j]
                                } else {
                                    n(0)
                                }
                            })
                            .sum()
                    })
                    .collect()
            })
            .collect()
    };
    let costs: Vec<Q> = defects
        .iter()
        .map(|r| r.iter().map(Q::abs).sum::<Q>() / n(2))
        .collect();
    let ac: Vec<Q> = residual
        .iter()
        .map(|r| r.iter().map(Q::abs).sum::<Q>() / n(2))
        .collect();
    let obj = |m: &Vec<Vec<Q>>| -> Q {
        m.iter()
            .zip(&defects)
            .map(|(a, b)| a.iter().zip(b).map(|(u, v)| u * v).sum::<Q>())
            .sum()
    };
    let mut out: Vec<Q> = vec![
        defects.clone(),
        mtz.clone(),
        mall.clone(),
        potential,
        residual,
        div(&mtz),
        div(&mall),
    ]
    .into_iter()
    .flatten()
    .flatten()
    .collect();
    out.extend(costs.clone());
    out.extend(ac.clone());
    out.extend([
        costs.into_iter().sum(),
        obj(&mtz),
        ac.into_iter().sum(),
        obj(&mall),
    ]);
    out
}

#[allow(non_snake_case)]
fn eval_tsirelson(x: &[Q]) -> Vec<Q> {
    assert!(x == [n(1)] || x == [n(-1)]);
    let sign = if x[0] == n(1) { 1 } else { -1 };
    let I = vec![vec![n(1), n(0)], vec![n(0), n(1)]];
    let Z = vec![vec![n(1), n(0)], vec![n(0), n(-1)]];
    let X = vec![vec![n(0), n(1)], vec![n(1), n(0)]];
    let P = ma(&qm(kron(&Z, &Z)), &qm(kron(&X, &X)), 1);
    let C: M = P
        .iter()
        .map(|r| r.iter().map(|v| (n(0), v.0.clone())).collect())
        .collect();
    let S: Vec<M> = vec![Z, X]
        .iter()
        .map(|a| ma(&qm(kron(a, &I)), &qm(kron(&I, a)), -sign))
        .collect();
    let ss = ma(&mm(&S[0], &S[0], 2), &mm(&S[1], &S[1], 2), 1);
    let rhs: M = ss
        .iter()
        .map(|r| r.iter().map(|z| (&z.1 / n(2), &z.0 / n(2))).collect())
        .collect();
    let ident: M = (0..4)
        .map(|i| {
            (0..4)
                .map(|j| (n(0), n(if i == j { 2 } else { 0 })))
                .collect()
        })
        .collect();
    let lhs = ma(&ident, &C, -sign);
    let rho = qm((0..4)
        .map(|i| {
            (0..4)
                .map(|j| {
                if (i == 0 || i == 3) && (j == 0 || j == 3) {
                    q("1/2")
                } else {
                    n(0)
                }
            })
            .collect()
        })
        .collect());
    let rc = mm(&rho, &C, 2);
    let exp = (0..4).fold((n(0), n(0)), |s, i| add(&s, &rc[i][i]));
    let mut out = flat(&C);
    for a in [&S[0], &S[1], &lhs, &rhs] {
        out.extend(flat(a));
    }
    out.extend([exp.0, exp.1]);
    out
}

fn eval_census(x: &[Q]) -> Vec<Q> {
    assert!(x.len() == 8 && x.iter().all(|v| v == &n(0) || v == &n(1)));
    let lost = x.iter().filter(|v| *v == &n(1)).count();
    let mut out = vec![n(8), n(lost as i64), n((8 - lost) as i64)];
    for val in [1, 0] {
        out.extend(
            x.iter()
                .enumerate()
                .filter(|(_, v)| *v == &n(val))
                .map(|(i, _)| n(i as i64)),
        );
    }
    out
}

#[allow(non_snake_case)]
fn eval_matrix(x: &[Q]) -> Vec<Q> {
    assert!(x.len() == 24 && x.iter().all(Q::is_integer));
    let p: Vec<E> = x.chunks(2).map(|a| (a[0].clone(), a[1].clone())).collect();
    let A = vec![p[0..2].to_vec(), p[2..4].to_vec()];
    let B = vec![p[4..6].to_vec(), p[6..8].to_vec()];
    let v = vec![vec![p[8].clone()], vec![p[9].clone()]];
    let u = vec![vec![p[10].clone()], vec![p[11].clone()]];
    let ab = mm(&A, &B, -1);
    let av = mm(&A, &v, -1);
    let ah = adj(&A);
    let inner = |a: &M, b: &M| -> E {
        (0..2).fold((n(0), n(0)), |s, i| {
            add(&s, &mul(&(a[i][0].0.clone(), -&a[i][0].1), &b[i][0], -1))
        })
    };
    let left = inner(&av, &u);
    let right = inner(&v, &mm(&ah, &u, -1));
    let mut out = flat(&ab);
    for m in [&av, &mm(&ab, &v, -1), &mm(&A, &mm(&B, &v, -1), -1), &ah] {
        out.extend(flat(m));
    }
    out.extend([left.0, left.1, right.0, right.1]);
    out.extend(flat(&A));
    out
}

#[allow(non_snake_case)]
fn eval_time(x: &[Q]) -> Vec<Q> {
    assert!(x.len() == 2 && x.iter().all(Q::is_integer));
    let M = vec![
        vec![(n(1), n(1)), (n(1), n(-1))],
        vec![(n(1), n(-1)), (n(1), n(1))],
    ];
    let mut out = vec![n(2) * &x[0] + n(1), n(2) * &x[1] + n(1)];
    for a in 0..2 {
        for b in 0..2 {
            let f = [a, b];
            out.push(n(2 * f[f[0] as usize] + f[f[1] as usize]));
        }
    }
    out.extend(flat(&mm(&M, &M, -1)));
    out.extend(flat(&mm(&scale(&M, -1), &scale(&M, -1), -1)));
    out.extend(flat(&mm(&adj(&M), &M, -1)));
    out
}

fn evaluate_algebraic(kind: &str, x: &[Q]) -> Option<Vec<Q>> {
    match kind {
        "power" => Some(eval_power(x)),
        "selection" => Some(eval_selection(x)),
        "quotient" => Some(eval_quotient(x)),
        "sorkin" => Some(eval_sorkin(x)),
        "pinching" => Some(eval_pinching(x)),
        _ => None,
    }
}

fn evaluate_structural(kind: &str, x: &[Q]) -> Option<Vec<Q>> {
    match kind {
        "k23" => Some(eval_k23(x)),
        "tsirelson" => Some(eval_tsirelson(x)),
        "census" => Some(eval_census(x)),
        "matrix" => Some(eval_matrix(x)),
        "time" => Some(eval_time(x)),
        _ => None,
    }
}

pub fn evaluate(kind: &str, vs: &[String]) -> Vec<String> {
    let x: Vec<Q> = vs.iter().map(|s| q(s)).collect();
    let out = evaluate_algebraic(kind, &x)
        .or_else(|| evaluate_structural(kind, &x))
        .unwrap_or_else(|| panic!("unknown domain"));
    out.iter().map(ToString::to_string).collect()
}
#[cfg(test)]
mod tests {
    use super::*;
    fn run(k: &str, a: &[&str]) -> Vec<String> {
        evaluate(k, &a.iter().map(|s| s.to_string()).collect::<Vec<_>>())
    }
    #[test]
    fn structure_power() {
        let a = run("power", &["1"]);
        assert_eq!(a[0], "12/5");
        assert_eq!(a[4], "0");
        assert_eq!(a[5], "2");
        assert_eq!(run("power", &["2"])[3], "0");
    }
    #[test]
    fn structure_selection() {
        let a = run("selection", &["1", "2"]);
        assert_eq!(a[2], "1/5");
        assert_eq!(a[4], "1/17");
    }
    #[test]
    fn structure_quotient() {
        assert_eq!(
            &run("quotient", &["0", "0", "2"])[..4],
            ["2", "0", "0", "1"]
        );
    }
    #[test]
    fn structure_sorkin() {
        assert_eq!(
            &run("sorkin", &["1", "1", "1", "1", "1", "2", "3"])[..2],
            ["36", "36"]
        );
    }
    #[test]
    fn structure_pinching() {
        assert_eq!(&run("pinching", &["3", "4", "2"])[..3], ["100", "36", "64"]);
    }
    #[test]
    fn structure_k23() {
        let a = run("k23", &["1"]);
        assert_eq!(&a[a.len() - 4..], ["6", "6", "9/2", "9/2"]);
    }
    #[test]
    fn structure_tsirelson() {
        let a = run("tsirelson", &["1"]);
        assert_eq!(&a[96..128], &a[128..160]);
        assert_eq!(&a[160..], ["0", "2"]);
    }
    #[test]
    fn structure_census() {
        assert_eq!(
            &run("census", &["1", "1", "0", "0", "0", "0", "1", "0"])[..3],
            ["8", "3", "5"]
        );
    }
    #[test]
    fn structure_matrix() {
        let a = run(
            "matrix",
            &[
                "1", "1", "0", "0", "0", "0", "1", "-1", "1", "0", "0", "0", "0", "0", "1", "0",
                "1", "0", "2", "0", "0", "1", "1", "0",
            ],
        );
        assert_eq!(&a[12..16], &a[16..20]);
        assert_eq!(&a[28..30], &a[30..32]);
    }
    #[test]
    fn structure_time() {
        let a = run("time", &["0", "1"]);
        assert_eq!(&a[2..6], ["0", "1", "1", "3"]);
        assert_eq!(&a[6..14], &a[14..22]);
    }
}
