
use num_rational::BigRational;
use tfqm_number_theory::cyclotomic::Cyc24;
use tfqm_number_theory::rational::ri;

pub const D: usize = 6;
pub const BASIS_COUNT: usize = 3;
pub const COLUMN_COUNT: usize = 18;

pub type ExactVec = [Cyc24; D];

fn rat(num: i64, den: i64) -> Cyc24 {
    Cyc24::rat(ri(num) / ri(den))
}

pub(crate) fn inv_sqrt2() -> Cyc24 {
    Cyc24::sqrt2().mul(&rat(1, 2))
}

pub(crate) fn inv_sqrt3() -> Cyc24 {
    Cyc24::sqrt3().mul(&rat(1, 3))
}

pub(crate) fn omega3_pow(exp: i64) -> Cyc24 {
    crate::native::exact::mub6_field::omega3_pow(exp)
}

pub(crate) fn zero_vec() -> ExactVec {
    std::array::from_fn(|_| Cyc24::zero())
}

pub(crate) fn tensor(qb: &[Cyc24; 2], qt: &[Cyc24; 3]) -> ExactVec {
    let mut out = zero_vec();
    for (a, qa) in qb.iter().enumerate() {
        for (b, qbt) in qt.iter().enumerate() {
            out[a * 3 + b] = qa.mul(qbt);
        }
    }
    out
}

pub(crate) fn qubit_x() -> [[Cyc24; 2]; 2] {
    let s = inv_sqrt2();
    [[s.clone(), s.clone()], [s.clone(), s.neg()]]
}

pub(crate) fn qubit_y() -> [[Cyc24; 2]; 2] {
    let s = inv_sqrt2();
    let i = Cyc24::zeta24(6);
    [[s.clone(), i.mul(&s)], [s.clone(), i.mul(&s).neg()]]
}

pub(crate) fn qutrit_q(a: i64) -> [[Cyc24; 3]; 3] {
    let s = inv_sqrt3();
    std::array::from_fn(|m| {
        std::array::from_fn(|j| {
            let exp = a * (j as i64) * (j as i64) + (m as i64) * (j as i64);
            omega3_pow(exp).mul(&s)
        })
    })
}

pub fn canonical_triple_exact() -> Vec<ExactVec> {
    let mut cols = Vec::with_capacity(COLUMN_COUNT);
    for idx in 0..D {
        let mut v = zero_vec();
        v[idx] = Cyc24::rat(ri(1));
        cols.push(v);
    }
    let x2 = qubit_x();
    let q0 = qutrit_q(0);
    for qb in &x2 {
        for qt in &q0 {
            cols.push(tensor(qb, qt));
        }
    }
    let y2 = qubit_y();
    let q1 = qutrit_q(1);
    for qb in &y2 {
        for qt in &q1 {
            cols.push(tensor(qb, qt));
        }
    }
    cols
}

pub fn inner(u: &ExactVec, v: &ExactVec) -> Cyc24 {
    let mut acc = Cyc24::zero();
    for k in 0..D {
        acc = acc.add(&u[k].conj().mul(&v[k]));
    }
    acc
}

pub fn abs_sq(z: &Cyc24) -> Cyc24 {
    tfqm_functional::MubFeasibilityWallFunctional::cyclotomic_squared_norm(std::slice::from_ref(z))
}

pub fn norm_sq(v: &ExactVec) -> Cyc24 {
    tfqm_functional::MubFeasibilityWallFunctional::cyclotomic_squared_norm(v)
}

pub fn connection_c1(columns: &[ExactVec], v: &ExactVec) -> Vec<Cyc24> {
    columns.iter().map(|e| inner(e, v)).collect()
}

pub fn curvature_c2(columns: &[ExactVec], v: &ExactVec) -> Vec<Cyc24> {
    let target = rat(1, D as i64);
    columns
        .iter()
        .map(|e| abs_sq(&inner(e, v)).sub(&target))
        .collect()
}

pub fn try_basis_closure(omega: &[Cyc24]) -> Result<[Cyc24; BASIS_COUNT], &'static str> {
    if omega.len() != COLUMN_COUNT {
        return Err("basis_closure expects the full 18-vector curvature cochain");
    }
    Ok(std::array::from_fn(|b| {
        let mut acc = Cyc24::zero();
        for j in 0..D {
            acc = acc.add(&omega[b * D + j]);
        }
        acc
    }))
}

pub fn basis_closure(omega: &[Cyc24]) -> [Cyc24; BASIS_COUNT] {
    try_basis_closure(omega).expect("basis_closure expects the full 18-vector curvature cochain")
}

pub fn try_wall_functional(omega: &[Cyc24]) -> Result<Cyc24, &'static str> {
    if omega.len() != COLUMN_COUNT {
        return Err("wall_functional expects the full 18-vector curvature cochain");
    }
    tfqm_functional::MubFeasibilityWallFunctional::exact_d6_wall(omega)
        .map_err(|_| "eighteen residuals required for exact_d6_wall")
}

pub fn wall_functional(omega: &[Cyc24]) -> Cyc24 {
    try_wall_functional(omega)
        .expect("wall_functional expects the full 18-vector curvature cochain")
}

fn column_pair_is_mu(
    columns: &[ExactVec],
    ci: usize,
    cj: usize,
    one: &Cyc24,
    zero: &Cyc24,
    target: &Cyc24,
) -> bool {
    let ip = inner(&columns[ci], &columns[cj]);
    if ci / D == cj / D {
        let want = if ci == cj { one } else { zero };
        &ip == want
    } else {
        &abs_sq(&ip) == target
    }
}

pub fn is_mutually_unbiased_triple_exact(columns: &[ExactVec]) -> bool {
    if columns.len() != COLUMN_COUNT {
        return false;
    }
    let one = Cyc24::rat(ri(1));
    let zero = Cyc24::zero();
    let target = rat(1, D as i64);
    for ci in 0..COLUMN_COUNT {
        for cj in 0..COLUMN_COUNT {
            if !column_pair_is_mu(columns, ci, cj, &one, &zero, &target) {
                return false;
            }
        }
    }
    true
}

pub fn as_rational(z: &Cyc24) -> Option<BigRational> {
    if z.a[1..].iter().all(num_traits::Zero::is_zero) {
        Some(z.a[0].clone())
    } else {
        None
    }
}

pub fn cmp_exact_real(a: &Cyc24, b: &Cyc24) -> std::cmp::Ordering {
    if a == b {
        return std::cmp::Ordering::Equal;
    }
    let diff = a.sub(b);
    let num = tfqm_number_theory::cyclotomic_field::CyclotomicNumber::from(&diff);
    match tfqm_number_theory::cyclotomic_ordered::standard_real_sign(&num) {
        Ok(1) => std::cmp::Ordering::Greater,
        Ok(-1) => std::cmp::Ordering::Less,
        Ok(0) => std::cmp::Ordering::Equal,
        _ => a.a.cmp(&b.a),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn canonical_triple_is_exactly_mutually_unbiased() {
        let cols = canonical_triple_exact();
        assert_eq!(cols.len(), COLUMN_COUNT);
        assert!(
            is_mutually_unbiased_triple_exact(&cols),
            "T0 must be an exact MU triple over Q(zeta_24)"
        );
        assert!(!is_mutually_unbiased_triple_exact(&cols[..17]));
        assert!(try_basis_closure(&[]).is_err());
        assert!(try_wall_functional(&[]).is_err());
    }

    #[test]
    fn standard_basis_vector_has_exact_zero_closure() {
        let cols = canonical_triple_exact();
        let mut v = zero_vec();
        v[0] = Cyc24::rat(ri(1));
        assert_eq!(norm_sq(&v), Cyc24::rat(ri(1)));
        let omega = curvature_c2(&cols, &v);
        let closures = basis_closure(&omega);
        for c in &closures {
            assert!(
                c.is_zero(),
                "exact Bianchi closure must vanish on a unit vector"
            );
        }
    }

    #[test]
    fn closure_equals_norm_minus_one_for_a_nonunit_vector() {
        let cols = canonical_triple_exact();
        let mut v = zero_vec();
        v[0] = Cyc24::rat(ri(2));
        let nsq = norm_sq(&v);
        assert_eq!(nsq, Cyc24::rat(ri(4)));
        let omega = curvature_c2(&cols, &v);
        let expected = nsq.sub(&Cyc24::rat(ri(1)));
        for c in &basis_closure(&omega) {
            assert_eq!(c, &expected, "closure must equal ||v||^2 - 1 exactly");
        }
    }

    #[test]
    fn curvature_at_e0_has_known_exact_values() {
        let cols = canonical_triple_exact();
        let mut v = zero_vec();
        v[0] = Cyc24::rat(ri(1));
        let omega = curvature_c2(&cols, &v);
        assert_eq!(omega[0], rat(5, 6));
        for j in 1..D {
            assert_eq!(omega[j], rat(-1, 6));
        }
        for i in D..COLUMN_COUNT {
            assert!(
                omega[i].is_zero(),
                "e_0 is exactly unbiased to bases 2 and 3"
            );
        }
    }

    #[test]
    fn wall_functional_is_one_at_a_perfectly_unbiased_vector() {
        let cols = canonical_triple_exact();
        let mut v = zero_vec();
        v[0] = Cyc24::rat(ri(1));
        let omega = curvature_c2(&cols, &v);
        let f = wall_functional(&omega);
        let fq = as_rational(&f).expect("wall value at e_0 is rational");
        assert_eq!(fq, ri(0));
    }
}
