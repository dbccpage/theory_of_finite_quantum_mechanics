"""
test_kitaev_honeycomb_bisimulation.py — Pytest suite for 2D Honeycomb Kitaev Spin Liquid.

AuthorityEffect: None.
"""

import math
from pathlib import Path
import sys
import pytest

code_dir = Path(__file__).resolve().parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.kitaev_honeycomb_evaluator import KitaevHoneycombModel, MockHoneycombGinIndex
from src.fsp.kitaev_honeycomb_bisimulation_bridge import (
    KitaevHoneycombBisimulationBridge,
    KitaevHoneycombReceipt,
)


@pytest.fixture
def clean_torus_model():
    return KitaevHoneycombModel(
        lattice_id="honeycomb_3x3_torus",
        lx=3,
        ly=3,
        boundary_condition="TORUS",
        jx=1.0,
        jy=1.0,
        jz=1.0,
        kappa=0.1,
    )


def test_honeycomb_lattice_construction(clean_torus_model):
    model = clean_torus_model
    # 3x3 cells, 2 sites per cell = 18 sites
    assert len(model.sites) == 18
    # 3 links per cell = 27 links
    assert len(model.links) == 27
    # 1 hexagon per cell = 9 plaquettes
    assert len(model.plaquettes) == 9

    # Check bipartite partition: 9 A sites and 9 B sites
    a_sites = [s for s in model.sites.values() if s.sublattice == "A"]
    b_sites = [s for s in model.sites.values() if s.sublattice == "B"]
    assert len(a_sites) == 9
    assert len(b_sites) == 9


def test_gin_index_inverted_postings(clean_torus_model):
    model = clean_torus_model
    gin = model.gin_index

    # On a torus, each link must belong to exactly 2 hexagonal plaquettes
    for l_id, p_list in gin.link_to_plaquettes.items():
        assert len(p_list) == 2, f"Link {l_id} should belong to 2 plaquettes, got {len(p_list)}"

    # Initially vortex-free
    assert len(gin.get_vortices()) == 0

    # Flip one link -> exactly 2 adjacent plaquettes become vortices
    sample_link = list(model.links.keys())[0]
    gin.flip_link(sample_link)
    vortices = gin.get_vortices()
    assert len(vortices) == 2
    assert set(vortices) == set(gin.link_to_plaquettes[sample_link])

    # Flip it back -> 0 vortices
    gin.flip_link(sample_link)
    assert len(gin.get_vortices()) == 0


def test_vortex_free_ground_state(clean_torus_model):
    model = clean_torus_model
    bridge = KitaevHoneycombBisimulationBridge()
    bridge.populate_from_model(model, time_steps=3, simulate_braid=False)

    # Plaquette audit
    plaq_audits = bridge.audit_plaquette_fluxes()
    assert len(plaq_audits) == 9
    assert all(r["audit_status"] == "FLUX_CONSISTENT" for r in plaq_audits)
    assert all(r["recorded_wp"] == 1 for r in plaq_audits)

    # Flux audit
    flux_summary = bridge.audit_total_flux()
    assert flux_summary["total_vortices"] == 0
    assert flux_summary["parity_audit_verdict"] == "FLUX_PARITY_VALID"

    # Parity audit
    parity_audits = bridge.audit_matter_parity()
    assert len(parity_audits) == 3
    assert all(r["conservation_verdict"] == "PARITY_CONSERVED" for r in parity_audits)

    # Terminal route: REPAIR
    route = bridge.audit_terminal_route()
    assert route == "REPAIR"


def test_vortex_pair_creation_and_parity(clean_torus_model):
    model = clean_torus_model
    # Flip a link to create an even pair of vortices
    sample_link = "link_z_0_0"
    model.gin_index.flip_link(sample_link)
    assert len(model.gin_index.get_vortices()) == 2

    bridge = KitaevHoneycombBisimulationBridge()
    bridge.populate_from_model(model, time_steps=3, simulate_braid=True)

    flux_summary = bridge.audit_total_flux()
    assert flux_summary["total_vortices"] == 2
    assert flux_summary["vortex_parity_mod2"] == 0
    assert flux_summary["parity_audit_verdict"] == "FLUX_PARITY_VALID"

    route = bridge.audit_terminal_route()
    assert route == "REPAIR"


def test_nonabelian_ising_braiding_phases(clean_torus_model):
    model = clean_torus_model
    sample_link = "link_z_1_1"
    model.gin_index.flip_link(sample_link)

    bridge = KitaevHoneycombBisimulationBridge()
    bridge.populate_from_model(model, time_steps=3, simulate_braid=True)

    braid_audits = bridge.audit_braiding()
    assert len(braid_audits) == 2  # vacuum channel (0) and fermion channel (1)

    vac_braid = [b for b in braid_audits if b["enclosed_parity"] == 0][0]
    ferm_braid = [b for b in braid_audits if b["enclosed_parity"] == 1][0]

    # Vacuum channel: -pi/4
    assert pytest.approx(vac_braid["berry_phase_rad"], 1e-5) == -math.pi / 4.0
    assert vac_braid["phase_status"] == "ISING_BRAIDING_CERTIFIED"
    assert vac_braid["terminal_route"] == "REPAIR"

    # Fermion channel: 3pi/4 = -pi/4 + pi
    assert pytest.approx(ferm_braid["berry_phase_rad"], 1e-5) == 3.0 * math.pi / 4.0
    assert ferm_braid["phase_status"] == "ISING_BRAIDING_CERTIFIED"
    assert ferm_braid["terminal_route"] == "REPAIR"


def test_odd_flux_anomaly_negative_control(clean_torus_model):
    model = clean_torus_model
    # Directly corrupt one plaquette flux to simulate an unclosed monopolar flux defect
    p_id = list(model.plaquettes.keys())[0]
    model.plaquettes[p_id].flux_wp = -1
    model.plaquettes[p_id].vortex_charge = 1

    bridge = KitaevHoneycombBisimulationBridge()
    bridge.populate_from_model(model, time_steps=3, simulate_braid=False)

    flux_summary = bridge.audit_total_flux()
    assert flux_summary["total_vortices"] == 1
    assert flux_summary["vortex_parity_mod2"] == 1
    assert flux_summary["parity_audit_verdict"] == "FLUX_PARITY_ANOMALY"

    route = bridge.audit_terminal_route()
    assert route == "SPLIT_BRAIN_REFUSAL"


def test_fermion_parity_flip_negative_control(clean_torus_model):
    model = clean_torus_model
    bridge = KitaevHoneycombBisimulationBridge()
    # Force parity flip at time step 2
    bridge.populate_from_model(model, time_steps=4, force_parity_flip_at=2, simulate_braid=False)

    parity_audits = bridge.audit_matter_parity()
    leakage_rows = [r for r in parity_audits if r["conservation_verdict"] == "PARITY_LEAKAGE_DEFECT"]
    assert len(leakage_rows) > 0

    route = bridge.audit_terminal_route()
    assert route == "SPLIT_BRAIN_REFUSAL"


def test_gauge_projector_violation_negative_control(clean_torus_model):
    model = clean_torus_model
    bridge = KitaevHoneycombBisimulationBridge()
    bridge.populate_from_model(model, time_steps=3, gauge_projector_valid=False, simulate_braid=False)

    parity_audits = bridge.audit_matter_parity()
    assert all(r["conservation_verdict"] == "GAUGE_PROJECTOR_DEFECT" for r in parity_audits)

    route = bridge.audit_terminal_route()
    assert route == "CLOSURE_FAILURE"


def test_receipt_emission_and_bisimulation(clean_torus_model):
    model = clean_torus_model
    # Normal vortex-pair state
    model.gin_index.flip_link("link_x_0_1")

    bridge = KitaevHoneycombBisimulationBridge()
    bridge.populate_from_model(model, time_steps=3, simulate_braid=True)
    receipt = bridge.emit_receipt(model)

    assert isinstance(receipt, KitaevHoneycombReceipt)
    assert receipt.total_vortices == 2
    assert receipt.flux_parity_status == "FLUX_PARITY_VALID"
    assert receipt.matter_parity_status == "PARITY_CONSERVED"
    assert receipt.braiding_certified is True
    assert receipt.terminal_route == "REPAIR"
    assert receipt.lean_bisimulation_passed is True
    assert receipt.authority_effect == "None"
