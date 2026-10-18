// AuthorityEffect: None.

//! Declared combinatorial area count and Page schedule from the finite-QM
//! simplicial host.
//!
//! Source: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/simplicial_gravity.rs`,
//! the functions `area_model` and `page_curve`. The constraint relaxation in
//! that file stays a JSON host over `omega_general_relativity::simplicial_dynamics`.
//!
//! `boundary_area = 4 n - 2 |glued|`. Bulk, boundary and reduction counts are
//! `d` to those powers. Entropy is the imposed convention `area / 4`, not a
//! derived von Neumann entropy. The Page schedule radiates `a` in `steps`
//! equal shares, with the remainder on the first steps. The clock is
//! `(tau - kappa * radiated / a) / (1 + tau * kappa * radiated / a)`.
//!
//! Refused: an empty complex, a carrier above the stated bounds, a face used
//! twice or outside its tetrahedron, an odd or tiny area, a nonpositive `tau`,
//! and a `kappa` outside `[0, tau]`.
//!
//! AuthorityEffect: None. Finite steps of this schedule do not establish a
//! continuum limit.

use num_bigint::BigInt;
use omega_number_theory::rational::{ri, rq, Rational as Q};
use serde::Serialize;
use std::collections::BTreeSet;

fn qstr(q: &Q) -> String {
    if q.denom() == &BigInt::from(1) {
        q.numer().to_string()
    } else {
        format!("{}/{}", q.numer(), q.denom())
    }
}

/// Face-gluing census of a declared tetrahedron complex.
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct AreaModel {
    pub tetrahedra: usize,
    pub internal_faces: usize,
    pub boundary_area: usize,
    pub bulk_states: String,
    pub boundary_states: String,
    pub reduction: String,
    pub entropy_convention: String,
}

/// One step of the imposed area schedule.
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct PageStep {
    pub step: usize,
    pub black_hole_area: usize,
    pub radiation_area: usize,
    pub entropy: String,
    pub schmidt_ceiling: String,
    pub defect: String,
    pub clock: String,
    pub rate_ratio: String,
    pub proper_time: String,
}

/// Count boundary faces and the imposed `A/4` label.
pub fn area_model(
    n: usize,
    glued: &[[(usize, usize); 2]],
    d: u32,
) -> Result<AreaModel, String> {
    if n == 0 || n > 256 || d < 2 || d > 256 || glued.len() > 2 * n {
        return Err("INVALID_AREA_MODEL_OR_RESOURCE_LIMIT".into());
    }
    let mut used = BTreeSet::new();
    for [a, b] in glued {
        if a == b
            || [a, b].iter().any(|&&(t, f)| t >= n || f >= 4)
            || !used.insert(*a)
            || !used.insert(*b)
        {
            return Err("INVALID_FACE_GLUING".into());
        }
    }
    let a = 4 * n - 2 * glued.len();
    let b = BigInt::from(d);
    Ok(AreaModel {
        tetrahedra: n,
        internal_faces: glued.len(),
        boundary_area: a,
        bulk_states: b.pow((4 * n) as u32).to_string(),
        boundary_states: b.pow(a as u32).to_string(),
        reduction: b.pow((2 * glued.len()) as u32).to_string(),
        entropy_convention: qstr(&rq(a as i64, 4)),
    })
}

/// Radiate area `a` in `steps` shares and record the imposed clock.
pub fn page_curve(
    a: usize,
    steps: usize,
    d: u32,
    tau: &Q,
    kappa: &Q,
) -> Result<Vec<PageStep>, String> {
    if a < 2
        || a % 2 != 0
        || a > 1024
        || steps == 0
        || steps > 1024
        || d < 2
        || d > 256
        || tau <= &ri(0)
        || kappa < &ri(0)
        || kappa > tau
    {
        return Err("INVALID_PAGE_PARAMETERS".into());
    }
    let mut radiated = 0;
    let mut proper = ri(0);
    let mut out = vec![];
    for i in 0..=steps {
        if i > 0 {
            radiated += a / steps + usize::from(i <= a % steps);
        }
        let black = a - radiated;
        let defect = kappa * rq(radiated as i64, a as i64);
        let clock = (tau - &defect) / (ri(1) + tau * &defect);
        let ratio = &clock / tau;
        if i > 0 {
            proper += &ratio;
        }
        out.push(PageStep {
            step: i,
            black_hole_area: black,
            radiation_area: radiated,
            entropy: qstr(&rq(black.min(radiated) as i64, 4)),
            schmidt_ceiling: BigInt::from(d).pow(black.min(radiated) as u32).to_string(),
            defect: qstr(&defect),
            clock: qstr(&clock),
            rate_ratio: qstr(&ratio),
            proper_time: qstr(&proper),
        });
    }
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn area_count_and_page_schedule_match_the_declared_arithmetic() {
        let model = area_model(2, &[[(0, 1), (1, 0)]], 2).unwrap();
        assert_eq!(
            (model.tetrahedra, model.internal_faces, model.boundary_area),
            (2, 1, 6)
        );
        assert_eq!(
            (
                model.bulk_states.as_str(),
                model.boundary_states.as_str(),
                model.reduction.as_str(),
                model.entropy_convention.as_str()
            ),
            ("256", "64", "4", "3/2")
        );
        assert!(area_model(2, &[[(0, 0), (1, 0)], [(0, 0), (1, 1)]], 2).is_err());
        let page = page_curve(12, 6, 2, &rq(1, 2), &rq(1, 4)).unwrap();
        let entropies: Vec<&str> = page.iter().map(|s| s.entropy.as_str()).collect();
        assert_eq!(entropies, vec!["0", "1/2", "1", "3/2", "1", "1/2", "0"]);
        assert_eq!((page[6].black_hole_area, page[6].radiation_area), (0, 12));
        assert_eq!(
            (page[6].clock.as_str(), page[6].rate_ratio.as_str()),
            ("2/9", "4/9")
        );
        assert!(page_curve(12, 6, 2, &rq(1, 4), &rq(1, 2)).is_err());
        assert!(page_curve(3, 2, 2, &ri(1), &ri(0)).is_err());
    }
}
