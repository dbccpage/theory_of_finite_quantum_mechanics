"""HARD invariant battery for repair-capacity / LGGR / packet-wall demos.

AuthorityEffect: None (diagnostic only).
"""

from __future__ import annotations

from .complexes import (
    closed_residual_syndrome_example,
    exact_syndrome_example,
    open_syndrome_example,
    plaquette,
    prism,
    surface_exact_from_vertex0,
    surface_grid_2x2_planar,
    surface_grid_2x2_torus,
    surface_open_single_edge_example,
    torus_logical_x_example,
    triangle,
    ChainComplexGf2,
)
from .gf2_terminalizer import (
    GF2Matrix,
    GF2ScheduleStatus,
    Gf2CocycleClassifier,
    AUTHORITY_FENCE,
)
from .packet_wall import (
    PacketWallTerminal,
    ToyRepairPacket,
    terminalize_packet,
)
from .repair_limit import (
    homology_distance,
    is_closed,
    lggr_demo_on,
    repair_capacity_bound,
)


def stock_complexes() -> list[ChainComplexGf2]:
    return [
        triangle(),
        plaquette(),
        prism(),
        surface_grid_2x2_planar(),
        surface_grid_2x2_torus(),
    ]


def inv1_all_stock_complexes_satisfy_d1_d0_zero() -> bool:
    for c in stock_complexes():
        if not c.verify_boundary():
            return False
        if not Gf2CocycleClassifier.verify_boundary(c.d0, c.d1):
            return False
    return True


def inv1_broken_boundary_refuses_terminalize() -> bool:
    c = triangle()
    bad_d1 = GF2Matrix.from_data([[1, 0, 0]])
    if Gf2CocycleClassifier.verify_boundary(c.d0, bad_d1):
        return False
    try:
        Gf2CocycleClassifier.classify(c.d0, bad_d1, [1, 0, 0])
        return False
    except ValueError:
        return True


def inv2_torus_exhibits_closed_residual_auth_none() -> bool:
    c = surface_grid_2x2_torus()
    omega = torus_logical_x_example()
    cert = Gf2CocycleClassifier.classify(c.d0, c.d1, omega)
    return (
        cert.schedule_status == GF2ScheduleStatus.ClosedResidual
        and cert.authority_effect == "None"
    )


def inv3_repair_capacity_matches_a_hand_table() -> bool:
    table = [
        (1, 0),
        (2, 0),
        (3, 1),
        (4, 1),
        (5, 2),
        (6, 2),
        (7, 3),
        (8, 3),
    ]
    for d, expected_t in table:
        if repair_capacity_bound(d) != expected_t:
            return False
    return True


def inv4_exact_is_not_lggr_and_open_is_not_lggr() -> bool:
    c = triangle()
    omega_exact = surface_exact_from_vertex0(c)
    lg_exact = lggr_demo_on(c, omega_exact)
    if lg_exact.is_lggr:
        return False

    omega_open = open_syndrome_example()
    lg_open = lggr_demo_on(c, omega_open)
    if lg_open.is_lggr:
        return False
    return True


def inv4_lggr_local_green_global_red_on_torus() -> bool:
    c = surface_grid_2x2_torus()
    omega = torus_logical_x_example()
    report = lggr_demo_on(c, omega)
    return report.local_green and report.global_red and report.is_lggr


def inv5_weight_zero_always_exact_on_all_stock() -> bool:
    for c in stock_complexes():
        zero = [0] * c.num_edges
        cert = Gf2CocycleClassifier.classify(c.d0, c.d1, zero)
        if cert.schedule_status != GF2ScheduleStatus.Exact:
            return False
    return True


def inv6_single_edge_open_on_torus_and_planar() -> bool:
    c_torus = surface_grid_2x2_torus()
    omega_torus = surface_open_single_edge_example()
    cert_torus = Gf2CocycleClassifier.classify(c_torus.d0, c_torus.d1, omega_torus)
    if cert_torus.schedule_status != GF2ScheduleStatus.OpenObstruction:
        return False

    c_planar = surface_grid_2x2_planar()
    omega_planar = [1] + [0] * (c_planar.num_edges - 1)
    cert_planar = Gf2CocycleClassifier.classify(c_planar.d0, c_planar.d1, omega_planar)
    if cert_planar.schedule_status != GF2ScheduleStatus.OpenObstruction:
        return False
    return True


def inv7_every_receipt_authority_effect_is_exactly_none() -> bool:
    c = triangle()
    receipt = Gf2CocycleClassifier.classify(c.d0, c.d1, [0, 0, 0])
    return receipt.authority_effect == "None"


def inv8_incomplete_packet_refuses() -> bool:
    packet = ToyRepairPacket(complex=None, residual=None)
    receipt = terminalize_packet(packet)
    return receipt.terminal == PacketWallTerminal.IncompleteRefusal


def run_all_hard_invariants() -> dict[str, bool]:
    results = {
        "inv1_all_stock_complexes_satisfy_d1_d0_zero": inv1_all_stock_complexes_satisfy_d1_d0_zero(),
        "inv1_broken_boundary_refuses_terminalize": inv1_broken_boundary_refuses_terminalize(),
        "inv2_torus_exhibits_closed_residual_auth_none": inv2_torus_exhibits_closed_residual_auth_none(),
        "inv3_repair_capacity_matches_a_hand_table": inv3_repair_capacity_matches_a_hand_table(),
        "inv4_exact_is_not_lggr_and_open_is_not_lggr": inv4_exact_is_not_lggr_and_open_is_not_lggr(),
        "inv4_lggr_local_green_global_red_on_torus": inv4_lggr_local_green_global_red_on_torus(),
        "inv5_weight_zero_always_exact_on_all_stock": inv5_weight_zero_always_exact_on_all_stock(),
        "inv6_single_edge_open_on_torus_and_planar": inv6_single_edge_open_on_torus_and_planar(),
        "inv7_every_receipt_authority_effect_is_exactly_none": inv7_every_receipt_authority_effect_is_exactly_none(),
        "inv8_incomplete_packet_refuses": inv8_incomplete_packet_refuses(),
    }
    return results
