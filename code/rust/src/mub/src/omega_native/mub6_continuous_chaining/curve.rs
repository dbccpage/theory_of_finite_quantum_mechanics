use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::d6_exact_curvature_cochain::D;
use crate::omega_native::exact::mub6_constants::{
    base_gap, certified_margin, delta_certified, delta_crit, lipschitz_bound,
};
use omega_number_theory::rational::rq;

/// Dimension of the ambient Hilbert space C^6.
pub const AMBIENT_DIM: usize = D;

pub const KARLSSON_BOUNDARY_Z_NUM: i64 = 1;
pub const KARLSSON_BOUNDARY_Z_DEN: i64 = 1000;
pub const T_MIN_MULTI_ANCHOR_NUM: i64 = 1;
pub const T_MIN_MULTI_ANCHOR_DEN: i64 = 180;
pub const T_MAX_MULTI_ANCHOR_NUM: i64 = 59;
pub const T_MAX_MULTI_ANCHOR_DEN: i64 = 180;
pub const GAP_PROBE_T_NUM: i64 = 1;
pub const GAP_PROBE_T_DEN: i64 = 122;
pub const NUM_ANCHORS_MIN: usize = 80;

/// Interface depth coordinate connecting to the Karlsson boundary manifold: z = 1/1000.
pub fn karlsson_boundary_z() -> BigRational {
    rq(KARLSSON_BOUNDARY_Z_NUM, KARLSSON_BOUNDARY_Z_DEN)
}

/// Domain lower bound for normalized angle t = θ / (2π): 0.
pub fn theta_interval_lower() -> BigRational {
    BigRational::zero()
}

/// Domain upper bound for normalized angle t = θ / (2π): 1 / 6 (corresponding to θ = π/3).
pub fn theta_interval_upper() -> BigRational {
    rq(1, 6)
}

/// Canonical multi-anchor domain lower bound: T_MIN = 1/180.
pub fn t_min_multi_anchor() -> BigRational {
    rq(T_MIN_MULTI_ANCHOR_NUM, T_MIN_MULTI_ANCHOR_DEN)
}

/// Canonical multi-anchor domain upper bound: T_MAX = 59/180.
pub fn t_max_multi_anchor() -> BigRational {
    rq(T_MAX_MULTI_ANCHOR_NUM, T_MAX_MULTI_ANCHOR_DEN)
}

/// Critical gap probe point: t = 1/122.
pub fn gap_probe_t() -> BigRational {
    rq(GAP_PROBE_T_NUM, GAP_PROBE_T_DEN)
}

/// Minimum number of certified anchor points required for multi-anchor covering: 80.
pub fn num_anchors_min() -> usize {
    NUM_ANCHORS_MIN
}

/// Errors arising during continuous parameter chaining and verification.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error, Serialize, Deserialize)]
pub enum ContinuousChainingError {
    #[error("Invalid parameter: {0}")]
    InvalidParameter(String),

    #[error("Step size {step} exceeds or equals critical threshold {delta_crit}")]
    StepExceedsCriticalThreshold {
        step: BigRational,
        delta_crit: BigRational,
    },

    #[error("Non-positive margin computed: margin = {margin} <= 0 (erosion {erosion}, base gap {base_gap})")]
    NonPositiveMargin {
        margin: BigRational,
        erosion: BigRational,
        base_gap: BigRational,
    },

    #[error("Coverage gap detected between adjacent intervals: left_hi = {left_hi} < right_lo = {right_lo}")]
    IntervalCoverageGap {
        left_hi: BigRational,
        right_lo: BigRational,
    },

    #[error("Point {point} lies outside declared domain [{bound_lo}, {bound_hi}]")]
    PointOutOfBounds {
        point: BigRational,
        bound_lo: BigRational,
        bound_hi: BigRational,
    },

    #[error("Curvature wall violation at {point}: margin {margin} below threshold {threshold}")]
    CurvatureWallViolation {
        point: BigRational,
        margin: BigRational,
        threshold: BigRational,
    },

    #[error("Non-unitary gauge transformation encountered: {0}")]
    NonUnitaryGauge(String),

    #[error("ZeroRel variety non-empty: residual squared sum = {residual_sum_sq} at {point}")]
    ZeroRelVarietyNonEmpty {
        point: BigRational,
        residual_sum_sq: BigRational,
    },

    #[error(
        "Cumulative travel degradation exhausted margin: travel = {travel}, margin = {margin} <= 0"
    )]
    CumulativeTravelExhausted {
        travel: BigRational,
        margin: BigRational,
    },

    #[error("Adjacent overlap violated between index {index} and {next_index}: step {step} > sum of radii {radii_sum}")]
    AdjacentOverlapViolated {
        index: usize,
        next_index: usize,
        step: BigRational,
        radii_sum: BigRational,
    },

    #[error(
        "Endpoint coverage violated: left {left} > t_min {t_min} or right {right} < t_max {t_max}"
    )]
    EndpointCoverageViolated {
        left: BigRational,
        t_min: BigRational,
        right: BigRational,
        t_max: BigRational,
    },

    #[error("Gap probe point {probe_t} not covered by any anchor ball in cover")]
    GapProbeNotCovered { probe_t: BigRational },
}

/// Parameter regimes along the 1-parameter curve θ ∈ (0, π/3).
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum CurveRegime {
    /// Cusp neighborhood θ -> 0 (normalized t in (0, 1/1000]).
    NearCusp,
    /// Intermediate curve segment (normalized t in (1/1000, 1/6 - 1/1000)).
    Intermediate,
    /// Boundary interface neighborhood θ -> π/3 (normalized t in [1/6 - 1/1000, 1/6)).
    NearBoundary,
}

/// Cusp and boundary collar neighborhood radius: 1/500 (corresponding to 2 * delta_certified).
pub fn cusp_neighborhood_radius() -> BigRational {
    rq(1, 500)
}

impl CurveRegime {
    /// Classify a normalized coordinate t = θ / (2π) into its curve regime.
    pub fn classify(t: &BigRational) -> Self {
        let radius = cusp_neighborhood_radius();
        let upper_bound = theta_interval_upper();
        let boundary_threshold = &upper_bound - &radius;

        if t <= &radius {
            Self::NearCusp
        } else if t >= &boundary_threshold {
            Self::NearBoundary
        } else {
            Self::Intermediate
        }
    }

    /// Descriptive name of the regime.
    pub fn name(&self) -> &'static str {
        match self {
            Self::NearCusp => "near_cusp_theta_to_zero",
            Self::Intermediate => "intermediate_curve_body",
            Self::NearBoundary => "near_boundary_theta_to_pi_third",
        }
    }
}

/// Certified rational step-size adaptivity engine.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct AdaptiveStepEngine {
    pub base_gap: BigRational,
    pub lipschitz_bound: BigRational,
    pub delta_crit: BigRational,
    pub max_certified_step: BigRational,
    pub min_certified_margin: BigRational,
}

impl AdaptiveStepEngine {
    /// Canonical step-size adaptivity engine matching the certified constants.
    pub fn canonical() -> Self {
        Self {
            base_gap: base_gap(),
            lipschitz_bound: lipschitz_bound(),
            delta_crit: delta_crit(),
            max_certified_step: delta_certified(),
            min_certified_margin: certified_margin(),
        }
    }

    /// Constructs and validates a custom step-size adaptivity engine.
    pub fn new(
        base_gap: BigRational,
        lipschitz_bound: BigRational,
    ) -> Result<Self, ContinuousChainingError> {
        let zero = BigRational::zero();
        if base_gap <= zero {
            return Err(ContinuousChainingError::InvalidParameter(format!(
                "base_gap must be strictly positive, got {base_gap}"
            )));
        }
        if lipschitz_bound <= zero {
            return Err(ContinuousChainingError::InvalidParameter(format!(
                "lipschitz_bound must be strictly positive, got {lipschitz_bound}"
            )));
        }

        let delta_crit = &base_gap / &lipschitz_bound;
        let max_step = delta_certified();
        let erosion = &lipschitz_bound * &max_step;
        let min_margin = &base_gap - &erosion;

        if min_margin <= zero {
            return Err(ContinuousChainingError::NonPositiveMargin {
                margin: min_margin,
                erosion,
                base_gap,
            });
        }

        Ok(Self {
            base_gap,
            lipschitz_bound,
            delta_crit,
            max_certified_step: max_step,
            min_certified_margin: min_margin,
        })
    }

    /// Computes quantitative erosion L · step.
    pub fn compute_erosion(&self, step: &BigRational) -> BigRational {
        &self.lipschitz_bound * step
    }

    /// Computes lower margin ε - L · step.
    pub fn compute_margin(&self, step: &BigRational) -> BigRational {
        &self.base_gap - self.compute_erosion(step)
    }

    /// Checks if a step size is strictly admissible: 0 < step < δ_crit.
    pub fn is_admissible_step(&self, step: &BigRational) -> bool {
        step > &BigRational::zero() && step < &self.delta_crit
    }

    /// Validates a step size against critical threshold and positivity requirements.
    /// Returns the verified certified margin if admissible.
    pub fn validate_step(
        &self,
        step: &BigRational,
    ) -> Result<BigRational, ContinuousChainingError> {
        if step <= &BigRational::zero() {
            return Err(ContinuousChainingError::InvalidParameter(format!(
                "step must be strictly positive, got {step}"
            )));
        }

        if step >= &self.delta_crit {
            return Err(ContinuousChainingError::StepExceedsCriticalThreshold {
                step: step.clone(),
                delta_crit: self.delta_crit.clone(),
            });
        }

        let margin = self.compute_margin(step);
        if margin <= BigRational::zero() {
            return Err(ContinuousChainingError::NonPositiveMargin {
                margin,
                erosion: self.compute_erosion(step),
                base_gap: self.base_gap.clone(),
            });
        }

        Ok(margin)
    }

    /// Computes the ratio of proposed step to the critical threshold: step / δ_crit.
    pub fn critical_ratio(&self, step: &BigRational) -> BigRational {
        step / &self.delta_crit
    }

    /// Dynamically adapts step size given an estimated local curvature scale factor.
    /// Clamps output to at most max_certified_step (1/1000).
    pub fn adapt_step(&self, curvature_factor: &BigRational) -> BigRational {
        if curvature_factor <= &BigRational::one() {
            self.max_certified_step.clone()
        } else {
            let adapted = &self.max_certified_step / curvature_factor;
            if adapted > self.max_certified_step {
                self.max_certified_step.clone()
            } else {
                adapted
            }
        }
    }
}

/// Exact rational parameter interval [lo, hi].
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ParameterInterval {
    pub lo: BigRational,
    pub hi: BigRational,
    pub center: BigRational,
    pub half_width: BigRational,
}

impl ParameterInterval {
    /// Create and validate a closed rational interval.
    pub fn new(lo: BigRational, hi: BigRational) -> Result<Self, ContinuousChainingError> {
        if lo > hi {
            return Err(ContinuousChainingError::InvalidParameter(format!(
                "Interval lo ({lo}) cannot exceed hi ({hi})"
            )));
        }
        let two = rq(2, 1);
        let center = (&lo + &hi) / &two;
        let half_width = (&hi - &lo) / &two;
        Ok(Self {
            lo,
            hi,
            center,
            half_width,
        })
    }

    /// Interval width: hi - lo.
    pub fn width(&self) -> BigRational {
        &self.hi - &self.lo
    }

    /// Check if a rational point lies within this closed interval.
    pub fn contains(&self, pt: &BigRational) -> bool {
        pt >= &self.lo && pt <= &self.hi
    }

    /// Check if this interval overlaps with another interval (closed intersection non-empty).
    pub fn overlaps(&self, other: &Self) -> bool {
        self.lo <= other.hi && other.lo <= self.hi
    }
}

/// A certified discrete node along the continuous parameter curve.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ChainingNode {
    pub index: usize,
    pub t: BigRational,
    pub interval: ParameterInterval,
    pub step_size: BigRational,
    pub regime: CurveRegime,
    pub local_base_gap: BigRational,
    pub local_lipschitz: BigRational,
    pub certified_margin: BigRational,
    pub is_certified: bool,
}

impl ChainingNode {
    /// Evaluates the worst-case lower bound at any point query_t within this node's cell:
    /// bound(query_t) = local_base_gap - local_lipschitz * |query_t - t|.
    pub fn evaluate_point_bound(&self, query_t: &BigRational) -> BigRational {
        let dist = (query_t - &self.t).abs();
        let erosion = &self.local_lipschitz * &dist;
        &self.local_base_gap - erosion
    }
}

/// Certificate of complete interval coverage without gaps.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct IntervalCoverageCertificate {
    pub total_nodes: usize,
    pub covered_range: (BigRational, BigRational),
    pub max_step_size: BigRational,
    pub min_margin: BigRational,
    pub gap_free: bool,
    pub all_nodes_certified: bool,
}

/// Continuous parameter chaining path covering θ ∈ (0, π/3).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ContinuousChainingPath {
    pub domain_lo: BigRational,
    pub domain_hi: BigRational,
    pub nodes: Vec<ChainingNode>,
    pub min_margin: BigRational,
    pub max_step: BigRational,
    pub total_nodes: usize,
    pub all_certified: bool,
    pub no_gaps: bool,
}

impl ContinuousChainingPath {
    /// Generate a uniform chaining path covering [domain_lo, domain_hi] with step size step.
    pub fn generate_uniform(
        domain_lo: BigRational,
        domain_hi: BigRational,
        step: BigRational,
    ) -> Result<Self, ContinuousChainingError> {
        let engine = AdaptiveStepEngine::canonical();
        let margin = engine.validate_step(&step)?;

        if domain_lo >= domain_hi {
            return Err(ContinuousChainingError::InvalidParameter(format!(
                "domain_lo ({domain_lo}) must be strictly less than domain_hi ({domain_hi})"
            )));
        }

        let two = rq(2, 1);
        let half_step = &step / &two;
        let mut nodes = Vec::new();
        let mut current_t = domain_lo.clone();
        let mut idx = 0;

        let mut min_margin = margin.clone();
        let mut max_step_actual = step.clone();

        while current_t < domain_hi {
            let iv_lo = if current_t >= half_step {
                &current_t - &half_step
            } else {
                BigRational::zero()
            };
            let iv_hi = &current_t + &half_step;
            let interval = ParameterInterval::new(iv_lo, iv_hi)?;
            let regime = CurveRegime::classify(&current_t);

            let node = ChainingNode {
                index: idx,
                t: current_t.clone(),
                interval,
                step_size: step.clone(),
                regime,
                local_base_gap: engine.base_gap.clone(),
                local_lipschitz: engine.lipschitz_bound.clone(),
                certified_margin: margin.clone(),
                is_certified: true,
            };

            if node.certified_margin < min_margin {
                min_margin = node.certified_margin.clone();
            }
            if node.step_size > max_step_actual {
                max_step_actual = node.step_size.clone();
            }

            nodes.push(node);
            idx += 1;
            current_t += &step;
        }

        // Add boundary endpoint node to enclose domain_hi
        let boundary_lo = &domain_hi - &half_step;
        let boundary_hi = &domain_hi + &half_step;
        let boundary_interval = ParameterInterval::new(boundary_lo, boundary_hi)?;
        let boundary_node = ChainingNode {
            index: idx,
            t: domain_hi.clone(),
            interval: boundary_interval,
            step_size: step.clone(),
            regime: CurveRegime::classify(&domain_hi),
            local_base_gap: engine.base_gap.clone(),
            local_lipschitz: engine.lipschitz_bound.clone(),
            certified_margin: margin,
            is_certified: true,
        };
        nodes.push(boundary_node);

        let mut path = Self {
            domain_lo,
            domain_hi,
            nodes,
            min_margin,
            max_step: max_step_actual,
            total_nodes: idx + 1,
            all_certified: true,
            no_gaps: true,
        };

        path.verify_coverage()?;
        Ok(path)
    }

    /// Generate the canonical continuous chaining path using certified step δ = 1/1000.
    pub fn generate_canonical() -> Result<Self, ContinuousChainingError> {
        Self::generate_uniform(
            theta_interval_lower(),
            theta_interval_upper(),
            delta_certified(),
        )
    }

    /// Verifies that adjacent nodes overlap with zero gaps and full domain coverage.
    pub fn verify_coverage(
        &mut self,
    ) -> Result<IntervalCoverageCertificate, ContinuousChainingError> {
        if self.nodes.is_empty() {
            return Err(ContinuousChainingError::InvalidParameter(
                "Cannot verify empty chaining path".to_string(),
            ));
        }

        // 1. Check lower boundary coverage
        if self.nodes[0].interval.lo > self.domain_lo {
            return Err(ContinuousChainingError::PointOutOfBounds {
                point: self.domain_lo.clone(),
                bound_lo: self.nodes[0].interval.lo.clone(),
                bound_hi: self.nodes[0].interval.hi.clone(),
            });
        }

        // 2. Check upper boundary coverage
        let last_idx = self.nodes.len() - 1;
        if self.nodes[last_idx].interval.hi < self.domain_hi {
            return Err(ContinuousChainingError::PointOutOfBounds {
                point: self.domain_hi.clone(),
                bound_lo: self.nodes[last_idx].interval.lo.clone(),
                bound_hi: self.nodes[last_idx].interval.hi.clone(),
            });
        }

        // 3. Check adjacent overlap (no-leakage contract: next.lo <= prev.hi)
        for i in 0..last_idx {
            let prev_hi = &self.nodes[i].interval.hi;
            let next_lo = &self.nodes[i + 1].interval.lo;
            if next_lo > prev_hi {
                self.no_gaps = false;
                return Err(ContinuousChainingError::IntervalCoverageGap {
                    left_hi: prev_hi.clone(),
                    right_lo: next_lo.clone(),
                });
            }
        }
        self.no_gaps = true;

        // 4. Verify all node margins are positive
        let zero = BigRational::zero();
        for node in &self.nodes {
            if node.certified_margin <= zero || !node.is_certified {
                self.all_certified = false;
                return Err(ContinuousChainingError::CurvatureWallViolation {
                    point: node.t.clone(),
                    margin: node.certified_margin.clone(),
                    threshold: certified_margin(),
                });
            }
        }
        self.all_certified = true;

        Ok(IntervalCoverageCertificate {
            total_nodes: self.nodes.len(),
            covered_range: (
                self.nodes[0].interval.lo.clone(),
                self.nodes[last_idx].interval.hi.clone(),
            ),
            max_step_size: self.max_step.clone(),
            min_margin: self.min_margin.clone(),
            gap_free: true,
            all_nodes_certified: true,
        })
    }

    /// Finds the first chaining node whose interval contains the query point.
    pub fn find_covering_node(&self, query_t: &BigRational) -> Option<&ChainingNode> {
        self.nodes
            .iter()
            .find(|node| node.interval.contains(query_t))
    }

    /// Evaluates the certified lower bound at an arbitrary rational point query_t.
    pub fn eval_margin_at_point(
        &self,
        query_t: &BigRational,
    ) -> Result<BigRational, ContinuousChainingError> {
        if query_t < &self.domain_lo || query_t > &self.domain_hi {
            return Err(ContinuousChainingError::PointOutOfBounds {
                point: query_t.clone(),
                bound_lo: self.domain_lo.clone(),
                bound_hi: self.domain_hi.clone(),
            });
        }

        let covering_node = self.find_covering_node(query_t).ok_or_else(|| {
            ContinuousChainingError::PointOutOfBounds {
                point: query_t.clone(),
                bound_lo: self.domain_lo.clone(),
                bound_hi: self.domain_hi.clone(),
            }
        })?;

        Ok(covering_node.evaluate_point_bound(query_t))
    }
}

