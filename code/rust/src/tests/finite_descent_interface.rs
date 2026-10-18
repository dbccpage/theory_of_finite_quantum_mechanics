//! Quantum mechanics as a declared descent interface: disjoint exact and scoped
//! evidence routes over certified M2 values, projection-obstruction visibility
//! through the Phi1 dual witness, the repair-capacity recurrence, and the
//! Kraus/Choi/Stinespring presentations of one declared channel.
use linear_algebra::exact_field::{involution, matrix};

use num_bigint::BigInt;
use num_traits::Zero;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::exact_channel::{
    apply_choi, apply_stinespring, choi_is_cptp, ExactChannelError, ExactKrausChannel,
};
use omega_quantum_physics::exact_hermitian::{self, gi, gq};
use omega_solvers::data_cochain_packet::FiniteCochainPacket;

use finite_qm_native::descent_evidence_routes::{
    route_evidence, ClosureStatus, DeclaredTolerance, EvidenceClass, EvidenceRoute, RouteRefusal,
};
use finite_qm_native::m2_quantum_packet::{verify, worked_example_packet};
use omega_quantum_physics::gauge_cochain_complex::QuantumResidual;
use omega_quantum_physics::repair_capacity::{
    residual_lower_bounds, satisfies_recurrence, windows_to_exceed, RepairBudget,
    RepairCapacityError, WINDOW_BUDGET,
};

fn tol(phi: Rational, gamma: Rational) -> DeclaredTolerance {
    DeclaredTolerance::new(phi, gamma).unwrap()
}

// ---------------------------------------------------------------------------
// Evidence routes
// ---------------------------------------------------------------------------

#[test]
fn evidence_routes_partition_into_exact_and_scoped_classes() {
    let exact = route_evidence(&ri(0), &ri(0), None).unwrap();
    assert_eq!(exact, EvidenceRoute::ExactQuantumReplay);
    assert_eq!(exact.class(), EvidenceClass::Exact);
    // Declaring a tolerance keeps even a zero-error replay in the scoped class.
    let empirical = route_evidence(&ri(0), &ri(0), Some(&tol(ri(0), ri(0)))).unwrap();
    assert_eq!(empirical.class(), EvidenceClass::Scoped);
    let approx = route_evidence(&rq(1, 10), &rq(1, 100), Some(&tol(rq(1, 5), rq(1, 50)))).unwrap();
    assert_eq!(
        approx,
        EvidenceRoute::ApproxQuantumReplay {
            phi: rq(1, 10),
            gamma: rq(1, 100),
            tolerance: tol(rq(1, 5), rq(1, 50)),
            closure: ClosureStatus::WitnessedNonzeroGamma
        }
    );
    let survivor = route_evidence(&ri(3), &ri(0), None).unwrap();
    assert_eq!(survivor, EvidenceRoute::QuantumSurvivor { phi: ri(3) });
    assert_eq!(survivor.class(), EvidenceClass::Scoped);
    assert_eq!(
        route_evidence(&ri(1), &ri(2), None),
        Err(RouteRefusal::OpenObstruction { gamma: ri(2) })
    );
    assert_eq!(
        route_evidence(&ri(0), &rq(1, 2), Some(&tol(ri(1), rq(1, 10)))),
        Err(RouteRefusal::OpenObstruction { gamma: rq(1, 2) })
    );
    // Gamma inside its envelope but nonzero, with Phi outside: refused, and the
    // refusal says which coordinate left the envelope.
    let refusal = route_evidence(&ri(1), &rq(1, 100), Some(&tol(rq(1, 5), rq(1, 50)))).unwrap_err();
    assert_eq!(
        refusal,
        RouteRefusal::OpenObstructionOutsidePhiTolerance {
            phi: Box::new(ri(1)),
            gamma: Box::new(rq(1, 100))
        }
    );
    assert!(refusal.to_string().contains("within the envelope"));
    assert_eq!(
        route_evidence(&ri(-1), &ri(0), None),
        Err(RouteRefusal::NegativeValue)
    );
    assert_eq!(
        DeclaredTolerance::new(ri(-1), ri(0)),
        Err(RouteRefusal::NegativeTolerance)
    );
}

#[test]
fn certified_m2_values_route_to_exactly_one_class() {
    let exact_packet = verify(worked_example_packet(rq(1, 2))).unwrap();
    let a = matrix::from_rows(vec![vec![gi(0, 0), gi(1, 0)], vec![gi(-1, 0), gi(0, 0)]]).unwrap();
    let values = |verified: &omega_quantum_physics::gauge_cochain_complex::VerifiedM2Packet,
                  x: &QuantumResidual| {
        let t = verified.functional_trichotomy(x).unwrap();
        (t.phi1_value().clone(), t.gamma2_value().clone())
    };
    let (phi, gamma) = values(&exact_packet, &exact_packet.gauge_displacement(&a).unwrap());
    assert_eq!(
        route_evidence(&phi, &gamma, None).unwrap(),
        EvidenceRoute::ExactQuantumReplay
    );

    let mismatch = verify(worked_example_packet(rq(3, 4))).unwrap();
    let (phi, gamma) = values(&mismatch, &mismatch.declared_born_residual());
    assert_eq!((phi.clone(), gamma.clone()), (rq(1, 4), rq(1, 4)));
    assert!(route_evidence(&phi, &gamma, None).is_err());
    assert_eq!(
        route_evidence(&phi, &gamma, Some(&tol(rq(1, 2), rq(1, 2))))
            .unwrap()
            .class(),
        EvidenceClass::Scoped
    );

    let closed = QuantumResidual {
        dp: vec![ri(1)],
        de: vec![matrix::identity(2).unwrap(), matrix::zeros(2, 2).unwrap()],
        drho: vec![matrix::zeros(2, 2).unwrap()],
    };
    let (phi, gamma) = values(&exact_packet, &closed);
    assert!(gamma.is_zero() && !phi.is_zero());
    assert!(matches!(
        route_evidence(&phi, &gamma, None).unwrap(),
        EvidenceRoute::QuantumSurvivor { .. }
    ));
}

// ---------------------------------------------------------------------------
// Projection obstruction and repair capacity
// ---------------------------------------------------------------------------

#[test]
fn a_nonzero_class_stays_visible_to_its_dual_pairing_under_repair() {
    let packet = FiniteCochainPacket::with_unit_weights(
        FiniteCochainPacket::build_complex(
            &["a", "b", "c"],
            &[("a", "b"), ("b", "c"), ("c", "a")],
            &[],
        )
        .unwrap(),
    )
    .unwrap();
    let omega = vec![ri(1), ri(1), ri(1)];
    let certificate = packet.quotient_mass(&omega).unwrap();
    let z = certificate.dual_witness().to_vec();
    let pair = |x: &[Rational]| x.iter().zip(&z).map(|(a, b)| a * b).sum::<Rational>();
    assert_eq!(pair(&omega), ri(3));
    for f in [vec![ri(0), ri(5), ri(2)], vec![rq(1, 2), ri(-3), ri(7)]] {
        let repair = packet.primitive_difference(&f).unwrap();
        let repaired: Vec<Rational> = omega.iter().zip(&repair).map(|(a, b)| a + b).collect();
        assert_eq!(
            pair(&repaired),
            ri(3),
            "admissible repair cannot erase the pairing"
        );
    }
}

#[test]
fn a_persistent_positive_gap_forces_the_residual_past_any_threshold() {
    let budget = RepairBudget::new(ri(3), ri(2), rq(1, 2)).unwrap();
    assert_eq!(budget.persistent_gap(), rq(1, 2));
    assert_eq!(
        residual_lower_bounds(&ri(1), &budget, 4).unwrap(),
        vec![ri(1), rq(3, 2), ri(2), rq(5, 2), ri(3)]
    );
    // 1 + 18/2 = 10 is not above 10; 1 + 19/2 is.
    assert_eq!(
        windows_to_exceed(&ri(1), &budget, &ri(10)).unwrap(),
        Some(BigInt::from(19))
    );
    assert_eq!(
        windows_to_exceed(&ri(12), &budget, &ri(10)).unwrap(),
        Some(BigInt::zero())
    );
    assert!(satisfies_recurrence(&[ri(1), rq(3, 2), ri(2)], &budget));
    assert!(!satisfies_recurrence(&[ri(1), ri(1), ri(2)], &budget));
}

#[test]
fn a_nonpositive_gap_implies_nothing() {
    let budget = RepairBudget::new(ri(1), ri(2), ri(0)).unwrap();
    assert_eq!(budget.persistent_gap(), ri(-1));
    assert_eq!(windows_to_exceed(&ri(1), &budget, &ri(10)).unwrap(), None);
    assert_eq!(
        residual_lower_bounds(&ri(1), &budget, 3).unwrap(),
        vec![ri(1), ri(0), ri(0), ri(0)]
    );
    assert_eq!(
        RepairBudget::new(ri(-1), ri(0), ri(0)),
        Err(RepairCapacityError::Negative)
    );
    assert_eq!(
        residual_lower_bounds(&ri(-1), &budget, 1),
        Err(RepairCapacityError::Negative)
    );
    // The listing is bounded; usize::MAX windows used to overflow.
    assert_eq!(
        residual_lower_bounds(&ri(1), &budget, WINDOW_BUDGET)
            .unwrap()
            .len(),
        WINDOW_BUDGET + 1
    );
    assert_eq!(
        residual_lower_bounds(&ri(1), &budget, usize::MAX),
        Err(RepairCapacityError::WindowBudget {
            windows: usize::MAX,
            budget: WINDOW_BUDGET
        })
    );
}

// ---------------------------------------------------------------------------
// Kraus, Choi and Stinespring presentations agree on one declared channel
// ---------------------------------------------------------------------------

fn test_channels() -> Vec<ExactKrausChannel> {
    let damping = vec![
        matrix::diagonal(&[gi(1, 0), gq(3, 5, 0, 1)]).unwrap(),
        matrix::from_rows(vec![
            vec![gi(0, 0), gq(4, 5, 0, 1)],
            vec![gi(0, 0), gi(0, 0)],
        ])
        .unwrap(),
    ];
    let pauli = vec![
        matrix::scale(&matrix::identity(2).unwrap(), &gq(2, 3, 0, 1)).unwrap(),
        matrix::from_rows(vec![
            vec![gi(0, 0), gq(2, 3, 0, 1)],
            vec![gq(2, 3, 0, 1), gi(0, 0)],
        ])
        .unwrap(),
        matrix::diagonal(&[gq(1, 3, 0, 1), gq(-1, 3, 0, 1)]).unwrap(),
    ];
    let embedding = vec![matrix::from_rows(vec![
        vec![gi(1, 0), gi(0, 0)],
        vec![gi(0, 0), gq(3, 5, 0, 1)],
        vec![gi(0, 0), gq(0, 1, 4, 5)],
    ])
    .unwrap()];
    [damping, pauli, embedding]
        .into_iter()
        .map(|k| ExactKrausChannel::from_operators(k).unwrap())
        .collect()
}

#[test]
fn kraus_choi_and_stinespring_presentations_agree_on_outputs_and_pairings() {
    let inputs = vec![
        matrix::diagonal(&[gi(1, 0), gi(0, 0)]).unwrap(),
        matrix::from_rows(vec![vec![gi(0, 0), gi(1, 0)], vec![gi(0, 0), gi(0, 0)]]).unwrap(),
        matrix::from_rows(vec![
            vec![gq(1, 3, 0, 1), gq(1, 4, -1, 5)],
            vec![gq(1, 4, 1, 5), gq(2, 3, 0, 1)],
        ])
        .unwrap(),
    ];
    for channel in test_channels() {
        let (din, dout, r) = (
            channel.dim_in(),
            channel.dim_out(),
            channel.operators().len(),
        );
        let choi = channel.choi().unwrap().matrix().clone();
        assert!(choi_is_cptp(&choi, din, dout));
        let v = channel.stinespring_isometry().unwrap();
        assert_eq!(
            matrix::multiply(&involution::adjoint(&v).unwrap(), &v).unwrap(),
            matrix::identity(din).unwrap()
        );
        let mut effect = matrix::scale(&matrix::identity(dout).unwrap(), &gq(1, 2, 0, 1)).unwrap();
        effect.set(0, 0, gq(5, 6, 0, 1)).unwrap();
        for rho in &inputs {
            let kraus = channel.apply(rho).unwrap();
            assert_eq!(apply_choi(&choi, din, dout, rho).unwrap(), kraus);
            assert_eq!(apply_stinespring(&v, dout, r, rho).unwrap(), kraus);
            // Schrodinger and Heisenberg pictures give the same pairing.
            let forward = matrix::trace(&matrix::multiply(&effect, &kraus).unwrap()).unwrap();
            let backward = matrix::trace(
                &matrix::multiply(&channel.adjoint_apply(&effect).unwrap(), rho).unwrap(),
            )
            .unwrap();
            assert_eq!(forward, backward);
        }
        let state = &inputs[2];
        assert_eq!(
            matrix::trace(&channel.complementary(state).unwrap()).unwrap(),
            matrix::trace(&state).unwrap()
        );
    }
}

#[test]
fn the_transpose_map_is_positive_and_trace_preserving_but_not_completely_positive() {
    // Choi matrix of rho -> rho^T on a qubit is the swap operator.
    let mut swap = matrix::zeros(4, 4).unwrap();
    for (row, col) in [(0, 0), (1, 2), (2, 1), (3, 3)] {
        swap.set(row, col, gi(1, 0)).unwrap();
    }
    let state = matrix::from_rows(vec![
        vec![gq(1, 3, 0, 1), gq(1, 4, -1, 5)],
        vec![gq(1, 4, 1, 5), gq(2, 3, 0, 1)],
    ])
    .unwrap();
    assert_eq!(
        apply_choi(&swap, 2, 2, &state).unwrap(),
        matrix::transpose(&state).unwrap()
    );
    assert!(!choi_is_cptp(&swap, 2, 2));
    assert!(!exact_hermitian::is_positive_semidefinite(&swap));
    // A Kraus family that is not trace preserving is refused.
    let leaky = vec![matrix::diagonal(&[gi(1, 0), gq(1, 2, 0, 1)]).unwrap()];
    assert_eq!(
        ExactKrausChannel::from_operators(leaky),
        Err(ExactChannelError::NotTracePreserving { row: 1, col: 1 })
    );
    assert_eq!(
        ExactKrausChannel::from_operators(vec![]),
        Err(ExactChannelError::EmptyKrausSet)
    );
}

#[test]
fn tolerance_preserves_nonzero_gamma_and_its_declared_envelope() {
    let declared = tol(rq(1, 5), rq(1, 50));
    let route = route_evidence(&rq(1, 10), &rq(1, 100), Some(&declared)).unwrap();
    match route {
        EvidenceRoute::ApproxQuantumReplay {
            phi,
            gamma,
            tolerance,
            closure,
        } => {
            assert_eq!((phi, gamma), (rq(1, 10), rq(1, 100)));
            assert_eq!(tolerance, declared);
            assert_eq!(closure, ClosureStatus::WitnessedNonzeroGamma);
        }
        _ => panic!("nonzero obstruction was promoted"),
    }
    let route = route_evidence(&ri(0), &ri(0), Some(&declared)).unwrap();
    assert!(matches!(
        route,
        EvidenceRoute::ApproxQuantumReplay {
            closure: ClosureStatus::ExactClosed,
            ..
        }
    ));
}
