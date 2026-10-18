//! The show-the-packet protocol as a replayable checker: typed refusals in the
//! protocol's order, replay of the declared finite algebra, the certified
//! class and logical visibility of a defect history, the host-computed
//! terminal, and the worked rotated-surface-code example. Every check is exact.

use num_bigint::BigInt;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_policy::trichotomy::ObstructionDiagnosticClass;
use omega_solvers::data_cochain_packet::FiniteCochainPacket;

use finite_qm_native::realization_packet_protocol::{
    terminalize, ClaimScope, EvidenceKind, PacketRefusal, PacketTerminal, PairingBound,
    RealizationPacket,
};
use omega_quantum_physics::threshold_repair_certificate::ThresholdScaling;

/// A square `a b c d` with diagonal `a -> c`; the triangle `a b c` is filled
/// and `a c d` is a hole. Edges: 0 `a->b`, 1 `b->c`, 2 `c->d`, 3 `d->a`, 4 `a->c`.
fn complex() -> FiniteCochainPacket {
    FiniteCochainPacket::with_unit_weights(
        FiniteCochainPacket::build_complex(
            &["a", "b", "c", "d"],
            &[("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"), ("a", "c")],
            &[&["a", "b", "c"]],
        )
        .unwrap(),
    )
    .unwrap()
}

fn columns(d0: &[Vec<Rational>]) -> Vec<Vec<Rational>> {
    (0..d0[0].len())
        .map(|j| d0.iter().map(|row| row[j].clone()).collect())
        .collect()
}

fn edge(index: usize) -> Vec<Rational> {
    (0..5).map(|e| ri(i64::from(e == index))).collect()
}

/// The circulation around the hole `a -> c -> d -> a`.
fn hole_circulation() -> Vec<Rational> {
    vec![ri(0), ri(0), ri(1), ri(1), ri(1)]
}

/// The boundary circulation of the filled face `a -> b -> c -> a`.
fn face_circulation() -> Vec<Rational> {
    vec![ri(1), ri(1), ri(0), ri(0), ri(-1)]
}

fn worked_scaling() -> ThresholdScaling {
    ThresholdScaling::new(ri(1), rq(1, 1000), rq(1, 100)).unwrap()
}

fn complete_packet() -> RealizationPacket {
    let k = complex();
    RealizationPacket {
        physical_carrier: Some("transmon array, 1 us cycle, correction window one cycle".into()),
        logical_distinction: Some("one logical qubit".into()),
        repair_space: Some(4),
        defect_space: Some(5),
        repair_boundary: Some(k.d0().to_vec()),
        repair_image: Some(columns(k.d0())),
        residual_quotient: Some(2),
        closure_map: Some(k.d1().to_vec()),
        defect_history: Some(edge(2)),
        repair_capacity: Some(rq(1, 100)),
        defect_rate: Some(rq(1, 1000)),
        mixing_bound: Some(rq(1, 500)),
        logical_witnesses: Some(vec![hole_circulation(), face_circulation()]),
        pairing_bound: Some(PairingBound::Measured(rq(1, 100))),
        evidence: Some(vec![EvidenceKind::Experiment]),
        accepted_overhead: Some("d^2 physical qubits per logical qubit".into()),
        claim: Some(ClaimScope::FiniteBenchmark {
            windows: 1000,
            visibility: ri(2),
        }),
        claimed_terminal: None,
    }
}

#[test]
fn a_complete_packet_is_replayed_and_terminalized() {
    let report = terminalize(&complete_packet()).unwrap();
    assert_eq!((report.repair_rank(), report.quotient_dimension()), (3, 2));
    assert_eq!(report.class(), ObstructionDiagnosticClass::ClosedResidual);
    assert_eq!(
        (report.residual_mass(), report.closure_defect()),
        (&ri(1), &ri(0))
    );
    // Visible to the hole's circulation, invisible to the filled face's.
    assert_eq!(report.witness_pairings(), &[ri(1), ri(0)]);
    assert_eq!(report.gap(), &rq(-11, 1000));
    assert_eq!(
        report.terminal(),
        &PacketTerminal::FailureNotEstablished { windows: 1000 }
    );
}

#[test]
fn each_missing_field_is_refused_in_the_protocol_order() {
    type Removal = fn(&mut RealizationPacket);
    let removals: [(Removal, PacketRefusal); 17] = [
        (
            |p| p.physical_carrier = None,
            PacketRefusal::NoPhysicalCarrier,
        ),
        (
            |p| p.logical_distinction = None,
            PacketRefusal::NoLogicalDistinction,
        ),
        (|p| p.repair_space = None, PacketRefusal::NoRepairSpace),
        (|p| p.defect_space = None, PacketRefusal::NoDefectSpace),
        (
            |p| p.repair_boundary = None,
            PacketRefusal::NoRepairBoundary,
        ),
        (|p| p.repair_image = None, PacketRefusal::NoRepairImage),
        (
            |p| p.residual_quotient = None,
            PacketRefusal::NoResidualQuotient { computed: 2 },
        ),
        (|p| p.closure_map = None, PacketRefusal::NoClosureMap),
        (
            |p| p.defect_history = None,
            PacketRefusal::NoProjectionDefectModel,
        ),
        (
            |p| p.repair_capacity = None,
            PacketRefusal::NoRepairCapacityBound,
        ),
        (
            |p| p.defect_rate = None,
            PacketRefusal::NoDefectProductionBound,
        ),
        (|p| p.mixing_bound = None, PacketRefusal::NoMixingBound),
        (
            |p| p.logical_witnesses = None,
            PacketRefusal::NoLogicalWitnessFamily { index: None },
        ),
        (|p| p.pairing_bound = None, PacketRefusal::NoPairingBound),
        (|p| p.evidence = None, PacketRefusal::NoEvidenceTerminalizer),
        (
            |p| p.accepted_overhead = None,
            PacketRefusal::NoAcceptedOverhead,
        ),
        (|p| p.claim = None, PacketRefusal::NoHumanSignificantScale),
    ];
    for (index, (remove, expected)) in removals.iter().enumerate() {
        let mut packet = complete_packet();
        remove(&mut packet);
        assert_eq!(terminalize(&packet).unwrap_err(), *expected);
        // With every later field removed as well, the same refusal comes first.
        for (later, _) in &removals[index + 1..] {
            later(&mut packet);
        }
        assert_eq!(terminalize(&packet).unwrap_err(), *expected);
    }
    let mut blank = complete_packet();
    blank.physical_carrier = Some("   ".into());
    assert_eq!(
        terminalize(&blank).unwrap_err(),
        PacketRefusal::NoPhysicalCarrier
    );
    assert_eq!(
        terminalize(&RealizationPacket::default()).unwrap_err(),
        PacketRefusal::NoPhysicalCarrier
    );
}

#[test]
fn declared_values_that_do_not_replay_are_refused() {
    let refused = |edit: &dyn Fn(&mut RealizationPacket)| {
        let mut packet = complete_packet();
        edit(&mut packet);
        terminalize(&packet).unwrap_err()
    };
    assert_eq!(
        refused(&|p| p.defect_space = Some(0)),
        PacketRefusal::NoDefectSpace
    );
    assert_eq!(
        refused(&|p| p.repair_space = Some(3)),
        PacketRefusal::NoRepairBoundary
    );
    // A vector outside im d0, and a declared image one dimension short.
    assert_eq!(
        refused(&|p| p.repair_image.as_mut().unwrap().push(edge(2))),
        PacketRefusal::NoRepairImage
    );
    assert_eq!(
        refused(&|p| {
            p.repair_image.as_mut().unwrap().truncate(2);
        }),
        PacketRefusal::NoRepairImage
    );
    assert_eq!(
        refused(&|p| p.residual_quotient = Some(3)),
        PacketRefusal::NoResidualQuotient { computed: 2 }
    );
    // A face row that misses one of its edges breaks d1 d0 = 0.
    assert_eq!(
        refused(&|p| p.closure_map = Some(vec![vec![ri(1), ri(1), ri(0), ri(0), ri(0)]])),
        PacketRefusal::NoClosureMap
    );
    assert_eq!(
        refused(&|p| p.defect_history = Some(vec![ri(1)])),
        PacketRefusal::NoProjectionDefectModel
    );
    assert_eq!(
        refused(&|p| p.repair_capacity = Some(rq(-1, 100))),
        PacketRefusal::NoRepairCapacityBound
    );
    assert_eq!(
        refused(&|p| p.mixing_bound = Some(rq(-1, 500))),
        PacketRefusal::NoMixingBound
    );
    assert_eq!(
        refused(&|p| p.logical_witnesses.as_mut().unwrap().push(edge(0))),
        PacketRefusal::NoLogicalWitnessFamily { index: Some(2) }
    );
    assert_eq!(
        refused(&|p| p.logical_witnesses = Some(vec![])),
        PacketRefusal::NoLogicalWitnessFamily { index: None }
    );
    assert_eq!(
        refused(&|p| p.pairing_bound = Some(PairingBound::Measured(rq(3, 2)))),
        PacketRefusal::NoPairingBound
    );
    assert_eq!(
        refused(&|p| p.evidence = Some(vec![])),
        PacketRefusal::NoEvidenceTerminalizer
    );
    assert_eq!(
        refused(&|p| p.claim = Some(ClaimScope::FiniteBenchmark {
            windows: 10,
            visibility: ri(0)
        })),
        PacketRefusal::NoHumanSignificantScale
    );
}

#[test]
fn the_defect_history_class_and_its_logical_visibility_are_computed() {
    let k = complex();
    let run = |omega: Vec<Rational>| {
        let mut packet = complete_packet();
        packet.defect_history = Some(omega);
        terminalize(&packet).unwrap()
    };
    let coboundary = k
        .primitive_difference(&[ri(0), ri(2), ri(5), ri(-1)])
        .unwrap();
    let exact = run(coboundary);
    assert_eq!(exact.class(), ObstructionDiagnosticClass::ExactRepair);
    assert_eq!(exact.residual_mass(), &ri(0));
    assert_eq!(exact.witness_pairings(), &[ri(0), ri(0)]);
    let active = run(edge(0));
    assert_eq!(
        active.class(),
        ObstructionDiagnosticClass::ActiveClosureFailure
    );
    assert_eq!(
        (active.residual_mass(), active.closure_defect()),
        (&ri(1), &ri(1))
    );
    assert_eq!(active.witness_pairings(), &[ri(0), ri(1)]);
    // A replayed Gamma2 > 0 is an open obstruction: it is the terminal, not a scoped success.
    assert_eq!(
        active.terminal(),
        &PacketTerminal::ActiveClosureFailure { gamma2: ri(1) }
    );
    assert_eq!(
        exact.terminal(),
        &PacketTerminal::FailureNotEstablished { windows: 1000 }
    );
    // Twice the hole edge plus a coboundary: the class, its mass and its pairing double.
    let mut shifted = k
        .primitive_difference(&[ri(1), ri(0), ri(0), ri(0)])
        .unwrap();
    for (value, hole_edge) in shifted.iter_mut().zip(edge(2)) {
        *value += ri(2) * hole_edge;
    }
    let doubled = run(shifted);
    assert_eq!(doubled.class(), ObstructionDiagnosticClass::ClosedResidual);
    assert_eq!(doubled.residual_mass(), &ri(2));
    assert_eq!(doubled.witness_pairings(), &[ri(2), ri(0)]);
    // A closed residual (Gamma2 = 0) is a resource question, so the recurrence still decides.
    assert!(matches!(
        doubled.terminal(),
        PacketTerminal::FailureNotEstablished { .. } | PacketTerminal::ResidualForced { .. }
    ));
    // The hole's circulation is a witness, not a closed cochain: it crosses the filled face.
    assert_eq!(
        k.face_coboundary(&hole_circulation()).unwrap(),
        vec![ri(-1)]
    );
}

#[test]
fn the_finite_benchmark_terminal_follows_the_recurrence() {
    let with = |lambda: Rational, windows: u64, visibility: Rational| {
        let mut packet = complete_packet();
        packet.defect_rate = Some(lambda);
        packet.claim = Some(ClaimScope::FiniteBenchmark {
            windows,
            visibility,
        });
        terminalize(&packet).unwrap().terminal().clone()
    };
    // Gap 20/1000 - 10/1000 - 2/1000 = 1/125 from Phi1 = 1 to 2: floor(125) + 1 windows.
    assert_eq!(
        with(rq(1, 50), 1000, ri(2)),
        PacketTerminal::ResidualForced {
            windows: BigInt::from(126)
        }
    );
    assert_eq!(
        with(rq(1, 50), 125, ri(2)),
        PacketTerminal::FailureNotEstablished { windows: 125 }
    );
    assert_eq!(
        with(rq(1, 50), 126, ri(2)),
        PacketTerminal::ResidualForced {
            windows: BigInt::from(126)
        }
    );
    // Already visible: the certified residual 1 exceeds the threshold 1/2.
    assert_eq!(
        with(rq(1, 1000), 10, rq(1, 2)),
        PacketTerminal::ResidualForced {
            windows: BigInt::from(0)
        }
    );
    assert_eq!(
        with(rq(1, 1000), 10, ri(1)),
        PacketTerminal::FailureNotEstablished { windows: 10 }
    );
}

#[test]
fn the_worked_surface_code_lower_bound_is_inconclusive_when_scoped_and_overreaches_when_scaled() {
    // The source's illustrative numbers: p = 1e-3, p_th = 1e-2, overhead d^2.
    let finite = terminalize(&complete_packet()).unwrap();
    assert_eq!(
        finite.terminal(),
        &PacketTerminal::FailureNotEstablished { windows: 1000 }
    );

    let scalable = ClaimScope::HumanSignificantScale {
        visibility: rq(1, 100),
        max_distance: 101,
    };
    let claim = |pairing: PairingBound, evidence: &[EvidenceKind], lambda: Rational| {
        let mut packet = complete_packet();
        packet.claim = Some(scalable.clone());
        packet.pairing_bound = Some(pairing);
        packet.evidence = Some(evidence.to_vec());
        packet.defect_rate = Some(lambda);
        terminalize(&packet)
    };
    let measured = PairingBound::Measured(rq(1, 100));
    let theorem = PairingBound::Scaling(worked_scaling());
    let above = PairingBound::Scaling(ThresholdScaling::new(ri(1), rq(1, 50), rq(1, 100)).unwrap());
    // Benchmark evidence alone, for a scalable claim.
    assert_eq!(
        claim(measured.clone(), &[EvidenceKind::Experiment], rq(1, 1000)),
        Err(PacketRefusal::ClaimOverreach)
    );
    assert_eq!(
        claim(measured, &[EvidenceKind::Theorem], rq(1, 1000)),
        Err(PacketRefusal::ClaimOverreach)
    );
    // A scaling with no theorem among its evidence, one above threshold, and a positive declared gap.
    for evidence in [
        &[EvidenceKind::Simulation][..],
        &[EvidenceKind::Experiment, EvidenceKind::Simulation][..],
    ] {
        assert_eq!(
            claim(theorem.clone(), evidence, rq(1, 1000)),
            Err(PacketRefusal::ClaimOverreach)
        );
    }
    assert_eq!(
        claim(above, &[EvidenceKind::Theorem], rq(1, 1000)),
        Err(PacketRefusal::ClaimOverreach)
    );
    assert_eq!(
        claim(theorem.clone(), &[EvidenceKind::Theorem], rq(1, 50)),
        Err(PacketRefusal::ClaimOverreach)
    );
    // Conditional on the imported hypotheses: below 1/100 from distance 5 on.
    for evidence in [
        &[EvidenceKind::Theorem][..],
        &[EvidenceKind::Theorem, EvidenceKind::Experiment][..],
    ] {
        assert_eq!(
            claim(theorem.clone(), evidence, rq(1, 1000))
                .unwrap()
                .terminal(),
            &PacketTerminal::ConditionalSurvival { least_distance: 5 }
        );
    }
    // A declared overhead that stops short of the suppressing distance overreaches.
    let mut short = complete_packet();
    short.claim = Some(ClaimScope::HumanSignificantScale {
        visibility: rq(1, 100),
        max_distance: 3,
    });
    short.pairing_bound = Some(theorem);
    short.evidence = Some(vec![EvidenceKind::Theorem]);
    assert_eq!(terminalize(&short), Err(PacketRefusal::ClaimOverreach));
}

#[test]
fn an_open_obstruction_dominates_every_resource_terminal() {
    let open = |claim: ClaimScope, pairing: PairingBound, evidence: Vec<EvidenceKind>| {
        let mut packet = complete_packet();
        packet.defect_history = Some(edge(0));
        packet.claim = Some(claim);
        packet.pairing_bound = Some(pairing);
        packet.evidence = Some(evidence);
        packet
    };
    let failure = PacketTerminal::ActiveClosureFailure { gamma2: ri(1) };
    // The finite benchmark, which the recurrence alone would call a success.
    let packet = open(
        ClaimScope::FiniteBenchmark {
            windows: 1000,
            visibility: ri(2),
        },
        PairingBound::Measured(rq(1, 100)),
        vec![EvidenceKind::Experiment],
    );
    assert_eq!(terminalize(&packet).unwrap().terminal(), &failure);
    // The theorem-backed scalable claim, which would be a conditional survival.
    let packet = open(
        ClaimScope::HumanSignificantScale {
            visibility: rq(1, 100),
            max_distance: 101,
        },
        PairingBound::Scaling(worked_scaling()),
        vec![EvidenceKind::Theorem],
    );
    assert_eq!(terminalize(&packet).unwrap().terminal(), &failure);
    // Claiming the success anyway is a terminal mismatch, not an acceptance.
    let mut packet = open(
        ClaimScope::FiniteBenchmark {
            windows: 1000,
            visibility: ri(2),
        },
        PairingBound::Measured(rq(1, 100)),
        vec![EvidenceKind::Experiment],
    );
    packet.claimed_terminal = Some(PacketTerminal::FailureNotEstablished { windows: 1000 });
    assert_eq!(
        terminalize(&packet),
        Err(PacketRefusal::TerminalMismatch {
            claimed: PacketTerminal::FailureNotEstablished { windows: 1000 },
            computed: failure.clone(),
        })
    );
    // Claiming the failure it computed is accepted.
    packet.claimed_terminal = Some(failure);
    assert!(terminalize(&packet).is_ok());
    // A malformed claim scope is still refused first, dominance or not.
    let packet = open(
        ClaimScope::FiniteBenchmark {
            windows: 1000,
            visibility: ri(0),
        },
        PairingBound::Measured(rq(1, 100)),
        vec![EvidenceKind::Experiment],
    );
    assert_eq!(
        terminalize(&packet),
        Err(PacketRefusal::NoHumanSignificantScale)
    );
}

#[test]
fn a_witness_family_of_zeros_names_no_logical_distinction() {
    let mut packet = complete_packet();
    packet.logical_witnesses = Some(vec![vec![ri(0); 5]]);
    assert_eq!(
        terminalize(&packet),
        Err(PacketRefusal::NoLogicalWitnessFamily { index: Some(0) })
    );
    // One genuine witness does not excuse a zero one.
    packet.logical_witnesses = Some(vec![hole_circulation(), vec![ri(0); 5]]);
    assert_eq!(
        terminalize(&packet),
        Err(PacketRefusal::NoLogicalWitnessFamily { index: Some(1) })
    );
}

#[test]
fn a_claimed_terminal_must_equal_the_computed_one() {
    let mut packet = complete_packet();
    packet.claimed_terminal = Some(PacketTerminal::FailureNotEstablished { windows: 1000 });
    assert!(terminalize(&packet)
        .is_ok_and(|r| r.terminal() == &PacketTerminal::FailureNotEstablished { windows: 1000 }));
    packet.claimed_terminal = Some(PacketTerminal::ConditionalSurvival { least_distance: 5 });
    assert_eq!(
        terminalize(&packet),
        Err(PacketRefusal::TerminalMismatch {
            claimed: PacketTerminal::ConditionalSurvival { least_distance: 5 },
            computed: PacketTerminal::FailureNotEstablished { windows: 1000 },
        })
    );
}

#[test]
fn the_threshold_theorem_mapping_fills_only_the_fields_it_names() {
    let k = complex();
    let mapped = RealizationPacket::from_threshold_theorem(
        &worked_scaling(),
        4,
        k.d0().to_vec(),
        vec![hole_circulation(), face_circulation()],
        "d^2 physical qubits per logical qubit",
    )
    .unwrap();
    assert_eq!(mapped.defect_rate, Some(rq(1, 1000)));
    assert_eq!(mapped.repair_capacity, Some(rq(1, 100)));
    assert_eq!(mapped.residual_quotient, Some(2));
    assert_eq!(mapped.evidence, Some(vec![EvidenceKind::Theorem]));
    // Walk the refusals: each names a field the mapping does not fill.
    type Supply = fn(&mut RealizationPacket);
    let supplies: [(Supply, PacketRefusal); 7] = [
        (
            |p| p.physical_carrier = Some("transmon array".into()),
            PacketRefusal::NoPhysicalCarrier,
        ),
        (
            |p| p.logical_distinction = Some("one logical qubit".into()),
            PacketRefusal::NoLogicalDistinction,
        ),
        (
            |p| p.repair_image = Some(columns(complex().d0())),
            PacketRefusal::NoRepairImage,
        ),
        (
            |p| p.closure_map = Some(complex().d1().to_vec()),
            PacketRefusal::NoClosureMap,
        ),
        (
            |p| p.defect_history = Some(edge(2)),
            PacketRefusal::NoProjectionDefectModel,
        ),
        (
            |p| p.mixing_bound = Some(rq(1, 500)),
            PacketRefusal::NoMixingBound,
        ),
        (
            |p| {
                p.claim = Some(ClaimScope::HumanSignificantScale {
                    visibility: rq(1, 100),
                    max_distance: 101,
                })
            },
            PacketRefusal::NoHumanSignificantScale,
        ),
    ];
    let mut packet = mapped;
    for (supply, expected) in supplies {
        assert_eq!(terminalize(&packet).unwrap_err(), expected);
        supply(&mut packet);
    }
    assert_eq!(
        terminalize(&packet).unwrap().terminal(),
        &PacketTerminal::ConditionalSurvival { least_distance: 5 }
    );
    assert_eq!(
        RealizationPacket::from_threshold_theorem(
            &worked_scaling(),
            3,
            k.d0().to_vec(),
            vec![],
            "d^2"
        ),
        Err(PacketRefusal::NoRepairBoundary)
    );
}

#[test]
fn an_empty_closure_map_cannot_hide_the_defect_history() {
    let mut packet = complete_packet();
    packet.closure_map = Some(vec![]);
    assert_eq!(terminalize(&packet), Err(PacketRefusal::NoClosureMap));
}
