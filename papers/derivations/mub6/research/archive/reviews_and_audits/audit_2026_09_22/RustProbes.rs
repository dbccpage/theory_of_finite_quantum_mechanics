use omega_mub::omega_native::l1_discrete_solver::network_simplex::{Arc, NetworkSimplex};
use omega_mub::omega_native::mub6_smale_sentry::{
    krawczyk_contractor, rat, QuadraticComponent, RationalInterval, RationalIntervalBox,
    RationalMatrix, SquarePolynomialSystem,
};

fn main() {
    let system = SquarePolynomialSystem::new(vec![QuadraticComponent::new(
        rat(-1, 1),
        vec![rat(0, 1)],
        RationalMatrix::from_rows(vec![vec![rat(2, 1)]]),
    )]);
    let box_x = RationalIntervalBox::new(vec![RationalInterval::new(rat(9, 10), rat(11, 10))]);
    let outside_center = vec![rat(2, 1)];
    let result = krawczyk_contractor(&system, &box_x, Some(&outside_center)).unwrap();
    let exact_root = vec![rat(1, 1)];
    assert!(box_x.contains_point(&exact_root));
    assert_eq!(system.eval(&exact_root), vec![rat(0, 1)]);
    assert!(result.is_disjoint);
    assert_eq!(result.krawczyk_box.intervals[0].lo, rat(129, 200));
    assert_eq!(result.krawczyk_box.intervals[0].hi, rat(169, 200));
    println!("KRAWCZYK_FALSE_EXCLUSION: exact root 1 in [9/10,11/10]; x0=2; K=[129/200,169/200]; is_disjoint=true");

    let arc = Arc {
        tail: 0,
        head: 1,
        cost: 1,
        lower: 0,
        upper: Some(0),
        original_edge: None,
        orientation_sign: 1,
    };
    let mut solver = NetworkSimplex::new(2, vec![arc], vec![-1, 1]);
    let bounded = solver.solve().unwrap();
    assert_eq!(bounded.flow[0], 1);
    println!("UPPER_BOUND_IGNORED: capacity=0, returned flow=1");

    let overflow = std::panic::catch_unwind(|| {
        let solver = NetworkSimplex::new(3, vec![], vec![i128::MAX, 1, i128::MIN]);
        solver.check_balanced_demand()
    });
    assert!(overflow.is_err());
    println!("DEMAND_SUM_OVERFLOW_PANIC: balanced mathematical sum, intermediate i128 overflow");

    let empty_scan =
        omega_mub::omega_native::mub6_smale_sentry::SmaleSentry::scan_bisection_leaves(&[]);
    assert!(empty_scan.all_positive);
    assert_eq!(empty_scan.scanned_count, 0);
    println!(
        "EMPTY_SCAN_PASSES: all_positive=true, scanned_count=0, min_margin={}",
        empty_scan.min_margin
    );
}
