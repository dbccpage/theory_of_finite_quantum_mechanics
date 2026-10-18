//! Integration tests for the Fermion Sign Problem (tfqm_fsp) crate
//! verifying CAR algebra, BQNF terminal routing, GIN posting lists,
//! exact rational Hubbard determinants, normal forms, and dual-face witnesses.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use std::collections::BTreeSet;
use tfqm_fsp::*;

#[test]
fn test_dual_face_witness_contract_and_refusals() {
    let w = witness();
    assert_eq!(w.signs, [1, -1, 1, 1, -1, -1]);
    assert_eq!(w.hop_product, -1);
    assert_eq!(w.parity_sum, 3);
    assert_eq!(w.parity_f2, 1);
    assert_eq!(w.gauges_checked, 64);
    assert_eq!(w.gauges_removing_holonomy, 0);
    assert_eq!(w.gauged_cycle_f2, 1);
    assert_eq!(w.site_cycle_rank, 0);
    assert_eq!(w.all_negative_product, 1);
    assert_eq!(w.k, 1);
    assert_eq!(w.weight_a, 1);
    assert_eq!(w.baseline_s, 1);
    assert_eq!(w.z_u, 0);
    assert_eq!(w.n_u, 2);
    assert_eq!(w.hat_o_num, 1);
    assert_eq!(w.hat_o_den, 1);
    assert_eq!(w.holonomy_removed, 0);
    assert_eq!(w.numerator_preserved, 0);
    assert_eq!(w.conjunction, 0);

    // Refusal gates
    assert!(refuse_removed_holonomy(-1).is_ok());
    assert!(refuse_removed_holonomy(1).is_err());
    assert!(refuse_foreign_fixture(912).is_err());
    assert!(refuse_foreign_fixture(36864).is_err());
    assert!(refuse_foreign_fixture(0).is_ok());
    assert!(refuse_foreign_fixture(2).is_ok());
}

#[test]
fn test_car_algebra_creation_annihilation_anticommutation() {
    // 4 sites vacuum state
    let vac = FockState::new(0, 0);
    assert_eq!(vac.total_particles(), 0);

    // Create fermions at site 0 and site 1 with spin Up
    let (s0, st0) = car_create(vac, 0, Spin::Up).unwrap();
    assert_eq!(s0, 1);
    assert_eq!(st0, FockState::new(1, 0));

    let (s1, st01) = car_create(st0, 1, Spin::Up).unwrap();
    assert_eq!(s1, -1); // site 0 was occupied, so sign = (-1)^1 = -1
    assert_eq!(st01, FockState::new(3, 0));

    // Reverse creation order: site 1 then site 0
    let (r1, st1) = car_create(vac, 1, Spin::Up).unwrap();
    assert_eq!(r1, 1);
    let (r0, st10) = car_create(st1, 0, Spin::Up).unwrap();
    assert_eq!(r0, 1);
    assert_eq!(st10, FockState::new(3, 0));

    // Anticommutation: c_1^\dagger c_0^\dagger |0> = - c_0^\dagger c_1^\dagger |0>
    assert_eq!(s0 * s1, -(r1 * r0));

    // Annihilation
    let (a0, st_after_a0) = car_annihilate(st01, 0, Spin::Up).unwrap();
    assert_eq!(a0, 1);
    assert_eq!(st_after_a0, FockState::new(2, 0)); // site 1 occupied

    // Cannot create where already occupied
    assert!(car_create(st_after_a0, 1, Spin::Up).is_none());
    // Cannot annihilate where empty
    assert!(car_annihilate(st_after_a0, 0, Spin::Up).is_none());
}

#[test]
fn test_discrete_fermionic_hamiltonian_and_euler_path_sum() {
    // 3-site triangle, 2 fermions (spin-up only)
    let lattice = FermionicLattice::triangle();
    let t = BigRational::one();
    let u = BigRational::zero();
    let mu = BigRational::zero();
    let ham = DiscreteFermionicHamiltonian::new(lattice, t, u, mu, 2, 0).unwrap();

    assert_eq!(ham.basis.len(), 3);
    assert_eq!(ham.matrix.len(), 3);

    let beta = BigRational::from(BigInt::from(1));
    let trotter_steps = 3;
    let receipt = ham.compute_partition_functions(&beta, trotter_steps).unwrap();
    assert!(receipt.z_fermionic > BigRational::zero());
    assert!(receipt.z_bosonic > BigRational::zero());
    assert!(receipt.average_sign <= BigRational::one());

    let paths = ham.generate_sample_paths(&beta, trotter_steps).unwrap();
    assert!(!paths.is_empty());
    let mut sum_signed = BigRational::zero();
    let mut sum_abs = BigRational::zero();
    for p in &paths {
        sum_signed = sum_signed + &p.signed_amplitude;
        sum_abs = sum_abs + &p.abs_weight;
    }
    assert_eq!(sum_signed, receipt.z_fermionic);
    assert_eq!(sum_abs, receipt.z_bosonic);
}

#[test]
fn test_bqnf_terminal_routing_5_fold_classification() {
    // Exact mapping to BqnfSignPacket.lean
    // 1. ClosureFailure
    let cf = SignPacketMetrics::new(false, false, BigRational::zero(), BigRational::zero(), false);
    assert_eq!(route_packet(&cf), TerminalRoute::ClosureFailure);

    // 2. SplitBrainRefusal
    let sbr = SignPacketMetrics::new(true, true, BigRational::zero(), BigRational::zero(), false);
    assert_eq!(route_packet(&sbr), TerminalRoute::SplitBrainRefusal);

    // 3. OpenSignObstruction
    let oso = SignPacketMetrics::new(true, false, BigRational::one(), BigRational::zero(), false);
    assert_eq!(route_packet(&oso), TerminalRoute::OpenSignObstruction);

    // 4. ExactRepair (zero residual mass)
    let er1 = SignPacketMetrics::new(true, false, BigRational::zero(), BigRational::zero(), false);
    assert_eq!(route_packet(&er1), TerminalRoute::ExactRepair);

    // 5. ExactRepair (involution witness restores exact repair)
    let er2 = SignPacketMetrics::new(true, false, BigRational::zero(), BigRational::one(), true);
    assert_eq!(route_packet(&er2), TerminalRoute::ExactRepair);

    // 6. ClosedResidual (nonzero residual mass, closed, no involution)
    let cr = SignPacketMetrics::new(true, false, BigRational::zero(), BigRational::one(), false);
    assert_eq!(route_packet(&cr), TerminalRoute::ClosedResidual);
}

#[test]
fn test_gin_inverted_index_and_cancellation_audit() {
    let mut gin = GinIndex::new();

    // 4-site bipartite lattice configurations
    let mut occ1 = BTreeSet::new();
    occ1.insert(1);
    occ1.insert(2);
    gin.index_configuration(1, "Bipartite", occ1, 4, BigRational::from(BigInt::from(10)), 1, 1);

    let mut occ2 = BTreeSet::new();
    occ2.insert(2);
    occ2.insert(3);
    gin.index_configuration(2, "Bipartite", occ2, 4, BigRational::from(BigInt::from(10)), -1, 1);

    // Inverted posting list lookup: mode 2 is in both 1 and 2
    let mut req = BTreeSet::new();
    req.insert(2);
    let candidates = gin.query_by_modes(&req, &BTreeSet::new());
    assert_eq!(candidates.len(), 2);
    assert!(candidates.contains(&1) && candidates.contains(&2));

    // Involution partner search: flip modes {1, 3} on cfg 1 -> transforms {1, 2} into {2, 3} (cfg 2)
    let mut flip = BTreeSet::new();
    flip.insert(1);
    flip.insert(3);
    let partner = gin.find_involution_partner(1, &flip, 4);
    assert_eq!(partner, Some(2));

    // Involution cancellation audit
    let receipt = gin.audit_involution_cancellations("Bipartite", &[(1, 2)]);
    assert!(receipt.all_exact_cancellations);
    assert_eq!(receipt.max_weight_defect, BigRational::zero());
    assert_eq!(receipt.total_uncancelled_mass, BigRational::zero());
    assert_eq!(receipt.terminal_route, "ExactRepair");
}

#[test]
fn test_kitaev_chain_majorana_zero_modes() {
    let l = 6;
    let receipt = audit_kitaev_chain_majorana(l).unwrap();
    assert_eq!(receipt.chain_length_l, 6);
    assert_eq!(receipt.total_modes_audited, 12);
    assert_eq!(receipt.unpaired_zero_modes, vec![1, 12]);
    assert_eq!(receipt.bulk_bonded_modes.len(), 10);
    assert!(receipt.is_boundary_isolated);
    assert_eq!(receipt.mzm_status, "MZM_TOPOLOGICALLY_PROTECTED");

    // Boundary zero modes are not in bulk
    for &edge in &receipt.unpaired_zero_modes {
        assert!(!receipt.bulk_bonded_modes.contains(&edge));
    }
}

#[test]
fn test_exact_rational_hubbard_determinants_and_attractive_symmetry() {
    // 4-site square plaquette
    let bonds = vec![(0, 1), (1, 2), (2, 3), (3, 0)];
    let r = BigRational::new(BigInt::from(3), BigInt::from(2));
    let hs = BigRational::from(BigInt::from(2));
    let fugacity = BigRational::one();
    let field_masks = vec![0, 3, 5, 10, 12, 15];

    // Attractive Hubbard: square-root symmetry det_up = det_down ensures all weights >= 0
    let summary = evaluate_hubbard_determinants(
        4,
        &bonds,
        1,
        &r,
        &hs,
        &fugacity,
        true, // Attractive
        &field_masks,
    )
    .unwrap();

    assert_eq!(summary.negative_fields_count, 0);
    assert!(summary.attractive_square_root_protected);
    assert_eq!(summary.average_sign, BigRational::one());
    assert!(summary.total_determinant_sum > BigRational::zero());
}

#[test]
fn test_normal_forms_rref_quotient_and_graph_switching() {
    // 1. RREF
    let m = vec![
        vec![BigRational::from(BigInt::from(2)), BigRational::from(BigInt::from(4))],
        vec![BigRational::from(BigInt::from(1)), BigRational::from(BigInt::from(3))],
    ];
    let res = rref_with_witness(&m, 2).unwrap();
    assert_eq!(res.rank, 2);
    assert_eq!(res.pivots, vec![0, 1]);

    // 2. Quotient Normal Form modulo im(d0)
    let d0 = vec![
        vec![BigRational::one(), BigRational::zero()],
        vec![BigRational::one(), BigRational::one()],
        vec![BigRational::zero(), BigRational::one()],
    ];
    let c1 = vec![
        BigRational::from(BigInt::from(3)),
        BigRational::from(BigInt::from(7)),
        BigRational::from(BigInt::from(4)),
    ];
    let qnf = normalize_cochain(&d0, &c1).unwrap();
    // Verification: c1 - N(c1) = d0 * gauge
    for i in 0..3 {
        let mut d0_gauge_i = BigRational::zero();
        for j in 0..2 {
            d0_gauge_i = d0_gauge_i + &d0[i][j] * &qnf.gauge[j];
        }
        let diff = &c1[i] - &qnf.representative[i];
        assert_eq!(diff, d0_gauge_i, "c1 - N(c1) must equal d0 * gauge");
    }

    // 3. Graph Switching Normal Form on 4-cycle
    let edges = vec![(0, 1), (1, 2), (2, 3), (3, 0)];
    let parities = vec![0, 0, 0, 1]; // odd total cycle flux
    let swnf = normalize_sign_cochain(4, &edges, &parities).unwrap();
    assert_eq!(swnf.forest_edges.len(), 3);
    assert_eq!(swnf.obstruction_cycles.len(), 1);
    assert_eq!(swnf.obstruction_cycles[0], vec![0, 1, 2, 3]);
}

#[test]
fn test_root_barrel_integration_and_inventory() {
    // Verify that crate root exports fsp and inventory mass holds
    use theory_of_finite_qm::fsp;
    assert!(fsp::fsp_crate_invariants_hold().is_ok());

    let w = fsp::witness();
    assert_eq!(w.hop_product, -1);
    assert_eq!(w.z_u, 0);
    assert_eq!(w.n_u, 2);

    assert!(theory_of_finite_qm::crate_root_inventory_holds().is_ok());
}
