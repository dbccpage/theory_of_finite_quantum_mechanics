"""Declared repair-capacity packet wall.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .complexes import ChainComplexGf2
from .gf2_terminalizer import (
    GF2Matrix,
    GF2ScheduleStatus,
    Gf2CocycleClassifier,
    Gf2ScheduleReceipt,
)
from .repair_limit import (
    face_syndrome,
    hamming_weight,
    repair_capacity_bound,
    syndrome_is_zero,
)

PACKET_WALL_RECEIPT_TAG = "omega.majorana-packet-wall-receipt.v1"
COUNT_RECEIPT_TAG = "omega.majorana-count-packet-receipt.v1"
PACKET_WALL_AUTHORITY_FENCE = (
    "AuthorityEffect None; incomplete packets refuse; residual+logical after repair "
    "saturation is a declared-packet capacity wall only; not a physical no-go."
)


class PacketWallTerminal(str, Enum):
    Absorbed = "Absorbed"
    ResidualInvisible = "ResidualInvisible"
    ResidualLogicallyVisible = "ResidualLogicallyVisible"
    Refused = "Refused"
    Exact = "Exact"
    ClosedResidual = "ClosedResidual"
    OpenObstruction = "OpenObstruction"
    IncompleteRefusal = "IncompleteRefusal"
    CapacityWallHit = "CapacityWallHit"


@dataclass
class DefectEvent:
    residual: List[int]
    weight: int


@dataclass
class RepairAction:
    proposed_weight: int
    within_capacity: Optional[bool] = None


@dataclass
class ToyRepairPacket:
    complex: Optional[ChainComplexGf2] = None
    residual: Optional[Sequence[int]] = None
    declared_distance: Optional[int] = None
    defect: Optional[DefectEvent] = None
    declared_distance_d: Optional[int] = None
    proposed_repair: Optional[RepairAction] = None

    def __post_init__(self) -> None:
        if self.defect is None and self.residual is not None:
            res_list = [int(b) % 2 for b in self.residual]
            self.defect = DefectEvent(residual=res_list, weight=hamming_weight(res_list))
        if self.declared_distance_d is None and self.declared_distance is not None:
            self.declared_distance_d = self.declared_distance
        if self.declared_distance is None and self.declared_distance_d is not None:
            self.declared_distance = self.declared_distance_d

    @classmethod
    def complete(cls, complex: ChainComplexGf2, residual: Sequence[int]) -> "ToyRepairPacket":
        res_list = [int(b) % 2 for b in residual]
        return cls(
            complex=complex,
            residual=res_list,
            defect=DefectEvent(residual=res_list, weight=hamming_weight(res_list)),
        )

    @classmethod
    def empty(cls) -> "ToyRepairPacket":
        return cls()


@dataclass
class PacketWallReceipt:
    certificate_tag: str
    terminal: PacketWallTerminal
    schedule_status: Optional[GF2ScheduleStatus]
    face_syndrome_zero: Optional[bool]
    complex_name: Optional[str]
    residual_weight: Optional[int]
    repair_capacity_t: Optional[int]
    authority_effect: str = "None"
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "certificate_tag": self.certificate_tag,
            "terminal": self.terminal.value,
            "schedule_status": self.schedule_status.value if self.schedule_status is not None else None,
            "face_syndrome_zero": self.face_syndrome_zero,
            "complex_name": self.complex_name,
            "residual_weight": self.residual_weight,
            "repair_capacity_t": self.repair_capacity_t,
            "authority_effect": self.authority_effect,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PacketWallReceipt":
        sched = data.get("schedule_status")
        return cls(
            certificate_tag=str(data["certificate_tag"]),
            terminal=PacketWallTerminal(str(data["terminal"])),
            schedule_status=GF2ScheduleStatus(str(sched)) if sched is not None else None,
            face_syndrome_zero=bool(data["face_syndrome_zero"]) if data.get("face_syndrome_zero") is not None else None,
            complex_name=str(data["complex_name"]) if data.get("complex_name") is not None else None,
            residual_weight=int(data["residual_weight"]) if data.get("residual_weight") is not None else None,
            repair_capacity_t=int(data["repair_capacity_t"]) if data.get("repair_capacity_t") is not None else None,
            authority_effect=str(data["authority_effect"]),
            notes=str(data["notes"]),
        )


def terminalize_packet(packet: ToyRepairPacket) -> PacketWallReceipt:
    t_opt = (
        repair_capacity_bound(packet.declared_distance_d)
        if packet.declared_distance_d is not None
        else None
    )
    if packet.complex is None:
        return PacketWallReceipt(
            certificate_tag=PACKET_WALL_RECEIPT_TAG,
            terminal=PacketWallTerminal.IncompleteRefusal,
            schedule_status=None,
            face_syndrome_zero=None,
            complex_name=None,
            residual_weight=None,
            repair_capacity_t=t_opt,
            authority_effect="None",
            notes="IncompletePacket: missing complex",
        )
    complex = packet.complex
    if packet.defect is None:
        return PacketWallReceipt(
            certificate_tag=PACKET_WALL_RECEIPT_TAG,
            terminal=PacketWallTerminal.IncompleteRefusal,
            schedule_status=None,
            face_syndrome_zero=None,
            complex_name=complex.name,
            residual_weight=None,
            repair_capacity_t=t_opt,
            authority_effect="None",
            notes="IncompletePacket: missing defect",
        )
    defect = packet.defect

    if not complex.verify_boundary():
        return PacketWallReceipt(
            certificate_tag=PACKET_WALL_RECEIPT_TAG,
            terminal=PacketWallTerminal.IncompleteRefusal,
            schedule_status=None,
            face_syndrome_zero=None,
            complex_name=complex.name,
            residual_weight=defect.weight,
            repair_capacity_t=t_opt,
            authority_effect="None",
            notes="IncompletePacket: boundary invalid (d1 d0 != 0); refused",
        )

    try:
        cert = Gf2CocycleClassifier.classify(complex.d0, complex.d1, defect.residual)
    except ValueError as exc:
        return PacketWallReceipt(
            certificate_tag=PACKET_WALL_RECEIPT_TAG,
            terminal=PacketWallTerminal.IncompleteRefusal,
            schedule_status=None,
            face_syndrome_zero=None,
            complex_name=complex.name,
            residual_weight=defect.weight,
            repair_capacity_t=t_opt,
            authority_effect="None",
            notes=f"IncompletePacket: terminalize refused: {exc}",
        )

    syn_zero: Optional[bool]
    try:
        syn = face_syndrome(complex.d1, defect.residual)
        syn_zero = all(s == 0 for s in syn)
    except ValueError:
        syn_zero = None

    capacity_hit = (
        t_opt is not None
        and cert.schedule_status == GF2ScheduleStatus.ClosedResidual
        and defect.weight > t_opt
    )

    if capacity_hit:
        terminal = PacketWallTerminal.CapacityWallHit
    elif cert.schedule_status == GF2ScheduleStatus.Exact:
        terminal = PacketWallTerminal.Exact
    elif cert.schedule_status == GF2ScheduleStatus.ClosedResidual:
        terminal = PacketWallTerminal.ClosedResidual
    else:
        terminal = PacketWallTerminal.OpenObstruction

    d_rust_fmt = (
        f"Some({packet.declared_distance_d})"
        if packet.declared_distance_d is not None
        else "None"
    )
    if terminal == PacketWallTerminal.ClosedResidual:
        notes = "Local green (face syndrome 0) + ClosedResidual = LGGR diagnostic; Auth=None"
    elif terminal == PacketWallTerminal.CapacityWallHit:
        notes = (
            f"Capacity wall: weight {defect.weight} > t={t_opt if t_opt is not None else 0} "
            f"for declared d={d_rust_fmt}; silent logical class possible. Auth=None"
        )
    elif terminal == PacketWallTerminal.Exact:
        notes = "Exact coboundary class; Auth=None"
    elif terminal == PacketWallTerminal.OpenObstruction:
        notes = "Open obstruction (detectable syndrome); Auth=None"
    elif terminal == PacketWallTerminal.IncompleteRefusal:
        notes = "refused"
    else:
        notes = "diagnostic terminal; Auth=None"

    return PacketWallReceipt(
        certificate_tag=PACKET_WALL_RECEIPT_TAG,
        terminal=terminal,
        schedule_status=cert.schedule_status,
        face_syndrome_zero=syn_zero,
        complex_name=complex.name,
        residual_weight=defect.weight,
        repair_capacity_t=t_opt,
        authority_effect="None",
        notes=notes,
    )


@dataclass
class CountPacketReceipt:
    certificate_tag: str
    terminal: PacketWallTerminal
    count_defects: int
    count_repair_capacity: int
    count_logical_witness: int
    authority_effect: str = "None"
    fence: str = PACKET_WALL_AUTHORITY_FENCE


@dataclass
class PacketRefusal:
    admitted: bool
    reason: Optional[str] = None


@dataclass
class DiagnosticPacket:
    d0_complete: bool
    d1_complete: bool
    syndrome_complete: bool


def admit_or_refuse(packet: DiagnosticPacket) -> PacketRefusal:
    if not packet.d0_complete:
        return PacketRefusal(admitted=False, reason="d0 declaration incomplete")
    if not packet.d1_complete:
        return PacketRefusal(admitted=False, reason="d1 declaration incomplete")
    if not packet.syndrome_complete:
        return PacketRefusal(admitted=False, reason="syndrome declaration incomplete")
    return PacketRefusal(admitted=True, reason=None)


@dataclass
class CountRepairPacket:
    count_c1_defects: Optional[int]
    count_repair_d0_capacity: Optional[int]
    count_logical_witness_remain: Optional[int]


def terminalize_count_packet(packet: CountRepairPacket) -> CountPacketReceipt:
    if (
        packet.count_c1_defects is None
        or packet.count_repair_d0_capacity is None
        or packet.count_logical_witness_remain is None
    ):
        return CountPacketReceipt(
            certificate_tag=COUNT_RECEIPT_TAG,
            terminal=PacketWallTerminal.Refused,
            count_defects=0,
            count_repair_capacity=0,
            count_logical_witness=0,
        )

    d = packet.count_c1_defects
    c = packet.count_repair_d0_capacity
    w = packet.count_logical_witness_remain

    if d <= c:
        term = PacketWallTerminal.Absorbed
    elif w == 0:
        term = PacketWallTerminal.ResidualInvisible
    else:
        term = PacketWallTerminal.ResidualLogicallyVisible

    return CountPacketReceipt(
        certificate_tag=COUNT_RECEIPT_TAG,
        terminal=term,
        count_defects=d,
        count_repair_capacity=c,
        count_logical_witness=w,
    )


def demo_count_packet() -> CountRepairPacket:
    return CountRepairPacket(
        count_c1_defects=5, count_repair_d0_capacity=2, count_logical_witness_remain=1
    )


def incomplete_count_packet() -> CountRepairPacket:
    return CountRepairPacket(
        count_c1_defects=None, count_repair_d0_capacity=2, count_logical_witness_remain=0
    )


def illustrative_p_pair() -> tuple[CountRepairPacket, CountRepairPacket]:
    p1 = CountRepairPacket(
        count_c1_defects=1, count_repair_d0_capacity=2, count_logical_witness_remain=0
    )
    p2 = CountRepairPacket(
        count_c1_defects=4, count_repair_d0_capacity=2, count_logical_witness_remain=1
    )
    return p1, p2


def illustrative_suppression_regime(
    p_pair: tuple[CountRepairPacket, CountRepairPacket]
) -> tuple[CountPacketReceipt, CountPacketReceipt]:
    return terminalize_count_packet(p_pair[0]), terminalize_count_packet(p_pair[1])


def wall_with_audit(packet: ToyRepairPacket) -> PacketWallReceipt:
    return terminalize_packet(packet)


# Aliases for export parity
CountDefectEvent = int
CountRepairAction = int
PacketMetrics = dict
