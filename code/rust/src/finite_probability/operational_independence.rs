//! Independent exact controls by orbit partitions and disjoint-support ranks.
//! Finite fixtures supplement the universal Lean model and do not derive QM.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use serde::Deserialize;

type Mat = Vec<Vec<Q>>;
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Certificate {
    schema: String,
    authority_effect: String,
    premises: Vec<String>,
    systems: Vec<System>,
    channels: Channels,
    instrument: Vec<Vec<Vec<String>>>,
    hidden_states: Hidden,
}
// A typed channel record rejects duplicates at this nested object too.
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Channels {
    identity: Vec<Vec<String>>,
    flag_flip: Vec<Vec<String>>,
    visible_flip: Vec<Vec<String>>,
    noise: Vec<Vec<String>>,
}
impl std::ops::Index<&str> for Channels {
    type Output = Vec<Vec<String>>;
    fn index(&self, name: &str) -> &Self::Output {
        match name {
            "identity" => &self.identity,
            "flag_flip" => &self.flag_flip,
            "visible_flip" => &self.visible_flip,
            "noise" => &self.noise,
            _ => panic!("unknown channel"),
        }
    }
}
impl Channels {
    fn values(&self) -> impl Iterator<Item = &Vec<Vec<String>>> {
        [
            &self.identity,
            &self.flag_flip,
            &self.visible_flip,
            &self.noise,
        ]
        .into_iter()
    }
}
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct System {
    atoms: usize,
    points: usize,
    flip: Vec<usize>,
    orbits: Vec<Vec<usize>>,
    observe: Vec<Vec<String>>,
    prepare: Vec<Vec<String>>,
}
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Hidden {
    rho: Vec<String>,
    sigma: Vec<String>,
    effect: Vec<String>,
}
const PREMISES: [&str; 6] = [
    "finite nonempty carriers with a declared involutive symmetry",
    "real invariant state vectors with coordinatewise positivity and sum normalization",
    "all nonnegative equivariant matrices are processes; events have column sums at most one",
    "parallel composition uses the diagonal symmetry on the Cartesian product",
    "finite instruments have total column sum one and transformations retain ancillary distinctions",
    "this package does not assume purification, local complex quantum structure or primitive selection",
];
fn q(n: usize) -> Q {
    Q::from_integer(BigInt::from(n))
}
fn rat(s: &str) -> Q {
    assert!(s.len() <= 48);
    let x: Q = s.parse().expect("rational");
    assert_eq!(x.to_string(), s);
    x
}
fn matrix(s: &[Vec<String>], rows: usize, cols: usize) -> Mat {
    assert_eq!(s.len(), rows);
    s.iter()
        .map(|r| {
            assert_eq!(r.len(), cols);
            r.iter().map(|x| rat(x)).collect()
        })
        .collect()
}
fn shape(a: &Mat) -> (usize, usize) {
    assert!(!a.is_empty() && !a[0].is_empty());
    assert!(a.iter().all(|r| r.len() == a[0].len()));
    (a.len(), a[0].len())
}
fn mul(a: &Mat, b: &Mat) -> Mat {
    let (n, k) = shape(a);
    let (l, m) = shape(b);
    assert_eq!(k, l);
    (0..n)
        .map(|i| {
            (0..m)
                .map(|j| (0..k).map(|v| &a[i][v] * &b[v][j]).sum())
                .collect()
        })
        .collect()
}
fn tensor(a: &Mat, b: &Mat) -> Mat {
    let (n, k) = shape(a);
    let (m, l) = shape(b);
    (0..n * m)
        .map(|i| {
            (0..k * l)
                .map(|j| &a[i / m][j / l] * &b[i % m][j % l])
                .collect()
        })
        .collect()
}
fn eye(n: usize) -> Mat {
    (0..n)
        .map(|i| (0..n).map(|j| q(usize::from(i == j))).collect())
        .collect()
}
fn flip_point(mut x: usize, n: usize) -> usize {
    let mut output = 0;
    let mut place = 1;
    for _ in 0..n {
        let d = x % 4;
        output += (if d % 2 == 0 { d + 1 } else { d - 1 }) * place;
        x /= 4;
        place *= 4;
    }
    output
}
fn visible(mut x: usize, n: usize) -> usize {
    let mut out = 0;
    let mut place = 1;
    for _ in 0..n {
        out += (x % 4 / 2) * place;
        x /= 4;
        place *= 2;
    }
    out
}
fn event(t: &Mat, fi: &[usize], fo: &[usize], channel: bool) {
    let (m, n) = shape(t);
    assert_eq!(fi.len(), n);
    assert_eq!(fo.len(), m);
    for (size, f) in [(n, fi), (m, fo)] {
        let mut sorted = f.to_vec();
        sorted.sort_unstable();
        assert_eq!(sorted, (0..size).collect::<Vec<_>>());
        for x in 0..size {
            assert_eq!(f[f[x]], x);
        }
    }
    for x in 0..n {
        let total: Q = (0..m).map(|y| t[y][x].clone()).sum();
        if channel {
            assert_eq!(total, q(1));
        } else {
            assert!(total <= q(1));
        }
        for y in 0..m {
            assert!(t[y][x] >= q(0));
            assert_eq!(t[fo[y]][fi[x]], t[y][x]);
        }
    }
}
fn raw() -> Vec<u8> {
    std::fs::read(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(
        "../../../../dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T202420Z_operational_independence/candidate.json")).unwrap()
}
fn verify(raw: &[u8]) -> Certificate {
    assert!(raw.len() < 1_000_000);
    let c: Certificate = serde_json::from_slice(raw).expect("strict certificate schema");
    assert_eq!(c.schema, "operational-independence.v1");
    assert_eq!(c.authority_effect, "None");
    assert_eq!(c.premises, PREMISES);
    assert_eq!(c.systems.len(), 5);
    for (n, s) in c.systems.iter().enumerate() {
        assert_eq!(s.atoms, n);
        assert_eq!(s.points, 4usize.pow(n as u32));
        let want: Vec<_> = (0..s.points).map(|x| flip_point(x, n)).collect();
        assert_eq!(s.flip, want);
        let orbits: Vec<Vec<usize>> = (0..s.points)
            .filter(|&x| x <= want[x])
            .map(|x| {
                if x == want[x] {
                    vec![x]
                } else {
                    vec![x, want[x]]
                }
            })
            .collect();
        assert_eq!(s.orbits, orbits);
        let mut partition: Vec<_> = orbits.iter().flatten().copied().collect();
        partition.sort_unstable();
        assert_eq!(partition, (0..s.points).collect::<Vec<_>>());
        // Orbit indicator vectors have disjoint nonempty supports and span all
        // invariant vectors. Product-observation rows also have disjoint supports.
        let k = orbits.len();
        let d = 2usize.pow(n as u32);
        assert_eq!(
            k,
            if n == 0 {
                1
            } else {
                2usize.pow((2 * n - 1) as u32)
            }
        );
        let m = matrix(&s.observe, d, k);
        let r = matrix(&s.prepare, k, d);
        for j in 0..d {
            let count = orbits.iter().filter(|o| visible(o[0], n) == j).count();
            assert!(count > 0);
            for (i, o) in orbits.iter().enumerate() {
                assert_eq!(m[j][i], q(usize::from(visible(o[0], n) == j)));
                assert_eq!(r[i][j], &m[j][i] / q(count));
            }
            for j2 in 0..d {
                let dot: Q = (0..k).map(|i| &m[j][i] * &m[j2][i]).sum();
                assert_eq!(dot, if j == j2 { q(count) } else { q(0) });
            }
        }
        assert_eq!(mul(&m, &r), eye(d));
    }
    let fi = [1, 0, 3, 2];
    for (name, perm) in [
        ("identity", [0, 1, 2, 3]),
        ("flag_flip", fi),
        ("visible_flip", [2, 3, 0, 1]),
        ("noise", [0; 4]),
    ] {
        let t = matrix(&c.channels[name], 4, 4);
        event(&t, &fi, &fi, true);
        for y in 0..4 {
            for x in 0..4 {
                assert_eq!(
                    t[y][x],
                    if name == "noise" {
                        q(1) / q(4)
                    } else {
                        q(usize::from(y == perm[x]))
                    }
                );
            }
        }
    }
    assert_eq!(c.instrument.len(), 2);
    for j in 0..2 {
        let t = matrix(&c.instrument[j], 4, 4);
        event(&t, &fi, &fi, false);
        for y in 0..4 {
            for x in 0..4 {
                assert_eq!(t[y][x], q(usize::from(y == x && x / 2 == j)));
            }
        }
    }
    for (s, indices) in [
        (&c.hidden_states.rho, [0, 5]),
        (&c.hidden_states.sigma, [1, 4]),
    ] {
        assert_eq!(s.len(), 16);
        let p: Vec<_> = s.iter().map(|x| rat(x)).collect();
        assert_eq!(p.iter().cloned().sum::<Q>(), q(1));
        for x in 0..16 {
            assert_eq!(
                p[x],
                if indices.contains(&x) {
                    q(1) / q(2)
                } else {
                    q(0)
                }
            );
            assert_eq!(p[x], p[flip_point(x, 2)]);
        }
    }
    assert_eq!(c.hidden_states.effect.len(), 16);
    let e: Vec<_> = c.hidden_states.effect.iter().map(|x| rat(x)).collect();
    for x in 0..16 {
        assert_eq!(e[x], q(usize::from((x / 4) % 2 == x % 2)));
    }
    for (p, result) in [(&c.hidden_states.rho, q(1)), (&c.hidden_states.sigma, q(0))] {
        assert_eq!(e.iter().zip(p).map(|(e, x)| e * rat(x)).sum::<Q>(), result);
    }
    c
}
#[test]
fn exact_orbit_partitions_and_disjoint_support_ranks() {
    verify(&raw());
}
#[test]
fn composition_no_signalling_and_ancillary_separation() {
    let c = verify(&raw());
    let id = eye(4);
    let flip = matrix(&c.channels["flag_flip"], 4, 4);
    let corr: Mat = (0..16)
        .map(|i| vec![if i / 4 == i % 4 { q(1) / q(4) } else { q(0) }])
        .collect();
    assert_ne!(
        mul(&tensor(&id, &id), &corr),
        mul(&tensor(&flip, &id), &corr)
    );
    for ts in c.channels.values() {
        let t = matrix(ts, 4, 4);
        let out = mul(&tensor(&t, &id), &corr);
        for y in 0..4 {
            for x in 0..4 {
                assert_eq!(&out[4 * y + x][0] * q(4), t[y][x]);
            }
        }
        for ss in c.channels.values() {
            let s = matrix(ss, 4, 4);
            for k in 0..16 {
                let p: Mat = (0..16)
                    .map(|i| {
                        vec![q(usize::from(i == k) + usize::from(i == flip_point(k, 2))) / q(2)]
                    })
                    .collect();
                let out = mul(&tensor(&t, &s), &p);
                let marginal: Mat = (0..4)
                    .map(|i| vec![(0..4).map(|j| p[4 * i + j][0].clone()).sum()])
                    .collect();
                let expected = mul(&t, &marginal);
                for i in 0..4 {
                    assert_eq!(
                        (0..4).map(|j| out[4 * i + j][0].clone()).sum::<Q>(),
                        expected[i][0]
                    );
                }
            }
        }
    }
}
#[test]
fn instrument_completion_and_parallel_interchange() {
    let c = verify(&raw());
    let fi = [1, 0, 3, 2];
    for entry in &c.instrument {
        let t = matrix(entry, 4, 4);
        let failure: Mat = (0..4)
            .map(|_| {
                (0..4)
                    .map(|x| (q(1) - t.iter().map(|r| r[x].clone()).sum::<Q>()) / q(4))
                    .collect()
            })
            .collect();
        event(&failure, &fi, &fi, false);
        let total: Mat = (0..4)
            .map(|y| (0..4).map(|x| &t[y][x] + &failure[y][x]).collect())
            .collect();
        event(&total, &fi, &fi, true);
    }
    let t = matrix(&c.channels["visible_flip"], 4, 4);
    let s = matrix(&c.channels["noise"], 4, 4);
    let u = matrix(&c.channels["flag_flip"], 4, 4);
    assert_eq!(
        tensor(&mul(&t, &s), &mul(&u, &t)),
        mul(&tensor(&t, &u), &tensor(&s, &t))
    );
    assert_eq!(tensor(&tensor(&t, &s), &u), tensor(&t, &tensor(&s, &u)));
}
#[test]
fn strict_scope_types_and_duplicate_fields() {
    let valid = raw();
    let base: serde_json::Value = serde_json::from_slice(&valid).unwrap();
    let mut cases = Vec::new();
    let mut c = base.clone();
    c["premises"] = serde_json::json!([]);
    cases.push(c);
    let mut c = base.clone();
    c["claim"] = serde_json::json!("unconditional tomography");
    cases.push(c);
    let mut c = base.clone();
    c["systems"].as_array_mut().unwrap().pop();
    cases.push(c);
    let mut c = base.clone();
    c["systems"][1]["flip"][0] = serde_json::json!(true);
    cases.push(c);
    let mut c = base.clone();
    c["systems"][1]["points"] = serde_json::json!(4.0);
    cases.push(c);
    let mut c = base.clone();
    c["instrument"].as_array_mut().unwrap().pop();
    cases.push(c);
    let mut c = base.clone();
    c["hidden_states"]["rho"][0] = serde_json::json!("1");
    cases.push(c);
    for c in cases {
        let data = serde_json::to_vec(&c).unwrap();
        assert!(std::panic::catch_unwind(|| verify(&data)).is_err());
    }
    let raw = String::from_utf8(valid).unwrap();
    for (key, value) in [
        ("schema", "\"wrong\""),
        ("atoms", "99"),
        ("rho", "[]"),
        ("identity", "[]"),
    ] {
        let data = raw.replacen(
            &format!("\"{key}\":"),
            &format!("\"{key}\":{value},\"{key}\":"),
            1,
        );
        assert!(std::panic::catch_unwind(|| verify(data.as_bytes())).is_err());
    }
}
