//! Physical frame and geometry checks replay through canonical exact linear algebra.
//! Fixture incidence/projector rows become BasicMatrix before numerical operations.
//! Cayley transforms are independently compared with column-image solves.
//! The Sorkin campaign evaluation agrees with the actual programme target receipt.
//!
//! AuthorityEffect: None.

use finite_qm_native::campaigns::cancellation_certificates::evaluate_sorkin_i3_cancellation;
use finite_qm_native::campaigns::foundational_targets::verify_target3_sorkin_interference;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::matrix as mx;
use linear_algebra::linear_algebra::image_kernel::{
    solve_in_image, ExactRowReduction, ImageMembership,
};
use omega_lie_theory::cayley::{cayley_transform, is_orthogonal};
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::finite_geometry::{cabello, interface_defect};
use omega_quantum_physics::frame_function_polytope::{FramePolytopeError, FrameSystem};
use omega_quantum_physics::kochen_specker::{CABELLO_18_VECTORS, CABELLO_9_CONTEXTS};

fn cabello_system() -> FrameSystem {
    FrameSystem::new(
        CABELLO_18_VECTORS
            .iter()
            .map(|r| r.iter().map(|&x| i64::from(x)).collect())
            .collect(),
        CABELLO_9_CONTEXTS.iter().map(|c| c.to_vec()).collect(),
    )
    .unwrap()
}

/// The rays and frames of every system compared below: the Cabello configuration and
/// three small planar systems that reach the rank-deficient and non-spanning branches.
fn systems() -> Vec<(Vec<Vec<i64>>, Vec<Vec<usize>>)> {
    let cabello_rays: Vec<Vec<i64>> = CABELLO_18_VECTORS
        .iter()
        .map(|r| r.iter().map(|&x| i64::from(x)).collect())
        .collect();
    let cabello_frames: Vec<Vec<usize>> = CABELLO_9_CONTEXTS.iter().map(|c| c.to_vec()).collect();
    let square = vec![vec![1, 0], vec![0, 1], vec![1, 1], vec![1, -1]];
    vec![
        (cabello_rays, cabello_frames),
        (square.clone(), vec![vec![0, 1], vec![2, 3]]),
        (vec![vec![1, 0], vec![0, 1]], vec![vec![0, 1]]),
        (vec![vec![1, 0], vec![0, 1]], vec![vec![0, 1], vec![1, 0]]),
    ]
}

/// The rows `r^T rho r / r^T r` of a system, as coefficients of `rho_ij`, `i <= j`, in the
/// order the physics crate uses.
fn projector_rows(rays: &[Vec<i64>]) -> BasicMatrix<Rational> {
    let dimension = rays[0].len();
    mx::from_rows(
        rays.iter()
            .map(|r| {
                let norm: i64 = r.iter().map(|x| x * x).sum();
                (0..dimension)
                    .flat_map(|i| (i..dimension).map(move |j| (i, j)))
                    .map(|(i, j)| rq(if i == j { r[i] * r[i] } else { 2 * r[i] * r[j] }, norm))
                    .collect()
            })
            .collect(),
    )
    .unwrap()
}

#[test]
fn frame_polytope_ranks_agree_with_the_adapter_rank_of_the_same_matrices() {
    for (rays, frames) in systems() {
        let system = FrameSystem::new(rays.clone(), frames).unwrap();
        assert_eq!(
            system.incidence_rank().unwrap(),
            system.incidence().unwrap().rank().unwrap()
        );
        assert_eq!(
            system.projector_span_rank().unwrap(),
            projector_rows(&rays).rank().unwrap()
        );
    }
    // The values are not degenerate: the Cabello incidence has rank 9 and its projectors span
    // all ten symmetric directions, while one frame on the axes spans only the diagonal.
    let cabello = cabello_system();
    assert_eq!(
        (
            cabello.incidence_rank().unwrap(),
            cabello.projector_span_rank().unwrap()
        ),
        (9, 10)
    );
    let axes = FrameSystem::new(vec![vec![1, 0], vec![0, 1]], vec![vec![0, 1]]).unwrap();
    assert_eq!(
        (
            axes.incidence_rank().unwrap(),
            axes.projector_span_rank().unwrap()
        ),
        (1, 2)
    );
}

#[test]
fn frame_polytope_states_solve_the_same_system_as_the_adapter_solve() {
    let cabello = cabello_system();
    let rays: Vec<Vec<i64>> = CABELLO_18_VECTORS
        .iter()
        .map(|r| r.iter().map(|&x| i64::from(x)).collect())
        .collect();
    let rows = projector_rows(&rays);
    let coordinates: Vec<(usize, usize)> =
        (0..4).flat_map(|i| (i..4).map(move |j| (i, j))).collect();
    // A frame function that is not the maximally mixed one: the state of the first ray projector.
    let norm: i64 = rays[0].iter().map(|x| x * x).sum();
    let projector = mx::from_rows(
        rays[0]
            .iter()
            .map(|&a| rays[0].iter().map(|&b| rq(a * b, norm)).collect())
            .collect(),
    )
    .unwrap();
    for f in [
        vec![rq(1, 4); 18],
        cabello.frame_function_of(&projector).unwrap(),
    ] {
        let rho = cabello.state_of(&f).unwrap();
        let ImageMembership::InImage(solution) = solve_in_image(&rows, &f).unwrap() else {
            panic!("a frame function is in the image of the projector rows");
        };
        for (&(i, j), value) in coordinates.iter().zip(&solution.potential) {
            assert_eq!(
                (rho.get_ref(i, j).unwrap(), rho.get_ref(j, i).unwrap()),
                (value, value),
                "coordinate ({i}, {j})"
            );
        }
    }
    // Zero is in every linear image, but it is not a normalized frame function.
    let zero_not_normalized = vec![ri(0); 18];
    assert_eq!(
        cabello.state_of(&zero_not_normalized),
        Err(FramePolytopeError::NotAFrameFunction)
    );
    assert!(matches!(
        solve_in_image(&rows, &zero_not_normalized).unwrap(),
        ImageMembership::InImage(_)
    ));
    // A single-ray weight violates equality of the sums over the complete frames.
    // It therefore supplies an actual off-image control for both routes.
    let mut off_image = vec![ri(0); 18];
    off_image[0] = ri(1);
    assert_eq!(
        cabello.state_of(&off_image),
        Err(FramePolytopeError::NotAFrameFunction)
    );
    assert!(matches!(
        solve_in_image(&rows, &off_image).unwrap(),
        ImageMembership::NotInImage { .. }
    ));
}

/// The Cayley transform through the adapter: one solve per basis vector for the columns of
/// `(I + tau X)^-1`, then the product with `I - tau X`.
fn cayley_by_canonical_column_solves(
    x: &BasicMatrix<Rational>,
    tau: &Rational,
) -> Option<BasicMatrix<Rational>> {
    let n = x.rows();
    let eye = mx::identity(n).ok()?;
    let scaled = mx::scale(x, tau).ok()?;
    let a = mx::sub(&eye, &scaled).ok()?;
    let b = mx::add(&eye, &scaled).ok()?;
    let basis = mx::to_rows(&eye).ok()?;
    let columns = (0..n)
        .map(|i| match solve_in_image(&b, &basis[i]).ok()? {
            ImageMembership::InImage(solution) => Some(solution.potential),
            ImageMembership::NotInImage { .. } => None,
        })
        .collect::<Option<Vec<_>>>()?;
    mx::multiply(&a, &mx::transpose(&mx::from_rows(columns).ok()?).ok()?).ok()
}

#[test]
fn the_cayley_transform_and_its_isometry_check_agree_with_the_adapter_route() {
    let skew = |n: usize, scale: i64| {
        mx::from_fn(n, n, |i, j| {
            rq(
                (i as i64 + j as i64 + 1) * (j as i64 - i as i64).signum(),
                scale,
            )
        })
        .unwrap()
    };
    for (n, scale) in [(2usize, 3i64), (3, 5), (8, 17)] {
        let x = skew(n, scale);
        for tau in [rq(1, 3), rq(-5, 2), ri(7), ri(0)] {
            let by_physics = cayley_transform(&x, &tau).unwrap();
            assert_eq!(
                Some(by_physics.clone()),
                cayley_by_canonical_column_solves(&x, &tau),
                "n = {n}, tau = {tau}"
            );
            assert!(is_orthogonal(&by_physics));
            let by_adapter = mx::multiply(&mx::transpose(&by_physics).unwrap(), &by_physics)
                .unwrap()
                == mx::identity::<Rational>(n).unwrap();
            assert_eq!(is_orthogonal(&by_physics), by_adapter);
        }
    }
    // A matrix that is not an isometry is refused by both routes.
    let shear = mx::from_rows(vec![vec![ri(1), ri(1)], vec![ri(0), ri(1)]]).unwrap();
    assert!(!is_orthogonal(&shear));
    assert_ne!(
        mx::multiply(&mx::transpose(&shear).unwrap(), &shear).unwrap(),
        mx::identity::<Rational>(2).unwrap()
    );
}

#[test]
fn the_cabello_incidence_rank_and_the_interface_defect_agree_with_the_adapter() {
    let incidence = mx::from_rows(
        CABELLO_9_CONTEXTS
            .iter()
            .map(|context| {
                (0..18)
                    .map(|ray| ri(i64::from(context.contains(&ray))))
                    .collect()
            })
            .collect(),
    )
    .unwrap();
    assert_eq!(cabello().incidence_rank, incidence.rank().unwrap());
    // The defect of a symmetric 4 x 4 matrix along a normal is `max(0, -n^T M n)`.
    let half = rq(1, 2);
    let m = mx::from_rows(vec![
        vec![rq(-1, 2), ri(0), ri(0), ri(0)],
        vec![ri(0), half.clone(), rq(1, 4), rq(1, 4)],
        vec![ri(0), rq(1, 4), half.clone(), rq(1, 4)],
        vec![ri(0), rq(1, 4), rq(1, 4), half],
    ])
    .unwrap();
    for normal in [
        vec![ri(1), ri(0), ri(0), ri(0)],
        vec![ri(0), ri(1), ri(1), ri(1)],
        vec![ri(1), ri(1), ri(0), ri(0)],
    ] {
        let value = mx::dot(&normal, &mx::multiply_vector(&m, &normal).unwrap()).unwrap();
        let expected = if value < ri(0) { -value } else { ri(0) };
        assert_eq!(interface_defect(&m, &normal).unwrap(), expected);
    }
    assert_eq!(
        interface_defect(&m, &[ri(1), ri(0), ri(0), ri(0)]).unwrap(),
        rq(1, 2)
    );
}

#[test]
fn the_sorkin_evaluation_of_the_cancellation_certificate_agrees_with_the_program_receipt() {
    let receipt = verify_target3_sorkin_interference();
    let evaluation = evaluate_sorkin_i3_cancellation();
    assert_eq!(
        evaluation.i3_identically_zero,
        receipt.sorkin_i3_identically_zero
    );
    assert!(evaluation.i3_identically_zero);
    // The same triple has a non-vanishing second-order term, so the vanishing is not vacuous.
    assert!(receipt.non_zero_second_order_interference);
}
