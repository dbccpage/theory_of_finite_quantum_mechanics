
#![forbid(unsafe_code)]

pub mod braid_action;
pub mod classify;
pub mod complexes;
pub mod dual_observer;
pub mod gf2_terminalizer;
pub mod hard_invariants;
pub mod harmonic;
pub mod holonomy;
pub mod lggr;
pub mod majorana_fock_algebra;
pub mod multiqubit_braid;
pub mod noise_mc;
pub mod pauli_noise;
pub mod packet_wall;
pub mod repair_capacity;
pub mod repair_limit;
pub mod sparse_kitaev;
pub mod tetron;

pub use majorana_fock_algebra::{
    first_anticommutation_failure, FockCarrier, MajoranaError, MAX_MODES,
};

pub use classify::{
    classify, classify_default, classify_with_diagnostics, ClassifiedReceipt, Terminal,
    CLASSIFIED_RECEIPT_TAG,
};
pub use harmonic::{
    code_distance, h1_basis, l1_harmonic_projection, H1Basis, L1HarmonicProjection,
    DEFAULT_BUDGET as HARMONIC_DEFAULT_BUDGET,
};
pub use tetron::{build_tetron_array, logical_class_representative, Axis, TetronReport, Topology};

pub use complexes::{
    closed_residual_syndrome_example, exact_syndrome_example, open_syndrome_example, plaquette,
    prism, surface_exact_from_vertex0, surface_grid, surface_grid_2x2_planar,
    surface_grid_2x2_torus, surface_open_single_edge_example, torus_logical_x_example,
    torus_logical_z_example, triangle, ChainComplexGf2,
};
pub use dual_observer::{
    dual_observe, observer_even_edge_parity, observer_face_syndrome, observer_first_face_only,
    DualObserverReceipt, ObservationMap, DUAL_OBS_RECEIPT_TAG,
};
pub use gf2_terminalizer::{
    Cyclotomic16Element, GF2Matrix, GF2ScheduleStatus, Gf2CocycleClassifier, Gf2ScheduleReceipt,
    AUTHORITY_FENCE as GF2_AUTHORITY_FENCE,
};
pub use holonomy::{
    connect_to_schedule_class, face_edge_support, face_holonomy_residual_gf2, gauge_transform_gf2,
    holonomy_receipt_cyclotomic_face0, holonomy_receipt_gf2, HolonomyReceiptCyclotomic,
    HolonomyReceiptGf2, AUTHORITY_FENCE as HOLONOMY_AUTHORITY_FENCE, HOLONOMY_RECEIPT_TAG,
};
pub use lggr::{apply_d1 as lggr_apply_d1, detect_lggr, LggrWitness};
pub use packet_wall::{
    admit_or_refuse, demo_count_packet, illustrative_p_pair, illustrative_suppression_regime,
    incomplete_count_packet, terminalize_count_packet, terminalize_packet, wall_with_audit,
    CountDefectEvent, CountPacketReceipt, CountRepairAction, CountRepairPacket, DefectEvent,
    DiagnosticPacket, PacketMetrics, PacketRefusal, PacketWallReceipt, PacketWallTerminal,
    RepairAction, ToyRepairPacket, AUTHORITY_FENCE as PACKET_WALL_AUTHORITY_FENCE,
};
pub use repair_capacity::{
    assert_repair_capacity_invariant, min_weight_nontrivial, repair_capacity_from_distance,
};
pub use repair_limit::{
    apply_d0, apply_d1, audit_repair_capacity, coset_decode_demo, face_syndrome, gf2_add,
    hamming_weight, homology_distance, in_image_d0, is_closed, lggr_demo_on, lggr_demo_torus,
    repair_capacity_bound, repair_capacity_t, solve_d0, syndrome_is_zero, CosetDecodeDemo,
    HomologyDistanceReport, LggrDemoReport, RepairCapacityReceipt,
    AUTHORITY_FENCE as REPAIR_LIMIT_AUTHORITY_FENCE,
};

pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";

pub const AUTHORITY_FENCE: &str = "AuthorityEffect None; not PROVED; not GlobalGreen; not physical Majorana; diagnostic GF(2) only.";

pub const RECEIPT_TAG: &str = "omega.majorana-gf2-receipt.v1";
