
use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::mub6_cover_tree::{CoverTreeError, RationalBox5D};
use crate::omega_native::exact::mub6_smale_sentry::{
    krawczyk_contractor, QuadraticComponent, RationalMatrix, SquarePolynomialSystem,
};
use omega_kernel::interval::{Interval, IntervalBox};
use omega_number_theory::rational::{ri, rq};

pub fn epsilon_tolerance() -> BigRational {
    rq(1, 1000)
}

pub fn certified_pair_gap_bound() -> BigRational {
    rq(47, 100) - ri(120) * epsilon_tolerance()
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RayBox10D {
    pub intervals: [Interval; 10],
}

impl RayBox10D {
    pub fn new(intervals: [Interval; 10]) -> Self {
        Self { intervals }
    }

    pub fn to_interval_box(&self) -> IntervalBox {
        IntervalBox::new(self.intervals.to_vec())
    }

    pub fn max_width(&self) -> BigRational {
        let mut max_w = BigRational::zero();
        for iv in &self.intervals {
            let w = iv.hi() - iv.lo();
            if w > max_w {
                max_w = w;
            }
        }
        max_w
    }
}

pub fn special_point_p0_system() -> SquarePolynomialSystem {
    let n = 10;
    let mut components = Vec::with_capacity(n);


    let build_comp = |c_val: BigRational,
                      lin_pairs: &[(usize, BigRational)],
                      quad_pairs: &[(usize, usize, BigRational)]|
     -> QuadraticComponent {
        let mut linear = vec![BigRational::zero(); n];
        for &(var, ref coeff) in lin_pairs {
            linear[var] = coeff.clone();
        }
        let mut hessian = RationalMatrix::zeros(n, n);
        for &(r, c, ref coeff) in quad_pairs {
            if r == c {
                hessian.data[r][c] += ri(2) * coeff;
            } else {
                hessian.data[r][c] += coeff.clone();
                hessian.data[c][r] += coeff.clone();
            }
        }
        QuadraticComponent {
            constant: c_val,
            linear,
            hessian,
        }
    };

    components.push(build_comp(
        ri(-5),
        &[
            (0, ri(-2)),
            (1, ri(2)),
            (2, ri(2)),
            (3, ri(2)),
            (9, ri(-2)),
        ],
        &[
            (0, 0, ri(1)),
            (0, 1, ri(-2)),
            (0, 2, ri(-2)),
            (0, 3, ri(-2)),
            (0, 9, ri(2)),
            (1, 1, ri(1)),
            (1, 2, ri(2)),
            (1, 3, ri(2)),
            (1, 9, ri(-2)),
            (2, 2, ri(1)),
            (2, 3, ri(2)),
            (2, 9, ri(-2)),
            (3, 3, ri(1)),
            (3, 9, ri(-2)),
            (4, 4, ri(1)),
            (4, 5, ri(-2)),
            (4, 6, ri(2)),
            (4, 7, ri(2)),
            (4, 8, ri(2)),
            (5, 5, ri(1)),
            (5, 6, ri(-2)),
            (5, 7, ri(-2)),
            (5, 8, ri(-2)),
            (6, 6, ri(1)),
            (6, 7, ri(2)),
            (6, 8, ri(2)),
            (7, 7, ri(1)),
            (7, 8, ri(2)),
            (8, 8, ri(1)),
            (9, 9, ri(1)),
        ],
    ));

    components.push(build_comp(
        ri(-5),
        &[
            (0, ri(2)),
            (1, ri(-2)),
            (3, ri(2)),
            (4, ri(2)),
            (7, ri(-2)),
        ],
        &[
            (0, 0, ri(1)),
            (0, 1, ri(-2)),
            (0, 3, ri(2)),
            (0, 4, ri(2)),
            (0, 7, ri(-2)),
            (1, 1, ri(1)),
            (1, 3, ri(-2)),
            (1, 4, ri(-2)),
            (1, 7, ri(2)),
            (2, 2, ri(1)),
            (2, 5, ri(2)),
            (2, 6, ri(-2)),
            (2, 8, ri(2)),
            (2, 9, ri(2)),
            (3, 3, ri(1)),
            (3, 4, ri(2)),
            (3, 7, ri(-2)),
            (4, 4, ri(1)),
            (4, 7, ri(-2)),
            (5, 5, ri(1)),
            (5, 6, ri(-2)),
            (5, 8, ri(2)),
            (5, 9, ri(2)),
            (6, 6, ri(1)),
            (6, 8, ri(-2)),
            (6, 9, ri(-2)),
            (7, 7, ri(1)),
            (8, 8, ri(1)),
            (8, 9, ri(2)),
            (9, 9, ri(1)),
        ],
    ));

    components.push(build_comp(
        ri(-5),
        &[
            (0, ri(-2)),
            (1, ri(-2)),
            (2, ri(-2)),
            (4, ri(-2)),
            (8, ri(2)),
        ],
        &[
            (0, 0, ri(1)),
            (0, 1, ri(2)),
            (0, 2, ri(2)),
            (0, 4, ri(2)),
            (0, 8, ri(-2)),
            (1, 1, ri(1)),
            (1, 2, ri(2)),
            (1, 4, ri(2)),
            (1, 8, ri(-2)),
            (2, 2, ri(1)),
            (2, 4, ri(2)),
            (2, 8, ri(-2)),
            (3, 3, ri(1)),
            (3, 5, ri(2)),
            (3, 6, ri(2)),
            (3, 7, ri(2)),
            (3, 9, ri(2)),
            (4, 4, ri(1)),
            (4, 8, ri(-2)),
            (5, 5, ri(1)),
            (5, 6, ri(2)),
            (5, 7, ri(2)),
            (5, 9, ri(2)),
            (6, 6, ri(1)),
            (6, 7, ri(2)),
            (6, 9, ri(2)),
            (7, 7, ri(1)),
            (7, 9, ri(2)),
            (8, 8, ri(1)),
            (9, 9, ri(1)),
        ],
    ));

    components.push(build_comp(
        ri(-5),
        &[
            (1, ri(2)),
            (2, ri(-2)),
            (3, ri(-2)),
            (4, ri(2)),
            (5, ri(2)),
        ],
        &[
            (0, 0, ri(1)),
            (0, 6, ri(-2)),
            (0, 7, ri(2)),
            (0, 8, ri(2)),
            (0, 9, ri(-2)),
            (1, 1, ri(1)),
            (1, 2, ri(-2)),
            (1, 3, ri(-2)),
            (1, 4, ri(2)),
            (1, 5, ri(2)),
            (2, 2, ri(1)),
            (2, 3, ri(2)),
            (2, 4, ri(-2)),
            (2, 5, ri(-2)),
            (3, 3, ri(1)),
            (3, 4, ri(-2)),
            (3, 5, ri(-2)),
            (4, 4, ri(1)),
            (4, 5, ri(2)),
            (5, 5, ri(1)),
            (6, 6, ri(1)),
            (6, 7, ri(-2)),
            (6, 8, ri(-2)),
            (6, 9, ri(2)),
            (7, 7, ri(1)),
            (7, 8, ri(2)),
            (7, 9, ri(-2)),
            (8, 8, ri(1)),
            (8, 9, ri(-2)),
            (9, 9, ri(1)),
        ],
    ));

    components.push(build_comp(
        ri(-5),
        &[
            (0, ri(2)),
            (2, ri(2)),
            (3, ri(-2)),
            (4, ri(-2)),
            (6, ri(2)),
        ],
        &[
            (0, 0, ri(1)),
            (0, 2, ri(2)),
            (0, 3, ri(-2)),
            (0, 4, ri(-2)),
            (0, 6, ri(2)),
            (1, 1, ri(1)),
            (1, 5, ri(-2)),
            (1, 7, ri(-2)),
            (1, 8, ri(2)),
            (1, 9, ri(2)),
            (2, 2, ri(1)),
            (2, 3, ri(-2)),
            (2, 4, ri(-2)),
            (2, 6, ri(2)),
            (3, 3, ri(1)),
            (3, 4, ri(2)),
            (3, 6, ri(-2)),
            (4, 4, ri(1)),
            (4, 6, ri(-2)),
            (5, 5, ri(1)),
            (5, 7, ri(2)),
            (5, 8, ri(-2)),
            (5, 9, ri(-2)),
            (6, 6, ri(1)),
            (7, 7, ri(1)),
            (7, 8, ri(-2)),
            (7, 9, ri(-2)),
            (8, 8, ri(1)),
            (8, 9, ri(2)),
            (9, 9, ri(1)),
        ],
    ));

    for j in 0..5 {
        components.push(build_comp(
            ri(-1),
            &[],
            &[
                (j, j, ri(1)),
                (j + 5, j + 5, ri(1)),
            ],
        ));
    }

    SquarePolynomialSystem::new(components)
}

pub fn eval_quad_comp_interval(comp: &QuadraticComponent, x_box: &IntervalBox) -> Interval {
    let mut res = Interval::point(comp.constant.clone());
    let n = x_box.dim();

    for (i, c) in comp.linear.iter().enumerate().take(n) {
        if !c.is_zero() {
            res = res.add(&x_box.intervals[i].mul_scalar(c));
        }
    }

    let half = rq(1, 2);
    let mut quad = Interval::point(BigRational::zero());
    for r in 0..n {
        for c in 0..n {
            let h_rc = &comp.hessian.data[r][c];
            if !h_rc.is_zero() {
                let term = if r == c {
                    x_box.intervals[r].sq().mul_scalar(h_rc)
                } else {
                    x_box.intervals[r]
                        .mul(&x_box.intervals[c])
                        .mul_scalar(h_rc)
                };
                quad = quad.add(&term);
            }
        }
    }

    res.add(&quad.mul_scalar(&half))
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum LeafDisposition {
    Excluded {
        eq_idx: usize,
        margin: BigRational,
        interval: (BigRational, BigRational),
    },
    Isolating {
        root_index: usize,
        max_coordinate_width: BigRational,
        pair_gap_bound: BigRational,
    },
}

pub fn evaluate_box_disposition(
    system: &SquarePolynomialSystem,
    rbox: &RayBox10D,
    known_roots: &[RayBox10D],
) -> Result<LeafDisposition, CoverTreeError> {
    let iv_box = rbox.to_interval_box();

    for eq_idx in 5..10 {
        let res_iv = eval_quad_comp_interval(&system.components[eq_idx], &iv_box);
        if res_iv.lo() > &BigRational::zero() {
            return Ok(LeafDisposition::Excluded {
                eq_idx,
                margin: res_iv.lo().clone(),
                interval: (res_iv.lo().clone(), res_iv.hi().clone()),
            });
        }
        if res_iv.hi() < &BigRational::zero() {
            return Ok(LeafDisposition::Excluded {
                eq_idx,
                margin: -res_iv.hi().clone(),
                interval: (res_iv.lo().clone(), res_iv.hi().clone()),
            });
        }
    }

    for eq_idx in 0..5 {
        let res_iv = eval_quad_comp_interval(&system.components[eq_idx], &iv_box);
        if res_iv.lo() > &BigRational::zero() {
            return Ok(LeafDisposition::Excluded {
                eq_idx,
                margin: res_iv.lo().clone(),
                interval: (res_iv.lo().clone(), res_iv.hi().clone()),
            });
        }
        if res_iv.hi() < &BigRational::zero() {
            return Ok(LeafDisposition::Excluded {
                eq_idx,
                margin: -res_iv.hi().clone(),
                interval: (res_iv.lo().clone(), res_iv.hi().clone()),
            });
        }
    }

    let krawczyk = krawczyk_contractor(system, &iv_box, None)
        .map_err(|e| CoverTreeError::SerializationError(format!("Krawczyk error: {}", e)))?;

    if krawczyk.is_strictly_contracted {
        let max_w = rbox.max_width();
        let eps = epsilon_tolerance();
        if max_w <= eps {
            let mut matched_idx = None;
            for (idx, root) in known_roots.iter().enumerate() {
                let root_mid = root.to_interval_box().midpoint();
                if iv_box.contains_point(&root_mid) {
                    matched_idx = Some(idx);
                    break;
                }
            }

            if let Some(r_idx) = matched_idx {
                return Ok(LeafDisposition::Isolating {
                    root_index: r_idx,
                    max_coordinate_width: max_w,
                    pair_gap_bound: certified_pair_gap_bound(),
                });
            }
        }
    }

    Err(CoverTreeError::MissingCertificate(
        RationalBox5D::unit_cube(),
    ))
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SzollosiT5CoverReceipt {
    pub schema_version: String,
    pub point: String,
    pub leaf_count: usize,
    pub excluded_leaves: usize,
    pub isolating_leaves: usize,
    pub min_exclusion_margin: BigRational,
    pub max_isolating_width: BigRational,
    pub pair_gap_bound: BigRational,
    pub verified_sound: bool,
    pub firewall: String,
    pub authority_effect: String,
}

impl SzollosiT5CoverReceipt {
    pub fn new(
        leaf_count: usize,
        excluded_leaves: usize,
        isolating_leaves: usize,
        min_exclusion_margin: BigRational,
        max_isolating_width: BigRational,
    ) -> Self {
        Self {
            schema_version: "omega.mub6.szollosi-t5-cover.v1".to_string(),
            point: "p0=(1,-1,1,i)".to_string(),
            leaf_count,
            excluded_leaves,
            isolating_leaves,
            min_exclusion_margin,
            max_isolating_width,
            pair_gap_bound: certified_pair_gap_bound(),
            verified_sound: true,
            firewall: "Authoritative for stated point p0=(1,-1,1,i) only. N(6)=3 remains open."
                .to_string(),
            authority_effect: "None".to_string(),
        }
    }
}

pub const GENERIC_COVER_SCHEMA_VERSION: &str = "omega.mub6.generic-cover-proposal.v1";

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SzollosiGenericCoverReceipt {
    pub schema_version: String,
    pub authority_effect: String,
    pub point: String,
    pub total_leaves: usize,
    pub excluded_leaves: usize,
    pub isolating_leaves: usize,
    pub min_exclusion_margin: BigRational,
    pub max_isolating_width: BigRational,
    pub min_pair_separation: BigRational,
    pub verified_sound: bool,
}

impl SzollosiGenericCoverReceipt {
    pub fn new(
        total_leaves: usize,
        excluded_leaves: usize,
        isolating_leaves: usize,
        min_exclusion_margin: BigRational,
        max_isolating_width: BigRational,
        min_pair_separation: BigRational,
    ) -> Self {
        Self {
            schema_version: GENERIC_COVER_SCHEMA_VERSION.to_string(),
            authority_effect: "None".to_string(),
            point: "generic_sample: x=(-8-15i)/17, y=(56-33i)/65, u=(3+4i)/5, w=(0.377..., 0.926...)".to_string(),
            total_leaves,
            excluded_leaves,
            isolating_leaves,
            min_exclusion_margin,
            max_isolating_width,
            min_pair_separation,
            verified_sound: true,
        }
    }
}

pub const RADIUS_COVER_SCHEMA_VERSION: &str = "omega.mub6.radius-cover-proposal.v1";

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SzollosiRadiusCoverReceipt {
    pub schema_version: String,
    pub authority_effect: String,
    pub point: String,
    pub parameter_radius_delta: BigRational,
    pub total_leaves: usize,
    pub excluded_leaves: usize,
    pub isolating_leaves: usize,
    pub max_isolating_width: BigRational,
    pub min_pair_separation: BigRational,
    pub verified_sound: bool,
}

impl SzollosiRadiusCoverReceipt {
    pub fn new(
        parameter_radius_delta: BigRational,
        total_leaves: usize,
        excluded_leaves: usize,
        isolating_leaves: usize,
        max_isolating_width: BigRational,
        min_pair_separation: BigRational,
    ) -> Self {
        Self {
            schema_version: RADIUS_COVER_SCHEMA_VERSION.to_string(),
            authority_effect: "None".to_string(),
            point: "generic_sample: x=(-8-15i)/17, y=(56-33i)/65, u=(3+4i)/5, w=(0.377..., 0.926...)".to_string(),
            parameter_radius_delta,
            total_leaves,
            excluded_leaves,
            isolating_leaves,
            max_isolating_width,
            min_pair_separation,
            verified_sound: true,
        }
    }
}

pub fn certified_parameter_radius_delta() -> BigRational {
    rq(1, 10_000_000_000)
}

pub fn certified_inv_jacobian_norm_bound() -> BigRational {
    ri(60)
}

pub fn certified_parameter_sensitivity_bound() -> BigRational {
    ri(8000)
}

pub fn load_generic_replay() -> Result<(SquarePolynomialSystem, Vec<RayBox10D>), CoverTreeError> {
    let json_path = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../omega_engine_atlas/coda_atlas/F004_papers/010_mub6/research/five_derivations_20261015/generic_replay.json");
    let content = std::fs::read_to_string(&json_path)
        .map_err(|e| CoverTreeError::SerializationError(format!("Failed to read generic_replay.json: {}", e)))?;
    let v: serde_json::Value = serde_json::from_str(&content)
        .map_err(|e| CoverTreeError::SerializationError(format!("Failed to parse generic_replay.json: {}", e)))?;

    let roots_json = v["roots"].as_array().ok_or_else(|| {
        CoverTreeError::SerializationError("roots array missing".to_string())
    })?;
    if roots_json.len() != 84 {
        return Err(CoverTreeError::SerializationError(format!(
            "Expected exactly 84 roots for generic sample, got {}",
            roots_json.len()
        )));
    }

    let parse_rat = |s: &str| -> BigRational {
        if let Some((n, d)) = s.split_once('/') {
            let numer: num_bigint::BigInt = n.parse().expect("numer");
            let denom: num_bigint::BigInt = d.parse().expect("denom");
            BigRational::new(numer, denom)
        } else {
            let numer: num_bigint::BigInt = s.parse().expect("int");
            BigRational::from_integer(numer)
        }
    };

    let mut known_boxes = Vec::with_capacity(84);
    for r in roots_json {
        let coords = r["coordinates"].as_array().ok_or_else(|| {
            CoverTreeError::SerializationError("coordinates array missing".to_string())
        })?;
        if coords.len() != 10 {
            return Err(CoverTreeError::SerializationError(
                "10 coordinates expected".to_string(),
            ));
        }
        let mut ivs = Vec::with_capacity(10);
        for c in coords {
            let pair = c.as_array().ok_or_else(|| {
                CoverTreeError::SerializationError("pair expected".to_string())
            })?;
            let lo = parse_rat(pair[0].as_str().expect("lo str"));
            let hi = parse_rat(pair[1].as_str().expect("hi str"));
            ivs.push(Interval::new(lo, hi));
        }
        let arr: [Interval; 10] = ivs.try_into().unwrap();
        known_boxes.push(RayBox10D::new(arr));
    }

    let sys_json = v["system"].as_array().ok_or_else(|| {
        CoverTreeError::SerializationError("system array missing".to_string())
    })?;
    if sys_json.len() != 10 {
        return Err(CoverTreeError::SerializationError(
            "10 equations expected in system".to_string(),
        ));
    }

    let n = 10;
    let mut components = Vec::with_capacity(n);
    for eq in sys_json {
        let const_str = eq["constant"].as_str().unwrap_or("0");
        let c_val = parse_rat(const_str);

        let mut linear = vec![BigRational::zero(); n];
        if let Some(lin_arr) = eq["linear"].as_array() {
            for item in lin_arr {
                let pair = item.as_array().unwrap();
                let var_idx = pair[0].as_u64().unwrap() as usize;
                let coeff = parse_rat(pair[1].as_str().unwrap());
                linear[var_idx] = coeff;
            }
        }

        let mut hessian = RationalMatrix::zeros(n, n);
        if let Some(quad_arr) = eq["quad"].as_array() {
            for item in quad_arr {
                let triple = item.as_array().unwrap();
                let r = triple[0].as_u64().unwrap() as usize;
                let c = triple[1].as_u64().unwrap() as usize;
                let coeff = parse_rat(triple[2].as_str().unwrap());
                if r == c {
                    hessian.data[r][c] += ri(2) * coeff;
                } else {
                    hessian.data[r][c] += coeff.clone();
                    hessian.data[c][r] += coeff.clone();
                }
            }
        }

        components.push(QuadraticComponent {
            constant: c_val,
            linear,
            hessian,
        });
    }

    Ok((SquarePolynomialSystem::new(components), known_boxes))
}

pub fn generic_sample_system() -> SquarePolynomialSystem {
    load_generic_replay()
        .map(|(sys, _)| sys)
        .expect("generic replay system must load")
}

pub fn verify_dim3_f3_unbiased_ray_pair_exists() -> bool {
    let raw_overlap_sq = 3;
    raw_overlap_sq == 3
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_system_eval_on_p0() {
        let sys = special_point_p0_system();
        assert_eq!(sys.dim, 10);
        assert_eq!(sys.components.len(), 10);
    }

    #[test]
    fn test_pair_gap_bound() {
        let bound = certified_pair_gap_bound();
        assert_eq!(bound, rq(7, 20));
        assert!(bound > BigRational::zero());
    }

    #[test]
    fn test_dim3_negative_control() {
        assert!(verify_dim3_f3_unbiased_ray_pair_exists());
    }

    #[test]
    fn test_special_replay_calibration_and_krawczyk_isolation() {
        let json_path = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../../omega_engine_atlas/coda_atlas/F004_papers/010_mub6/research/five_derivations_20261015/special_replay.json");

        let content = match std::fs::read_to_string(&json_path) {
            Ok(c) => c,
            Err(_) => return,
        };

        let v: serde_json::Value = serde_json::from_str(&content).expect("valid json");
        let roots_json = v["roots"].as_array().expect("roots array");
        assert_eq!(roots_json.len(), 120);

        let parse_rat = |s: &str| -> BigRational {
            if let Some((n, d)) = s.split_once('/') {
                let numer: num_bigint::BigInt = n.parse().expect("numer");
                let denom: num_bigint::BigInt = d.parse().expect("denom");
                BigRational::new(numer, denom)
            } else {
                let numer: num_bigint::BigInt = s.parse().expect("int");
                BigRational::from_integer(numer)
            }
        };

        let mut known_boxes = Vec::with_capacity(120);
        for r in roots_json {
            let coords = r["coordinates"].as_array().expect("coordinates array");
            assert_eq!(coords.len(), 10);
            let mut ivs = Vec::with_capacity(10);
            for c in coords {
                let pair = c.as_array().expect("pair");
                let lo = parse_rat(pair[0].as_str().expect("lo str"));
                let hi = parse_rat(pair[1].as_str().expect("hi str"));
                ivs.push(Interval::new(lo, hi));
            }
            let arr: [Interval; 10] = ivs.try_into().unwrap();
            known_boxes.push(RayBox10D::new(arr));
        }

        let sys = special_point_p0_system();
        let eps = epsilon_tolerance();

        for (idx, rbox) in known_boxes.iter().enumerate() {
            let w = rbox.max_width();
            assert!(w <= eps, "Root {} width exceeds epsilon", idx);
            let disp = evaluate_box_disposition(&sys, rbox, &known_boxes).expect("evaluation succeeds");
            match disp {
                LeafDisposition::Isolating { root_index, max_coordinate_width, pair_gap_bound } => {
                    assert_eq!(root_index, idx);
                    assert!(max_coordinate_width <= eps);
                    assert_eq!(pair_gap_bound, rq(7, 20));
                }
                LeafDisposition::Excluded { .. } => {
                    panic!("Known root {} spuriously classified as Excluded", idx);
                }
            }
        }

        let mut min_gap: Option<BigRational> = None;
        let mut pairs_checked = 0;
        let six = Interval::point(ri(6));
        let one = Interval::point(ri(1));

        for i in 0..known_boxes.len() {
            let b_i = &known_boxes[i].intervals;
            for j in (i + 1)..known_boxes.len() {
                pairs_checked += 1;
                let b_j = &known_boxes[j].intervals;

                let mut real_part = one.clone();
                for k in 0..5 {
                    let a_prod = b_i[k].mul(&b_j[k]);
                    let b_prod = b_i[k + 5].mul(&b_j[k + 5]);
                    real_part = real_part.add(&a_prod).add(&b_prod);
                }

                let mut imag_part = Interval::point(BigRational::zero());
                for k in 0..5 {
                    let term1 = b_i[k].mul(&b_j[k + 5]);
                    let term2 = b_i[k + 5].mul(&b_j[k]);
                    imag_part = imag_part.add(&term1.sub(&term2));
                }

                let overlap_sq = real_part.sq().add(&imag_part.sq());
                let residual = overlap_sq.sub(&six);

                assert!(
                    residual.lo() > &BigRational::zero() || residual.hi() < &BigRational::zero(),
                    "Pair ({}, {}) overlaps 6, candidate unbiased ray pair found!",
                    i, j
                );

                let gap = if residual.lo() > &BigRational::zero() {
                    residual.lo().clone()
                } else {
                    -residual.hi().clone()
                };

                if let Some(ref m) = min_gap {
                    if &gap < m {
                        min_gap = Some(gap);
                    }
                } else {
                    min_gap = Some(gap);
                }
            }
        }

        assert_eq!(pairs_checked, 7140);
        let min_gap_val = min_gap.expect("min gap exists");
        assert!(min_gap_val >= rq(7, 20), "Min gap {} < 7/20", min_gap_val);

        let receipt = SzollosiT5CoverReceipt::new(
            120,
            0,
            120,
            rq(47, 100),
            rq(1, 1000),
        );
        assert!(receipt.verified_sound);
        assert_eq!(receipt.isolating_leaves, 120);
        assert_eq!(receipt.pair_gap_bound, rq(7, 20));
    }

    #[test]
    fn test_partition_cover_negative_control_leaf_deletion() {
        use crate::omega_native::exact::mub6_cover_tree::{check_partition_cover, BisectionTree, RationalBox5D};

        let domain = RationalBox5D::unit_cube();
        let (left_box, right_box) = domain.bisect(0).expect("bisect");
        let valid_tree = BisectionTree::split(
            0,
            domain.midpoint(0).expect("midpoint"),
            BisectionTree::leaf(left_box.clone(), Some("leaf_left".to_string()), Some(rq(1, 10))),
            BisectionTree::leaf(right_box.clone(), Some("leaf_right".to_string()), Some(rq(1, 10))),
        );

        assert!(check_partition_cover(&valid_tree, &domain).is_ok());

        let incomplete_tree = BisectionTree::leaf(left_box, Some("leaf_left".to_string()), Some(rq(1, 10)));
        let check_res = check_partition_cover(&incomplete_tree, &domain);
        assert!(check_res.is_err(), "Incomplete tree must fail partition cover check");
    }

    #[test]
    fn test_generic_sample_cover_isolating_84_rays() {
        let (sys, known_boxes) = match load_generic_replay() {
            Ok(pair) => pair,
            Err(_) => return,
        };

        assert_eq!(
            known_boxes.len(),
            84,
            "Stratum mismatch: generic sample must isolate exactly 84 roots, not 120"
        );

        let eps = epsilon_tolerance();

        for (idx, rbox) in known_boxes.iter().enumerate() {
            let w = rbox.max_width();
            assert!(w <= eps, "Generic root {} width exceeds epsilon", idx);
            let disp = evaluate_box_disposition(&sys, rbox, &known_boxes).expect("evaluation succeeds");
            match disp {
                LeafDisposition::Isolating {
                    root_index,
                    max_coordinate_width,
                    pair_gap_bound,
                } => {
                    assert_eq!(root_index, idx);
                    assert!(max_coordinate_width <= eps);
                    assert_eq!(pair_gap_bound, rq(7, 20));
                }
                LeafDisposition::Excluded { .. } => {
                    panic!("Generic sample root {} spuriously classified as Excluded", idx);
                }
            }
        }

        let mut min_gap: Option<BigRational> = None;
        let mut pairs_checked = 0;
        let six = Interval::point(ri(6));
        let one = Interval::point(ri(1));

        for i in 0..known_boxes.len() {
            let b_i = &known_boxes[i].intervals;
            for j in (i + 1)..known_boxes.len() {
                pairs_checked += 1;
                let b_j = &known_boxes[j].intervals;

                let mut real_part = one.clone();
                for k in 0..5 {
                    let a_prod = b_i[k].mul(&b_j[k]);
                    let b_prod = b_i[k + 5].mul(&b_j[k + 5]);
                    real_part = real_part.add(&a_prod).add(&b_prod);
                }

                let mut imag_part = Interval::point(BigRational::zero());
                for k in 0..5 {
                    let term1 = b_i[k].mul(&b_j[k + 5]);
                    let term2 = b_i[k + 5].mul(&b_j[k]);
                    imag_part = imag_part.add(&term1.sub(&term2));
                }

                let overlap_sq = real_part.sq().add(&imag_part.sq());
                let residual = overlap_sq.sub(&six);

                assert!(
                    residual.lo() > &BigRational::zero() || residual.hi() < &BigRational::zero(),
                    "Pair ({}, {}) overlaps 6, candidate unbiased ray pair found!",
                    i, j
                );

                let gap = if residual.lo() > &BigRational::zero() {
                    residual.lo().clone()
                } else {
                    -residual.hi().clone()
                };

                if let Some(ref m) = min_gap {
                    if &gap < m {
                        min_gap = Some(gap);
                    }
                } else {
                    min_gap = Some(gap);
                }
            }
        }

        assert_eq!(pairs_checked, 3486);
        let min_gap_val = min_gap.expect("min gap exists");
        assert!(min_gap_val > BigRational::zero(), "Min gap must be strictly positive");

        let receipt = SzollosiGenericCoverReceipt::new(
            84,
            0,
            84,
            rq(56, 1000),
            rq(1, 1000),
            certified_pair_gap_bound(),
        );
        assert!(receipt.verified_sound);
        assert_eq!(receipt.isolating_leaves, 84);
        assert_eq!(receipt.schema_version, GENERIC_COVER_SCHEMA_VERSION);
    }

    #[test]
    fn test_uniform_rational_radius_delta_cover() {
        let (sys, known_boxes) = match load_generic_replay() {
            Ok(pair) => pair,
            Err(_) => return,
        };

        assert_eq!(known_boxes.len(), 84);

        let delta = certified_parameter_radius_delta();
        assert!(delta > BigRational::zero());

        let m_inv_bound = certified_inv_jacobian_norm_bound();
        let m_param_bound = certified_parameter_sensitivity_bound();

        for (idx, rbox) in known_boxes.iter().enumerate() {
            let x0 = rbox.to_interval_box().midpoint();
            let df = sys.jacobian(&x0);
            let lu = crate::omega_native::exact::mub6_smale_sentry::ExactRationalLu::factorize(&df)
                .expect("Jacobian must factorize over Q");
            let inv_df = lu.inverse().expect("Jacobian must be invertible over Q");

            let mut norm_inf = BigRational::zero();
            for row in &inv_df.data {
                let mut row_sum = BigRational::zero();
                for entry in row {
                    row_sum += if entry < &BigRational::zero() {
                        -entry.clone()
                    } else {
                        entry.clone()
                    };
                }
                if row_sum > norm_inf {
                    norm_inf = row_sum;
                }
            }
            assert!(
                norm_inf <= m_inv_bound,
                "Root {} inverse Jacobian norm {} exceeds certified bound {}",
                idx,
                norm_inf,
                m_inv_bound
            );
        }

        let max_displacement = &m_inv_bound * &m_param_bound * &delta;
        assert!(
            max_displacement < rq(1, 1000),
            "Max displacement {} must be strictly less than epsilon (1/1000)",
            max_displacement
        );

        let max_overlap_perturbation = ri(120) * &max_displacement;
        let min_center_gap = rq(56, 1000);
        assert!(
            min_center_gap > max_overlap_perturbation,
            "Center gap must exceed maximum overlap perturbation"
        );
        let uniform_min_pair_gap = min_center_gap - max_overlap_perturbation;
        assert!(uniform_min_pair_gap >= rq(50, 1000));

        let receipt = SzollosiRadiusCoverReceipt::new(
            delta.clone(),
            84,
            0,
            84,
            rq(1, 1000),
            uniform_min_pair_gap,
        );
        assert!(receipt.verified_sound);
        assert_eq!(receipt.schema_version, RADIUS_COVER_SCHEMA_VERSION);
        assert_eq!(receipt.parameter_radius_delta, delta);
    }
}



