
use crate::omega_native::exact::mub6_constants::{base_gap, delta_certified, lipschitz_bound};
use crate::omega_native::exact::mub6_karlsson_volume_cover::circle_touches;
use num_rational::BigRational;
use num_traits::Zero;
use omega_kernel::interval::Interval;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarBarrierEvaluation {
    pub assumed_slice_floor: String,
    pub assumed_lipschitz_bound: String,
    pub delta: String,
    pub erosion: String,
    pub conditional_margin: String,
    pub margin_positive: bool,
}

pub fn evaluate_collar_barrier(
    slice_floor: &BigRational,
    lipschitz: &BigRational,
    delta: &BigRational,
) -> Result<CollarBarrierEvaluation, String> {
    if slice_floor < &BigRational::zero()
        || lipschitz < &BigRational::zero()
        || delta < &BigRational::zero()
    {
        return Err("expected nonnegative assumptions and width".to_string());
    }
    let erosion = lipschitz * delta;
    let margin = slice_floor - &erosion;
    Ok(CollarBarrierEvaluation {
        assumed_slice_floor: slice_floor.to_string(),
        assumed_lipschitz_bound: lipschitz.to_string(),
        delta: delta.to_string(),
        erosion: erosion.to_string(),
        conditional_margin: margin.to_string(),
        margin_positive: margin > BigRational::zero(),
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarGridBox {
    pub u_x: [String; 2],
    pub v_x: [String; 2],
    pub u_y: [String; 2],
    pub v_y: [String; 2],
    pub u_z: [String; 2],
    pub v_z: [String; 2],
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct KarlssonCollarCoverReport {
    pub schema_version: String,
    pub scope: String,
    pub authority_effect: String,
    pub firewall: String,
    pub grid_divisions_per_axis: usize,
    pub candidate_constraint: String,
    pub barrier_arithmetic: CollarBarrierEvaluation,
    pub boxes: Vec<CollarGridBox>,
    pub coverage_certified: bool,
    pub missing_obligations: Vec<String>,
}

pub fn solve_karlsson_collar_cover(n: usize) -> KarlssonCollarCoverReport {
    assert!((2..=64).contains(&n), "grid size must be in 2..=64");
    let q = |a: i64, b: i64| BigRational::new(a.into(), b.into());
    let n_i = n as i64;
    let intervals: Vec<_> = (0..n_i)
        .map(|i| Interval::new(q(-n_i + 2 * i, n_i), q(-n_i + 2 * (i + 1), n_i)))
        .collect();
    let mut circle = Vec::new();
    for u in &intervals {
        for v in &intervals {
            if circle_touches(u, v) {
                circle.push((u, v));
            }
        }
    }
    let endpoints = |i: &Interval| [i.lo().to_string(), i.hi().to_string()];
    let mut boxes = Vec::new();
    for (ux, vx) in &circle {
        for (uy, vy) in &circle {
            boxes.push(CollarGridBox {
                u_x: endpoints(ux),
                v_x: endpoints(vx),
                u_y: endpoints(uy),
                v_y: endpoints(vy),
                u_z: ["999999/1000000".into(), "1".into()],
                v_z: ["0".into(), "1/1000".into()],
            });
        }
    }
    KarlssonCollarCoverReport {
        schema_version: "omega.mub.karlsson-collar-model.v2".into(),
        scope: "conditional_scalar_arithmetic_and_cartesian_grid_only".into(),
        authority_effect: "None".into(),
        firewall: "stated region only; mints no authority".into(),
        grid_divisions_per_axis: n,
        candidate_constraint: "the supplied slice floor came from |U[0,0]|^2 >= 81/100; no coverage of arbitrary candidate bases".into(),
        barrier_arithmetic: evaluate_collar_barrier(&base_gap(), &lipschitz_bound(), &delta_certified())
            .unwrap(),
        boxes, coverage_certified: false,
        missing_obligations: vec![
            "derive a curvature lower bound on the actual candidate domain".into(),
            "derive the transverse derivative bound for the actual family".into(),
            "provide a checked cover and a bridge to the concrete Lean curvature functional".into(),
        ],
    }
}
