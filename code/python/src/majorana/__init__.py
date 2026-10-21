"""Package seal for the Majorana certificate.

Origin: lean4/FiniteQM.lean theorem car_clifford_nilpotency_and_occupation_projector.
Claim: urn:omega:fqm:majorana:package-car-seal:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/majorana/test_majorana_control.py.
Gate 5: use source-bound observations; reexports remain under separate provider review.
Scope Fence: package_seal checks the 2x2 CAR matrices. It does not claim a continuum Majorana field.
"""

from __future__ import annotations

from typing import Mapping

from .majorana_modes import MajoranaError, MAX_INTEGER_BITS, car_nilpotency_witness


class PackageError(ValueError):
    """One violated package invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> PackageError:
    return PackageError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if issubclass(type(value), float):
        raise _fail("float refused at the package boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer was required", role=role)
    if type(value) is int:
        if value.bit_length() > MAX_INTEGER_BITS:
            raise _fail("integer bit budget exceeded", role=role, limit=MAX_INTEGER_BITS)
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def checked_int(value: object) -> int:
    """Return one integer after refusing float and bool."""
    return _require_int(value, "checked")


def _sum(left: int, right: int) -> int:
    return left + right


def _gap(left: int, right: int) -> int:
    return left - right


def _product(left: int, right: int) -> int:
    return left * right


def package_seal() -> int:
    """Return the package certificate when the local integer checks agree."""
    value = checked_int(car_nilpotency_witness())
    if value != 0:
        raise _fail("package certificate drifted", value=value)
    if _sum(1, 3) != 4:
        raise _fail("package sum drifted", total=_sum(1, 3))
    if _gap(6, 2) != 4:
        raise _fail("package gap drifted", gap=_gap(6, 2))
    if _product(2, 3) != 6:
        raise _fail("package product drifted", product=_product(2, 3))
    return value


def main() -> int:
    """Print the package certificate."""
    try:
        print(package_seal())
    except (PackageError, MajoranaError) as error:
        try:
            print(error.invariant)
        except (OSError, ValueError):
            return 2
        return 1
    except (OSError, ValueError):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# ---------------------------------------------------------------------------
# Re-exports for Majorana GF(2) parity diagnostic and complexes
# ---------------------------------------------------------------------------
from .majorana_modes import (
    MajoranaMonomial,
    MajoranaOperator,
    anticommutator,
    commutator,
    kitaev_chain_parity,
)

from .majorana_fock_algebra import (
    MAX_MODES,
    FockCarrier,
    first_anticommutation_failure,
)

from .classify import (
    CLASSIFIED_RECEIPT_TAG,
    ClassifiedReceipt,
    ResidualPacketWallReceipt,
    Terminal,
    benchmark_classify_residual,
    classify,
    classify_default,
    classify_residual,
    classify_residual_from_canonical_json,
    classify_residual_to_canonical_json,
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

from .multiqubit_braid import (
    CompiledMultiQubitBraid,
    MultiQubitBraidError,
    MultiQubitBraidScalingRow,
    MultiQubitOperation,
    benchmark_multiqubit_braid_scaling,
    compile_multi_qubit_braid,
    compile_multiqubit_braid,
    compile_multiqubit_braid_with_limit,
    multiqubit_braid_scaling_from_canonical_json,
    multiqubit_braid_scaling_to_canonical_json,
)

from .pauli_noise import (
    MAX_NOISE_MODES,
    DeterministicRationalNoiseGenerator,
    LocalMajoranaNoise,
    NoiseError,
    NoiseEvaluation,
    PauliNoiseScalingRow,
    SkewNoiseMatrix,
    benchmark_pauli_noise_scaling,
    correlated_cluster_couplings,
    evaluate_noise,
    pauli_noise_scaling_from_canonical_json,
    pauli_noise_scaling_to_canonical_json,
)

from .sparse_kitaev import (
    MAX_WIRE_SITES,
    BoundaryIsolation,
    KitaevWire,
    KitaevWireError,
    KitaevWireScalingReceipt,
    MajoranaBilinear,
    SparseKitaevWire,
    benchmark_sparse_kitaev_scaling,
    sparse_kitaev_scaling_from_canonical_json,
    sparse_kitaev_scaling_to_canonical_json,
)

from .tetron import (
    Axis,
    TetronReport,
    TetronScalingRow,
    Topology,
    benchmark_tetron_lattice_scaling,
    build_tetron_array,
    logical_class_representative,
    tetron_scaling_from_canonical_json,
    tetron_scaling_to_canonical_json,
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

from .majorana_evaluator import (
    ContinuumCrossJunctionFemModel,
    DetectorAdequacyAudit,
    DetectorAdequacyReceipt,
    F2CochainComplex,
    IsingFusionAlgebra,
    KitaevSweetSpotChain,
    MultiTerminalTransferReceipt,
    NonMarkovianBosonicBathModel,
    NonMarkovianTransferReceipt,
    OpenSystemMajoranaBraidModel,
    ParityAlgebraModel,
    TetronCarrier,
    TransferBoundReceipt,
    TrichotomyClass,
    audit_legacy_carrier,
    build_tetron_carrier,
    compute_coset_weight,
    compute_skew_pfaffian,
    logical_representative,
    pfaffian_z2_invariant,
    verify_norm_equivalence,
)

AUTHORITY_FENCE: str = (
    "AuthorityEffect None; not PROVED; not GlobalGreen; not physical Majorana; "
    "diagnostic GF(2) only."
)
RECEIPT_TAG: str = "omega.majorana-gf2-receipt.v1"

AUTHORITY_EFFECT: str = "AuthorityEffect: None"
