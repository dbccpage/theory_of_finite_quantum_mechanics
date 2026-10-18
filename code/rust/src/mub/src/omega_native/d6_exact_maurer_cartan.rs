
use crate::omega_native::exact::d6_exact_curvature_cochain::{abs_sq, curvature_c2, inner, ExactVec, D};
use crate::omega_native::exact::d6_exact_lift_repair::solve_exact;
use crate::omega_native::exact::d6_exact_obstruction_cohomology::bianchi_d1;
use crate::omega_native::exact::d6_exact_tangent_obstruction::{
    curvature_jacobian, im, mat_vec, re, REAL_DIM,
};
use omega_number_theory::cyclotomic::Cyc24;

pub fn quadratic_bracket(columns: &[ExactVec], dv: &ExactVec) -> Vec<Cyc24> {
    columns.iter().map(|e| abs_sq(&inner(e, dv))).collect()
}

pub struct SecondOrderObstruction {
    pub bracket: Vec<Cyc24>,
    pub bianchi_closed: bool,
    pub quadratic_in_jacobian_image: bool,
    pub is_first_order_tangent: bool,
    pub is_first_order_repair: bool,
    pub formal_extension_valid: bool,
    pub second_order_absorbable: bool,
}

pub fn second_order_obstruction(
    columns: &[ExactVec],
    v: &ExactVec,
    dv: &ExactVec,
) -> SecondOrderObstruction {
    let q = quadratic_bracket(columns, dv);
    let bianchi_closed = mat_vec(&bianchi_d1(), &q)
        .expect("Bianchi row width matches the quadratic bracket")
        .iter()
        .all(|z| z.is_zero());
    let j = curvature_jacobian(columns, v);
    let neg_q: Vec<Cyc24> = q.iter().map(|x| x.neg()).collect();
    let quadratic_in_jacobian_image = matches!(solve_exact(&j, &neg_q), Ok(Some(_)));

    let omega = curvature_c2(columns, v);
    let neg_omega: Vec<Cyc24> = omega.iter().map(|w| w.neg()).collect();
    let mut dv_real = vec![Cyc24::zero(); REAL_DIM];
    for k in 0..D {
        dv_real[2 * k] = re(&dv[k]);
        dv_real[2 * k + 1] = im(&dv[k]);
    }
    let j_dv = mat_vec(&j, &dv_real).expect("jacobian row width matches the deformation");
    let is_first_order_tangent =
        j_dv.iter().all(|z| z.is_zero()) && omega.iter().all(|z| z.is_zero());
    let is_first_order_repair = j_dv == neg_omega;
    let formal_extension_valid =
        (is_first_order_tangent || is_first_order_repair) && quadratic_in_jacobian_image;

    SecondOrderObstruction {
        bracket: q,
        bianchi_closed,
        quadratic_in_jacobian_image,
        is_first_order_tangent,
        is_first_order_repair,
        formal_extension_valid,
        second_order_absorbable: quadratic_in_jacobian_image,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::exact::d6_exact_curvature_cochain::{
        canonical_triple_exact, norm_sq, BASIS_COUNT, COLUMN_COUNT, D,
    };
    use omega_number_theory::rational::ri;

    fn rat(num: i64, den: i64) -> Cyc24 {
        Cyc24::rat(ri(num) / ri(den))
    }

    fn e0() -> ExactVec {
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[0] = Cyc24::rat(ri(1));
        v
    }

    fn generic_unit() -> ExactVec {
        let s = Cyc24::zeta24(3).add(&Cyc24::zeta24(-3)).mul(&rat(1, 2));
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[0] = s.clone();
        v[1] = Cyc24::zeta24(6).mul(&s);
        v
    }

    #[test]
    fn quadratic_bracket_at_e0_has_known_values() {
        let cols = canonical_triple_exact();
        let q = quadratic_bracket(&cols, &e0());
        assert_eq!(q[0], Cyc24::rat(ri(1)));
        for j in 1..D {
            assert!(q[j].is_zero());
        }
        for i in D..COLUMN_COUNT {
            assert_eq!(q[i], rat(1, D as i64));
        }
    }

    #[test]
    fn bracket_respects_bianchi_via_parseval() {
        let cols = canonical_triple_exact();
        for dv in [e0(), generic_unit()] {
            let q = quadratic_bracket(&cols, &dv);
            let nsq = norm_sq(&dv);
            for b in 0..BASIS_COUNT {
                let mut s = Cyc24::zero();
                for j in 0..D {
                    s = s.add(&q[b * D + j]);
                }
                assert_eq!(
                    s, nsq,
                    "Parseval: per-basis bracket sum must equal ||dv||^2"
                );
            }
            assert!(mat_vec(&bianchi_d1(), &q)
                .expect("rectangular")
                .iter()
                .all(|z| z.is_zero()));
        }
    }

    #[test]
    fn second_order_obstruction_is_well_formed_and_bianchi_closed() {
        let cols = canonical_triple_exact();
        let report = second_order_obstruction(&cols, &generic_unit(), &e0());
        assert_eq!(report.bracket.len(), COLUMN_COUNT);
        assert!(
            report.bianchi_closed,
            "the MC quadratic term is Bianchi-closed (Parseval)"
        );
        let j = curvature_jacobian(&cols, &generic_unit());
        let neg_q: Vec<Cyc24> = report.bracket.iter().map(|x| x.neg()).collect();
        assert_eq!(
            report.second_order_absorbable,
            matches!(solve_exact(&j, &neg_q), Ok(Some(_)))
        );
    }
}
