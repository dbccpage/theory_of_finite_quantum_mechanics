//! Exact reset controls using orthogonal Gram witnesses, not Gaussian rank.
//! This tests finite rational fixtures, not physical admission or primitive QM.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::{One, Zero};
use serde_json::Value;
type Mat = Vec<Vec<Q>>;
fn q(x: i64) -> Q {
    Q::from_integer(BigInt::from(x))
}
fn parse(v: &Value, rows: usize, cols: usize) -> Mat {
    let a = v.as_array().expect("matrix array");
    assert_eq!(a.len(), rows);
    a.iter()
        .map(|r| {
            let row = r.as_array().expect("row array");
            assert_eq!(row.len(), cols);
            row.iter()
                .map(|x| {
                    let s = x.as_str().expect("rational string");
                    let r = s.parse::<Q>().expect("rational");
                    assert_eq!(r.to_string(), s);
                    r
                })
                .collect()
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
fn eye(n: usize) -> Mat {
    (0..n)
        .map(|i| (0..n).map(|j| q(i64::from(i == j))).collect())
        .collect()
}
fn candidate() -> Value {
    let path=std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(
      "../../../../dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T185210Z_filter_family/candidate.json");
    serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap()
}
fn orthogonal_nonzero(vectors: &[Vec<Q>]) {
    assert!(!vectors.is_empty());
    let n = vectors[0].len();
    assert!(n > 0 && vectors.iter().all(|r| r.len() == n));
    for i in 0..vectors.len() {
        for j in 0..vectors.len() {
            let dot: Q = (0..n).map(|k| &vectors[i][k] * &vectors[j][k]).sum();
            if i == j {
                assert!(dot > q(0));
            } else {
                assert!(dot.is_zero());
            }
        }
    }
}
fn check(c: &Value) {
    assert_eq!(c["schema"], "operational-filter-family.v1");
    assert_eq!(c["authority_effect"], "None");
    assert_eq!(c["models"].as_object().unwrap().len(), 4);
    for (name, n, np, ne, descends) in [
        ("classical_product", 4, 4, 4, true),
        ("doubled_visible", 8, 4, 4, true),
        ("doubled_all_preparations", 8, 8, 4, true),
        ("doubled_global_tests", 8, 8, 8, false),
    ] {
        let v = &c["models"][name];
        assert_eq!(v["state_dimension"].as_u64(), Some(n as u64));
        assert_eq!(v["local_frame_sizes"], serde_json::json!([2, 2]));
        let m = parse(&v["observe"], 4, n);
        let r = parse(&v["prepare"], n, 4);
        let p = parse(&v["preparations"], n, np);
        let e = parse(&v["effects"], ne, n);
        for i in 0..4 {
            for j in 0..n {
                assert_eq!(m[i][j], q(i64::from(i == j % 4)));
            }
        }
        for i in 0..n {
            for j in 0..4 {
                assert_eq!(r[i][j], q(i64::from(i % 4 == j)) / q((n / 4) as i64));
            }
        }
        assert_eq!(mul(&m, &r), eye(4));
        assert_eq!(p, if np == 4 { r.clone() } else { eye(n) });
        assert_eq!(e, if ne == 4 { m.clone() } else { eye(n) });
        let cols: Vec<Vec<Q>> = (0..np)
            .map(|j| (0..n).map(|i| p[i][j].clone()).collect())
            .collect();
        orthogonal_nonzero(&cols);
        orthogonal_nonzero(&e);
        assert!(cols
            .iter()
            .all(|v| v.iter().all(|x| x >= &q(0)) && v.iter().cloned().sum::<Q>().is_one()));
        assert!(e.iter().flatten().all(|x| x >= &q(0) && x <= &q(1)));
        let fs = v["filters"].as_array().unwrap();
        let ls = v["coordinate_filters"].as_array().unwrap();
        assert_eq!(fs.len(), np * ne);
        assert_eq!(ls.len(), np * ne);
        let mut flattened = Vec::new();
        let mut all_descend = true;
        let mut exposes_hidden = false;
        for a in 0..np {
            for b in 0..ne {
                let t = parse(&fs[a * ne + b], n, n);
                let l = parse(&ls[a * ne + b], 4, 4);
                for i in 0..n {
                    for j in 0..n {
                        assert_eq!(t[i][j], &p[i][a] * &e[b][j]);
                    }
                }
                assert_eq!(l, mul(&mul(&m, &t), &r));
                all_descend &= mul(&m, &t) == mul(&l, &m);
                for j in 0..n {
                    assert!(t.iter().map(|row| row[j].clone()).sum::<Q>() <= q(1));
                }
                assert!(t.iter().flatten().all(|x| x >= &q(0)));
                if n == 8 {
                    let h: Mat = (0..n)
                        .map(|i| vec![q(i64::from(i == 0) - i64::from(i == 4))])
                        .collect();
                    assert!(mul(&m, &h).iter().flatten().all(Q::is_zero));
                    let th = mul(&t, &h);
                    if descends {
                        assert!(th.iter().flatten().all(Q::is_zero));
                    }
                    exposes_hidden |= mul(&m, &th).iter().flatten().any(|x| !x.is_zero());
                }
                flattened.push(t.into_iter().flatten().collect());
            }
        }
        // Nonzero orthogonal reset operators are independent. Exactly n^2 of
        // them span End(Q^n); shorter families have an explicit hidden kernel.
        orthogonal_nonzero(&flattened);
        assert_eq!(
            flattened.len() == n * n,
            name == "classical_product" || name == "doubled_global_tests"
        );
        assert_eq!(all_descend, descends);
        if n == 8 {
            assert_eq!(exposes_hidden, !descends);
        }
        assert_eq!(e == mul(&mul(&e, &r), &m), descends);
    }
}
#[test]
fn exact_reset_construction_and_orthogonal_rank_witnesses() {
    check(&candidate());
}
#[test]
fn missing_extra_and_corrupted_filters_are_rejected() {
    for key in ["filters", "coordinate_filters"] {
        for mode in 0..4 {
            let mut c = candidate();
            let a = c["models"]["classical_product"][key]
                .as_array_mut()
                .unwrap();
            match mode {
                0 => a.clear(),
                1 => {
                    a.pop();
                }
                2 => a.push(a[0].clone()),
                _ => a[0][0][0] = Value::String("2".into()),
            }
            assert!(std::panic::catch_unwind(|| check(&c)).is_err());
        }
    }
}
#[test]
fn visible_output_and_coarse_graining_bound_are_essential() {
    let m = vec![vec![q(1), q(1)]];
    let e = vec![vec![q(1), q(0)]];
    let r = vec![vec![q(1) / q(2)], vec![q(1) / q(2)]];
    assert_ne!(e, mul(&mul(&e, &r), &m));
    let zero = vec![vec![q(0)], vec![q(0)]];
    assert!(mul(&m, &mul(&zero, &e)).iter().flatten().all(Q::is_zero));
    let p = vec![vec![q(1)], vec![q(0)]];
    let t = mul(&p, &e);
    assert_ne!(mul(&m, &t), mul(&mul(&mul(&m, &t), &r), &m));
    let twice: Mat = t
        .iter()
        .map(|row| row.iter().map(|x| x * q(2)).collect())
        .collect();
    assert_eq!(twice.iter().map(|row| row[0].clone()).sum::<Q>(), q(2));
}
