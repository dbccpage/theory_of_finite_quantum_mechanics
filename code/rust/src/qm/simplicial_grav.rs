//! Exact declared simplicial models, with no continuum-gravity or unitarity inference.
use crate::qm::finite_witness::{field_q, field_usize, parse_q, qstr, qvec};
use crate::linear_algebra::matrix as mx;
use num_traits::Zero;
use omega_general_relativity::simplicial_dynamics::{
    bianchi, emit_angular, CauchySlice, Constraints, ReggeFourSimplex,
};
use omega_lie_theory::cayley::{cayley_transform, is_orthogonal};
use omega_number_theory::rational::{ri, rq, Rational as Q};
use serde_json::{json, Value};
use std::collections::BTreeMap;

pub use omega_quantum_physics::simplicial_entropy_schedule::{
    area_model, page_curve, AreaModel, PageStep,
};

fn constraints_json(c: &Constraints) -> Value {
    json!({"gauss":c.gauss.iter().map(|v|qvec(v)).collect::<Vec<_>>(),"vector":c.vector.iter().map(|v|qvec(v)).collect::<Vec<_>>(),"scalar":qvec(&c.scalar),"master":qstr(&c.master),"curvature":qvec(&c.curvature),"variance":qstr(&c.variance),"boundary_area":c.boundary_area})
}

pub fn run(input: &Value) -> Result<Value, String> {
    evaluate(input).map_err(|e| e.to_string())
}
fn evaluate(
    input: &Value,
) -> Result<Value, omega_general_relativity::simplicial_dynamics::SimplicialDynamicsError> {
    let n = field_usize(input, "tetrahedra", 2, 256)?;
    let a = field_usize(input, "area", 12, 1024)?;
    let steps = field_usize(input, "steps", a / 2, 1024)?;
    let d = field_usize(input, "alphabet", 2, 256)? as u32;
    let tau = field_q(input, "tau", rq(1, 2))?;
    let kappa = field_q(input, "kappa", rq(1, 4))?;
    let glued = if let Some(g) = input.get("glued") {
        serde_json::from_value::<Vec<[(usize, usize); 2]>>(g.clone())
            .map_err(|_| "INVALID_GLUING")?
    } else {
        (1..n).map(|i| [(i - 1, 1), (i, 0)]).collect()
    };
    let area = area_model(n, &glued, d)?;
    let page = page_curve(a, steps, d, &tau, &kappa)?;
    let positions = if let Some(v) = input.get("positions") {
        let rows = v.as_array().ok_or("INVALID_POSITIONS")?;
        rows.iter()
            .map(|v| {
                let x = v.as_array().ok_or("INVALID_POSITION")?;
                if x.len() != 3 {
                    return Err("INVALID_POSITION".into());
                }
                Ok([parse_q(&x[0])?, parse_q(&x[1])?, parse_q(&x[2])?])
            })
            .collect::<Result<Vec<_>, String>>()?
    } else {
        vec![
            [ri(0), ri(0), ri(0)],
            [ri(1), ri(0), ri(0)],
            [ri(0), ri(1), ri(0)],
            [ri(0), ri(0), ri(1)],
            [ri(0), ri(0), ri(-1)],
        ]
    };
    let tetrahedra = if let Some(t) = input.get("cells") {
        serde_json::from_value(t.clone()).map_err(|_| "INVALID_CELLS")?
    } else {
        vec![[0, 1, 2, 3], [0, 1, 2, 4]]
    };
    let mut slice = CauchySlice::new(positions, tetrahedra)?;
    let skew = vec![
        vec![ri(0), ri(-1), ri(0)],
        vec![ri(1), ri(0), ri(0)],
        vec![ri(0), ri(0), ri(0)],
    ];
    let skew = mx::from_rows(skew)?;
    let (&(u, v), _) = slice.holonomies().first_key_value().ok_or("EMPTY_EDGES")?;
    slice.set_connection(u, v, &skew, &tau)?;
    let frozen_initial = slice.holonomies().clone();
    let initial = slice.constraints();
    let mut history = vec![constraints_json(&initial)];
    let mut master_nonincreasing = true;
    let mut variance_nonincreasing = true;
    for _ in 0..field_usize(input, "relaxation_steps", 2, 4)? {
        let (dm, dv) = slice.relaxation_step(
            &rq(1, 10),
            input
                .get("freeze_boundary")
                .and_then(Value::as_bool)
                .unwrap_or(false),
        )?;
        master_nonincreasing &= dm <= ri(0);
        variance_nonincreasing &= dv <= ri(0);
        history.push(constraints_json(&slice.constraints()));
    }
    let freeze = input
        .get("freeze_boundary")
        .and_then(Value::as_bool)
        .unwrap_or(false);
    let boundary_fixed = !freeze
        || slice
            .boundary_edges()
            .iter()
            .all(|e| slice.holonomies()[e] == frozen_initial[e]);
    let (bracket, induced, anomaly) = slice.scalar_anomaly(u, v, &ri(2), &ri(3))?;
    let mut evolved = slice.clone();
    let generators = BTreeMap::from([((u, v), skew.clone())]);
    evolved.evolve(&generators, &vec![rq(1, 100); slice.positions().len()])?;
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
        .map(|(i, p)| {
            let mut p = p.clone();
            p.push(ri(i as i64));
            p
        })
        .collect();
    let (_, force4, torque4) = bianchi(&p4, &hinges)?;
    let mut jb = mx::zeros(4, 4)?;
    let mut jr = jb.clone();
    emit_angular(
        &mut jb,
        &mut jr,
        &[ri(1), ri(2), ri(3), ri(4)],
        &[ri(2), ri(-1), ri(3), ri(0)],
    )?;
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
    let regge = mx::is_zero_matrix(&simplex.boundary_bianchi()?)
        && simplex
            .tetrahedron_bianchi([0, 1, 2, 3], false)?
            .as_slice()
            .iter()
            .all(Q::is_zero);
    let tetrad = cayley_transform(&simplex.hinge_bivector([0, 1, 2])?, &tau)?;
    Ok(
        json!({"authority_effect":"None","scope":"declared combinatorial entropy and rational constraint models; no continuum gravity, physical unitarity, or convergence theorem","area":area,"page":page,"constraints":history,"relaxation":{"master_nonincreasing":master_nonincreasing,"variance_nonincreasing":variance_nonincreasing,"converged":slice.constraints().variance.is_zero()},"bianchi":{"local":local.iter().map(|v|qvec(v)).collect::<Vec<_>>(),"total_force":qvec(&force),"torque":mx::to_rows(&torque)?.iter().map(|v|qvec(v)).collect::<Vec<_>>()},"checks":{"global_force_zero":force.iter().all(Q::is_zero),"global_torque_zero":mx::is_zero_matrix(&torque),"four_dimensional_conservation":force4.iter().all(Q::is_zero)&&mx::is_zero_matrix(&torque4),"angular_momentum_conservation":mx::is_zero_matrix(&mx::add(&jb,&jr)?),"regge_boundary_nilpotency":regge,"four_dimensional_tetrad":is_orthogonal(&tetrad),"connections_isometric":slice.holonomies().values().all(is_orthogonal),"boundary_area_preserved":initial.boundary_area==slice.constraints().boundary_area,"frozen_boundary_connections_preserved":boundary_fixed,"master_nonnegative":slice.constraints().master>=ri(0),"scalar_anomaly_definition":bracket==induced+anomaly,"evolution_isometric":evolved.holonomies().values().all(is_orthogonal)},"limitations":["Entropy A/4 is an imposed convention; Page endpoint zero follows from the imposed area schedule.","Global central-force cancellation does not imply each vertex Bianchi sum is zero.","Master self-commutation is scalar arithmetic; gauge/diffeomorphism zeros in the source are declared.","Zero-volume tetrahedra and unused slice vertices are refused.","Relaxation records observed descent; finite steps do not establish convergence."]}),
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
