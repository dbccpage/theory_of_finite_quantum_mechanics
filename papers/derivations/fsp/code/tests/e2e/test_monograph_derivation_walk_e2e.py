"""
test_monograph_derivation_walk_e2e.py — End-to-End Test for the Full Derivation Walk
Status: E2E Test Suite
AuthorityEffect: None

Tests the entire derivation trajectory:
1. Stage 0: Void <>
2. Stage 1: Lone Mark <a>
3. Stage 2: Unmarked Pair <ab>
4. Stage 3: Directed Cut <arb> (Fermion germ D2, rigid Aut = {id}, boundary b - a)
5. Stage 4: Refused Self-Loop <ara> (boundary a - a = 0)
6. Stage 5: Symmetric Link <a=b> (Boson germ S2, Aut = Z2)
7. Swap-invariant predicate blindness.
8. Stage 14: Discrete Fermionic Hamiltonian generation on lattices.
9. Hamiltonian GIN Bridge indexing and sign resolution:
   - Bipartite model: 100% paired -> uncancelled defect = 0.0 -> <Sign>_GIN = 1.0 -> TerminalRoute.Repair.
   - Frustrated triangle: disjoint weights -> unpartnered negatives -> <Sign>_GIN < 1.0 -> TerminalRoute.SplitBrainRefusal.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

current_dir = Path(__file__).resolve().parent
code_dir = current_dir.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from fermion_boson_germ import (
    GermState,
    DirectedCutD2,
    SymmetricLinkS2,
    verify_invariant_blindness,
)
from fermionic_hamiltonian import (
    FermionicLattice,
    DiscreteFermionicHamiltonian,
)
from hamiltonian_gin_bridge import HamiltonianGinBridge
from bqnf_sign_evaluator import (
    CochainComplex,
    BQNFSignEvaluator,
    TerminalRoute,
)


def test_monograph_full_derivation_walk_e2e():
    state = GermState()

    state.step_00_void()
    assert state.stage == 0
    assert len(state.carrier) == 0

    state.step_01_lone_mark("u")
    assert state.stage == 1
    assert state.carrier == {"u"}

    state.step_02_unmarked_pair("u", "v")
    assert state.stage == 2
    assert state.carrier == {"u", "v"}

    d2 = state.step_03_directed_cut("u", "v")
    assert d2.source == "u"
    assert d2.target == "v"
    assert d2.boundary_0chain == {"v": 1, "u": -1}
    assert len(d2.automorphism_group()) == 1

    refused, reason = state.step_04_refuse_self_loop("u")
    assert not refused
    assert "boundary a - a = 0" in reason

    s2 = state.step_05_symmetric_link("u", "v")
    assert len(s2.automorphism_group()) == 2

    blindness = verify_invariant_blindness(
        d2,
        [
            lambda p: set(p),
            lambda p: len(p),
            lambda p: p[0] == p[1],
        ]
    )
    assert all(blindness.values())

    bridge = HamiltonianGinBridge(in_memory=True)
    try:
        bip_lat = FermionicLattice.linear_chain(4, periodic=True)
        h_bip = DiscreteFermionicHamiltonian(bip_lat, t=1.0, u=0.0, num_up=2, num_down=0)

        res_bip = bridge.index_hamiltonian_paths(h_bip, beta=1.5, trotter_steps=4, model_name="E2E_Bipartite")
        assert res_bip["negative_paths"] == 32
        assert res_bip["matched_pairs"] == 32
        assert res_bip["unpartnered_negatives"] == 0
        assert res_bip["is_completely_paired"] is True

        audit_bip = bridge.audit_sign_resolution("E2E_Bipartite")
        assert audit_bip.all_exact_cancellations is True
        assert audit_bip.total_uncancelled_mass < 1e-12
        assert audit_bip.gin_quotiented_average_sign == 1.0
        assert audit_bip.terminal_route == "Repair"

        tri_lat = FermionicLattice.triangle_cluster()
        h_tri = DiscreteFermionicHamiltonian(tri_lat, t=1.0, u=0.0, num_up=2, num_down=0)

        res_tri = bridge.index_hamiltonian_paths(h_tri, beta=2.0, trotter_steps=3, model_name="E2E_Frustrated")
        assert res_tri["negative_paths"] == 6
        assert res_tri["matched_pairs"] == 0
        assert res_tri["unpartnered_negatives"] == 6
        assert res_tri["is_completely_paired"] is False

        audit_tri = bridge.audit_sign_resolution("E2E_Frustrated")
        assert audit_tri.all_exact_cancellations is False
        assert audit_tri.total_uncancelled_mass > 0.0
        assert audit_tri.gin_quotiented_average_sign < 1.0
        assert audit_tri.terminal_route == "SplitBrainRefusal"

        mzm = bridge.index_kitaev_chain_majorana(L=4, model_name="E2E_Kitaev")
        assert mzm.is_boundary_isolated is True
        assert set(mzm.unpaired_zero_modes) == {1, 8}
        assert mzm.mzm_status == "MZM_TOPOLOGICALLY_PROTECTED"

    finally:
        bridge.close()
