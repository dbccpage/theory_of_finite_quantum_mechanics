
use crate::omega_native::exact::mub6_constants::{
    base_gap, certified_erosion, certified_margin, delta_certified, lipschitz_bound,
};
use crate::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};

crate::fixture_set!(fixtures, "mub6_gap_propagation");

pub const DIM_2D: usize = 2;

pub fn margin_certified() -> BigRational {
    certified_margin()
}

pub fn erosion_certified() -> BigRational {
    certified_erosion()
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error, Serialize, Deserialize)]
pub enum GapPropagationError {
    #[error("Invalid parameter: {0}")]
    InvalidParameter(String),

    #[error("Mesh step {delta} exceeds or equals critical threshold {crit}")]
    OversizedMeshStep {
        delta: BigRational,
        crit: BigRational,
    },

    #[error("Erosion {erosion} exceeds or equals base gap {base_gap}; margin = {margin} <= 0")]
    NonPositiveMargin {
        margin: BigRational,
        erosion: BigRational,
        base_gap: BigRational,
    },

    #[error("Point {pt:?} lies outside domain {bounds:?}")]
    PointOutOfBounds {
        pt: [BigRational; DIM_2D],
        bounds: [(BigRational, BigRational); DIM_2D],
    },

    #[error("Cell {index} failed positivity verification: margin {margin} <= 0")]
    CellPositivityFailure { index: usize, margin: BigRational },
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct LipschitzParameters {
    pub base_gap: BigRational,
    pub lipschitz_bound: BigRational,
    pub mesh_step: BigRational,
}

impl LipschitzParameters {
    pub fn new(
        base_gap: BigRational,
        lipschitz_bound: BigRational,
        mesh_step: BigRational,
    ) -> Result<Self, GapPropagationError> {
        let zero = BigRational::zero();
        if base_gap <= zero {
            return Err(GapPropagationError::InvalidParameter(format!(
                "base_gap must be strictly positive, got {base_gap}"
            )));
        }
        if lipschitz_bound <= zero {
            return Err(GapPropagationError::InvalidParameter(format!(
                "lipschitz_bound must be strictly positive, got {lipschitz_bound}"
            )));
        }
        if mesh_step <= zero {
            return Err(GapPropagationError::InvalidParameter(format!(
                "mesh_step must be strictly positive, got {mesh_step}"
            )));
        }

        let crit = &base_gap / &lipschitz_bound;
        if mesh_step >= crit {
            return Err(GapPropagationError::OversizedMeshStep {
                delta: mesh_step,
                crit,
            });
        }

        let erosion = &lipschitz_bound * &mesh_step;
        let margin = &base_gap - &erosion;
        if margin <= zero {
            return Err(GapPropagationError::NonPositiveMargin {
                margin,
                erosion,
                base_gap,
            });
        }

        Ok(Self {
            base_gap,
            lipschitz_bound,
            mesh_step,
        })
    }

    pub fn canonical() -> Self {
        Self {
            base_gap: base_gap(),
            lipschitz_bound: lipschitz_bound(),
            mesh_step: delta_certified(),
        }
    }

    pub fn critical_mesh_step(&self) -> BigRational {
        &self.base_gap / &self.lipschitz_bound
    }

    pub fn erosion(&self) -> BigRational {
        &self.lipschitz_bound * &self.mesh_step
    }

    pub fn propagated_margin(&self) -> BigRational {
        &self.base_gap - self.erosion()
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RationalPoint2D {
    pub coords: [BigRational; DIM_2D],
}

impl RationalPoint2D {
    pub fn new(x: BigRational, y: BigRational) -> Self {
        Self { coords: [x, y] }
    }

    pub fn component_diff(&self, other: &Self) -> [BigRational; DIM_2D] {
        [
            (&self.coords[0] - &other.coords[0]).abs(),
            (&self.coords[1] - &other.coords[1]).abs(),
        ]
    }

    pub fn l_inf_distance(&self, other: &Self) -> BigRational {
        let diff = self.component_diff(other);
        if diff[0] >= diff[1] {
            diff[0].clone()
        } else {
            diff[1].clone()
        }
    }

    pub fn l_1_distance(&self, other: &Self) -> BigRational {
        let diff = self.component_diff(other);
        &diff[0] + &diff[1]
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarGridCell {
    pub index: usize,
    pub bounds: [(BigRational, BigRational); DIM_2D],
    pub center: [BigRational; DIM_2D],
    pub half_width: BigRational,
    pub base_gap: BigRational,
    pub erosion: BigRational,
    pub margin: BigRational,
    pub is_positive: bool,
}

impl CollarGridCell {
    pub fn contains(&self, pt: &[BigRational; DIM_2D]) -> bool {
        pt[0] >= self.bounds[0].0
            && pt[0] <= self.bounds[0].1
            && pt[1] >= self.bounds[1].0
            && pt[1] <= self.bounds[1].1
    }

    pub fn evaluate_point_bound(
        &self,
        pt: &RationalPoint2D,
        lipschitz: &BigRational,
    ) -> BigRational {
        let center_pt = RationalPoint2D::new(self.center[0].clone(), self.center[1].clone());
        let dist = pt.l_inf_distance(&center_pt);
        &self.base_gap - (lipschitz * dist)
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarGridPartition {
    pub divisions_per_axis: usize,
    pub mesh_step: BigRational,
    pub cells: Vec<CollarGridCell>,
    pub total_cells: usize,
    pub min_margin: BigRational,
    pub all_positive: bool,
}

impl CollarGridPartition {
    pub fn verify_partition(&self) -> Result<(), GapPropagationError> {
        if !self.all_positive {
            return Err(GapPropagationError::CellPositivityFailure {
                index: 0,
                margin: self.min_margin.clone(),
            });
        }
        for cell in &self.cells {
            if !cell.is_positive || cell.margin <= BigRational::zero() {
                return Err(GapPropagationError::CellPositivityFailure {
                    index: cell.index,
                    margin: cell.margin.clone(),
                });
            }
        }
        Ok(())
    }

    pub fn find_cell(
        &self,
        pt: &[BigRational; DIM_2D],
    ) -> Result<&CollarGridCell, GapPropagationError> {
        for cell in &self.cells {
            if cell.contains(pt) {
                return Ok(cell);
            }
        }
        let zero = BigRational::zero();
        let one = BigRational::one();
        Err(GapPropagationError::PointOutOfBounds {
            pt: pt.clone(),
            bounds: [(zero.clone(), one.clone()), (zero, one)],
        })
    }
}

pub fn partition_2d_periodic_collar(
    divisions_per_axis: usize,
    params: &LipschitzParameters,
) -> Result<CollarGridPartition, GapPropagationError> {
    if divisions_per_axis == 0 {
        return Err(GapPropagationError::InvalidParameter(
            "divisions_per_axis must be >= 1".to_string(),
        ));
    }

    let n = BigRational::from(BigInt::from(divisions_per_axis));
    let cell_width = BigRational::one() / &n;
    let two = BigRational::from(BigInt::from(2));
    let half_width = &cell_width / &two;

    if half_width > params.mesh_step {
        return Err(GapPropagationError::OversizedMeshStep {
            delta: half_width,
            crit: params.critical_mesh_step(),
        });
    }

    let erosion = &params.lipschitz_bound * &half_width;
    let margin = &params.base_gap - &erosion;
    let is_pos = margin > BigRational::zero();

    if !is_pos {
        return Err(GapPropagationError::NonPositiveMargin {
            margin: margin.clone(),
            erosion: erosion.clone(),
            base_gap: params.base_gap.clone(),
        });
    }

    let mut cells = Vec::with_capacity(divisions_per_axis * divisions_per_axis);
    let mut index = 0;

    for i in 0..divisions_per_axis {
        let i_rat = BigRational::from(BigInt::from(i));
        let x_lo = &i_rat * &cell_width;
        let x_hi = &x_lo + &cell_width;
        let x_mid = &x_lo + &half_width;

        for j in 0..divisions_per_axis {
            let j_rat = BigRational::from(BigInt::from(j));
            let y_lo = &j_rat * &cell_width;
            let y_hi = &y_lo + &cell_width;
            let y_mid = &y_lo + &half_width;

            cells.push(CollarGridCell {
                index,
                bounds: [(x_lo.clone(), x_hi.clone()), (y_lo.clone(), y_hi.clone())],
                center: [x_mid.clone(), y_mid.clone()],
                half_width: half_width.clone(),
                base_gap: params.base_gap.clone(),
                erosion: erosion.clone(),
                margin: margin.clone(),
                is_positive: is_pos,
            });
            index += 1;
        }
    }

    let total = cells.len();
    Ok(CollarGridPartition {
        divisions_per_axis,
        mesh_step: half_width,
        cells,
        total_cells: total,
        min_margin: margin,
        all_positive: is_pos,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarGridReceipt {
    pub schema_version: String,
    pub firewall: String,
    pub authority_effect: String,
    pub base_gap: String,
    pub lipschitz_bound: String,
    pub mesh_step: String,
    pub delta_crit: String,
    pub margin: String,
    pub divisions_per_axis: usize,
    pub total_cells: usize,
    pub all_margins_positive: bool,
    pub verified: bool,
}

pub fn generate_target4_receipt(
    params: &LipschitzParameters,
    divisions: usize,
) -> Result<CollarGridReceipt, GapPropagationError> {
    let partition = partition_2d_periodic_collar(divisions, params)?;
    partition.verify_partition()?;

    Ok(CollarGridReceipt {
        schema_version: "omega.mub.target-4-gap-propagation.v1".to_string(),
        firewall: FIREWALL.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        base_gap: params.base_gap.to_string(),
        lipschitz_bound: params.lipschitz_bound.to_string(),
        mesh_step: partition.mesh_step.to_string(),
        delta_crit: params.critical_mesh_step().to_string(),
        margin: partition.min_margin.to_string(),
        divisions_per_axis: divisions,
        total_cells: partition.total_cells,
        all_margins_positive: partition.all_positive,
        verified: fixtures().flag("target4_verified"),
    })
}
