use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::finite_cochain_map::{CochainMap, CochainWindow};
use num_rational::BigRational;
use tfqm_category_theory::context_reflection::ContextSystem;
use tfqm_functional::phi1::ExactPhi1Certificate;
use omega_wdp::coda::diagnostic_routing::DiagnosticPacket;
use omega_wdp::prime_algos::finite_routing::*;
fn q(x: i64) -> BigRational {
    BigRational::from_integer(x.into())
}
fn cert(values: &[i64]) -> ExactPhi1Certificate {
    ExactPhi1Certificate {
        omega: values.iter().map(|&x| q(x)).collect(),
        d0: vec![vec![q(0)]; values.len()],
        weights: vec![q(1); values.len()],
        alpha: vec![q(0)],
        primal_residual: values.iter().map(|&x| q(x)).collect(),
        dual_witness: values.iter().map(|x| q(x.signum())).collect(),
        reported_value: q(values.iter().map(|x| x.abs()).sum()),
    }
}
fn packet(values: &[i64], d1: Vec<Vec<BigRational>>) -> DiagnosticPacket {
    DiagnosticPacket::replay(
        ContextSystem::new(vec![0], vec![vec![0]], 1).unwrap(),
        cert(values),
        d1,
    )
    .unwrap()
}
fn m(x: i64) -> BasicMatrix<BigRational> {
    BasicMatrix::try_from_fn(1, 1, |_, _| q(x)).unwrap()
}
#[test]
fn actual_lift_squares_transport_and_inclusion_are_independent_checks() {
    let source = packet(&[2], vec![vec![q(0)]]);
    let target = packet(&[4], vec![vec![q(0)]]);
    let window = CochainWindow::try_new([1, 1, 1], m(0), m(0)).unwrap();
    let map = CochainMap::try_new(&window, &window, [m(1), m(2), m(1)]).unwrap();
    let mut contract = LiftContract {
        map,
        require_coordinate_inclusion: false,
    };
    assert_eq!(check_lift(&source, &target, Some(&contract)), Ok(()));
    assert_eq!(
        check_lift(&source, &source, Some(&contract)),
        Err(FiniteRefusal::InvalidLift)
    );
    contract.require_coordinate_inclusion = true;
    assert_eq!(
        check_lift(&source, &target, Some(&contract)),
        Err(FiniteRefusal::InvalidLift)
    );
    assert_eq!(
        check_lift(&source, &target, None),
        Err(FiniteRefusal::MissingLift)
    );
    let inclusion = LiftContract {
        map: CochainMap::try_new(&window, &window, [m(1), m(1), m(1)]).unwrap(),
        require_coordinate_inclusion: true,
    };
    assert_eq!(check_lift(&source, &source, Some(&inclusion)), Ok(()));
    assert!(target.phi1().value() > source.phi1().value());
}
#[test]
fn closure_damage_is_checked_even_when_phi_strictly_descends() {
    let before = packet(&[3, 0], vec![vec![q(0), q(1)]]);
    assert_eq!(
        guarded_edit(&before, cert(&[1, 1]), None),
        Err(FiniteRefusal::MissingGuard)
    );
    assert_eq!(
        guarded_edit(
            &before,
            cert(&[1, 1]),
            Some(&ClosureGuard {
                max_gamma_increase: q(0)
            })
        ),
        Err(FiniteRefusal::ClosureDamageExceeded)
    );
    let after = guarded_edit(
        &before,
        cert(&[1, 1]),
        Some(&ClosureGuard {
            max_gamma_increase: q(1),
        }),
    )
    .unwrap();
    assert_eq!(after.classification().gamma2_value(), &q(1));
    assert_eq!(
        guarded_edit(
            &before,
            cert(&[3, 0]),
            Some(&ClosureGuard {
                max_gamma_increase: q(1)
            })
        ),
        Err(FiniteRefusal::NoStrictDescent)
    );
}
#[test]
fn declared_terminal_table_and_real_fixedpoint_not_closedness_alone() {
    let p = packet(&[2], vec![vec![q(0)]]);
    let policy = TerminalPolicy {
        rows: [
            Some(FiniteTerminal::ExactCertified),
            Some(FiniteTerminal::StabilizedSurvivor),
            Some(FiniteTerminal::ActiveCertified),
        ],
    };
    assert_eq!(
        terminalize(&p, None, None),
        Err(FiniteRefusal::MissingPolicy)
    );
    assert_eq!(
        terminalize(&p, Some(&policy), None),
        Err(FiniteRefusal::MissingStabilization)
    );
    let mut d = FiniteDynamics {
        packets: vec![p.clone(), p.clone()],
        next: vec![1, 0],
    };
    assert_eq!(
        terminalize(
            &p,
            Some(&policy),
            Some((&d, FixedPointWitness { state: 0 }))
        ),
        Err(FiniteRefusal::InvalidStabilization)
    );
    d.next[0] = 0;
    assert_eq!(
        terminalize(
            &p,
            Some(&policy),
            Some((&d, FixedPointWitness { state: 0 }))
        ),
        Ok(FiniteTerminal::StabilizedSurvivor)
    );
    let bad = TerminalPolicy {
        rows: [None, Some(FiniteTerminal::ExactCertified), None],
    };
    assert_eq!(
        terminalize(&p, Some(&bad), None),
        Err(FiniteRefusal::IncompatibleTerminal)
    );
}
