//! The registry-relative tower walk: lift pressure, holonomy commutator
//! pressure, the seven-row interface registry adjudicated by computation, the
//! transition ledger's refusal rule, and the exact norm-selection branches.
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::matrix;
use omega_kernel::resource_limits::OperationLimits;
use omega_number_theory::cyclotomic::GaussianRat;
use omega_quantum_physics::tower_walk_validator::{
    find_lift_trigger, half_trace_norm_2x2, holonomy_commutator, rotational_edge_norm,
    scalar_edge_norm, TowerWalkError,
};

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;
use omega_holonomy::{DiscreteConnection, ExactMatrix as FieldMatrix};
use omega_number_theory::quadratic::Surd;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::exact_channel::ExactKrausChannel;
use omega_quantum_physics::exact_hermitian::{gi, gq};

use finite_qm_native::m2_quantum_packet::{verify, worked_example_packet, M2Refusal};
use finite_qm_native::tower_walk_validator::{
    audit_registry, canonical_prerequisites, declared_registry, validate_tower_walk,
    CandidateInterface, DeclaredCandidate, FailureWitness, ForcedLiftPrerequisites,
    ForcedLiftScope, Prerequisite, RegistryTerminal, TransitionStatus,
};
use omega_policy::trichotomy::ObstructionDiagnosticClass;
use omega_quantum_physics::gauge_cochain_complex::ClassificationWitness;

fn rational_2x2(a: [(i64, i64); 4]) -> FieldMatrix<BigRational> {
    FieldMatrix::try_new(2, 2, a.iter().map(|&(n, d)| rq(n, d)).collect()).unwrap()
}

// ---------------------------------------------------------------------------
// Lift pressure
// ---------------------------------------------------------------------------

#[test]
fn a_context_that_separates_merged_points_is_a_lift_trigger() {
    let projection = [0, 0, 1, 1];
    let identity = vec![0, 1, 2, 3];
    let swap_middle = vec![0, 2, 1, 3];
    assert_eq!(
        find_lift_trigger(&projection, std::slice::from_ref(&identity)).unwrap(),
        None
    );
    let witness = find_lift_trigger(&projection, &[identity, swap_middle])
        .unwrap()
        .unwrap();
    assert_eq!((witness.x, witness.y, witness.context), (0, 1, 1));
    // A faithful projection merges nothing, so no context can separate a merged pair.
    assert_eq!(
        find_lift_trigger(&[0, 1, 2, 3], &[vec![3, 2, 1, 0]]).unwrap(),
        None
    );
}

#[test]
fn lift_trigger_inputs_are_validated() {
    assert_eq!(
        find_lift_trigger(&[], &[]),
        Err(TowerWalkError::EmptyCarrier)
    );
    assert!(matches!(
        find_lift_trigger(&[0, 0], &[vec![0]]),
        Err(TowerWalkError::ContextLength {
            context: 0,
            expected: 2,
            actual: 1
        })
    ));
    assert!(matches!(
        find_lift_trigger(&[0, 0], &[vec![0, 7]]),
        Err(TowerWalkError::ContextOutOfRange {
            context: 0,
            point: 7
        })
    ));
}

#[test]
fn noncommuting_holonomies_are_detected_exactly() {
    let limits = OperationLimits::holonomy();
    let rotation = rational_2x2([(3, 5), (-4, 5), (4, 5), (3, 5)]);
    let reflection = rational_2x2([(1, 1), (0, 1), (0, 1), (-1, 1)]);
    let identity = FieldMatrix::try_identity(2).unwrap();
    let build = |second_loop: FieldMatrix<BigRational>| {
        let mut connection = DiscreteConnection::new(2, limits);
        connection
            .set_connection("a", "b", rotation.clone())
            .unwrap();
        connection
            .set_connection("b", "c", identity.clone())
            .unwrap();
        connection
            .set_connection("c", "a", identity.clone())
            .unwrap();
        connection.set_connection("a", "d", second_loop).unwrap();
        connection
            .set_connection("d", "c", identity.clone())
            .unwrap();
        connection
    };
    let pressured = build(reflection);
    let commutator =
        holonomy_commutator(&pressured, &["a", "b", "c", "a"], &["a", "d", "c", "a"]).unwrap();
    assert!(commutator.data.as_slice().iter().any(|x| !x.is_zero()));
    // A second loop carrying R^2 commutes with the first: no operator-order pressure.
    let calm = build(rotation.matmul(&rotation).unwrap());
    let commutator =
        holonomy_commutator(&calm, &["a", "b", "c", "a"], &["a", "d", "c", "a"]).unwrap();
    assert!(commutator.data.as_slice().iter().all(Zero::is_zero));
}

// ---------------------------------------------------------------------------
// The seven-row registry and minimality relative to it
// ---------------------------------------------------------------------------

#[test]
fn the_declared_registry_has_exactly_one_resolver() {
    let audit = audit_registry(&declared_registry(), &worked_example_packet(rq(1, 2)));
    use CandidateInterface::*;
    let expected = vec![
        (
            ScalarL1,
            RegistryTerminal::Fail(FailureWitness::NoStateEffectStructure),
        ),
        (
            RotationalL1L2,
            RegistryTerminal::Fail(FailureWitness::NoBornPairingOrCptp),
        ),
        (
            ClassicalContextualGluing,
            RegistryTerminal::Fail(FailureWitness::NoGlobalSection {
                assignments_checked: 512,
            }),
        ),
        (GptConvex, RegistryTerminal::Refuse),
        (
            RealHilbertRebit,
            RegistryTerminal::Fail(FailureWitness::LocalTomography {
                local: 9,
                joint: 10,
            }),
        ),
        (QuaternionicGuarded, RegistryTerminal::Refuse),
        (ComplexHilbertCptp, RegistryTerminal::Resolve),
    ];
    assert_eq!(audit.rows, expected);
    assert_eq!(audit.minimal_interface(), Some(ComplexHilbertCptp));
}

#[test]
fn a_failed_m2_replay_removes_the_only_resolver() {
    let mut packet = worked_example_packet(rq(1, 2));
    packet.states[0] = matrix::from_rows(vec![
        vec![gq(3, 2, 0, 1), gi(0, 0)],
        vec![gi(0, 0), gq(-1, 2, 0, 1)],
    ])
    .unwrap();
    let audit = audit_registry(&declared_registry(), &packet);
    assert_eq!(
        audit.rows.last().unwrap(),
        &(
            CandidateInterface::ComplexHilbertCptp,
            RegistryTerminal::Fail(FailureWitness::M2Replay(M2Refusal::InvalidState(0)))
        )
    );
    assert_eq!(audit.minimal_interface(), None);
}

#[test]
fn a_born_defect_dominates_a_packet_that_replays() {
    // p = 1/3 is a probability, so the packet replays, but Tr(E rho) = 1/2.
    let packet = worked_example_packet(rq(1, 3));
    let verified = verify(packet.clone()).unwrap();
    let classification = verified
        .classify(&verified.declared_born_residual())
        .unwrap();
    assert_eq!(
        classification.class,
        ObstructionDiagnosticClass::ActiveClosureFailure
    );
    assert_eq!(
        classification.witness,
        ClassificationWitness::BornDefect {
            entry: 0,
            value: rq(-1, 6)
        }
    );
    // The registry terminal agrees with the classification: the defect fails the row.
    let audit = audit_registry(&declared_registry(), &packet);
    assert_eq!(
        audit.rows.last().unwrap(),
        &(
            CandidateInterface::ComplexHilbertCptp,
            RegistryTerminal::Fail(FailureWitness::BornDefect {
                entry: 0,
                defect: rq(-1, 6)
            })
        )
    );
    assert_eq!(audit.minimal_interface(), None);
    // The canonical walk therefore has neither Resolve nor a minimal interface.
    let pre = canonical_prerequisites(&packet);
    assert!(!pre.resolves);
    assert_eq!(
        validate_tower_walk(&pre).unwrap_err(),
        vec![Prerequisite::Resolve, Prerequisite::MinimalInterface]
    );
}

#[test]
fn minimality_is_relative_to_the_rows_declared() {
    let packet = worked_example_packet(rq(1, 2));
    // A declaration flag supplies no composite replay and cannot add a resolver.
    let mut widened = declared_registry();
    widened[3] = DeclaredCandidate {
        interface: CandidateInterface::GptConvex,
        composite_rule_declared: true,
    };
    let declared_only = audit_registry(&widened, &packet);
    assert_eq!(declared_only.rows[3].1, RegistryTerminal::Refuse);
    assert_eq!(
        declared_only.minimal_interface(),
        Some(CandidateInterface::ComplexHilbertCptp)
    );
    // Both complex rows independently replay the packet; two resolving rows are ambiguous.
    widened.push(declared_registry()[6]);
    let ambiguous = audit_registry(&widened, &packet);
    assert_eq!(
        ambiguous
            .rows
            .iter()
            .filter(|(_, terminal)| *terminal == RegistryTerminal::Resolve)
            .count(),
        2
    );
    assert_eq!(ambiguous.minimal_interface(), None);
    // A two-row registry still has the complex packet as its unique resolver.
    let narrow = [declared_registry()[0], declared_registry()[6]];
    assert_eq!(
        audit_registry(&narrow, &packet).minimal_interface(),
        Some(CandidateInterface::ComplexHilbertCptp)
    );
}

// ---------------------------------------------------------------------------
// The transition ledger
// ---------------------------------------------------------------------------

#[test]
fn the_canonical_walk_emits_a_registry_relative_ledger() {
    let ledger =
        validate_tower_walk(&canonical_prerequisites(&worked_example_packet(rq(1, 2)))).unwrap();
    assert_eq!(
        ledger.forced_lift_scope,
        ForcedLiftScope::DeclaredRegistryOnly(CandidateInterface::ComplexHilbertCptp)
    );
    assert!(!ledger.universal_forced_lift_proved);
    assert!(!ledger.origin_derivation_proved);
    assert!(!ledger.full_survives_descent_claim);
    assert!(!ledger.external_sealed_terminal_supplied);
    let status = |t: &str| {
        ledger
            .rows
            .iter()
            .find(|r| r.transition == t)
            .unwrap()
            .status
    };
    assert_eq!(
        status("Phi1(q) > 0 => LicensedLift"),
        TransitionStatus::Refused
    );
    assert_eq!(
        status("LiftTrigger => LicensedLift"),
        TransitionStatus::Refused
    );
    assert_eq!(
        status("StructureDerived => IsAuth"),
        TransitionStatus::Refused
    );
    assert_eq!(status("D(x,y) = y - x"), TransitionStatus::Derived);
}

#[test]
fn the_ledger_is_refused_when_any_antecedent_is_absent() {
    let base = canonical_prerequisites(&worked_example_packet(rq(1, 2)));
    type Removal = fn(&mut ForcedLiftPrerequisites);
    let cases: [(Removal, Prerequisite); 5] = [
        (|p| p.open_comm = false, Prerequisite::OpenComm),
        (|p| p.lift_protocol = false, Prerequisite::LiftProtocol),
        (|p| p.admissible = false, Prerequisite::Admissible),
        (|p| p.valid_transport = false, Prerequisite::ValidTransport),
        (|p| p.resolves = false, Prerequisite::Resolve),
    ];
    for (drop, which) in cases {
        let mut pre = base.clone();
        drop(&mut pre);
        assert_eq!(validate_tower_walk(&pre).unwrap_err(), vec![which]);
    }
}

#[test]
fn open_minimality_remains_an_explicit_condition_but_failed_minimality_is_refused() {
    let packet = worked_example_packet(rq(1, 2));
    let mut pre = canonical_prerequisites(&packet);
    pre.minimality = None;
    let ledger = validate_tower_walk(&pre).unwrap();
    assert_eq!(
        ledger.forced_lift_scope,
        ForcedLiftScope::ConditionalOnMinimality
    );

    let mut widened = declared_registry();
    widened[5] = DeclaredCandidate {
        interface: CandidateInterface::QuaternionicGuarded,
        composite_rule_declared: true,
    };
    let declared_only = audit_registry(&widened, &packet);
    assert_eq!(declared_only.rows[5].1, RegistryTerminal::Refuse);
    assert_eq!(
        declared_only.minimal_interface(),
        Some(CandidateInterface::ComplexHilbertCptp)
    );
    widened.push(declared_registry()[6]);
    pre.minimality = Some(audit_registry(&widened, &packet));
    assert_eq!(
        pre.minimality
            .as_ref()
            .unwrap()
            .rows
            .iter()
            .filter(|(_, terminal)| *terminal == RegistryTerminal::Resolve)
            .count(),
        2
    );
    assert_eq!(
        validate_tower_walk(&pre).unwrap_err(),
        vec![Prerequisite::MinimalInterface]
    );
}

// ---------------------------------------------------------------------------
// Norm-selection branches
// ---------------------------------------------------------------------------

#[test]
fn the_rotational_branch_is_an_exact_surd_sum_and_rotation_invariant() {
    let weights = vec![ri(1), ri(1)];
    let vectors = vec![vec![ri(3), ri(4)], vec![ri(1), ri(1)]];
    let norm = rotational_edge_norm(&weights, &vectors).unwrap();
    assert_eq!(norm.terms().get(&BigInt::from(1)), Some(&ri(5)));
    assert_eq!(norm.terms().get(&BigInt::from(2)), Some(&ri(1)));
    assert_eq!(norm.as_rational(), None);
    // Rotate every edge vector by the Pythagorean rotation (3/5, 4/5).
    let rotate = |v: &Vec<Rational>| {
        vec![
            rq(3, 5) * &v[0] - rq(4, 5) * &v[1],
            rq(4, 5) * &v[0] + rq(3, 5) * &v[1],
        ]
    };
    let rotated: Vec<Vec<Rational>> = vectors.iter().map(rotate).collect();
    assert_eq!(rotational_edge_norm(&weights, &rotated).unwrap(), norm);
    // The scalar L1 branch is not rotation invariant: (3, 4) -> (-7/5, 24/5).
    assert_eq!(scalar_edge_norm(&weights, &vectors[0]).unwrap(), ri(7));
    assert_eq!(scalar_edge_norm(&weights, &rotated[0]).unwrap(), rq(31, 5));
    assert_eq!(
        rotational_edge_norm(&[ri(2)], &[vec![ri(6), ri(8)]])
            .unwrap()
            .as_rational(),
        Some(ri(20))
    );
}

#[test]
fn half_trace_norm_of_hermitian_2x2_matrices_is_exact() {
    let traceless = matrix::from_rows(vec![
        vec![gq(3, 5, 0, 1), gq(4, 5, 0, 1)],
        vec![gq(4, 5, 0, 1), gq(-3, 5, 0, 1)],
    ])
    .unwrap();
    assert_eq!(
        half_trace_norm_2x2(&traceless).unwrap(),
        Surd::rational(ri(1))
    );
    let positive = matrix::from_rows(vec![
        vec![gi(1, 0), gi(0, 0)],
        vec![gi(0, 0), gq(1, 2, 0, 1)],
    ])
    .unwrap();
    assert_eq!(
        half_trace_norm_2x2(&positive).unwrap(),
        Surd::rational(rq(3, 4))
    );
    let golden =
        matrix::from_rows(vec![vec![gi(1, 0), gi(1, 0)], vec![gi(1, 0), gi(0, 0)]]).unwrap();
    assert_eq!(
        half_trace_norm_2x2(&golden).unwrap(),
        Surd::new(rq(1, 2), &ri(5)).unwrap()
    );
    let skew =
        matrix::from_rows(vec![vec![gi(0, 0), gi(1, 0)], vec![gi(-1, 0), gi(0, 0)]]).unwrap();
    assert_eq!(
        half_trace_norm_2x2(&skew),
        Err(TowerWalkError::NotHermitian2x2)
    );
}

#[test]
fn cptp_monotonicity_does_not_select_the_trace_distance_normalization() {
    let square = |s: &Surd| s.square();
    let x = matrix::from_rows(vec![
        vec![gq(1, 2, 0, 1), gq(1, 3, 1, 4)],
        vec![gq(1, 3, -1, 4), gq(-1, 2, 0, 1)],
    ])
    .unwrap();
    let rho_minus_sigma = matrix::from_rows(vec![
        vec![gq(1, 2, 0, 1), gq(-1, 2, 0, 1)],
        vec![gq(-1, 2, 0, 1), gq(-1, 2, 0, 1)],
    ])
    .unwrap();
    let pauli_x =
        matrix::from_rows(vec![vec![gi(0, 0), gi(1, 0)], vec![gi(1, 0), gi(0, 0)]]).unwrap();
    let pauli_z =
        matrix::from_rows(vec![vec![gi(1, 0), gi(0, 0)], vec![gi(0, 0), gi(-1, 0)]]).unwrap();
    let rotation = matrix::from_rows(vec![
        vec![gq(3, 5, 0, 1), gq(-4, 5, 0, 1)],
        vec![gq(4, 5, 0, 1), gq(3, 5, 0, 1)],
    ])
    .unwrap();
    let pauli_mixture = vec![
        matrix::scale(&matrix::identity(2).unwrap(), &gq(2, 3, 0, 1)).unwrap(),
        matrix::scale(&pauli_x, &gq(2, 3, 0, 1)).unwrap(),
        matrix::scale(&pauli_z, &gq(1, 3, 0, 1)).unwrap(),
    ];
    let dephasing = vec![
        matrix::from_rows(vec![vec![gi(1, 0), gi(0, 0)], vec![gi(0, 0), gi(0, 0)]]).unwrap(),
        matrix::from_rows(vec![vec![gi(0, 0), gi(0, 0)], vec![gi(0, 0), gi(1, 0)]]).unwrap(),
    ];
    // j is the squared half trace norm, compared exactly.
    let j = |m: &BasicMatrix<GaussianRat>| square(&half_trace_norm_2x2(m).unwrap());
    assert_eq!(j(&x), rq(61, 144));
    for kraus in [pauli_mixture, dephasing.clone(), vec![rotation.clone()]] {
        let channel = ExactKrausChannel::from_operators(kraus).unwrap();
        for input in [&x, &rho_minus_sigma] {
            assert!(j(&channel.apply(input).unwrap()) <= j(input));
        }
    }
    // The bound is strict under dephasing and an equality under a unitary.
    assert_eq!(
        j(&ExactKrausChannel::from_operators(dephasing)
            .unwrap()
            .apply(&x)
            .unwrap()),
        rq(1, 4)
    );
    assert_eq!(
        j(&ExactKrausChannel::from_operators(vec![rotation])
            .unwrap()
            .apply(&x)
            .unwrap()),
        j(&x)
    );
    // Every positive multiple of a contractive functional is contractive, so
    // monotonicity cannot fix the factor 1/2. Distinguishability does: the two
    // orthogonal pure states |0><0| and |1><1| are at half-trace distance 1.
    assert_eq!(
        half_trace_norm_2x2(&pauli_z).unwrap(),
        Surd::rational(ri(1))
    );
}
