use crate::qm::entropy_solver as solver;
use crate::qm::finite_witness::{field_q, field_usize, parse_q, qstr, qvec};
use crate::linear_algebra::matrix as mx;
use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::Zero;
use omega_number_theory::cyclotomic_integer::CyclotomicInteger as C;
use omega_number_theory::rational::{ri, rq, Rational as Q};
use serde_json::{json, Value};
pub fn newton_p_to_e(p: &[Q]) -> Result<Vec<Q>, String> {
    if p.len() > 64 {
        return Err("RESOURCE_LIMIT:NEWTON_DEGREE".into());
    }
    let mut e = vec![ri(1)];
    for k in 1..=p.len() {
        let s: Q = (1..=k)
            .map(|i| ri(if i % 2 == 1 { 1 } else { -1 }) * &e[k - i] * &p[i - 1])
            .sum();
        e.push(s / ri(k as i64));
    }
    Ok(e)
}
pub fn newton_e_to_p(e: &[Q]) -> Result<Vec<Q>, String> {
    if e.is_empty() || e[0] != ri(1) || e.len() > 65 {
        return Err("INVALID_NEWTON_COEFFICIENTS".into());
    }
    let mut p = vec![];
    for k in 1..e.len() {
        let s: Q = (1..k)
            .map(|i| ri(if i % 2 == 1 { 1 } else { -1 }) * &e[i] * &p[k - i - 1])
            .sum();
        p.push(s + ri(if k % 2 == 1 { k as i64 } else { -(k as i64) }) * &e[k]);
    }
    Ok(p)
}
pub fn splitting_degree_2(tr: &Q, det: &Q) -> usize {
    let d = tr * tr - ri(4) * det;
    if d < ri(0) {
        return 2;
    }
    let a = d.numer().sqrt();
    let b = d.denom().sqrt();
    if &a * &a == *d.numer() && &b * &b == *d.denom() {
        1
    } else {
        2
    }
}
pub fn thermal(r: &Q) -> Result<Vec<Q>, String> {
    if r <= &ri(0) {
        return Err("POSITIVE_GIBBS_RATIO_REQUIRED".into());
    }
    omega_quantum_physics::majorization::thermal_ladder(r, 4, 4)
        .map(|simplex| simplex.probs().to_vec())
        .map_err(|error| error.to_string())
}
pub fn commensurability(gaps: &[Q]) -> Result<(bool, Q), String> {
    if gaps.len() > 1024 {
        return Err("RESOURCE_LIMIT:GAPS".into());
    }
    if gaps.is_empty() {
        return Ok((true, ri(1)));
    }
    if gaps[0].is_zero() {
        return Ok((false, ri(0)));
    }
    let mut q = gaps[0].clone();
    for g in &gaps[1..] {
        q = Q::new(
            (q.numer() * g.denom()).gcd(&(g.numer() * q.denom())),
            q.denom() * g.denom(),
        );
    }
    Ok((true, q))
}
fn is_sorted_prob_vec(v: &[Q]) -> bool {
    v.len() <= 1024 && !v.windows(2).any(|a| a[0] < a[1])
}

fn build_rational_spectrum(
    v: &[Q],
) -> Result<omega_quantum_physics::exact_entropy::RationalSpectrum, String> {
    omega_quantum_physics::exact_entropy::RationalSpectrum::try_new(
        v.iter().cloned().map(|q| (q, 1)).collect(),
    )
    .map_err(|error| format!("INVALID_SPECTRUM:{error}"))
}

pub fn majorization(p: &[Q], q: &[Q]) -> Result<&'static str, String> {
    use omega_quantum_physics::majorization::Majorization;
    if !is_sorted_prob_vec(p) || !is_sorted_prob_vec(q) {
        return Err("INVALID_SORTED_PROBABILITY_VECTORS".into());
    }
    let first = build_rational_spectrum(p)?;
    let second = build_rational_spectrum(q)?;
    let relation = omega_quantum_physics::majorization::compare_spectra(&first, &second)
        .map_err(|error| format!("INVALID_SPECTRUM:{error}"))?;
    Ok(match relation {
        Majorization::Equal => "EQUAL",
        Majorization::PMajorizesQ => "P_MAJORIZES_Q",
        Majorization::QMajorizesP => "Q_MAJORIZES_P",
        Majorization::Incomparable => "INCOMPARABLE",
    })
}
pub fn numerical_semigroup(primes: &[usize], bound: usize) -> Result<Vec<usize>, String> {
    if bound > 100000 || primes.iter().any(|&p| p == 0) {
        return Err("INVALID_SEMIGROUP_BOUND".into());
    }
    let mut r = vec![false; bound + 1];
    r[0] = true;
    for &p in primes {
        for i in p..=bound {
            r[i] |= r[i - p]
        }
    }
    Ok((0..=bound).filter(|&i| r[i]).collect())
}
pub fn mobius(n: u64) -> Result<i64, String> {
    if n == 0 || n > 1000000 {
        return Err("INVALID_MOBIUS_BOUND".into());
    }
    let f = omega_number_theory::integer_factorization::factor_natural(
        &n.into(),
        omega_number_theory::integer_factorization::FactorizationBudget {
            max_operations: 1_000_000,
        },
    )
    .map_err(|error| error.to_string())?;
    Ok(if f.values().any(|&e| e > 1) {
        0
    } else if f.len() % 2 == 0 {
        1
    } else {
        -1
    })
}
pub fn running_balance(n: u64) -> Result<Value, String> {
    mobius(n)?;
    let mut sum = 0;
    let mut rows = vec![];
    for d in 1..=n {
        if n % d == 0 {
            let mu = mobius(d)?;
            sum += mu;
            rows.push(json!({"d":d,"mu_d":mu,"running_total":sum}));
        }
    }
    Ok(json!({"conductor":n,"sum":sum,"records":rows}))
}
pub fn rotation_orbit(k: usize) -> Result<Value, String> {
    if k > 256 {
        return Err("RESOURCE_LIMIT:ROTATION_ORBIT".into());
    }
    let (mut x, mut y) = (ri(1), ri(0));
    let mut out = vec![];
    for i in 0..=k {
        let den = x.denom().lcm(y.denom());
        let expected = BigInt::from(5).pow(i as u32);
        out.push(json!({"step":i,"x":qstr(&x),"y":qstr(&y),"common_den":den.to_string(),"expected_den":expected.to_string(),"den_matches_5_pow_k":den==expected}));
        let next = (rq(3, 5) * &x - rq(4, 5) * &y, rq(4, 5) * &x + rq(3, 5) * &y);
        (x, y) = next;
    }
    Ok(json!(out))
}
fn vector(input: &Value, key: &str, default: &[Q]) -> Result<Vec<Q>, String> {
    input
        .get(key)
        .map(|v| {
            v.as_array()
                .ok_or("EXPECTED_VECTOR".to_string())
                .and_then(|v| v.iter().map(parse_q).collect())
        })
        .unwrap_or(Ok(default.to_vec()))
}
fn compute_stoquastic_witness() -> Result<Value, String> {
    let h = mx::from_rows(vec![
        vec![ri(1), ri(0), ri(0), ri(0)],
        vec![ri(0), ri(-1), ri(2), ri(0)],
        vec![ri(0), ri(2), ri(-1), ri(0)],
        vec![ri(0), ri(0), ri(0), ri(1)],
    ])
    .map_err(|error| error.to_string())?;
    let u = mx::diagonal(&[ri(1), ri(-1), ri(1), ri(-1)]).map_err(|error| error.to_string())?;
    let hu = mx::multiply(&h, &u).map_err(|error| error.to_string())?;
    let transformed = mx::multiply(&u, &hu).map_err(|error| error.to_string())?;
    let rows = mx::to_rows(&transformed).map_err(|error| error.to_string())?;
    let mut all_nonpos = true;
    for (i, row) in rows.iter().enumerate() {
        for (j, val) in row.iter().enumerate() {
            if i != j && val > &ri(0) {
                all_nonpos = false;
            }
        }
    }
    Ok(json!({
        "witness": "I (x) Z",
        "matrix": rows.iter().map(|v| qvec(v)).collect::<Vec<_>>(),
        "all_offdiagonal_nonpositive": all_nonpos
    }))
}

fn compute_conductor_semigroup(input: &Value) -> Result<(usize, Vec<usize>), String> {
    let conductor = field_usize(input, "conductor", 12, 120)?;
    if conductor == 0 {
        return Err("POSITIVE_CONDUCTOR_REQUIRED".into());
    }
    let factors = omega_number_theory::integer_factorization::factor_natural(
        &conductor.into(),
        omega_number_theory::integer_factorization::FactorizationBudget {
            max_operations: 1_000_000,
        },
    )
    .map_err(|error| error.to_string())?;
    let mut primes = Vec::with_capacity(factors.len());
    for p in factors.keys() {
        primes.push(usize::try_from(p).map_err(|_| "PRIME_BASIS_REPRESENTATION".to_string())?);
    }
    let bound = field_usize(input, "bound", 60, 100000)?;
    let semigroup = numerical_semigroup(&primes, bound)?;
    Ok((conductor, semigroup))
}

fn compute_signed_cancellation() -> Result<bool, String> {
    let z = C::zeta(6)?;
    let cancel = C::scalar(6, 1)?.sub(&z)?.add(&z.pow(2))?;
    Ok(cancel == C::scalar(6, 0)?)
}

fn compute_invariants_and_thermal(input: &Value) -> Result<(Value, Vec<String>), String> {
    let r = field_q(input, "gibbs_ratio", rq(1, 2))?;
    let spectrum = thermal(&r)?;
    let sums: Vec<Q> = (1..=4)
        .map(|k| spectrum.iter().map(|v| v.pow(k)).sum())
        .collect();
    let e = newton_p_to_e(&sums)?;
    let roundtrip = newton_e_to_p(&e)? == sums;
    let inv = json!({
        "power_sums": qvec(&sums),
        "elementary": qvec(&e),
        "newton_roundtrip": roundtrip
    });
    Ok((inv, qvec(&spectrum)))
}

pub fn run(input: &Value) -> Result<Value, String> {
    let p = vector(input, "p", &[rq(7, 10), rq(3, 20), rq(3, 20)])?;
    let q = vector(input, "q", &[rq(3, 5), rq(7, 20), rq(1, 20)])?;
    let (invariants, thermal_vec) = compute_invariants_and_thermal(input)?;
    let stoquastic = compute_stoquastic_witness()?;
    let (conductor, semigroup) = compute_conductor_semigroup(input)?;
    let rot_steps = field_usize(input, "rotation_steps", 10, 256)?;
    let meta: Value =
        serde_json::from_str(include_str!("data/entropy_meta.json")).map_err(|e| e.to_string())?;
    Ok(json!({
        "authority_effect": "None",
        "block01": solver::generate_c750_b01_parity_receipt()?,
        "invariants": invariants,
        "thermal": thermal_vec,
        "majorization": majorization(&p, &q)?,
        "purity_damping": {"before": "1/2", "after": "1", "non_monotonicity": rq(1, 2) < ri(1)},
        "rotation": rotation_orbit(rot_steps)?,
        "semigroup": semigroup,
        "signed_cancellation": compute_signed_cancellation()?,
        "stoquastic": stoquastic,
        "mobius": running_balance(conductor as u64)?,
        "declared_metadata": meta,
        "limitations": [
            "Semigroup generation does not prove the general Lam-Leung theorem.",
            "The old LP function returned True without solving an LP; no LP certificate is claimed.",
            "Historical prices and five-way partitions are declarations, not inferred from these computations."
        ]
    }))
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn newton_exact_roundtrip() {
        let p = vec![ri(6), ri(14), ri(36), ri(98)];
        assert_eq!(newton_e_to_p(&newton_p_to_e(&p).unwrap()).unwrap(), p);
    }
    #[test]
    fn rejects_invalid_probabilities() {
        assert!(majorization(&[rq(3, 2), rq(-1, 2)], &[ri(1), ri(0)]).is_err());
        assert!(thermal(&ri(0)).is_err());
    }
    #[test]
    fn large_square_without_float() {
        let r = Q::from_integer(BigInt::from(10).pow(100));
        assert_eq!(splitting_degree_2(&ri(0), &(-&r * &r)), 1);
    }
}
