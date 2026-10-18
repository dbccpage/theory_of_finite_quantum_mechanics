//! The finite Hilbert boundary walked from a report-fiber primitive
//! difference: phase-blind weights and their fiber, readouts along orthogonal
//! Gaussian-integer frames, product rules on two labels, report dynamics that
//! are not reversible or have no half step, pairings that share a unit total,
//! the carrier stages and cyclotomic hosts, the higher-dimensional ray
//! configurations and their frame polytopes, the Cayley hinge spectrum, and
//! the declared simplicial and spin-foam models. Rows proved in the paper's
//! receipted Lean keep that status; the tests here replay finite content and
//! pin the countermodels found on the way.

use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};
use omega_general_relativity::simplicial_dynamics::{CauchySlice, ReggeFourSimplex};

use finite_qm_native::finite_spinfoam::{self, ModelVersion, PachnerState};
use finite_qm_native::report_fiber::{
    carrier_stage, dump_right, entanglement_determinant, mix, phase_blind, tensor2,
};
use finite_qm_native::simplicial_gravity::{area_model, page_curve};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::elimination;
use linear_algebra::exact_field::{involution, involution::Involution, matrix};
use omega_lie_theory::cayley::unit_from_parameter;
use omega_lie_theory::scalar::multiplicative_order;
use omega_number_theory::cyclotomic::{Cyc12, Cyc8, GaussianRat};
use omega_number_theory::cyclotomic_integer::CyclotomicInteger;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::exact_hermitian::{gi, gq};
use omega_quantum_physics::finite_geometry;
use omega_quantum_physics::kochen_specker::{CABELLO_18_VECTORS, CABELLO_9_CONTEXTS};
use omega_quantum_physics::pairing_audit::{
    audit_row, CompositeTier, Pairing, PairingOrigin, PairingPacket, PairingRow, PairingTerminal,
};
use omega_quantum_physics::phase_blind_quotient::{discrete_fiber, UnitPhaseGroup};

use omega_quantum_physics::finite_report_dynamics::{
    half_steps, reversible_dilations, swap_interpolants, ReportDynamicsError,
};
use omega_quantum_physics::frame_function_polytope::{
    eigenvalues_above, eigenvalues_at_least, FramePolytopeError, FrameSystem,
};
use omega_quantum_physics::gaussian_frame_readout::{
    frame_additivity_violation, frame_operator, frame_total, orthogonal_frames, readout,
    report_basis_law, scale_vectors, square_is_frame_additive, FrameError,
};

fn g(re: i64, im: i64) -> GaussianRat {
    gi(re, im)
}

fn psi21() -> [GaussianRat; 2] {
    [g(2, 0), g(1, 0)]
}

fn hadamard_frame() -> ([GaussianRat; 2], [GaussianRat; 2]) {
    ([g(1, 0), g(1, 0)], [g(1, 0), g(-1, 0)])
}

fn rotated_frame() -> ([GaussianRat; 2], [GaussianRat; 2]) {
    ([g(1, 0), g(0, 1)], [g(1, 0), g(0, -1)])
}

fn units() -> Vec<GaussianRat> {
    vec![g(1, 0), g(0, 1), g(-1, 0), g(0, -1)]
}

fn qmat(rows: &[&[(i64, i64)]]) -> Vec<Vec<Rational>> {
    rows.iter()
        .map(|row| row.iter().map(|&(n, d)| rq(n, d)).collect())
        .collect()
}

fn identity_q(n: usize) -> Vec<Vec<Rational>> {
    (0..n)
        .map(|i| (0..n).map(|j| ri(i64::from(i == j))).collect())
        .collect()
}

fn cabello() -> FrameSystem {
    FrameSystem::new(
        CABELLO_18_VECTORS
            .iter()
            .map(|r| r.iter().map(|&x| i64::from(x)).collect())
            .collect(),
        CABELLO_9_CONTEXTS.iter().map(|c| c.to_vec()).collect(),
    )
    .unwrap()
}

fn projector(ray: &[i64]) -> Vec<Vec<Rational>> {
    let norm: i64 = ray.iter().map(|x| x * x).sum();
    ray.iter()
        .map(|&a| ray.iter().map(|&b| rq(a * b, norm)).collect())
        .collect()
}

// ---------------------------------------------------------------------------
// QM-122-C9: phase-blind squares and the fiber they leave.
// ---------------------------------------------------------------------------

#[test]
fn phase_blind_squares_leave_a_fiber_larger_than_the_global_phase_orbit() {
    let plus = [g(1, 0), g(1, 0)];
    let minus = [g(1, 0), g(-1, 0)];
    assert_eq!(phase_blind(&plus).unwrap(), vec![ri(1), ri(1)]);
    assert_eq!(phase_blind(&minus).unwrap(), phase_blind(&plus).unwrap());
    assert_ne!(plus, minus);
    // Global phases stay in the fiber.
    let orbit: Vec<[GaussianRat; 2]> = units()
        .iter()
        .map(|u| [u.mul(&plus[0]), u.mul(&plus[1])])
        .collect();
    assert!(orbit
        .iter()
        .all(|v| phase_blind(v).unwrap() == vec![ri(1), ri(1)]));
    // The fiber of (1, 1) in Z[i]^2 is every pair of units: sixteen vectors,
    // four global-phase orbits. (1, -1) is in the fiber and not in the orbit of (1, 1).
    let mut fiber = Vec::new();
    for a in -1..=1 {
        for b in -1..=1 {
            for c in -1..=1 {
                for d in -1..=1 {
                    let v = [g(a, b), g(c, d)];
                    if phase_blind(&v).unwrap() == vec![ri(1), ri(1)] {
                        fiber.push(v);
                    }
                }
            }
        }
    }
    assert_eq!(fiber.len(), 16);
    assert!(!orbit.contains(&minus));
    let quarter_turns = UnitPhaseGroup::new(units()).unwrap();
    assert_eq!(discrete_fiber(&plus, &quarter_turns).unwrap().len(), 4);
    // Mixing separates the pair: (4, 0) against (0, 4).
    assert_eq!(phase_blind(&mix(&plus)).unwrap(), vec![ri(4), ri(0)]);
    assert_eq!(phase_blind(&mix(&minus)).unwrap(), vec![ri(0), ri(4)]);
    // Only Gaussian integers are admitted as amplitudes on this host.
    assert!(phase_blind(&[gq(1, 2, 0, 1)]).is_err());
}

// ---------------------------------------------------------------------------
// QM-122-C12: readouts along orthogonal scale-2 frames.
// ---------------------------------------------------------------------------

#[test]
fn the_square_is_frame_additive_at_scale_two_for_every_state() {
    assert_eq!(scale_vectors(1).unwrap().len(), 8);
    assert_eq!(scale_vectors(2).unwrap().len(), 24);
    let frames = orthogonal_frames(2).unwrap();
    assert_eq!(frames.len(), 96);
    assert!(frames.contains(&hadamard_frame()) && frames.contains(&rotated_frame()));
    let two_i = matrix::scale(&matrix::identity::<GaussianRat>(2).unwrap(), &g(2, 0)).unwrap();
    assert!(frames.iter().all(|f| frame_operator(f) == two_i));
    for scale in [1, 2, 4, 5] {
        assert!(square_is_frame_additive(scale).unwrap(), "scale {scale}");
    }
    // The square's totals on the two exhibited frames, and on every frame for (2, 1).
    assert_eq!(frame_total(&hadamard_frame(), &psi21(), 1).unwrap(), ri(10));
    assert_eq!(frame_total(&rotated_frame(), &psi21(), 1).unwrap(), ri(10));
    assert!(frames
        .iter()
        .all(|f| frame_total(f, &psi21(), 1).unwrap() == ri(10)));
    assert_eq!(frame_additivity_violation(2, 1, 2).unwrap(), None);
    // A non-orthogonal pair of scale-2 vectors has a frame operator other than 2I.
    let skew = ([g(1, 0), g(1, 0)], [g(1, 0), g(0, 1)]);
    assert!(!frames.contains(&skew));
    assert_ne!(frame_operator(&skew), two_i);
}

#[test]
fn every_higher_power_breaks_scale_two_frame_additivity_though_every_power_normalizes() {
    assert_eq!(frame_total(&hadamard_frame(), &psi21(), 2).unwrap(), ri(82));
    assert_eq!(frame_total(&rotated_frame(), &psi21(), 2).unwrap(), ri(50));
    assert_eq!(
        frame_total(&hadamard_frame(), &psi21(), 3).unwrap(),
        ri(730)
    );
    assert_eq!(frame_total(&rotated_frame(), &psi21(), 3).unwrap(), ri(250));
    for power in 2..=4 {
        let violation = frame_additivity_violation(2, power, 2)
            .unwrap()
            .expect("a violating state");
        assert_ne!(violation.first_total, violation.second_total);
        assert_eq!(
            frame_total(&violation.first, &violation.state, power).unwrap(),
            violation.first_total
        );
        assert_eq!(
            frame_total(&violation.second, &violation.state, power).unwrap(),
            violation.second_total
        );
    }
    // At scale 1 the frames are the coordinate axes up to units: no power is excluded.
    for power in 1..=4 {
        assert_eq!(
            frame_additivity_violation(1, power, 1).unwrap(),
            None,
            "power {power}"
        );
    }
    // Along the report basis the fourth power of (2, 1) is (16, 1), not a rescaled (4, 1).
    assert_eq!(readout(&[g(1, 0), g(0, 0)], &psi21(), 2).unwrap(), ri(16));
    assert_eq!(
        report_basis_law(&psi21(), 1).unwrap(),
        Some(vec![rq(4, 5), rq(1, 5)])
    );
    assert_eq!(
        report_basis_law(&psi21(), 2).unwrap(),
        Some(vec![rq(16, 17), rq(1, 17)])
    );
    // Every power normalizes; only the square is frame additive.
    for power in 1..=4 {
        let law = report_basis_law(&psi21(), power).unwrap().unwrap();
        assert_eq!(law.iter().sum::<Rational>(), ri(1));
    }
    assert_eq!(report_basis_law(&[g(0, 0), g(0, 0)], 1).unwrap(), None);
    assert_eq!(scale_vectors(0), Err(FrameError::Scale(0)));
    assert_eq!(scale_vectors(17), Err(FrameError::Scale(17)));
    assert_eq!(readout(&psi21(), &psi21(), 0), Err(FrameError::ZeroPower));
    assert_eq!(
        frame_additivity_violation(2, 1, 5),
        Err(FrameError::SearchBox(5))
    );
}

// ---------------------------------------------------------------------------
// QM-122-C14: collapse, dilations, half steps and scaled interpolants.
// ---------------------------------------------------------------------------

#[test]
fn collapse_has_no_same_basis_isometry_and_four_reversible_dilations() {
    // Columns are the images of the report basis: collapse sends both to e_false.
    let collapse = matrix::from_rows(vec![vec![g(1, 0), g(1, 0)], vec![g(0, 0), g(0, 0)]]).unwrap();
    assert_eq!(
        matrix::multiply(&involution::adjoint(&collapse).unwrap(), &collapse).unwrap(),
        matrix::from_rows(vec![vec![g(1, 0), g(1, 0)], vec![g(1, 0), g(1, 0)]]).unwrap()
    );
    let toggle = matrix::from_rows(vec![vec![g(0, 0), g(1, 0)], vec![g(1, 0), g(0, 0)]]).unwrap();
    assert_eq!(
        matrix::multiply(&involution::adjoint(&toggle).unwrap(), &toggle).unwrap(),
        matrix::identity::<GaussianRat>(2).unwrap()
    );
    // Ancilla prepared at false: exactly four bijections of Bool x Bool collapse the prepared slice.
    let collapse_dilations = reversible_dilations(&[0, 0], 2, Some(0)).unwrap();
    assert_eq!(collapse_dilations.len(), 4);
    // Each sends the prepared slice (0, false), (1, false) into report false.
    assert!(collapse_dilations
        .iter()
        .all(|p| p[0] / 2 == 0 && p[2] / 2 == 0));
    // Three labels, two collapsed and one kept: 2 * 2 placements of the slice, 3! for the rest.
    assert_eq!(
        reversible_dilations(&[0, 0, 1], 2, Some(0)).unwrap().len(),
        24
    );
    // Identity on the report coordinate for every ancilla value: four, one per pair of fiber flips.
    let identity_dilations = reversible_dilations(&[0, 1], 2, None).unwrap();
    let expected: Vec<Vec<usize>> = (0..4usize)
        .map(|flips| {
            (0..4)
                .map(|x| (x / 2) * 2 + ((x % 2) ^ ((flips >> (x / 2)) & 1)))
                .collect()
        })
        .collect();
    let mut sorted = identity_dilations.clone();
    sorted.sort();
    let mut expected_sorted = expected;
    expected_sorted.sort();
    assert_eq!(sorted, expected_sorted);
    // Two distinct reversible dilations share one reduction.
    assert!(
        identity_dilations.contains(&vec![0, 1, 2, 3])
            && identity_dilations.contains(&vec![1, 0, 3, 2])
    );
    // Without a prepared ancilla no bijection collapses all four points.
    assert!(reversible_dilations(&[0, 0], 2, None).unwrap().is_empty());
    assert_eq!(reversible_dilations(&[0, 1], 2, Some(0)).unwrap().len(), 8);
    assert_eq!(reversible_dilations(&[1, 0], 2, None).unwrap().len(), 4);
}

#[test]
fn the_toggle_has_no_half_step_and_its_interpolants_exist_only_at_scales_four_and_sixteen() {
    assert!(half_steps(&[1, 0]).unwrap().is_empty());
    assert_eq!(half_steps(&[0, 1]).unwrap(), vec![vec![1, 0], vec![0, 1]]);
    assert_eq!(half_steps(&[1, 2, 0]).unwrap(), vec![vec![2, 0, 1]]);
    // A single transposition has no square root; two of them do (a four-cycle).
    assert!(half_steps(&[1, 0, 2, 3]).unwrap().is_empty());
    assert_eq!(half_steps(&[1, 0, 3, 2]).unwrap().len(), 2);
    // After complex coefficients: M^2 = 4 X has exactly four solutions in M_2(Z[i]).
    let roots = swap_interpolants(4).unwrap();
    assert_eq!(roots.len(), 4);
    let sqrt_swap =
        matrix::from_rows(vec![vec![g(1, 1), g(1, -1)], vec![g(1, -1), g(1, 1)]]).unwrap();
    assert!(
        roots.contains(&sqrt_swap)
            && roots.contains(&matrix::scale(&sqrt_swap, &g(-1, 0)).unwrap())
    );
    let four_swap =
        matrix::from_rows(vec![vec![g(0, 0), g(4, 0)], vec![g(4, 0), g(0, 0)]]).unwrap();
    assert!(roots
        .iter()
        .all(|m| matrix::multiply(&m, m).unwrap() == four_swap));
    for scale in 1..=16 {
        let count = swap_interpolants(scale).unwrap().len();
        assert_eq!(
            count,
            if scale == 4 || scale == 16 { 4 } else { 0 },
            "scale {scale}"
        );
    }
    // Over Q no scale works: det(c X) = -c^2 < 0 is not a square of a determinant.
    for c in 1..=16i64 {
        assert!(ri(-c * c).is_negative());
    }
    assert_eq!(swap_interpolants(0), Err(ReportDynamicsError::Scale(0)));
    assert!(swap_interpolants(17).unwrap().is_empty());
    assert!(matches!(
        half_steps(&[0; 7]),
        Err(ReportDynamicsError::Budget(_))
    ));
    assert!(matches!(
        reversible_dilations(&[0, 1, 2], 3, None),
        Err(ReportDynamicsError::Budget(_))
    ));
    assert_eq!(half_steps(&[]), Err(ReportDynamicsError::Empty));
    assert_eq!(
        half_steps(&[0, 2]),
        Err(ReportDynamicsError::ImageOutOfRange {
            label: 1,
            image: 2,
            labels: 2
        })
    );
    assert_eq!(
        reversible_dilations(&[0, 1], 0, None),
        Err(ReportDynamicsError::EmptyAncilla)
    );
    assert_eq!(
        reversible_dilations(&[0, 1], 2, Some(2)),
        Err(ReportDynamicsError::PreparedOutOfRange {
            prepared: 2,
            ancilla: 2
        })
    );
}

// ---------------------------------------------------------------------------
// QM-122-C43, C49: the Cabello frame polytope, exhaustively.
// ---------------------------------------------------------------------------

#[test]
fn cabello_frame_functions_are_exactly_the_trace_one_symmetric_matrices() {
    let system = cabello();
    assert_eq!((system.dimension(), system.ray_count()), (4, 18));
    assert_eq!(system.incidence_rank().unwrap(), 9);
    assert_eq!(system.ray_degrees(), vec![2; 18]);
    // The projectors span all ten symmetric directions, and 18 - 9 = 9 = 10 - 1.
    assert_eq!(system.projector_span_rank().unwrap(), 10);
    // Parity: summing A f = 1 over the nine tetrads counts every ray twice, so
    // sum f = 9/2 and no frame function has integer values.
    let uniform = vec![rq(1, 4); 18];
    assert!(system.is_feasible(&uniform).unwrap());
    let incidence = system.incidence().unwrap();
    let column_sums: Vec<Rational> = (0..18)
        .map(|r| {
            (0..incidence.rows())
                .map(|row| incidence.get_ref(row, r).unwrap().clone())
                .sum()
        })
        .collect();
    assert_eq!(column_sums, vec![ri(2); 18]);
    // The uniform frame function is the maximally mixed state, a round trip.
    let mixed = matrix::to_rows(&system.state_of(&uniform).unwrap()).unwrap();
    assert_eq!(
        mixed,
        qmat(&[
            &[(1, 4), (0, 1), (0, 1), (0, 1)],
            &[(0, 1), (1, 4), (0, 1), (0, 1)],
            &[(0, 1), (0, 1), (1, 4), (0, 1)],
            &[(0, 1), (0, 1), (0, 1), (1, 4)]
        ])
    );
    assert_eq!(
        system
            .frame_function_of(&matrix::from_rows((&mixed).to_vec()).unwrap())
            .unwrap(),
        uniform
    );
    // A vector that fails A f = 1 is refused.
    assert_eq!(
        system.state_of(&vec![ri(0); 18]),
        Err(FramePolytopeError::NotAFrameFunction)
    );
}

#[test]
fn every_cabello_vertex_is_half_integral_and_non_psd_with_least_eigenvalue_at_least_minus_one_half()
{
    let system = cabello();
    let vertices = system.vertices().unwrap();
    assert_eq!(vertices.len(), 146);
    let values = [ri(0), rq(1, 2), ri(1)];
    let mut at_minus_half = 0;
    for v in &vertices {
        assert!(system.is_vertex(v).unwrap());
        assert!(v.iter().all(|x| values.contains(x)));
        assert!(v.contains(&rq(1, 2)), "no vertex is a {{0, 1}} coloring");
        let rho = matrix::to_rows(&system.state_of(v).unwrap()).unwrap();
        assert_eq!(
            system
                .frame_function_of(&matrix::from_rows((&rho).to_vec()).unwrap())
                .unwrap(),
            *v
        );
        // Not a state: some eigenvalue is negative.
        assert!(
            !eigenvalues_at_least(&matrix::from_rows((&rho).to_vec()).unwrap(), &ri(0)).unwrap()
        );
        // Yet no eigenvalue is below -1/2.
        assert!(
            eigenvalues_at_least(&matrix::from_rows((&rho).to_vec()).unwrap(), &rq(-1, 2)).unwrap()
        );
        if eigenvalues_above(&matrix::from_rows((&rho).to_vec()).unwrap(), &rq(-1, 2)).unwrap() {
            assert!(
                eigenvalues_above(&matrix::from_rows((&rho).to_vec()).unwrap(), &rq(-1, 4))
                    .unwrap()
            );
        } else {
            at_minus_half += 1;
        }
    }
    // 26 vertices reach -1/2 exactly; the other 120 stay above -1/4.
    assert_eq!(at_minus_half, 26);
}

#[test]
fn the_sources_extreme_pseudo_states_and_the_ray_projectors_are_not_vertices() {
    let system = cabello();
    // The two matrices the source calls canonical extreme vertices.
    for sign in [-1, 1] {
        let rho = qmat(&[
            &[(-1, 2), (0, 1), (0, 1), (0, 1)],
            &[(0, 1), (1, 2), (sign, 4), (1, 4)],
            &[(0, 1), (sign, 4), (1, 2), (sign, 4)],
            &[(0, 1), (1, 4), (sign, 4), (1, 2)],
        ]);
        let f = system
            .frame_function_of(&matrix::from_rows((&rho).to_vec()).unwrap())
            .unwrap();
        assert!(system.is_feasible(&f).unwrap());
        assert!(!system.is_vertex(&f).unwrap());
        assert_eq!(
            f.iter().filter(|x| !x.is_zero()).count(),
            12,
            "support exceeds rank 9"
        );
        assert!(
            eigenvalues_at_least(&matrix::from_rows((&rho).to_vec()).unwrap(), &rq(-1, 2)).unwrap()
                && !eigenvalues_above(&matrix::from_rows((&rho).to_vec()).unwrap(), &rq(-1, 2))
                    .unwrap()
        );
    }
    // The eighteen ray projectors are states, pairwise distinct, and none is a vertex.
    let projectors: Vec<Vec<Vec<Rational>>> = CABELLO_18_VECTORS
        .iter()
        .map(|r| projector(&r.map(i64::from)))
        .collect();
    for (i, p) in projectors.iter().enumerate() {
        assert!(eigenvalues_at_least(&matrix::from_rows((p).to_vec()).unwrap(), &ri(0)).unwrap());
        let f = system
            .frame_function_of(&matrix::from_rows((p).to_vec()).unwrap())
            .unwrap();
        assert!(system.is_feasible(&f).unwrap());
        assert!(!system.is_vertex(&f).unwrap(), "projector {i}");
        assert!(projectors[..i].iter().all(|q| q != p));
    }
}

#[test]
fn frame_systems_refuse_malformed_declarations_and_unsupported_enumerations() {
    let square = || vec![vec![1, 0], vec![0, 1], vec![1, 1], vec![1, -1]];
    assert_eq!(
        FrameSystem::new(vec![], vec![vec![0]]),
        Err(FramePolytopeError::Empty)
    );
    assert_eq!(
        FrameSystem::new(vec![vec![0, 0]], vec![vec![0]]),
        Err(FramePolytopeError::BadRay { ray: 0 })
    );
    assert_eq!(
        FrameSystem::new(square(), vec![vec![0, 2]]),
        Err(FramePolytopeError::NotOrthogonal {
            frame: 0,
            left: 0,
            right: 2
        })
    );
    assert_eq!(
        FrameSystem::new(square(), vec![vec![0, 0]]),
        Err(FramePolytopeError::BadFrame {
            frame: 0,
            dimension: 2
        })
    );
    assert_eq!(
        FrameSystem::new(square(), vec![vec![0, 1, 2]]),
        Err(FramePolytopeError::BadFrame {
            frame: 0,
            dimension: 2
        })
    );
    // Two frames, each ray in one: frame functions exist but vertices are not enumerated here.
    let plane = FrameSystem::new(square(), vec![vec![0, 1], vec![2, 3]]).unwrap();
    assert_eq!(
        plane.vertices(),
        Err(FramePolytopeError::NotDegreeTwo { ray: 0, count: 1 })
    );
    assert_eq!(plane.projector_span_rank().unwrap(), 3);
    let half = vec![rq(1, 2); 4];
    assert_eq!(
        matrix::to_rows(&plane.state_of(&half).unwrap()).unwrap(),
        qmat(&[&[(1, 2), (0, 1)], &[(0, 1), (1, 2)]])
    );
    assert_eq!(
        plane.frame_function_of(
            &matrix::from_rows((&[vec![ri(1), ri(2)], vec![ri(3), ri(4)]]).to_vec()).unwrap()
        ),
        Err(FramePolytopeError::NotSymmetric { dimension: 2 })
    );
    assert_eq!(
        plane.is_feasible(&[ri(1)]),
        Err(FramePolytopeError::VectorLength {
            expected: 4,
            actual: 1
        })
    );
    // One frame on the axes: its projectors span only the diagonal.
    let axes = FrameSystem::new(vec![vec![1, 0], vec![0, 1]], vec![vec![0, 1]]).unwrap();
    assert_eq!(
        axes.state_of(&[rq(1, 3), rq(2, 3)]),
        Err(FramePolytopeError::ProjectorsDoNotSpan { rank: 2, needed: 3 })
    );
    // The same frame declared twice: every ray in two frames, dependent rows.
    let doubled =
        FrameSystem::new(vec![vec![1, 0], vec![0, 1]], vec![vec![0, 1], vec![1, 0]]).unwrap();
    assert_eq!(
        doubled.vertices(),
        Err(FramePolytopeError::RankDeficient { rank: 1, frames: 2 })
    );
}

// ---------------------------------------------------------------------------
// QM-122-C13, C22: products on Bool x Bool, a same-host rival, and the Bell vector.
// ---------------------------------------------------------------------------

fn two(a: i64, b: i64) -> [Rational; 2] {
    [ri(a), ri(b)]
}

fn small_pairs() -> Vec<[Rational; 2]> {
    (-2..=2)
        .flat_map(|a| (-2..=2).map(move |b| two(a, b)))
        .collect()
}

fn add4(x: &[Rational; 4], y: &[Rational; 4]) -> [Rational; 4] {
    std::array::from_fn(|i| &x[i] + &y[i])
}

#[test]
fn the_kronecker_normalized_product_is_the_pointwise_product_and_dump_right_is_a_rival() {
    let basis = [two(1, 0), two(0, 1)];
    let unit4 = |k: usize| -> [Rational; 4] { std::array::from_fn(|i| ri(i64::from(i == k))) };
    for a in 0..2 {
        for b in 0..2 {
            // Kronecker normalization: (e_a, e_b) lands on e_(a, b).
            assert_eq!(tensor2(&basis[a], &basis[b]), unit4(2 * a + b));
            // The rival tags (a, b) with (a, false): some composite report, not the pair.
            assert_eq!(dump_right(&basis[a], &basis[b]), unit4(2 * a));
        }
    }
    // Both maps are bilinear, so each is fixed by its four basis values;
    // Kronecker normalization fixes all four, hence the product.
    let pairs = small_pairs();
    for u in &pairs {
        for v in &pairs {
            let expand = |f: fn(&[Rational; 2], &[Rational; 2]) -> [Rational; 4]| -> [Rational; 4] {
                let mut acc: [Rational; 4] = std::array::from_fn(|_| ri(0));
                for a in 0..2 {
                    for b in 0..2 {
                        let term = f(&basis[a], &basis[b]).map(|x| x * &u[a] * &v[b]);
                        acc = add4(&acc, &term);
                    }
                }
                acc
            };
            assert_eq!(tensor2(u, v), expand(tensor2));
            assert_eq!(dump_right(u, v), expand(dump_right));
            // Every product vector has vanishing 2 x 2 determinant.
            assert!(entanglement_determinant(&tensor2(u, v)).is_zero());
        }
    }
    // The two maps disagree at (e_false, e_true): 0 against 1 on coordinate (false, true).
    assert_eq!(tensor2(&basis[0], &basis[1])[1], ri(1));
    assert_eq!(dump_right(&basis[0], &basis[1])[1], ri(0));
    // The tagging of dump_right is not injective: (false, false) and (false, true) share a report.
    assert_eq!(
        dump_right(&basis[0], &basis[0]),
        dump_right(&basis[0], &basis[1])
    );
    // The correlated vector (1, 0, 0, 1) has determinant 1, so it is no product;
    // its coefficient matrix has rank 2.
    let bell = [ri(1), ri(0), ri(0), ri(1)];
    assert_eq!(entanglement_determinant(&bell), ri(1));
    assert_eq!(
        elimination::rank(
            &matrix::from_rows((&[vec![ri(1), ri(0)], vec![ri(0), ri(1)]]).to_vec()).unwrap()
        )
        .unwrap(),
        2
    );
}

// ---------------------------------------------------------------------------
// QM-122-C23: two effect rules on the same quadratic weights.
// ---------------------------------------------------------------------------

#[test]
fn the_dual_and_the_report_swapped_pairings_share_unit_totals_and_disagree() {
    let born = |w: &[Rational], e: &[Rational; 2]| -> Rational { &w[0] * &e[0] + &w[1] * &e[1] };
    let swapped = |w: &[Rational], e: &[Rational; 2]| -> Rational { &w[0] * &e[1] + &w[1] * &e[0] };
    let unit = two(1, 1);
    for re0 in -2..=2 {
        for im0 in -2..=2 {
            for re1 in -2..=2 {
                for im1 in -2..=2 {
                    let w = phase_blind(&[g(re0, im0), g(re1, im1)]).unwrap();
                    let total = &w[0] + &w[1];
                    assert_eq!(born(&w, &unit), total);
                    assert_eq!(swapped(&w, &unit), total);
                    for e in [two(1, 0), two(0, 1), two(2, 1), two(0, 3)] {
                        assert!(!born(&w, &e).is_negative() && !swapped(&w, &e).is_negative());
                    }
                }
            }
        }
    }
    let w21 = phase_blind(&psi21()).unwrap();
    assert_eq!(
        (born(&w21, &two(1, 0)), swapped(&w21, &two(1, 0))),
        (ri(4), ri(1))
    );
    // The same two rules as rows of the state-effect pairing audit: normalized
    // weights, the unit effect and the two indicators, no composite declared.
    let states = vec![
        vec![rq(4, 5), rq(1, 5)],
        vec![rq(1, 2), rq(1, 2)],
        vec![ri(1), ri(0)],
        vec![ri(0), ri(1)],
    ];
    let effects = vec![vec![ri(1), ri(1)], vec![ri(1), ri(0)], vec![ri(0), ri(1)]];
    let row = |name: &'static str, gram: Vec<Vec<Rational>>| PairingRow {
        name,
        origin: PairingOrigin::Imported,
        packet: PairingPacket::new(
            states.clone(),
            effects.clone(),
            vec![vec![0], vec![1, 2]],
            Pairing::Bilinear(matrix::from_rows(gram).unwrap()),
            vec![],
        )
        .unwrap(),
        composite: CompositeTier::Undeclared,
    };
    let dual = row("dual", vec![vec![ri(1), ri(0)], vec![ri(0), ri(1)]]);
    let swap = row("swapped", vec![vec![ri(0), ri(1)], vec![ri(1), ri(0)]]);
    assert_eq!(
        audit_row(&dual).unwrap(),
        PairingTerminal::RefusedCompositeUndeclared
    );
    assert_eq!(
        audit_row(&swap).unwrap(),
        PairingTerminal::RefusedCompositeUndeclared
    );
    assert_eq!(
        (
            dual.packet.value(1, &states[0]).unwrap(),
            swap.packet.value(1, &states[0]).unwrap()
        ),
        (rq(4, 5), rq(1, 5))
    );
}

// ---------------------------------------------------------------------------
// QM-122-C39, C40, C41: carrier stages, the two-state scaling law, cyclotomic hosts.
// ---------------------------------------------------------------------------

#[test]
fn the_carrier_stages_have_the_declared_betti_numbers_and_symmetries() {
    let table: Vec<(usize, usize, usize)> = (0..=5)
        .map(|s| {
            let stage = carrier_stage(s).unwrap();
            (stage.betti_h0, stage.betti_h1, stage.automorphism_order)
        })
        .collect();
    assert_eq!(
        table,
        vec![
            (0, 0, 1),
            (1, 0, 1),
            (2, 0, 2),
            (1, 0, 1),
            (1, 1, 2),
            (1, 1, 2)
        ]
    );
    // The primitive cut has boundary b - a; the self-loop has boundary 0.
    assert_eq!(
        carrier_stage(3).unwrap().boundary,
        vec![vec![ri(-1)], vec![ri(1)]]
    );
    assert_eq!(carrier_stage(4).unwrap().boundary, vec![vec![ri(0)]]);
    // A filled triangle kills the loop of the unfilled one.
    assert_eq!(
        (
            carrier_stage(7).unwrap().betti_h1,
            carrier_stage(8).unwrap().betti_h1
        ),
        (1, 0)
    );
    assert!(carrier_stage(9).is_err());
}

#[test]
fn among_power_norms_only_the_square_scales_uniformly_under_the_integer_mix() {
    let vectors = [(1i64, 0i64), (0, 1), (1, 1), (1, -1), (2, 1)];
    let norm = |v: (i64, i64), p: u32| -> Rational { ri(v.0.abs().pow(p) + v.1.abs().pow(p)) };
    let mixed = |v: (i64, i64)| (v.0 + v.1, v.0 - v.1);
    let uniform: Vec<u32> = (1..=6)
        .filter(|&p| {
            vectors
                .iter()
                .all(|&v| norm(mixed(v), p) / norm(v, p) == ri(2))
        })
        .collect();
    assert_eq!(uniform, vec![2]);
    // On (1, 1) the ratio is 2^(p-1), on the basis vectors it is always 2.
    assert_eq!(norm(mixed((1, 1)), 4) / norm((1, 1), 4), ri(8));
    assert_eq!(norm(mixed((1, 0)), 4) / norm((1, 0), 4), ri(2));
}

#[test]
fn cyclotomic_hosts_reduce_exactly_and_the_qutrit_fourier_map_is_a_scaled_isometry() {
    for (n, phi) in [(3usize, 2usize), (4, 2), (5, 4), (8, 4), (12, 4)] {
        let zeta = CyclotomicInteger::zeta(n).unwrap();
        for k in 0..(2 * n) {
            assert!(zeta.pow(k).coefficients().len() <= phi, "zeta_{n}^{k}");
        }
        assert_eq!(zeta.pow(n), CyclotomicInteger::scalar(n, 1).unwrap());
    }
    let z8 = CyclotomicInteger::zeta(8).unwrap();
    let sqrt2 = z8.sub(&z8.pow(3)).unwrap();
    assert_eq!(
        sqrt2.mul(&sqrt2).unwrap(),
        CyclotomicInteger::scalar(8, 2).unwrap()
    );
    assert_eq!(
        Cyc8::sqrt2().mul(&Cyc8::sqrt2()),
        Cyc8::one().scale_rat(&ri(2))
    );
    // F_jk = zeta_3^(jk): F* F = 3 I over Z[zeta_3].
    let z3 = CyclotomicInteger::zeta(3).unwrap();
    for i in 0..3 {
        for j in 0..3 {
            let entry = (0..3).fold(CyclotomicInteger::scalar(3, 0).unwrap(), |acc, k| {
                acc.add(
                    &z3.pow((i * k) % 3)
                        .conj()
                        .mul(&z3.pow((j * k) % 3))
                        .unwrap(),
                )
                .unwrap()
            });
            assert_eq!(
                entry,
                CyclotomicInteger::scalar(3, if i == j { 3 } else { 0 }).unwrap()
            );
        }
    }
    // Non-integral coefficients, conductor 0 and mixed conductors are refused.
    assert!(CyclotomicInteger::new(8, vec![rq(1, 2)]).is_err());
    assert!(CyclotomicInteger::new(0, vec![ri(1)]).is_err());
    assert!(z8.add(&z3).is_err());
}

// ---------------------------------------------------------------------------
// QM-122-C42 to C44: Peres, Cabello, the 24-cell and E8 as frame systems.
// ---------------------------------------------------------------------------

fn orthogonal_cliques(rays: &[Vec<i64>], size: usize) -> Vec<Vec<usize>> {
    let orthogonal = |a: usize, b: usize| {
        rays[a]
            .iter()
            .zip(&rays[b])
            .map(|(x, y)| x * y)
            .sum::<i64>()
            == 0
    };
    let mut out = Vec::new();
    let mut stack: Vec<Vec<usize>> = (0..rays.len()).map(|r| vec![r]).collect();
    while let Some(clique) = stack.pop() {
        if clique.len() == size {
            out.push(clique);
            continue;
        }
        let last = *clique.last().unwrap();
        for next in (last + 1)..rays.len() {
            if clique.iter().all(|&c| orthogonal(c, next)) {
                let mut grown = clique.clone();
                grown.push(next);
                stack.push(grown);
            }
        }
    }
    out.sort();
    out
}

#[test]
fn peres_and_cabello_counts_and_the_dimension_of_their_frame_functions() {
    let peres = finite_geometry::peres();
    assert_eq!(
        (peres.rays, peres.orthogonal_pairs, peres.frames),
        (33, 72, 16)
    );
    assert_eq!((peres.incidence_rank, peres.affine_nullity), (16, 17));
    assert!(!peres.has_classical_coloring);
    // Every Peres ray lies in some triad, so the frame polytope is bounded; its
    // 17 affine dimensions exceed the 5 of trace-one symmetric 3 x 3 matrices,
    // so most Peres frame functions come from no symmetric matrix at all.
    assert!(peres.ray_frame_degrees.iter().all(|&d| d >= 1));
    assert!(peres.affine_nullity > 3 * 4 / 2 - 1);
    let cabello = finite_geometry::cabello();
    assert_eq!(
        (
            cabello.rays,
            cabello.orthogonal_pairs,
            cabello.frames,
            cabello.incidence_rank
        ),
        (18, 63, 9, 9)
    );
    assert!(!cabello.has_classical_coloring);
    // The contexts of `contextuality_obstruction` are exactly the orthogonal tetrads.
    let rays: Vec<Vec<i64>> = CABELLO_18_VECTORS
        .iter()
        .map(|r| r.iter().map(|&x| i64::from(x)).collect())
        .collect();
    let mut contexts: Vec<Vec<usize>> = CABELLO_9_CONTEXTS.iter().map(|c| c.to_vec()).collect();
    contexts.sort();
    assert_eq!(orthogonal_cliques(&rays, 4), contexts);
}

#[test]
fn the_bare_twenty_four_cell_has_three_disjoint_tetrads_and_e8_projectors_span_every_symmetric_direction(
) {
    // The twelve rays (e_i +- e_j) of the 24-cell.
    let mut d4 = Vec::new();
    for i in 0..4 {
        for j in (i + 1)..4 {
            for s in [1, -1] {
                let mut v = vec![0i64; 4];
                v[i] = 1;
                v[j] = s;
                d4.push(v);
            }
        }
    }
    let tetrads = orthogonal_cliques(&d4, 4);
    assert_eq!(tetrads.len(), 3);
    let covered: Vec<usize> = tetrads.iter().flatten().copied().collect();
    let distinct: std::collections::BTreeSet<usize> = covered.iter().copied().collect();
    assert_eq!((covered.len(), distinct.len()), (12, 12));
    let system = FrameSystem::new(d4.clone(), tetrads).unwrap();
    assert_eq!(system.ray_degrees(), vec![1; 12]);
    // Every orthogonal pair lies inside one tetrad, so the tetrads constrain
    // independently: 4^3 = 64 colorings.
    let orthogonal_pairs = (0..12)
        .flat_map(|a| ((a + 1)..12).map(move |b| (a, b)))
        .filter(|&(a, b)| d4[a].iter().zip(&d4[b]).map(|(x, y)| x * y).sum::<i64>() == 0)
        .count();
    assert_eq!(orthogonal_pairs, 3 * 6);
    // E8: 120 rays; one coordinate-pair octad is enough to declare the system.
    let e8 = finite_geometry::e8_rays();
    assert_eq!(e8.len(), 120);
    let octad: Vec<usize> = (0..4)
        .flat_map(|k| {
            let rays = &e8;
            [1, -1].map(|s| {
                let mut v = vec![0i64; 8];
                v[2 * k] = 1;
                v[2 * k + 1] = s;
                rays.iter().position(|r| *r == v).unwrap()
            })
        })
        .collect();
    let e8_system = FrameSystem::new(e8.clone(), vec![octad]).unwrap();
    assert_eq!(e8_system.projector_span_rank().unwrap(), 36);
}

// ---------------------------------------------------------------------------
// QM-122-C45 to C48, C50: the diamond complex, declared cyclotomic identities,
// Sorkin sums, rational Cayley isometries, S_3 recoupling, signed permutations.
// ---------------------------------------------------------------------------

fn qexact(rows: &[&[i64]]) -> BasicMatrix<Rational> {
    BasicMatrix::from_row_major(
        rows.len(),
        rows[0].len(),
        rows.iter().flat_map(|r| r.iter().map(|&x| ri(x))).collect(),
    )
    .unwrap()
}

#[test]
fn the_diamond_boundary_cancels_the_interior_edge_and_the_declared_generators_meet_their_identities(
) {
    use linear_algebra::backend::basic_matrix::BasicMatrix;
    let edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)];
    let mut d1 = vec![vec![ri(0); 5]; 4];
    for (j, &(a, b)) in edges.iter().enumerate() {
        d1[a][j] = ri(-1);
        d1[b][j] = ri(1);
    }
    // Triangle (0, 1, 2) and triangle (1, 3, 2), oriented to share edge (1, 2) oppositely.
    let d2 = vec![
        vec![ri(1), ri(0)],
        vec![ri(-1), ri(0)],
        vec![ri(1), ri(-1)],
        vec![ri(0), ri(1)],
        vec![ri(0), ri(-1)],
    ];
    let complex = |second: &Vec<Vec<Rational>>| {
        let b1 = BasicMatrix::from_row_major(4, 5, d1.iter().flatten().cloned().collect()).unwrap();
        let b2 =
            BasicMatrix::from_row_major(5, 2, second.iter().flatten().cloned().collect()).unwrap();
        omega_homology::chain_complex::ChainComplex::new(4, 5, 2, b1, b2)
    };
    assert!(complex(&d2).is_ok());
    assert_eq!(
        matrix::multiply_vector(&matrix::from_rows((&d2).to_vec()).unwrap(), &[ri(1), ri(1)])
            .unwrap(),
        vec![ri(1), ri(-1), ri(0), ri(1), ri(-1)]
    );
    assert_eq!(
        (
            4 - elimination::rank(&matrix::from_rows((&d1).to_vec()).unwrap()).unwrap(),
            5 - elimination::rank(&matrix::from_rows((&d1).to_vec()).unwrap()).unwrap()
                - elimination::rank(&matrix::from_rows((&d2).to_vec()).unwrap()).unwrap()
        ),
        (1, 0)
    );
    // A wrongly oriented second face breaks d1 d2 = 0.
    let bad = vec![
        vec![ri(1), ri(0)],
        vec![ri(-1), ri(0)],
        vec![ri(1), ri(1)],
        vec![ri(0), ri(1)],
        vec![ri(0), ri(-1)],
    ];
    assert!(complex(&bad).is_err());
    // rho_J = i, rho_tau = zeta_3 in Q(zeta_12).
    let z = Cyc12::zeta12(1);
    let (rho_j, rho_tau) = (Cyc12::i(), Cyc12::zeta3());
    assert_eq!(rho_j.mul(&rho_tau).neg(), z);
    let z2 = z.mul(&z);
    assert_eq!((z2.mul(&z), z2.mul(&z2)), (rho_j.clone(), rho_tau.clone()));
    assert!(z2.mul(&z2).sub(&z2).add(&Cyc12::one()).is_zero());
    assert_eq!(rho_j.mul(&rho_j), Cyc12::one().neg());
    assert!(rho_tau
        .mul(&rho_tau)
        .add(&rho_tau)
        .add(&Cyc12::one())
        .is_zero());
    // J and tau on Q^2.
    let j = qexact(&[&[0, 1], &[-1, 0]]);
    let tau = qexact(&[&[-1, 1], &[-1, 0]]);
    let id = matrix::identity::<Rational>(2).unwrap();
    assert_eq!(
        matrix::multiply(&j, &j).unwrap(),
        matrix::scale(&id, &ri(-1)).unwrap()
    );
    assert_eq!(
        matrix::multiply(
            &matrix::multiply(&matrix::multiply(&j, &j).unwrap(), &j).unwrap(),
            &j
        )
        .unwrap(),
        id
    );
    assert_eq!(
        matrix::multiply(&matrix::multiply(&tau, &tau).unwrap(), &tau).unwrap(),
        id
    );
    assert_eq!(
        matrix::add(
            &matrix::add(&matrix::multiply(&tau, &tau).unwrap(), &tau).unwrap(),
            &id
        )
        .unwrap(),
        matrix::zeros::<Rational>(2, 2).unwrap()
    );
}

#[test]
fn third_order_sorkin_sums_vanish_for_linear_and_quadratic_readouts_and_second_order_ones_only_for_linear(
) {
    let vanishing_i3: Vec<u32> = (1..=8)
        .filter(|&p| {
            finite_geometry::sorkin_coefficients(p)
                .unwrap()
                .values()
                .all(Zero::is_zero)
        })
        .collect();
    assert_eq!(vanishing_i3, vec![1, 2]);
    assert_eq!(
        finite_geometry::sorkin_coefficients(3).unwrap()[&[1, 1, 1]],
        ri(6)
    );
    assert_eq!(
        finite_geometry::sorkin(&ri(1), &ri(1), &ri(1), 3).unwrap(),
        ri(6)
    );
    // I_2(a, b) = (a + b)^p - a^p - b^p at (1, 1) is 2^p - 2: zero only for p = 1.
    let vanishing_i2: Vec<u32> = (1..=8)
        .filter(|&p| (ri(2).pow(p as i32) - ri(2)).is_zero())
        .collect();
    assert_eq!(vanishing_i2, vec![1]);
    // Only p = 2 has I_3 = 0 with I_2 != 0; I_3 = 0 alone also admits p = 1.
    let both: Vec<u32> = vanishing_i3
        .iter()
        .copied()
        .filter(|p| !vanishing_i2.contains(p))
        .collect();
    assert_eq!(both, vec![2]);
    assert!(finite_geometry::sorkin_coefficients(0).is_err());
}

fn rational_determinant(m: &Vec<Vec<Rational>>) -> Rational {
    let lcm = m.iter().flatten().fold(BigInt::one(), |acc, x| {
        num_integer::Integer::lcm(&acc, x.denom())
    });
    let scaled: Vec<Vec<BigInt>> = m
        .iter()
        .map(|row| {
            row.iter()
                .map(|x| (x * Rational::from_integer(lcm.clone())).to_integer())
                .collect()
        })
        .collect();
    let det = linear_algebra::determinant::bareiss_determinant(&scaled).unwrap();
    Rational::new(det, lcm.pow(m.len() as u32))
}

#[test]
fn skew_rational_matrices_span_so8_and_their_cayley_transforms_lie_in_so8_q() {
    let mut basis = Vec::new();
    for i in 0..8 {
        for j in (i + 1)..8 {
            let mut m = vec![vec![ri(0); 8]; 8];
            m[i][j] = ri(1);
            m[j][i] = ri(-1);
            basis.push(m);
        }
    }
    let flat: Vec<Vec<Rational>> = basis
        .iter()
        .map(|m| m.iter().flatten().cloned().collect())
        .collect();
    assert_eq!(
        elimination::rank(&matrix::from_rows((&flat).to_vec()).unwrap()).unwrap(),
        28
    );
    let is_skew =
        |m: &Vec<Vec<Rational>>| (0..8).all(|i| (0..8).all(|j| m[i][j] == -m[j][i].clone()));
    for a in 0..basis.len() {
        for b in (a + 1)..basis.len() {
            let ab = matrix::multiply(
                &matrix::from_rows((&basis[a]).to_vec()).unwrap(),
                &matrix::from_rows((&basis[b]).to_vec()).unwrap(),
            )
            .and_then(|m| matrix::to_rows(&m))
            .unwrap();
            let ba = matrix::multiply(
                &matrix::from_rows((&basis[b]).to_vec()).unwrap(),
                &matrix::from_rows((&basis[a]).to_vec()).unwrap(),
            )
            .and_then(|m| matrix::to_rows(&m))
            .unwrap();
            let bracket: Vec<Vec<Rational>> = ab
                .iter()
                .zip(&ba)
                .map(|(x, y)| x.iter().zip(y).map(|(p, q)| p - q).collect())
                .collect();
            assert!(is_skew(&bracket));
        }
    }
    // skew[i][j] = (i + j + 1)/17 above the diagonal, its negative below.
    let skew: Vec<Vec<Rational>> = (0..8i64)
        .map(|i| {
            (0..8i64)
                .map(|j| rq((i + j + 1) * (j - i).signum(), 17))
                .collect()
        })
        .collect();
    assert!(is_skew(&skew));
    for tau in [rq(1, 3), rq(-5, 2), ri(7)] {
        let c = omega_lie_theory::cayley::cayley_transform(
            &linear_algebra::exact_field::matrix::from_rows((&skew).to_vec()).unwrap(),
            &tau,
        )
        .and_then(|m| {
            linear_algebra::exact_field::matrix::to_rows(&m)
                .map_err(omega_lie_theory::cayley::CayleyError::from)
        })
        .unwrap();
        assert!(omega_lie_theory::cayley::is_orthogonal(
            &matrix::from_rows((&c).to_vec()).unwrap()
        ));
        assert_eq!(rational_determinant(&c), ri(1));
        // I + C is invertible: -1 is never an eigenvalue of a Cayley transform.
        let shifted: Vec<Vec<Rational>> = c
            .iter()
            .enumerate()
            .map(|(i, row)| {
                row.iter()
                    .enumerate()
                    .map(|(k, x)| if i == k { x + ri(1) } else { x.clone() })
                    .collect()
            })
            .collect();
        assert!(!rational_determinant(&shifted).is_zero());
    }
    // So diag(-1, -1, 1, .., 1), a rational rotation with I + R singular, is not a Cayley transform.
    let flip: Vec<Vec<Rational>> = (0..8)
        .map(|i| {
            (0..8)
                .map(|j| {
                    ri(if i != j {
                        0
                    } else if i < 2 {
                        -1
                    } else {
                        1
                    })
                })
                .collect()
        })
        .collect();
    assert!(
        omega_lie_theory::cayley::is_orthogonal(&matrix::from_rows((&flip).to_vec()).unwrap())
            && rational_determinant(&flip) == ri(1)
    );
    assert!(omega_lie_theory::cayley::cayley_transform(
        &matrix::from_rows((&identity_q(2)).to_vec()).unwrap(),
        &ri(1)
    )
    .is_err());
}

/// The corrected H019 numerator of the Cayley transform of `X_ij = E_ij - E_ji`
/// at `tau = p/q`: for `i = j` the generator is zero and the numerator is
/// `(p^2 + q^2) I`. With `corrected = false`, the published formula, which has
/// no `i = j` case.
fn h019_numerator(i: usize, j: usize, p: i64, q: i64, corrected: bool) -> Vec<Vec<Rational>> {
    let (pp, qq) = (p * p, q * q);
    (0..8)
        .map(|r| {
            (0..8)
                .map(|c| {
                    ri(if corrected && i == j {
                        if r == c {
                            pp + qq
                        } else {
                            0
                        }
                    } else if r == i && c == i {
                        qq - pp
                    } else if r == i && c == j {
                        -2 * p * q
                    } else if r == j && c == i {
                        2 * p * q
                    } else if r == j && c == j {
                        qq - pp
                    } else if r == c {
                        pp + qq
                    } else {
                        0
                    })
                })
                .collect()
        })
        .collect()
}

#[test]
fn the_rust_cayley_transform_matches_the_corrected_h019_numerator() {
    // finite_geometry::cayley solves (I - tau X)(I + tau X)^-1 exactly, so it has no
    // separate zero-generator case to get wrong: it agrees with the corrected
    // numerator for every X_ij, X_ii = 0 included.
    for (p, q) in [(1i64, 1i64), (1, 2), (3, 4), (2, 1)] {
        let denominator = ri(p * p + q * q);
        for i in 0..8 {
            for j in 0..8 {
                let mut x = vec![vec![ri(0); 8]; 8];
                if i != j {
                    x[i][j] = ri(1);
                    x[j][i] = ri(-1);
                }
                let c = omega_lie_theory::cayley::cayley_transform(
                    &linear_algebra::exact_field::matrix::from_rows((&x).to_vec()).unwrap(),
                    &rq(p, q),
                )
                .and_then(|m| {
                    linear_algebra::exact_field::matrix::to_rows(&m)
                        .map_err(omega_lie_theory::cayley::CayleyError::from)
                })
                .unwrap();
                let scaled: Vec<Vec<Rational>> = c
                    .iter()
                    .map(|row| row.iter().map(|v| v * &denominator).collect())
                    .collect();
                assert_eq!(
                    scaled,
                    h019_numerator(i, j, p, q, true),
                    "X_{i}{j} at tau = {p}/{q}"
                );
            }
        }
        // The published numerator of a zero generator is not (p^2 + q^2) I.
        assert_ne!(
            h019_numerator(3, 3, p, q, false),
            h019_numerator(3, 3, p, q, true)
        );
    }
    // At p = q = 1 its repeated-index entry is 0, so it is singular.
    assert!(rational_determinant(&h019_numerator(0, 0, 1, 1, false)).is_zero());
}

#[test]
fn the_rational_recoupling_matrices_generate_s3_and_satisfy_the_braid_relation() {
    let s12 = qmat(&[&[(1, 1), (0, 1)], &[(0, 1), (-1, 1)]]);
    let s23 = qmat(&[&[(-1, 2), (1, 1)], &[(3, 4), (1, 2)]]);
    let mul = |a: &Vec<Vec<Rational>>, b: &Vec<Vec<Rational>>| {
        matrix::multiply(
            &matrix::from_rows((a).to_vec()).unwrap(),
            &matrix::from_rows((b).to_vec()).unwrap(),
        )
        .and_then(|m| matrix::to_rows(&m))
        .unwrap()
    };
    let id = identity_q(2);
    assert_eq!(mul(&s12, &s12), id);
    assert_eq!(mul(&s23, &s23), id);
    let rotation = mul(&s12, &s23);
    assert_eq!(mul(&mul(&rotation, &rotation), &rotation), id);
    assert_eq!(rational_determinant(&s23), ri(-1));
    // What the source calls the rational pentagon is this braid relation.
    assert_eq!(mul(&mul(&s23, &s12), &s23), mul(&mul(&s12, &s23), &s12));
    // The generated group has six elements.
    let as_qi = |m: &Vec<Vec<Rational>>| {
        matrix::from_rows(
            m.iter()
                .map(|row| {
                    row.iter()
                        .map(|x| GaussianRat::from_rational(x.clone()))
                        .collect()
                })
                .collect(),
        )
        .unwrap()
    };
    let group = omega_lie_theory::finite_group::generate(
        &[as_qi(&s12), as_qi(&s23)],
        matrix::identity::<GaussianRat>(2).unwrap(),
        |a, b| matrix::multiply(a, b).expect("admitted two-dimensional generators"),
        |m| m.as_slice().to_vec(),
        12,
    )
    .unwrap();
    assert_eq!(group.len(), 6);
    // Characters on (identity, transpositions, three-cycles), class sizes (1, 3, 2).
    let trace = |m: &Vec<Vec<Rational>>| &m[0][0] + &m[1][1];
    let standard = [trace(&id), trace(&s12), trace(&rotation)];
    assert_eq!(standard, [ri(2), ri(0), ri(-1)]);
    assert_eq!(trace(&s23), ri(0));
    let sizes = [ri(1), ri(3), ri(2)];
    let characters = [[ri(1), ri(1), ri(1)], [ri(1), ri(-1), ri(1)], standard];
    for a in 0..3 {
        for b in 0..3 {
            let inner: Rational = (0..3)
                .map(|k| &sizes[k] * &characters[a][k] * &characters[b][k])
                .sum();
            assert_eq!(inner, ri(if a == b { 6 } else { 0 }));
        }
    }
}

#[test]
fn the_integer_matrices_preserving_the_standard_form_are_the_signed_permutations() {
    for (n, expected) in [(2usize, 8usize), (3, 48)] {
        let mut count = 0;
        for code in 0..3usize.pow((n * n) as u32) {
            let mut c = code;
            let m: Vec<Vec<i64>> = (0..n)
                .map(|_| {
                    (0..n)
                        .map(|_| {
                            let digit = (c % 3) as i64 - 1;
                            c /= 3;
                            digit
                        })
                        .collect()
                })
                .collect();
            let orthogonal = (0..n).all(|i| {
                (0..n).all(|j| (0..n).map(|k| m[k][i] * m[k][j]).sum::<i64>() == i64::from(i == j))
            });
            if !orthogonal {
                continue;
            }
            count += 1;
            assert!(m
                .iter()
                .all(|row| row.iter().filter(|&&x| x != 0).count() == 1));
            // It preserves the l1 norm on a box of integer vectors.
            for v in 0..5usize.pow(n as u32) {
                let x: Vec<i64> = (0..n)
                    .map(|k| ((v / 5usize.pow(k as u32)) % 5) as i64 - 2)
                    .collect();
                let y: Vec<i64> = (0..n)
                    .map(|i| (0..n).map(|k| m[i][k] * x[k]).sum())
                    .collect();
                assert_eq!(
                    y.iter().map(|a| a.abs()).sum::<i64>(),
                    x.iter().map(|a| a.abs()).sum::<i64>()
                );
            }
        }
        assert_eq!(count, expected, "n = {n}");
    }
}

// ---------------------------------------------------------------------------
// QM-122-C51: the Cayley hinge spectrum.
// ---------------------------------------------------------------------------

fn two_by_two<T: Involution>(entries: [[T; 2]; 2]) -> BasicMatrix<T> {
    BasicMatrix::from_row_major(2, 2, entries.into_iter().flatten().collect()).unwrap()
}

fn matrix_power<T: Involution>(m: &BasicMatrix<T>, k: usize) -> BasicMatrix<T> {
    (0..k).fold(matrix::identity(2).unwrap(), |acc, _| {
        matrix::multiply(&acc, m).unwrap()
    })
}

/// `(I - tau X) = C (I + tau X)` with `X = [[0, -1], [1, 0]]`: `C` is the
/// Cayley transform of `tau X`, checked without dividing.
fn is_cayley_transform<T: Involution>(c: &BasicMatrix<T>, tau: &T) -> bool {
    let (one, zero) = (T::one(), T::zero());
    let minus = zero.sub(tau);
    let left = two_by_two([[one.clone(), tau.clone()], [minus.clone(), one.clone()]]);
    let right = two_by_two([[one.clone(), minus], [tau.clone(), one]]);
    left == matrix::multiply(&c, &right).unwrap()
}

#[test]
fn rational_cayley_rotations_have_finite_order_only_at_zero_and_plus_minus_one() {
    let x = qmat(&[&[(0, 1), (-1, 1)], &[(1, 1), (0, 1)]]);
    let mut torsion = Vec::new();
    let mut grid = 0;
    for p in -12i64..=12 {
        for q in 1i64..=12 {
            if num_integer::Integer::gcd(&p, &q) != 1 {
                continue;
            }
            grid += 1;
            let tau = rq(p, q);
            let u = unit_from_parameter(&tau);
            // The Cayley matrix is the rotation [[re u, im u], [-im u, re u]].
            let c = omega_lie_theory::cayley::cayley_transform(
                &linear_algebra::exact_field::matrix::from_rows((&x).to_vec()).unwrap(),
                &tau,
            )
            .and_then(|m| {
                linear_algebra::exact_field::matrix::to_rows(&m)
                    .map_err(omega_lie_theory::cayley::CayleyError::from)
            })
            .unwrap();
            assert_eq!(
                c,
                vec![
                    vec![u.re.clone(), u.im.clone()],
                    vec![-u.im.clone(), u.re.clone()]
                ]
            );
            if let Some(order) = multiplicative_order(&u, 24) {
                torsion.push((tau, order));
            }
        }
    }
    assert_eq!(grid, 183);
    assert_eq!(torsion, vec![(ri(-1), 4), (ri(0), 1), (ri(1), 4)]);
}

#[test]
fn hinge_closure_up_to_sign_admits_parameters_outside_the_declared_twelfth_cyclotomic_spectrum() {
    // tau = sqrt 2 - 1 over Q(zeta_8): its Cayley transform is the eighth turn, C^4 = -I.
    let tau = Cyc8::sqrt2().sub(&Cyc8::one());
    let s = Cyc8::sqrt2().scale_rat(&rq(1, 2));
    let c = two_by_two([[s.clone(), s.clone()], [s.neg(), s.clone()]]);
    assert!(is_cayley_transform(&c, &tau));
    let id = matrix::identity::<Cyc8>(2).unwrap();
    let minus_id = matrix::scale(&id, &Cyc8::one().neg()).unwrap();
    assert_eq!(matrix_power(&c, 4), minus_id);
    assert!(matrix_power(&c, 2) != id && matrix_power(&c, 2) != minus_id);
    // tau is a root of none of the source's spectrum polynomials: tau, tau^2 - 1,
    // tau^2 - 3, 3 tau^2 - 1, tau^2 - 4 tau + 1, tau^2 + 4 tau + 1.
    let t2 = tau.mul(&tau);
    let four_tau = tau.scale_rat(&ri(4));
    let candidates = [
        tau.clone(),
        t2.sub(&Cyc8::one()),
        t2.sub(&Cyc8::one().scale_rat(&ri(3))),
        t2.scale_rat(&ri(3)).sub(&Cyc8::one()),
        t2.sub(&four_tau).add(&Cyc8::one()),
        t2.add(&four_tau).add(&Cyc8::one()),
    ];
    assert!(candidates.iter().all(|value| !value.is_zero()));
    // tau = sqrt 3 - 2 over Q(zeta_12) has order exactly 12, yet solves
    // tau^2 + 4 tau + 1 = 0, not the source's tau^2 - 4 tau + 1 = 0.
    let sqrt3 = Cyc12::zeta12(1).add(&Cyc12::zeta12(11));
    assert_eq!(sqrt3.mul(&sqrt3), Cyc12::one().scale_rat(&ri(3)));
    let tau12 = sqrt3.sub(&Cyc12::one().scale_rat(&ri(2)));
    let half = rq(1, 2);
    let c12 = two_by_two([
        [sqrt3.scale_rat(&half), Cyc12::one().scale_rat(&rq(-1, 2))],
        [
            Cyc12::one().scale_rat(&half.clone()),
            sqrt3.scale_rat(&half),
        ],
    ]);
    assert!(is_cayley_transform(&c12, &tau12));
    let id12 = matrix::identity::<Cyc12>(2).unwrap();
    assert_eq!(matrix_power(&c12, 12), id12);
    assert!(matrix_power(&c12, 6) != id12 && matrix_power(&c12, 4) != id12);
    let t12 = tau12.mul(&tau12);
    let four = tau12.scale_rat(&ri(4));
    assert!(t12.add(&four).add(&Cyc12::one()).is_zero());
    assert!(!t12.sub(&four).add(&Cyc12::one()).is_zero());
    // 1 / sqrt 3 is not an algebraic integer: its square is 1/3, and its
    // coordinates in the integral basis of Z[zeta_12] are not integers.
    let inv_sqrt3 = sqrt3.scale_rat(&rq(1, 3));
    assert_eq!(inv_sqrt3.mul(&inv_sqrt3).as_rational(), Some(rq(1, 3)));
    assert!(!inv_sqrt3.is_integer_ring_element());
    assert!(CyclotomicInteger::new(12, inv_sqrt3.a.to_vec()).is_err());
}

#[test]
fn the_hinge_defect_vanishes_only_on_the_identity_and_retardation_composes_with_an_inverse_turn() {
    let x = qmat(&[&[(0, 1), (-1, 1)], &[(1, 1), (0, 1)]]);
    let taus = [rq(1, 2), rq(-1, 2), rq(1, 3), rq(2, 7), ri(3), rq(-1, 3)];
    for a in &taus {
        for b in &taus {
            for c in &taus {
                let u = [a, b, c]
                    .iter()
                    .map(|t| {
                        omega_lie_theory::cayley::cayley_transform(
                            &linear_algebra::exact_field::matrix::from_rows((&x).to_vec()).unwrap(),
                            t,
                        )
                        .and_then(|m| {
                            linear_algebra::exact_field::matrix::to_rows(&m)
                                .map_err(omega_lie_theory::cayley::CayleyError::from)
                        })
                        .unwrap()
                    })
                    .reduce(|acc, m| {
                        matrix::multiply(
                            &matrix::from_rows((&acc).to_vec()).unwrap(),
                            &matrix::from_rows((&m).to_vec()).unwrap(),
                        )
                        .and_then(|m| matrix::to_rows(&m))
                        .unwrap()
                    })
                    .unwrap();
                let defect = ri(2) - (&u[0][0] + &u[1][1]);
                assert!(!defect.is_negative());
                assert_eq!(defect.is_zero(), u == identity_q(2));
            }
        }
    }
    // tau_c = (tau_0 - eps) / (1 + tau_0 eps) is the parameter of the turn by
    // tau_0 followed by the inverse turn by eps.
    let retarded = |t0: &Rational, eps: &Rational| (t0 - eps) / (ri(1) + t0 * eps);
    for t0 in [rq(1, 2), rq(1, 3), ri(2)] {
        for eps in [rq(1, 4), rq(1, 10), rq(1, 2)] {
            let tc = retarded(&t0, &eps);
            assert_eq!(
                unit_from_parameter(&tc),
                unit_from_parameter(&t0).mul(&unit_from_parameter(&eps).conj())
            );
            assert!(tc < t0);
        }
    }
    // With a negative clock parameter the "retarded" parameter exceeds it.
    assert_eq!(retarded(&ri(-2), &ri(1)), ri(3));
}

// ---------------------------------------------------------------------------
// QM-122-C52 to C65: what the declared simplicial and spin-foam models compute.
// ---------------------------------------------------------------------------

#[test]
fn the_area_count_and_page_schedule_are_arithmetic_of_the_declared_model() {
    let model = area_model(2, &[[(0, 1), (1, 0)]], 2).unwrap();
    assert_eq!(
        (model.tetrahedra, model.internal_faces, model.boundary_area),
        (2, 1, 6)
    );
    let parse = |s: &str| s.parse::<u64>().unwrap();
    assert_eq!(
        parse(&model.bulk_states),
        parse(&model.boundary_states) * parse(&model.reduction)
    );
    assert_eq!(
        (parse(&model.bulk_states), model.entropy_convention.as_str()),
        (256, "3/2")
    );
    assert!(area_model(2, &[[(0, 0), (1, 0)], [(0, 0), (1, 1)]], 2).is_err());
    let page = page_curve(12, 6, 2, &rq(1, 2), &rq(1, 4)).unwrap();
    let entropies: Vec<&str> = page.iter().map(|s| s.entropy.as_str()).collect();
    assert_eq!(entropies, vec!["0", "1/2", "1", "3/2", "1", "1/2", "0"]);
    // The last black-hole area is zero because the schedule radiates everything.
    assert_eq!((page[6].black_hole_area, page[6].radiation_area), (0, 12));
    assert_eq!(
        (page[6].clock.as_str(), page[6].rate_ratio.as_str()),
        ("2/9", "4/9")
    );
    assert!(page_curve(12, 6, 2, &rq(1, 4), &rq(1, 2)).is_err());
}

#[test]
fn global_force_and_momentum_balances_hold_for_any_declared_data() {
    let positions = vec![
        vec![ri(0), ri(0), ri(0)],
        vec![rq(3, 2), ri(1), ri(-2)],
        vec![ri(5), rq(-1, 3), ri(4)],
        vec![ri(1), ri(7), rq(2, 5)],
    ];
    let hinges = vec![
        (0, 1, rq(9, 7)),
        (1, 2, ri(-4)),
        (2, 3, rq(1, 11)),
        (0, 3, ri(13)),
        (0, 2, rq(-5, 3)),
    ];
    let (local, total, torque) =
        omega_general_relativity::simplicial_dynamics::bianchi(&positions, &hinges).unwrap();
    assert!(total.iter().all(Zero::is_zero));
    assert!(matrix::is_zero_matrix(&torque));
    assert!(
        local.iter().any(|f| f.iter().any(|x| !x.is_zero())),
        "local closure fails"
    );
    let mut body = matrix::zeros::<Rational>(3, 3).unwrap();
    let mut radiation = body.clone();
    omega_general_relativity::simplicial_dynamics::emit_angular(
        &mut body,
        &mut radiation,
        &[ri(4), rq(-2, 9), ri(1)],
        &[ri(-7), ri(3), rq(5, 2)],
    )
    .unwrap();
    for i in 0..3 {
        for j in 0..3 {
            assert!((body.get_ref(i, j).unwrap() + radiation.get_ref(i, j).unwrap()).is_zero());
        }
    }
    // The four-simplex boundary sum vanishes for arbitrary hinge weights: it is d d = 0.
    let faces = [
        [0, 1, 2],
        [0, 1, 3],
        [0, 1, 4],
        [0, 2, 3],
        [0, 2, 4],
        [0, 3, 4],
        [1, 2, 3],
        [1, 2, 4],
        [1, 3, 4],
        [2, 3, 4],
    ];
    let defects = faces
        .into_iter()
        .enumerate()
        .map(|(k, f)| (f, rq(k as i64 * 7 - 3, 5)))
        .collect();
    let simplex = ReggeFourSimplex {
        positions: std::array::from_fn(|i| {
            std::array::from_fn(|j| ri(((i * 3 + j * 5) % 7) as i64))
        }),
        hinge_defects: defects,
    };
    assert!(simplex
        .boundary_bianchi()
        .unwrap()
        .as_slice()
        .iter()
        .all(Zero::is_zero));
}

#[test]
fn the_declared_constraint_bracket_is_a_commutator_of_numbers() {
    let positions = vec![
        [ri(0), ri(0), ri(0)],
        [ri(1), ri(0), ri(0)],
        [ri(0), ri(1), ri(0)],
        [ri(0), ri(0), ri(1)],
        [ri(0), ri(0), ri(-1)],
    ];
    let mut slice = CauchySlice::new(positions, vec![[0, 1, 2, 3], [0, 1, 2, 4]]).unwrap();
    let skew = vec![
        vec![ri(0), ri(-1), ri(0)],
        vec![ri(1), ri(0), ri(0)],
        vec![ri(0), ri(0), ri(0)],
    ];
    slice
        .set_connection(
            0,
            1,
            &linear_algebra::exact_field::matrix::from_rows(skew).unwrap(),
            &rq(1, 2),
        )
        .unwrap();
    assert!(!slice.constraints().scalar.iter().all(Zero::is_zero));
    for (n, m) in [(ri(2), ri(3)), (rq(-1, 2), ri(5))] {
        let (bracket, induced, anomaly) = slice.scalar_anomaly(0, 1, &n, &m).unwrap();
        assert!(bracket.is_zero(), "rational numbers commute");
        assert_eq!(anomaly, -induced);
    }
}

#[test]
fn spin_foam_amplitudes_are_signs_and_the_transition_matrix_is_not_unitary() {
    let signs = [
        CyclotomicInteger::scalar(12, 0).unwrap(),
        CyclotomicInteger::scalar(12, 1).unwrap(),
        CyclotomicInteger::scalar(12, -1).unwrap(),
    ];
    for level in [2u32, 3] {
        for code in 0..level.pow(6) {
            let mut c = code;
            let spins: [u32; 6] = std::array::from_fn(|_| {
                let s = c % level;
                c /= level;
                s
            });
            let a = finite_spinfoam::tetrahedron(&spins);
            assert!(signs.contains(&a), "tetrahedron {spins:?}");
            assert_eq!(a.conj(), a);
        }
    }
    for code in 0..1024u32 {
        let spins: [u32; 10] = std::array::from_fn(|i| (code >> i) & 1);
        assert!(signs.contains(&finite_spinfoam::simplex4(&spins)));
    }
    let q2 = finite_spinfoam::quantum_integer(2);
    assert_eq!(
        q2.mul(&q2).unwrap(),
        CyclotomicInteger::scalar(12, 3).unwrap()
    );
    assert_eq!(
        finite_spinfoam::quantum_integer(6),
        CyclotomicInteger::scalar(12, 0).unwrap()
    );
    // In the published model every transition between the eight admissible
    // four-spin boundaries is 1, so the vacuum column has squared norm 8, not 1.
    let boundaries: Vec<[u32; 4]> = (0..16u32)
        .map(|c| std::array::from_fn(|i| (c >> i) & 1))
        .filter(|s: &[u32; 4]| finite_spinfoam::admissible(s))
        .collect();
    assert_eq!(boundaries.len(), 8);
    let column_norm =
        boundaries
            .iter()
            .fold(CyclotomicInteger::scalar(12, 0).unwrap(), |acc, out| {
                let w =
                    finite_spinfoam::transition(ModelVersion::Published, &[0; 4], out, &[0; 10]);
                acc.add(&w.conj().mul(&w).unwrap()).unwrap()
            });
    assert_eq!(column_norm, CyclotomicInteger::scalar(12, 8).unwrap());
    // The published Pachner "partition" multiplies an amplitude by itself, not by its conjugate.
    let state = PachnerState {
        external: [0; 6],
        internal: vec![0],
        amplitude: CyclotomicInteger::zeta(12).unwrap().pow(3),
    };
    assert_eq!(
        state.partition(ModelVersion::Published).unwrap(),
        CyclotomicInteger::scalar(12, -1).unwrap()
    );
}

fn cyclo(k: i64) -> CyclotomicInteger {
    CyclotomicInteger::scalar(12, k).unwrap()
}

fn norm_squared(psi: &[Cyc12]) -> Cyc12 {
    involution::inner_product(psi, psi).unwrap()
}
fn static12(z: &CyclotomicInteger) -> Cyc12 {
    assert_eq!(z.conductor(), 12);
    Cyc12 {
        a: std::array::from_fn(|i| {
            z.coefficient_values()
                .get(i)
                .cloned()
                .unwrap_or_else(Rational::zero)
        }),
    }
}

#[test]
fn the_corrected_spin_foam_transition_is_unitary_on_the_admissible_basis() {
    // The basis is the set of admissible binary boundaries, each once.
    let mut basis = finite_spinfoam::ADMISSIBLE_BASIS.to_vec();
    basis.sort();
    let mut admissible: Vec<[u32; 4]> = (0..16u32)
        .map(|c| std::array::from_fn(|i| (c >> i) & 1))
        .filter(|s: &[u32; 4]| finite_spinfoam::admissible(s))
        .collect();
    admissible.sort();
    assert_eq!(basis, admissible);
    let identity = matrix::identity::<Cyc12>(8).unwrap();
    let zero = matrix::zeros::<Cyc12>(8, 8).unwrap();
    let mut unitary_bulks = 0;
    for code in 0..1024u32 {
        let bulk: [u32; 10] = std::array::from_fn(|i| (code >> i) & 1);
        let a = finite_spinfoam::simplex4(&bulk);
        let corrected = finite_spinfoam::transition_matrix(ModelVersion::Corrected, &bulk);
        let published = finite_spinfoam::transition_matrix(ModelVersion::Published, &bulk);
        // Corrected: a(W) on the diagonal. Published: a(W) in every entry.
        for r in 0..8 {
            for c in 0..8 {
                assert_eq!(
                    *corrected.get_ref(r, c).unwrap(),
                    if r == c { static12(&a) } else { Cyc12::zero() }
                );
                assert_eq!(*published.get_ref(r, c).unwrap(), static12(&a));
            }
        }
        // The reversed bulk realizes the adjoint, in both versions.
        let reversed = finite_spinfoam::adjoint_bulk(&bulk);
        for (version, t) in [
            (ModelVersion::Corrected, &corrected),
            (ModelVersion::Published, &published),
        ] {
            assert_eq!(
                finite_spinfoam::transition_matrix(version, &reversed),
                involution::adjoint(t).unwrap()
            );
        }
        if a != cyclo(0) {
            // a(W) = +-1, so the corrected matrix is unitary and the published one is 8 times all-ones.
            assert!(a == cyclo(1) || a == cyclo(-1));
            assert_eq!(
                matrix::multiply(&involution::adjoint(&corrected).unwrap(), &corrected).unwrap(),
                identity
            );
            assert_eq!(
                matrix::multiply(&involution::adjoint(&published).unwrap(), &published).unwrap(),
                matrix::from_rows(vec![vec![Cyc12::one().scale_rat(&ri(8)); 8]; 8]).unwrap()
            );
            unitary_bulks += 1;
        } else if code % 97 == 0 {
            // A bulk with amplitude 0 gives the zero matrix in both versions.
            assert_eq!(
                matrix::multiply(&involution::adjoint(&corrected).unwrap(), &corrected).unwrap(),
                zero
            );
        }
    }
    assert_eq!(unitary_bulks, 64);

    // The vacuum bulk is the identity channel, and it preserves the norm of a
    // wavepacket; the published vacuum sends it to 8 |sum psi|^2.
    let z = Cyc12::zeta12(1);
    let psi: Vec<Cyc12> = (0..8)
        .map(|k| {
            omega_number_theory::scalar::power_unsigned(&z, k as u64)
                .unwrap()
                .add(&Cyc12::one().scale_rat(&ri(k as i64)))
        })
        .collect();
    let vacuum = [0u32; 10];
    let corrected = finite_spinfoam::transition_matrix(ModelVersion::Corrected, &vacuum);
    assert_eq!(corrected, identity);
    assert_eq!(
        norm_squared(&matrix::multiply_vector(&corrected, &psi).unwrap()),
        norm_squared(&psi)
    );
    let published = finite_spinfoam::transition_matrix(ModelVersion::Published, &vacuum);
    let total = psi.iter().fold(Cyc12::zero(), |acc, v| acc.add(v));
    assert_eq!(
        norm_squared(&matrix::multiply_vector(&published, &psi).unwrap()),
        Cyc12::one()
            .scale_rat(&ri(8))
            .mul(&total.conj().mul(&total))
    );
    assert_ne!(
        norm_squared(&matrix::multiply_vector(&published, &psi).unwrap()),
        norm_squared(&psi)
    );
    // A bulk with a(W) = -1 flips the sign and still preserves the norm.
    let flip = (0..1024u32)
        .map(|code| -> [u32; 10] { std::array::from_fn(|i| (code >> i) & 1) })
        .find(|bulk| finite_spinfoam::simplex4(bulk) == cyclo(-1))
        .expect("a bulk with amplitude -1");
    let t = finite_spinfoam::transition_matrix(ModelVersion::Corrected, &flip);
    assert_eq!(
        matrix::multiply_vector(&t, &psi).unwrap(),
        psi.iter().map(|v| v.scale_rat(&ri(-1))).collect::<Vec<_>>()
    );
    assert_eq!(
        norm_squared(&matrix::multiply_vector(&t, &psi).unwrap()),
        norm_squared(&psi)
    );
    // An inadmissible boundary is annihilated, and a boundary never reaches another.
    assert_eq!(
        finite_spinfoam::transition(
            ModelVersion::Corrected,
            &[1, 0, 0, 0],
            &[1, 0, 0, 0],
            &vacuum
        ),
        cyclo(0)
    );
    assert_eq!(
        finite_spinfoam::transition(ModelVersion::Corrected, &[0; 4], &[1, 1, 0, 0], &vacuum),
        cyclo(0)
    );
    assert!(
        matrix::from_rows(vec![vec![Cyc12::one()], vec![Cyc12::one(), Cyc12::zero()]]).is_err()
    );
}

#[test]
fn the_corrected_pachner_partition_is_a_nonnegative_norm() {
    let z = CyclotomicInteger::zeta(12).unwrap();
    // All 81 amplitudes c0 + c1 zeta + c2 zeta^2 + c3 zeta^3 with coefficients in {-1, 0, 1}.
    let amplitudes: Vec<CyclotomicInteger> = (0..81i64)
        .map(|code| {
            (0..4).fold(cyclo(0), |acc, k| {
                acc.add(
                    &z.pow(k)
                        .mul(&cyclo(code / 3i64.pow(k as u32) % 3 - 1))
                        .unwrap(),
                )
                .unwrap()
            })
        })
        .collect();
    assert_eq!(amplitudes.iter().filter(|a| **a == cyclo(0)).count(), 1);
    let externals = [
        [0u32; 6],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
    ];
    for external in externals {
        let admissible = finite_spinfoam::admissible(&external);
        for a in &amplitudes {
            let state = PachnerState {
                external,
                internal: vec![1],
                amplitude: a.clone(),
            };
            let norm = state.partition(ModelVersion::Corrected).unwrap();
            let value = finite_spinfoam::real_value(&norm)
                .unwrap()
                .expect("a Hermitian norm is real");
            assert!(value.is_nonnegative(), "{external:?} {a:?}");
            // Zero exactly on the zero amplitude and on inadmissible states.
            assert_eq!(value.is_zero(), !admissible || *a == cyclo(0));
            // Invariant under unit phases and under the 2-3 move.
            for k in [1, 3, 5, 11] {
                let rotated = PachnerState {
                    amplitude: a.mul(&z.pow(k)).unwrap(),
                    ..state.clone()
                };
                assert_eq!(rotated.partition(ModelVersion::Corrected).unwrap(), norm);
            }
            assert_eq!(
                state
                    .two_to_three()
                    .unwrap()
                    .partition(ModelVersion::Corrected)
                    .unwrap(),
                norm
            );
        }
    }
    // |1 + zeta|^2 = 2 + sqrt(3): irrational, and positive.
    let one_plus = PachnerState {
        external: [0; 6],
        internal: vec![0],
        amplitude: cyclo(1).add(&z).unwrap(),
    };
    let norm = one_plus.partition(ModelVersion::Corrected).unwrap();
    assert_eq!(
        finite_spinfoam::real_value(&norm).unwrap(),
        Some(omega_number_theory::quadratic::Quadratic::<3>::new(
            ri(2),
            ri(1)
        ))
    );
    // The published product is no norm: amplitude i gives -1, and zeta gives zeta^2, which is not real.
    let vacuum = |amplitude: CyclotomicInteger| PachnerState {
        external: [0; 6],
        internal: vec![0],
        amplitude,
    };
    let minus =
        finite_spinfoam::real_value(&vacuum(z.pow(3)).partition(ModelVersion::Published).unwrap())
            .unwrap()
            .unwrap();
    assert_eq!(
        minus,
        omega_number_theory::quadratic::Quadratic::<3>::new(ri(-1), ri(0))
    );
    assert!(!minus.is_nonnegative());
    assert_eq!(
        finite_spinfoam::real_value(
            &vacuum(z.clone())
                .partition(ModelVersion::Published)
                .unwrap()
        )
        .unwrap(),
        None
    );
}
