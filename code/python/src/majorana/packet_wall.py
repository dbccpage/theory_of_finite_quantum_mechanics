"""Declared repair-capacity packet wall.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence

from .complexes import ChainComplexGf2
from .gf2_terminalizer import (
    GF2ScheduleStatus,
    Gf2CocycleClassifier,
)
from .repair_limit import (
    hamming_weight,
    repair_capacity_t,
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
class PacketWallReceipt:
    certificate_tag: str
    terminal: PacketWallTerminal
    complex_name: str
    num_edges: int
    residual_weight: int
    schedule_status: Optional[GF2ScheduleStatus]
    declared_distance: Optional[int]
    repair_capacity_t: Optional[int]
    authority_effect: str = "None"
    fence: str = PACKET_WALL_AUTHORITY_FENCE


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
class ToyRepairPacket:
    complex: Optional[ChainComplexGf2]
    residual: Optional[Sequence[int]]
    declared_distance: Optional[int] = None


def terminalize_packet(packet: ToyRepairPacket) -> PacketWallReceipt:
    if packet.complex is None or packet.residual is None:
        return PacketWallReceipt(
            certificate_tag=PACKET_WALL_RECEIPT_TAG,
            terminal=PacketWallTerminal.IncompleteRefusal,
            complex_name="unknown",
            num_edges=0,
            residual_weight=0,
            schedule_status=None,
            declared_distance=None,
            repair_capacity_t=None,
        )

    complex = packet.complex
    residual = packet.residual
    wt = hamming_weight(residual)
    t = packet.declared_distance
    cap_t = (t - 1) // 2 if (t is not None and t > 0) else None

    # Check capacity wall hit if distance is declared
    if cap_t is not None and wt > cap_t:
        return PacketWallReceipt(
            certificate_tag=PACKET_WALL_RECEIPT_TAG,
            terminal=PacketWallTerminal.CapacityWallHit,
            complex_name=complex.name,
            num_edges=complex.num_edges,
            residual_weight=wt,
            schedule_status=None,
            declared_distance=t,
            repair_capacity_t=cap_t,
        )

    # Otherwise classify through GF2 terminalizer
    cert = Gf2CocycleClassifier.classify(complex.d0, complex.d1, residual)
    if cert.schedule_status == GF2ScheduleStatus.Exact:
        term = PacketWallTerminal.Exact
    elif cert.schedule_status == GF2ScheduleStatus.ClosedResidual:
        term = PacketWallTerminal.ClosedResidual
    else:
        term = PacketWallTerminal.OpenObstruction

    return PacketWallReceipt(
        certificate_tag=PACKET_WALL_RECEIPT_TAG,
        terminal=term,
        complex_name=complex.name,
        num_edges=complex.num_edges,
        residual_weight=wt,
        schedule_status=cert.schedule_status,
        declared_distance=t,
        repair_capacity_t=cap_t,
    )


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
    return CountRepairPacket(count_c1_defects=5, count_repair_d0_capacity=2, count_logical_witness_remain=1)


def incomplete_count_packet() -> CountRepairPacket:
    return CountRepairPacket(count_c1_defects=None, count_repair_d0_capacity=2, count_logical_witness_remain=0)


def illustrative_p_pair() -> tuple[CountRepairPacket, CountRepairPacket]:
    p1 = CountRepairPacket(count_c1_defects=1, count_repair_d0_capacity=2, count_logical_witness_remain=0)
    p2 = CountRepairPacket(count_c1_defects=4, count_repair_d0_capacity=2, count_logical_witness_remain=1)
    return p1, p2


def illustrative_suppression_regime(
    p_pair: tuple[CountRepairPacket, CountRepairPacket]
) -> tuple[CountPacketReceipt, CountPacketReceipt]:
    return terminalize_count_packet(p_pair[0]), terminalize_count_packet(p_pair[1])


def wall_with_audit(packet: ToyRepairPacket) -> PacketWallReceipt:
    return terminalize_packet(packet)


# Aliases for export parity
CountDefectEvent = int
CountPacketReceipt = CountPacketReceipt
CountRepairAction = int
CountRepairPacket = CountRepairPacket
DefectEvent = int
DiagnosticPacket = DiagnosticPacket
PacketMetrics = dict
PacketRefusal = PacketRefusal
PacketWallReceipt = PacketWallReceipt
PacketWallTerminal = PacketWallTerminal
RepairAction = int
ToyRepairPacket = ToyRepairPacket
