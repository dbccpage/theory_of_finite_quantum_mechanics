"""
test_part4_review_remediations.py — Regression & Adversarial Verification Suite
Covering Part 4 Code and Contract Review Findings.

AuthorityEffect: None.
Reference: Part 4 Review Remediation Suite (CT-AUX, Fermionic Hamiltonian, Germ, GIN, Cobordism, Chiral, Anyon)

Claim Hygiene:
1. What this supports:
   - Verification of negative-energy CT-AUX Green's function values against analytical spectral formulas.
   - Verification of full-predicate inverted index intersection in StreamingGinPostingIndex.
   - Verification of weight preservation and duplicate cancellation prevention in streaming involution.
   - Verification of state transition atomicity and carrier naming in primitive difference germ.
   - Verification of integer/envelope admission and boolean string deserialization in fermionic Hamiltonian.
   - Verification of non-spin input refusal and manifold type validation in 5D cobordism anomaly engine.
   - Verification of fail-closed receipts on empty database audits in chiral superconductor bisimulation bridge.
   - Verification of partner uniqueness, weight equality, and opposite sign in fermion GIN index.
2. What this does not support:
   - Universal proof of Monte Carlo sign problem solvability or general continuous anomaly inflows.
3. Narrowest defensible claim:
   - The tested components satisfy their declared discrete error boundaries, refusal gates, and exact numerical formulas.
4. Next test needed:
   - Run multi-step Monte Carlo sampling trajectory with verified CT-AUX Green's functions.
"""

from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
import sys
import numpy as np
import pytest

code_dir = Path(__file__).resolve().parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.bqnf_sign_evaluator import TerminalRoute
from src.fsp.chiral_superconductor_bisimulation_bridge import (
    ChiralSuperconductorBisimulationBridge,
    ChiralSuperconductorReceipt,
)
from src.fsp.chiral_superconductor_evaluator import ChiralSuperconductor3DModel
from src.fsp.cobordism_5d_higher_anomaly import (
    CobordismAnomalyEngine,
    MappingTorusCobordismModel,
)
from src.fsp.ct_aux_streaming_gin_engine import (
    CtAuxConfiguration,
    CtAuxMarkovChainSampler,
    CtAuxVertex,
    StreamingGinPostingIndex,
)
from src.fsp.fermion_boson_germ import DirectedCutD2, GermState, SymmetricLinkS2
from src.fsp.fermion_gin_index import MockFermionGinIndex
from src.fsp.fermionic_hamiltonian import (
    DiscreteFermionicHamiltonian,
    FermionicLattice,
    FockLatticeScalingRow,
)


# ===========================================================================
# 1. CT-AUX Green's Function Remediations
# ===========================================================================

def test_ct_aux_greens_function_negative_energy_exact_magnitude():
    """Independent counterexample verification:
    Single-site model: t=0, mu=5, beta=2 => epsilon = -5.
    Expected equal-time magnitude at tau=0:
        1 - n_F(-5) = 1 / (1 + exp(10)) approx 4.53978687e-5.
    Previous defective branch returned approx 22025.4658.
    """
    sampler = CtAuxMarkovChainSampler(
        num_sites=1,
        beta=2.0,
        t_hopping=0.0,
        mu_chemical_potential=5.0,
        u_interaction=0.0,
    )
    assert sampler.evals[0] == pytest.approx(-5.0, abs=1e-12)

    expected_g0 = 1.0 / (1.0 + math.exp(10.0))
    actual_g0 = sampler.g0(1, 1, 0.0)

    assert actual_g0 == pytest.approx(expected_g0, rel=1e-9)
    assert actual_g0 < 1.0
    assert abs(actual_g0 - 22025.4658) > 22000.0


def test_ct_aux_greens_function_positive_and_zero_energies():
    """Verifies Green's function symmetry and stability for positive and zero energies."""
    sampler_pos = CtAuxMarkovChainSampler(
        num_sites=1,
        beta=2.0,
        t_hopping=0.0,
        mu_chemical_potential=-5.0,
        u_interaction=0.0,
    )
    assert sampler_pos.evals[0] == pytest.approx(5.0, abs=1e-12)
    # For eps > 0, 1 - n_F(eps) = 1.0 / (1.0 + exp(-10.0)) approx 0.9999546
    expected_pos = 1.0 / (1.0 + math.exp(-10.0))
    assert sampler_pos.g0(1, 1, 0.0) == pytest.approx(expected_pos, rel=1e-9)

    sampler_zero = CtAuxMarkovChainSampler(
        num_sites=1,
        beta=2.0,
        t_hopping=0.0,
        mu_chemical_potential=0.0,
        u_interaction=0.0,
    )
    assert sampler_zero.evals[0] == pytest.approx(0.0, abs=1e-12)
    assert sampler_zero.g0(1, 1, 0.0) == pytest.approx(0.5, rel=1e-9)


def test_ct_aux_build_N_matrices_negative_energy_stability():
    """Verifies that build_N_matrices uses the stable negative-energy formulation."""
    sampler = CtAuxMarkovChainSampler(
        num_sites=1,
        beta=2.0,
        t_hopping=0.0,
        mu_chemical_potential=5.0,
        u_interaction=0.0,
    )
    vertices = [CtAuxVertex(site=1, tau=0.5, spin=1)]
    n_up, n_down = sampler.build_N_matrices(vertices)

    assert n_up.shape == (1, 1)
    assert n_down.shape == (1, 1)
    assert math.isfinite(float(n_up[0, 0]))
    assert math.isfinite(float(n_down[0, 0]))
    assert abs(float(n_up[0, 0])) < 100.0


# ===========================================================================
# 2. Streaming GIN Query & Involution Pairing Remediations
# ===========================================================================

def test_streaming_gin_query_all_modes_intersected():
    """Executable counterexample verification:
    Config 1: active modes {1}
    Config 2: active modes {2}
    Query query_by_modes({1, 2}, set()):
    Expected: set() (no configuration satisfies both required modes).
    Defective implementation prematurely broke on len(candidates) <= 1, returning {1}.
    """
    idx = StreamingGinPostingIndex(max_window_size=100)
    cfg1 = CtAuxConfiguration(
        cfg_id=1,
        order=1,
        vertices=(),
        active_modes=frozenset({1}),
        log_weight=0.0,
        weight=1.0,
        sign=1,
        logdet_up=0.0,
        logdet_down=0.0,
    )
    cfg2 = CtAuxConfiguration(
        cfg_id=2,
        order=1,
        vertices=(),
        active_modes=frozenset({2}),
        log_weight=0.0,
        weight=1.0,
        sign=1,
        logdet_up=0.0,
        logdet_down=0.0,
    )
    idx.insert_configuration(cfg1)
    idx.insert_configuration(cfg2)

    result = idx.query_by_modes(required_modes={1, 2}, forbidden_modes=set())
    assert result == set(), f"Expected set(), got {result}"


def test_streaming_gin_involution_weight_preservation():
    """Counterexample verification:
    Config 1: modes {1}, sign +1, weight 1.0
    Config 2: modes {2}, sign -1, weight 4.0
    Query find_streaming_involution_partner(1, {1, 2}):
    Must refuse pairing because weights are unequal (1.0 vs 4.0).
    """
    idx = StreamingGinPostingIndex(max_window_size=100)
    cfg1 = CtAuxConfiguration(
        cfg_id=1,
        order=1,
        vertices=(),
        active_modes=frozenset({1}),
        log_weight=0.0,
        weight=1.0,
        sign=1,
        logdet_up=0.0,
        logdet_down=0.0,
    )
    cfg2 = CtAuxConfiguration(
        cfg_id=2,
        order=1,
        vertices=(),
        active_modes=frozenset({2}),
        log_weight=0.0,
        weight=4.0,
        sign=-1,
        logdet_up=0.0,
        logdet_down=0.0,
    )
    idx.insert_configuration(cfg1)
    idx.insert_configuration(cfg2)

    partner = idx.find_streaming_involution_partner(1, {1, 2})
    assert partner is None, f"Expected None due to weight mismatch, got {partner}"


def test_streaming_gin_duplicate_cancellation_prevention():
    """Counterexample verification:
    Calling register_involution_cancellation(1, 2) repeatedly must not double-decrement
    or increment paired_partners_count multiple times.
    """
    idx = StreamingGinPostingIndex(max_window_size=100)
    cfg1 = CtAuxConfiguration(
        cfg_id=1,
        order=1,
        vertices=(),
        active_modes=frozenset({1}),
        log_weight=0.0,
        weight=1.0,
        sign=1,
        logdet_up=0.0,
        logdet_down=0.0,
    )
    cfg2 = CtAuxConfiguration(
        cfg_id=2,
        order=1,
        vertices=(),
        active_modes=frozenset({2}),
        log_weight=0.0,
        weight=1.0,
        sign=-1,
        logdet_up=0.0,
        logdet_down=0.0,
    )
    idx.insert_configuration(cfg1)
    idx.insert_configuration(cfg2)

    d1 = idx.register_involution_cancellation(1, 2)
    assert d1 == pytest.approx(0.0, abs=1e-12)
    assert idx.paired_partners_count == 1

    d2 = idx.register_involution_cancellation(1, 2)
    assert d2 == 0.0
    assert idx.paired_partners_count == 1, "Duplicate cancellation must not increment paired count"


def test_streaming_gin_index_invalid_window_size():
    """Verifies that max_window_size <= 0 is refused with ValueError."""
    with pytest.raises(ValueError, match="must be a positive integer"):
        StreamingGinPostingIndex(max_window_size=0)
    with pytest.raises(ValueError, match="must be a positive integer"):
        StreamingGinPostingIndex(max_window_size=-10)


def test_streaming_gin_index_duplicate_cfg_id():
    """Verifies that duplicate cfg_id is refused in active window."""
    idx = StreamingGinPostingIndex(max_window_size=10)
    cfg = CtAuxConfiguration(
        cfg_id=1,
        order=1,
        vertices=(),
        active_modes=frozenset({1}),
        log_weight=0.0,
        weight=1.0,
        sign=1,
        logdet_up=0.0,
        logdet_down=0.0,
    )
    idx.insert_configuration(cfg)
    with pytest.raises(ValueError, match="already exists"):
        idx.insert_configuration(cfg)


# ===========================================================================
# 3. Fermion-Boson Germ Remediations
# ===========================================================================

def test_germ_state_transition_atomicity_on_self_loop_failure():
    """Counterexample verification:
    Calling step_03_directed_cut('x', 'x') fails irreflexivity.
    The state MUST NOT be mutated (stage must remain 0, carrier empty).
    """
    germ = GermState()
    assert germ.stage == 0
    assert germ.carrier == set()
    assert germ.relations == set()

    with pytest.raises(ValueError, match="Diagonal self-loop refused"):
        germ.step_03_directed_cut("x", "x")

    assert germ.stage == 0, f"Expected stage 0, got {germ.stage}"
    assert germ.carrier == set(), f"Expected empty carrier, got {germ.carrier}"
    assert germ.relations == set(), f"Expected empty relations, got {germ.relations}"


def test_germ_state_unmarked_pair_distinct_loci():
    """Verifies that step_02_unmarked_pair refuses identical loci."""
    germ = GermState()
    with pytest.raises(ValueError, match="Unmarked pair requires distinct loci"):
        germ.step_02_unmarked_pair("z", "z")


def test_germ_automorphism_groups_use_dynamic_carriers():
    """Verifies that automorphism groups use the instance's carrier symbols."""
    d = DirectedCutD2(source="x", target="y")
    assert d.automorphism_group() == [{"x": "x", "y": "y"}]

    sym = SymmetricLinkS2(endpoint1="u", endpoint2="v")
    aut = sym.automorphism_group()
    assert len(aut) == 2
    assert {"u": "u", "v": "v"} in aut
    assert {"u": "v", "v": "u"} in aut


# ===========================================================================
# 4. Fermionic Hamiltonian Remediations
# ===========================================================================

def test_fermionic_lattice_rejects_booleans_and_huge_envelope():
    """Counterexample verification:
    FermionicLattice(True, []) must be rejected with ValueError.
    Edge endpoints with booleans must be rejected with TypeError.
    Sites exceeding finite envelope (> 32) must be rejected.
    """
    with pytest.raises(ValueError, match="positive integer"):
        FermionicLattice(True, [])

    with pytest.raises(ValueError, match="positive integer"):
        FermionicLattice(False, [])

    with pytest.raises(TypeError, match="Edge endpoints must be integers"):
        FermionicLattice(4, [(True, 1)])

    with pytest.raises(ValueError, match="exceeds maximum finite lattice envelope"):
        FermionicLattice(33, [])


def test_discrete_fermionic_hamiltonian_rejects_bool_counts():
    """Verifies particle counts cannot be booleans."""
    lat = FermionicLattice.linear_chain(2)
    with pytest.raises(TypeError, match="Fermion particle counts must be integers"):
        DiscreteFermionicHamiltonian(lat, num_up=True, num_down=0)

    with pytest.raises(TypeError, match="Fermion particle counts must be integers"):
        DiscreteFermionicHamiltonian(lat, num_up=0, num_down=False)


def test_fock_scaling_row_boolean_string_deserialization():
    """Counterexample verification:
    FockLatticeScalingRow.from_dict() with 'False' string must produce False, not True.
    """
    data_false = {
        "label": "test_chain",
        "num_sites": 2,
        "num_edges": 1,
        "num_up": 1,
        "num_down": 0,
        "fock_dim": 2,
        "trotter_steps": 2,
        "z_fermionic": "1",
        "z_bosonic": "1",
        "average_sign": "1",
        "has_sign_cancellation": "False",
    }
    row_false = FockLatticeScalingRow.from_dict(data_false)
    assert row_false.has_sign_cancellation is False

    data_false_lower = dict(data_false)
    data_false_lower["has_sign_cancellation"] = "false"
    assert FockLatticeScalingRow.from_dict(data_false_lower).has_sign_cancellation is False

    data_true = dict(data_false)
    data_true["has_sign_cancellation"] = "True"
    assert FockLatticeScalingRow.from_dict(data_true).has_sign_cancellation is True


# ===========================================================================
# 5. 5D Cobordism Higher Anomaly Remediations
# ===========================================================================

def test_cobordism_anomaly_refuses_non_spin_orientable():
    """Counterexample verification:
    Supplying MappingTorusCobordismModel(is_spin=False, is_orientable=True)
    must route to TerminalRoute.REFUSED with zero average sign.
    Defective implementation returned nu_5 = 0, ExactRepair, average_sign = 1.0.
    """
    model = MappingTorusCobordismModel(
        four_manifold_type="T4",
        is_spin=False,
        is_orientable=True,
    )
    receipt = CobordismAnomalyEngine.audit_cobordism_anomaly(model)
    assert receipt.terminal_route == TerminalRoute.REFUSED
    assert receipt.average_sign_gin == 0.0


def test_cobordism_anomaly_refuses_unrecognized_manifold_type():
    """Verifies that unrecognized four_manifold_type is rejected."""
    with pytest.raises(ValueError, match="Unrecognized four_manifold_type"):
        MappingTorusCobordismModel(four_manifold_type="NonExistent4Manifold")


# ===========================================================================
# 6. Chiral Superconductor Bisimulation Bridge Remediations
# ===========================================================================

def test_chiral_superconductor_bridge_empty_audits_fail_closed():
    """Counterexample verification:
    When arc or inflow audit tables are unpopulated, emit_receipt must fail closed
    with lean_bisimulation_passed = False and typed missing-data statuses.
    """
    model = ChiralSuperconductor3DModel(
        lattice_id="empty_audit_test",
        lx=4,
        ly=4,
        lz=8,
        k0=0.5 * math.pi,
        delta_0=0.3,
        mu=0.0,
        phs_symmetric=True,
    )
    bridge = ChiralSuperconductorBisimulationBridge()
    # Intentionally do NOT call bridge.populate_from_model(model)
    receipt = bridge.emit_receipt(model)

    assert receipt.majorana_status == "NO_MAJORANA_ARCS_RECORDED"
    assert receipt.inflow_verdict == "NO_INFLOW_AUDIT_ROWS"
    assert receipt.lean_bisimulation_passed is False


# ===========================================================================
# 7. Fermion GIN Index Remediations
# ===========================================================================

def test_fermion_gin_index_partner_unambiguous_and_equal_weight():
    """Counterexample verification:
    find_involution_partner must verify equal weight, opposite sign, and partner uniqueness.
    """
    gin = MockFermionGinIndex(in_memory=True)
    # Source: cfg 1, modes {1, 4}, weight 1.0, sign +1
    gin.index_configuration(1, "TestModel", {1, 4}, 4, 1.0, 1, 1)

    # Candidate with wrong weight: cfg 2, modes {2, 4}, weight 4.0, sign -1
    gin.index_configuration(2, "TestModel", {2, 4}, 4, 4.0, -1, 1)

    # Partner lookup must return None because weights differ
    partner_mismatch = gin.find_involution_partner(cfg_id=1, flip_modes={1, 2}, total_modes=4)
    assert partner_mismatch is None

    # Now add candidate with matching weight and opposite sign: cfg 3, modes {2, 4}, weight 1.0, sign -1
    gin.index_configuration(3, "TestModel", {2, 4}, 4, 1.0, -1, 1)
    partner_valid = gin.find_involution_partner(cfg_id=1, flip_modes={1, 2}, total_modes=4)
    assert partner_valid == 3

    # Now add duplicate matching candidate: cfg 4, modes {2, 4}, weight 1.0, sign -1
    gin.index_configuration(4, "TestModel", {2, 4}, 4, 1.0, -1, 1)
    partner_ambiguous = gin.find_involution_partner(cfg_id=1, flip_modes={1, 2}, total_modes=4)
    assert partner_ambiguous is None, "Ambiguous multiple candidates must return None"
    gin.close()
