//! Cochain repair capacity and error-threshold boundaries: exact distances of
//! declared stabilizer and cochain codes, the correction radius
//! `floor((d - 1)/2)` checked in both directions, local green against global
//! red, and exact decoding probabilities that bound the logical failure of
//! maximum-likelihood decoding by `1 - 1/|H^1|`. Every check is exact.

use finite_qm_native::campaigns::foundational_targets::verify_target12_css_code;
use finite_qm_native::campaigns::toric::ToricCode2x2;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::pauli::Pauli;
use omega_quantum_physics::shor::ShorNineQubitCode;

use omega_quantum_physics::cochain_repair_code::{
    repetition, torus, CochainCodeError, CochainRepairCode, DecodingRule,
};
use omega_quantum_physics::stabilizer_code_distance::{
    pauli_string, pauli_weight, product, strings_of_weight, StabilizerCode, StabilizerCodeError,
    DEFAULT_CANDIDATE_BUDGET,
};

const XYZ: [Pauli; 3] = [Pauli::X, Pauli::Y, Pauli::Z];

fn code(generators: &[&str]) -> StabilizerCode {
    StabilizerCode::try_new(
        generators
            .iter()
            .map(|g| pauli_string(g).unwrap())
            .collect(),
    )
    .unwrap()
}

fn shor() -> StabilizerCode {
    StabilizerCode::try_new(
        ShorNineQubitCode::stabilizers()
            .iter()
            .map(|g| g.to_vec())
            .collect(),
    )
    .unwrap()
}

fn steane() -> StabilizerCode {
    code(&[
        "IIIXXXX", "IXXIIXX", "XIXIXIX", "IIIZZZZ", "IZZIIZZ", "ZIZIZIZ",
    ])
}

fn five_qubit() -> StabilizerCode {
    code(&["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"])
}

fn toric_2x2() -> StabilizerCode {
    let generators = ToricCode2x2::star_operators()
        .iter()
        .chain(ToricCode2x2::plaquette_operators().iter())
        .map(|g| g.to_vec())
        .collect();
    StabilizerCode::try_new(generators).unwrap()
}

#[test]
fn declared_codes_have_their_exact_parameters() {
    let cases: [(&str, StabilizerCode, [usize; 3]); 6] = [
        ("Shor", shor(), [9, 1, 3]),
        ("Steane", steane(), [7, 1, 3]),
        ("five-qubit", five_qubit(), [5, 1, 3]),
        ("[[4,2,2]]", code(&["XXXX", "ZZZZ"]), [4, 2, 2]),
        ("2x2 torus", toric_2x2(), [8, 2, 2]),
        ("bit flip", code(&["ZZI", "IZZ"]), [3, 1, 1]),
    ];
    for (name, c, [n, k, d]) in cases {
        let certificate = c.distance().unwrap();
        assert_eq!([c.n(), c.k(), certificate.distance()], [n, k, d], "{name}");
        assert_eq!(pauli_weight(certificate.witness()), d, "{name}");
        assert!(c.is_logical(certificate.witness()).unwrap(), "{name}");
        let lighter: usize = (1..d)
            .map(|w| strings_of_weight(n, w, &XYZ).unwrap().len())
            .sum();
        assert_eq!(certificate.lighter_candidates_checked(), lighter, "{name}");
    }
    // The library records these distances and the torus's logical count as constants.
    assert_eq!(
        ShorNineQubitCode::new().distance,
        shor().distance().unwrap().distance()
    );
    assert_eq!(
        verify_target12_css_code().code_distance,
        code(&["XXXX", "ZZZZ"]).distance().unwrap().distance()
    );
    assert_eq!(ToricCode2x2::new().k_logical, toric_2x2().k());
    // Shor: 27 + 324 strings of weight 1 and 2 checked below d = 3.
    assert_eq!(shor().distance().unwrap().lighter_candidates_checked(), 351);
    // The torus has 8 generators of rank 6; the bit-flip code resists bit flips only.
    assert_eq!(toric_2x2().rank(), 6);
    let bit_flip = code(&["ZZI", "IZZ"]);
    assert_eq!(
        bit_flip
            .distance_over(&[Pauli::X], DEFAULT_CANDIDATE_BUDGET)
            .unwrap()
            .distance(),
        3
    );
    assert_eq!(
        bit_flip
            .distance_over(&[Pauli::Z], DEFAULT_CANDIDATE_BUDGET)
            .unwrap()
            .witness(),
        pauli_string("ZII").unwrap().as_slice()
    );
}

#[test]
fn every_error_up_to_the_correction_radius_is_corrected_and_one_more_defeats_every_decoder() {
    let x_only = [Pauli::X];
    let cases: Vec<(&str, StabilizerCode, &[Pauli], usize)> = vec![
        ("Shor", shor(), &XYZ, 1),
        ("Steane", steane(), &XYZ, 1),
        ("five-qubit", five_qubit(), &XYZ, 1),
        ("2x2 torus", toric_2x2(), &XYZ, 0),
        (
            "3x3 torus bit flips",
            torus(3).unwrap().stabilizer_code().unwrap(),
            &x_only,
            1,
        ),
        (
            "repetition 5",
            repetition(5).unwrap().stabilizer_code().unwrap(),
            &x_only,
            2,
        ),
    ];
    for (name, c, alphabet, radius) in cases {
        let certificate = c.distance_over(alphabet, DEFAULT_CANDIDATE_BUDGET).unwrap();
        let t = certificate.correction_radius().unwrap();
        assert_eq!(t, radius, "{name}");
        let decoder = c.minimum_weight_decoder(t + 1, alphabet).unwrap();
        let n = c.n();
        for w in 0..=t {
            for error in strings_of_weight(n, w, alphabet).unwrap() {
                assert_eq!(
                    c.is_corrected(&decoder, &error).unwrap(),
                    Some(true),
                    "{name}"
                );
            }
        }
        let (first, second) = certificate.uncorrectable_pair();
        let d = certificate.distance();
        assert_eq!(
            (pauli_weight(&first), pauli_weight(&second)),
            (d.div_ceil(2), d / 2),
            "{name}"
        );
        assert!(pauli_weight(&first) <= t + 1, "{name}");
        assert_eq!(
            c.syndrome(&first).unwrap(),
            c.syndrome(&second).unwrap(),
            "{name}"
        );
        // Any correction C with C E1 and C E2 in the group would put E1 E2 in the group.
        assert!(
            c.is_logical(&product(&first, &second).unwrap()).unwrap(),
            "{name}"
        );
        let outcomes = [
            c.is_corrected(&decoder, &first).unwrap(),
            c.is_corrected(&decoder, &second).unwrap(),
        ];
        assert!(outcomes.contains(&Some(false)), "{name}");
    }
}

#[test]
fn shor_corrects_all_single_errors_through_degenerate_syndromes() {
    let c = shor();
    let decoder = c.minimum_weight_decoder(1, &XYZ).unwrap();
    // Identity, 9 bit flips, 9 Y errors, and one syndrome per block of phase flips.
    assert_eq!(decoder.syndrome_count(), 1 + 9 + 9 + 3);
    let singles = strings_of_weight(9, 1, &XYZ).unwrap();
    assert_eq!(singles.len(), 27);
    for error in &singles {
        assert_eq!(c.is_corrected(&decoder, error).unwrap(), Some(true));
        let array: [Pauli; 9] = error.as_slice().try_into().unwrap();
        assert!(ShorNineQubitCode::recover_error(&array));
    }
    let z1 = pauli_string("ZIIIIIIII").unwrap();
    let z2 = pauli_string("IZIIIIIII").unwrap();
    assert_eq!(c.syndrome(&z1).unwrap(), c.syndrome(&z2).unwrap());
    assert!(c.in_stabilizer_group(&product(&z1, &z2).unwrap()).unwrap());
}

#[test]
fn the_repair_distance_is_the_least_weight_of_a_cocycle_that_is_not_a_coboundary() {
    for (side, h1, d) in [(2, 2, 2), (3, 2, 3)] {
        let t = torus(side).unwrap();
        assert_eq!(t.cells(), [side * side, 2 * side * side, side * side]);
        assert_eq!(t.cohomology_dimension(), h1);
        assert_eq!(t.repair_distance().unwrap().distance(), d);
        assert_eq!(t.stabilizer_code().unwrap().k(), h1);
    }
    assert_eq!(
        torus(3)
            .unwrap()
            .stabilizer_code()
            .unwrap()
            .distance()
            .unwrap()
            .distance(),
        3
    );
    let r = repetition(5).unwrap();
    assert_eq!((r.cells(), r.cohomology_dimension()), ([0, 5, 4], 1));
    assert_eq!(r.repair_distance().unwrap().distance(), 5);

    // The definition, by brute force over all 256 cochains of the 2x2 torus.
    let t = torus(2).unwrap();
    let css = t.stabilizer_code().unwrap();
    let mut least = usize::MAX;
    for mask in 0u32..256 {
        let e: Vec<u8> = (0..8).map(|i| (mask >> i & 1) as u8).collect();
        let syndrome = t.syndrome(&e).unwrap();
        let x_string: Vec<Pauli> = e
            .iter()
            .map(|&b| if b == 1 { Pauli::X } else { Pauli::I })
            .collect();
        // The four X generators come first and commute with every bit flip.
        let css_syndrome = css.syndrome(&x_string).unwrap();
        assert!(css_syndrome[..4].iter().all(|&b| b == 0));
        assert_eq!(css_syndrome[4..], syndrome[..]);
        assert_eq!(
            t.is_coboundary(&e).unwrap(),
            css.in_stabilizer_group(&x_string).unwrap()
        );
        if syndrome.iter().all(|&b| b == 0) && !t.is_coboundary(&e).unwrap() {
            least = least.min(mask.count_ones() as usize);
        }
    }
    assert_eq!(least, 2);
}

#[test]
fn local_green_does_not_prevent_a_logical_error() {
    let t = torus(3).unwrap();
    let certificate = t.repair_distance().unwrap();
    let e: Vec<u8> = certificate
        .witness()
        .iter()
        .map(|&p| u8::from(p == Pauli::X))
        .collect();
    // Every face check passes, yet the cochain is not a coboundary.
    assert!(t.syndrome(&e).unwrap().iter().all(|&b| b == 0));
    assert!(!t.is_coboundary(&e).unwrap());
    assert_eq!(e.iter().filter(|&&b| b == 1).count(), 3);
    // A coboundary also passes every check and is harmless.
    let star: Vec<u8> = (0..18)
        .map(|edge| u8::from([0, 2, 9, 15].contains(&edge)))
        .collect();
    assert!(t.is_coboundary(&star).unwrap());
    assert!(t.syndrome(&star).unwrap().iter().all(|&b| b == 0));
    // A single flip is detected by two faces.
    let single: Vec<u8> = (0..18).map(|edge| u8::from(edge == 0)).collect();
    assert_eq!(
        t.syndrome(&single)
            .unwrap()
            .iter()
            .filter(|&&b| b == 1)
            .count(),
        2
    );
}

#[test]
fn maximum_likelihood_failure_never_exceeds_one_minus_one_over_the_class_count() {
    let t = torus(2).unwrap();
    let floor = rq(1, 4);
    for p in [
        ri(0),
        rq(1, 10),
        rq(1, 4),
        rq(2, 5),
        rq(1, 2),
        rq(3, 5),
        rq(3, 4),
        rq(9, 10),
        ri(1),
    ] {
        let ml = t
            .logical_success_probability(&p, DecodingRule::MaximumLikelihood)
            .unwrap();
        let mw = t
            .logical_success_probability(&p, DecodingRule::MinimumWeight)
            .unwrap();
        assert!(ml >= floor && ml >= mw, "p = {p}");
    }
    for rule in [DecodingRule::MaximumLikelihood, DecodingRule::MinimumWeight] {
        assert_eq!(
            t.logical_success_probability(&rq(1, 2), rule).unwrap(),
            floor
        );
        assert_eq!(t.logical_success_probability(&ri(0), rule).unwrap(), ri(1));
    }
}

#[test]
fn failure_approaching_one_above_threshold_belongs_to_the_decoder_not_the_code() {
    let p = rq(3, 5);
    let failure = |code: &CochainRepairCode, rule| {
        ri(1) - code.logical_success_probability(&p, rule).unwrap()
    };
    let codes: Vec<CochainRepairCode> = [3, 5, 7].iter().map(|&n| repetition(n).unwrap()).collect();
    let minimum_weight: Vec<Rational> = codes
        .iter()
        .map(|c| failure(c, DecodingRule::MinimumWeight))
        .collect();
    let likelihood: Vec<Rational> = codes
        .iter()
        .map(|c| failure(c, DecodingRule::MaximumLikelihood))
        .collect();
    // Majority decoding above p = 1/2 fails more as the code grows ...
    assert_eq!(
        minimum_weight,
        vec![rq(81, 125), rq(2133, 3125), rq(11097, 15625)]
    );
    // ... while maximum likelihood on the same codes fails less.
    assert_eq!(
        likelihood,
        vec![rq(44, 125), rq(992, 3125), rq(4528, 15625)]
    );
    for c in &codes {
        for rule in [DecodingRule::MaximumLikelihood, DecodingRule::MinimumWeight] {
            assert_eq!(
                c.logical_success_probability(&rq(1, 2), rule).unwrap(),
                rq(1, 2)
            );
        }
    }
    // Below threshold the two rules agree: (9/10)^3 + 3 (1/10) (9/10)^2.
    let three = &codes[0];
    for rule in [DecodingRule::MaximumLikelihood, DecodingRule::MinimumWeight] {
        assert_eq!(
            three.logical_success_probability(&rq(1, 10), rule).unwrap(),
            rq(243, 250)
        );
    }
}

#[test]
fn malformed_complexes_codes_and_probabilities_are_refused() {
    assert_eq!(
        CochainRepairCode::new(1, vec![], vec![]),
        Err(CochainCodeError::EmptyCochains)
    );
    assert_eq!(
        CochainRepairCode::new(2, vec![vec![1, 1], vec![1]], vec![]),
        Err(CochainCodeError::D0RowLength {
            row: 1,
            expected: 2,
            actual: 1
        })
    );
    assert_eq!(
        CochainRepairCode::new(2, vec![vec![1, 1]], vec![vec![1, 0]]),
        Err(CochainCodeError::D1RowLength {
            row: 0,
            expected: 1,
            actual: 2
        })
    );
    assert_eq!(
        CochainRepairCode::new(1, vec![vec![2]], vec![]),
        Err(CochainCodeError::NonBinary {
            map: "d0",
            row: 0,
            column: 0
        })
    );
    // A triangle whose face omits one of its edges: d1 d0 != 0.
    let triangle_d0 = vec![vec![1, 1, 0], vec![0, 1, 1], vec![1, 0, 1]];
    assert_eq!(
        CochainRepairCode::new(3, triangle_d0.clone(), vec![vec![1, 1, 0]]),
        Err(CochainCodeError::ClosureFails)
    );
    let filled = CochainRepairCode::new(3, triangle_d0, vec![vec![1, 1, 1]]).unwrap();
    assert_eq!(filled.cohomology_dimension(), 0);
    assert_eq!(
        filled.repair_distance(),
        Err(CochainCodeError::Stabilizer(
            StabilizerCodeError::NoLogicalQubits { n: 3, rank: 3 }
        ))
    );
    assert_eq!(
        filled.syndrome(&[1, 0]),
        Err(CochainCodeError::CochainLength {
            expected: 3,
            actual: 2
        })
    );
    assert_eq!(
        filled.is_coboundary(&[1, 2, 0]),
        Err(CochainCodeError::NonBinaryCochain { index: 1 })
    );
    let t = torus(2).unwrap();
    for p in [rq(-1, 2), rq(3, 2)] {
        assert_eq!(
            t.logical_success_probability(&p, DecodingRule::MaximumLikelihood),
            Err(CochainCodeError::ProbabilityOutOfRange(p.clone()))
        );
    }
    assert_eq!(
        torus(3)
            .unwrap()
            .logical_success_probability(&rq(1, 10), DecodingRule::MinimumWeight),
        Err(CochainCodeError::TooLargeToEnumerate)
    );
    assert_eq!(
        torus(1),
        Err(CochainCodeError::FamilyTooSmall { minimum: 2 })
    );
    assert_eq!(
        repetition(1),
        Err(CochainCodeError::FamilyTooSmall { minimum: 2 })
    );

    assert_eq!(
        StabilizerCode::try_new(vec![]),
        Err(StabilizerCodeError::NoGenerators)
    );
    assert_eq!(
        StabilizerCode::try_new(vec![vec![]]),
        Err(StabilizerCodeError::ZeroQubits)
    );
    // Size is bounded by the search budget, not by a qubit cap: a 40-qubit code
    // is declared, and a decoder over all its strings is refused before it is built.
    let wide = StabilizerCode::try_new(vec![vec![Pauli::Z; 40]]).unwrap();
    assert_eq!(wide.distance().unwrap().distance(), 1);
    assert!(matches!(
        wide.minimum_weight_decoder(40, &XYZ),
        Err(StabilizerCodeError::CandidateBudgetExceeded {
            candidates_checked: 0,
            ..
        })
    ));
    assert_eq!(
        StabilizerCode::try_new(vec![
            pauli_string("XX").unwrap(),
            pauli_string("Z").unwrap()
        ]),
        Err(StabilizerCodeError::RaggedGenerator {
            index: 1,
            expected: 2,
            actual: 1
        })
    );
    assert_eq!(
        StabilizerCode::try_new(vec![
            pauli_string("XI").unwrap(),
            pauli_string("ZI").unwrap()
        ]),
        Err(StabilizerCodeError::AnticommutingGenerators { left: 0, right: 1 })
    );
    assert_eq!(
        pauli_string("XQZ"),
        Err(StabilizerCodeError::UnknownSymbol {
            index: 1,
            symbol: 'Q'
        })
    );
    let bell = code(&["XX", "ZZ"]);
    assert_eq!(bell.k(), 0);
    assert_eq!(
        bell.distance(),
        Err(StabilizerCodeError::NoLogicalQubits { n: 2, rank: 2 })
    );
    for alphabet in [&[][..], &[Pauli::I][..], &[Pauli::X, Pauli::X][..]] {
        assert_eq!(
            steane().distance_over(alphabet, DEFAULT_CANDIDATE_BUDGET),
            Err(StabilizerCodeError::BadAlphabet)
        );
    }
    assert_eq!(
        steane().syndrome(&pauli_string("XX").unwrap()),
        Err(StabilizerCodeError::LengthMismatch {
            expected: 7,
            actual: 2
        })
    );
}
