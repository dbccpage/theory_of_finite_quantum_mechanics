"""
test_chiral_superconductor_bisimulation.py — Pytest suite for 3D Chiral Topological Superconductor.

AuthorityEffect: None.
"""

import math
from pathlib import Path
import sys
import pytest

code_dir = Path(__file__).resolve().parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.chiral_superconductor_evaluator import (
    ChiralSuperconductor3DModel,
    MockChiralSuperconductorGinIndex,
    ChiralSuperconductorEvaluationResult,
)
from src.fsp.chiral_superconductor_bisimulation_bridge import (
    ChiralSuperconductorBisimulationBridge,
    ChiralSuperconductorReceipt,
)


@pytest.fixture
def clean_model():
    return ChiralSuperconductor3DModel(
        lattice_id="weyl_sc_test_01",
        lx=8,
        ly=8,
        lz=16,
        k0=0.5 * math.pi,
        delta_0=0.3,
        mu=0.0,
        phs_symmetric=True,
    )


def test_weyl_nodes_nielsen_ninomiya_cancellation(clean_model):
    model = clean_model
    assert len(model.nodes) == 2
    n_pos = [n for n in model.nodes if n.chirality == 1][0]
    n_neg = [n for n in model.nodes if n.chirality == -1][0]

    assert pytest.approx(n_pos.kz, rel=1e-5) == model.k0
    assert pytest.approx(n_neg.kz, rel=1e-5) == -model.k0
    assert sum(n.chirality for n in model.nodes) == 0


def test_kz_slice_chern_numbers(clean_model):
    model = clean_model
    assert len(model.slices) == 16

    topo_slices = [s for s in model.slices if s.chern_number == 1]
    trivial_slices = [s for s in model.slices if s.chern_number == 0]

    assert len(topo_slices) > 0
    assert len(trivial_slices) > 0

    # All topological slices must lie strictly within (-k0, k0)
    for s in topo_slices:
        assert abs(s.kz_val) < model.k0


def test_surface_majorana_fermi_arcs(clean_model):
    model = clean_model
    assert len(model.arcs) == 2

    top_arc = [a for a in model.arcs if a.surface_orientation == "TOP"][0]
    bottom_arc = [a for a in model.arcs if a.surface_orientation == "BOTTOM"][0]

    assert pytest.approx(top_arc.arc_length, rel=1e-5) == 2.0 * model.k0
    assert pytest.approx(bottom_arc.arc_length, rel=1e-5) == 2.0 * model.k0
    assert top_arc.is_self_conjugate == 1
    assert bottom_arc.is_self_conjugate == 1
    assert top_arc.spectral_residual == 0.0


def test_callan_harvey_anomaly_inflow_conservation(clean_model):
    model = clean_model
    assert len(model.spectral_trajectory) == 9 # 8 steps + 0

    for step in model.spectral_trajectory:
        assert step.net_anomaly == 0
        assert step.bulk_pumped_charge + step.surface_pumped_charge == step.net_anomaly


def test_gin_index_inverted_postings(clean_model):
    model = clean_model
    gin = model.gin_index

    chiral_plus = gin.search_postings("CHIRAL_PLUS")
    assert len(chiral_plus) == 1
    assert chiral_plus[0] == f"{model.lattice_id}_node_pos"

    chiral_minus = gin.search_postings("CHIRAL_MINUS")
    assert len(chiral_minus) == 1
    assert chiral_minus[0] == f"{model.lattice_id}_node_neg"

    topo_slices = gin.search_postings("TOPOLOGICAL_SLICE")
    assert len(topo_slices) == len([s for s in model.slices if s.chern_number == 1])

    top_arcs = gin.search_postings("SURFACE_TOP")
    assert len(top_arcs) == 1
    assert top_arcs[0] == f"{model.lattice_id}_arc_top"

    self_conjugate = gin.search_postings("SELF_CONJUGATE")
    assert len(self_conjugate) == 2


def test_ansi_sql_views_audit_clean(clean_model):
    model = clean_model
    bridge = ChiralSuperconductorBisimulationBridge()
    bridge.populate_from_model(model)

    anomaly_dict = bridge.audit_chiral_anomaly()
    assert anomaly_dict["anomaly_status"] == "ANOMALY_CANCELLED_VALID"
    assert anomaly_dict["net_chirality"] == 0
    assert anomaly_dict["total_nodes"] == 2

    flow_dict = bridge.audit_surface_bulk_spectral_flow()
    assert flow_dict["bulk_boundary_status"] == "BULK_BOUNDARY_MATCH"
    assert flow_dict["recorded_arcs"] == 2
    assert flow_dict["expected_total_arcs"] == 2

    arc_rows = bridge.audit_majorana_arcs()
    assert len(arc_rows) == 2
    assert all(a["majorana_status"] == "MAJORANA_SELF_CONJUGATE_VALID" for a in arc_rows)

    inflow_rows = bridge.audit_anomaly_inflow()
    assert len(inflow_rows) == 9
    assert all(i["inflow_verdict"] == "ANOMALY_INFLOW_CONSERVED" for i in inflow_rows)

    route = bridge.audit_terminal_route()
    assert route == "REPAIR"


def test_unpaired_weyl_node_negative_control(clean_model):
    model = clean_model
    model.inject_unpaired_weyl_node(chirality=1)

    bridge = ChiralSuperconductorBisimulationBridge()
    bridge.populate_from_model(model)

    anomaly_dict = bridge.audit_chiral_anomaly()
    assert anomaly_dict["anomaly_status"] == "CHIRAL_ANOMALY_DEFECT"
    assert anomaly_dict["net_chirality"] != 0

    route = bridge.audit_terminal_route()
    assert route == "SPLIT_BRAIN_REFUSAL"


def test_missing_surface_arc_bulk_boundary_discrepancy(clean_model):
    model = clean_model
    model.remove_surface_arc()

    bridge = ChiralSuperconductorBisimulationBridge()
    bridge.populate_from_model(model)

    flow_dict = bridge.audit_surface_bulk_spectral_flow()
    assert flow_dict["bulk_boundary_status"] == "BULK_BOUNDARY_DISCREPANCY"
    assert flow_dict["recorded_arcs"] == 1

    route = bridge.audit_terminal_route()
    assert route == "SPLIT_BRAIN_REFUSAL"


def test_broken_particle_hole_symmetry_negative_control(clean_model):
    model = clean_model
    model.break_particle_hole_symmetry()

    bridge = ChiralSuperconductorBisimulationBridge()
    bridge.populate_from_model(model)

    arc_rows = bridge.audit_majorana_arcs()
    assert any(a["majorana_status"] == "MAJORANA_SYMMETRY_DEFECT" for a in arc_rows)

    route = bridge.audit_terminal_route()
    assert route == "CLOSURE_FAILURE"


def test_anomaly_inflow_leakage_negative_control(clean_model):
    model = clean_model
    model.inject_inflow_anomaly(delta_anomaly=1)

    bridge = ChiralSuperconductorBisimulationBridge()
    bridge.populate_from_model(model)

    inflow_rows = bridge.audit_anomaly_inflow()
    assert any(i["inflow_verdict"] == "INFLOW_LEAKAGE_DEFECT" for i in inflow_rows)

    route = bridge.audit_terminal_route()
    assert route == "SPLIT_BRAIN_REFUSAL"


def test_receipt_emission_and_lean_bisimulation(clean_model):
    model = clean_model
    bridge = ChiralSuperconductorBisimulationBridge()
    bridge.populate_from_model(model)
    receipt = bridge.emit_receipt(model)

    assert isinstance(receipt, ChiralSuperconductorReceipt)
    assert receipt.total_bulk_nodes == 2
    assert receipt.net_chirality == 0
    assert receipt.anomaly_status == "ANOMALY_CANCELLED_VALID"
    assert receipt.recorded_arcs == 2
    assert receipt.bulk_boundary_status == "BULK_BOUNDARY_MATCH"
    assert receipt.majorana_status == "MAJORANA_SELF_CONJUGATE_VALID"
    assert receipt.inflow_verdict == "ANOMALY_INFLOW_CONSERVED"
    assert receipt.terminal_route == "REPAIR"
    assert receipt.lean_bisimulation_passed is True
    assert receipt.authority_effect == "None"
