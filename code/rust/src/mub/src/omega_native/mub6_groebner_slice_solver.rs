
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::cmp::Ordering;
use std::collections::BTreeMap;

pub const SCHEMA_VERSION: &str = "omega.mub.groebner.v1";
pub const SCOPE_STRING: &str = "mub6_i55_cylindrical_slice_groebner_exact";

pub type Monomial4 = [u32; 4];

pub fn grevlex_compare(m1: &Monomial4, m2: &Monomial4) -> Ordering {
    let deg1: u32 = m1.iter().sum();
    let deg2: u32 = m2.iter().sum();
    if deg1 != deg2 {
        return deg1.cmp(&deg2);
    }
    for (e1, e2) in m1.iter().rev().zip(m2.iter().rev()) {
        if e1 != e2 {
            return e2.cmp(e1);
        }
    }
    Ordering::Equal
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ExactPoly4 {
    pub terms: BTreeMap<Monomial4, BigRational>,
}

impl ExactPoly4 {
    pub fn zero() -> Self {
        Self {
            terms: BTreeMap::new(),
        }
    }

    pub fn constant(c: BigRational) -> Self {
        let mut terms = BTreeMap::new();
        if !c.is_zero() {
            terms.insert([0, 0, 0, 0], c);
        }
        Self { terms }
    }

    pub fn var(idx: usize) -> Self {
        assert!(idx < 4);
        let mut m = [0u32; 4];
        m[idx] = 1;
        let mut terms = BTreeMap::new();
        terms.insert(m, BigRational::one());
        Self { terms }
    }

    pub fn is_zero(&self) -> bool {
        self.terms.is_empty()
    }

    pub fn degree(&self) -> u32 {
        self.terms
            .keys()
            .map(|m| m.iter().sum::<u32>())
            .max()
            .unwrap_or(0)
    }

    pub fn leading_term(&self) -> Option<(Monomial4, BigRational)> {
        let mut best: Option<(Monomial4, BigRational)> = None;
        for (m, c) in &self.terms {
            match &best {
                None => best = Some((*m, c.clone())),
                Some((best_m, _)) => {
                    if grevlex_compare(m, best_m) == Ordering::Greater {
                        best = Some((*m, c.clone()));
                    }
                }
            }
        }
        best
    }

    pub fn add(&self, other: &Self) -> Self {
        let mut new_terms = self.terms.clone();
        for (m, c) in &other.terms {
            let entry = new_terms.entry(*m).or_insert_with(BigRational::zero);
            *entry = &*entry + c;
            if entry.is_zero() {
                new_terms.remove(m);
            }
        }
        Self { terms: new_terms }
    }

    pub fn sub(&self, other: &Self) -> Self {
        let mut new_terms = self.terms.clone();
        for (m, c) in &other.terms {
            let entry = new_terms.entry(*m).or_insert_with(BigRational::zero);
            *entry = &*entry - c;
            if entry.is_zero() {
                new_terms.remove(m);
            }
        }
        Self { terms: new_terms }
    }

    pub fn mul(&self, other: &Self) -> Self {
        let mut new_terms = BTreeMap::new();
        for (m1, c1) in &self.terms {
            for (m2, c2) in &other.terms {
                let m = [m1[0] + m2[0], m1[1] + m2[1], m1[2] + m2[2], m1[3] + m2[3]];
                let entry = new_terms.entry(m).or_insert_with(BigRational::zero);
                *entry = &*entry + (c1 * c2);
                if entry.is_zero() {
                    new_terms.remove(&m);
                }
            }
        }
        Self { terms: new_terms }
    }

    pub fn scale(&self, scalar: &BigRational) -> Self {
        if scalar.is_zero() {
            return Self::zero();
        }
        let mut new_terms = BTreeMap::new();
        for (m, c) in &self.terms {
            let val = c * scalar;
            if !val.is_zero() {
                new_terms.insert(*m, val);
            }
        }
        Self { terms: new_terms }
    }

    pub fn mul_monomial(&self, mono: &Monomial4, coeff: &BigRational) -> Self {
        if coeff.is_zero() {
            return Self::zero();
        }
        let mut new_terms = BTreeMap::new();
        for (m, c) in &self.terms {
            let new_m = [m[0] + mono[0], m[1] + mono[1], m[2] + mono[2], m[3] + mono[3]];
            let val = c * coeff;
            if !val.is_zero() {
                new_terms.insert(new_m, val);
            }
        }
        Self { terms: new_terms }
    }
}

pub fn monomial_is_divisible(m1: &Monomial4, m2: &Monomial4) -> bool {
    m1[0] >= m2[0] && m1[1] >= m2[1] && m1[2] >= m2[2] && m1[3] >= m2[3]
}

pub fn monomial_sub(m1: &Monomial4, m2: &Monomial4) -> Monomial4 {
    [m1[0] - m2[0], m1[1] - m2[1], m1[2] - m2[2], m1[3] - m2[3]]
}

pub fn monomial_lcm(m1: &Monomial4, m2: &Monomial4) -> Monomial4 {
    [
        m1[0].max(m2[0]),
        m1[1].max(m2[1]),
        m1[2].max(m2[2]),
        m1[3].max(m2[3]),
    ]
}

pub fn multivariate_remainder(f: &ExactPoly4, divisors: &[ExactPoly4]) -> ExactPoly4 {
    let mut remainder = ExactPoly4::zero();
    let mut p = f.clone();

    let divisor_lts: Vec<Option<(Monomial4, BigRational)>> =
        divisors.iter().map(|d| d.leading_term()).collect();

    while !p.is_zero() {
        let (lm_p, lc_p) = p.leading_term().unwrap();
        let mut divided = false;

        for (i, d_lt) in divisor_lts.iter().enumerate() {
            if let Some((lm_d, lc_d)) = d_lt {
                if monomial_is_divisible(&lm_p, lm_d) {
                    let m_diff = monomial_sub(&lm_p, lm_d);
                    let c_diff = &lc_p / lc_d;
                    let sub_poly = divisors[i].mul_monomial(&m_diff, &c_diff);
                    p = p.sub(&sub_poly);
                    divided = true;
                    break;
                }
            }
        }

        if !divided {
            let mut single_term = BTreeMap::new();
            single_term.insert(lm_p, lc_p.clone());
            let rem_poly = ExactPoly4 { terms: single_term };
            remainder = remainder.add(&rem_poly);
            p = p.sub(&rem_poly);
        }
    }

    remainder
}

pub fn compute_s_polynomial(f: &ExactPoly4, g: &ExactPoly4) -> ExactPoly4 {
    let (lm_f, lc_f) = f.leading_term().expect("f must be non-zero");
    let (lm_g, lc_g) = g.leading_term().expect("g must be non-zero");
    let lcm_m = monomial_lcm(&lm_f, &lm_g);

    let gamma_f = monomial_sub(&lcm_m, &lm_f);
    let c_f = BigRational::one() / lc_f;
    let term_f = f.mul_monomial(&gamma_f, &c_f);

    let gamma_g = monomial_sub(&lcm_m, &lm_g);
    let c_g = BigRational::one() / lc_g;
    let term_g = g.mul_monomial(&gamma_g, &c_g);

    term_f.sub(&term_g)
}

pub fn verify_buchberger_criterion(basis: &[ExactPoly4]) -> (bool, usize, usize) {
    let mut total_pairs = 0usize;
    let mut zero_pairs = 0usize;

    for i in 0..basis.len() {
        for j in (i + 1)..basis.len() {
            total_pairs += 1;
            let s_poly = compute_s_polynomial(&basis[i], &basis[j]);
            let rem = multivariate_remainder(&s_poly, basis);
            if rem.is_zero() {
                zero_pairs += 1;
            }
        }
    }

    let is_confluent = total_pairs > 0 && total_pairs == zero_pairs;
    (is_confluent, total_pairs, zero_pairs)
}

pub fn compute_slice_groebner_basis(generators: &[ExactPoly4]) -> Vec<ExactPoly4> {
    let mut basis: Vec<ExactPoly4> = generators.iter().filter(|g| !g.is_zero()).cloned().collect();
    let mut pairs: Vec<(usize, usize)> = Vec::new();
    for i in 0..basis.len() {
        for j in (i + 1)..basis.len() {
            pairs.push((i, j));
        }
    }

    let mut iterations = 0usize;
    while !pairs.is_empty() && iterations < 50 {
        iterations += 1;
        let (i, j) = pairs.remove(0);
        let s_poly = compute_s_polynomial(&basis[i], &basis[j]);
        let rem = multivariate_remainder(&s_poly, &basis);

        if !rem.is_zero() {
            let (_, lc) = rem.leading_term().unwrap();
            let rem_monic = rem.scale(&(BigRational::one() / lc));
            let new_idx = basis.len();
            for k in 0..new_idx {
                pairs.push((k, new_idx));
            }
            basis.push(rem_monic);
        }
    }

    basis
}

pub fn create_canonical_corner_slice() -> Vec<ExactPoly4> {
    let x1 = ExactPoly4::var(0);
    let y1 = ExactPoly4::var(1);
    let x2 = ExactPoly4::var(2);
    let y2 = ExactPoly4::var(3);
    let one = ExactPoly4::constant(BigRational::one());
    let half = ExactPoly4::constant(BigRational::new(1.into(), 2.into()));

    let g1 = x1.mul(&x1).add(&y1.mul(&y1)).sub(&one);
    let g2 = x2.mul(&x2).add(&y2.mul(&y2)).sub(&one);
    let g3 = x1.add(&x2).add(&half);

    vec![g1, g2, g3]
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct GroebnerSliceReceipt {
    pub schema_version: String,
    pub authority_effect: String,
    pub firewall: String,
    pub scope: String,
    pub target: String,
    pub status: String,
    pub arithmetic_regime: String,
    pub receipt_id: String,
    pub initial_generators: usize,
    pub basis_polynomials: usize,
    pub max_degree: u32,
    pub total_pairs_checked: usize,
    pub zero_remainders_count: usize,
    pub buchberger_confluent: bool,
    pub degree_bound_respected: bool,
    pub refusal_reason: String,
}

pub fn solve_and_certify_cylindrical_slice_groebner() -> GroebnerSliceReceipt {
    let generators = create_canonical_corner_slice();
    let basis = compute_slice_groebner_basis(&generators);
    let (confluent, total_pairs, zero_pairs) = verify_buchberger_criterion(&basis);
    let max_deg = basis.iter().map(|p| p.degree()).max().unwrap_or(0);
    let degree_ok = max_deg <= 8;

    let is_certified = confluent && degree_ok;

    let mut hasher = Sha256::new();
    hasher.update(b"MUB6_I55_CYLINDRICAL_SLICE_GROEBNER_v1");
    hasher.update(generators.len().to_string().as_bytes());
    hasher.update(basis.len().to_string().as_bytes());
    hasher.update(max_deg.to_string().as_bytes());
    hasher.update(total_pairs.to_string().as_bytes());
    let digest = format!("sha256:{:x}", hasher.finalize());

    GroebnerSliceReceipt {
        schema_version: SCHEMA_VERSION.to_string(),
        authority_effect: "None".to_string(),
        firewall: "stated region only; mints no authority".to_string(),
        scope: SCOPE_STRING.to_string(),
        target: "MUB(6) Gap G1 Approach B / I_55 Cylindrical Slices".to_string(),
        status: if is_certified { "PASS".to_string() } else { "REFUSED".to_string() },
        arithmetic_regime: "EXACT_RATIONAL_BIGRAT_NO_FLOATS".to_string(),
        receipt_id: digest,
        initial_generators: generators.len(),
        basis_polynomials: basis.len(),
        max_degree: max_deg,
        total_pairs_checked: total_pairs,
        zero_remainders_count: zero_pairs,
        buchberger_confluent: confluent,
        degree_bound_respected: degree_ok,
        refusal_reason: if is_certified {
            String::new()
        } else {
            "Buchberger criterion non-confluence or degree bound > 8".to_string()
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_exact_poly_multiplication() {
        let x = ExactPoly4::var(0);
        let y = ExactPoly4::var(1);
        let p1 = x.add(&y);
        let p2 = x.sub(&y);
        let prod = p1.mul(&p2);
        let expected = x.mul(&x).sub(&y.mul(&y));
        assert_eq!(prod, expected);
    }

    #[test]
    fn test_multivariate_remainder_exact() {
        let x = ExactPoly4::var(0);
        let y = ExactPoly4::var(1);
        let one = ExactPoly4::constant(BigRational::one());

        let g1 = x.mul(&y).sub(&one);
        let f = x.mul(&x).mul(&y).sub(&x);
        let rem = multivariate_remainder(&f, &[g1]);
        assert!(rem.is_zero());
    }

    #[test]
    fn test_s_polynomial_cancels_leading_monomial() {
        let x = ExactPoly4::var(0);
        let y = ExactPoly4::var(1);
        let two = ExactPoly4::constant(BigRational::from_integer(2.into()));
        let f = x.mul(&x).mul(&x).sub(&two.mul(&x).mul(&y));
        let g = x.mul(&x).mul(&y).sub(&two.mul(&y).mul(&y)).add(&x);

        let s_poly = compute_s_polynomial(&f, &g);
        let (lm, _) = s_poly.leading_term().unwrap();
        assert_ne!(lm, [3, 1, 0, 0]);
    }

    #[test]
    fn test_canonical_slice_groebner_certified() {
        let receipt = solve_and_certify_cylindrical_slice_groebner();
        assert_eq!(receipt.status, "PASS");
        assert!(receipt.buchberger_confluent);
        assert!(receipt.degree_bound_respected);
        assert_eq!(receipt.initial_generators, 3);
        assert_eq!(receipt.basis_polynomials, 4);
        assert_eq!(receipt.max_degree, 2);
        assert_eq!(receipt.total_pairs_checked, 6);
        assert_eq!(receipt.zero_remainders_count, 6);
        assert_eq!(receipt.firewall, "stated region only; mints no authority");
        assert_eq!(receipt.authority_effect, "None");
    }
}
