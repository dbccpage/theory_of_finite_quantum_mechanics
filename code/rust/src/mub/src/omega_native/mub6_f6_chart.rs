
use serde::Serialize;

use crate::omega_native::exact::d6_exact_curvature_cochain::{abs_sq, inner, ExactVec, D};
use crate::omega_native::exact::mub6_field::inv_sqrt6;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

fn f3(j: usize, k: usize) -> Cyc24 {
    Cyc24::zeta24(((8 * j * k) % 24) as i32)
}

pub fn f6_family_columns(dx: i64, dy: i64) -> [ExactVec; D] {
    let s = inv_sqrt6();
    let dphase = [
        Cyc24::rat(ri(1)),
        Cyc24::zeta24(dx as i32),
        Cyc24::zeta24(dy as i32),
    ];
    std::array::from_fn(|col| {
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        if col < 3 {
            for j in 0..3 {
                let e = f3(j, col).mul(&s);
                v[j] = e.clone();
                v[j + 3] = e;
            }
        } else {
            let m = col - 3;
            for j in 0..3 {
                let e = dphase[j].mul(&f3(j, m)).mul(&s);
                v[j] = e.clone();
                v[j + 3] = e.neg();
            }
        }
        v
    })
}

pub fn f6_point_is_exact_chm(dx: i64, dy: i64) -> bool {
    let cols = f6_family_columns(dx, dy);
    let target = Cyc24::rat(ri(1) / ri(D as i64));
    for col in &cols {
        for entry in col {
            if abs_sq(entry) != target {
                return false;
            }
        }
    }
    let one = Cyc24::rat(ri(1));
    let zero = Cyc24::zero();
    for i in 0..D {
        for j in 0..D {
            let ip = inner(&cols[i], &cols[j]);
            let want = if i == j { &one } else { &zero };
            if &ip != want {
                return false;
            }
        }
    }
    true
}

#[derive(Debug, Clone, Serialize)]
pub struct F6Chart {
    pub chart_id: &'static str,
    pub family: &'static str,
    pub params: &'static str,
    pub hadamard_for_all_params: bool,
    pub unbiased_to_standard: bool,
    pub charts: &'static str,
    pub cover_obligation: &'static str,
    pub firewall: &'static str,
}

pub fn declare_f6_chart() -> F6Chart {
    F6Chart {
        chart_id: "mub6-moduli-piece1-affine-fourier-F6",
        family: "Dita affine Fourier family F6(x,y) = (1/sqrt6)[[F3, D F3],[F3, -D F3]], D=diag(1,e^{ix},e^{iy})",
        params: "(x,y) phases; exact at e^{ix}=zeta_24^{dx}, e^{iy}=zeta_24^{dy}",
        hadamard_for_all_params: true,
        unbiased_to_standard: true,
        charts: "the 2-parameter affine Fourier slice of 6x6 CHMs = MU pairs {I, F6(x,y)/sqrt6}; one CHM factor of an MU triple",
        cover_obligation: "the no-go cover needs a TRIPLE; F6(x,y) is one CHM factor (B2). EXACT finding (f6_family_pair_is_mutually_unbiased): the family is internally NON-mutually-unbiased -- distinct members share their first 3 columns and have vanishing cross-block overlaps -- so NO MU triple lives inside it. A no-go cover requires a third basis B3 mutually unbiased to {I, F6(x,y)} from OUTSIDE the family (or a proof none exists); that external B3 is the gating coordinate before mub6_basis_cover can run over the (x,y) box",
        firewall: "declares a chart + proves it Hadamard exactly + records the exact self-non-MU finding (the interval cover is not yet runnable: no triple lives inside the family); charts a 2-parameter slice, NOT the whole moduli; stated region only; mints no authority",
    }
}

pub fn f6_cross_overlap(dx: i64, dy: i64, dxp: i64, dyp: i64, i: usize, j: usize) -> Cyc24 {
    let b = f6_family_columns(dx, dy);
    let bp = f6_family_columns(dxp, dyp);
    inner(&b[i], &bp[j])
}

pub fn f6_family_pair_is_mutually_unbiased(dx: i64, dy: i64, dxp: i64, dyp: i64) -> bool {
    let b = f6_family_columns(dx, dy);
    let bp = f6_family_columns(dxp, dyp);
    let target = Cyc24::rat(ri(1) / ri(D as i64));
    for i in 0..D {
        for j in 0..D {
            if abs_sq(&inner(&b[i], &bp[j])) != target {
                return false;
            }
        }
    }
    true
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn f6_base_point_is_exact_complex_hadamard() {
        assert!(f6_point_is_exact_chm(0, 0));
    }

    #[test]
    fn f6_nontrivial_points_stay_exact_hadamard() {
        assert!(f6_point_is_exact_chm(8, 16));
        assert!(f6_point_is_exact_chm(3, 7));
        assert!(f6_point_is_exact_chm(11, 23));
    }

    #[test]
    fn declared_chart_records_exactly_witnessed_properties() {
        let c = declare_f6_chart();
        assert!(c.hadamard_for_all_params && f6_point_is_exact_chm(5, 13));
        assert!(c.unbiased_to_standard);
        assert!(c.firewall.contains("NOT the whole moduli"));
        assert!(c.cover_obligation.contains("third basis B3"));
    }

    #[test]
    fn f6_family_is_internally_non_mu_so_no_triple_inside() {
        for (a, b, c, d) in [(0, 0, 8, 16), (3, 7, 11, 23), (0, 0, 5, 13)] {
            assert!(!f6_family_pair_is_mutually_unbiased(a, b, c, d));
            assert_eq!(f6_cross_overlap(a, b, c, d, 0, 0), Cyc24::rat(ri(1)));
            assert!(f6_cross_overlap(a, b, c, d, 0, 3).is_zero());
            assert!(f6_cross_overlap(a, b, c, d, 3, 0).is_zero());
        }
    }
}
