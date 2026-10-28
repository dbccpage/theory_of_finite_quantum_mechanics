
use std::collections::BTreeSet;

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, ToPrimitive, Zero};
use serde::{Deserialize, Serialize};

use crate::native::exact::mub6_constants::{
    base_gap, certified_margin, delta_certified, lipschitz_bound,
};
use crate::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::native::exact::mub6_matrix6::{eye3, mul_mat3};
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::ri;
use engine_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge};

crate::fixture_set!(fixtures, "mub6_collar_boundary");

pub const DIM_2D: usize = 2;
pub const DIM_3D: usize = 3;

pub fn collar_margin() -> BigRational {
    certified_margin()
}

pub fn karlsson_volume_margin() -> BigRational {
    fixtures().rational("karlsson_volume_margin")
}

pub fn interface_margin() -> BigRational {
    let cm = collar_margin();
    let km = karlsson_volume_margin();
    if cm <= km {
        cm
    } else {
        km
    }
}

pub fn critical_mesh_step() -> BigRational {
    &base_gap() / &lipschitz_bound()
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error, Serialize, Deserialize)]
pub enum CollarBoundaryError {
    #[error("Invalid parameter: {0}")]
    InvalidParameter(String),

    #[error("Boundary gap detected between z={gap_lo} and z={gap_hi}")]
    BoundaryGapDetected {
        gap_lo: BigRational,
        gap_hi: BigRational,
    },

    #[error("Interface box {box_index} uncertified or non-positive margin ({margin} <= 0)")]
    UncertifiedInterfaceBox {
        box_index: usize,
        margin: BigRational,
    },

    #[error("Volume conservation mismatch: expected {expected}, actual {actual}")]
    VolumeConservationMismatch {
        expected: BigRational,
        actual: BigRational,
    },

    #[error("Interface cycle {cycle_index} has non-positive circulation: {circulation} <= 0")]
    NonPositiveCirculation {
        cycle_index: usize,
        circulation: i128,
    },

    #[error("Coboundary sum non-zero around cycle {cycle_index}: {sum}")]
    CoboundarySumNonZero { cycle_index: usize, sum: i128 },

    #[error("Non-zero duality gap for cycle {cycle_index}: phi1={phi1}, l1_norm={l1_norm}")]
    DualGapNonZero {
        cycle_index: usize,
        phi1: i128,
        l1_norm: i128,
    },

    #[error("Network simplex solver error: {0}")]
    SimplexFailure(String),
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarBoundaryBox3D {
    pub index: usize,
    pub bounds_xy: [(BigRational, BigRational); DIM_2D],
    pub z_range: (BigRational, BigRational),
    pub collar_certified: bool,
    pub collar_margin: BigRational,
    pub karlsson_certified: bool,
    pub karlsson_margin: BigRational,
    pub effective_margin: BigRational,
}

impl CollarBoundaryBox3D {
    pub fn volume(&self) -> BigRational {
        let wx = &self.bounds_xy[0].1 - &self.bounds_xy[0].0;
        let wy = &self.bounds_xy[1].1 - &self.bounds_xy[1].0;
        let wz = &self.z_range.1 - &self.z_range.0;
        &(&wx * &wy) * &wz
    }

    pub fn is_overlap(&self) -> bool {
        self.collar_certified && self.karlsson_certified
    }

    pub fn contains_point(&self, pt: &[BigRational; DIM_3D]) -> bool {
        pt[0] >= self.bounds_xy[0].0
            && pt[0] <= self.bounds_xy[0].1
            && pt[1] >= self.bounds_xy[1].0
            && pt[1] <= self.bounds_xy[1].1
            && pt[2] >= self.z_range.0
            && pt[2] <= self.z_range.1
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarBoundaryConfig {
    pub collar_max_depth: BigRational,
    pub karlsson_min_depth: BigRational,
    pub divisions_xy: usize,
}

impl CollarBoundaryConfig {
    pub fn canonical(divisions_xy: usize) -> Self {
        Self {
            collar_max_depth: delta_certified(),
            karlsson_min_depth: delta_certified(),
            divisions_xy,
        }
    }

    pub fn overlapping(divisions_xy: usize, karlsson_min_depth: BigRational) -> Self {
        Self {
            collar_max_depth: delta_certified(),
            karlsson_min_depth,
            divisions_xy,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct BoundaryOverlapPartition {
    pub divisions_xy: usize,
    pub collar_max_depth: BigRational,
    pub karlsson_min_depth: BigRational,
    pub boxes: Vec<CollarBoundaryBox3D>,
    pub total_volume: BigRational,
    pub min_margin: BigRational,
    pub overlap_box_count: usize,
    pub boundary_gap_empty: bool,
    pub all_margins_positive: bool,
}

fn depth_is_supported(depth: &BigRational) -> bool {
    depth > &BigRational::zero() && depth <= &delta_certified()
}

fn collar_margin_at(depth: &BigRational) -> BigRational {
    &base_gap() - &(&lipschitz_bound() * depth)
}

fn checked_i128_sum(values: &[i128]) -> Result<i128, CollarBoundaryError> {
    let mut acc = 0i128;
    for value in values {
        acc = acc.checked_add(*value).ok_or_else(|| {
            CollarBoundaryError::InvalidParameter("integer sum overflowed i128".to_string())
        })?;
    }
    Ok(acc)
}

fn midpoint(lo: &BigRational, hi: &BigRational) -> BigRational {
    (lo + hi) / BigRational::from_integer(BigInt::from(2))
}

fn meets_below_karlsson(box3: &CollarBoundaryBox3D, karlsson_min: &BigRational) -> bool {
    let z_lo = &box3.z_range.0;
    let z_hi = &box3.z_range.1;
    if z_hi <= z_lo {
        return false;
    }
    let below_hi = if z_hi < karlsson_min {
        z_hi.clone()
    } else {
        karlsson_min.clone()
    };
    &below_hi > z_lo
}

fn collect_box_grid_coordinates(
    boxes: &[CollarBoundaryBox3D],
    z_hi: &BigRational,
) -> Option<(Vec<BigRational>, Vec<BigRational>, Vec<BigRational>)> {
    let zero = BigRational::zero();
    let one = BigRational::one();
    if z_hi <= &zero {
        return None;
    }
    let mut xs = BTreeSet::from([zero.clone(), one.clone()]);
    let mut ys = BTreeSet::from([zero.clone(), one.clone()]);
    let mut zs = BTreeSet::from([zero, z_hi.clone()]);
    for box3 in boxes {
        if box3.bounds_xy[0].1 < box3.bounds_xy[0].0
            || box3.bounds_xy[1].1 < box3.bounds_xy[1].0
            || box3.z_range.1 < box3.z_range.0
        {
            return None;
        }
        xs.insert(box3.bounds_xy[0].0.clone());
        xs.insert(box3.bounds_xy[0].1.clone());
        ys.insert(box3.bounds_xy[1].0.clone());
        ys.insert(box3.bounds_xy[1].1.clone());
        zs.insert(box3.z_range.0.clone());
        zs.insert(box3.z_range.1.clone());
    }
    Some((
        xs.into_iter().collect(),
        ys.into_iter().collect(),
        zs.into_iter().collect(),
    ))
}

fn count_boxes_containing_point(
    boxes: &[CollarBoundaryBox3D],
    point: &[BigRational; DIM_3D],
) -> usize {
    let mut hits = 0usize;
    for box3 in boxes {
        if box3.contains_point(point) {
            hits += 1;
        }
    }
    hits
}

fn point_inside_target_prism(point: &[BigRational; DIM_3D], z_hi: &BigRational) -> bool {
    let zero = BigRational::zero();
    let one = BigRational::one();
    let xy_ok = point[0] >= zero && point[0] <= one && point[1] >= zero && point[1] <= one;
    xy_ok && point[2] >= zero && &point[2] <= z_hi
}

fn check_grid_cell_coverage(
    boxes: &[CollarBoundaryBox3D],
    point: &[BigRational; DIM_3D],
    z_hi: &BigRational,
    saw_target: &mut bool,
) -> bool {
    let inside = point_inside_target_prism(point, z_hi);
    let hits = count_boxes_containing_point(boxes, point);
    if inside {
        *saw_target = true;
        hits == 1
    } else {
        hits == 0
    }
}

fn check_yz_slice_coverage(
    boxes: &[CollarBoundaryBox3D],
    xm: &BigRational,
    ys: &[BigRational],
    zs: &[BigRational],
    z_hi: &BigRational,
    saw_target: &mut bool,
) -> bool {
    for iy in 0..ys.len().saturating_sub(1) {
        if ys[iy + 1] <= ys[iy] {
            continue;
        }
        let ym = midpoint(&ys[iy], &ys[iy + 1]);
        for iz in 0..zs.len().saturating_sub(1) {
            if zs[iz + 1] <= zs[iz] {
                continue;
            }
            let zm = midpoint(&zs[iz], &zs[iz + 1]);
            let point = [xm.clone(), ym.clone(), zm];
            if !check_grid_cell_coverage(boxes, &point, z_hi, saw_target) {
                return false;
            }
        }
    }
    true
}

fn rectangle_partition_holds(boxes: &[CollarBoundaryBox3D], z_hi: &BigRational) -> bool {
    let Some((xs, ys, zs)) = collect_box_grid_coordinates(boxes, z_hi) else {
        return false;
    };
    let mut saw_target = false;
    for ix in 0..xs.len().saturating_sub(1) {
        if xs[ix + 1] <= xs[ix] {
            continue;
        }
        let xm = midpoint(&xs[ix], &xs[ix + 1]);
        if !check_yz_slice_coverage(boxes, &xm, &ys, &zs, z_hi, &mut saw_target) {
            return false;
        }
    }
    saw_target
}

impl BoundaryOverlapPartition {
    fn verify_partition_depths(&self) -> Result<(), CollarBoundaryError> {
        let supported = depth_is_supported(&self.collar_max_depth)
            && depth_is_supported(&self.karlsson_min_depth);
        let gap_empty = supported && self.collar_max_depth >= self.karlsson_min_depth;
        if self.boundary_gap_empty != gap_empty || !gap_empty {
            if !supported {
                return Err(CollarBoundaryError::InvalidParameter(format!(
                    "depth is outside the certified Lipschitz radius {}",
                    delta_certified()
                )));
            }
            return Err(CollarBoundaryError::BoundaryGapDetected {
                gap_lo: self.collar_max_depth.clone(),
                gap_hi: self.karlsson_min_depth.clone(),
            });
        }
        Ok(())
    }

    fn verify_single_partition_box(
        &self,
        box3: &CollarBoundaryBox3D,
        collar_m: &BigRational,
        interface_m: &BigRational,
    ) -> Result<BigRational, CollarBoundaryError> {
        let volume = box3.volume();
        if volume <= BigRational::zero() {
            return Err(CollarBoundaryError::InvalidParameter(format!(
                "box {} does not have positive volume",
                box3.index
            )));
        }
        let below = meets_below_karlsson(box3, &self.karlsson_min_depth);
        let certs_valid = if below {
            !box3.karlsson_certified && box3.collar_certified
        } else {
            box3.karlsson_certified && box3.collar_certified
        };
        let applicable = if below { collar_m } else { interface_m };
        if !certs_valid || &box3.effective_margin != applicable {
            return Err(CollarBoundaryError::UncertifiedInterfaceBox {
                box_index: box3.index,
                margin: box3.effective_margin.clone(),
            });
        }
        Ok(volume)
    }

    fn verify_partition_boxes_and_accumulate(
        &self,
        collar_m: &BigRational,
        interface_m: &BigRational,
    ) -> Result<(BigRational, BigRational, usize), CollarBoundaryError> {
        let mut actual_volume = BigRational::zero();
        let mut min_margin: Option<BigRational> = None;
        let mut overlap_count = 0usize;
        for box3 in &self.boxes {
            let volume = self.verify_single_partition_box(box3, collar_m, interface_m)?;
            actual_volume += &volume;
            if box3.is_overlap() {
                overlap_count += 1;
            }
            min_margin = Some(match min_margin {
                Some(current) if current <= box3.effective_margin => current,
                _ => box3.effective_margin.clone(),
            });
        }
        Ok((
            actual_volume,
            min_margin.unwrap_or_else(BigRational::zero),
            overlap_count,
        ))
    }

    fn verify_partition_summary_totals(
        &self,
        expected_volume: BigRational,
        actual_volume: BigRational,
        min_margin: BigRational,
        overlap_count: usize,
    ) -> Result<(), CollarBoundaryError> {
        let all_positive = min_margin > BigRational::zero();
        if self.total_volume != actual_volume || actual_volume != expected_volume {
            return Err(CollarBoundaryError::VolumeConservationMismatch {
                expected: expected_volume,
                actual: actual_volume,
            });
        }
        if self.min_margin != min_margin
            || self.all_margins_positive != all_positive
            || !all_positive
        {
            return Err(CollarBoundaryError::UncertifiedInterfaceBox {
                box_index: 0,
                margin: self.min_margin.clone(),
            });
        }
        if self.overlap_box_count != overlap_count {
            return Err(CollarBoundaryError::InvalidParameter(
                "overlap count does not match the boxes".to_string(),
            ));
        }
        if !rectangle_partition_holds(&self.boxes, &self.collar_max_depth) {
            return Err(CollarBoundaryError::VolumeConservationMismatch {
                expected: expected_volume,
                actual: self.total_volume.clone(),
            });
        }
        Ok(())
    }

    pub fn verify_partition(&self) -> Result<(), CollarBoundaryError> {
        let zero = BigRational::zero();
        self.verify_partition_depths()?;

        let expected_volume = self.collar_max_depth.clone();
        let collar_m = collar_margin_at(&self.collar_max_depth);
        let karlsson_m = karlsson_volume_margin();
        let interface_m = if collar_m <= karlsson_m {
            collar_m.clone()
        } else {
            karlsson_m.clone()
        };
        if collar_m <= zero {
            return Err(CollarBoundaryError::InvalidParameter(format!(
                "collar margin {collar_m} is not positive"
            )));
        }
        if self.boxes.is_empty() {
            return Err(CollarBoundaryError::VolumeConservationMismatch {
                expected: expected_volume,
                actual: zero,
            });
        }

        let (actual_volume, min_margin, overlap_count) =
            self.verify_partition_boxes_and_accumulate(&collar_m, &interface_m)?;
        self.verify_partition_summary_totals(
            expected_volume,
            actual_volume,
            min_margin,
            overlap_count,
        )
    }

    pub fn find_box(&self, pt: &[BigRational; DIM_3D]) -> Option<&CollarBoundaryBox3D> {
        self.boxes.iter().find(|b| b.contains_point(pt))
    }
}

fn validate_boundary_overlap_config(
    config: &CollarBoundaryConfig,
) -> Result<BigRational, CollarBoundaryError> {
    if config.divisions_xy == 0 {
        return Err(CollarBoundaryError::InvalidParameter(
            "divisions_xy must be >= 1".to_string(),
        ));
    }
    let zero = BigRational::zero();
    if config.collar_max_depth <= zero {
        return Err(CollarBoundaryError::InvalidParameter(
            "collar_max_depth must be strictly positive".to_string(),
        ));
    }
    if config.karlsson_min_depth <= zero {
        return Err(CollarBoundaryError::InvalidParameter(
            "karlsson_min_depth must be strictly positive".to_string(),
        ));
    }
    if config.collar_max_depth < config.karlsson_min_depth {
        return Err(CollarBoundaryError::BoundaryGapDetected {
            gap_lo: config.collar_max_depth.clone(),
            gap_hi: config.karlsson_min_depth.clone(),
        });
    }
    if !depth_is_supported(&config.collar_max_depth)
        || !depth_is_supported(&config.karlsson_min_depth)
    {
        return Err(CollarBoundaryError::InvalidParameter(format!(
            "depth is outside the certified Lipschitz radius {}",
            delta_certified()
        )));
    }
    let cm = collar_margin_at(&config.collar_max_depth);
    if cm <= zero {
        return Err(CollarBoundaryError::InvalidParameter(format!(
            "collar margin {cm} is not positive at the requested depth"
        )));
    }
    Ok(cm)
}

fn push_cell_boundary_boxes(
    boxes: &mut Vec<CollarBoundaryBox3D>,
    index: &mut usize,
    overlap_count: &mut usize,
    config: &CollarBoundaryConfig,
    bounds_xy: [(BigRational, BigRational); 2],
    cm: &BigRational,
    km: &BigRational,
    if_margin: &BigRational,
) {
    let zero = BigRational::zero();
    if config.karlsson_min_depth < config.collar_max_depth {
        boxes.push(CollarBoundaryBox3D {
            index: *index,
            bounds_xy: bounds_xy.clone(),
            z_range: (zero.clone(), config.karlsson_min_depth.clone()),
            collar_certified: fixtures().flag("collar_layer_certified"),
            collar_margin: cm.clone(),
            karlsson_certified: false,
            karlsson_margin: zero,
            effective_margin: cm.clone(),
        });
        *index += 1;

        boxes.push(CollarBoundaryBox3D {
            index: *index,
            bounds_xy,
            z_range: (
                config.karlsson_min_depth.clone(),
                config.collar_max_depth.clone(),
            ),
            collar_certified: fixtures().flag("collar_layer_certified"),
            collar_margin: cm.clone(),
            karlsson_certified: fixtures().flag("overlap_layer_karlsson_certified"),
            karlsson_margin: km.clone(),
            effective_margin: if_margin.clone(),
        });
        *index += 1;
        *overlap_count += 1;
    } else {
        boxes.push(CollarBoundaryBox3D {
            index: *index,
            bounds_xy,
            z_range: (zero.clone(), config.collar_max_depth.clone()),
            collar_certified: fixtures().flag("collar_layer_certified"),
            collar_margin: cm.clone(),
            karlsson_certified: false,
            karlsson_margin: zero,
            effective_margin: cm.clone(),
        });
        *index += 1;
    }
}

pub fn evaluate_boundary_overlap(
    config: &CollarBoundaryConfig,
) -> Result<BoundaryOverlapPartition, CollarBoundaryError> {
    let cm = validate_boundary_overlap_config(config)?;
    let n = BigRational::from(BigInt::from(config.divisions_xy));
    let cell_width = BigRational::one() / &n;
    let km = karlsson_volume_margin();
    let if_margin = if cm <= km { cm.clone() } else { km.clone() };

    let mut boxes = Vec::new();
    let mut index = 0;
    let mut overlap_count = 0;

    for i in 0..config.divisions_xy {
        let x_lo = BigRational::from(BigInt::from(i)) * &cell_width;
        let x_hi = &x_lo + &cell_width;
        for j in 0..config.divisions_xy {
            let y_lo = BigRational::from(BigInt::from(j)) * &cell_width;
            let y_hi = &y_lo + &cell_width;
            push_cell_boundary_boxes(
                &mut boxes,
                &mut index,
                &mut overlap_count,
                config,
                [(x_lo.clone(), x_hi.clone()), (y_lo, y_hi)],
                &cm,
                &km,
                &if_margin,
            );
        }
    }

    let mut total_vol = BigRational::zero();
    let mut min_m = cm;
    for b in &boxes {
        total_vol = &total_vol + &b.volume();
        if b.effective_margin < min_m {
            min_m = b.effective_margin.clone();
        }
    }

    let partition = BoundaryOverlapPartition {
        divisions_xy: config.divisions_xy,
        collar_max_depth: config.collar_max_depth.clone(),
        karlsson_min_depth: config.karlsson_min_depth.clone(),
        boxes,
        total_volume: total_vol,
        min_margin: min_m.clone(),
        overlap_box_count: overlap_count,
        boundary_gap_empty: true,
        all_margins_positive: min_m > BigRational::zero(),
    };

    partition.verify_partition()?;
    Ok(partition)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct InterfaceTransition {
    pub from_chart: usize,
    pub to_chart: usize,
    pub matrix: [[Cyc24; 3]; 3],
    pub edge_defect: BigRational,
}

impl InterfaceTransition {
    pub fn new(from: usize, to: usize, matrix: [[Cyc24; 3]; 3], defect: BigRational) -> Self {
        Self {
            from_chart: from,
            to_chart: to,
            matrix,
            edge_defect: defect,
        }
    }

    pub fn phase_transition(
        from: usize,
        to: usize,
        phi1: Cyc24,
        phi2: Cyc24,
        defect: BigRational,
    ) -> Self {
        let zero = Cyc24::zero();
        let one = Cyc24::rat(ri(1));
        let matrix = [
            [one, zero.clone(), zero.clone()],
            [zero.clone(), phi1, zero.clone()],
            [zero.clone(), zero, phi2],
        ];
        Self {
            from_chart: from,
            to_chart: to,
            matrix,
            edge_defect: defect,
        }
    }

    pub fn permutation_transition(
        from: usize,
        to: usize,
        perm: [usize; 3],
        defect: BigRational,
    ) -> Self {
        let zero = Cyc24::zero();
        let one = Cyc24::rat(ri(1));
        let mut matrix = [
            [zero.clone(), zero.clone(), zero.clone()],
            [zero.clone(), zero.clone(), zero.clone()],
            [zero.clone(), zero.clone(), zero],
        ];
        for (j, &target_row) in perm.iter().enumerate() {
            matrix[target_row][j] = one.clone();
        }
        Self {
            from_chart: from,
            to_chart: to,
            matrix,
            edge_defect: defect,
        }
    }

    pub fn identity(from: usize, to: usize, defect: BigRational) -> Self {
        Self {
            from_chart: from,
            to_chart: to,
            matrix: eye3(),
            edge_defect: defect,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct InterfaceCycle {
    pub index: usize,
    pub name: String,
    pub transitions: [InterfaceTransition; 3],
}

impl InterfaceCycle {
    pub fn new(index: usize, name: String, transitions: [InterfaceTransition; 3]) -> Self {
        Self {
            index,
            name,
            transitions,
        }
    }

    pub fn canonical(index: usize) -> Self {
        let g01 = InterfaceTransition::phase_transition(
            0,
            1,
            Cyc24::zeta24(8),
            Cyc24::zeta24(16),
            collar_margin(),
        );
        let g12 = InterfaceTransition::phase_transition(
            1,
            2,
            Cyc24::zeta24(16),
            Cyc24::zeta24(8),
            interface_margin(),
        );
        let g20 = InterfaceTransition::identity(2, 0, karlsson_volume_margin());
        Self::new(
            index,
            format!("canonical_interface_cycle_{index}"),
            [g01, g12, g20],
        )
    }

    pub fn twisted(index: usize) -> Self {
        let g01 = InterfaceTransition::permutation_transition(0, 1, [1, 0, 2], collar_margin());
        let g12 = InterfaceTransition::permutation_transition(1, 2, [0, 2, 1], interface_margin());
        let g20 = InterfaceTransition::identity(2, 0, karlsson_volume_margin());
        Self::new(
            index,
            format!("twisted_interface_cycle_{index}"),
            [g01, g12, g20],
        )
    }

    pub fn chained_holonomy(&self) -> [[Cyc24; 3]; 3] {
        let t01 = &self.transitions[0].matrix;
        let t12 = &self.transitions[1].matrix;
        let t20 = &self.transitions[2].matrix;
        mul_mat3(&mul_mat3(t01, t12), t20)
    }

    pub fn is_cocycle_trivial(&self) -> bool {
        let w = self.chained_holonomy();
        let eye = eye3();
        for i in 0..3 {
            for j in 0..3 {
                if w[i][j] != eye[i][j] {
                    return false;
                }
            }
        }
        true
    }

    pub fn build_boundary_and_cochain(
        &self,
        scale: i128,
    ) -> Result<(Boundary1, Vec<i128>), CollarBoundaryError> {
        if scale <= 0 {
            return Err(CollarBoundaryError::InvalidParameter(
                "scale must be strictly positive".to_string(),
            ));
        }
        let boundary = Boundary1 {
            num_vertices: 3,
            edges: vec![
                BoundaryEdge {
                    tail: 0,
                    head: 1,
                    weight: 1,
                },
                BoundaryEdge {
                    tail: 1,
                    head: 2,
                    weight: 1,
                },
                BoundaryEdge {
                    tail: 2,
                    head: 0,
                    weight: 1,
                },
            ],
        };

        let scale_rat = BigRational::from_integer(BigInt::from(scale));
        let mut omega = Vec::with_capacity(3);
        for t in &self.transitions {
            let scaled = &t.edge_defect * &scale_rat;
            if !scaled.denom().is_one() {
                return Err(CollarBoundaryError::InvalidParameter(format!(
                    "scaled edge defect {scaled} is not an integer"
                )));
            }
            let integer = scaled.to_integer();
            let coefficient = integer.to_i128().ok_or_else(|| {
                CollarBoundaryError::InvalidParameter(format!(
                    "scaled edge defect {integer} does not fit in i128"
                ))
            })?;
            omega.push(coefficient);
        }

        Ok((boundary, omega))
    }

    fn sum_coboundary_steps(
        edges: &[BoundaryEdge],
        vertex_potential: &[i128],
    ) -> Result<i128, CollarBoundaryError> {
        let mut d_alpha_sum = 0i128;
        for edge in edges {
            let step = vertex_potential[edge.head]
                .checked_sub(vertex_potential[edge.tail])
                .ok_or_else(|| {
                    CollarBoundaryError::InvalidParameter(
                        "coboundary difference overflowed i128".to_string(),
                    )
                })?;
            d_alpha_sum = d_alpha_sum.checked_add(step).ok_or_else(|| {
                CollarBoundaryError::InvalidParameter("coboundary sum overflowed i128".to_string())
            })?;
        }
        Ok(d_alpha_sum)
    }

    pub fn verify_circulation(
        &self,
        scale: i128,
    ) -> Result<InterfaceCycleCirculationCert, CollarBoundaryError> {
        let (boundary, omega) = self.build_boundary_and_cochain(scale)?;
        let phi1_sol = solve_phi1(&boundary, &omega)
            .map_err(|e| CollarBoundaryError::SimplexFailure(format!("{e:?}")))?;

        let net_circulation = checked_i128_sum(&omega)?;
        if net_circulation <= 0 {
            return Err(CollarBoundaryError::NonPositiveCirculation {
                cycle_index: self.index,
                circulation: net_circulation,
            });
        }

        let d_alpha_sum = Self::sum_coboundary_steps(&boundary.edges, &phi1_sol.vertex_potential)?;
        if d_alpha_sum != 0 {
            return Err(CollarBoundaryError::CoboundarySumNonZero {
                cycle_index: self.index,
                sum: d_alpha_sum,
            });
        }

        let dual_gap_zero = phi1_sol.verified_phi1().is_some();
        if !dual_gap_zero {
            return Err(CollarBoundaryError::SimplexFailure(
                "missing canonical Phi1 replay".into(),
            ));
        }

        let certified = phi1_sol.objective >= net_circulation && net_circulation > 0;

        Ok(InterfaceCycleCirculationCert {
            cycle_index: self.index,
            cycle_name: self.name.clone(),
            is_cocycle_trivial: self.is_cocycle_trivial(),
            edge_cochain: omega,
            net_circulation,
            phi1_objective: phi1_sol.objective,
            coboundary_sum: d_alpha_sum,
            dual_gap_zero,
            circulation_conserved: d_alpha_sum == 0,
            certified,
        })
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct InterfaceCycleCirculationCert {
    pub cycle_index: usize,
    pub cycle_name: String,
    pub is_cocycle_trivial: bool,
    pub edge_cochain: Vec<i128>,
    pub net_circulation: i128,
    pub phi1_objective: i128,
    pub coboundary_sum: i128,
    pub dual_gap_zero: bool,
    pub circulation_conserved: bool,
    pub certified: bool,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct InterfaceCycleChain {
    pub cycles: Vec<InterfaceCycle>,
}

impl InterfaceCycleChain {
    pub fn new(cycles: Vec<InterfaceCycle>) -> Self {
        Self { cycles }
    }

    pub fn canonical_chain(count: usize) -> Self {
        let mut cycles = Vec::with_capacity(count);
        for idx in 0..count {
            cycles.push(InterfaceCycle::canonical(idx));
        }
        Self { cycles }
    }

    pub fn verify_all(
        &self,
        scale: i128,
    ) -> Result<Vec<InterfaceCycleCirculationCert>, CollarBoundaryError> {
        let mut certs = Vec::with_capacity(self.cycles.len());
        for cycle in &self.cycles {
            let cert = cycle.verify_circulation(scale)?;
            certs.push(cert);
        }
        Ok(certs)
    }

    pub fn compound_holonomy(&self) -> [[Cyc24; 3]; 3] {
        let mut w = eye3();
        for cycle in &self.cycles {
            let h = cycle.chained_holonomy();
            w = mul_mat3(&w, &h);
        }
        w
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarBoundaryReceipt {
    pub schema_version: String,
    pub firewall: String,
    pub authority_effect: String,
    pub base_gap: String,
    pub lipschitz_bound: String,
    pub mesh_step: String,
    pub collar_margin: String,
    pub karlsson_volume_margin: String,
    pub interface_margin: String,
    pub boundary_depth: String,
    pub overlap_region_certified: bool,
    pub boundary_gap_empty: bool,
    pub num_interface_boxes: usize,
    pub total_interface_volume: String,
    pub num_interface_cycles: usize,
    pub all_cycles_positive_circulation: bool,
    pub min_cycle_phi1: i128,
    pub coboundary_sum_zero: bool,
    pub dual_gap_zero: bool,
    pub verified: bool,
}

impl CollarBoundaryReceipt {
    pub fn to_json_string(&self) -> Result<String, serde_json::Error> {
        serde_json::to_string_pretty(self)
    }

    pub fn from_json_str(s: &str) -> Result<Self, serde_json::Error> {
        serde_json::from_str(s)
    }
}

fn summarize_cycle_certs(
    certs: &[InterfaceCycleCirculationCert],
) -> (i128, bool, bool, bool) {
    let mut min_phi1 = i128::MAX;
    let mut all_pos = true;
    let mut all_dual_zero = true;
    let mut all_coboundary_zero = true;

    for c in certs {
        if c.phi1_objective < min_phi1 {
            min_phi1 = c.phi1_objective;
        }
        if !c.certified || c.net_circulation <= 0 {
            all_pos = false;
        }
        if !c.dual_gap_zero {
            all_dual_zero = false;
        }
        if !c.circulation_conserved || c.coboundary_sum != 0 {
            all_coboundary_zero = false;
        }
    }
    (min_phi1, all_pos, all_dual_zero, all_coboundary_zero)
}

pub fn certify_collar_boundary_overlap(
    divisions_xy: usize,
    num_cycles: usize,
    scale: i128,
) -> Result<CollarBoundaryReceipt, CollarBoundaryError> {
    if num_cycles == 0 {
        return Err(CollarBoundaryError::InvalidParameter(
            "num_cycles must be at least 1".to_string(),
        ));
    }
    let config = CollarBoundaryConfig::canonical(divisions_xy);
    let partition = evaluate_boundary_overlap(&config)?;

    let chain = InterfaceCycleChain::canonical_chain(num_cycles);
    let certs = chain.verify_all(scale)?;
    if certs.is_empty() {
        return Err(CollarBoundaryError::InvalidParameter(
            "no interface cycles were checked".to_string(),
        ));
    }

    let (min_phi1, all_pos, all_dual_zero, all_coboundary_zero) = summarize_cycle_certs(&certs);
    let partition_ok = partition.boundary_gap_empty && partition.all_margins_positive;
    let verified = partition_ok && all_pos && all_dual_zero && all_coboundary_zero;

    Ok(CollarBoundaryReceipt {
        schema_version: "omega.mub.target-a8-collar-boundary.v1".to_string(),
        firewall: FIREWALL.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        base_gap: base_gap().to_string(),
        lipschitz_bound: lipschitz_bound().to_string(),
        mesh_step: delta_certified().to_string(),
        collar_margin: collar_margin().to_string(),
        karlsson_volume_margin: karlsson_volume_margin().to_string(),
        interface_margin: interface_margin().to_string(),
        boundary_depth: delta_certified().to_string(),
        overlap_region_certified: partition.overlap_box_count > 0 && partition.all_margins_positive,
        boundary_gap_empty: partition.boundary_gap_empty,
        num_interface_boxes: partition.boxes.len(),
        total_interface_volume: partition.total_volume.to_string(),
        num_interface_cycles: num_cycles,
        all_cycles_positive_circulation: all_pos,
        min_cycle_phi1: min_phi1,
        coboundary_sum_zero: all_coboundary_zero,
        dual_gap_zero: all_dual_zero,
        verified,
    })
}
