//! Exact operations; bounded enumerations never imply an unbounded theorem.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::{One, ToPrimitive, Zero};
use std::path::Path;
fn q(s: &str) -> Q {
    let (a, b) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(a.parse::<BigInt>().unwrap(), b.parse::<BigInt>().unwrap())
}
fn n(v: i64) -> Q {
    Q::from_integer(v.into())
}
fn sq(v: &Q) -> Q {
    v * v
}
fn binary(x: &Q, y: &Q) -> Q {
    n(
        if x * y > Q::zero() || (x * y == Q::zero() && y.is_zero()) {
            1
        } else {
            0
        },
    )
}
pub fn evaluate(kind: &str, vs: &[String], root: &Path) -> Vec<String> {
    if kind == "corpus" || kind == "custody" {
        let b = std::fs::read(root.join(&vs[0])).unwrap();
        let count = |s: &[u8]| b.windows(s.len()).filter(|w| *w == s).count();
        return vec![
            b.len(),
            b.iter().filter(|v| **v == b'\n').count(),
            count(b"sorry"),
            count(b"Classical.choice"),
            count(b"axiom"),
        ]
        .iter()
        .map(|v| v.to_string())
        .collect();
    }
    let x: Vec<Q> = vs.iter().map(|s| q(s)).collect();
    let two = n(2);
    let four = n(4);
    let out = match kind {
        "continuum" => vec![
            &two * &x[0],
            &two * &x[1],
            sq(&x[2]) - &x[2] - Q::one(),
            sq(&(&two * &x[2] - Q::one())),
            n(5),
        ],
        "tensor" => {
            let a = &x[0];
            let b = &x[1];
            let c = &x[2];
            let d = &x[3];
            let v = vec![a * c, a * d, b * c, b * d];
            let det = &v[0] * &v[3] - &v[1] * &v[2];
            let norm = v.iter().map(sq).sum();
            let mut out = v;
            out.extend([det, norm, (sq(a) + sq(b)) * (sq(c) + sq(d))]);
            out
        }
        "u1" => {
            let t = &x[0];
            assert!(x[1].is_integer());
            let k = x[1].to_integer().to_i64().unwrap();
            assert!(k.abs() <= 32);
            let den = Q::one() + sq(t);
            let re = (Q::one() - sq(t)) / &den;
            let im = &two * t / &den;
            let mut z = Q::one();
            let mut w = Q::zero();
            let a = q("3/5");
            let b = q(if k >= 0 { "4/5" } else { "-4/5" });
            for _ in 0..k.abs() {
                (z, w) = (&z * &a - &w * &b, &z * &b + &w * &a);
            }
            vec![
                re.clone(),
                im.clone(),
                sq(&re) + sq(&im),
                &re + Q::one(),
                &im / (&re + Q::one()),
                z.clone(),
                w.clone(),
                sq(&z) + sq(&w),
            ]
        }
        "d2" => {
            let (a, b, k, u, v) = (&x[0], &x[1], &x[2], &x[3], &x[4]);
            assert!(!k.is_zero() && !(a.is_zero() && b.is_zero()) && !(u.is_zero() && v.is_zero()));
            vec![
                binary(a, b),
                binary(&(k * a), &(k * b)),
                binary(&(-b), a),
                a * u + b * v,
                binary(u, v),
                sq(a) + a * b,
                binary(a, b) * (sq(a) + sq(b)),
            ]
        }
        "interference" | "zero" => {
            let (a, b, c, d, v, w) = (&x[0], &x[1], &x[2], &x[3], &x[4], &x[5]);
            vec![
                sq(v),
                sq(w),
                sq(&(a * v + b * w)),
                sq(&(c * v + d * w)),
                sq(&(a * v - b * w)),
                sq(&(c * v - d * w)),
                &four * a * b * v * w,
                &four * c * d * v * w,
            ]
        }
        "fiber" => {
            assert!(x.iter().all(|v| v.is_integer()));
            let a = x[0].to_integer().to_i64().unwrap();
            let b = x[1].to_integer().to_i64().unwrap();
            let r = a.abs() + b.abs();
            assert!(r <= 10);
            let norm = a * a + b * b;
            let mut orbit = vec![(a, b), (-b, a), (-a, -b), (b, -a)];
            orbit.sort();
            orbit.dedup();
            let mut fiber = vec![];
            for u in -r..=r {
                for v in -r..=r {
                    if u * u + v * v == norm {
                        fiber.push((u, v));
                    }
                }
            }
            let mut out = vec![n(norm), n(orbit.len() as i64), n(fiber.len() as i64)];
            for (u, v) in orbit.into_iter().chain(fiber) {
                out.extend([n(u), n(v)]);
            }
            out
        }
        "weights" => {
            let (p, q, s, t) = (&x[0], &x[1], &x[2], &x[3]);
            let mass = p + q;
            vec![
                mass.clone(),
                std::cmp::min(p, q).clone(),
                p * s + q * t,
                -&two * &mass,
                &two * &mass,
            ]
        }
        _ => panic!("unknown operation"),
    };
    out.iter().map(|v| v.to_string()).collect()
}
#[cfg(test)]
mod tests {
    use super::*;
    fn run(k: &str, v: &[&str]) -> Vec<String> {
        evaluate(
            k,
            &v.iter().map(|s| s.to_string()).collect::<Vec<_>>(),
            Path::new("."),
        )
    }
    #[test]
    fn phase_scope_continuum() {
        assert_eq!(
            run("continuum", &["0", "1", "0"]),
            ["0", "2", "-1", "1", "5"]
        );
    }
    #[test]
    fn phase_scope_tensor() {
        let r = run("tensor", &["1", "2", "3", "4"]);
        assert_eq!(&r[4..], ["0", "125", "125"]);
    }
    #[test]
    fn phase_scope_u1() {
        let r = run("u1", &["3/4", "-1"]);
        assert_eq!(r[2], "1");
        assert_eq!(r[4], "3/4");
        assert_eq!(r[6], "-4/5");
    }
    #[test]
    fn phase_scope_d2() {
        let r = run("d2", &["1", "2", "-3", "-2", "1"]);
        assert_eq!(r[3], "0");
        assert_eq!(&r[5..], ["3", "5"]);
    }
    #[test]
    fn phase_scope_interference() {
        let r = run("interference", &["1", "1", "1", "-1", "1", "1"]);
        assert_eq!(&r[2..6], ["4", "0", "0", "4"]);
    }
    #[test]
    fn phase_scope_zero() {
        let r = run("zero", &["1", "1", "1", "1", "1", "1"]);
        assert_eq!(&r[2..6], ["4", "4", "0", "0"]);
    }
    #[test]
    fn phase_scope_fiber() {
        let r = run("fiber", &["5", "0"]);
        assert_eq!(&r[..3], ["25", "4", "12"]);
    }
    #[test]
    fn phase_scope_weights() {
        let r = run("weights", &["2", "-1", "2", "-2"]);
        assert_eq!(&r[..3], ["1", "-1", "6"]);
    }
    fn bytes(k: &str) {
        let p =
            std::env::temp_dir().join(format!("tfqm_phase_scope_{}_{}.txt", k, std::process::id()));
        std::fs::write(&p, b"axiom\nClassical.choice\nsorry\n").unwrap();
        let r = evaluate(k, &[p.to_string_lossy().into()], Path::new("."));
        std::fs::remove_file(p).unwrap();
        assert_eq!(&r[1..], ["3", "1", "1", "1"]);
    }
    #[test]
    fn phase_scope_corpus() {
        bytes("corpus");
    }
    #[test]
    fn phase_scope_custody() {
        bytes("custody");
    }
}
