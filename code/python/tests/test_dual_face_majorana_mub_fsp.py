"""Tests for the dual-face Python modules matching Rust in code/rust/src.

Covers:
- 18 modules in src/majorana matching code/rust/src/majorana/
- MUB verification and crate exports matching code/rust/src/mub/
- FSP witness and refusal gates matching code/rust/src/wdp/derivation_controls/wdp_21_16_fsp.rs
AuthorityEffect: None.
"""

from fractions import Fraction
import pytest

from src.majorana import (
    # Fock and operators
    first_anticommutation_failure,
    FockCarrier,
    MajoranaError,
    MAX_MODES,
    MajoranaMonomial,
    MajoranaOperator,
    anticommutator,
    commutator,
    kitaev_chain_parity,
    # Classifier
    classify,
    classify_default,
    ClassifiedReceipt,
    Terminal,
    CLASSIFIED_RECEIPT_TAG,
    # Harmonic and Betti
    code_distance,
    h1_basis,
    l1_harmonic_projection,
    H1Basis,
    L1HarmonicProjection,
    HARMONIC_DEFAULT_BUDGET,
    # Tetron array
    build_tetron_array,
    logical_class_representative,
    Axis,
    TetronReport,
    Topology,
    # Stock complexes
    closed_residual_syndrome_example,
    exact_syndrome_example,
    open_syndrome_example,
    plaquette,
    prism,
    surface_exact_from_vertex0,
    surface_grid,
    surface_grid_2x2_planar,
    surface_grid_2x2_torus,
    surface_open_single_edge_example,
    torus_logical_x_example,
    torus_logical_z_example,
    triangle,
    ChainComplexGf2,
    # Dual observer
    dual_observe,
    observer_even_edge_parity,
    observer_face_syndrome,
    observer_first_face_only,
    DualObserverReceipt,
    ObservationMap,
    DUAL_OBS_RECEIPT_TAG,
    # GF(2) terminalizer
    Cyclotomic16Element,
    GF2Matrix,
    GF2ScheduleStatus,
    Gf2CocycleClassifier,
    Gf2ScheduleReceipt,
    GF2_AUTHORITY_FENCE,
    # Holonomy
    connect_to_schedule_class,
    face_edge_support,
    face_holonomy_residual_gf2,
    gauge_transform_gf2,
    holonomy_receipt_cyclotomic_face0,
    holonomy_receipt_gf2,
    HolonomyReceiptCyclotomic,
    HolonomyReceiptGf2,
    HOLONOMY_AUTHORITY_FENCE,
    HOLONOMY_RECEIPT_TAG,
    # LGGR
    lggr_apply_d1,
    detect_lggr,
    LggrWitness,
    # Packet wall
    admit_or_refuse,
    demo_count_packet,
    illustrative_p_pair,
    illustrative_suppression_regime,
    incomplete_count_packet,
    terminalize_count_packet,
    terminalize_packet,
    wall_with_audit,
    CountPacketReceipt,
    CountRepairPacket,
    DiagnosticPacket,
    PacketRefusal,
    PacketWallReceipt,
    PacketWallTerminal,
    ToyRepairPacket,
    PACKET_WALL_AUTHORITY_FENCE,
    # Repair capacity
    assert_repair_capacity_invariant,
    min_weight_nontrivial,
    repair_capacity_from_distance,
    # Repair limit
    apply_d0,
    apply_d1,
    audit_repair_capacity,
    coset_decode_demo,
    face_syndrome,
    gf2_add,
    hamming_weight,
    homology_distance,
    in_image_d0,
    is_closed,
    lggr_demo_on,
    lggr_demo_torus,
    repair_capacity_bound,
    repair_capacity_t,
    solve_d0,
    syndrome_is_zero,
    CosetDecodeDemo,
    HomologyDistanceReport,
    LggrDemoReport,
    RepairCapacityReceipt,
    REPAIR_LIMIT_AUTHORITY_FENCE,
    # Authority
    AUTHORITY_EFFECT,
    AUTHORITY_FENCE,
    RECEIPT_TAG,
)

from src.majorana import (
    braid_action,
    multiqubit_braid,
    sparse_kitaev,
    pauli_noise,
    noise_mc,
    hard_invariants,
)

from src.mub import (
    verify_mub_crate_invariants,
    authority_effect as mub_authority_effect,
    package_info as mub_package_info,
    Cyc24,
    IndependentMubVerifier,
)

from src.fsp import (
    witness as fsp_witness,
    refuse_removed_holonomy as fsp_refuse_removed_holonomy,
    refuse_foreign_fixture as fsp_refuse_foreign_fixture,
    Witness as FspWitness,
    HOPS as FSP_HOPS,
    MASKS as FSP_MASKS,
    AUTHORITY_EFFECT as FSP_AUTHORITY_EFFECT,
)


def test_majorana_hard_invariants():
    """Execute the full 10-invariant battery mirroring hard_invariants.rs."""
    results = hard_invariants.run_all_hard_invariants()
    for name, passed in results.items():
        assert passed, f"Hard invariant failed: {name}"


def test_majorana_fock_and_modes():
    """Verify Fock carrier Jordan-Wigner relations and mode algebra."""
    fc = FockCarrier(2)
    assert fc.modes() == 2
    assert fc.dimension() == 4
    g1 = fc.majorana_generator(1)
    g2 = fc.majorana_generator(2)
    p = fc.parity_operator()
    assert len(g1) == 4
    assert len(g2) == 4
    assert len(p) == 4

    # Monomial algebra check
    m0 = MajoranaMonomial.single(0)
    m1 = MajoranaMonomial.single(1)
    sign, prod = m0.multiply(m1)
    assert sign == Fraction(1)
    assert prod.modes == (0, 1)


def test_majorana_braiding_and_multiqubit():
    """Verify exact braid action and multi-qubit compilation."""
    act = braid_action.MajoranaBraidAction.elementary(4, 1)
    assert act.image(1) == braid_action.SignedMajorana(2, 1)
    assert act.image(2) == braid_action.SignedMajorana(1, -1)
    assert act.determinant_sign() == 1

    compiled = multiqubit_braid.compile_multi_qubit_braid(
        2,
        [
            multiqubit_braid.MultiQubitOperation.Phase(1),
            multiqubit_braid.MultiQubitOperation.Hadamard(2),
        ],
    )
    assert compiled.action.mode_count() == 8
    assert compiled.gate_count == 2


def test_sparse_kitaev_wire():
    """Verify sweet spot Majorana isolation on open Kitaev chain."""
    wire = sparse_kitaev.SparseKitaevWire(4, Fraction(1), Fraction(1), Fraction(0))
    iso = wire.isolated_majoranas()
    assert iso == [1, 8]


def test_tetron_and_harmonic():
    """Verify tetron surface carriers and Betti classification."""
    c, rep = build_tetron_array(2, 2, Topology.Torus)
    assert rep.dim_h1 == 2
    assert rep.code_distance == 2
    assert rep.topology == Topology.Torus

    # Logical representatives
    x_rep = logical_class_representative(rep, Axis.Column, 0)
    z_rep = logical_class_representative(rep, Axis.Row, 0)
    assert len(x_rep) == 8
    assert len(z_rep) == 8

    # Classification
    rec = classify_default(c.d0, c.d1, x_rep)
    assert rec.terminal == Terminal.TypedHarmonic
    assert rec.phi1_certified


def test_packet_wall_and_dual_observer():
    """Verify packet wall capacity limits and dual observation."""
    c = surface_grid_2x2_torus()
    x_log = torus_logical_x_example()

    # Dual observer
    obs_face = observer_face_syndrome(c)
    obs_first = observer_first_face_only(c)
    receipt = dual_observe(c, x_log, obs_face, obs_first)
    assert receipt.agree_on_zero

    # Packet wall
    p_toy = ToyRepairPacket(complex=c, residual=x_log, declared_distance=2)
    pw_rec = terminalize_packet(p_toy)
    # wt=2 > (2-1)//2 = 0 -> CapacityWallHit
    assert pw_rec.terminal == PacketWallTerminal.CapacityWallHit


def test_mub_dual_face():
    """Verify MUB crate exports and invariant check matching Rust."""
    assert verify_mub_crate_invariants()
    assert mub_authority_effect() == "None"
    info = mub_package_info()
    assert info["name"] == "omega_mub"
    assert info["math_ssot"] == "rust"


def test_fsp_witness_and_refusal():
    """Verify FSP witness matching Rust wdp_21_16_fsp.rs."""
    w = fsp_witness()
    assert w.hop_product == -1
    assert w.parity_sum == 3
    assert w.parity_f2 == 1
    assert w.k == 1
    assert w.z_u == 0
    assert w.n_u == 2
    assert w.all_negative_product == 1

    fsp_refuse_removed_holonomy(-1)
    fsp_refuse_foreign_fixture(0)
    fsp_refuse_foreign_fixture(2)

    with pytest.raises(ValueError):
        fsp_refuse_removed_holonomy(1)

    with pytest.raises(ValueError):
        fsp_refuse_foreign_fixture(912)

    with pytest.raises(ValueError):
        fsp_refuse_foreign_fixture(36864)
