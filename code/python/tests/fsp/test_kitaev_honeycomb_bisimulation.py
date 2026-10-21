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
    assert len(model.sites) == 18
    assert len(model.links) == 27
    assert len(model.plaquettes) == 9

    a_sites = [s for s in model.sites.values() if s.sublattice == "A"]
    b_sites = [s for s in model.sites.values() if s.sublattice == "B"]
    assert len(a_sites) == 9
    assert len(b_sites) == 9


def test_gin_index_inverted_postings(clean_torus_model):
    model = clean_torus_model
    gin = model.gin_index

    for l_id, p_list in gin.link_to_plaquettes.items():
        assert len(p_list) == 2, f"Link {l_id} should belong to 2 plaquettes, got {len(p_list)}"

    assert len(gin.get_vortices()) == 0

    sample_link = list(model.links.keys())[0]
    gin.flip_link(sample_link)
    vortices = gin.get_vortices()
    assert len(vortices) == 2
    assert set(vortices) == set(gin.link_to_plaquettes[sample_link])

    gin.flip_link(sample_link)
    assert len(gin.get_vortices()) == 0


def test_vortex_free_ground_state(clean_torus_model):
    model = clean_torus_model
    bridge = KitaevHoneycombBisimulationBridge()
    bridge.populate_from_model(model, time_steps=3, simulate_braid=False)

    plaq_audits = bridge.audit_plaquette_fluxes()
    assert len(plaq_audits) == 9
    assert all(r["audit_status"] == "FLUX_CONSISTENT" for r in plaq_audits)
    assert all(r["recorded_wp"] == 1 for r in plaq_audits)

    flux_summary = bridge.audit_total_flux()
    assert flux_summary["total_vortices"] == 0
    assert flux_summary["parity_audit_verdict"] == "FLUX_PARITY_VALID"

    parity_audits = bridge.audit_matter_parity()
    assert len(parity_audits) == 3
    assert all(r["conservation_verdict"] == "PARITY_CONSERVED" for r in parity_audits)

    route = bridge.audit_terminal_route()
    assert route == "REPAIR"


def test_vortex_pair_creation_and_parity(clean_torus_model):
    model = clean_torus_model
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
    assert len(braid_audits) == 2

    vac_braid = [b for b in braid_audits if b["enclosed_parity"] == 0][0]
    ferm_braid = [b for b in braid_audits if b["enclosed_parity"] == 1][0]

    assert pytest.approx(vac_braid["berry_phase_rad"], 1e-5) == -math.pi / 4.0
    assert vac_braid["phase_status"] == "ISING_BRAIDING_CERTIFIED"
    assert vac_braid["terminal_route"] == "REPAIR"

    assert pytest.approx(ferm_braid["berry_phase_rad"], 1e-5) == 3.0 * math.pi / 4.0
    assert ferm_braid["phase_status"] == "ISING_BRAIDING_CERTIFIED"
    assert ferm_braid["terminal_route"] == "REPAIR"


def test_odd_flux_anomaly_negative_control(clean_torus_model):
    model = clean_torus_model
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


def test_pfaffian_parity_sign_flip_counterexample():
    """Verifies that fermion parity correctly tracks true Pfaffian sign changes.

    Counterexample test from audit: 2x2 lattice with Jx=0.7, Jy=1.1, Jz=1.9, kappa=0.0.
    Initial state: Pf ≈ +1.2765 -> parity +1.
    Flipped link_z_0_0: Pf ≈ -12.5137 -> parity -1.
    """
    model = KitaevHoneycombModel(
        lattice_id="honeycomb_2x2_pfaffian_test",
        lx=2,
        ly=2,
        boundary_condition="TORUS",
        jx=0.7,
        jy=1.1,
        jz=1.9,
        kappa=0.0,
    )
    A_init = model.compute_majorana_hamiltonian()
    pf_init = model.compute_pfaffian(A_init)
    assert pytest.approx(pf_init, 1e-4) == 1.2765
    assert model.compute_fermion_parity() == 1

    model.gin_index.flip_link("link_z_0_0")
    A_flipped = model.compute_majorana_hamiltonian()
    pf_flipped = model.compute_pfaffian(A_flipped)
    assert pytest.approx(pf_flipped, 1e-4) == -12.5137
    assert model.compute_fermion_parity() == -1


def test_braid_validation_negative_controls(clean_torus_model):
    """Verifies fail-closed input validation for vortex braiding simulation."""
    model = clean_torus_model
    with pytest.raises(ValueError, match="vortex_a 'nonexistent_a' not found"):
        model.simulate_vortex_braid("nonexistent_a", "p_0_0", enclosed_parity=0)

    p_first = list(model.plaquettes.keys())[0]
    with pytest.raises(ValueError, match="vortex_b 'nonexistent_b' not found"):
        model.simulate_vortex_braid(p_first, "nonexistent_b", enclosed_parity=0)

    with pytest.raises(ValueError, match="enclosed_parity must be in {0, 1}"):
        model.simulate_vortex_braid(p_first, p_first, enclosed_parity=99)

