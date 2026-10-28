
use crate::native::exact::d6_exact_curvature_cochain::{ExactVec, BASIS_COUNT, COLUMN_COUNT, D};
use crate::native::exact::d6_exact_tangent_obstruction::{
    curvature_jacobian, mat_vec, rank_cyc24, REAL_DIM,
};
use tfqm_number_theory::cyclotomic::Cyc24;
use tfqm_number_theory::rational::ri;

pub const C2_DIM: usize = BASIS_COUNT - 1;

pub fn bianchi_d1() -> Vec<Vec<Cyc24>> {
    let one = Cyc24::rat(ri(1));
    let neg_one = one.neg();
    let mut row0 = vec![Cyc24::zero(); COLUMN_COUNT];
    let mut row1 = vec![Cyc24::zero(); COLUMN_COUNT];
    for i in 0..D {
        row0[i] = one.clone();
        row1[i] = one.clone();
    }
    for i in D..2 * D {
        row0[i] = neg_one.clone();
    }
    for i in 2 * D..3 * D {
        row1[i] = neg_one.clone();
    }
    vec![row0, row1]
}

pub struct ObstructionCohomology {
    pub d0_rank: usize,
    pub d1_rank: usize,
    pub h1_dim: Option<usize>,
    pub h2_dim: usize,
    pub d1_after_d0_zero: bool,
}

pub fn obstruction_cohomology(columns: &[ExactVec], v: &ExactVec) -> ObstructionCohomology {
    let d0 = curvature_jacobian(columns, v);
    let d0_rank = rank_cyc24(&d0).expect("jacobian rows are rectangular");
    let d1 = bianchi_d1();
    let d1_rank = rank_cyc24(&d1).expect("Bianchi rows are rectangular");

    let mut d1_after_d0_zero = true;
    for k in 0..REAL_DIM {
        let col: Vec<Cyc24> = d0.iter().map(|row| row[k].clone()).collect();
        if !mat_vec(&d1, &col)
            .expect("Bianchi row width matches a jacobian column")
            .iter()
            .all(|z| z.is_zero())
        {
            d1_after_d0_zero = false;
            break;
        }
    }

    let ker_d1 = COLUMN_COUNT - d1_rank;
    let h1_dim = if d1_after_d0_zero {
        Some(ker_d1.saturating_sub(d0_rank))
    } else {
        None
    };
    ObstructionCohomology {
        d0_rank,
        d1_rank,
        h1_dim,
        h2_dim: C2_DIM - d1_rank,
        d1_after_d0_zero,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::native::exact::d6_exact_curvature_cochain::canonical_triple_exact;

    fn rat(num: i64, den: i64) -> Cyc24 {
        Cyc24::rat(ri(num) / ri(den))
    }

    fn generic_unit() -> ExactVec {
        let s = Cyc24::zeta24(3).add(&Cyc24::zeta24(-3)).mul(&rat(1, 2));
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[0] = s.clone();
        v[1] = Cyc24::zeta24(6).mul(&s);
        v
    }

    #[test]
    fn bianchi_d1_has_rank_two() {
        assert_eq!(rank_cyc24(&bianchi_d1()).expect("rectangular"), 2);
    }

    #[test]
    fn d1_after_d0_is_exactly_zero() {
        let cols = canonical_triple_exact();
        let report = obstruction_cohomology(&cols, &generic_unit());
        assert!(
            report.d1_after_d0_zero,
            "linearized Bianchi identity d1 . d0 = 0 must hold exactly"
        );
    }

    #[test]
    fn obstruction_cohomology_is_well_formed_and_large() {
        let cols = canonical_triple_exact();
        let report = obstruction_cohomology(&cols, &generic_unit());
        assert_eq!(report.d1_rank, 2);
        assert_eq!(report.h2_dim, 0, "C^2 = R^2 is fully hit by d1");
        assert!(
            report.d0_rank <= 11,
            "rank(J) = {} exceeds the tangent sphere",
            report.d0_rank
        );
        assert_eq!(
            report.h1_dim,
            Some(COLUMN_COUNT - report.d1_rank - report.d0_rank)
        );
        assert!(
            report.h1_dim.unwrap() >= 5,
            "obstruction cohomology H^1 = {:?} unexpectedly small",
            report.h1_dim
        );
    }

    #[test]
    fn invalid_chain_yields_none_h1() {
        let mut cols = canonical_triple_exact();
        for k in 0..6 {
            cols[0][k] = cols[0][k].mul(&rat(2, 1));
        }
        let report = obstruction_cohomology(&cols, &generic_unit());
        assert!(
            !report.d1_after_d0_zero,
            "d1 . d0 should not vanish on deformed columns"
        );
        assert_eq!(report.h1_dim, None, "H^1 must be None when d1 . d0 != 0");
    }
}
