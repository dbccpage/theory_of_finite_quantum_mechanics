//! Exact witnesses on supplied finite carriers. No physical selection oracle.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::{Signed, ToPrimitive, Zero};
type M = Vec<Vec<Q>>;
fn n(x: i64) -> Q {
    Q::from_integer(x.into())
}
fn q(s: &str) -> Q {
    let (a, b) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(a.parse::<BigInt>().unwrap(), b.parse::<BigInt>().unwrap())
}
fn sq(a: &Q) -> Q {
    a * a
}
fn unit(a: &Q) {
    assert!(a >= &n(0) && a <= &n(1));
}
fn integer(a: &Q, lo: i64, hi: i64) -> i64 {
    assert!(a.is_integer());
    let k = a.to_integer().to_i64().unwrap();
    assert!(lo <= k && k <= hi);
    k
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
fn cm(a: &(Q, Q), b: &(Q, Q)) -> (Q, Q) {
    (&a.0 * &b.0 - &a.1 * &b.1, &a.0 * &b.1 + &a.1 * &b.0)
}
fn norm(a: &(Q, Q)) -> Q {
    sq(&a.0) + sq(&a.1)
}
fn rot(t: &Q) -> (Q, Q) {
    let d = n(1) + sq(t);
    ((n(1) - sq(t)) / &d, n(2) * t / d)
}
fn contexts(t: &Q) -> Vec<Q> {
    unit(t);
    let mut v = vec![];
    for x in 0..2 {
        for y in 0..2 {
            for a in 0..2 {
                for b in 0..2 {
                    v.push((n(1) + t * n(if (a + b + x * y) % 2 == 0 { 1 } else { -1 })) / n(4));
                }
            }
        }
    }
    v
}
fn stats(v: &[Q]) -> Vec<Q> {
    assert_eq!(v.len(), 16);
    assert!(v.iter().all(|z| z >= &n(0)));
    let p = |x: usize, y: usize, a: usize, b: usize| v[8 * x + 4 * y + 2 * a + b].clone();
    let mut norms = vec![];
    let mut am = vec![];
    let mut bm = vec![];
    let mut cor = vec![];
    for x in 0..2 {
        for y in 0..2 {
            let mut total = n(0);
            let mut c = n(0);
            for a in 0..2 {
                am.push(p(x, y, a, 0) + p(x, y, a, 1));
                for b in 0..2 {
                    total += p(x, y, a, b);
                    c += n(if a == b { 1 } else { -1 }) * p(x, y, a, b);
                }
            }
            for b in 0..2 {
                bm.push(p(x, y, 0, b) + p(x, y, 1, b));
            }
            norms.push(total);
            cor.push(c);
        }
    }
    assert_eq!(norms, vec![n(1); 4]);
    let mut dev = vec![];
    for x in 0..2 {
        for a in 0..2 {
            dev.push(&am[4 * x + a] - &am[4 * x + 2 + a]);
        }
    }
    for y in 0..2 {
        for b in 0..2 {
            dev.push(&bm[2 * y + b] - &bm[4 + 2 * y + b]);
        }
    }
    let mut defects = vec![];
    for x in 0..2 {
        for y in 0..2 {
            for a in 0..2 {
                for b in 0..2 {
                    defects.push(p(x, y, a, b) - &am[4 * x + 2 * y + a] * &bm[4 * x + 2 * y + b]);
                }
            }
        }
    }
    let ch = &cor[0] + &cor[1] + &cor[2] - &cor[3];
    [norms, am, bm, dev, cor, vec![ch], defects].concat()
}
pub fn evaluate(kind: &str, values: &[String]) -> Vec<String> {
    let x: Vec<Q> = values.iter().map(|s| q(s)).collect();
    let out: Vec<Q> = match kind {
        "projection" => {
            let [a, b, e, f] = x.as_slice() else {
                panic!("arity")
            };
            assert!(a >= &n(0) && b >= &n(0) && a + b > n(0));
            unit(e);
            unit(f);
            vec![
                e * a,
                f * b,
                e * e * a,
                f * f * b,
                sq(e) - e,
                sq(f) - f,
                a / (a + b),
                sq(a) / (sq(a) + sq(b)),
            ]
        }
        "fiber" | "interference" => {
            let [a, b, c, d] = x.as_slice() else {
                panic!("arity")
            };
            let u = sq(a) + sq(b);
            let v = sq(c) + sq(d);
            let plus = sq(&(a + c)) + sq(&(b + d));
            let minus = sq(&(a - c)) + sq(&(b - d));
            let h = n(2) * (a * c + b * d);
            vec![
                u.clone(),
                v.clone(),
                u.clone(),
                v.clone(),
                plus.clone(),
                minus.clone(),
                plus - &u - &v,
                h.clone(),
                minus - u - v,
                n(2) * h,
            ]
        }
        "buildability" => {
            let [la, mu, eps, floor, reach, adv] = x.as_slice() else {
                panic!("arity")
            };
            assert!(la >= &n(0) && mu >= &n(0) && eps >= &n(0));
            integer(reach, 0, 1);
            integer(adv, 0, 1);
            let gap = la - mu - eps;
            let b = [gap <= n(0), floor > &n(0), reach == &n(1), adv == &n(1)];
            let mut v = vec![gap];
            v.extend(b.map(|z| n(z as i64)));
            v.push(n(b.iter().all(|z| *z) as i64));
            v
        }
        "torsion" => {
            assert_eq!(x.len(), 1);
            let k = integer(&x[0], 0, 32);
            let j = vec![vec![n(0), n(-1)], vec![n(1), n(0)]];
            let mut m = vec![vec![n(1), n(0)], vec![n(0), n(1)]];
            for _ in 0..k {
                m = mm(&m, &j);
            }
            let mut v = flat(&m);
            v.extend([n(k % 4), n((k + 4) % 4), n(k + 4)]);
            v
        }
        "selector" => {
            let [a, b, c, d] = x.as_slice() else {
                panic!("arity")
            };
            let aa = vec![vec![a.clone(), -b], vec![b.clone(), a.clone()]];
            let bb = vec![vec![c.clone(), -d], vec![d.clone(), c.clone()]];
            [
                flat(&mm(&aa, &bb)),
                vec![a * c - b * d, a * d + b * c],
                flat(&mm(&tr(&aa), &aa)),
            ]
            .concat()
        }
        "holonomy" => {
            let [a, b, c, d, t] = x.as_slice() else {
                panic!("arity")
            };
            let g = rot(t);
            let z = (a.clone(), b.clone());
            let w = (c.clone(), d.clone());
            let gz = cm(&g, &z);
            let gw = cm(&g, &w);
            let h = cm(&(a.clone(), -b), &w);
            let hh = cm(&(gz.0.clone(), -&gz.1), &gw);
            vec![
                g.0,
                g.1,
                gz.0.clone(),
                gz.1.clone(),
                gw.0.clone(),
                gw.1.clone(),
                h.0.clone(),
                h.1,
                hh.0,
                hh.1,
                norm(&z),
                norm(&w),
                sq(&(a + c)) + sq(&(b + d)),
                sq(&(gz.0 + gw.0)) + sq(&(gz.1 + gw.1)),
                n(2) * h.0,
            ]
        }
        "annex" => {
            let [a, b, c, f, g, h, p, q, u, v, t] = x.as_slice() else {
                panic!("arity")
            };
            unit(p);
            unit(q);
            let y0 = p * u + q * v;
            let y1 = (n(1) - p) * u + (n(1) - q) * v;
            let mut out = vec![
                g - f,
                h - g,
                f - h,
                (g - f) + (h - g) + (f - h),
                a + b + c,
                (a + g - f) + (b + h - g) + (c + f - h),
                y0.clone(),
                y1.clone(),
                u.abs() + v.abs(),
                y0.abs() + y1.abs(),
            ];
            out.extend(stats(&contexts(t)));
            out
        }
        "product" => {
            assert_eq!(x.len(), 4);
            assert!(x.iter().all(|z| z >= &n(0)));
            let w: Q = x.iter().cloned().sum();
            assert!(w > n(0));
            let r = vec![&x[0] + &x[1], &x[2] + &x[3]];
            let c = vec![&x[0] + &x[2], &x[1] + &x[3]];
            let mut out = vec![w.clone()];
            out.extend(r.clone());
            out.extend(c.clone());
            out.extend(r.iter().map(|z| z / &w));
            out.extend(c.iter().map(|z| z / &w));
            let mut residual = vec![];
            for i in 0..2 {
                for j in 0..2 {
                    out.push(&r[i] * &c[j] / sq(&w));
                    residual.push(&w * &x[2 * i + j] - &r[i] * &c[j]);
                }
            }
            out.extend(x.iter().map(|z| z / &w));
            out.extend(residual.clone());
            out.push(residual.iter().map(sq).sum());
            out.push(&x[0] * &x[3] - &x[1] * &x[2]);
            out
        }
        "witness" => {
            let [a, b, c, d] = x.as_slice() else {
                panic!("arity")
            };
            assert_eq!(sq(a) + sq(b), n(1));
            assert_eq!(sq(c) + sq(d), n(1));
            let v = vec![a * c, a * d, b * c, b * d];
            let rho: M = v
                .iter()
                .map(|u| v.iter().map(|w| u * w).collect())
                .collect();
            let f = (&rho[0][0] + &rho[0][3] + &rho[3][0] + &rho[3][3]) / n(2);
            [
                v.clone(),
                flat(&rho),
                vec![
                    v.iter().map(sq).sum(),
                    f.clone(),
                    n(1) / n(2) - f,
                    sq(&(a * d - b * c)) / n(2),
                    n(1),
                    n(1) / n(2),
                ],
            ]
            .concat()
        }
        "qubit" => {
            let [a, b] = x.as_slice() else {
                panic!("arity")
            };
            let nn = sq(a) + sq(b);
            assert!(nn > n(0));
            let p = sq(a) / &nn;
            let c = a * b / nn;
            vec![
                p.clone(),
                c.clone(),
                c.clone(),
                n(1) - &p,
                p.clone(),
                -&c,
                -&c,
                n(1) - &p,
                p.clone(),
                n(0),
                n(0),
                n(1) - &p,
                p.clone(),
                n(1) - &p,
                n(1) / n(2) + &c,
                n(1) / n(2) - &c,
                sq(&p) + sq(&(n(1) - &p)) + n(2) * sq(&c),
                sq(&p) + sq(&(n(1) - p)),
            ]
        }
        "bell_import" => {
            assert_eq!(x.len(), 1);
            let mut v = contexts(&x[0]);
            v.extend(stats(&v.clone()));
            v
        }
        "chsh" => {
            assert_eq!(x.len(), 16);
            assert!(x.iter().all(|z| z >= &n(0)));
            assert_eq!(x.iter().cloned().sum::<Q>(), n(1));
            let mut cs = vec![];
            let mut signs = vec![];
            for a in [-1, 1] {
                for b in [-1, 1] {
                    for c in [-1, 1] {
                        for d in [-1, 1] {
                            cs.push(n(a * (c + d) + b * (c - d)));
                            signs.push([a, b, c, d]);
                        }
                    }
                }
            }
            let mut cor = vec![];
            for i in 0..2 {
                for j in 0..2 {
                    cor.push(
                        x.iter()
                            .zip(&signs)
                            .map(|(w, s)| w * n(s[i] * s[2 + j]))
                            .sum(),
                    );
                }
            }
            let value: Q = x.iter().zip(&cs).map(|(w, z)| w * z).sum();
            let bound: Q = x.iter().zip(&cs).map(|(w, z)| w * z.abs()).sum();
            [cs, cor, vec![value, bound, n(2)], contexts(&n(1))].concat()
        }
        "nosignal" => stats(&x),
        "trace_select" => {
            let [p, q, c] = x.as_slice() else {
                panic!("arity")
            };
            unit(p);
            unit(q);
            assert!(c >= &n(0));
            let d = p - q;
            let a = d.abs();
            vec![
                d.clone(),
                -d,
                a.clone(),
                a.clone(),
                a.clone(),
                a.clone(),
                c * &a,
                n(2) * a,
            ]
        }
        "dual" => {
            let [r, s, t, k] = x.as_slice() else {
                panic!("arity")
            };
            assert!(s.abs() <= n(1) && t.abs() <= n(1));
            let sg = n(if r >= &n(0) { 1 } else { -1 });
            vec![
                r * s - r * t,
                r * (s + k) - r * (t + k),
                n(2) * r.abs(),
                r * &sg - r * (-&sg),
                sg.clone(),
                -sg,
                r.abs(),
            ]
        }
        "monotone" => {
            let [p, q, u, v] = x.as_slice() else {
                panic!("arity")
            };
            unit(p);
            unit(q);
            let y0 = p * u + q * v;
            let y1 = (n(1) - p) * u + (n(1) - q) * v;
            let a = u.abs() + v.abs();
            let b = y0.abs() + y1.abs();
            vec![
                y0,
                y1,
                a.clone(),
                b.clone(),
                n(2) * &a,
                n(2) * &b,
                &a - &b,
                n(2) * (a - b),
            ]
        }
        "stochastic" => {
            assert_eq!(x.len(), 12);
            let k: M = x[..9].chunks(3).map(|r| r.to_vec()).collect();
            assert!(x[..9].iter().all(|z| z >= &n(0)));
            let cols: Vec<Q> = (0..3)
                .map(|j| (0..3).map(|i| k[i][j].clone()).sum())
                .collect();
            assert_eq!(cols, vec![n(1); 3]);
            let v: M = x[9..].iter().map(|z| vec![z.clone()]).collect();
            let y = flat(&mm(&k, &v));
            let a: Q = x[9..].iter().map(|z| z.abs()).sum();
            let b: Q = y.iter().map(|z| z.abs()).sum();
            let budgets: Vec<Q> = (0..3)
                .map(|i| (0..3).map(|j| (&k[i][j] * &x[9 + j]).abs()).sum())
                .collect();
            [cols, y, vec![a, b], budgets].concat()
        }
        "channel" => {
            let [t, u, p, c] = x.as_slice() else {
                panic!("arity")
            };
            unit(p);
            assert!(sq(c) <= p * (n(1) - p));
            let (r, s) = rot(t);
            let (v, w) = rot(u);
            let ks = vec![
                vec![vec![r.clone(), n(0)], vec![n(0), n(0)]],
                vec![vec![n(0), n(0)], vec![s.clone(), n(0)]],
                vec![vec![n(0), v.clone()], vec![n(0), n(0)]],
                vec![vec![n(0), n(0)], vec![n(0), w.clone()]],
            ];
            let rho = vec![vec![p.clone(), c.clone()], vec![c.clone(), n(1) - p]];
            let mut comp = vec![vec![n(0); 2]; 2];
            let mut res = comp.clone();
            for k in &ks {
                let a = mm(&tr(k), k);
                let b = mm(&mm(k, &rho), &tr(k));
                for i in 0..2 {
                    for j in 0..2 {
                        comp[i][j] += &a[i][j];
                        res[i][j] += &b[i][j];
                    }
                }
            }
            let kernel = vec![vec![sq(&r), sq(&v)], vec![sq(&s), sq(&w)]];
            let mut out = flat(&kernel);
            for k in &ks {
                out.extend(flat(k));
            }
            out.extend(flat(&comp));
            out.extend(flat(&res));
            out.extend(flat(&rho));
            out.extend([p.clone(), n(0), n(0), n(1) - p]);
            out.extend(flat(&mm(
                &vec![vec![n(0), n(1)], vec![n(1), n(0)]],
                &kernel,
            )));
            out
        }
        "firewall" => {
            let [score, defect, bound] = x.as_slice() else {
                panic!("arity")
            };
            for z in &x {
                integer(z, 0, 1000000);
            }
            vec![
                score.clone(),
                defect.clone(),
                bound.clone(),
                n(defect.is_zero() as i64),
                score + n(1),
                n(defect.is_zero() as i64),
            ]
        }
        _ => panic!("unknown resource operation"),
    };
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
    fn resources_projection() {
        let v = run("projection", &["1", "2", "1", "0"]);
        assert_eq!(v[4], n(0));
        assert_ne!(v[6], v[7]);
    }
    #[test]
    fn resources_fiber() {
        let v = run("fiber", &["1", "0", "1", "0"]);
        assert_eq!(v[0], v[2]);
        assert_eq!(v[1], v[3]);
        assert_ne!(v[4], v[5]);
    }
    #[test]
    fn resources_buildability() {
        let v = run("buildability", &["10", "15", "0", "1", "1", "1"]);
        assert_eq!(v[5], n(1));
    }
    #[test]
    fn resources_interference() {
        let v = run("interference", &["1", "0", "1", "0"]);
        assert_eq!(v[6], v[7]);
        assert_eq!(v[6], n(2));
    }
    #[test]
    fn resources_torsion() {
        let v = run("torsion", &["0"]);
        assert_eq!(v[..4], [n(1), n(0), n(0), n(1)]);
    }
    #[test]
    fn resources_selector() {
        let v = run("selector", &["3", "4", "1", "2"]);
        assert_eq!(v[6], v[9]);
        assert!(v[7].is_zero() && v[8].is_zero());
    }
    #[test]
    fn resources_holonomy() {
        let v = run("holonomy", &["1", "0", "1", "0", "0"]);
        assert_eq!(v[6..8], v[8..10]);
        assert_eq!(v[12], v[13]);
    }
    #[test]
    fn resources_annex() {
        let v = run(
            "annex",
            &["1", "2", "3", "0", "2", "-1", "1/2", "1/3", "1", "-1", "1"],
        );
        assert_eq!(v[3], n(0));
        assert_eq!(v[4], v[5]);
        assert!(v[9] <= v[8]);
    }
    #[test]
    fn resources_product() {
        let v = run("product", &["1", "0", "0", "1"]);
        assert_eq!(v[21], n(4) * sq(&v[22]));
        assert!(v[21] > n(0));
    }
    #[test]
    fn resources_witness() {
        let v = run("witness", &["1", "0", "1", "0"]);
        assert_eq!(v[20], n(1));
        assert_eq!(v[22], v[23]);
        assert!(v[21] <= n(1) / n(2));
    }
    #[test]
    fn resources_qubit() {
        let v = run("qubit", &["1", "1"]);
        assert_eq!(v[0], v[4]);
        assert_ne!(v[14], v[15]);
        assert_eq!(v[16], n(1));
    }
    #[test]
    fn resources_bell_import() {
        let v = run("bell_import", &["0"]);
        assert!(v[16 + 32] <= n(4));
        assert_eq!(v[16 + 20..16 + 28], vec![n(0); 8]);
    }
    #[test]
    fn resources_chsh() {
        let v = run(
            "chsh",
            &[
                "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16",
                "1/16", "1/16", "1/16", "1/16", "1/16", "1/16",
            ],
        );
        assert!(v[20].abs() <= n(2));
        assert_eq!(v[21], n(2));
    }
    #[test]
    fn resources_nosignal() {
        let v = run(
            "nosignal",
            &[
                "1/2", "0", "0", "1/2", "1/2", "0", "0", "1/2", "1/2", "0", "0", "1/2", "0", "1/2",
                "1/2", "0",
            ],
        );
        assert_eq!(v[20..28], vec![n(0); 8]);
        assert_ne!(v[33], n(0));
    }
    #[test]
    fn resources_trace_select() {
        let v = run("trace_select", &["1/4", "3/4", "1"]);
        assert_eq!(v[4], v[5]);
        assert_eq!(v[7], n(2) * &v[4]);
    }
    #[test]
    fn resources_dual() {
        let v = run("dual", &["2", "1", "-1", "5"]);
        assert_eq!(v[0], v[1]);
        assert_eq!(v[2], v[3]);
    }
    #[test]
    fn resources_monotone() {
        let v = run("monotone", &["1/2", "1/2", "1", "-1"]);
        assert!(v[3] <= v[2]);
        assert_eq!(v[5], n(2) * &v[3]);
    }
    #[test]
    fn resources_stochastic() {
        let v = run(
            "stochastic",
            &["1", "0", "0", "0", "1", "0", "0", "0", "1", "1", "-2", "3"],
        );
        assert!(v[7] <= v[6]);
    }
    #[test]
    fn resources_channel() {
        let v = run("channel", &["0", "1/2", "1/2", "1/2"]);
        assert_eq!(v[20..24], [n(1), n(0), n(0), n(1)]);
        assert_eq!(&v[24] + &v[27], n(1));
    }
    #[test]
    fn resources_firewall() {
        let v = run("firewall", &["0", "0", "0"]);
        assert_eq!(v[3], v[5]);
        assert_eq!(v[3], n(1));
    }
    #[test]
    #[should_panic]
    fn resources_reject_invalid_kernel() {
        run("monotone", &["2", "0", "1", "-1"]);
    }
}
