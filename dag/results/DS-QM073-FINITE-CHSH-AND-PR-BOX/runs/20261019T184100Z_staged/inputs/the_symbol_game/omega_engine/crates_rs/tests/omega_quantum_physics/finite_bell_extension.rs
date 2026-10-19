use num_rational::BigRational as Q;
use omega_finite_probability::local_deterministic::LocalVertexLimits;
use omega_number_theory::rational::ri;
use omega_quantum_physics::finite_bell_extension::*;
use omega_solvers::solver_convex_farkas_feasibility::{FeasibilityError, FeasibilityVerdict};
fn limits() -> BellLimits {
    BellLimits {
        vertices: LocalVertexLimits {
            assignments: 256,
            coordinates: 256,
            entries: 65536,
        },
        solver_cells: 1_000_000,
    }
}
fn isotropic(v: Q) -> FiniteBellProblem {
    let mut rows = Vec::new();
    for x in 0..2 {
        for y in 0..2 {
            rows.push(
                (0..4)
                    .map(|k| {
                        if ((k % 2) ^ (k / 2)) == (x * y) {
                            (ri(1) + &v) / ri(4)
                        } else {
                            (ri(1) - &v) / ri(4)
                        }
                    })
                    .collect(),
            );
        }
    }
    FiniteBellProblem::new(vec![2, 2], vec![2, 2], rows, limits()).unwrap()
}
#[test]
fn full_support_does_not_imply_positive_bell_extension() {
    let p = isotropic(ri(3) / ri(5));
    assert_eq!(p.supported_assignments().len(), 16);
    let c = p.decide(10_000).unwrap();
    let FeasibilityVerdict::Infeasible { multipliers } = &c else {
        panic!("CHSH 12/5 is nonlocal")
    };
    p.verify(&c).unwrap();
    p.system().verify_farkas(multipliers).unwrap();
    let zero = FeasibilityVerdict::Infeasible {
        multipliers: vec![ri(0); multipliers.len()],
    };
    assert!(p.verify(&zero).is_err());
    let mut bad = multipliers.clone();
    bad[0] = -ri(1);
    assert!(p
        .verify(&FeasibilityVerdict::Infeasible { multipliers: bad })
        .is_err());
}
#[test]
fn boundary_local_model_decodes_actual_response_functions() {
    let p = isotropic(ri(1) / ri(2));
    let c = p.decide(10_000).unwrap();
    let FeasibilityVerdict::Feasible { point } = &c else {
        panic!("local CHSH boundary")
    };
    let model = p.local_model(point).unwrap();
    assert_eq!(model.iter().map(|r| r.weight.clone()).sum::<Q>(), ri(1));
    assert!(model
        .iter()
        .all(|r| r.left.len() == 2 && r.right.len() == 2));
    assert!(isotropic(ri(3) / ri(5)).verify(&c).is_err());
    let mut negative = point.clone();
    negative[0] = ri(-1);
    assert!(p.local_model(&negative).is_err());
    assert!(p
        .verify(&FeasibilityVerdict::Feasible { point: vec![] })
        .is_err());
}
#[test]
fn nonbinary_and_extra_setting_models_have_exact_extensions() {
    for (left, right) in [(vec![3, 2], vec![2]), (vec![2, 2, 2], vec![2, 2])] {
        let rows = left
            .iter()
            .flat_map(|&a| {
                right
                    .iter()
                    .map(move |&b| vec![ri(1) / ri((a * b) as i64); a * b])
            })
            .collect();
        let p = FiniteBellProblem::new(left.clone(), right.clone(), rows, limits()).unwrap();
        let c = p.decide(10_000).unwrap();
        p.verify(&c).unwrap();
        let FeasibilityVerdict::Feasible { point } = c else {
            panic!("independent uniform model")
        };
        for r in p.local_model(&point).unwrap() {
            assert!(r.left.iter().zip(&left).all(|(a, n)| a < n));
            assert!(r.right.iter().zip(&right).all(|(a, n)| a < n));
        }
    }
}
#[test]
fn signalling_is_an_obstruction_under_explicit_locality_premises() {
    // Bob's only outcome changes with Alice's setting.
    let p = FiniteBellProblem::new(
        vec![1, 1],
        vec![2],
        vec![vec![ri(1), ri(0)], vec![ri(0), ri(1)]],
        limits(),
    )
    .unwrap();
    let c = p.decide(1000).unwrap();
    assert!(matches!(c, FeasibilityVerdict::Infeasible { .. }));
    p.verify(&c).unwrap();
}
#[test]
fn malformed_tables_and_budget_failures_are_not_verdicts() {
    assert!(FiniteBellProblem::new(vec![0], vec![2], vec![], limits()).is_err());
    assert!(FiniteBellProblem::new(vec![2], vec![2], vec![vec![ri(1); 4]], limits()).is_err());
    assert!(FiniteBellProblem::new(
        vec![1],
        vec![1],
        vec![vec![Q::new_raw(1.into(), 0.into())]],
        limits()
    )
    .is_err());
    assert_eq!(
        FiniteBellProblem::new(
            vec![1],
            vec![1],
            vec![vec![ri(1)]],
            BellLimits {
                solver_cells: 0,
                ..limits()
            }
        ),
        Err(BellExtensionError::SolverCells)
    );
    assert_eq!(
        isotropic(ri(1) / ri(2)).decide(0),
        Err(BellExtensionError::Solver(
            FeasibilityError::BudgetExhausted
        ))
    );
}

#[test]
fn nonuniform_mixed_outcomes_bind_response_order_to_experimental_cells() {
    // f=(2,0), g=(1): mixed-radix assignment 2 + 3*0 + 6*1 = 8.
    let mut first = vec![ri(0); 6];
    first[5] = ri(1);
    let mut second = vec![ri(0); 4];
    second[2] = ri(1);
    let p = FiniteBellProblem::new(vec![3, 2], vec![2], vec![first, second], limits()).unwrap();
    let mut point = vec![ri(0); 12];
    point[8] = ri(1);
    let responses = p.local_model(&point).unwrap();
    assert_eq!(
        responses,
        vec![LocalResponse {
            left: vec![2, 0],
            right: vec![1],
            weight: ri(1)
        }]
    );
    point.swap(7, 8);
    assert!(p.local_model(&point).is_err());
}
