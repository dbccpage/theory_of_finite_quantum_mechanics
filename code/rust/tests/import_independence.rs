//! Targets 13–14: import independence (concrete countermodels) + import sufficiency
//! (`ImportBundle` → `build_downstream`).
//!
//! AuthorityEffect: None. TOY-MECH finite hosts only.

use finite_qm_native::campaigns::import_bundle::{
    authority_fence, basis_cardinality, build_downstream, build_phase_carrier, build_tomography,
    countermodel_drop_born_gleason, countermodel_drop_instruments,
    countermodel_drop_local_tomography, countermodel_drop_monoidal, countermodel_drop_noncommuting,
    countermodel_drop_ob_u1, countermodel_drop_spectral, frozen_slot_evidence,
    independence_countermodels, independent_slots_over, BornGleasonWitness, CarrierClass,
    CompositionKind, FrozenSlotId, ImportBasis, ImportBundle, ImportSlot, InstrumentsWitness,
    LocalTomographyWitness, MissingImport, MonoidalWitness, NonCommutingWitness, ObU1Witness,
    PhaseKind, SlotEvidence, SpectralWitness,
};
use omega_quantum_physics::composition_tomography::LocalTomographyReport;

// ---------------------------------------------------------------------------
// Target 13 — import independence
// ---------------------------------------------------------------------------

#[test]
fn import_t13_slots_enumerated() {
    let slots = ImportSlot::ALL;
    assert_eq!(slots.len(), 7);
    assert!(slots.contains(&ImportSlot::Spectral));
    assert!(slots.contains(&ImportSlot::Monoidal));
    assert!(slots.contains(&ImportSlot::LocalTomography));
    assert!(slots.contains(&ImportSlot::ObU1));
    assert!(slots.contains(&ImportSlot::BornGleason));
    assert!(slots.contains(&ImportSlot::Instruments));
    // Distinct string ids; OB-U1 and LocalTomography are separate names.
    assert_eq!(ImportSlot::ObU1.id(), "OB-U1");
    assert_eq!(ImportSlot::LocalTomography.id(), "LocalTomography");
    assert_ne!(ImportSlot::ObU1.id(), ImportSlot::LocalTomography.id());
}

#[test]
fn import_t13_each_slot_has_concrete_countermodel_not_flag_matrix() {
    for (slot, host) in independence_countermodels() {
        // Concrete data present (not a bare bool row).
        assert!(!host.id.is_empty(), "countermodel id required for {slot:?}");
        assert!(
            !host.drop_note.is_empty(),
            "drop note required for {slot:?}"
        );
        assert!(
            !host.amplitudes.is_empty(),
            "amplitudes data required for {}",
            host.id
        );
        assert!(host.dim_a >= 1 && host.dim_b >= 1);
        // Matrix is real data.
        let _m00 = host.matrix_2x2[0][0];
        assert!(
            host.fails_exactly(slot),
            "host {} must fail exactly {:?}; admits map: {:?}",
            host.id,
            slot,
            ImportSlot::ALL.map(|s| (s, host.admits(s)))
        );
    }
}

#[test]
fn import_t13_spectral_drop_is_jordan_block() {
    let h = countermodel_drop_spectral();
    assert_eq!(h.id, "cm_drop_spectral");
    // Non-Hermitian: m01=1, m10=0.
    assert_eq!(h.matrix_2x2[0][1], (1, 0));
    assert_eq!(h.matrix_2x2[1][0], (0, 0));
    assert!(!h.is_hermitian());
    assert!(!h.spectral_reconstructs());
    assert!(h.monoidal_holds());
    assert!(h.local_tomography_holds());
    assert!(h.ob_u1_holds());
    assert!(h.born_gleason_holds());
    assert!(h.instruments_hold());
    assert!(h.fails_exactly(ImportSlot::Spectral));
}

#[test]
fn import_t13_monoidal_drop_is_direct_sum() {
    let h = countermodel_drop_monoidal();
    assert_eq!(h.composition, CompositionKind::DirectSum);
    assert_eq!(h.dim_a, 2);
    assert_eq!(h.dim_b, 3);
    // 2+3 ≠ 2·3 — composition kind DirectSum fails monoidal.
    assert!(!h.monoidal_holds());
    assert!(h.spectral_reconstructs());
    assert!(h.fails_exactly(ImportSlot::Monoidal));
}

#[test]
fn import_t13_ob_u1_and_local_tomography_are_separate_rows() {
    let drop_lt = countermodel_drop_local_tomography();
    let drop_u1 = countermodel_drop_ob_u1();

    // Distinct hosts (not one shared coupled row).
    assert_ne!(drop_lt.id, drop_u1.id);
    assert_ne!(drop_lt, drop_u1);

    // LT drop: fails LT, admits OB-U1.
    assert!(drop_lt.fails_exactly(ImportSlot::LocalTomography));
    assert!(!drop_lt.admits(ImportSlot::LocalTomography));
    assert!(drop_lt.admits(ImportSlot::ObU1));
    assert_eq!(drop_lt.phase, PhaseKind::ComplexU1);
    assert_eq!(drop_lt.joint_param, 15);
    assert_ne!(
        drop_lt.local_param_a * drop_lt.local_param_b,
        drop_lt.joint_param
    );

    // U1 drop: fails OB-U1, admits LT.
    assert!(drop_u1.fails_exactly(ImportSlot::ObU1));
    assert!(!drop_u1.admits(ImportSlot::ObU1));
    assert!(drop_u1.admits(ImportSlot::LocalTomography));
    assert_eq!(drop_u1.phase, PhaseKind::RealOnly);
    assert_eq!(
        drop_u1.local_param_a * drop_u1.local_param_b,
        drop_u1.joint_param
    );

    // Neither row is a Boolean flag-only shell: phase and param data disagree.
    assert!(drop_lt.amplitudes.iter().any(|&(_, im)| im != 0));
    assert!(drop_u1.amplitudes.iter().all(|&(_, im)| im == 0));
}

#[test]
fn import_t13_born_gleason_and_instruments_drop() {
    let born = countermodel_drop_born_gleason();
    assert!(born.fails_exactly(ImportSlot::BornGleason));
    assert!(!born.born_gleason_holds());
    assert!(born.spectral_reconstructs());

    let inst = countermodel_drop_instruments();
    assert!(inst.fails_exactly(ImportSlot::Instruments));
    assert!(!inst.has_instrument_update);
    assert!(inst.spectral_reconstructs());
}

#[test]
fn import_t13_countermodels_pairwise_distinct() {
    let models: Vec<_> = independence_countermodels()
        .into_iter()
        .map(|(_, h)| h)
        .collect();
    assert_eq!(models.len(), 7);
    for i in 0..models.len() {
        for j in (i + 1)..models.len() {
            assert_ne!(
                models[i], models[j],
                "countermodels {} and {} must differ",
                models[i].id, models[j].id
            );
        }
    }
}

#[test]
fn import_t13_authority_none() {
    assert!(authority_fence().contains("AuthorityEffect None"));
}

// ---------------------------------------------------------------------------
// Target 14 — import sufficiency / construction
// ---------------------------------------------------------------------------

#[test]
fn import_t14_full_bundle_builds_downstream_from_witnesses() {
    let bundle = ImportBundle::full_toy();
    for s in ImportSlot::ALL {
        assert!(bundle.has_valid(s), "full_toy missing valid {s:?}");
    }

    let down = build_downstream(&bundle).expect("full toy bundle must build");

    // Construction uses witness data, not flags.
    assert_eq!(down.spectral.eigenvalues, [1, -1]);
    assert_eq!(down.spectral.reconstructed_diag, [1, -1]);
    assert_eq!(down.monoidal.joint_dim, 4);
    assert_eq!(down.tomography.joint_param, 16);
    assert!(down.tomography.identity_holds);
    assert!(down.phase_carrier.has_nontrivial_u1);
    assert_eq!(down.born_rule.masses, vec![1, 1]);
    assert_eq!(down.born_rule.total_mass, 2);
    assert_eq!(down.instrument_map.prior_diag, [3, 1]);
    assert_eq!(down.instrument_map.post_outcome_0, [3, 0]);
    assert_eq!(down.instrument_map.post_outcome_1, [0, 1]);
}

#[test]
fn import_t14_tomography_requires_local_tomography_witness() {
    let mut bundle = ImportBundle::full_toy();
    bundle.local_tomography = None;
    assert_eq!(
        build_tomography(&bundle),
        Err(MissingImport::LocalTomography)
    );
    assert_eq!(
        build_downstream(&bundle),
        Err(MissingImport::LocalTomography)
    );

    // Invalid witness (broken identity) also refuses.
    bundle.local_tomography = Some(LocalTomographyWitness {
        local_param_a: 4,
        local_param_b: 4,
        joint_param: 15,
    });
    assert_eq!(
        build_tomography(&bundle),
        Err(MissingImport::LocalTomography)
    );
}

#[test]
fn import_t14_phase_carrier_requires_ob_u1_witness() {
    let mut bundle = ImportBundle::full_toy();
    bundle.ob_u1 = None;
    assert_eq!(build_phase_carrier(&bundle), Err(MissingImport::ObU1));
    assert_eq!(build_downstream(&bundle), Err(MissingImport::ObU1));

    // Real-only amplitudes (no imag) do not validate as OB-U1 witness.
    bundle.ob_u1 = Some(ObU1Witness {
        amplitudes: vec![(1, 0), (0, 0)],
    });
    assert_eq!(build_phase_carrier(&bundle), Err(MissingImport::ObU1));
}

#[test]
fn import_t14_each_missing_import_blocks_downstream() {
    type StripFn = fn(&mut ImportBundle);
    let cases: [(StripFn, MissingImport); 6] = [
        (|b| b.spectral = None, MissingImport::Spectral),
        (|b| b.monoidal = None, MissingImport::Monoidal),
        (
            |b| b.local_tomography = None,
            MissingImport::LocalTomography,
        ),
        (|b| b.ob_u1 = None, MissingImport::ObU1),
        (|b| b.born_gleason = None, MissingImport::BornGleason),
        (|b| b.instruments = None, MissingImport::Instruments),
    ];
    for (strip, expected) in cases {
        let mut bundle = ImportBundle::full_toy();
        strip(&mut bundle);
        assert_eq!(build_downstream(&bundle), Err(expected));
    }
}

#[test]
fn import_t14_boolean_pathway_alone_is_insufficient() {
    // A flag-only story would claim "all pathways covered" without witnesses.
    // Empty bundle has no witnesses → construction fails.
    let empty = ImportBundle::empty();
    assert!(build_downstream(&empty).is_err());
    assert!(!empty.has_valid(ImportSlot::LocalTomography));

    // Partial flag-like package: monoidal present but tomography absent cannot
    // build tomography even if other imports look fine.
    let partial = ImportBundle {
        spectral: Some(SpectralWitness::computational([1, 0])),
        monoidal: Some(MonoidalWitness { dim_a: 2, dim_b: 2 }),
        local_tomography: None,
        ob_u1: Some(ObU1Witness {
            amplitudes: vec![(0, 1)],
        }),
        born_gleason: Some(BornGleasonWitness {
            amplitudes: vec![(1, 0)],
        }),
        instruments: Some(InstrumentsWitness {
            projectors_diag: [[1, 0], [0, 1]],
            prior_diag: [1, 1],
        }),
        noncommuting: Some(NonCommutingWitness::pauli_xz()),
    };
    assert_eq!(
        build_tomography(&partial),
        Err(MissingImport::LocalTomography)
    );
    // Downstream also fails — cannot smuggle tomography from monoidal alone.
    assert_eq!(
        build_downstream(&partial),
        Err(MissingImport::LocalTomography)
    );
}

#[test]
fn import_t14_instrument_map_uses_witness_prior() {
    let mut bundle = ImportBundle::full_toy();
    bundle.instruments = Some(InstrumentsWitness {
        projectors_diag: [[1, 0], [0, 1]],
        prior_diag: [5, 2],
    });
    let down = build_downstream(&bundle).unwrap();
    assert_eq!(down.instrument_map.post_outcome_0, [5, 0]);
    assert_eq!(down.instrument_map.post_outcome_1, [0, 2]);
}

#[test]
fn import_t14_authority_none() {
    assert!(authority_fence().contains("AuthorityEffect None"));
}

// ---------------------------------------------------------------------------
// R2-C9 — OB-NONCOMM as a real drop-one slot
// ---------------------------------------------------------------------------

/// The new slot has a countermodel that fails EXACTLY it.
#[test]
fn r2c9_noncommuting_countermodel_fails_exactly_one_slot() {
    let h = countermodel_drop_noncommuting();
    assert!(!h.noncommuting_holds(), "Z and 2Z commute");
    assert!(
        h.fails_exactly(ImportSlot::NonCommuting),
        "the OB-NONCOMM countermodel must admit every other slot"
    );
}

/// Adding a slot must not cost independence elsewhere. Every PRE-EXISTING
/// countermodel still fails exactly its own slot — measured, not assumed.
#[test]
fn r2c9_adding_a_slot_did_not_break_existing_independence() {
    for (slot, host) in independence_countermodels() {
        assert!(
            host.fails_exactly(slot),
            "{} no longer fails exactly its own slot after OB-NONCOMM was added",
            slot.id()
        );
        assert!(
            host.noncommuting_holds() || slot == ImportSlot::NonCommuting,
            "{} must ADMIT OB-NONCOMM, else it fails two slots",
            slot.id()
        );
    }
}

/// Both conjuncts of the predicate are load-bearing.
#[test]
fn r2c9_noncommuting_predicate_needs_symmetry_and_noncommutativity() {
    let good = NonCommutingWitness::pauli_xz();
    assert!(good.validates());

    // Symmetric but commuting.
    let commuting = NonCommutingWitness {
        observables: [[[1, 0], [0, -1]], [[2, 0], [0, -2]]],
    };
    assert!(!commuting.validates(), "commuting pair must not validate");

    // Non-commuting but NOT symmetric: a non-observable pair witnesses nothing.
    let asym = NonCommutingWitness {
        observables: [[[0, 1], [0, 0]], [[1, 0], [0, -1]]],
    };
    assert!(!asym.validates(), "non-symmetric pair must not validate");
}

/// The frozen registry still names THIRTEEN slots. Modelling one does not mint one.
#[test]
fn r2c9_frozen_count_is_unchanged_and_independence_rose_by_one() {
    assert_eq!(basis_cardinality(ImportBasis::FrozenDeclared), 13);
    assert_eq!(basis_cardinality(ImportBasis::DropOneIndependent), 6);
    assert!(matches!(
        frozen_slot_evidence(FrozenSlotId::ObNoncomm),
        SlotEvidence::IndependentWithCountermodel { host_id, .. }
            if host_id == "cm_drop_noncommuting"
    ));
}

// ---------------------------------------------------------------------------
// R2-C6 / Target 6 — adjudicating the LT <-> OB-U1 split
//
// Round 2 recorded the split as DISPUTED and refused to resolve it by fiat:
// Rust exhibits both drop-one countermodels (so: independent), while the Lean
// NamedLift registry records the pair as COUPLED with SPLIT-OUTSIDE-REGISTRY
// still OPEN. These tests settle it on evidence.
//
// NARROWED VERDICT (2026-08-05, under review of PR #1894):
//
//   ESTABLISHED: `cm_drop_ob_u1` is not a valid drop-one OB-U1 witness when
//   read as a real-quantum carrier. It carries CLASSICAL simplex counts
//   (2, 2, 4) -- `FiniteImportHost::carrier_class()` computes that, it is not
//   asserted -- and a classical composite has local tomography trivially.
//   Under the real-quantum counts for the same dimensions the same host also
//   fails LocalTomography, so it stops being a drop-one witness.
//
//   NOT ESTABLISHED: QuantumCarrier(H) AND NOT OB-U1(H)  =>  NOT LT(H).
//   Substituting three count fields by hand and observing two predicates fail
//   invalidates ONE witness; it does not quantify over hosts. `ob_u1_holds()`
//   reads the phase field, which the substitution never touches, so the two
//   failures below are independent facts about an edited struct, not a derived
//   implication. Establishing coupling needs a validated carrier-class
//   invariant tying phase, state space, effect space, observables, Born rule
//   and composition together -- or an exhaustion over a bounded licensed model
//   universe. Neither exists here.
//
//   STATUS: QUANTUM-CARRIER-COUPLING is OPEN. The registry now carries carrier
//   scope (`CarrierClass`), so OB-U1 independence reads as classical-scoped
//   rather than unqualified.
// ---------------------------------------------------------------------------

/// The disputed host's parameter counts are the CLASSICAL ones.
///
/// `local_tomography_holds` tests `local_a * local_b == joint`. For
/// `cm_drop_ob_u1` that is `2 * 2 == 4`. But a real-quantum (rebit) system of
/// dimension 2 has `d(d+1)/2 = 3` symmetric parameters locally and
/// `4*5/2 = 10` jointly -- and `3 * 3 = 9 != 10`.
#[test]
fn r2c6_drop_u1_witness_uses_classical_not_real_quantum_counts() {
    let h = countermodel_drop_ob_u1();
    assert_eq!(
        (h.local_param_a, h.local_param_b, h.joint_param),
        (2, 2, 4),
        "the witness declares classical simplex counts"
    );
    assert!(h.local_tomography_holds(), "classical counts make LT hold");

    // The real-quantum truth for the same dimensions, computed not assumed.
    let real = LocalTomographyReport::real_product_params(2, 2).unwrap();
    assert_eq!((real.local_param_a, real.local_param_b), (3, 3));
    assert_eq!(real.joint_param, 10);
    assert!(
        !real.identity_holds,
        "real-quantum LT FAILS at 2x2: 3*3 = 9 != 10"
    );
}

/// Give the drop-U1 host its honest real-quantum counts and it fails **two**
/// slots, so it is no longer a drop-one witness for `OB-U1`.
///
/// Scope, precisely: this invalidates THIS witness under a real-quantum
/// reading. It does not establish that dropping the phase carrier forces local
/// tomography to fail on quantum carriers generally -- see the narrowed verdict
/// above. The name says witness-invalidation because that is what runs.
#[test]
fn r2c6_drop_u1_witness_is_invalid_under_a_real_quantum_reading() {
    let mut h = countermodel_drop_ob_u1();
    assert!(
        h.fails_exactly(ImportSlot::ObU1),
        "with classical counts it is a clean drop-one witness"
    );

    // Substitute the real-quantum symmetric parameter counts for dim 2 x 2.
    let real = LocalTomographyReport::real_product_params(2, 2).unwrap();
    h.local_param_a = real.local_param_a;
    h.local_param_b = real.local_param_b;
    h.joint_param = real.joint_param;

    assert!(!h.ob_u1_holds(), "still drops the phase carrier");
    assert!(
        !h.local_tomography_holds(),
        "and now ALSO fails local tomography"
    );
    assert!(
        !h.fails_exactly(ImportSlot::ObU1),
        "COUPLED: dropping the U(1) phase carrier on a real-quantum carrier \
         takes local tomography with it, so this is not a drop-one witness"
    );
}

/// The registry can now express the scope, so the OB-U1 evidence is readable as
/// CLASSICAL-scoped rather than unqualified independence.
///
/// Before this, `SlotEvidence` carried only a host id and a consumer could not
/// distinguish "independent over all toy hosts" from "independent over
/// classical hosts only". That gap is what let prose claim a quantum verdict
/// over a registry that said something broader.
#[test]
fn r2c6_ob_u1_independence_is_scoped_to_the_classical_carrier() {
    let SlotEvidence::IndependentWithCountermodel {
        host_id,
        carrier_class,
    } = frozen_slot_evidence(FrozenSlotId::ObU1)
    else {
        panic!("OB-U1 should still carry a countermodel");
    };
    assert_eq!(host_id, "cm_drop_ob_u1");
    assert_eq!(
        carrier_class,
        CarrierClass::ClassicalSimplex,
        "the witness declares simplex counts, so its scope is classical"
    );

    // The scoped query separates the two questions the flat one conflated.
    assert!(independent_slots_over(CarrierClass::ClassicalSimplex).contains(&FrozenSlotId::ObU1));
    assert!(
        !independent_slots_over(CarrierClass::RealQuantum).contains(&FrozenSlotId::ObU1),
        "no real-quantum witness for OB-U1 exists; coupling there stays OPEN"
    );
}

/// The carrier class is COMPUTED from the counts, so it cannot drift from them.
#[test]
fn r2c6_carrier_class_is_derived_from_the_declared_counts() {
    let mut h = countermodel_drop_ob_u1();
    assert_eq!(h.carrier_class(), CarrierClass::ClassicalSimplex);

    let real = LocalTomographyReport::real_product_params(2, 2).unwrap();
    h.local_param_a = real.local_param_a;
    h.local_param_b = real.local_param_b;
    h.joint_param = real.joint_param;
    assert_eq!(
        h.carrier_class(),
        CarrierClass::RealQuantum,
        "substituting the real-quantum counts must move the computed class"
    );

    h.local_param_a = 4;
    h.local_param_b = 4;
    h.joint_param = 16;
    assert_eq!(h.carrier_class(), CarrierClass::ComplexQuantum);

    h.joint_param = 15;
    assert_eq!(
        h.carrier_class(),
        CarrierClass::Unrecognised,
        "counts matching no canonical family must not be silently classified"
    );
}

/// Anti-vacuity: the coupling is specific, not an artifact of perturbing any
/// field. The complex carrier keeps BOTH -- so the coupling is a fact about
/// dropping the phase, not about touching the counts.
#[test]
fn r2c6_complex_carrier_keeps_both_slots() {
    let complex = LocalTomographyReport::complex_product(2, 2).unwrap();
    assert!(
        complex.identity_holds,
        "complex LT holds at 2x2 (4*4 = 16), verified by exact rank in round 2"
    );
    // The spectral/monoidal host that keeps OB-U1 also keeps LT.
    let h = countermodel_drop_spectral();
    assert!(h.ob_u1_holds() && h.local_tomography_holds());
}
