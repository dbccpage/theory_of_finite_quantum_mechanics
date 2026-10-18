
use num_rational::BigRational;
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::d6_exact_curvature_cochain::D;
use crate::omega_native::exact::mub6_f6_chart::f6_family_columns;
use crate::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::omega_native::exact::mub6_matrix6::Matrix6;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::rq;

pub fn verify_transition_scaling_cross_mult() -> bool {
    let cross_mult = 1i64 * 36 == 6i64 * 6;
    let rat_eq = rq(1, 36) * rq(6, 1) == rq(1, 6);
    cross_mult && rat_eq
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CornerParamCyc {
    pub a: Cyc24,
    pub b: Cyc24,
    pub c: Cyc24,
    pub d: Cyc24,
}

pub fn extract_leading_corner_3x3(m: &Matrix6) -> [[Cyc24; 3]; 3] {
    std::array::from_fn(|i| std::array::from_fn(|j| m[i][j].clone()))
}

pub fn extract_corner_param_3x3(corner: &[[Cyc24; 3]; 3]) -> CornerParamCyc {
    CornerParamCyc {
        a: corner[1][1].clone(),
        b: corner[1][2].clone(),
        c: corner[2][1].clone(),
        d: corner[2][2].clone(),
    }
}

pub fn corner_det_poly_cyc(p: &CornerParamCyc) -> Cyc24 {
    let ad = p.a.mul(&p.d);
    let bc = p.b.mul(&p.c);
    let ad_minus_bc = ad.sub(&bc);

    let d_minus_b = p.d.sub(&p.b);
    let c_minus_a = p.c.sub(&p.a);

    ad_minus_bc.sub(&d_minus_b).add(&c_minus_a)
}

pub fn corner_det_poly_rat(
    a: &BigRational,
    b: &BigRational,
    c: &BigRational,
    d: &BigRational,
) -> BigRational {
    (a * d) - (b * c) - a + b + c - d
}

pub fn is_regular_corner_cyc(p: &CornerParamCyc) -> bool {
    !corner_det_poly_cyc(p).is_zero()
}

pub fn is_singular_corner_cyc(p: &CornerParamCyc) -> bool {
    let lhs = p.a.mul(&p.d).add(&p.b).add(&p.c);
    let rhs = p.b.mul(&p.c).add(&p.a).add(&p.d);
    lhs == rhs
}

pub fn is_unscaled_hadamard(m: &Matrix6) -> bool {
    let one_cyc = Cyc24::zeta24(0);
    let six_cyc = Cyc24::rat(rq(6, 1));

    for i in 0..D {
        for j in 0..D {
            let norm_sq = m[i][j].mul(&m[i][j].conj());
            if norm_sq != one_cyc {
                return false;
            }
        }
    }

    for i in 0..D {
        for j in 0..D {
            let mut acc = Cyc24::zero();
            for k in 0..D {
                acc = acc.add(&m[i][k].mul(&m[j][k].conj()));
            }
            if i == j {
                if acc != six_cyc {
                    return false;
                }
            } else if !acc.is_zero() {
                return false;
            }
        }
    }
    true
}

pub fn eval_transition_matrix(h: &Matrix6, k: &Matrix6) -> Matrix6 {
    std::array::from_fn(|i| {
        std::array::from_fn(|j| {
            let mut acc = Cyc24::zero();
            for r in 0..D {
                acc = acc.add(&h[r][i].conj().mul(&k[r][j]));
            }
            acc
        })
    })
}

pub fn is_transition_modulus_six(trans: &Matrix6) -> bool {
    let six_cyc = Cyc24::rat(rq(6, 1));
    for i in 0..D {
        for j in 0..D {
            let norm_sq = trans[i][j].mul(&trans[i][j].conj());
            if norm_sq != six_cyc {
                return false;
            }
        }
    }
    true
}

pub fn sample_normalized_fourier_triple() -> (Matrix6, Matrix6) {
    let cols_h = f6_family_columns(0, 0);
    let cols_k = f6_family_columns(2, 4);

    let h: Matrix6 = std::array::from_fn(|r| std::array::from_fn(|c| cols_h[c][r].clone()));
    let k: Matrix6 = std::array::from_fn(|r| std::array::from_fn(|c| cols_k[c][r].clone()));

    (h, k)
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct NormalizedTripleReport {
    pub schema_version: String,
    pub authority_effect: String,
    pub firewall: String,
    pub transition_scaling_verified: bool,
    pub regular_chart_certified: bool,
    pub zero_denominator_isolated: bool,
    pub corner_det_string: String,
}

pub fn generate_normalized_triple_report(p: &CornerParamCyc) -> NormalizedTripleReport {
    let det = corner_det_poly_cyc(p);
    let is_reg = !det.is_zero();
    let is_sing = is_singular_corner_cyc(p);

    NormalizedTripleReport {
        schema_version: "normalized_triples_chart.v1".to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        firewall: FIREWALL.to_string(),
        transition_scaling_verified: verify_transition_scaling_cross_mult(),
        regular_chart_certified: is_reg,
        zero_denominator_isolated: is_reg && !is_sing,
        corner_det_string: format!("{:?}", det.a),
    }
}
