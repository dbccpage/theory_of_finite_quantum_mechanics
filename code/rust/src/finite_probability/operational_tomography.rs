//! Independent exact replay of the same candidate matrices. AuthorityEffect: None.
//! These finite tests do not establish the general Lean theorem or availability.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::{One, Zero};
use serde_json::Value;
type Mat = Vec<Vec<Q>>;
fn q(n: i64) -> Q {
    Q::from_integer(BigInt::from(n))
}
fn eye(n: usize) -> Mat {
    (0..n)
        .map(|i| (0..n).map(|j| if i == j { q(1) } else { q(0) }).collect())
        .collect()
}
fn mul(a: &Mat, b: &Mat) -> Mat {
    assert_eq!(a[0].len(), b.len());
    (0..a.len())
        .map(|i| {
            (0..b[0].len())
                .map(|j| (0..b.len()).map(|k| &a[i][k] * &b[k][j]).sum())
                .collect()
        })
        .collect()
}
fn sub(a: &Mat, b: &Mat) -> Mat {
    a.iter()
        .zip(b)
        .map(|(r, s)| r.iter().zip(s).map(|(x, y)| x - y).collect())
        .collect()
}
fn rank(input: &Mat) -> usize {
    // Reduced echelon elimination, independent of Python's forward elimination.
    let mut a = input.clone();
    let mut r = 0;
    for c in 0..a[0].len() {
        if let Some(p) = (r..a.len()).find(|&i| !a[i][c].is_zero()) {
            a.swap(r, p);
            let pivot = a[r][c].clone();
            for x in &mut a[r] {
                *x /= &pivot;
            }
            let row = a[r].clone();
            for (i, other) in a.iter_mut().enumerate() {
                if i != r {
                    let f = other[c].clone();
                    for (x, y) in other.iter_mut().zip(&row) {
                        *x -= &f * y;
                    }
                }
            }
            r += 1;
            if r == a.len() {
                break;
            }
        }
    }
    r
}
fn parse(v: &Value) -> Mat {
    v.as_array()
        .unwrap()
        .iter()
        .map(|row| {
            row.as_array()
                .unwrap()
                .iter()
                .map(|v| {
                    let s = v.as_str().unwrap();
                    let x = s.parse::<Q>().unwrap();
                    assert_eq!(x.to_string(), s);
                    x
                })
                .collect()
        })
        .collect()
}
fn candidate() -> Value {
    let path=std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(
        "../../../../dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography/p1/candidate.json");
    serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap()
}
fn ops(e: &Value, key: &str) -> Vec<Mat> {
    e[key].as_array().unwrap().iter().map(parse).collect()
}
#[test]
fn exact_ranks_and_descent() {
    let c = candidate();
    for (name, n, defect, span, descent) in [
        ("product_filters", 4, 0, 16, true),
        ("doubled_filters", 8, 4, 16, true),
        ("tomographic_identity", 4, 0, 1, true),
        ("irreducible_without_descent", 8, 4, 64, false),
    ] {
        let e = &c["examples"][name];
        let m = parse(&e["observe"]);
        let r = parse(&e["prepare"]);
        assert_eq!(mul(&m, &r), eye(4));
        assert_eq!(n - rank(&m), defect);
        let ts = ops(e, "operations");
        let ls = ops(e, "coordinate_operations");
        let flat = ts
            .iter()
            .map(|t| t.iter().flatten().cloned().collect())
            .collect();
        assert_eq!(rank(&flat), span);
        assert_eq!(
            ts.iter().zip(&ls).all(|(t, l)| mul(&m, t) == mul(l, &m)),
            descent
        );
        let h = sub(&eye(n), &mul(&r, &m));
        assert_eq!(mul(&h, &h), h);
        assert!(mul(&m, &h).iter().flatten().all(Q::is_zero));
        assert_eq!(rank(&h), defect);
    }
}
#[test]
fn doubled_normalized_states_and_protected_question() {
    let c = candidate();
    let e = &c["examples"]["doubled_filters"];
    let m = parse(&e["observe"]);
    let x: Mat = (0..8)
        .map(|i| vec![q(if i == 0 { 1 } else { 0 })])
        .collect();
    let y: Mat = (0..8)
        .map(|i| vec![q(if i == 4 { 1 } else { 0 })])
        .collect();
    assert_eq!(mul(&m, &x), mul(&m, &y));
    assert_ne!(x, y);
    assert_eq!(x.iter().map(|r| r[0].clone()).sum::<Q>(), q(1));
    assert_eq!(y.iter().map(|r| r[0].clone()).sum::<Q>(), q(1));
    assert_eq!(x[..4].iter().map(|r| r[0].clone()).sum::<Q>(), q(1));
    assert_eq!(y[..4].iter().map(|r| r[0].clone()).sum::<Q>(), q(0));
    let h = sub(&x, &y);
    for t in ops(e, "operations") {
        assert!(mul(&m, &mul(&t, &h)).iter().flatten().all(Q::is_zero));
    }
    let all = ops(&c["examples"]["irreducible_without_descent"], "operations");
    assert!(all
        .iter()
        .any(|t| mul(&m, &mul(t, &h)).iter().flatten().any(|x| !x.is_zero())));
}
#[test]
fn filters_positive_and_subnormalized_but_not_all_trace_preserving() {
    let c = candidate();
    for (name, e) in c["examples"].as_object().unwrap() {
        let ts = ops(e, "operations");
        let mut all_preserve = true;
        for t in ts {
            assert!(t.iter().flatten().all(|x| x >= &q(0)));
            for j in 0..t.len() {
                let sum: Q = t.iter().map(|r| r[j].clone()).sum();
                assert!(sum <= q(1));
                all_preserve &= sum.is_one();
            }
        }
        assert_eq!(all_preserve, name == "tomographic_identity");
    }
}
#[test]
fn product_filters_are_actual_local_tensor_products() {
    let c = candidate();
    let e = &c["examples"]["product_filters"];
    for (index, t) in ops(e, "operations").iter().enumerate() {
        let a = index / 4;
        let b = index % 4;
        for i in 0..4 {
            for j in 0..4 {
                // Product of two binary matrix units: E_(a0,b0) tensor E_(a1,b1).
                let expected =
                    if i / 2 == a / 2 && j / 2 == b / 2 && i % 2 == a % 2 && j % 2 == b % 2 {
                        1
                    } else {
                        0
                    };
                assert_eq!(t[i][j], q(expected));
            }
        }
    }
}
#[test]
fn zero_observation_shows_nonzero_premise_is_needed() {
    let z = vec![vec![q(0); 2]];
    assert_eq!(rank(&z), 0);
    let ts: Vec<Mat> = (0..4)
        .map(|k| {
            (0..2)
                .map(|i| {
                    (0..2)
                        .map(|j| q(if 2 * i + j == k { 1 } else { 0 }))
                        .collect()
                })
                .collect()
        })
        .collect();
    assert_eq!(
        rank(
            &ts.iter()
                .map(|t| t.iter().flatten().cloned().collect())
                .collect()
        ),
        4
    );
    for t in ts {
        assert_eq!(mul(&z, &t), z);
    }
}
