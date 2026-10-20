use crate::qm::bridge::matrix as mx;
use crate::qm::finite_witness::{field_q, field_usize, parse_q, qstr, qvec};
use num_traits::Zero;
use omega_general_relativity::simplicial_dynamics::{
    bianchi, emit_angular, CauchySlice, Constraints, ReggeFourSimplex,
};
use omega_lie_theory::cayley::{cayley_transform, is_orthogonal};
use omega_number_theory::rational::{ri, rq, Rational as Q};
use serde_json::{json, Value};
use std::collections::BTreeMap;

pub use crate::qm::domain::simplicial_entropy_schedule::{
    area_model, page_curve, AreaModel, PageStep,
};

fn constraints_json(c: &Constraints) -> Value {
    json!({"gauss":c.gauss.iter().map(|v|qvec(v)).collect::<Vec<_>>(),"vector":c.vector.iter().map(|v|qvec(v)).collect::<Vec<_>>(),"scalar":qvec(&c.scalar),"master":qstr(&c.master),"curvature":qvec(&c.curvature),"variance":qstr(&c.variance),"boundary_area":c.boundary_area})
}

pub fn run(input: &Value) -> Result<Value, String> {
    evaluate(input).map_err(|e| e.to_string())
}
type GravError = omega_general_relativity::simplicial_dynamics::SimplicialDynamicsError;

fn parse_glued(input: &Value, n: usize) -> Result<Vec<[(usize, usize); 2]>, GravError> {
    if let Some(g) = input.get("glued") {
        Ok(
            serde_json::from_value::<Vec<[(usize, usize); 2]>>(g.clone())
                .map_err(|_| "INVALID_GLUING")?,
        )
    } else {
        Ok((1..n).map(|i| [(i - 1, 1), (i, 0)]).collect())
    }
}

fn parse_single_position(v: &Value) -> Result<[Q; 3], String> {
    let x = v.as_array().ok_or("INVALID_POSITION")?;
    if x.len() != 3 {
        return Err("INVALID_POSITION".into());
    }
    Ok([parse_q(&x[0])?, parse_q(&x[1])?, parse_q(&x[2])?])
}

fn parse_positions(input: &Value) -> Result<Vec<[Q; 3]>, GravError> {
    if let Some(v) = input.get("positions") {
        let rows = v.as_array().ok_or("INVALID_POSITIONS")?;
        let mut out = Vec::with_capacity(rows.len());
        for row in rows {
            out.push(parse_single_position(row)?);
        }
        Ok(out)
    } else {
        Ok(vec![
            [ri(0), ri(0), ri(0)],
            [ri(1), ri(0), ri(0)],
            [ri(0), ri(1), ri(0)],
            [ri(0), ri(0), ri(1)],
            [ri(0), ri(0), ri(-1)],
        ])
    }
}

fn parse_tetrahedra(input: &Value) -> Result<Vec<[usize; 4]>, GravError> {
    if let Some(t) = input.get("cells") {
        Ok(serde_json::from_value(t.clone()).map_err(|_| "INVALID_CELLS")?)
    } else {
        Ok(vec![[0, 1, 2, 3], [0, 1, 2, 4]])
    }
}

fn run_relaxation_loop(
    slice: &mut CauchySlice,
    steps: usize,
    freeze: bool,
) -> Result<(Vec<Value>, bool, bool), GravError> {
    let mut history = vec![constraints_json(&slice.constraints())];
    let mut master_nonincreasing = true;
    let mut variance_nonincreasing = true;
    for _ in 0..steps {
        let (dm, dv) = slice.relaxation_step(&rq(1, 10), freeze)?;
        master_nonincreasing &= dm <= ri(0);
        variance_nonincreasing &= dv <= ri(0);
        history.push(constraints_json(&slice.constraints()));
    }
    Ok((history, master_nonincreasing, variance_nonincreasing))
}

fn check_regge_and_tetrad(tau: &Q) -> Result<(bool, bool), GravError> {
    let mut defects = BTreeMap::new();
    for i in 0..5 {
        for j in i + 1..5 {
            for k in j + 1..5 {
                defects.insert([i, j, k], rq((i + j + k) as i64, 7));
            }
        }
    }
    let simplex = ReggeFourSimplex {
        positions: std::array::from_fn(|i| std::array::from_fn(|j| ri(i64::from(i == j + 1)))),
        hinge_defects: defects,
    };
    let b_bianchi = simplex.boundary_bianchi()?;
    let t_bianchi = simplex.tetrahedron_bianchi([0, 1, 2, 3], false)?;
    let regge = mx::is_zero_matrix(&b_bianchi)? && t_bianchi.as_slice().iter().all(Q::is_zero);
    let bivector = simplex.hinge_bivector([0, 1, 2])?;
    let tetrad = cayley_transform(&bivector, tau)?;
    Ok((regge, is_orthogonal(&tetrad)))
}

fn check_angular_conservation() -> Result<bool, GravError> {
    let mut jb = mx::zeros(4, 4)?;
    let mut jr = jb.clone();
    emit_angular(
        &mut jb,
        &mut jr,
        &[ri(1), ri(2), ri(3), ri(4)],
        &[ri(2), ri(-1), ri(3), ri(0)],
    )?;
    let j_sum = mx::add(&jb, &jr)?;
    Ok(mx::is_zero_matrix(&j_sum)?)
}

fn compute_bianchi_and_angular(
    slice: &CauchySlice,
) -> Result<(Value, bool, bool, bool, bool), GravError> {
    let p: Vec<_> = slice.positions().iter().map(|v| v.to_vec()).collect();
    let hinges: Vec<_> = slice
        .holonomies()
        .keys()
        .map(|&(u, v)| (u, v, rq((u + v + 1) as i64, 7)))
        .collect();
    let (local, force, torque) = bianchi(&p, &hinges)?;
    let p4: Vec<_> = p
        .iter()
        .enumerate()
        .map(|(i, row)| {
            let mut row = row.clone();
            row.push(ri(i as i64));
            row
        })
        .collect();
    let (_, force4, torque4) = bianchi(&p4, &hinges)?;
    let torque_rows = mx::to_rows(&torque)?;
    let bianchi_val = json!({
        "local": local.iter().map(|v| qvec(v)).collect::<Vec<_>>(),
        "total_force": qvec(&force),
        "torque": torque_rows.iter().map(|v| qvec(v)).collect::<Vec<_>>()
    });
    let force_zero = force.iter().all(Q::is_zero);
    let torque_zero = mx::is_zero_matrix(&torque)?;
    let four_d_cons = force4.iter().all(Q::is_zero) && mx::is_zero_matrix(&torque4)?;
    let ang_cons = check_angular_conservation()?;
    Ok((bianchi_val, force_zero, torque_zero, four_d_cons, ang_cons))
}

fn evaluate_area_and_page(input: &Value) -> Result<(AreaModel, Vec<PageStep>, Q), GravError> {
    let n = field_usize(input, "tetrahedra", 2, 256)?;
    let a = field_usize(input, "area", 12, 1024)?;
    let steps = field_usize(input, "steps", a / 2, 1024)?;
    let d = field_usize(input, "alphabet", 2, 256)? as u32;
    let tau = field_q(input, "tau", rq(1, 2))?;
    let kappa = field_q(input, "kappa", rq(1, 4))?;
    let glued = parse_glued(input, n)?;
    let area = area_model(n, &glued, d)?;
    let page = page_curve(a, steps, d, &tau, &kappa)?;
    Ok((area, page, tau))
}

fn init_slice_and_skew(
    input: &Value,
    tau: &Q,
) -> Result<
    (
        CauchySlice,
        ::linear_algebra::backend::basic_matrix::BasicMatrix<Q>,
        (usize, usize),
    ),
    GravError,
> {
    let mut slice = CauchySlice::new(parse_positions(input)?, parse_tetrahedra(input)?)?;
    let skew = mx::from_rows(vec![
        vec![ri(0), ri(-1), ri(0)],
        vec![ri(1), ri(0), ri(0)],
        vec![ri(0), ri(0), ri(0)],
    ])?;
    let (&(u, v), _) = slice.holonomies().first_key_value().ok_or("EMPTY_EDGES")?;
    slice.set_connection(u, v, &skew, tau)?;
    Ok((slice, skew, (u, v)))
}

fn prepare_slice_and_relax(
    input: &Value,
    tau: &Q,
) -> Result<
    (
        CauchySlice,
        CauchySlice,
        Vec<Value>,
        bool,
        bool,
        bool,
        usize,
        bool,
    ),
    GravError,
> {
    let (mut slice, skew, (u, v)) = init_slice_and_skew(input, tau)?;
    let frozen_initial = slice.holonomies().clone();
    let initial_area = slice.constraints().boundary_area;
    let freeze = input
        .get("freeze_boundary")
        .and_then(Value::as_bool)
        .unwrap_or(false);
    let relax_steps = field_usize(input, "relaxation_steps", 2, 4)?;
    let (history, master_nonincreasing, variance_nonincreasing) =
        run_relaxation_loop(&mut slice, relax_steps, freeze)?;
    let boundary_fixed = !freeze
        || slice
            .boundary_edges()
            .iter()
            .all(|e| slice.holonomies()[e] == frozen_initial[e]);
    let (bracket, induced, anomaly) = slice.scalar_anomaly(u, v, &ri(2), &ri(3))?;
    let anomaly_ok = bracket == induced + anomaly;
    let mut evolved = slice.clone();
    let generators = BTreeMap::from([((u, v), skew)]);
    evolved.evolve(&generators, &vec![rq(1, 100); slice.positions().len()])?;
    Ok((
        slice,
        evolved,
        history,
        master_nonincreasing,
        variance_nonincreasing,
        boundary_fixed,
        initial_area,
        anomaly_ok,
    ))
}

fn evaluate(input: &Value) -> Result<Value, GravError> {
    let (area, page, tau) = evaluate_area_and_page(input)?;
    let (
        slice,
        evolved,
        history,
        master_nonincreasing,
        variance_nonincreasing,
        boundary_fixed,
        initial_area,
        anomaly_ok,
    ) = prepare_slice_and_relax(input, &tau)?;
    let (bianchi_val, force_zero, torque_zero, four_d_cons, ang_cons) =
        compute_bianchi_and_angular(&slice)?;
    let (regge, tetrad_orth) = check_regge_and_tetrad(&tau)?;
    let final_constraints = slice.constraints();
    Ok(
        json!({"authority_effect":"None","scope":"declared combinatorial entropy and rational constraint models; no continuum gravity, physical unitarity, or convergence theorem","area":area,"page":page,"constraints":history,"relaxation":{"master_nonincreasing":master_nonincreasing,"variance_nonincreasing":variance_nonincreasing,"converged":final_constraints.variance.is_zero()},"bianchi":bianchi_val,"checks":{"global_force_zero":force_zero,"global_torque_zero":torque_zero,"four_dimensional_conservation":four_d_cons,"angular_momentum_conservation":ang_cons,"regge_boundary_nilpotency":regge,"four_dimensional_tetrad":tetrad_orth,"connections_isometric":slice.holonomies().values().all(is_orthogonal),"boundary_area_preserved":initial_area==final_constraints.boundary_area,"frozen_boundary_connections_preserved":boundary_fixed,"master_nonnegative":final_constraints.master>=ri(0),"scalar_anomaly_definition":anomaly_ok,"evolution_isometric":evolved.holonomies().values().all(is_orthogonal)},"limitations":["Entropy A/4 is an imposed convention; Page endpoint zero follows from the imposed area schedule.","Global central-force cancellation does not imply each vertex Bianchi sum is zero.","Master self-commutation is scalar arithmetic; gauge/diffeomorphism zeros in the source are declared.","Zero-volume tetrahedra and unused slice vertices are refused.","Relaxation records observed descent; finite steps do not establish convergence."]}),
    )
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn area_and_page() {
        assert!(area_model(2, &[[(0, 0), (1, 0)], [(0, 0), (1, 1)]], 2).is_err());
        let p = page_curve(12, 6, 2, &rq(1, 2), &rq(1, 4)).unwrap();
        assert_eq!(p[3].entropy, "3/2");
        assert_eq!(p[6].entropy, "0");
        assert!(page_curve(3, 2, 2, &ri(1), &ri(0)).is_err());
    }
    #[test]
    fn gravity_checks() {
        let v = run(&Value::Null).unwrap();
        assert!(v["checks"].as_object().unwrap().values().all(|v| v == true));
    }
    #[test]
    fn malformed_carrier() {
        assert!(CauchySlice::new(vec![[ri(0), ri(0), ri(0)]; 3], vec![[0, 1, 2, 2]]).is_err());
    }
}
