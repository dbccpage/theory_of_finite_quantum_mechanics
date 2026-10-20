//! Exact finite computations with literal import boundaries and validity tags.
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
fn mm(a: &[Q], b: &[Q]) -> Vec<Q> {
    (0..2)
        .flat_map(|i| (0..2).map(move |j| (0..2).map(|k| &a[2 * i + k] * &b[2 * k + j]).sum()))
        .collect()
}
fn act(a: &[Q], v: &[Q]) -> Vec<Q> {
    (0..2)
        .map(|i| &a[2 * i] * &v[0] + &a[2 * i + 1] * &v[1])
        .collect()
}
fn sq(v: &Q) -> Q {
    v * v
}
pub fn evaluate(kind: &str, values: &[String]) -> Vec<String> {
    let x = values.iter().map(|v| parse(v)).collect::<Vec<_>>();
    let mut o: Vec<Q> = vec![];
    let bit = |v: bool| n(v as i64);
    macro_rules! e{($($v:expr),* $(,)?)=>{$(o.push($v);)*};}
    match kind {
        "isometry" => {
            let k = x[0].to_integer().to_usize().unwrap();
            assert!(x[0].is_integer() && k < 4);
            let (a, b) = (&x[1], &x[2]);
            let f = [k / 2, k % 2];
            let t = (0..2)
                .flat_map(|i| (0..2).map(move |j| bit(f[j] == i)))
                .collect::<Vec<_>>();
            let g = (0..2)
                .flat_map(|i| {
                    (0..2).map({
                        let t = &t;
                        move |j| (0..2).map(|k| &t[2 * k + i] * &t[2 * k + j]).sum::<Q>()
                    })
                })
                .collect::<Vec<_>>();
            let v = act(&t, &[a.clone(), b.clone()]);
            o.extend(t.clone());
            o.extend(g);
            e!(&t[0] * &t[3] - &t[1] * &t[2], bit(f[0] != f[1]));
            o.extend(v.clone());
            e!(a * a + b * b, v.iter().map(sq).sum());
        }
        "orthogonal" => {
            let (a, b, c, d) = (&x[0], &x[1], &x[2], &x[3]);
            assert!(a * a + b * b == n(1));
            let p = vec![a * a, a * b, a * b, b * b];
            let r = vec![b * b, -a * b, -a * b, a * a];
            let u = sq(&(a * c + b * d));
            let v = sq(&(-b * c + a * d));
            o.extend(p.clone());
            o.extend(r.clone());
            o.extend((0..4).map(|i| &p[i] + &r[i]));
            e!(
                u.clone(),
                v.clone(),
                &u + &v,
                c * c + d * d,
                &u * &u + &v * &v,
                sq(&sq(c)) + sq(&sq(d)),
                &u * &u + &v * &v - sq(&sq(c)) - sq(&sq(d))
            );
        }
        "sqrt" => {
            if x.iter().any(|v| v < &n(0)) {
                return vec!["-1".into()];
            };
            let m = x.iter().cloned().sum::<Q>();
            if m.is_zero() {
                return vec!["0".into()];
            };
            let p = x.iter().map(|v| v / &m).collect::<Vec<_>>();
            let mut roots = vec![];
            let mut flags = vec![];
            for z in &p {
                let a = z.numer().sqrt();
                let b = z.denom().sqrt();
                let yes = &a * &a == *z.numer() && &b * &b == *z.denom();
                flags.push(bit(yes));
                roots.push(if yes { Q::new(a, b) } else { n(0) });
            }
            e!(n(1), m);
            o.extend(p);
            o.extend(flags.clone());
            o.extend(roots);
            o.push(bit(flags.iter().all(|v| *v == n(1))));
        }
        "phases" => {
            let (a, b) = (&x[0], &x[1]);
            e!(a * a, b * b);
            for (u, v) in [(1, 0), (0, 1), (-1, 0), (0, -1)] {
                o.push(sq(&(a + b * n(u))) + sq(&(b * n(v))));
            }
            e!(sq(&(a + b)), sq(&(a + b)), sq(&(a - b)), n(2) * a * b);
        }
        "trace" => {
            let v = &x[..3];
            let (s, has, m) = (&x[3], &x[4], &x[5]);
            assert!((*has == n(0) || *has == n(1)) && *m >= n(0));
            let w = v.iter().map(|z| z.abs()).sum::<Q>();
            if w.is_zero() || s.is_zero() {
                return vec!["0".into()];
            };
            let p = v.iter().map(|z| z.abs() / &w).collect::<Vec<_>>();
            let scaled = v.iter().map(|z| (s * z).abs()).collect::<Vec<_>>();
            let sw = scaled.iter().cloned().sum::<Q>();
            let out = p
                .iter()
                .map(|z| if has.is_zero() { n(0) } else { m * z })
                .collect::<Vec<_>>();
            o.push(n(1));
            for i in 0..3 {
                for j in 0..3 {
                    o.push(if i == j { v[i].clone() } else { n(0) });
                }
            }
            o.extend(v.iter().map(|v| v.abs()));
            e!(w, sw.clone());
            o.extend(p);
            o.extend(scaled.iter().map(|v| v / &sw));
            o.push(has.clone());
            o.extend(out.clone());
            o.push(bit(
                !has.is_zero() && out == v.iter().map(|z| z.abs()).collect::<Vec<_>>()
            ));
        }
        "factor" => {
            let (p, q, r, s, a, b) = (&x[0], &x[1], &x[2], &x[3], &x[4], &x[5]);
            assert!(
                [p, q, r, s].iter().all(|z| **z >= n(0) && **z <= n(1))
                    && *a >= n(0)
                    && *b >= n(0)
                    && a + b == n(1)
            );
            let t = vec![p.clone(), n(1) - q, n(1) - p, q.clone()];
            let u = vec![r.clone(), n(1) - s, n(1) - r, s.clone()];
            let c = mm(&t, &u);
            let v = act(&c, &[a.clone(), b.clone()]);
            let via = act(&t, &act(&u, &[a.clone(), b.clone()]));
            o.extend(t);
            o.extend(u);
            o.extend(c);
            o.extend(v.clone());
            o.extend(via);
            e!(
                v[0].clone(),
                n(0),
                n(0),
                v[1].clone(),
                n(2),
                n(0),
                n(0),
                n(2),
                n(1),
                n(0),
                n(0),
                n(1)
            );
        }
        "branch" => {
            let (a, b) = (&x[0], &x[1]);
            let nn = a * a + b * b;
            if nn.is_zero() {
                return vec!["0".into()];
            };
            let matrix_a = vec![a * a / &nn, a * b / &nn, a * b / &nn, b * b / &nn];
            let matrix_b = vec![a * a / &nn, -a * b / &nn, -a * b / &nn, b * b / &nn];
            let d = vec![a * a / &nn, n(0), n(0), b * b / &nn];
            let c = Q::new(3.into(), 5.into());
            let s = Q::new(4.into(), 5.into());
            let matrix_r = vec![c.clone(), -s.clone(), s.clone(), c.clone()];
            let v = act(&matrix_r, &[a.clone(), b.clone()]);
            let w = act(&matrix_r, &[a.clone(), -b]);
            o.push(n(1));
            o.extend(matrix_a);
            o.extend(matrix_b);
            o.extend(d.clone());
            o.extend(d);
            o.extend(v.iter().map(|v| v * v / &nn));
            o.extend(w.iter().map(|v| v * v / &nn));
            o.push(-n(4) * c * s * a * b / &nn);
        }
        "normalize" => {
            let w = &x[..3];
            let c = &x[3];
            let m = w.iter().cloned().sum::<Q>();
            if m.is_zero() {
                return vec!["0".into()];
            };
            let p = w.iter().map(|v| v / &m).collect::<Vec<_>>();
            let scaled = w.iter().map(|v| c * v).collect::<Vec<_>>();
            let s = scaled.iter().cloned().sum::<Q>();
            let q = scaled
                .iter()
                .map(|v| if s.is_zero() { n(0) } else { v / &s })
                .collect::<Vec<_>>();
            e!(n(1), m.clone(), s.clone());
            o.extend(p.clone());
            o.extend(p.clone());
            o.push(bit(!s.is_zero()));
            o.extend(q.clone());
            e!(
                bit(!s.is_zero() && p == q),
                bit(*c > n(0)),
                bit(w.iter().all(|v| *v >= n(0)) && m > n(0))
            );
        }
        "defect" => {
            let (a, b) = (&x[0], &x[1]);
            let d = a.abs() + b.abs() - (a + b).abs();
            e!(
                a.abs(),
                b.abs(),
                d.clone(),
                a.abs() + b.abs(),
                n(0),
                bit(a * b >= n(0)),
                bit(d.is_zero()),
                bit(a * b < n(0))
            );
        }
        "minkowski" => {
            let (a, b, p) = (&x[0], &x[1], &x[2]);
            let k = p.to_integer().to_i32().unwrap();
            assert!(p.is_integer() && (2..=6).contains(&k) && *a >= n(0) && *b >= n(0));
            let aa = a.pow(k);
            let bb = b.pow(k);
            let cc = (a + b).pow(k);
            e!(
                aa.clone(),
                bb.clone(),
                cc.clone(),
                &aa + &bb,
                &cc - &aa - &bb,
                bit(cc > aa + bb),
                bit(*a > n(0) && *b > n(0))
            );
        }
        "sparse" => {
            let (a, b, c, d) = (&x[0], &x[1], &x[2], &x[3]);
            let plus = vec![sq(&(a + b)), sq(&(c + d))];
            let minus = vec![sq(&(a - b)), sq(&(c - d))];
            let rs = (a * b).is_zero() && (c * d).is_zero();
            let mono = (a.is_zero() != b.is_zero())
                && (c.is_zero() != d.is_zero())
                && (a.is_zero() != c.is_zero())
                && (b.is_zero() != d.is_zero());
            let det = a * d - b * c;
            let rank = if !det.is_zero() {
                2
            } else {
                (x.iter().any(|v| !v.is_zero())) as i64
            };
            o.extend(plus.clone());
            o.extend(minus.clone());
            o.extend((0..2).map(|i| &plus[i] - &minus[i]));
            e!(bit(rs), det, bit(mono), n(rank));
        }
        "redundancy" => {
            let w = &x[..3];
            let a = &x[3..];
            assert!(w.iter().all(|v| *v >= n(0)));
            let z = (0..3)
                .map(|i| sq(&a[2 * i]) + sq(&a[2 * i + 1]))
                .collect::<Vec<_>>();
            let ww = w.iter().cloned().sum::<Q>();
            let nn = z.iter().cloned().sum::<Q>();
            if ww.is_zero() || nn.is_zero() {
                return vec!["0".into()];
            };
            let p = w.iter().map(|v| v / &ww).collect::<Vec<_>>();
            let q = z.iter().map(|v| v / &nn).collect::<Vec<_>>();
            o.push(n(1));
            o.extend(z.clone());
            e!(ww, nn, bit(z == w));
            o.extend(p.clone());
            o.extend(q.clone());
            o.push(bit(p == q));
        }
        "shadow" => {
            let matrix_a = &x[..9];
            let u = &x[9..];
            let ph = [(1, 0), (0, 1), (-1, 0), (0, -1)];
            let mut means = vec![n(0); 18];
            let mut vals = vec![];
            for i in 0..4 {
                for j in 0..4 {
                    for k in 0..4 {
                        let gs = [ph[i], ph[j], ph[k]];
                        let mut matrix_b = vec![];
                        for s in 0..3 {
                            for t in 0..3 {
                                matrix_b.push(
                                    &matrix_a[3 * s + t] * n(gs[s].0 * gs[t].0 + gs[s].1 * gs[t].1),
                                );
                                matrix_b.push(
                                    &matrix_a[3 * s + t] * n(gs[s].1 * gs[t].0 - gs[s].0 * gs[t].1),
                                );
                            }
                        }
                        for z in 0..18 {
                            means[z] += &matrix_b[z];
                        }
                        let mut v = n(0);
                        for s in 0..3 {
                            for t in 0..3 {
                                v += &u[s] * &matrix_b[2 * (3 * s + t)] * &u[t];
                            }
                        }
                        vals.push(v);
                    }
                }
            }
            let diag = (0..3)
                .flat_map(|i| {
                    (0..3).map(move |j| {
                        if i == j {
                            matrix_a[3 * i + j].clone()
                        } else {
                            n(0)
                        }
                    })
                })
                .collect::<Vec<_>>();
            let coherent = (0..3)
                .flat_map(|i| (0..3).map(move |j| &u[i] * &matrix_a[3 * i + j] * &u[j]))
                .sum::<Q>();
            e!(n(64));
            o.extend(means.iter().map(|v| v / n(64)));
            o.extend(diag);
            o.extend(vals.clone());
            e!(
                coherent.clone(),
                vals.iter().cloned().sum::<Q>() / n(64),
                (0..3).map(|i| sq(&u[i]) * &matrix_a[4 * i]).sum::<Q>(),
                coherent
            );
        }
        "scope" => {
            if x.iter().any(|v| *v < n(0)) {
                return vec!["-1".into()];
            };
            let w = x.iter().cloned().sum::<Q>();
            let s = x.iter().map(sq).sum::<Q>();
            if w.is_zero() {
                return vec!["0".into()];
            };
            let p = x.iter().map(|v| v / &w).collect::<Vec<_>>();
            let q = x.iter().map(|v| v * v / &s).collect::<Vec<_>>();
            o.push(n(1));
            o.extend(p.clone());
            o.extend(q.clone());
            e!(
                &p[0] + &p[1],
                p[2].clone(),
                &q[0] + &q[1],
                q[2].clone(),
                n(1),
                n(1)
            );
            o.extend((0..3).map(|i| &p[i] - &q[i]));
        }
        "gleason" => {
            let (a, b, c, u, v) = (&x[0], &x[1], &x[2], &x[3], &x[4]);
            assert!(a + c == n(1) && *a >= n(0) && *c >= n(0) && a * c >= b * b);
            if u * u + v * v != n(1) {
                return vec!["-1".into()];
            };
            let f = |s: &Q, t: &Q| a * s * s + n(2) * b * s * t + c * t * t;
            let ee = f(u, v);
            let ff = f(&(-v), u);
            let z = f(&Q::new(3.into(), 5.into()), &Q::new(4.into(), 5.into()));
            let rec = (&z - Q::new(9.into(), 25.into()) * a - Q::new(16.into(), 25.into()) * c)
                / Q::new(24.into(), 25.into());
            e!(
                n(1),
                ee.clone(),
                ff.clone(),
                ee + ff,
                a.clone(),
                c.clone(),
                z,
                rec,
                a.clone(),
                b.clone(),
                b.clone(),
                c.clone(),
                a * c - b * b
            );
        }
        "capacity" => {
            let (a, b, c, s) = (&x[0], &x[1], &x[2], &x[3]);
            assert!(c * c + s * s == n(1));
            let nn = a * a + b * b;
            if nn.is_zero() {
                return vec!["0".into()];
            };
            let matrix_r = vec![c.clone(), -s, s.clone(), c.clone()];
            let matrix_t = vec![c.clone(), s.clone(), -s, c.clone()];
            let v = act(&matrix_r, &[a.clone(), b.clone()]);
            let w = act(&matrix_r, &[a.clone(), -b]);
            o.push(n(1));
            o.extend(matrix_r.clone());
            o.extend(mm(&matrix_t, &matrix_r));
            o.extend(v.iter().map(|v| v * v / &nn));
            o.extend(w.iter().map(|v| v * v / &nn));
            e!(
                a * a / &nn,
                b * b / &nn,
                v.iter().map(sq).sum(),
                w.iter().map(sq).sum(),
                nn.clone(),
                -n(4) * c * s * a * b / nn
            );
        }
        "ladder" => {
            let (p, q, a, b, k) = (&x[0], &x[1], &x[2], &x[3], &x[4]);
            let nnstep = k.to_integer().to_usize().unwrap();
            assert!(
                k.is_integer()
                    && nnstep <= 4
                    && *p >= n(0)
                    && *p <= n(1)
                    && *q >= n(0)
                    && *q <= n(1)
            );
            let nn = a * a + b * b;
            if nn.is_zero() {
                return vec!["0".into()];
            };
            let matrix_t = vec![p.clone(), n(1) - q, n(1) - p, q.clone()];
            let mut power = vec![n(1), n(0), n(0), n(1)];
            for _ in 0..nnstep {
                power = mm(&power, &matrix_t);
            }
            let mut terms = vec![];
            let mut matrix_p = vec![n(0); 4];
            for start in 0..2 {
                for code in 0..(1usize << nnstep) {
                    let mut state = start;
                    let mut w = n(1);
                    for step in 0..nnstep {
                        let dest = (code >> step) & 1;
                        w *= &matrix_t[2 * dest + state];
                        state = dest;
                    }
                    terms.push(w.clone());
                    matrix_p[2 * state + start] += w;
                }
            }
            let v = act(&power, &[a * a / &nn, b * b / &nn]);
            o.push(n(1));
            o.extend(power);
            o.extend(matrix_p);
            o.extend(terms);
            o.extend(v);
            e!(
                sq(&(a + b)) / (n(2) * &nn),
                sq(&(a - b)) / (n(2) * &nn),
                Q::new(1.into(), 2.into()),
                Q::new(1.into(), 2.into()),
                a * b / nn
            );
        }
        "pairing" => {
            let (a, b, c, d) = (&x[0], &x[1], &x[2], &x[3]);
            let aa = a * a + b * b;
            let bb = c * c + d * d;
            let ww = &aa + &bb;
            let ss = &aa * &aa + &bb * &bb;
            if ww.is_zero() {
                return vec!["0".into()];
            };
            let matrix_h = vec![sq(&(a + c)) + sq(&(b + d)), sq(&(a - c)) + sq(&(b - d))];
            let matrix_r = vec![sq(&(a - d)) + sq(&(b + c)), sq(&(a + d)) + sq(&(b - c))];
            e!(
                n(1),
                aa.clone(),
                bb.clone(),
                &aa * &aa,
                &bb * &bb,
                bb.clone(),
                aa.clone(),
                &aa / &ww,
                &bb / &ww,
                &aa * &aa / &ss,
                &bb * &bb / &ss,
                ww,
                ss
            );
            o.extend(matrix_h.clone());
            o.extend(matrix_r.clone());
            e!(
                matrix_h.iter().cloned().sum(),
                matrix_r.iter().cloned().sum(),
                matrix_h.iter().map(sq).sum(),
                matrix_r.iter().map(sq).sum(),
                matrix_h.iter().map(sq).sum::<Q>() - matrix_r.iter().map(sq).sum::<Q>()
            );
        }
        "selector" => {
            let nn = x[0].to_integer().to_usize().unwrap();
            assert!(x[0].is_integer() && [2, 3, 4].contains(&nn));
            let matrix_t = (0..nn)
                .flat_map(|i| (0..nn).map(move |j| bit(i == (j + 1) % nn)))
                .collect::<Vec<_>>();
            let matrix_s = (0..nn)
                .flat_map(|i| {
                    (0..nn).map({
                        let matrix_t = &matrix_t;
                        move |j| {
                            (0..nn)
                                .map(|k| &matrix_t[nn * i + k] * &matrix_t[nn * k + j])
                                .sum::<Q>()
                        }
                    })
                })
                .collect::<Vec<_>>();
            let matrix_i = (0..nn)
                .flat_map(|i| (0..nn).map(move |j| bit(i == j)))
                .collect::<Vec<_>>();
            o.extend(matrix_t);
            o.extend(matrix_s.clone());
            o.extend(matrix_i.clone());
            e!(n(nn as i64), bit(matrix_s == matrix_i), bit(nn > 2));
        }
        "finish" => {
            let (a, b) = (&x[0], &x[1]);
            let nn = a * a + b * b;
            let units = (0..4)
                .map(|k| (0..4).map(|j| bit(k == j)).collect::<Vec<_>>())
                .collect::<Vec<_>>();
            e!(
                nn.clone(),
                bit(nn == n(1)),
                bit(!nn.is_zero()),
                if nn.is_zero() { n(0) } else { a / &nn },
                if nn.is_zero() { n(0) } else { -b / &nn }
            );
            for matrix_a in &units {
                for matrix_b in &units {
                    o.extend(mm(matrix_a, matrix_b));
                }
            }
            let matrix_u = mm(&units[1], &units[2]);
            let matrix_v = mm(&units[2], &units[1]);
            o.extend((0..4).map(|i| &matrix_u[i] - &matrix_v[i]));
        }
        _ => panic!("unknown declared finite operation"),
    }
    o.iter().map(ToString::to_string).collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn born_boundary_isometry() {
        let input = vec!["0".to_string(), "1".to_string(), "-1".to_string()];
        let y = evaluate("isometry", &input);
        assert_eq!(
            &y[0..14],
            &["1", "1", "0", "0", "1", "1", "1", "1", "0", "0", "0", "0", "2", "0"]
        );
    }
    #[test]
    fn born_boundary_orthogonal() {
        let input = vec![
            "1".to_string(),
            "0".to_string(),
            "2".to_string(),
            "1".to_string(),
        ];
        let y = evaluate("orthogonal", &input);
        assert_eq!(&y[12..19], &["4", "1", "5", "5", "17", "17", "0"]);
    }
    #[test]
    fn born_boundary_sqrt() {
        let input = vec!["9".to_string(), "16".to_string(), "0".to_string()];
        let y = evaluate("sqrt", &input);
        assert_eq!(
            &y[0..12],
            &["1", "25", "9/25", "16/25", "0", "1", "1", "1", "3/5", "4/5", "0", "1"]
        );
    }
    #[test]
    fn born_boundary_phases() {
        let input = vec!["1".to_string(), "1".to_string()];
        let y = evaluate("phases", &input);
        assert_eq!(
            &y[0..10],
            &["1", "1", "4", "2", "0", "2", "4", "4", "0", "2"]
        );
    }
    #[test]
    fn born_boundary_trace() {
        let input = vec![
            "2".to_string(),
            "-1".to_string(),
            "1".to_string(),
            "-2".to_string(),
            "1".to_string(),
            "4".to_string(),
        ];
        let y = evaluate("trace", &input);
        assert_eq!(
            &y[13..26],
            &["4", "8", "1/2", "1/4", "1/4", "1/2", "1/4", "1/4", "1", "2", "1", "1", "1"]
        );
    }
    #[test]
    fn born_boundary_factor() {
        let input = vec![
            "1".to_string(),
            "1".to_string(),
            "0".to_string(),
            "0".to_string(),
            "1".to_string(),
            "0".to_string(),
        ];
        let y = evaluate("factor", &input);
        assert_eq!(&y[20..28], &["2", "0", "0", "2", "1", "0", "0", "1"]);
    }
    #[test]
    fn born_boundary_branch() {
        let input = vec!["1".to_string(), "1".to_string()];
        let y = evaluate("branch", &input);
        assert_eq!(&y[17..22], &["1/50", "49/50", "49/50", "1/50", "-24/25"]);
    }
    #[test]
    fn born_boundary_normalize() {
        let input = vec![
            "1".to_string(),
            "2".to_string(),
            "3".to_string(),
            "-2".to_string(),
        ];
        let y = evaluate("normalize", &input);
        assert_eq!(&y[13..16], &["1", "0", "1"]);
    }
    #[test]
    fn born_boundary_defect() {
        let input = vec!["1".to_string(), "-1".to_string()];
        let y = evaluate("defect", &input);
        assert_eq!(&y[0..8], &["1", "1", "2", "2", "0", "0", "0", "1"]);
    }
    #[test]
    fn born_boundary_minkowski() {
        let input = vec!["2".to_string(), "3".to_string(), "3".to_string()];
        let y = evaluate("minkowski", &input);
        assert_eq!(&y[0..7], &["8", "27", "125", "35", "90", "1", "1"]);
    }
    #[test]
    fn born_boundary_sparse() {
        let input = vec![
            "1".to_string(),
            "0".to_string(),
            "2".to_string(),
            "0".to_string(),
        ];
        let y = evaluate("sparse", &input);
        assert_eq!(
            &y[0..10],
            &["1", "4", "1", "4", "0", "0", "1", "0", "0", "1"]
        );
    }
    #[test]
    fn born_boundary_redundancy() {
        let input = vec![
            "9".to_string(),
            "16".to_string(),
            "0".to_string(),
            "3".to_string(),
            "0".to_string(),
            "4".to_string(),
            "0".to_string(),
            "0".to_string(),
            "0".to_string(),
        ];
        let y = evaluate("redundancy", &input);
        assert_eq!(
            &y[7..14],
            &["9/25", "16/25", "0", "9/25", "16/25", "0", "1"]
        );
    }
    #[test]
    fn born_boundary_shadow() {
        let input = vec![
            "1/2".to_string(),
            "1/8".to_string(),
            "0".to_string(),
            "1/8".to_string(),
            "1/4".to_string(),
            "1/8".to_string(),
            "0".to_string(),
            "1/8".to_string(),
            "1/4".to_string(),
            "2".to_string(),
            "1".to_string(),
            "1/2".to_string(),
        ];
        let y = evaluate("shadow", &input);
        assert_eq!(&y[92..96], &["47/16", "37/16", "37/16", "47/16"]);
    }
    #[test]
    fn born_boundary_scope() {
        let input = vec!["2".to_string(), "1".to_string(), "1".to_string()];
        let y = evaluate("scope", &input);
        assert_eq!(&y[13..16], &["-1/6", "1/12", "1/12"]);
    }
    #[test]
    fn born_boundary_gleason() {
        let input = vec![
            "1/2".to_string(),
            "0".to_string(),
            "1/2".to_string(),
            "3/5".to_string(),
            "4/5".to_string(),
        ];
        let y = evaluate("gleason", &input);
        assert_eq!(&y[7..13], &["0", "1/2", "0", "0", "1/2", "1/4"]);
    }
    #[test]
    fn born_boundary_capacity() {
        let input = vec![
            "1".to_string(),
            "1".to_string(),
            "3/5".to_string(),
            "4/5".to_string(),
        ];
        let y = evaluate("capacity", &input);
        assert_eq!(
            &y[9..19],
            &["1/50", "49/50", "49/50", "1/50", "1/2", "1/2", "2", "2", "2", "-24/25"]
        );
    }
    #[test]
    fn born_boundary_ladder() {
        let input = vec![
            "1".to_string(),
            "1".to_string(),
            "1".to_string(),
            "1".to_string(),
            "0".to_string(),
        ];
        let y = evaluate("ladder", &input);
        assert_eq!(
            &y[9..18],
            &["1", "1", "1/2", "1/2", "1", "0", "1/2", "1/2", "1/2"]
        );
    }
    #[test]
    fn born_boundary_pairing() {
        let input = vec![
            "2".to_string(),
            "0".to_string(),
            "1".to_string(),
            "0".to_string(),
        ];
        let y = evaluate("pairing", &input);
        assert_eq!(
            &y[13..22],
            &["9", "1", "5", "5", "10", "10", "82", "50", "32"]
        );
    }
    #[test]
    fn born_boundary_selector() {
        let input = vec!["3".to_string()];
        let y = evaluate("selector", &input);
        assert_eq!(&y[27..30], &["3", "0", "1"]);
    }
    #[test]
    fn born_boundary_finish() {
        let input = vec!["1".to_string(), "1".to_string()];
        let y = evaluate("finish", &input);
        assert_eq!(&y[69..73], &["1", "0", "0", "-1"]);
    }
}
