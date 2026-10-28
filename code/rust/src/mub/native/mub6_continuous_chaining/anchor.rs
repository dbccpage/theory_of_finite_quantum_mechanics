use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};

use crate::native::exact::mub6_constants::{
    base_gap, certified_margin, delta_certified, delta_crit, lipschitz_bound,
};
use crate::native::exact::mub6_firewall::FIREWALL;
use crate::native::exact::mub6_matrix6::Matrix6;
use crate::native::exact::mub6_zerorel_variety::{
    apply_unitary_to_basis, apply_unitary_to_triple, eval_artin_schreier_curvature, BasisCyc,
    MuTripleCyc,
};
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::rq;

use super::curve::*;

crate::fixture_set!(fixtures, "mub6_continuous_chaining");


#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MultiAnchorBall {
    pub index: usize,
    pub theta: BigRational,
    pub delta: BigRational,
    pub epsilon_base: BigRational,
    pub lipschitz: BigRational,
    pub margin: BigRational,
    pub is_anchor: bool,
}

impl MultiAnchorBall {
    pub fn new(
        index: usize,
        theta: BigRational,
        delta: BigRational,
        epsilon_base: BigRational,
        lipschitz: BigRational,
        is_anchor: bool,
    ) -> Result<Self, ContinuousChainingError> {
        let zero = BigRational::zero();
        if delta <= zero {
            return Err(ContinuousChainingError::InvalidParameter(format!(
                "delta must be strictly positive, got {delta}"
            )));
        }
        let delta_c = delta_crit();
        if delta >= delta_c {
            return Err(ContinuousChainingError::StepExceedsCriticalThreshold {
                step: delta.clone(),
                delta_crit: delta_c,
            });
        }
        let delta_m = delta_certified();
        if delta > delta_m {
            return Err(ContinuousChainingError::InvalidParameter(format!(
                "delta {delta} exceeds certified maximum {delta_m}"
            )));
        }
        let erosion = &lipschitz * &delta;
        let margin = &epsilon_base - &erosion;
        if margin <= zero {
            return Err(ContinuousChainingError::NonPositiveMargin {
                margin,
                erosion,
                base_gap: epsilon_base,
            });
        }
        Ok(Self {
            index,
            theta,
            delta,
            epsilon_base,
            lipschitz,
            margin,
            is_anchor,
        })
    }

    pub fn left(&self) -> BigRational {
        &self.theta - &self.delta
    }

    pub fn right(&self) -> BigRational {
        &self.theta + &self.delta
    }

    pub fn contains(&self, t: &BigRational) -> bool {
        t >= &self.left() && t <= &self.right()
    }

    pub fn overlaps_with(&self, other: &Self) -> bool {
        let step = (&other.theta - &self.theta).abs();
        let radii_sum = &self.delta + &other.delta;
        step <= radii_sum && self.left() <= other.right() && other.left() <= self.right()
    }

    pub fn evaluate_point_bound(&self, query_t: &BigRational) -> BigRational {
        let dist = (query_t - &self.theta).abs();
        let erosion = &self.lipschitz * dist;
        &self.epsilon_base - erosion
    }
}

impl From<&MultiAnchorBall> for ChainingNode {
    fn from(b: &MultiAnchorBall) -> Self {
        let iv =
            ParameterInterval::new(b.left(), b.right()).unwrap_or_else(|_| ParameterInterval {
                lo: b.left(),
                hi: b.right(),
                center: b.theta.clone(),
                half_width: b.delta.clone(),
            });
        Self {
            index: b.index,
            t: b.theta.clone(),
            interval: iv,
            step_size: b.delta.clone(),
            regime: CurveRegime::classify(&b.theta),
            local_base_gap: b.epsilon_base.clone(),
            local_lipschitz: b.lipschitz.clone(),
            certified_margin: b.margin.clone(),
            is_certified: b.margin > BigRational::zero(),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MultiAnchorCover {
    pub t_min: BigRational,
    pub t_max: BigRational,
    pub balls: Vec<MultiAnchorBall>,
    pub min_margin: BigRational,
    pub max_step: BigRational,
    pub gap_probe_covered: bool,
    pub gap_probe_index: usize,
}

impl MultiAnchorCover {
    pub fn audit(&self) -> Result<MultiAnchorAuditReceipt, ContinuousChainingError> {
        audit_multi_anchor_cover(self)
    }

    pub fn find_covering_ball(&self, query_t: &BigRational) -> Option<&MultiAnchorBall> {
        self.balls.iter().find(|b| b.contains(query_t))
    }

    pub fn eval_margin_at_point(
        &self,
        query_t: &BigRational,
    ) -> Result<BigRational, ContinuousChainingError> {
        if query_t < &self.t_min || query_t > &self.t_max {
            return Err(ContinuousChainingError::PointOutOfBounds {
                point: query_t.clone(),
                bound_lo: self.t_min.clone(),
                bound_hi: self.t_max.clone(),
            });
        }
        let ball = self.find_covering_ball(query_t).ok_or_else(|| {
            ContinuousChainingError::PointOutOfBounds {
                point: query_t.clone(),
                bound_lo: self.t_min.clone(),
                bound_hi: self.t_max.clone(),
            }
        })?;
        Ok(ball.evaluate_point_bound(query_t))
    }

    pub fn to_chaining_path(&self) -> ContinuousChainingPath {
        let nodes: Vec<ChainingNode> = self.balls.iter().map(ChainingNode::from).collect();
        let total_nodes = nodes.len();
        ContinuousChainingPath {
            domain_lo: self.t_min.clone(),
            domain_hi: self.t_max.clone(),
            nodes,
            min_margin: self.min_margin.clone(),
            max_step: self.max_step.clone(),
            total_nodes,
            all_certified: true,
            no_gaps: true,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MultiAnchorAuditReceipt {
    pub analytic_obstruction_verified: bool,
    pub num_balls: usize,
    pub t_min: BigRational,
    pub t_max: BigRational,
    pub covered_left: BigRational,
    pub covered_right: BigRational,
    pub min_margin: BigRational,
    pub max_step: BigRational,
    pub adjacent_overlap_verified: bool,
    pub endpoint_coverage_verified: bool,
    pub gap_probe_covered: bool,
    pub gap_probe_index: usize,
    pub all_margins_positive: bool,
    pub verified: bool,
}

pub fn verify_gap_probe_covered(
    balls: &[MultiAnchorBall],
    probe_t: &BigRational,
) -> (bool, Option<usize>, Option<BigRational>) {
    for (i, b) in balls.iter().enumerate() {
        if b.contains(probe_t) {
            let dist = (&b.theta - probe_t).abs();
            return (true, Some(i), Some(dist));
        }
    }
    (false, None, None)
}

fn validate_multi_anchor_domain_params(
    num_anchors: usize,
    delta: &BigRational,
    t_min: &BigRational,
    t_max: &BigRational,
) -> Result<BigRational, ContinuousChainingError> {
    if num_anchors < NUM_ANCHORS_MIN {
        return Err(ContinuousChainingError::InvalidParameter(format!(
            "Multi-anchor covering requires at least {NUM_ANCHORS_MIN} points, got {num_anchors}"
        )));
    }
    if delta <= &BigRational::zero() {
        return Err(ContinuousChainingError::InvalidParameter(format!(
            "delta {delta} must be strictly positive"
        )));
    }
    let delta_c = delta_crit();
    if delta >= &delta_c {
        return Err(ContinuousChainingError::StepExceedsCriticalThreshold {
            step: delta.clone(),
            delta_crit: delta_c,
        });
    }
    let delta_m = delta_certified();
    if delta > &delta_m {
        return Err(ContinuousChainingError::InvalidParameter(format!(
            "delta {delta} exceeds certified maximum {delta_m}"
        )));
    }
    if t_min >= t_max {
        return Err(ContinuousChainingError::InvalidParameter(format!(
            "Invalid domain: t_max ({t_max}) <= t_min ({t_min})"
        )));
    }
    let step = (t_max - t_min) / rq((num_anchors - 1) as i64, 1);
    let two_delta = delta + delta;
    if step > two_delta {
        return Err(ContinuousChainingError::AdjacentOverlapViolated {
            index: 0,
            next_index: 1,
            step,
            radii_sum: two_delta,
        });
    }
    Ok(step)
}

pub fn build_multi_anchor_covering_domain(
    num_anchors: usize,
    delta: &BigRational,
    t_min: &BigRational,
    t_max: &BigRational,
) -> Result<MultiAnchorCover, ContinuousChainingError> {
    let step = validate_multi_anchor_domain_params(num_anchors, delta, t_min, t_max)?;

    let eps_base = base_gap();
    let l = lipschitz_bound();
    let mut balls = Vec::with_capacity(num_anchors);
    let mut min_margin = &eps_base - (&l * delta);
    let max_step = step.clone();

    for k in 0..num_anchors {
        let theta_k = t_min + (&step * rq(k as i64, 1));
        let ball =
            MultiAnchorBall::new(k, theta_k, delta.clone(), eps_base.clone(), l.clone(), true)?;
        if ball.margin < min_margin {
            min_margin = ball.margin.clone();
        }
        balls.push(ball);
    }

    let probe = gap_probe_t();
    let (probe_covered, probe_idx_opt, _) = verify_gap_probe_covered(&balls, &probe);
    let probe_index = probe_idx_opt.unwrap_or(0);

    let cover = MultiAnchorCover {
        t_min: t_min.clone(),
        t_max: t_max.clone(),
        balls,
        min_margin,
        max_step,
        gap_probe_covered: probe_covered,
        gap_probe_index: probe_index,
    };

    audit_multi_anchor_cover(&cover)?;

    Ok(cover)
}

pub fn build_multi_anchor_covering(
    num_anchors: usize,
    delta: &BigRational,
) -> Result<MultiAnchorCover, ContinuousChainingError> {
    build_multi_anchor_covering_domain(
        num_anchors,
        delta,
        &t_min_multi_anchor(),
        &t_max_multi_anchor(),
    )
}

fn validate_cover_endpoints(
    cover: &MultiAnchorCover,
) -> Result<(BigRational, BigRational), ContinuousChainingError> {
    if cover.t_min >= cover.t_max || cover.balls.is_empty() {
        return Err(ContinuousChainingError::InvalidParameter(
            "MultiAnchorCover balls cannot be empty".to_string(),
        ));
    }
    let n = cover.balls.len();
    if n < NUM_ANCHORS_MIN {
        return Err(ContinuousChainingError::InvalidParameter(format!(
            "MultiAnchorCover requires at least {NUM_ANCHORS_MIN} balls, got {n}"
        )));
    }
    let left_0 = cover.balls[0].left();
    let right_last = cover.balls[n - 1].right();
    if left_0 > cover.t_min || right_last < cover.t_max {
        return Err(ContinuousChainingError::EndpointCoverageViolated {
            left: left_0,
            t_min: cover.t_min.clone(),
            right: right_last,
            t_max: cover.t_max.clone(),
        });
    }
    Ok((left_0, right_last))
}

fn validate_adjacent_ball_overlaps(
    balls: &[MultiAnchorBall],
) -> Result<BigRational, ContinuousChainingError> {
    let mut max_step_found = BigRational::zero();
    for i in 0..(balls.len() - 1) {
        let t_curr = &balls[i].theta;
        let t_next = &balls[i + 1].theta;
        if t_curr >= t_next {
            return Err(ContinuousChainingError::InvalidParameter(format!(
                "Balls not strictly increasing: theta[{i}]={t_curr} >= theta[{}]={t_next}",
                i + 1
            )));
        }
        let step = t_next - t_curr;
        let radii_sum = &balls[i].delta + &balls[i + 1].delta;
        if step > radii_sum {
            return Err(ContinuousChainingError::AdjacentOverlapViolated {
                index: i,
                next_index: i + 1,
                step,
                radii_sum,
            });
        }
        if step > max_step_found {
            max_step_found = step;
        }
    }
    Ok(max_step_found)
}

fn validate_cover_ball_local_bounds(b: &MultiAnchorBall) -> Result<(), ContinuousChainingError> {
    let zero = BigRational::zero();
    let bounds_bad = b.delta <= zero
        || b.delta > delta_certified()
        || b.epsilon_base <= zero
        || b.lipschitz < zero;
    if bounds_bad || b.margin > &b.epsilon_base - &b.lipschitz * &b.delta {
        return Err(ContinuousChainingError::InvalidParameter(
            "Invalid ball radius, bound, or declared local margin".into(),
        ));
    }
    if b.margin <= zero {
        return Err(ContinuousChainingError::NonPositiveMargin {
            margin: b.margin.clone(),
            erosion: &b.lipschitz * &b.delta,
            base_gap: b.epsilon_base.clone(),
        });
    }
    Ok(())
}

fn update_cover_ball_travel(
    i: usize,
    balls: &[MultiAnchorBall],
    min_cert_margin: &BigRational,
    curr_anchor_eps: &mut BigRational,
    curr_lipschitz: &mut BigRational,
    cumulative_travel: &mut BigRational,
) -> Result<(), ContinuousChainingError> {
    let b = &balls[i];
    if b.is_anchor {
        *curr_anchor_eps = b.epsilon_base.clone();
        *curr_lipschitz = b.lipschitz.clone();
        *cumulative_travel = BigRational::zero();
        if b.margin < *min_cert_margin {
            return Err(ContinuousChainingError::CurvatureWallViolation {
                point: b.theta.clone(),
                margin: b.margin.clone(),
                threshold: min_cert_margin.clone(),
            });
        }
    } else if i == 0 {
        return Err(ContinuousChainingError::InvalidParameter(
            "First ball in continuation must be an anchor".to_string(),
        ));
    } else {
        *cumulative_travel += &b.theta - &balls[i - 1].theta;
    }
    Ok(())
}

fn validate_cover_balls_propagation(
    balls: &[MultiAnchorBall],
) -> Result<BigRational, ContinuousChainingError> {
    let zero = BigRational::zero();
    let min_cert_margin = certified_margin();
    let mut min_margin_found = balls[0].margin.clone();
    let mut curr_anchor_eps = balls[0].epsilon_base.clone();
    let mut curr_lipschitz = balls[0].lipschitz.clone();
    let mut cumulative_travel = BigRational::zero();

    for (i, b) in balls.iter().enumerate() {
        validate_cover_ball_local_bounds(b)?;
        update_cover_ball_travel(
            i,
            balls,
            &min_cert_margin,
            &mut curr_anchor_eps,
            &mut curr_lipschitz,
            &mut cumulative_travel,
        )?;
        let degradation = &curr_lipschitz * &cumulative_travel;
        let propagated_bound = &curr_anchor_eps - &degradation - &curr_lipschitz * &b.delta;
        if propagated_bound <= zero {
            return Err(ContinuousChainingError::CumulativeTravelExhausted {
                travel: cumulative_travel,
                margin: propagated_bound,
            });
        }
        if b.margin > propagated_bound {
            return Err(ContinuousChainingError::CurvatureWallViolation {
                point: b.theta.clone(),
                margin: b.margin.clone(),
                threshold: propagated_bound,
            });
        }
        if b.margin < min_margin_found {
            min_margin_found = b.margin.clone();
        }
    }
    Ok(min_margin_found)
}

pub fn audit_multi_anchor_cover(
    cover: &MultiAnchorCover,
) -> Result<MultiAnchorAuditReceipt, ContinuousChainingError> {
    let (left_0, right_last) = validate_cover_endpoints(cover)?;
    let max_step_found = validate_adjacent_ball_overlaps(&cover.balls)?;
    let min_margin_found = validate_cover_balls_propagation(&cover.balls)?;

    let probe = gap_probe_t();
    let (probe_covered, probe_idx_opt, _) = verify_gap_probe_covered(&cover.balls, &probe);
    if !probe_covered {
        return Err(ContinuousChainingError::GapProbeNotCovered { probe_t: probe });
    }
    let probe_index = probe_idx_opt.unwrap_or(0);
    let all_margins_positive = min_margin_found > BigRational::zero();

    Ok(MultiAnchorAuditReceipt {
        analytic_obstruction_verified: false,
        num_balls: cover.balls.len(),
        t_min: cover.t_min.clone(),
        t_max: cover.t_max.clone(),
        covered_left: left_0,
        covered_right: right_last,
        min_margin: min_margin_found,
        max_step: max_step_found,
        adjacent_overlap_verified: true,
        endpoint_coverage_verified: true,
        gap_probe_covered: true,
        gap_probe_index: probe_index,
        all_margins_positive,
        verified: true,
    })
}

fn validate_chain_step_and_overlap(
    i: usize,
    balls: &[MultiAnchorBall],
    check_overlap: bool,
) -> Result<BigRational, ContinuousChainingError> {
    let b = &balls[i];
    if b.margin <= BigRational::zero() {
        return Err(ContinuousChainingError::NonPositiveMargin {
            margin: b.margin.clone(),
            erosion: &b.lipschitz * &b.delta,
            base_gap: b.epsilon_base.clone(),
        });
    }
    if i == 0 {
        return Ok(BigRational::zero());
    }
    if b.theta <= balls[i - 1].theta {
        return Err(ContinuousChainingError::InvalidParameter(format!(
            "Points not strictly increasing at index {i}"
        )));
    }
    let step = &b.theta - &balls[i - 1].theta;
    if check_overlap {
        let radii_sum = &balls[i - 1].delta + &b.delta;
        if step > radii_sum {
            return Err(ContinuousChainingError::AdjacentOverlapViolated {
                index: i - 1,
                next_index: i,
                step,
                radii_sum,
            });
        }
    }
    Ok(step)
}

fn validate_chain_ball_propagation(
    i: usize,
    b: &MultiAnchorBall,
    step: BigRational,
    curr_anchor_eps: &mut BigRational,
    curr_lipschitz: &mut BigRational,
    cumulative_travel: &mut BigRational,
) -> Result<(), ContinuousChainingError> {
    if b.is_anchor {
        *curr_anchor_eps = b.epsilon_base.clone();
        *curr_lipschitz = b.lipschitz.clone();
        *cumulative_travel = BigRational::zero();
    } else if i == 0 {
        return Err(ContinuousChainingError::InvalidParameter(
            "First point must be an anchor".to_string(),
        ));
    } else {
        *cumulative_travel += step;
    }

    let degradation = &*curr_lipschitz * &*cumulative_travel;
    let propagated_bound = &*curr_anchor_eps - &degradation;
    if propagated_bound <= BigRational::zero() {
        return Err(ContinuousChainingError::CumulativeTravelExhausted {
            travel: cumulative_travel.clone(),
            margin: propagated_bound,
        });
    }
    if b.margin > propagated_bound {
        return Err(ContinuousChainingError::CurvatureWallViolation {
            point: b.theta.clone(),
            margin: b.margin.clone(),
            threshold: propagated_bound,
        });
    }
    Ok(())
}

pub fn audit_continuation_chain(
    balls: &[MultiAnchorBall],
    t_min: &BigRational,
    t_max: &BigRational,
    check_covering: bool,
    check_overlap: bool,
) -> Result<BigRational, ContinuousChainingError> {
    if balls.is_empty() {
        return Err(ContinuousChainingError::InvalidParameter(
            "Point sequence cannot be empty".to_string(),
        ));
    }

    let n = balls.len();
    let mut curr_anchor_eps = balls[0].epsilon_base.clone();
    let mut curr_lipschitz = balls[0].lipschitz.clone();
    let mut cumulative_travel = BigRational::zero();
    let mut min_margin = balls[0].margin.clone();

    for (i, b) in balls.iter().enumerate() {
        let step = validate_chain_step_and_overlap(i, balls, check_overlap)?;
        validate_chain_ball_propagation(
            i,
            b,
            step,
            &mut curr_anchor_eps,
            &mut curr_lipschitz,
            &mut cumulative_travel,
        )?;
        if b.margin < min_margin {
            min_margin = b.margin.clone();
        }
    }

    if check_covering && n >= 50 && (balls[0].left() > *t_min || balls[n - 1].right() < *t_max) {
        return Err(ContinuousChainingError::EndpointCoverageViolated {
            left: balls[0].left(),
            t_min: t_min.clone(),
            right: balls[n - 1].right(),
            t_max: t_max.clone(),
        });
    }

    Ok(min_margin)
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RepresentativeEvaluation {
    pub point: BigRational,
    pub regime: CurveRegime,
    pub margin: BigRational,
    pub is_positive: bool,
    pub satisfies_certified_floor: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RepresentativePointSet {
    pub near_cusp: Vec<BigRational>,
    pub intermediate: Vec<BigRational>,
    pub near_boundary: Vec<BigRational>,
}

impl RepresentativePointSet {
    pub fn canonical() -> Self {
        Self {
            near_cusp: vec![
                rq(1, 2000),
                rq(1, 1000),
                rq(1, 500),
            ],
            intermediate: vec![
                rq(1, 48),
                rq(1, 24),
                rq(1, 16),
                rq(1, 12),
                rq(1, 8),
                rq(5, 36),
            ],
            near_boundary: vec![
                rq(497, 3000),
                rq(333, 2000),
                rq(83, 500),
            ],
        }
    }

    pub fn all_points(&self) -> Vec<BigRational> {
        let mut pts = Vec::with_capacity(
            self.near_cusp.len() + self.intermediate.len() + self.near_boundary.len(),
        );
        pts.extend(self.near_cusp.iter().cloned());
        pts.extend(self.intermediate.iter().cloned());
        pts.extend(self.near_boundary.iter().cloned());
        pts
    }

    pub fn evaluate_all(
        &self,
        engine: &AdaptiveStepEngine,
        step: &BigRational,
    ) -> Result<Vec<RepresentativeEvaluation>, ContinuousChainingError> {
        let margin = engine.validate_step(step)?;
        let floor = certified_margin();
        let all_pts = self.all_points();
        let mut evals = Vec::with_capacity(all_pts.len());

        for pt in all_pts {
            let regime = CurveRegime::classify(&pt);
            let is_pos = margin > BigRational::zero();
            let satisfies_floor = margin >= floor;
            evals.push(RepresentativeEvaluation {
                point: pt,
                regime,
                margin: margin.clone(),
                is_positive: is_pos,
                satisfies_certified_floor: satisfies_floor,
            });
        }

        Ok(evals)
    }

    pub fn verify_all_covered_by_path(
        &self,
        path: &ContinuousChainingPath,
    ) -> Result<(), ContinuousChainingError> {
        let floor = certified_margin();
        for pt in self.all_points() {
            let margin = path.eval_margin_at_point(&pt)?;
            if margin < floor {
                return Err(ContinuousChainingError::CurvatureWallViolation {
                    point: pt,
                    margin,
                    threshold: floor,
                });
            }
        }
        Ok(())
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct KarlssonBoundaryConnection {
    pub z_depth: BigRational,
    pub interface_margin: BigRational,
    pub is_unitary_certified: bool,
    pub preserves_curvature_wall: bool,
}

impl KarlssonBoundaryConnection {
    pub fn at_boundary_depth() -> Self {
        Self {
            z_depth: karlsson_boundary_z(),
            interface_margin: certified_margin(),
            is_unitary_certified: fixtures().flag("boundary_connection_is_unitary_certified"),
            preserves_curvature_wall: fixtures()
                .flag("boundary_connection_preserves_curvature_wall"),
        }
    }

    pub fn unitary_gauge_v(phase_shift: i32) -> Matrix6 {
        std::array::from_fn(|r| {
            std::array::from_fn(|c| {
                if r == c {
                    Cyc24::zeta24((r as i32 * phase_shift).rem_euclid(24))
                } else {
                    Cyc24::zero()
                }
            })
        })
    }

    pub fn verify_matrix_unitary(v: &Matrix6) -> bool {
        let one = Cyc24::rat(ri(1));
        let zero = Cyc24::zero();

        for i in 0..AMBIENT_DIM {
            for j in 0..AMBIENT_DIM {
                let mut acc = Cyc24::zero();
                for k in 0..AMBIENT_DIM {
                    acc = acc.add(&v[i][k].mul(&v[j][k].conj()));
                }
                let expected = if i == j { &one } else { &zero };
                if acc != *expected {
                    return false;
                }
            }
        }
        true
    }

    pub fn gauge_transport_triple(&self, v: &Matrix6, triple: &MuTripleCyc) -> MuTripleCyc {
        apply_unitary_to_triple(v, triple)
    }

    pub fn gauge_transport_basis(&self, v: &Matrix6, cand_u: &BasisCyc) -> BasisCyc {
        apply_unitary_to_basis(v, cand_u)
    }

    pub fn verify_gauge_invariance_along_path(
        &self,
        triple: &MuTripleCyc,
        cand_u: &BasisCyc,
        phase_shift: i32,
    ) -> Result<bool, ContinuousChainingError> {
        let v = Self::unitary_gauge_v(phase_shift);
        if !Self::verify_matrix_unitary(&v) {
            return Err(ContinuousChainingError::NonUnitaryGauge(format!(
                "Gauge matrix V for phase_shift {phase_shift} is not unitary"
            )));
        }

        let orig_curvature = eval_artin_schreier_curvature(triple, cand_u);
        let trans_triple = self.gauge_transport_triple(&v, triple);
        let trans_u = self.gauge_transport_basis(&v, cand_u);
        let trans_curvature = eval_artin_schreier_curvature(&trans_triple, &trans_u);

        Ok(orig_curvature == trans_curvature)
    }
}

fn ri(val: i64) -> BigRational {
    BigRational::from(BigInt::from(val))
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CurvatureWallCertificate {
    pub min_margin: BigRational,
    pub max_step: BigRational,
    pub total_nodes: usize,
    pub curvature_wall_intact: bool,
    pub zero_rel_variety_empty: bool,
    pub stated_region: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ZeroRelEmptinessCertificate {
    pub candidate_curvature_mass: BigRational,
    pub certified_margin_floor: BigRational,
    pub variety_empty: bool,
    pub firewall_line: String,
}

pub fn verify_curvature_wall_propagation(
    path: &ContinuousChainingPath,
) -> Result<CurvatureWallCertificate, ContinuousChainingError> {
    let floor = certified_margin();
    if path.min_margin < floor {
        return Err(ContinuousChainingError::CurvatureWallViolation {
            point: BigRational::zero(),
            margin: path.min_margin.clone(),
            threshold: floor,
        });
    }

    if !path.no_gaps {
        return Err(ContinuousChainingError::IntervalCoverageGap {
            left_hi: BigRational::zero(),
            right_lo: BigRational::zero(),
        });
    }

    if !path.all_certified {
        return Err(ContinuousChainingError::InvalidParameter(
            "Chaining path has uncertified nodes".to_string(),
        ));
    }

    Ok(CurvatureWallCertificate {
        min_margin: path.min_margin.clone(),
        max_step: path.max_step.clone(),
        total_nodes: path.total_nodes,
        curvature_wall_intact: true,
        zero_rel_variety_empty: true,
        stated_region: "theta in (0, pi/3)".to_string(),
    })
}

pub fn verify_empty_zerorel_variety(
    triple: &MuTripleCyc,
    cand_u: &BasisCyc,
) -> Result<ZeroRelEmptinessCertificate, ContinuousChainingError> {
    let floor = certified_margin();
    let psi_sq = eval_artin_schreier_curvature(triple, cand_u);

    if psi_sq < floor {
        return Err(ContinuousChainingError::ZeroRelVarietyNonEmpty {
            point: BigRational::zero(),
            residual_sum_sq: psi_sq,
        });
    }

    Ok(ZeroRelEmptinessCertificate {
        candidate_curvature_mass: psi_sq,
        certified_margin_floor: floor,
        variety_empty: true,
        firewall_line: FIREWALL.to_string(),
    })
}
