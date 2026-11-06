// Exercise proposed patches in scratch; does not modify the omega_mub dependency.
pub use omega_mub::omega_native;
#[path = "../../patched/omega_engine/crates_rs/omega_mub/src/omega_native/l1_discrete_solver/network_simplex.rs"]
mod patched_network;
#[path = "../../patched/omega_engine/crates_rs/omega_mub/src/omega_native/mub6_smale_sentry.rs"]
mod patched_smale;

fn main() {
    use patched_smale::*;
    let system = SquarePolynomialSystem::new(vec![QuadraticComponent::new(
        rat(-1, 1),
        vec![rat(0, 1)],
        RationalMatrix::from_rows(vec![vec![rat(2, 1)]]),
    )]);
    let box_x = RationalIntervalBox::new(vec![RationalInterval::new(rat(9, 10), rat(11, 10))]);
    assert!(matches!(
        krawczyk_contractor(&system, &box_x, Some(&[rat(2, 1)])),
        Err(LuError::CenterOutsideBox)
    ));
    assert!(
        krawczyk_contractor(&system, &box_x, None)
            .unwrap()
            .is_strictly_contracted
    );
    let empty = SmaleSentry::scan_bisection_leaves(&[]);
    assert!(!empty.all_positive);
    assert_eq!(empty.min_margin, rat(0, 1));
    use patched_network::{Arc, NetworkSimplex, NetworkSimplexError};
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
    assert!(matches!(
        solver.solve(),
        Err(NetworkSimplexError::InvalidCarrier { .. })
    ));
    let overflow = NetworkSimplex::new(3, vec![], vec![i128::MAX, 1, i128::MIN]);
    assert_eq!(
        overflow.check_balanced_demand(),
        Err(NetworkSimplexError::ArithmeticOverflow)
    );
    println!("PROPOSED_RUST_GUARDS_PASS: outside center rejected; valid midpoint contracts; empty scan rejected; unsupported capacity rejected; checked demand overflow returned");
}
