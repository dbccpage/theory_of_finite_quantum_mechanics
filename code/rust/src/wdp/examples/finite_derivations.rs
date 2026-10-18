
use std::collections::BTreeSet;

use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::semiring_lumpability::lumpable_quotient;
use omega_finite_probability::finite_valuation::BooleanValuation;
use omega_measurement::affine_calibration::{AffineCalibration, BoundedReading};
use omega_measurement::finite_chain_clock::ChainClock;
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::{ri, rq};
use omega_quantum_physics::exact_hermitian::outer;
use omega_quantum_physics::exact_instrument::ExactDensityState;
use omega_quantum_physics::instrument_repeatability::analyze_repeatability;
use omega_wdp::calibration_adapter::{
    evaluate_calibration_packet, verify_calibration_receipt, CalibrationPacket,
    NamedCalibrationStage,
};
use omega_wdp::clock_adequacy_adapter::{
    evaluate_clock_adequacy, evaluate_clock_coarsening, verify_clock_adequacy,
    verify_clock_coarsening, NamedChainClockPacket,
};
use omega_wdp::empirical_adapter::{MeasurementCover, RunTable};
use omega_wdp::empirical_repair::{repair, sampling_tolerance, verify_repair};
use omega_wdp::instrument_adapter::FiniteQuantumInstrument;
use omega_wdp::profile_evaluator::{FiniteProfile, ProfileStatus, TableEvidence};
use omega_wdp::retention::{compute_behavioral_quotient, make_cm1_static_carrier};

fn main() {
    let (classes, _) = compute_behavioral_quotient(&make_cm1_static_carrier()).unwrap();
    println!("Retention: {classes} behavioral classes");

    let clock = ChainClock::new(
        [1, 2, 3, 4].into_iter().map(ri).collect(),
        [0, 2, 5, 7, 12].into_iter().map(ri).collect(),
        ri(1),
        vec![ri(1); 4],
    )
    .unwrap();
    let full_interval = clock.interval_bound(0, 4).unwrap();
    assert_eq!(full_interval.discrepancy, ri(2));
    assert_eq!(full_interval.error_budget, ri(4));
    let clock_packet = NamedChainClockPacket::new(
        "finite-clock".into(),
        (0..=4).map(|index| format!("occurrence-{index}")).collect(),
        clock,
    )
    .unwrap();
    let clock_receipt = evaluate_clock_adequacy(&clock_packet).unwrap();
    assert!(verify_clock_adequacy(&clock_packet, &clock_receipt).unwrap());
    let coarsening = evaluate_clock_coarsening(&clock_packet, &[0, 2, 4]).unwrap();
    assert!(verify_clock_coarsening(&clock_packet, &[0, 2, 4], &coarsening).unwrap());
    println!("Clock: interval discrepancy 2 <= budget 4; adequacy and block coarsening verified");

    let valuation = BooleanValuation::try_new(
        2,
        vec![(BTreeSet::new(), ri(0)), (BTreeSet::from([0, 1]), ri(9))],
    )
    .unwrap();
    assert!(!valuation.singleton_extension_is_unique());
    println!(
        "Valuation: atom mass {}; individual witness masses are ambiguous",
        valuation.atom_masses()[0]
    );

    let transition = BasicMatrix::from_row_major(
        3,
        3,
        [2, -1, 3, 0, 1, 3, 4, -2, 1].into_iter().map(ri).collect(),
    )
    .unwrap();
    let quotient = lumpable_quotient(&transition, &[vec![0, 1], vec![2]])
        .unwrap()
        .expect("declared partition satisfies outgoing block sums");
    println!(
        "Coarse-graining: quotient [[{}, {}], [{}, {}]] preserves endpoint-block sums",
        quotient.get_ref(0, 0).unwrap(),
        quotient.get_ref(0, 1).unwrap(),
        quotient.get_ref(1, 0).unwrap(),
        quotient.get_ref(1, 1).unwrap()
    );

    let packet = CalibrationPacket::new(
        "finite-measurement".into(),
        BoundedReading::new(ri(2), rq(1, 10)).unwrap(),
        vec![
            NamedCalibrationStage::new(
                "first".into(),
                AffineCalibration::new(ri(2), ri(1), rq(1, 10), rq(1, 20), ri(0)).unwrap(),
            )
            .unwrap(),
            NamedCalibrationStage::new(
                "second".into(),
                AffineCalibration::new(ri(-3), ri(2), ri(0), ri(0), rq(1, 50)).unwrap(),
            )
            .unwrap(),
        ],
    )
    .unwrap();
    let receipt = evaluate_calibration_packet(&packet).unwrap();
    assert!(verify_calibration_receipt(&packet, &receipt).unwrap());
    let output = receipt.readings.last().unwrap();
    assert_eq!(output.center(), &ri(-13));
    assert_eq!(output.radius(), &rq(7, 5));
    println!(
        "Calibration: {} +/- {}; actual packet replay verified",
        output.center(),
        output.radius()
    );

    let amplitude = vec![
        GaussianRat::from_rational(rq(3, 5)),
        GaussianRat::from_rational(rq(4, 5)),
        GaussianRat::zero(),
    ];
    let state = ExactDensityState::try_new(outer(&amplitude, &amplitude).unwrap()).unwrap();
    let projectors = (0..3)
        .map(|index| {
            let mut basis = vec![GaussianRat::zero(); 3];
            basis[index] = GaussianRat::from_ints(1, 0);
            vec![outer(&basis, &basis).unwrap()]
        })
        .collect();
    let instrument = FiniteQuantumInstrument::new(3, 3, projectors, "three-outcome").unwrap();
    let mut probabilities = Vec::new();
    for outcome in 0..3 {
        let receipt = instrument.receipt(outcome, &state).unwrap();
        assert!(instrument.verify_receipt(&state, &receipt).unwrap());
        probabilities.push(receipt.probability);
    }
    assert_eq!(probabilities, vec![rq(9, 25), rq(16, 25), ri(0)]);
    println!("Quantum instrument: probabilities 9/25, 16/25, 0; all receipts verified");
    assert!(analyze_repeatability(instrument.instrument())
        .unwrap()
        .is_repeatable());
    println!("Repeatability: every cross-outcome Kraus product vanishes");

    let cover = MeasurementCover::new(1, 3, vec![vec![0]; 3]).unwrap();
    let runs = RunTable::new(&cover, vec![vec![vec![0]], vec![vec![1]], vec![vec![2]]]).unwrap();
    let repair_receipt = repair(&cover, &runs, 20, 2000).unwrap();
    verify_repair(&cover, &runs, &repair_receipt, 20).unwrap();
    assert_eq!(repair_receipt.radius, rq(4, 3));
    println!("Empirical repair: three-context radius 4/3; exact primal/dual replay verified");

    let sample_cover = MeasurementCover::new(1, 2, vec![vec![0]; 2]).unwrap();
    let sample_runs = RunTable::new(&sample_cover, vec![vec![vec![0]; 400]; 2]).unwrap();
    let tolerance =
        sampling_tolerance(&sample_cover, &sample_runs, &[rq(1, 10), rq(1, 10)], 10).unwrap();
    assert_eq!(tolerance.uniform_tolerance, rq(1, 5));
    println!("Sampling: iid compatible-population pair tolerance 1/5, failure bound 1/2");

    let query = "calibration-replay".to_owned();
    let profile = FiniteProfile::new(
        vec![(query.clone(), true)],
        BTreeSet::from([query.clone()]),
        BTreeSet::new(),
        1,
    )
    .unwrap();
    let evidence = [TableEvidence {
        query: query.clone(),
        value: verify_calibration_receipt(&packet, &receipt).unwrap(),
    }];
    let status_receipt = profile.evaluate_with_receipt(&query, &evidence).unwrap();
    profile
        .verify_receipt(&query, &evidence, &status_receipt)
        .unwrap();
    assert_eq!(status_receipt.status, ProfileStatus::Proved);
    println!("Profile: Proved in the declared finite table; receipt replay verified");
}
