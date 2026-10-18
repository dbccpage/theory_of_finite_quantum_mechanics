//! Finite quantum packets for M2: the verifier's typed refusals, the cochain
//! identity d1 d0 = 0, and the decidable, witness-producing classification,
//! cross-checked against omega_functional's Phi/Gamma trichotomy.
use linear_algebra::backend::basic_matrix::{BasicMatrix, OperationLimits};
use linear_algebra::exact_field::{involution, matrix};

use num_traits::Zero;
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_policy::trichotomy::ObstructionDiagnosticClass;
use omega_quantum_physics::exact_hermitian::{self, gi, gq};

use finite_qm_native::m2_quantum_packet::{verify, worked_example_packet, M2Refusal};
use omega_quantum_physics::gauge_cochain_complex::{
    BornEntry, ClassificationWitness, M2Packet, QuantumResidual, ResidualError, VerifiedM2Packet,
};

fn paper_generator() -> BasicMatrix<GaussianRat> {
    matrix::from_rows(vec![vec![gi(0, 0), gi(1, 0)], vec![gi(-1, 0), gi(0, 0)]]).unwrap()
}

fn zero2() -> BasicMatrix<GaussianRat> {
    matrix::zeros(2, 2).unwrap()
}

#[test]
fn the_worked_example_is_accepted_and_d1_d0_vanishes() {
    let verified = verify(worked_example_packet(rq(1, 2))).unwrap();
    assert!(verified
        .d1_d0()
        .unwrap()
        .as_slice()
        .iter()
        .all(Zero::is_zero));
    // The commutators the paper computes by hand.
    let a = paper_generator();
    let x = verified.gauge_displacement(&a).unwrap();
    assert_eq!(
        x.drho[0],
        matrix::from_rows(vec![vec![gi(0, 0), gi(-1, 0)], vec![gi(-1, 0), gi(0, 0)]]).unwrap()
    );
    assert_eq!(
        x.de[0],
        matrix::from_rows(vec![vec![gi(1, 0), gi(0, 0)], vec![gi(0, 0), gi(-1, 0)]]).unwrap()
    );
    // Born invariance under exact gauge repair.
    assert_eq!(
        verified.born_coboundary(&x).unwrap(),
        vec![Rational::zero()]
    );
    assert_eq!(verified.born_residuals(), vec![Rational::zero()]);
}

#[test]
fn a_gauge_displacement_classifies_as_exact_repair_with_a_replayable_witness() {
    let verified = verify(worked_example_packet(rq(1, 2))).unwrap();
    let x = verified.gauge_displacement(&paper_generator()).unwrap();
    let classification = verified.classify(&x).unwrap();
    assert_eq!(
        classification.class,
        ObstructionDiagnosticClass::ExactRepair
    );
    let ClassificationWitness::Gauge(witness) = classification.witness else {
        panic!("exact repair must carry a gauge witness");
    };
    // The witness is anti-Hermitian and reproduces x; it may differ from the
    // paper's A by a generator commuting with every state and effect.
    assert_eq!(
        involution::adjoint(&witness).unwrap(),
        matrix::scale(&witness, &gi(-1, 0)).unwrap()
    );
    assert_eq!(verified.gauge_displacement(&witness).unwrap(), x);
    assert!(verified.quotient_mass_l1(&x).unwrap().value().is_zero());
}

#[test]
fn a_declared_born_mismatch_lands_in_c2_as_active_closure_failure() {
    let verified = verify(worked_example_packet(rq(3, 4))).unwrap();
    assert_eq!(verified.born_residuals(), vec![rq(1, 4)]);
    let x = verified.declared_born_residual();
    let classification = verified.classify(&x).unwrap();
    assert_eq!(
        classification.class,
        ObstructionDiagnosticClass::ActiveClosureFailure
    );
    assert_eq!(
        classification.witness,
        ClassificationWitness::BornDefect {
            entry: 0,
            value: rq(1, 4)
        }
    );
    let functional = verified.functional_trichotomy(&x).unwrap();
    assert_eq!(
        functional.diagnostic_class(),
        ObstructionDiagnosticClass::ActiveClosureFailure
    );
}

#[test]
fn a_closed_residual_outside_the_gauge_image_carries_a_separator() {
    let verified = verify(worked_example_packet(rq(1, 2))).unwrap();
    // dp = 1 and dE_0 = I: d1 x = 1 - Tr(I rho) = 0, but no gauge move changes dp.
    let x = QuantumResidual {
        dp: vec![ri(1)],
        de: vec![matrix::identity(2).unwrap(), zero2()],
        drho: vec![zero2()],
    };
    assert_eq!(
        verified.born_coboundary(&x).unwrap(),
        vec![Rational::zero()]
    );
    let classification = verified.classify(&x).unwrap();
    assert_eq!(
        classification.class,
        ObstructionDiagnosticClass::ClosedResidual
    );
    let ClassificationWitness::Separator(lambda) = classification.witness else {
        panic!("closed residual must carry a separator");
    };
    let on_generators =
        matrix::multiply_vector(&matrix::transpose(verified.d0()).unwrap(), &lambda).unwrap();
    assert!(
        on_generators.iter().all(Zero::is_zero),
        "separator must kill im d0"
    );
    let functional = verified.functional_trichotomy(&x).unwrap();
    assert_eq!(
        functional.diagnostic_class(),
        ObstructionDiagnosticClass::ClosedResidual
    );
    assert!(!verified.quotient_mass_l1(&x).unwrap().value().is_zero());
}

#[test]
fn classification_agrees_with_the_functional_trichotomy_on_mixed_residuals() {
    let packet = M2Packet {
        states: vec![
            matrix::diagonal(&[gi(1, 0), gi(0, 0)]).unwrap(),
            matrix::from_rows(vec![
                vec![gq(1, 2, 0, 1), gq(0, 1, 1, 4)],
                vec![gq(0, 1, -1, 4), gq(1, 2, 0, 1)],
            ])
            .unwrap(),
        ],
        effects: vec![
            matrix::diagonal(&[gi(1, 0), gi(0, 0)]).unwrap(),
            matrix::diagonal(&[gi(0, 0), gi(1, 0)]).unwrap(),
        ],
        povms: vec![vec![0, 1]],
        channels: vec![],
        born_table: vec![
            BornEntry {
                state: 0,
                effect: 0,
                probability: ri(1),
            },
            BornEntry {
                state: 1,
                effect: 0,
                probability: rq(1, 2),
            },
            BornEntry {
                state: 1,
                effect: 1,
                probability: rq(1, 3),
            },
        ],
    };
    let verified = verify(packet).unwrap();
    assert!(verified
        .d1_d0()
        .unwrap()
        .as_slice()
        .iter()
        .all(Zero::is_zero));
    assert_eq!(
        verified.born_residuals(),
        vec![Rational::zero(), Rational::zero(), rq(-1, 6)]
    );
    let gauge = verified.gauge_displacement(&paper_generator()).unwrap();
    let declared = verified.declared_born_residual();
    for x in [gauge, declared] {
        let ours = verified.classify(&x).unwrap().class;
        let functional = verified
            .functional_trichotomy(&x)
            .unwrap()
            .diagnostic_class();
        assert_eq!(ours, functional);
    }
}

#[test]
fn a_rational_amplitude_damping_channel_is_accepted_and_applied_exactly() {
    let mut packet = worked_example_packet(rq(1, 2));
    packet
        .states
        .push(matrix::diagonal(&[gi(0, 0), gi(1, 0)]).unwrap());
    let k0 = matrix::diagonal(&[gi(1, 0), gq(3, 5, 0, 1)]).unwrap();
    let k1 = matrix::from_rows(vec![
        vec![gi(0, 0), gq(4, 5, 0, 1)],
        vec![gi(0, 0), gi(0, 0)],
    ])
    .unwrap();
    packet.channels.push(vec![k0, k1]);
    let verified = verify(packet).unwrap();
    let out = verified.apply_channel(1, 1).unwrap();
    assert_eq!(
        out,
        matrix::diagonal(&[gq(16, 25, 0, 1), gq(9, 25, 0, 1)]).unwrap()
    );
    assert_eq!(matrix::trace(&out).unwrap(), GaussianRat::one());
    assert!(exact_hermitian::is_positive_semidefinite(&out));
}

#[test]
fn the_verifier_refuses_in_its_declared_order() {
    let good = worked_example_packet(rq(1, 2));

    let mut p = good.clone();
    p.states.clear();
    assert_eq!(verify(p).unwrap_err(), M2Refusal::MissingField("states"));

    let mut p = good.clone();
    p.states[0] = matrix::identity(3).unwrap();
    assert!(matches!(
        verify(p).unwrap_err(),
        M2Refusal::UnsupportedCarrier {
            field: "state",
            index: 0,
            rows: 3,
            cols: 3
        }
    ));

    let mut p = good.clone();
    p.states[0] = matrix::diagonal(&[gq(3, 2, 0, 1), gq(-1, 2, 0, 1)]).unwrap();
    assert_eq!(verify(p).unwrap_err(), M2Refusal::InvalidState(0));

    let mut p = good.clone();
    p.states[0] = matrix::diagonal(&[gq(1, 2, 0, 1), gq(1, 4, 0, 1)]).unwrap();
    assert_eq!(verify(p).unwrap_err(), M2Refusal::InvalidState(0));

    let mut p = good.clone();
    p.effects[1] = matrix::scale(&matrix::identity(2).unwrap(), &gi(2, 0)).unwrap();
    assert_eq!(verify(p).unwrap_err(), M2Refusal::InvalidEffect(1));

    let mut p = good.clone();
    p.povms = vec![vec![0]];
    assert_eq!(verify(p).unwrap_err(), M2Refusal::InvalidPovm(0));

    let mut p = good.clone();
    p.channels = vec![vec![matrix::scale(
        &matrix::identity(2).unwrap(),
        &gi(2, 0),
    )
    .unwrap()]];
    assert_eq!(verify(p).unwrap_err(), M2Refusal::InvalidChannel(0));

    let mut p = good.clone();
    p.born_table[0].probability = rq(3, 2);
    assert_eq!(verify(p).unwrap_err(), M2Refusal::InconsistentBornEntry(0));

    let mut p = good.clone();
    p.born_table[0].effect = 5;
    assert_eq!(verify(p).unwrap_err(), M2Refusal::InconsistentBornEntry(0));

    // A packet with a bad state and a bad effect is refused for the state first.
    let mut p = good;
    p.states[0] = matrix::diagonal(&[gq(3, 2, 0, 1), gq(-1, 2, 0, 1)]).unwrap();
    p.effects[0] = matrix::scale(&matrix::identity(2).unwrap(), &gi(2, 0)).unwrap();
    assert_eq!(verify(p).unwrap_err(), M2Refusal::InvalidState(0));
}

#[test]
fn residuals_must_live_in_c1() {
    let verified = verify(worked_example_packet(rq(1, 2))).unwrap();
    let short = QuantumResidual {
        dp: vec![],
        de: vec![zero2(), zero2()],
        drho: vec![zero2()],
    };
    assert!(matches!(
        verified.classify(&short),
        Err(ResidualError::Shape {
            field: "dp",
            expected: 1,
            actual: 0
        })
    ));
    let skew = matrix::from_rows(vec![vec![gi(0, 0), gi(1, 0)], vec![gi(0, 0), gi(0, 0)]]).unwrap();
    let non_hermitian = QuantumResidual {
        dp: vec![Rational::zero()],
        de: vec![skew, zero2()],
        drho: vec![zero2()],
    };
    assert!(matches!(
        verified.classify(&non_hermitian),
        Err(ResidualError::NotHermitian {
            field: "dE",
            index: 0
        })
    ));
}

#[test]
fn the_gauge_core_refuses_invalid_generators_indices_and_construction_budgets() {
    let packet = worked_example_packet(rq(1, 2));
    let verified = verify(packet.clone()).unwrap();
    for invalid in [matrix::identity(3).unwrap(), matrix::identity(2).unwrap()] {
        assert_eq!(
            verified.gauge_displacement(&invalid),
            Err(ResidualError::InvalidGaugeGenerator)
        );
    }
    assert!(verified.gauge_displacement(&paper_generator()).is_ok());
    assert!(matches!(
        verified.apply_channel(packet.channels.len(), 0),
        Err(ResidualError::UndeclaredIndex {
            field: "channel",
            ..
        })
    ));
    assert!(matches!(
        verified.apply_channel(0, packet.states.len()),
        Err(ResidualError::UndeclaredIndex { field: "state", .. })
    ));
    for limits in [
        OperationLimits {
            max_elements: 1,
            max_scalar_ops: usize::MAX,
        },
        OperationLimits {
            max_elements: usize::MAX,
            max_scalar_ops: 1,
        },
    ] {
        assert_eq!(
            VerifiedM2Packet::from_declaration_with_limits(packet.clone(), limits),
            Err(ResidualError::ResourceBudget)
        );
    }
    assert!(VerifiedM2Packet::from_declaration_with_limits(
        packet,
        exact_hermitian::exact_limits()
    )
    .is_ok());
}
