//! Program buildability declaration tests, retained from the mixed superposition suite.
use finite_qm_native::campaigns::buildability_criterion::{ArchitectureDeclaration, ResidualRace};
use omega_number_theory::rational::{ri, rq};
use omega_quantum_physics::exact_hermitian::{gi, gq};
use omega_quantum_physics::u1_graph_connection::U1Connection;
use omega_solvers::data_cochain_packet::FiniteCochainPacket;

fn packet(vertices: &[&str], edges: &[(&str, &str)]) -> FiniteCochainPacket {
    FiniteCochainPacket::with_unit_weights(
        FiniteCochainPacket::build_complex(vertices, edges, &[]).unwrap(),
    )
    .unwrap()
}

fn triangle() -> FiniteCochainPacket {
    packet(&["a", "b", "c"], &[("a", "b"), ("b", "c"), ("c", "a")])
}

fn path_tree() -> FiniteCochainPacket {
    packet(&["a", "b", "c", "d"], &[("a", "b"), ("b", "c"), ("c", "d")])
}

// ---------------------------------------------------------------------------
// QM-061-C12..C14: the declared buildability set S.
// ---------------------------------------------------------------------------

fn resource(packet: &FiniteCochainPacket, present: bool) -> U1Connection {
    if present {
        U1Connection::new(packet, vec![gi(0, 1), gi(1, 0), gi(1, 0)]).unwrap()
    } else {
        U1Connection::trivial(packet)
    }
}

fn race(lambda: i64, mu: i64, eps: i64) -> ResidualRace {
    ResidualRace::new(ri(lambda), ri(mu), ri(eps))
}

#[test]
fn the_residual_stays_bounded_exactly_when_the_step_is_not_positive() {
    let rho0 = rq(7, 2);
    let repairing = race(10, 15, 0);
    assert_eq!(repairing.step(), ri(-5));
    let mut iterated = rho0.clone();
    for n in 0..=20u64 {
        assert_eq!(repairing.residual_after(&rho0, n), iterated);
        iterated += repairing.step();
    }
    for n in 0..=100u64 {
        assert!(repairing.residual_after(&rho0, n) <= rho0);
    }
    assert_eq!(repairing.first_excess_cycle(), None);

    let overwhelmed = race(20, 10, 0);
    assert_eq!(overwhelmed.residual_after(&rho0, 1), &rho0 + ri(10));
    assert_eq!(overwhelmed.first_excess_cycle(), Some(1));
    let balanced = race(10, 10, 0);
    assert_eq!(balanced.residual_after(&rho0, 1000), rho0);
    assert_eq!(balanced.first_excess_cycle(), None);
    let barely = ResidualRace::new(ri(10) + rq(1, 1_000_000_000_000), ri(10), ri(0));
    assert_eq!(barely.first_excess_cycle(), Some(1));
    assert_eq!(race(12, 10, 3).step(), ri(-1));
}

#[test]
fn set_s_over_all_sixteen_assignments_is_the_conjunction() {
    let tri = triangle();
    for mask in 0..16u32 {
        let wanted = [mask & 1 == 1, mask & 2 == 2, mask & 4 == 4, mask & 8 == 8];
        let declaration = ArchitectureDeclaration::new(
            if wanted[0] {
                race(5, 10, 0)
            } else {
                race(25, 10, 0)
            },
            if wanted[1] { rq(1, 100) } else { ri(0) },
            wanted[2],
            &tri,
            &resource(&tri, wanted[3]),
        )
        .unwrap();
        assert_eq!(declaration.conditions(), wanted);
        assert_eq!(declaration.satisfies_set_s(), mask == 15);
    }
}

#[test]
fn each_member_of_s_is_necessary_and_s_is_satisfiable() {
    let tri = triangle();
    let tree = path_tree();
    let floor = rq(1, 1000);
    let rotation = U1Connection::new(&tri, vec![gq(3, 5, 4, 5), gi(1, 0), gi(1, 0)]).unwrap();
    let satisfiable =
        ArchitectureDeclaration::new(race(10, 15, 0), floor.clone(), true, &tri, &rotation)
            .unwrap();
    assert_eq!(satisfiable.conditions(), [true; 4]);
    assert!(satisfiable.satisfies_set_s());

    let drop_s1 =
        ArchitectureDeclaration::new(race(20, 10, 0), floor.clone(), true, &tri, &rotation)
            .unwrap();
    let drop_s2 =
        ArchitectureDeclaration::new(race(10, 15, 0), ri(0), true, &tri, &rotation).unwrap();
    let drop_s3 =
        ArchitectureDeclaration::new(race(10, 15, 0), floor.clone(), false, &tri, &rotation)
            .unwrap();
    // Any connection on a tree is gauge trivial, so a tree carrier has no S4 resource.
    let on_tree = U1Connection::new(&tree, vec![gi(0, 1), gq(3, 5, -4, 5), gi(-1, 0)]).unwrap();
    let drop_s4 =
        ArchitectureDeclaration::new(race(10, 15, 0), floor, true, &tree, &on_tree).unwrap();
    for (declaration, missing) in [(drop_s1, 0), (drop_s2, 1), (drop_s3, 2), (drop_s4, 3)] {
        let conditions = declaration.conditions();
        for (index, condition) in conditions.iter().enumerate() {
            assert_eq!(*condition, index != missing);
        }
        assert!(!declaration.satisfies_set_s());
    }
    let negative_floor =
        ArchitectureDeclaration::new(race(5, 10, 0), ri(-1), true, &tri, &rotation).unwrap();
    assert!(!negative_floor.conditions()[1]);
    // A pure-gauge connection on the triangle carries no resource either.
    let pure_gauge = U1Connection::new(&tri, vec![gi(0, 1), gi(0, 1), gi(-1, 0)]).unwrap();
    let flat =
        ArchitectureDeclaration::new(race(5, 10, 0), rq(1, 2), true, &tri, &pure_gauge).unwrap();
    assert_eq!(flat.conditions(), [true, true, true, false]);
}
