"""End-to-end residual classifier: residual -> terminal + receipt.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any, Dict, List, Optional, Sequence

from .complexes import (
    ChainComplexGf2,
    closed_residual_syndrome_example,
    exact_syndrome_example,
    open_syndrome_example,
    plaquette,
    surface_exact_from_vertex0,
    surface_grid_2x2_planar,
    surface_grid_2x2_torus,
    surface_open_single_edge_example,
    torus_logical_x_example,
    torus_logical_z_example,
    triangle,
)
from .gf2_terminalizer import (
    GF2Matrix,
    GF2ScheduleStatus,
    Gf2CocycleClassifier,
)
from .harmonic import (
    DEFAULT_BUDGET,
    H1Basis,
    h1_basis,
    l1_harmonic_projection,
)
from .lggr import detect_lggr
from .packet_wall import PacketWallReceipt, ToyRepairPacket, terminalize_packet
from .repair_limit import (
    apply_d0,
    apply_d1,
    gf2_add,
    hamming_weight,
    in_image_d0,
    repair_capacity_bound,
    solve_d0,
)
from .tetron import Axis, Topology, build_tetron_array, logical_class_representative

CLASSIFIED_RECEIPT_TAG = "omega.majorana-tetron-classified.v1"


class Terminal(str, Enum):
    Exact = "Exact"
    OpenObstruction = "OpenObstruction"
    ClosedResidual = "ClosedResidual"
    TypedHarmonic = "TypedHarmonic"
    RepresentationInvalid = "RepresentationInvalid"

    def reading(self) -> str:
        readings = {
            Terminal.Exact: "pure gauge: an MZM reference-frame relabelling; no defect",
            Terminal.OpenObstruction: (
                "an island parity constraint is violated; a localized "
                "violated declared island parity relation, named by the coherence \n"
                "                 witness; physical cause UNDETERMINED"
            ),
            Terminal.ClosedResidual: (
                "consistent with every island constraint but not gauge: a logical "
                "parity error whose minimum weight was not certified"
            ),
            Terminal.TypedHarmonic: (
                "a logical parity error, identified in the H^1 basis, with a "
                "certified minimum-weight witness"
            ),
            Terminal.RepresentationInvalid: "the declared carrier is not a cochain complex",
        }
        return readings[self]


@dataclass
class ClassifiedReceipt:
    certificate_tag: str
    terminal: Terminal
    terminal_reading: str
    reason: str
    dim_h1: Optional[int]
    class_coordinates: Optional[List[int]]
    class_id: Optional[str]
    coherence_witness: Optional[List[int]]
    certificate_alpha: Optional[List[int]]
    certificate_verified: Optional[bool]
    phi1_weight: Optional[int]
    phi1_exact: Optional[bool]
    phi1_representative: Optional[List[int]]
    phi1_alpha: Optional[List[int]]
    phi1_searched: Optional[int]
    phi1_coset_size: Optional[int]
    phi1_verified: Optional[bool]
    authority_effect: str = "None"

    @property
    def phi1_certified(self) -> bool:
        return bool(self.phi1_exact)

    @property
    def phi1_min_weight(self) -> Optional[int]:
        return self.phi1_weight

    def to_dict(self) -> Dict[str, Any]:
        return {
            "certificate_tag": self.certificate_tag,
            "terminal": self.terminal.value,
            "terminal_reading": self.terminal_reading,
            "reason": self.reason,
            "dim_h1": self.dim_h1,
            "class_coordinates": self.class_coordinates,
            "class_id": self.class_id,
            "coherence_witness": self.coherence_witness,
            "certificate_alpha": self.certificate_alpha,
            "certificate_verified": self.certificate_verified,
            "phi1_weight": self.phi1_weight,
            "phi1_exact": self.phi1_exact,
            "phi1_representative": self.phi1_representative,
            "phi1_alpha": self.phi1_alpha,
            "phi1_searched": self.phi1_searched,
            "phi1_coset_size": self.phi1_coset_size,
            "phi1_verified": self.phi1_verified,
            "authority_effect": self.authority_effect,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClassifiedReceipt":
        return cls(
            certificate_tag=str(data["certificate_tag"]),
            terminal=Terminal(str(data["terminal"])),
            terminal_reading=str(data["terminal_reading"]),
            reason=str(data["reason"]),
            dim_h1=int(data["dim_h1"]) if data.get("dim_h1") is not None else None,
            class_coordinates=(
                [int(x) for x in data["class_coordinates"]]
                if data.get("class_coordinates") is not None
                else None
            ),
            class_id=str(data["class_id"]) if data.get("class_id") is not None else None,
            coherence_witness=(
                [int(x) for x in data["coherence_witness"]]
                if data.get("coherence_witness") is not None
                else None
            ),
            certificate_alpha=(
                [int(x) for x in data["certificate_alpha"]]
                if data.get("certificate_alpha") is not None
                else None
            ),
            certificate_verified=(
                bool(data["certificate_verified"])
                if data.get("certificate_verified") is not None
                else None
            ),
            phi1_weight=int(data["phi1_weight"]) if data.get("phi1_weight") is not None else None,
            phi1_exact=bool(data["phi1_exact"]) if data.get("phi1_exact") is not None else None,
            phi1_representative=(
                [int(x) for x in data["phi1_representative"]]
                if data.get("phi1_representative") is not None
                else None
            ),
            phi1_alpha=(
                [int(x) for x in data["phi1_alpha"]]
                if data.get("phi1_alpha") is not None
                else None
            ),
            phi1_searched=int(data["phi1_searched"]) if data.get("phi1_searched") is not None else None,
            phi1_coset_size=int(data["phi1_coset_size"]) if data.get("phi1_coset_size") is not None else None,
            phi1_verified=(
                bool(data["phi1_verified"]) if data.get("phi1_verified") is not None else None
            ),
            authority_effect=str(data["authority_effect"]),
        )


def _invalid(reason: str) -> ClassifiedReceipt:
    return ClassifiedReceipt(
        certificate_tag=CLASSIFIED_RECEIPT_TAG,
        terminal=Terminal.RepresentationInvalid,
        terminal_reading=Terminal.RepresentationInvalid.reading(),
        reason=reason,
        dim_h1=None,
        class_coordinates=None,
        class_id=None,
        coherence_witness=None,
        certificate_alpha=None,
        certificate_verified=None,
        phi1_weight=None,
        phi1_exact=None,
        phi1_representative=None,
        phi1_alpha=None,
        phi1_searched=None,
        phi1_coset_size=None,
        phi1_verified=None,
        authority_effect="None",
    )


def _classify_inner(
    d0: GF2Matrix,
    d1: GF2Matrix,
    residual: Sequence[int],
    budget: int,
    always_project: bool,
) -> ClassifiedReceipt:
    if len(residual) != d0.rows:
        return _invalid("residual length does not match the channel count")
    if not Gf2CocycleClassifier.verify_boundary(d0, d1):
        return _invalid("d1 * d0 != 0")

    normalized = [int(v) % 2 for v in residual]
    basis = h1_basis(d0, d1)
    coordinates = basis.class_coordinates(normalized)

    try:
        syndrome = apply_d1(d1, normalized)
    except ValueError as exc:
        return _invalid(str(exc))

    is_open = 1 in syndrome
    is_exact = in_image_d0(d0, normalized)

    if (is_open or is_exact) and not always_project:
        projection = None
    else:
        try:
            projection = l1_harmonic_projection(d0, normalized, budget)
        except ValueError as exc:
            return _invalid(str(exc))

    verified: Optional[bool]
    if projection is not None:
        try:
            img = apply_d0(d0, projection.alpha)
            combined = gf2_add(normalized, img)
            verified = combined == projection.representative
        except ValueError:
            verified = False
    else:
        verified = None

    if is_exact:
        terminal = Terminal.Exact
        reason = "residual lies in im(d0)"
        witness: Optional[List[int]] = None
    elif is_open:
        terminal = Terminal.OpenObstruction
        reason = "d1 * r != 0"
        witness = syndrome
    elif projection is not None and projection.exact and coordinates is not None:
        label = H1Basis.class_id(coordinates)
        terminal = Terminal.TypedHarmonic
        reason = (
            f"nontrivial class {label} in H^1 (dim {basis.dim}); "
            f"l1-minimal weight {projection.weight} certified"
        )
        witness = None
    else:
        terminal = Terminal.ClosedResidual
        reason = "r not in im(d0) and d1 * r = 0; l1 minimum not certified"
        witness = None

    certificate_alpha = solve_d0(d0, normalized) if terminal == Terminal.Exact else None
    certificate_verified: Optional[bool]
    if certificate_alpha is not None:
        try:
            certificate_verified = apply_d0(d0, certificate_alpha) == normalized
        except ValueError:
            certificate_verified = False
    else:
        certificate_verified = None

    if projection is not None:
        phi1_weight: Optional[int] = projection.weight
        phi1_exact: Optional[bool] = projection.exact
    elif terminal == Terminal.Exact:
        phi1_weight = 0
        phi1_exact = True
    else:
        phi1_weight = None
        phi1_exact = None

    return ClassifiedReceipt(
        certificate_tag=CLASSIFIED_RECEIPT_TAG,
        terminal=terminal,
        terminal_reading=terminal.reading(),
        reason=reason,
        dim_h1=basis.dim,
        class_coordinates=coordinates,
        class_id=H1Basis.class_id(coordinates) if coordinates is not None else None,
        coherence_witness=witness,
        certificate_alpha=certificate_alpha,
        certificate_verified=certificate_verified,
        phi1_weight=phi1_weight,
        phi1_exact=phi1_exact,
        phi1_representative=list(projection.representative) if projection is not None else None,
        phi1_alpha=list(projection.alpha) if projection is not None else None,
        phi1_searched=projection.searched if projection is not None else None,
        phi1_coset_size=projection.coset_size if projection is not None else None,
        phi1_verified=verified,
        authority_effect="None",
    )


def classify(
    d0: GF2Matrix, d1: GF2Matrix, residual: Sequence[int], budget: int = DEFAULT_BUDGET
) -> ClassifiedReceipt:
    return _classify_inner(d0, d1, residual, budget, False)


def classify_default(d0: GF2Matrix, d1: GF2Matrix, residual: Sequence[int]) -> ClassifiedReceipt:
    return classify(d0, d1, residual, DEFAULT_BUDGET)


def classify_with_diagnostics(
    d0: GF2Matrix, d1: GF2Matrix, residual: Sequence[int], budget: int = DEFAULT_BUDGET
) -> ClassifiedReceipt:
    return _classify_inner(d0, d1, residual, budget, True)


@dataclass
class ResidualPacketWallReceipt:
    label: str
    complex_name: str
    num_vertices: int
    num_edges: int
    num_faces: int
    residual: List[int]
    residual_weight: int
    declared_distance_d: Optional[int]
    repair_capacity_t: Optional[int]
    budget: int
    schedule_status: Optional[GF2ScheduleStatus]
    local_green: bool
    global_red: bool
    is_lggr: bool
    classified: ClassifiedReceipt
    packet_wall: PacketWallReceipt
    authority_effect: str = "None"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "complex_name": self.complex_name,
            "num_vertices": self.num_vertices,
            "num_edges": self.num_edges,
            "num_faces": self.num_faces,
            "residual": list(self.residual),
            "residual_weight": self.residual_weight,
            "declared_distance_d": self.declared_distance_d,
            "repair_capacity_t": self.repair_capacity_t,
            "budget": self.budget,
            "schedule_status": self.schedule_status.value if self.schedule_status is not None else None,
            "local_green": self.local_green,
            "global_red": self.global_red,
            "is_lggr": self.is_lggr,
            "classified": self.classified.to_dict(),
            "packet_wall": self.packet_wall.to_dict(),
            "authority_effect": self.authority_effect,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResidualPacketWallReceipt":
        sched = data.get("schedule_status")
        return cls(
            label=str(data["label"]),
            complex_name=str(data["complex_name"]),
            num_vertices=int(data["num_vertices"]),
            num_edges=int(data["num_edges"]),
            num_faces=int(data["num_faces"]),
            residual=[int(x) for x in data["residual"]],
            residual_weight=int(data["residual_weight"]),
            declared_distance_d=(
                int(data["declared_distance_d"])
                if data.get("declared_distance_d") is not None
                else None
            ),
            repair_capacity_t=(
                int(data["repair_capacity_t"])
                if data.get("repair_capacity_t") is not None
                else None
            ),
            budget=int(data["budget"]),
            schedule_status=GF2ScheduleStatus(str(sched)) if sched is not None else None,
            local_green=bool(data["local_green"]),
            global_red=bool(data["global_red"]),
            is_lggr=bool(data["is_lggr"]),
            classified=ClassifiedReceipt.from_dict(data["classified"]),
            packet_wall=PacketWallReceipt.from_dict(data["packet_wall"]),
            authority_effect=str(data["authority_effect"]),
        )


def classify_residual(
    label: str,
    complex: ChainComplexGf2,
    residual: Sequence[int],
    declared_distance_d: Optional[int] = None,
    budget: int = DEFAULT_BUDGET,
) -> ResidualPacketWallReceipt:
    normalized = [int(b) % 2 for b in residual]
    residual_weight = hamming_weight(normalized)
    repair_capacity_t_val = (
        repair_capacity_bound(declared_distance_d)
        if declared_distance_d is not None
        else None
    )
    classified = classify(complex.d0, complex.d1, normalized, budget)
    packet = ToyRepairPacket.complete(complex, normalized)
    packet.declared_distance_d = declared_distance_d
    packet.declared_distance = declared_distance_d
    packet_wall = terminalize_packet(packet)
    try:
        lggr_w = detect_lggr(complex.d0, complex.d1, normalized)
        schedule_status: Optional[GF2ScheduleStatus] = lggr_w.certificate.schedule_status
        local_green = lggr_w.local_green
        global_red = lggr_w.global_red
        is_lggr = lggr_w.is_lggr
    except ValueError:
        schedule_status = None
        local_green = False
        global_red = False
        is_lggr = False

    return ResidualPacketWallReceipt(
        label=label,
        complex_name=complex.name,
        num_vertices=complex.num_vertices,
        num_edges=complex.num_edges,
        num_faces=complex.num_faces,
        residual=normalized,
        residual_weight=residual_weight,
        declared_distance_d=declared_distance_d,
        repair_capacity_t=repair_capacity_t_val,
        budget=budget,
        schedule_status=schedule_status,
        local_green=local_green,
        global_red=global_red,
        is_lggr=is_lggr,
        classified=classified,
        packet_wall=packet_wall,
        authority_effect="None",
    )


def benchmark_classify_residual() -> List[ResidualPacketWallReceipt]:
    """Benchmark the Exact-vs-LGGR-vs-Open cochain packet wall classifier across 14 canonical
    cochain complexes, residuals, declared repair distances, and search budgets.
    Matches Rust tfqm_majorana::benchmark_classify_residual bit-for-bit.
    """
    rows: List[ResidualPacketWallReceipt] = []

    tri = triangle()
    rows.append(
        classify_residual("triangle_exact", tri, exact_syndrome_example(), None, DEFAULT_BUDGET)
    )
    rows.append(
        classify_residual("triangle_open", tri, open_syndrome_example(), None, DEFAULT_BUDGET)
    )

    plaq = plaquette()
    rows.append(
        classify_residual(
            "plaquette_even_cycle_exact",
            plaq,
            closed_residual_syndrome_example(),
            None,
            DEFAULT_BUDGET,
        )
    )

    planar = surface_grid_2x2_planar()
    planar_exact = surface_exact_from_vertex0(planar.d0)
    planar_open = surface_open_single_edge_example(planar.num_edges)
    rows.append(
        classify_residual("planar_2x2_exact_vertex0", planar, planar_exact, None, DEFAULT_BUDGET)
    )
    rows.append(
        classify_residual("planar_2x2_single_edge_open", planar, planar_open, None, DEFAULT_BUDGET)
    )

    torus_2x2 = surface_grid_2x2_torus()
    torus_lx = torus_logical_x_example()
    torus_lz = torus_logical_z_example()
    rows.append(
        classify_residual("torus_2x2_logical_x_lggr", torus_2x2, torus_lx, None, DEFAULT_BUDGET)
    )
    rows.append(
        classify_residual(
            "torus_2x2_logical_x_capacity_wall", torus_2x2, torus_lx, 2, DEFAULT_BUDGET
        )
    )
    rows.append(
        classify_residual(
            "torus_2x2_logical_z_capacity_wall", torus_2x2, torus_lz, 2, DEFAULT_BUDGET
        )
    )

    torus_3x3, report_3x3 = build_tetron_array(3, 3, Topology.Torus)
    alpha_3x3 = [0] * report_3x3.num_mzm
    alpha_3x3[0] = 1
    gauge_3x3 = apply_d0(torus_3x3.d0, alpha_3x3)
    open_3x3 = [0] * report_3x3.num_channels
    open_3x3[0] = 1
    logical_col_3x3 = logical_class_representative(report_3x3, Axis.Column, 0)

    rows.append(
        classify_residual(
            "tetron_torus_3x3_gauge_exact", torus_3x3, gauge_3x3, 3, DEFAULT_BUDGET
        )
    )
    rows.append(
        classify_residual(
            "tetron_torus_3x3_single_edge_open", torus_3x3, open_3x3, 3, DEFAULT_BUDGET
        )
    )
    rows.append(
        classify_residual(
            "tetron_torus_3x3_logical_col_typed_harmonic",
            torus_3x3,
            logical_col_3x3,
            3,
            DEFAULT_BUDGET,
        )
    )
    rows.append(
        classify_residual(
            "tetron_torus_3x3_logical_col_capped_budget",
            torus_3x3,
            logical_col_3x3,
            None,
            4,
        )
    )

    torus_3x4, report_3x4 = build_tetron_array(3, 4, Topology.Torus)
    logical_row_3x4 = logical_class_representative(report_3x4, Axis.Row, 0)
    rows.append(
        classify_residual(
            "tetron_torus_3x4_logical_row_typed_harmonic",
            torus_3x4,
            logical_row_3x4,
            3,
            DEFAULT_BUDGET,
        )
    )

    broken = ChainComplexGf2(
        name="broken_boundary",
        d0=GF2Matrix.from_data([[1, 0], [0, 1]]),
        d1=GF2Matrix.from_data([[1, 0]]),
        num_vertices=2,
        num_edges=2,
        num_faces=1,
    )
    rows.append(
        classify_residual(
            "invalid_broken_boundary_refusal",
            broken,
            [1, 0],
            None,
            DEFAULT_BUDGET,
        )
    )

    return rows


def classify_residual_to_canonical_json(rows: Sequence[ResidualPacketWallReceipt]) -> str:
    """Serialize ResidualPacketWallReceipt list to canonical 2-space pretty JSON with LF line endings."""
    return json.dumps([row.to_dict() for row in rows], indent=2)


def classify_residual_from_canonical_json(json_str: str) -> List[ResidualPacketWallReceipt]:
    """Deserialize ResidualPacketWallReceipt list from canonical JSON string."""
    raw = json.loads(json_str)
    return [ResidualPacketWallReceipt.from_dict(item) for item in raw]
