
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use crate::native::exact::mub6_constants::{base_gap, delta_certified, lipschitz_bound};
use crate::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use engine_number_theory::rational::rq;
use engine_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge, Phi1Solution};

pub const DIM_2D: usize = 2;

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error, Serialize, Deserialize)]
pub enum CollarCoverError {
    #[error("Invalid dimension {0}: must be strictly less than 2")]
    InvalidDimension(usize),

    #[error("Invalid interval for dimension {dim}: lo ({lo}) >= hi ({hi})")]
    InvalidInterval {
        dim: usize,
        lo: BigRational,
        hi: BigRational,
    },

    #[error("Cut out of bounds for dimension {dim}: cut ({cut}) is not strictly interior to ({lo}, {hi})")]
    CutOutOfBounds {
        dim: usize,
        cut: BigRational,
        lo: BigRational,
        hi: BigRational,
    },

    #[error("Box geometry mismatch: expected {expected:?}, got {actual:?}")]
    BoxMismatch {
        expected: Box<RationalBox2D>,
        actual: Box<RationalBox2D>,
    },

    #[error(
        "Volume conservation mismatch: expected domain area {expected}, total leaf area {actual}"
    )]
    AreaMismatch {
        expected: BigRational,
        actual: BigRational,
    },

    #[error("Leaf box margin is non-positive ({margin} <= 0)")]
    NonPositiveMargin { margin: BigRational },

    #[error("Network simplex error: {0}")]
    SimplexFailure(String),
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct RationalBox2D {
    pub bounds: [(BigRational, BigRational); DIM_2D],
}

impl RationalBox2D {
    pub fn unit_square() -> Self {
        let zero = BigRational::zero();
        let one = BigRational::one();
        Self {
            bounds: [(zero.clone(), one.clone()), (zero, one)],
        }
    }

    pub fn new(bounds: [(BigRational, BigRational); DIM_2D]) -> Result<Self, CollarCoverError> {
        for j in 0..DIM_2D {
            if bounds[j].0 >= bounds[j].1 {
                return Err(CollarCoverError::InvalidInterval {
                    dim: j,
                    lo: bounds[j].0.clone(),
                    hi: bounds[j].1.clone(),
                });
            }
        }
        Ok(Self { bounds })
    }

    pub fn contains_point(&self, pt: &[BigRational; DIM_2D]) -> bool {
        for j in 0..DIM_2D {
            let (ref lo, ref hi) = self.bounds[j];
            if &pt[j] < lo || &pt[j] > hi {
                return false;
            }
        }
        true
    }

    pub fn radius(&self) -> BigRational {
        let two = rq(2, 1);
        self.bounds
            .iter()
            .map(|(lo, hi)| (hi - lo) / &two)
            .max()
            .expect("a 2D box has two intervals")
    }

    pub fn area(&self) -> BigRational {
        let w0 = &self.bounds[0].1 - &self.bounds[0].0;
        let w1 = &self.bounds[1].1 - &self.bounds[1].0;
        w0 * w1
    }

    pub fn subdivide(
        &self,
        dim: usize,
        cut: &BigRational,
    ) -> Result<(Self, Self), CollarCoverError> {
        if dim >= DIM_2D {
            return Err(CollarCoverError::InvalidDimension(dim));
        }
        let (ref lo, ref hi) = self.bounds[dim];
        if cut <= lo || cut >= hi {
            return Err(CollarCoverError::CutOutOfBounds {
                dim,
                cut: cut.clone(),
                lo: lo.clone(),
                hi: hi.clone(),
            });
        }
        let mut left_bounds = self.bounds.clone();
        left_bounds[dim].1 = cut.clone();

        let mut right_bounds = self.bounds.clone();
        right_bounds[dim].0 = cut.clone();

        Ok((
            Self {
                bounds: left_bounds,
            },
            Self {
                bounds: right_bounds,
            },
        ))
    }
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum CollarBisectionTree {
    Leaf(RationalBox2D),
    Split {
        dim: usize,
        cut: BigRational,
        left: Box<CollarBisectionTree>,
        right: Box<CollarBisectionTree>,
    },
}

impl CollarBisectionTree {
    pub fn leaves(&self) -> Vec<RationalBox2D> {
        let mut result = Vec::new();
        self.collect_leaves(&mut result);
        result
    }

    fn collect_leaves(&self, acc: &mut Vec<RationalBox2D>) {
        match self {
            CollarBisectionTree::Leaf(b) => acc.push(b.clone()),
            CollarBisectionTree::Split { left, right, .. } => {
                left.collect_leaves(acc);
                right.collect_leaves(acc);
            }
        }
    }

    pub fn total_area(&self) -> BigRational {
        self.leaves()
            .iter()
            .fold(BigRational::zero(), |acc, b| acc + b.area())
    }

    pub fn verify_partition_cover(&self, domain: &RationalBox2D) -> Result<(), CollarCoverError> {
        match self {
            CollarBisectionTree::Leaf(b) => {
                if b != domain {
                    return Err(CollarCoverError::BoxMismatch {
                        expected: Box::new(domain.clone()),
                        actual: Box::new(b.clone()),
                    });
                }
                Ok(())
            }
            CollarBisectionTree::Split {
                dim,
                cut,
                left,
                right,
            } => {
                let (left_domain, right_domain) = domain.subdivide(*dim, cut)?;
                left.verify_partition_cover(&left_domain)?;
                right.verify_partition_cover(&right_domain)?;
                Ok(())
            }
        }
    }

    pub fn verify_volume_conservation(
        &self,
        expected: &BigRational,
    ) -> Result<(), CollarCoverError> {
        let actual = self.total_area();
        if &actual != expected {
            return Err(CollarCoverError::AreaMismatch {
                expected: expected.clone(),
                actual,
            });
        }
        Ok(())
    }
}

pub fn sample_quadrant_tree() -> CollarBisectionTree {
    let half = rq(1, 2);
    let unit = RationalBox2D::unit_square();

    let (left_d0, right_d0) = unit.subdivide(0, &half).unwrap();
    let (b_ll, b_lr) = left_d0.subdivide(1, &half).unwrap();
    let (b_rl, b_rr) = right_d0.subdivide(1, &half).unwrap();

    CollarBisectionTree::Split {
        dim: 0,
        cut: half.clone(),
        left: Box::new(CollarBisectionTree::Split {
            dim: 1,
            cut: half.clone(),
            left: Box::new(CollarBisectionTree::Leaf(b_ll)),
            right: Box::new(CollarBisectionTree::Leaf(b_lr)),
        }),
        right: Box::new(CollarBisectionTree::Split {
            dim: 1,
            cut: half,
            left: Box::new(CollarBisectionTree::Leaf(b_rl)),
            right: Box::new(CollarBisectionTree::Leaf(b_rr)),
        }),
    }
}

pub fn build_uniform_dyadic_tree(depth: usize) -> CollarBisectionTree {
    fn recurse(
        domain: RationalBox2D,
        current_depth: usize,
        max_depth: usize,
    ) -> CollarBisectionTree {
        if current_depth >= max_depth {
            return CollarBisectionTree::Leaf(domain);
        }
        let dim = current_depth % DIM_2D;
        let cut = (&domain.bounds[dim].0 + &domain.bounds[dim].1) / rq(2, 1);
        let (left_dom, right_dom) = domain.subdivide(dim, &cut).unwrap();
        CollarBisectionTree::Split {
            dim,
            cut,
            left: Box::new(recurse(left_dom, current_depth + 1, max_depth)),
            right: Box::new(recurse(right_dom, current_depth + 1, max_depth)),
        }
    }
    recurse(RationalBox2D::unit_square(), 0, depth)
}

pub fn evaluate_collar_barrier_margin(
    slice_floor: &BigRational,
    lipschitz: &BigRational,
    delta: &BigRational,
) -> Result<BigRational, CollarCoverError> {
    if slice_floor <= &BigRational::zero()
        || lipschitz <= &BigRational::zero()
        || delta <= &BigRational::zero()
    {
        return Err(CollarCoverError::NonPositiveMargin {
            margin: BigRational::zero(),
        });
    }
    let erosion = lipschitz * delta;
    let margin = slice_floor - &erosion;
    if margin <= BigRational::zero() {
        return Err(CollarCoverError::NonPositiveMargin { margin });
    }
    Ok(margin)
}

pub fn standard_collar_barrier_margin() -> BigRational {
    evaluate_collar_barrier_margin(&base_gap(), &lipschitz_bound(), &delta_certified())
        .expect("standard collar barrier margin must be positive")
}

pub fn collar_cell_margin(cell: &RationalBox2D) -> BigRational {
    base_gap() - lipschitz_bound() * cell.radius()
}

pub fn collar_certification_depth(max_depth: usize) -> Option<usize> {
    (0..=max_depth).find(|&depth| {
        generate_collar_cover_report(&build_uniform_dyadic_tree(depth)).all_margins_positive
    })
}

pub fn solve_collar_cycle_circulation(
    weights: &[i128; 3],
    omega: &[i128; 3],
) -> Result<Phi1Solution, CollarCoverError> {
    let boundary = Boundary1 {
        num_vertices: 3,
        edges: vec![
            BoundaryEdge {
                tail: 0,
                head: 1,
                weight: weights[0],
            },
            BoundaryEdge {
                tail: 1,
                head: 2,
                weight: weights[1],
            },
            BoundaryEdge {
                tail: 2,
                head: 0,
                weight: weights[2],
            },
        ],
    };
    solve_phi1(&boundary, omega).map_err(|e| CollarCoverError::SimplexFailure(e.to_string()))
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarCellCertificate {
    pub box_bounds: [(String, String); DIM_2D],
    pub area: String,
    pub obstruction_type: String,
    pub margin: String,
    pub certified: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarPartitionCoverReport {
    pub schema_version: String,
    pub scope: String,
    pub authority_effect: String,
    pub firewall: String,
    pub total_leaves: usize,
    pub total_area: String,
    pub area_conserved: bool,
    pub all_margins_positive: bool,
    pub min_margin: String,
    pub certificates: Vec<CollarCellCertificate>,
}

pub fn generate_collar_cover_report(tree: &CollarBisectionTree) -> CollarPartitionCoverReport {
    let leaves = tree.leaves();
    let total_area = tree.total_area();

    let certificates: Vec<CollarCellCertificate> = leaves
        .iter()
        .map(|b| {
            let margin = collar_cell_margin(b);
            CollarCellCertificate {
                box_bounds: [
                    (b.bounds[0].0.to_string(), b.bounds[0].1.to_string()),
                    (b.bounds[1].0.to_string(), b.bounds[1].1.to_string()),
                ],
                area: b.area().to_string(),
                obstruction_type: "TransverseCollarBarrier".to_string(),
                certified: margin > BigRational::zero(),
                margin: margin.to_string(),
            }
        })
        .collect();
    let min_margin = leaves
        .iter()
        .map(collar_cell_margin)
        .min()
        .unwrap_or_else(BigRational::zero);

    CollarPartitionCoverReport {
        schema_version: "collar_partition_cover.v2".to_string(),
        scope: "periodic_collar_slice_theta1_theta2".to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        firewall: FIREWALL.to_string(),
        total_leaves: leaves.len(),
        total_area: total_area.to_string(),
        area_conserved: total_area == BigRational::one(),
        all_margins_positive: !certificates.is_empty()
            && certificates.iter().all(|cert| cert.certified),
        min_margin: min_margin.to_string(),
        certificates,
    }
}
