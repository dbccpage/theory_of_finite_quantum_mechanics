//! Exact finite census and product spans. AuthorityEffect: None.
//! Classification, independence and tomography are supplied premises.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::{One, Zero};

type Scalar = [Q; 4];
type Mat = Vec<Vec<Scalar>>;
fn q(n: i64) -> Q {
    Q::from_integer(BigInt::from(n))
}
fn scalar(n: i64) -> Scalar {
    [q(n), q(0), q(0), q(0)]
}
fn unit(k: usize) -> Scalar {
    let mut a = scalar(0);
    a[k] = q(1);
    a
}
fn add(a: &Scalar, b: &Scalar) -> Scalar {
    std::array::from_fn(|k| &a[k] + &b[k])
}
fn scale(a: &Scalar, s: &Q) -> Scalar {
    std::array::from_fn(|k| &a[k] * s)
}
fn conj(a: &Scalar) -> Scalar {
    std::array::from_fn(|k| if k == 0 { a[k].clone() } else { -&a[k] })
}
fn mul(a: &Scalar, b: &Scalar) -> Scalar {
    let [w, x, y, z] = a;
    let [t, u, v, r] = b;
    [
        w * t - x * u - y * v - z * r,
        w * u + x * t + y * r - z * v,
        w * v - x * r + y * t + z * u,
        w * r + x * v - y * u + z * t,
    ]
}
fn zero(n: usize) -> Mat {
    vec![vec![scalar(0); n]; n]
}
fn basis(n: usize, d: usize) -> Vec<Mat> {
    assert!([1, 2, 4].contains(&d));
    let mut out = Vec::new();
    for i in 0..n {
        let mut a = zero(n);
        a[i][i] = scalar(1);
        out.push(a);
    }
    for i in 0..n {
        for j in i + 1..n {
            for k in 0..d {
                let mut a = zero(n);
                a[i][j] = unit(k);
                a[j][i] = conj(&unit(k));
                out.push(a);
            }
        }
    }
    out
}
fn kron(a: &Mat, b: &Mat) -> Mat {
    let n = a.len();
    let m = b.len();
    let mut c = zero(n * m);
    for i in 0..n {
        for j in 0..n {
            for k in 0..m {
                for l in 0..m {
                    c[i * m + k][j * m + l] = mul(&a[i][j], &b[k][l]);
                }
            }
        }
    }
    c
}
fn adjoint(a: &Mat) -> Mat {
    (0..a.len())
        .map(|i| (0..a.len()).map(|j| conj(&a[j][i])).collect())
        .collect()
}
fn project(a: &Mat) -> Mat {
    let h = adjoint(a);
    let half = Q::new(1.into(), 2.into());
    a.iter()
        .zip(h.iter())
        .map(|(r, s)| {
            r.iter()
                .zip(s.iter())
                .map(|(x, y)| scale(&add(x, y), &half))
                .collect()
        })
        .collect()
}
fn flatten(a: &Mat) -> Vec<Q> {
    a.iter().flatten().flat_map(|x| x.iter().cloned()).collect()
}
fn rank(mut a: Vec<Vec<Q>>) -> usize {
    if a.is_empty() {
        return 0;
    }
    let mut r = 0;
    for c in 0..a[0].len() {
        if let Some(p) = (r..a.len()).find(|&i| !a[i][c].is_zero()) {
            a.swap(r, p);
            let pivot = a[r][c].clone();
            for x in &mut a[r] {
                *x /= &pivot;
            }
            let row = a[r].clone();
            for (i, target) in a.iter_mut().enumerate() {
                if i != r {
                    let factor = target[c].clone();
                    for (x, y) in target.iter_mut().zip(&row) {
                        *x -= &factor * y;
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
/// Exact dimension, unbounded integer output. d=0 is deliberately retained.
pub fn dimension(d: u32, n: u32) -> BigInt {
    let n = BigInt::from(n);
    &n + BigInt::from(d) * &n * (&n - 1) / 2
}
#[derive(Debug, PartialEq, Eq)]
pub struct SpanReport {
    pub local: usize,
    pub joint: usize,
    pub raw_rank: usize,
    pub projected_rank: usize,
    pub nonhermitian: usize,
}
/// Raw quaternionic products live in all matrices, not in Herm_4(H).
pub fn span_report(d: usize) -> SpanReport {
    let b = basis(2, d);
    let products: Vec<_> = b
        .iter()
        .flat_map(|a| b.iter().map(move |c| kron(a, c)))
        .collect();
    SpanReport {
        local: b.len(),
        joint: basis(4, d).len(),
        raw_rank: rank(products.iter().map(flatten).collect()),
        projected_rank: rank(products.iter().map(|a| flatten(&project(a))).collect()),
        nonhermitian: products.iter().filter(|a| **a != adjoint(a)).count(),
    }
}
fn trace_pair(a: &Mat, b: &Mat) -> Scalar {
    let mut s = scalar(0);
    for i in 0..a.len() {
        for j in 0..a.len() {
            s = add(&s, &mul(&a[i][j], &b[j][i]));
        }
    }
    s
}
fn witness() -> (Mat, Mat, Mat) {
    let y = vec![vec![scalar(0), scalar(-1)], vec![scalar(1), scalar(0)]];
    let delta = kron(&y, &y);
    let mut plus = zero(4);
    let mut minus = zero(4);
    let quarter = Q::new(1.into(), 4.into());
    for i in 0..4 {
        for j in 0..4 {
            let id = scalar(i64::from(i == j));
            plus[i][j] = scale(&add(&id, &delta[i][j]), &quarter);
            minus[i][j] = scale(&add(&id, &scale(&delta[i][j], &q(-1))), &quarter);
        }
    }
    (delta, plus, minus)
}
fn determinant(a: &[Vec<Q>]) -> Q {
    if a.is_empty() {
        return Q::one();
    }
    (0..a.len())
        .map(|j| {
            let minor: Vec<_> = a[1..]
                .iter()
                .map(|r| {
                    r.iter()
                        .enumerate()
                        .filter(|(k, _)| *k != j)
                        .map(|(_, x)| x.clone())
                        .collect()
                })
                .collect();
            q(if j % 2 == 0 { 1 } else { -1 }) * &a[0][j] * determinant(&minor)
        })
        .sum()
}
/// All principal minors are nonnegative: exact rational PSD certificate.
fn psd(a: &Mat) -> bool {
    a == &adjoint(a)
        && (1..(1usize << a.len())).all(|mask| {
            let ids: Vec<_> = (0..a.len()).filter(|i| mask >> i & 1 == 1).collect();
            let minor: Vec<_> = ids
                .iter()
                .map(|&i| ids.iter().map(|&j| a[i][j][0].clone()).collect())
                .collect();
            determinant(&minor) >= q(0)
        })
}
#[cfg(test)]
mod complex_selection_tests {
    use super::*;
    #[test]
    fn dimension_census() {
        for d in [1, 2, 4] {
            for n in 1..=6 {
                for m in 1..=6 {
                    let equal = dimension(d, n * m) == dimension(d, n) * dimension(d, m);
                    assert_eq!(equal, d == 2 || n == 1 || m == 1);
                }
            }
        }
        assert_eq!(dimension(1, 4), 10.into());
        assert_eq!(dimension(4, 4), 28.into());
    }
    #[test]
    fn unrestricted_zero_control_and_polynomial() {
        for d in 0..=7 {
            for n in 1..=6 {
                for m in 1..=6 {
                    let defect = dimension(d, n * m) - dimension(d, n) * dimension(d, m);
                    let rhs = BigInt::from(d) * (BigInt::from(2) - d) * n * m * (n - 1) * (m - 1);
                    assert_eq!(4 * defect, rhs);
                }
            }
        }
    }
    #[test]
    fn exact_product_spans() {
        for (d, local, joint, raw, projected, bad) in [
            (1, 3, 10, 9, 9, 0),
            (2, 4, 16, 16, 16, 0),
            (4, 6, 28, 31, 28, 6),
        ] {
            assert_eq!(
                span_report(d),
                SpanReport {
                    local,
                    joint,
                    raw_rank: raw,
                    projected_rank: projected,
                    nonhermitian: bad
                }
            );
        }
    }
    #[test]
    fn real_states_and_all_basis_tests() {
        let (delta, p, m) = witness();
        assert_ne!(p, m);
        assert_eq!(delta, adjoint(&delta));
        for state in [&p, &m] {
            assert!(psd(state));
            assert_eq!((0..4).map(|i| &state[i][i][0]).sum::<Q>(), q(1));
        }
        for a in basis(2, 1) {
            for b in basis(2, 1) {
                let product = kron(&a, &b);
                assert_eq!(trace_pair(&delta, &product), scalar(0));
                assert_eq!(trace_pair(&p, &product), trace_pair(&m, &product));
            }
        }
        assert_eq!(trace_pair(&delta, &p), scalar(1));
        assert_eq!(trace_pair(&delta, &m), scalar(-1));
    }
    #[test]
    fn quaternion_codomain_and_projected_kernel() {
        assert_eq!(mul(&unit(1), &unit(2)), unit(3));
        assert_eq!(mul(&unit(2), &unit(1)), scale(&unit(3), &q(-1)));
        let b = basis(2, 4);
        let product = kron(&b[3], &b[4]);
        assert_ne!(product, adjoint(&product));
        assert_eq!(project(&product), zero(4));
        // The domain basis tensor is nonzero but its projected image is zero.
        assert_eq!(
            span_report(4).local.pow(2) - span_report(4).projected_rank,
            8
        );
    }
    #[test]
    fn witness_mutations_are_detected() {
        let (delta, p, m) = witness();
        for i in 0..4 {
            for j in 0..4 {
                let mut bad = delta.clone();
                bad[i][j][0] += q(1);
                let passes = bad == adjoint(&bad)
                    && basis(2, 1).iter().all(|a| {
                        basis(2, 1)
                            .iter()
                            .all(|b| trace_pair(&bad, &kron(a, b)) == scalar(0))
                    });
                assert!(!passes);
            }
        }
        assert_ne!(trace_pair(&p, &delta), trace_pair(&m, &delta));
    }
}
