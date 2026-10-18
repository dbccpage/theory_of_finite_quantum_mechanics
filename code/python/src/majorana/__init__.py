"""Majorana GF(2) parity diagnostic playground and dual-face package.

AuthorityEffect: None.
"""

from __future__ import annotations

# Re-exports from majorana_modes.py (preserving backward compatibility)
from .majorana_modes import (
    MajoranaError,
    MajoranaMonomial,
    MajoranaOperator,
    anticommutator,
    commutator,
    kitaev_chain_parity,
)

# Re-exports matching code/rust/src/majorana/lib.rs
from .majorana_fock_algebra import (
    MAX_MODES,
    FockCarrier,
    first_anticommutation_failure,
)

from .classify import (
    CLASSIFIED_RECEIPT_TAG,
    ClassifiedReceipt,
    Terminal,
    classify,
    classify_default,
    classify_with_diagnostics,
)

from .harmonic import (
    DEFAULT_BUDGET as HARMONIC_DEFAULT_BUDGET,
    H1Basis,
    L1HarmonicProjection,
    code_distance,
    h1_basis,
    l1_harmonic_projection,
)

from .tetron import (
    Axis,
    TetronReport,
    Topology,
    build_tetron_array,
    logical_class_representative,
)

from .complexes import (
    ChainComplexGf2,
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
)

from .dual_observer import (
    DUAL_OBS_RECEIPT_TAG,
    DualObserverReceipt,
    ObservationMap,
    dual_observe,
    observer_even_edge_parity,
    observer_face_syndrome,
    observer_first_face_only,
)

from .gf2_terminalizer import (
    AUTHORITY_FENCE as GF2_AUTHORITY_FENCE,
    Cyclotomic16Element,
    GF2Matrix,
    GF2ScheduleStatus,
    Gf2CocycleClassifier,
    Gf2ScheduleReceipt,
)

from .holonomy import (
    AUTHORITY_FENCE as HOLONOMY_AUTHORITY_FENCE,
    HOLONOMY_RECEIPT_TAG,
    HolonomyReceiptCyclotomic,
    HolonomyReceiptGf2,
    connect_to_schedule_class,
    face_edge_support,
    face_holonomy_residual_gf2,
    gauge_transform_gf2,
    holonomy_receipt_cyclotomic_face0,
    holonomy_receipt_gf2,
)

from .lggr import (
    LggrWitness,
    apply_d1 as lggr_apply_d1,
    detect_lggr,
)

from .packet_wall import (
    PACKET_WALL_AUTHORITY_FENCE,
    CountDefectEvent,
    CountPacketReceipt,
    CountRepairAction,
    CountRepairPacket,
    DefectEvent,
    DiagnosticPacket,
    PacketMetrics,
    PacketRefusal,
    PacketWallReceipt,
    PacketWallTerminal,
    RepairAction,
    ToyRepairPacket,
    admit_or_refuse,
    demo_count_packet,
    illustrative_p_pair,
    illustrative_suppression_regime,
    incomplete_count_packet,
    terminalize_count_packet,
    terminalize_packet,
    wall_with_audit,
)

from .repair_capacity import (
    assert_repair_capacity_invariant,
    min_weight_nontrivial,
    repair_capacity_from_distance,
)

from .repair_limit import (
    AUTHORITY_FENCE as REPAIR_LIMIT_AUTHORITY_FENCE,
    CosetDecodeDemo,
    HomologyDistanceReport,
    LggrDemoReport,
    RepairCapacityReceipt,
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
)

AUTHORITY_EFFECT: str = "AuthorityEffect: None"
AUTHORITY_FENCE: str = (
    "AuthorityEffect None; not PROVED; not GlobalGreen; not physical Majorana; "
    "diagnostic GF(2) only."
)
RECEIPT_TAG: str = "omega.majorana-gf2-receipt.v1"
